"""Persistent spend ledger with a hard cap, shared by every process in this checkout.

Every paid call (LLM or sandbox) is appended to `.gf_cache/spend.jsonl`.
Before an LLM call we add its *worst-case* cost (estimated prompt tokens x
input price + max_tokens x output price) to what has already been spent, and
refuse the call if that would cross GF_SPEND_CAP_USD. So the cap can't be
overrun by a single call, only approached.

Prices come from config.tiers() (live prices from /v1/models).

Billing as observed on 2026-10-08 (console vs ledger): Nemotron inference is billed;
Sandboxes are NOT billed during the Beta even though every run reports a `cost`. So the cap
GF_SPEND_CAP_USD covers billed kinds only (llm, reconcile), and reported sandbox cost has its
own guard, GF_SANDBOX_GUARD_USD, in case billing starts. Calls that fail after being sent are
recorded at their estimated input cost ("llm_unconfirmed"): the console showed ~10% more
inference than the ledger, most likely from billed calls that timed out client-side.
"""

from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path

from gapfinder.config import settings

DEFAULT_CAP_USD = 5.0
DEFAULT_SANDBOX_GUARD_USD = 60.0
BILLED_KINDS = {"llm", "llm_unconfirmed", "reconcile"}
_lock = threading.Lock()


class BudgetExceeded(RuntimeError):
    pass


def _path() -> Path:
    return settings().cache_dir / "spend.jsonl"


def cap_usd() -> float:
    return float(os.environ.get("GF_SPEND_CAP_USD", DEFAULT_CAP_USD))


def entries() -> list[dict]:
    """Every recorded entry. A line that doesn't parse (a write torn by a crash) is skipped, not fatal: one
    damaged line once crashed every running search (devbatch-1). Locked appends below keep new ones whole."""
    p = _path()
    if not p.exists():
        return []
    out = []
    for line in p.read_bytes().split(b"\n"):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


class _FileLock:
    """An exclusive OS lock on a file, across processes (several searches append to one ledger)."""

    def __init__(self, f):
        self.f = f

    def __enter__(self):
        if os.name == "nt":
            import msvcrt

            self.f.seek(0)
            while True:
                try:
                    msvcrt.locking(self.f.fileno(), msvcrt.LK_LOCK, 1)  # retries for about 10 s, then raises
                    break
                except OSError:
                    continue
        else:
            import fcntl

            fcntl.flock(self.f.fileno(), fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc):
        if os.name == "nt":
            import msvcrt

            self.f.seek(0)
            msvcrt.locking(self.f.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(self.f.fileno(), fcntl.LOCK_UN)


def spent_usd() -> float:
    """Money actually billed (inference), as far as the ledger knows."""
    return sum(e.get("cost_usd", 0.0) for e in entries() if e.get("kind") in BILLED_KINDS)


def sandbox_reported_usd() -> float:
    """What sandbox runs report as `cost` (not billed during the Beta)."""
    return sum(e.get("cost_usd", 0.0) for e in entries() if e.get("kind") == "sandbox")


def record(kind: str, cost_usd: float, **detail) -> None:
    if os.environ.get("GF_SPEND_TAG"):  # e.g. "ruskey": lets one project have its own cap
        detail.setdefault("tag", os.environ["GF_SPEND_TAG"])
    p = _path()
    p.parent.mkdir(parents=True, exist_ok=True)
    line = (json.dumps({"t": round(time.time(), 1), "kind": kind, "cost_usd": round(cost_usd, 8), **detail}) + "\n").encode()
    with _lock, (p.parent / (p.name + ".lock")).open("a+b") as lk, _FileLock(lk), p.open("ab") as f:
        f.write(line)  # one write of a whole line, under a lock other processes respect


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


def check(worst_case_usd: float, what: str, kind: str = "llm") -> None:
    if kind == "sandbox":
        guard = float(os.environ.get("GF_SANDBOX_GUARD_USD", DEFAULT_SANDBOX_GUARD_USD))
        if sandbox_reported_usd() + worst_case_usd > guard:
            raise BudgetExceeded(f"refusing {what}: sandbox runs have reported ${sandbox_reported_usd():.2f}, "
                                 f"over the ${guard:.2f} guard (GF_SANDBOX_GUARD_USD)")
        _check_tag(worst_case_usd, what)
        return
    spent, cap = spent_usd(), cap_usd()
    if spent + worst_case_usd > cap:
        raise BudgetExceeded(
            f"refusing {what}: spent ${spent:.4f} + worst case ${worst_case_usd:.4f} would exceed the "
            f"${cap:.2f} cap (GF_SPEND_CAP_USD). Raise the cap deliberately if this spend is intended."
        )
    _check_tag(worst_case_usd, what)


def _check_tag(worst_case_usd: float, what: str) -> None:
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
            "sandbox_reported_usd": round(sandbox_reported_usd(), 6),
            "by_kind": {k: round(v, 6) for k, v in sorted(by_kind.items())}}
