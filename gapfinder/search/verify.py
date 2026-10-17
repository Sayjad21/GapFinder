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
    partial: bool = False  # supported in direction only: moves toward the paper's value, which wasn't tested
    source: str = ""  # where the support came from: "paper", "docs", "code" or "web" (empty when unsupported)


_CHOICES = re.compile(r"choices\s*=\s*[\[(][^\])]*[\])]")


_DOC = re.compile(r"(?:^|/)(?:readme[^/]*|docs?/.*|[^/]*\.(?:md|rst|txt))$", re.I)


def _source(ev) -> str:
    """'docs' for a repo file the authors wrote as prose (README, docs/, .md/.rst/.txt): it says how they ran
    things. 'code' for source and config files: a default or a script line says what the code does, which a
    dataset's config may override (blind-2: argparse `--mask_rate 0.5`, overridden to 0.75 for COLLAB)."""
    if ev.kind != "code":
        return ev.kind
    path = str(ev.ref).split(":")[0].replace("\\", "/")
    return "docs" if _DOC.search(path) else "code"


def _norm(v: str) -> str:
    return str(v).strip().lower().strip("\"'")


def _num(v) -> float | None:
    try:
        return float(str(v).strip().replace(",", "").replace("_", ""))
    except (TypeError, ValueError):
        return None


def plausible(assumption: Assumption | None, value: str, naive: str | None = None) -> Plausibility:
    """Is `value` backed by evidence, or just the number that happens to fit?

    Supported when the paper states that value, or when the value appears in
    an evidence quote (paper, code, web) attached to the assumption.
    """
    if assumption is None:
        return Plausibility(False, "no assumption record for this knob, so no evidence")
    v = _norm(value)
    paper = _norm(assumption.paper_value)
    if not paper.startswith("unstated") and re.search(rf"(?<![\w.]){re.escape(v)}(?!\w|\.\w)", paper):
        return Plausibility(True, f"paper states {assumption.paper_value!r}", source="paper")
    for ev in assumption.evidence:
        # an options list (argparse choices=[...]) says what the code allows, not what the authors used
        quote = _CHOICES.sub(" ", ev.quote.lower())
        if re.search(rf"(?<![\w.]){re.escape(v)}(?!\w|\.\w)", quote):
            return Plausibility(True, f"{ev.kind} evidence at {ev.ref}: {ev.quote[:120]!r}", source=_source(ev))
    p, n, x = _num(assumption.paper_value), _num(naive), _num(value)
    if None not in (p, n, x) and p != n and min(n, p) < x < max(n, p):
        # e.g. the paper states 100M keys, the reproduction ran 500K, and 2M was tested
        return Plausibility(True, f"moves from the naive {naive} toward the paper's stated {assumption.paper_value}; "
                                  "the stated value itself was not tested", partial=True, source="paper")
    return Plausibility(False, f"no evidence mentions {value!r}; it fits, but nothing says the authors used it")


def held_out_ok(gap_before: float, gap_after: float, band: float) -> bool:
    """A held-out claim must not get worse by more than its noise band."""
    return abs(gap_after) <= abs(gap_before) + band


def gap_returns(gap_with: float, gap_without: float, band: float) -> bool:
    """Counterfactual: reverting a knob must reopen the gap by more than noise."""
    return abs(gap_without) - abs(gap_with) > band
