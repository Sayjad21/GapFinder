"""Paper-versus-code constant matcher: deterministic, no model call, no runs.

For each setting the paper states (a ledger assumption with a value and a verbatim quote) whose name matches
no harness knob, look for a named literal in the code with the same core words; a literal whose value differs
from the paper's is a lead for the patch round, carrying the paper's value and quote. It is the $0 companion of
the contrast call (search/contrast.py): the same output format, found by name and value instead of by reading.

A lead is a place to test, not a finding: the patch round runs it, and only a measured fit is reported.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

from gapfinder.ledger.schemas import Assumption


def _number(v: str) -> tuple[float, bool] | None:
    """The number in a stated value and whether it was a percentage ('10%', '0.5', '1e-3', '200 epochs')."""
    from gapfinder.ledger.assumptions import _value

    s = str(v).strip()
    pct = "%" in s or "percent" in s.lower()
    m = re.search(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", s.replace(",", ""))
    parsed = _value(s.replace("%", "")) if not pct else None
    if isinstance(parsed, float):
        return parsed, False
    if m is None:
        return None
    return float(m.group(0)), pct


def _close(a: float, b: float) -> bool:
    return abs(a - b) <= 1e-9 + 1e-6 * max(abs(a), abs(b))


def _strip(name: str) -> str:
    name = re.sub(r"\s*\(.*$", "", name.strip())
    return re.sub(r"^(?:[A-Za-z_]\w*\.)+", "", name).strip().replace(" ", "_")


def _paper_quote(a: Assumption, number: float) -> str | None:
    """A verbatim paper quote that contains the stated number (the value is grounded, not only the setting)."""
    for e in a.evidence:
        if e.kind != "paper" or not e.quote:
            continue
        for m in re.finditer(r"\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", e.quote.replace(",", "")):
            x = float(m.group(0))
            if _close(x, number) or _close(x, number * 100) or _close(x / 100, number):
                return e.quote
    return None


def _spell(paper: float, literal: str) -> str:
    """The paper's value in the literal's type: an int stays an int."""
    if re.fullmatch(r"[-+]?\d+", literal.strip()) and float(paper).is_integer():
        return str(int(paper))
    return repr(float(paper))


def match_constants(assumptions: list[Assumption], root: str | Path, per_setting: int = 2) -> list[dict]:
    """Literal leads where the code's constant differs from the value the paper states, paper evidence attached.
    Matched by core words (`num_epochs` ~ `epochs`); an equal value anywhere in the code under the same name
    means the setting is already as stated, and no lead is made for it."""
    from gapfinder.ingest.code_checks import named_literals
    from gapfinder.search.engine import _core

    inventory = named_literals(root)
    by_core: dict[frozenset, list] = {}
    for lit in inventory:
        c = _core(lit.name)
        if c:
            by_core.setdefault(c, []).append(lit)
    out, seen = [], set()
    for a in assumptions:
        if str(a.paper_value).strip().lower().startswith("unstated"):
            continue
        parsed = _number(a.paper_value)
        if parsed is None:
            continue
        paper, pct = parsed
        quote = _paper_quote(a, paper)
        if quote is None:
            continue  # the stated number isn't in a verbatim quote: not paper evidence
        core = _core(_strip(a.knob))
        if not core:
            continue
        exact = by_core.get(core, [])
        # one extra word on either side ("dropout" ~ "attn_dropout"), scored after exact matches
        near = [lit for c, lits in by_core.items() if c != core and (c > core or c < core)
                and len(c ^ core) == 1 for lit in lits]
        hits = []
        for lit in exact + near:
            try:
                v = float(ast.literal_eval(lit.value))  # a numeric literal, from ast.unparse
            except (ValueError, TypeError, SyntaxError):
                continue
            # a percentage in the paper may be a fraction in the code (10% and 0.1)
            target = paper / 100 if pct and abs(v) <= 1 else paper
            hits.append((lit, v, target))
        if any(_close(v, target) for lit, v, target in hits if _core(lit.name) == core):
            continue  # the code already holds the paper's value under this name
        n = 0
        for lit, v, target in hits:
            if _close(v, target) or (lit.file, lit.line, lit.name) in seen:
                continue
            seen.add((lit.file, lit.line, lit.name))
            out.append({"family": "unexposed_setting", "source": "matcher", "file": lit.file, "line": lit.line,
                        "name": lit.name, "value": lit.value, "code": lit.code,
                        "paper_value": _spell(target, lit.value), "quote": quote,
                        "detail": f"the paper states {a.knob} = {a.paper_value}; `{lit.name}` is {lit.value} "
                                  f"({lit.detail}) at {lit.file}:{lit.line}"})
            n += 1
            if n >= per_setting:
                break
    return out
