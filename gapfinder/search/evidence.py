"""Web evidence for candidate values (Tavily): GitHub issues, errata, the authors' other artifacts.

Used by the plausibility gate when a value fits the gap but neither the paper
nor the code mentions it. A web result counts as evidence only if the text
Tavily returned mentions both the value and the knob (or most of its name's
words). The quote is the sentence copied from that returned text, so it is
grounded by construction. Results are cached on disk: each query costs one
Tavily credit, once.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from gapfinder.config import settings
from gapfinder.ledger.schemas import Evidence

TAVILY_URL = "https://api.tavily.com/search"


GENERIC_VALUES = {"true", "false", "on", "off", "yes", "no", "none", "0", "1", "enabled", "disabled"}


def _knob_words(knob: str) -> list[str]:
    return [w for w in re.split(r"[^a-z0-9]+", knob.lower().lstrip("-")) if len(w) >= 3]


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]


def _word(w: str, text: str) -> bool:
    return re.search(rf"(?<![a-z0-9]){re.escape(w)}(?![a-z0-9])", text) is not None


def supporting_sentence(text: str, knob: str, value: str) -> str | None:
    """A sentence that mentions the value and the knob, if any.

    The knob counts if its exact name appears, or at least half of its name's words (3+ letters)
    appear as whole words. A generic value (true, on, 1, ...) only counts within 30 characters
    of the knob's exact name: "direct_io=true" yes, "create_if_missing=True" no.
    """
    name = knob.lower().lstrip("-")
    spaced = name.replace("_", " ").replace("-", " ")
    words = _knob_words(knob)
    v = str(value).lower()
    for sent in _sentences(text):
        low = sent.lower()
        if not re.search(rf"(?<![\w.]){re.escape(v)}(?!\w|\.\w)", low):
            continue
        exact = [m.start() for n in {name, spaced} for m in re.finditer(re.escape(n), low)]
        if v in GENERIC_VALUES:
            vpos = [m.start() for m in re.finditer(rf"(?<![\w.]){re.escape(v)}(?!\w|\.\w)", low)]
            if any(abs(a - b) <= 30 for a in exact for b in vpos):
                return sent[:400]
            continue
        if exact or (words and sum(_word(w, low) for w in words) * 2 >= len(words)):
            return sent[:400]
    return None


class EvidenceSearch:
    """`context` names the system (e.g. "RusKey RocksDB LSM-tree"); `transport` is injectable for tests."""

    def __init__(self, context: str, anchors: list[str] | None = None, api_key: str | None = None,
                 max_results: int = 5, transport=None, cache_dir: Path | None = None):
        """`anchors`: names one of which a source must mention (system or paper name) to count as
        evidence about *these authors'* setup rather than general practice."""
        self.context = context
        self.anchors = [a.lower() for a in (anchors or [])]
        self.api_key = api_key or os.environ.get("TAVILY_API_KEY")
        self.max_results = max_results
        self.cache_dir = cache_dir or settings().cache_dir / "tavily"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._injected = transport is not None
        self._transport = transport or self._http
        self.queries = 0  # credits actually spent this session

    @property
    def enabled(self) -> bool:
        return bool(self.api_key) or self._injected

    async def _http(self, payload: dict) -> dict:
        import httpx

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(TAVILY_URL, json=payload, headers={"Authorization": f"Bearer {self.api_key}"})
            r.raise_for_status()
            return r.json()

    async def search(self, query: str) -> list[dict]:
        key = hashlib.sha256(f"{query}|{self.max_results}".encode()).hexdigest()
        path = self.cache_dir / f"{key}.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        if os.environ.get("GF_CACHE_ONLY") == "1":
            return []
        data = await self._transport({"query": query, "max_results": self.max_results, "search_depth": "basic"})
        self.queries += 1
        results = [{"url": r.get("url", ""), "title": r.get("title", ""), "content": r.get("content", "")}
                   for r in data.get("results", [])]
        path.write_text(json.dumps(results), encoding="utf-8")
        return results

    async def find(self, knob: str, value: str) -> Evidence | None:
        if not self.enabled:
            return None
        query = f'{self.context} {knob.lstrip("-").replace("_", " ")} {value}'
        try:
            results = await self.search(query)
        except Exception:  # evidence search is best-effort; it never fails the run
            return None
        for r in results:
            blob = f"{r['title']} {r['content']} {r['url']}".lower()
            if self.anchors and not any(a in blob for a in self.anchors):
                continue  # about something else: general practice isn't evidence of what the authors did
            sent = supporting_sentence(r["content"], knob, value)
            if sent:
                return Evidence(kind="web", ref=r["url"], quote=sent)
        return None
