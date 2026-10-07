"""Persistent spend ledger with a hard cap, shared by every process in this checkout.

Every paid call (LLM or sandbox) is appended to `.gf_cache/spend.jsonl`.
Before an LLM call we add its *worst-case* cost (estimated prompt tokens x
input price + max_tokens x output price) to what has already been spent, and
refuse the call if that would cross GF_SPEND_CAP_USD. So the cap can't be
overrun by a single call, only approached.

Prices come from config.tiers(). They're list prices from the plan; check the
ledger total against the console balance after the first real run.
"""

from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path

from gapfinder.config import settings

DEFAULT_CAP_USD = 5.0
_lock = threading.Lock()


class BudgetExceeded(RuntimeError):
    pass


def _path() -> Path:
    return settings().cache_dir / "spend.jsonl"


def cap_usd() -> float:
    return float(os.environ.get("GF_SPEND_CAP_USD", DEFAULT_CAP_USD))


def entries() -> list[dict]:
    p = _path()
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def spent_usd() -> float:
    return sum(e.get("cost_usd", 0.0) for e in entries())


def record(kind: str, cost_usd: float, **detail) -> None:
    if os.environ.get("GF_SPEND_TAG"):  # e.g. "ruskey": lets one project have its own cap
        detail.setdefault("tag", os.environ["GF_SPEND_TAG"])
    p = _path()
    p.parent.mkdir(parents=True, exist_ok=True)
    with _lock, p.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"t": round(time.time(), 1), "kind": kind, "cost_usd": round(cost_usd, 8), **detail}) + "\n")


def estimate_prompt_tokens(messages: list[dict]) -> int:
    """Deliberately high: ~3 chars/token (English averages ~4); images count as 1500."""
    chars, images = 0, 0
    for m in messages:
        c = m.get("content")
        if isinstance(c, str):
            chars += len(c)
        elif isinstance(c, list):
            for part in c:
                if part.get("type") == "text":
                    chars += len(part.get("text", ""))
                else:
                    images += 1
    return chars // 3 + 1500 * images + 50


def tag_spent_usd(tag: str) -> float:
    return sum(e.get("cost_usd", 0.0) for e in entries() if e.get("tag") == tag)


def check(worst_case_usd: float, what: str) -> None:
    spent, cap = spent_usd(), cap_usd()
    if spent + worst_case_usd > cap:
        raise BudgetExceeded(
            f"refusing {what}: spent ${spent:.4f} + worst case ${worst_case_usd:.4f} would exceed the "
            f"${cap:.2f} cap (GF_SPEND_CAP_USD). Raise the cap deliberately if this spend is intended."
        )
    tag, tag_cap = os.environ.get("GF_SPEND_TAG"), os.environ.get("GF_TAG_CAP_USD")
    if tag and tag_cap and tag_spent_usd(tag) + worst_case_usd > float(tag_cap):
        raise BudgetExceeded(
            f"refusing {what}: {tag!r} has spent ${tag_spent_usd(tag):.4f} of its ${float(tag_cap):.2f} "
            f"budget (GF_TAG_CAP_USD)")


def summary() -> dict:
    by_kind: dict[str, float] = {}
    for e in entries():
        k = f"{e['kind']}:{e.get('tier', '')}".rstrip(":")
        by_kind[k] = by_kind.get(k, 0.0) + e.get("cost_usd", 0.0)
    return {"spent_usd": round(spent_usd(), 6), "cap_usd": cap_usd(),
            "by_kind": {k: round(v, 6) for k, v in sorted(by_kind.items())}}
