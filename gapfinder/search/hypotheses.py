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
# value coverage: coarse first (x10 leads, so an order-of-magnitude error is reached at once), then the
# common x2 and x5 before the far x50 and x100. v1.1 had (10, 2, 50, 5, 100), which pushed x5 past the
# 6-value cap (test-v11-05: epochs 15 -> 75 never tested)
LADDER = (10, 2, 5, 50, 100)
# knobs whose default lies in (0, 1) but which are not fractions: values above 1 are meaningful, and the
# fraction ladder's complement steps (1 - (1 - d)/k) are not (test-v11-04: lr 0.1 -> 0.91 won a run)
_UNBOUNDED_NAME = re.compile(r"(?:^|_)(?:lr|eta|learning|step_size|temperature|temp|tau|length_?scale|"
                             r"weight_decay|wd|l1|l2|lambda|reg|sigma|std|scale|clip|margin|init)(?:$|_)", re.I)
# a multiplier knob's natural values are the factors a paper states ("10x more iterations")
MULTIPLIER_FACTORS = ("1", "2", "5", "10", "100")
_MULT_NAME = re.compile(r"(?:_|^)(?:mult|multiplier|scale|factor|times)$|^[a-z]{3,}x$", re.I)
_MULT_HELP = re.compile(r"multipl|\bfactor\b|\bscal(?:e|ing)\b|\btimes\b", re.I)
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


def coverage_values(knob, name: str = "") -> list[str]:
    """Values a knob can take that a reader of the paper may never propose: every accepted choice of a
    categorical flag, or a coarse-first log ladder around a numeric default. `name` (the knob's name)
    tells a fraction (a discount, a probability, a split) from a small unbounded number (a learning rate)."""
    if knob.choices:
        return [c for c in knob.choices if c != knob.default]
    d = knob.default.strip()
    if knob.role:  # a traced role (gapfinder/search/trace.py) beats the name rules below
        if (vals := role_values(knob.role, d)) is not None:
            return vals
    if knob.multiplier:
        out = [f for f in MULTIPLIER_FACTORS if not _same_number(f, d)]
        return out + [v for v in generate_values(d, LADDER) if not any(_same_number(v, f) for f in out)]
    if re.fullmatch(r"\d+", d) and int(d) >= 2:  # an integer knob's boundary value 1 (one layer, one thread)
        ladder = generate_values(d, LADDER)
        return ladder[:2] + ["1"] + [v for v in ladder[2:] if v != "1"]
    if _NUM.fullmatch(d) and 0 < float(d) < 1 and "." in d and not _UNBOUNDED_NAME.search(name.lstrip("-")):
        return _with_zero(fraction_values(float(d)))
    vals = generate_values(knob.default, LADDER)
    if "." in d and _NUM.fullmatch(d) and float(d) > 0:  # a float knob's boundary value 0 (no exploration, no noise)
        return _with_zero(vals)
    return vals


def role_values(role: str, d: str) -> list[str] | None:
    """Candidate values from a traced role; None when the role says nothing for this default (e.g. text)."""
    if role == "seed":
        return []  # a seed is noise, not a cause
    if not _NUM.fullmatch(d):
        return None
    x = float(d)
    if role == "fraction" and 0 <= x < 1:
        return _with_zero(fraction_values(x)) if x > 0 else ["0.1", "0.5", "0.25", "0.05", "0.75", "0.9"]
    if role == "rate" and x > 0:
        return generate_values(d, LADDER)  # log scale, above 1 allowed, never 0
    if role == "rate0":
        return _with_zero(generate_values(d, LADDER)) if x > 0 else ["1e-4", "1e-3", "1e-5", "1e-2", "1e-6"]
    if role == "size" and re.fullmatch(r"\d+", d) and int(d) >= 1:
        return patch_values("size", d)
    if role == "count" and re.fullmatch(r"\d+", d) and int(d) >= 1:
        ladder = generate_values(d, LADDER)
        return ladder[:2] + (["1"] if int(d) >= 2 else []) + [v for v in ladder[2:] if v != "1"]
    if role == "multiplier":
        out = [f for f in MULTIPLIER_FACTORS if not _same_number(f, d)]
        return out + [v for v in generate_values(d, LADDER) if not any(_same_number(v, f) for f in out)]
    return None


_SIZE_NAME = re.compile(r"batch|size|hidden|units|width|dim|channels|heads|layers|_n$|^n_", re.I)


def patch_values(name: str, literal: str) -> list[str]:
    """Candidate values for a patch knob (a hard-coded literal): powers of two first for size-like integer
    names (batch_size 128 -> 64, 256, 32, 512, ...; papers state batch sizes as powers of two), then the
    coverage ladder."""
    from gapfinder.sandbox.spec import Knob

    d = literal.strip()
    if d in ("True", "False"):  # a switch has one other value
        return ["False" if d == "True" else "True"]
    out: list[str] = []
    if re.fullmatch(r"\d+", d) and int(d) >= 2 and _SIZE_NAME.search(name):
        x = int(d)
        for f in (2, 4, 8, 16):
            for v in (x // f, x * f):
                if v >= 1 and str(v) != d and str(v) not in out:
                    out.append(str(v))
    for v in coverage_values(Knob(layer="environment", default=d), name):
        if v not in out and v != d and not _same_number(v, d):
            out.append(v)
    return out


def _with_zero(vals: list[str]) -> list[str]:
    """Insert the boundary value 0.0 after the two coarsest candidates."""
    return vals[:2] + ["0.0"] + [v for v in vals[2:] if not _same_number(v, "0")]


def fraction_values(x: float) -> list[str]:
    """A default strictly between 0 and 1 is usually a fraction, probability or rate, so values above it
    approach 1 instead of overshooting it: 0.5 gives 0.05, 0.95, 0.25, 0.75, 0.01, 0.99, ..."""
    out: list[str] = []
    for f in LADDER:
        for v in (x / f, 1 - (1 - x) / f):
            s = _fmt(v)
            if 0 < v < 1 and s not in out and float(s) != x:
                out.append(s)
    return out


_COUNT_LIKE = re.compile(r"epoch|iter|step|size|count|num|len|rounds|^n_|_n$|^n$", re.I)


def mark_multipliers_from_flow(spec: HarnessSpec, scales: dict[str, list[str]]) -> int:
    """A whole-number knob that the code multiplies a count-like quantity by (epochs, iterations, steps,
    sizes) is a multiplier; record what it scales. Plain arithmetic such as lr x gradient doesn't count."""
    n = 0
    for name, k in spec.knobs.items():
        targets = scales.get(name.lstrip("-").replace("-", "_"), [])
        if not targets:
            continue
        k.scales = list(targets)
        if not k.multiplier and not k.choices and re.fullmatch(r"\d+", k.default.strip())                 and any(_COUNT_LIKE.search(t) for t in targets):
            k.multiplier = True
            n += 1
    return n


def is_multiplier(name: str, help_text: str = "") -> bool:
    return bool(_MULT_NAME.search(name.lstrip("-")) or _MULT_HELP.search(help_text or ""))


def fill_choices(spec: HarnessSpec, flags) -> int:
    """Copy argparse `choices` from the repo map into spec knobs that don't list them, and mark knobs
    whose name or help text says they multiply something. Returns how many knobs changed."""
    by_name, text = {}, {}
    for f in flags:
        key = f.name.lstrip("-").replace("-", "_").lower()
        text.setdefault(key, getattr(f, "text", ""))
        if getattr(f, "choices", None):
            by_name.setdefault(key, f.choices)
    n = 0
    for name, k in spec.knobs.items():
        key = name.lstrip("-").replace("-", "_").lower()
        ch = by_name.get(key)
        changed = False
        if ch and not k.choices:
            k.choices, changed = list(ch), True
        if not k.multiplier and not k.choices and is_multiplier(name, text.get(key, "")):
            k.multiplier, changed = True, True
        n += changed
    return n


def knob_candidates(spec: HarnessSpec, knob: str) -> list[str]:
    k = spec.knobs[knob]
    out = [c for c in k.candidates if c != k.default]
    # a categorical knob's other choices (planted SparseTSF: `loss` in {mse, mae} had no candidate values in repo-map
    # mode, so loss=mae was never run; lradj and embed likewise)
    out += [c for c in k.choices if c != k.default and c not in out]
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
