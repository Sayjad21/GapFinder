"""Tier routing for Nemotron on Token Factory: retries, caching, token accounting.

Two gotchas shape this module:

* Every Nemotron model on Token Factory is a reasoning model. The reasoning
  trace counts against max_tokens, so a small limit can leave `content` empty
  (nebius/api#211). We use generous limits, look for the answer in `content`,
  then fall back to text after a closing </think>, and never let an empty
  answer silently become `{}`.
* Context windows are not as large as some listings claim, so callers send a
  repo map plus the few files that matter, never a whole repo.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from gapfinder.config import ModelTier, settings, tiers
from gapfinder.models import budget

T = TypeVar("T", bound=BaseModel)

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)


class EmptyAnswerError(RuntimeError):
    """The model spent its whole budget reasoning and returned no answer."""


class BadJSONError(RuntimeError):
    pass


class CacheMiss(RuntimeError):
    """GF_CACHE_ONLY=1 and the answer isn't cached: refuse rather than spend."""


# ------------------------------------------------------------ response parsing


def split_reasoning(content: str | None, reasoning_field: str | None = None) -> tuple[str, str]:
    """Return (reasoning, answer) from a chat completion message.

    Handles three shapes: a separate reasoning field with a clean content;
    content wrapped as `<think>...</think>answer`; and content that is only an
    unterminated `<think>...` (budget exhausted -> empty answer).
    """
    content = content or ""
    reasoning = reasoning_field or ""
    if "<think>" in content.lower() or "</think>" in content.lower():
        thinks = re.findall(r"<think>(.*?)</think>", content, re.DOTALL | re.IGNORECASE)
        reasoning = (reasoning + "\n" + "\n".join(thinks)).strip()
        answer = _THINK_RE.sub("", content)
        if "</think>" in answer.lower():  # closing tag without an opening one
            pre, _, answer = re.split(r"(</think>)", answer, maxsplit=1, flags=re.IGNORECASE)
            reasoning = (reasoning + "\n" + pre).strip()
        if re.search(r"<think>", answer, re.IGNORECASE):  # unterminated: all reasoning
            idx = re.search(r"<think>", answer, re.IGNORECASE).start()
            reasoning = (reasoning + "\n" + answer[idx:]).strip()
            answer = answer[:idx]
        content = answer
    return reasoning, content.strip()


def extract_json(answer: str) -> Any:
    """Parse the JSON payload of an answer, tolerating fences and leading prose."""
    if not answer.strip():
        raise EmptyAnswerError("empty answer")
    candidates = [answer.strip()]
    candidates += [m.strip() for m in _FENCE_RE.findall(answer)]
    for opener, closer in (("{", "}"), ("[", "]")):
        start, end = answer.find(opener), answer.rfind(closer)
        if start != -1 and end > start:
            candidates.append(answer[start : end + 1])
    for cand in candidates:
        try:
            return json.loads(cand)
        except json.JSONDecodeError:
            continue
    raise BadJSONError(f"no JSON object in answer: {answer[:200]!r}")


# ---------------------------------------------------------------------- cache


class ResponseCache:
    """On-disk cache keyed on hash(model, messages, schema). Makes tests deterministic."""

    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def key(model: str, messages: list[dict], schema: dict | None, extra: dict | None = None) -> str:
        blob = json.dumps({"m": model, "msg": messages, "s": schema, "x": extra or {}}, sort_keys=True)
        return hashlib.sha256(blob.encode()).hexdigest()

    def get(self, key: str) -> dict | None:
        path = self.root / key[:2] / f"{key}.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    def put(self, key: str, value: dict) -> None:
        path = self.root / key[:2] / f"{key}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")


# ----------------------------------------------------------- token accounting


@dataclass
class Usage:
    calls: int = 0
    cached_calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    reasoning_tokens: int = 0
    seconds: float = 0.0
    cached_prompt_tokens: int = 0  # tokens a cache hit would have cost on a fresh run
    cached_completion_tokens: int = 0

    def cost(self, tier: ModelTier) -> float:
        return (self.prompt_tokens * tier.price_in + self.completion_tokens * tier.price_out) / 1e6

    def fresh_cost(self, tier: ModelTier) -> float:
        """What these calls cost without the cache: the fair number for comparing methods."""
        return self.cost(tier) + (self.cached_prompt_tokens * tier.price_in
                                  + self.cached_completion_tokens * tier.price_out) / 1e6


@dataclass
class TokenMeter:
    by_tier: dict[str, Usage] = field(default_factory=dict)

    def record(self, tier: str, usage: dict, seconds: float, cached: bool) -> None:
        u = self.by_tier.setdefault(tier, Usage())
        u.calls += 1
        if cached:  # paid nothing now, but record what a fresh run would cost
            u.cached_calls += 1
            u.cached_prompt_tokens += usage.get("prompt_tokens", 0) or 0
            u.cached_completion_tokens += usage.get("completion_tokens", 0) or 0
            return
        u.prompt_tokens += usage.get("prompt_tokens", 0) or 0
        u.completion_tokens += usage.get("completion_tokens", 0) or 0
        details = usage.get("completion_tokens_details") or {}
        u.reasoning_tokens += details.get("reasoning_tokens", 0) or 0
        u.seconds += seconds

    def summary(self) -> dict[str, dict]:
        t = tiers()
        return {
            name: {**u.__dict__, "cost_usd": round(u.cost(t[name]), 6)} for name, u in self.by_tier.items()
        }

    def total_cost(self) -> float:
        t = tiers()
        return sum(u.cost(t[name]) for name, u in self.by_tier.items())

    def total_fresh_cost(self) -> float:
        t = tiers()
        return sum(u.fresh_cost(t[name]) for name, u in self.by_tier.items())


# --------------------------------------------------------------------- router


class Router:
    """Calls a Nemotron tier and returns validated pydantic objects.

    `transport` is injectable so unit tests can run without a network: it takes
    (model_id, messages, max_tokens, response_format) and returns a dict shaped
    like an OpenAI chat completion (`choices[0].message`, `usage`).
    """

    def __init__(self, transport=None, cache: ResponseCache | None = None, use_cache: bool = True):
        s = settings()
        self.tiers = tiers()
        self.cache = cache or ResponseCache(s.cache_dir / "llm")
        self.use_cache = use_cache
        self.meter = TokenMeter()
        self._transport = transport or self._openai_transport()

    @staticmethod
    def _openai_transport():
        from openai import AsyncOpenAI

        s = settings()
        client = None

        async def call(model: str, messages: list[dict], max_tokens: int, response_format: dict | None) -> dict:
            nonlocal client
            if client is None:
                if not s.token_factory_api_key:
                    raise RuntimeError(f"no API key for LLM provider {s.llm_provider!r} (see .env.example)")
                client = AsyncOpenAI(base_url=s.token_factory_base_url, api_key=s.token_factory_api_key)
            kwargs: dict[str, Any] = {"model": model, "messages": messages, "max_tokens": max_tokens}
            if response_format:
                kwargs["response_format"] = response_format
            resp = await client.chat.completions.create(**kwargs)
            return resp.model_dump()

        return call

    async def complete(
        self, tier: str, messages: list[dict], *, schema: dict | None = None, max_tokens: int | None = None
    ) -> tuple[str, str, dict]:
        """Return (reasoning, answer, raw). Retries transient errors; caches answers."""
        t = self.tiers[tier]
        max_tokens = max_tokens or t.max_tokens
        response_format = (
            {"type": "json_schema", "json_schema": {"name": "out", "schema": schema}} if schema else None
        )
        key = ResponseCache.key(t.model_id, messages, schema,
                                {"max_tokens": max_tokens, "provider": settings().llm_provider})
        if self.use_cache and (hit := self.cache.get(key)):
            self.meter.record(tier, hit.get("usage") or {}, 0.0, cached=True)
            return hit["reasoning"], hit["answer"], hit
        if os.environ.get("GF_CACHE_ONLY") == "1":
            raise CacheMiss(f"{tier}: not in cache and GF_CACHE_ONLY=1, so no paid call was made")

        last_exc: Exception | None = None
        doubled = False
        prompt_est = budget.estimate_prompt_tokens(messages)
        for attempt in range(4):
            budget.check((prompt_est * t.price_in + max_tokens * t.price_out) / 1e6, f"{tier} call")
            start = time.monotonic()
            try:
                raw = await self._transport(t.model_id, messages, max_tokens, response_format)
            except Exception as exc:  # network / 429 / 5xx
                if _is_schema_rejection(exc) and response_format is not None:
                    response_format = {"type": "json_object"}  # endpoint lacks json_schema support
                    continue
                if _is_fatal(exc):  # bad key, no funds, unknown model: retrying won't help
                    raise
                # the request may have been processed and billed even though no answer came back
                budget.record("llm_unconfirmed", prompt_est * t.price_in / 1e6, tier=tier, model=t.model_id,
                              error=type(exc).__name__)
                last_exc = exc
                await asyncio.sleep(min(2**attempt, 20))
                continue
            msg = raw["choices"][0]["message"]
            reasoning, answer = split_reasoning(msg.get("content"), msg.get("reasoning_content"))
            usage = raw.get("usage") or {}
            self.meter.record(tier, usage, time.monotonic() - start, cached=False)
            budget.record("llm", _usage_cost(usage, t), tier=tier, model=t.model_id,
                          prompt_tokens=usage.get("prompt_tokens"), completion_tokens=usage.get("completion_tokens"))
            if not answer:
                # Budget eaten by reasoning: double the limit once, then give up.
                last_exc = EmptyAnswerError(f"{tier}: empty content at max_tokens={max_tokens}")
                if doubled:
                    break
                max_tokens, doubled = max_tokens * 2, True
                continue
            record = {"reasoning": reasoning, "answer": answer, "usage": usage, "model": t.model_id}
            if self.use_cache:
                self.cache.put(key, record)
            return reasoning, answer, record
        raise last_exc or RuntimeError("model call failed")

    async def structured(
        self, tier: str, messages: list[dict], model: type[T], *, max_tokens: int | None = None
    ) -> T:
        """Call a tier and validate its JSON answer as `model`; one repair round on failure."""
        schema = model.model_json_schema()
        sys_hint = {
            "role": "system",
            "content": "Answer with a single JSON object that validates against this JSON schema. "
            "No prose outside the JSON.\n" + json.dumps(schema),
        }
        msgs = [sys_hint, *messages]
        _, answer, _ = await self.complete(tier, msgs, schema=schema, max_tokens=max_tokens)
        try:
            return model.model_validate(extract_json(answer))
        except (BadJSONError, ValidationError) as err:
            repair = msgs + [
                {"role": "assistant", "content": answer},
                {"role": "user", "content": f"That did not validate: {str(err)[:1500]}\nReturn corrected JSON only."},
            ]
            _, answer, _ = await self.complete(tier, repair, schema=schema, max_tokens=max_tokens)
            return model.model_validate(extract_json(answer))


def _usage_cost(usage: dict, tier: ModelTier) -> float:
    return ((usage.get("prompt_tokens") or 0) * tier.price_in + (usage.get("completion_tokens") or 0) * tier.price_out) / 1e6


def _is_fatal(exc: Exception) -> bool:
    if isinstance(exc, budget.BudgetExceeded):
        return True
    status = getattr(exc, "status_code", None)
    return status in (400, 401, 402, 403, 404) and not _is_schema_rejection(exc)


def _is_schema_rejection(exc: Exception) -> bool:
    text = str(exc).lower()
    return "response_format" in text or "json_schema" in text
