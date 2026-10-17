"""Append-only JSONL event log. The live UI and replay mode both read this file.

Event types: checkpoint, branch_created, branch_started, branch_finished,
metrics, pruned, survivor, verified, noise_band, cost, note.
"""

from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from typing import Any, Iterator

EVENT_TYPES = {
    "run_started",
    "trace",  # the dry-run sink trace (gapfinder/search/trace.py)
    "checkpoint",
    "branch_created",
    "branch_started",
    "branch_finished",
    "metrics",
    "pruned",
    "survivor",
    "verified",
    "noise_band",
    "cost",
    "note",
    "round",
    "attribution",
    "run_finished",
}


class EventLog:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._seq = sum(1 for _ in self.read()) if self.path.exists() else 0
        self._subscribers: list = []

    def emit(self, type: str, **data: Any) -> dict:
        if type not in EVENT_TYPES:
            raise ValueError(f"unknown event type {type}")
        with self._lock:
            self._seq += 1
            ev = {"seq": self._seq, "t": round(time.time(), 3), "type": type, **data}
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(ev, default=str) + "\n")
        for cb in list(self._subscribers):
            cb(ev)
        return ev

    def subscribe(self, cb) -> None:
        self._subscribers.append(cb)

    def read(self) -> Iterator[dict]:
        if not self.path.exists():
            return
        with self.path.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)
