"""Hypotheses without the ledger: every knob of the harness spec, each with candidate values.

The harness spec's knobs are the repo map's flags (the spec exposes every flag it found). This builds an
assumption list from them with no paper evidence and no ranking: uniform priors, status "unstated",
paper value "unstated". With `gapfinder search --hypotheses repomap --rank random` it is the random-search
arm over all flags (P1-1): the ledger contributes nothing, neither its ranking nor its evidence.

Candidate values per knob, in this order:
1. the spec's own `candidates`, if it lists any;
2. numbers: the default divided and multiplied by 2, 5 and 10, interleaved (/2, x2, /5, x5, /10, x10);
   integers stay integers and must stay at least 1 (when the default is at least 1);
3. on/off style booleans: the opposite value.
A knob with none of these (a text or list default and no spec candidates, or a default of 0) has no
candidate values and is left out; `assumptions_from_spec` returns which ones.
"""

from __future__ import annotations

import re

from gapfinder.ledger.schemas import Assumption
from gapfinder.sandbox.spec import HarnessSpec

FACTORS = (2, 5, 10)
# v1.1 value coverage: coarse first, so the span is covered before the resolution (a 50x change, e.g.
# MC Dropout's epochx 500 -> 10, is reached within the first few candidates)
LADDER = (10, 2, 50, 5, 100)
_FLIP = {"true": "false", "false": "true", "on": "off", "off": "on", "yes": "no", "no": "yes",
         "enabled": "disabled", "disabled": "enabled"}
_NUM = re.compile(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")


def _fmt(x: float) -> str:
    return f"{x:.6g}"


def generate_values(default: str, factors: tuple[int, ...] = FACTORS) -> list[str]:
    """Values around `default`: each factor below and above for numbers (in the given order), the flip
    for booleans."""
    d = default.strip()
    if d.lower() in _FLIP:
        flipped = _FLIP[d.lower()]
        return [flipped.capitalize() if d[:1].isupper() else flipped]
    if not _NUM.fullmatch(d):
        return []
    x = float(d)
    if x == 0:
        return []
    is_int = re.fullmatch(r"[-+]?\d+", d) is not None
    out: list[str] = []
    for f in factors:
        for v in (x / f, x * f):
            if is_int:
                v = int(v + 0.5) if v > 0 else -int(-v + 0.5)
                if x >= 1 and v < 1:
                    continue
                s = str(v)
            else:
                s = _fmt(v)
            if s != d and s not in out and float(s) != x:
                out.append(s)
    return out


def coverage_values(knob) -> list[str]:
    """Values a knob can take that a reader of the paper may never propose: every accepted choice of a
    categorical flag, or a coarse-first log ladder around a numeric default."""
    if knob.choices:
        return [c for c in knob.choices if c != knob.default]
    return generate_values(knob.default, LADDER)


def fill_choices(spec: HarnessSpec, flags) -> int:
    """Copy argparse `choices` from the repo map into spec knobs that don't list them. Returns how many."""
    by_name = {}
    for f in flags:
        if getattr(f, "choices", None):
            by_name.setdefault(f.name.lstrip("-").replace("-", "_").lower(), f.choices)
    n = 0
    for name, k in spec.knobs.items():
        ch = by_name.get(name.lstrip("-").replace("-", "_").lower())
        if ch and not k.choices:
            k.choices = list(ch)
            n += 1
    return n


def knob_candidates(spec: HarnessSpec, knob: str) -> list[str]:
    k = spec.knobs[knob]
    out = [c for c in k.candidates if c != k.default]
    for v in generate_values(k.default):
        if v not in out and not any(_same_number(v, c) for c in out):
            out.append(v)
    return out


def _same_number(a: str, b: str) -> bool:
    """'2' and '2.0' are one value."""
    return bool(_NUM.fullmatch(a.strip()) and _NUM.fullmatch(b.strip())) and float(a) == float(b)


def assumptions_from_spec(spec: HarnessSpec) -> tuple[list[Assumption], list[str]]:
    """(assumptions, knobs left out for lack of candidate values), in the spec's knob order."""
    out, skipped = [], []
    for knob, k in spec.knobs.items():
        values = knob_candidates(spec, knob)
        if not values:
            skipped.append(knob)
            continue
        out.append(Assumption(id=f"R{len(out) + 1}", knob=knob, layer=k.layer, paper_value="unstated",
                              code_default=k.default, candidate_values=values, evidence=[], prior_score=0.5,
                              status="unstated", affects_claims=[]))
    return out, skipped
