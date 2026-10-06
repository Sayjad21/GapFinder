"""Minimal explaining set: delta debugging over experimental conditions.

Given a set of knob changes that closes a gap, find a 1-minimal subset that
still closes it: removing any single remaining knob reopens the gap. This is
where the "git bisect" name comes from, applied to conditions instead of commits.
"""

from __future__ import annotations

from typing import Awaitable, Callable

Changes = dict[str, str]


async def minimal_set(changes: Changes, closes: Callable[[Changes], Awaitable[bool]]) -> Changes:
    """One-at-a-time reduction. `closes(subset)` runs the subset and reports whether the gap stays closed.

    Knobs are tried in sorted order so the result (and the runs it costs) is deterministic.
    Cost: at most len(changes) evaluations.
    """
    current = dict(changes)
    for knob in sorted(changes):
        if len(current) == 1:
            break
        trial = {k: v for k, v in current.items() if k != knob}
        if await closes(trial):
            current = trial  # knob wasn't needed
    return current
