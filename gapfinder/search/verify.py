"""Checks that stop GapFinder from fooling itself.

A setting that makes the number match is easy to find. Calling it the reason
needs evidence: the value must be backed by a source (plausibility), removing
it must bring the gap back (counterfactual), and it must not make other
claims worse (held-out). This module holds the pure parts of those checks.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from gapfinder.ledger.schemas import Assumption


@dataclass
class Plausibility:
    supported: bool
    reason: str


_CHOICES = re.compile(r"choices\s*=\s*[\[(][^\])]*[\])]")


def _norm(v: str) -> str:
    return str(v).strip().lower().strip("\"'")


def plausible(assumption: Assumption | None, value: str) -> Plausibility:
    """Is `value` backed by evidence, or just the number that happens to fit?

    Supported when the paper states that value, or when the value appears in
    an evidence quote (paper, code, web) attached to the assumption.
    """
    if assumption is None:
        return Plausibility(False, "no assumption record for this knob, so no evidence")
    v = _norm(value)
    paper = _norm(assumption.paper_value)
    if not paper.startswith("unstated") and re.search(rf"(?<![\w.]){re.escape(v)}(?!\w|\.\w)", paper):
        return Plausibility(True, f"paper states {assumption.paper_value!r}")
    for ev in assumption.evidence:
        # an options list (argparse choices=[...]) says what the code allows, not what the authors used
        quote = _CHOICES.sub(" ", ev.quote.lower())
        if re.search(rf"(?<![\w.]){re.escape(v)}(?!\w|\.\w)", quote):
            return Plausibility(True, f"{ev.kind} evidence at {ev.ref}: {ev.quote[:120]!r}")
    return Plausibility(False, f"no evidence mentions {value!r}; it fits, but nothing says the authors used it")


def held_out_ok(gap_before: float, gap_after: float, band: float) -> bool:
    """A held-out claim must not get worse by more than its noise band."""
    return abs(gap_after) <= abs(gap_before) + band


def gap_returns(gap_with: float, gap_without: float, band: float) -> bool:
    """Counterfactual: reverting a knob must reopen the gap by more than noise."""
    return abs(gap_without) - abs(gap_with) > band
