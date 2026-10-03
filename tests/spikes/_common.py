"""Shared helpers for the M0 spikes. Each spike writes eval/results/spikes/<name>.json."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
OUT = ROOT / "eval" / "results" / "spikes"


def need(*names: str) -> None:
    import gapfinder.config  # noqa: F401  (loads .env)

    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        print(f"SKIP: set {', '.join(missing)} (see .env.example)")
        raise SystemExit(2)


def save(name: str, result: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    result = {"spike": name, "recorded": time.strftime("%Y-%m-%dT%H:%M:%S%z"), **result}
    path = OUT / f"{name}.json"
    path.write_text(json.dumps(result, indent=2, default=str))
    verdict = "PASS" if result.get("pass") else "FAIL"
    print(f"{name}: {verdict} -> {path}")


class Check:
    def __init__(self):
        self.items: dict[str, dict] = {}

    def __call__(self, name: str, ok: bool, **detail) -> bool:
        self.items[name] = {"ok": bool(ok), **detail}
        print(f"  [{'ok' if ok else 'FAIL'}] {name} {detail if detail else ''}")
        return ok

    @property
    def all_ok(self) -> bool:
        return all(v["ok"] for v in self.items.values())
