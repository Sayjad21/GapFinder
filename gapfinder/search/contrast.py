"""Contrastive paper-to-trace diffing: where does the code, as it ran, differ from what the paper describes?

Used only when history matching says "out of space" (no setting fits every claim). One cached Nemotron 3
Super call gets:
- the paper's training/evaluation details and its hyperparameter tables;
- the dry-run trace: config values each process saw, the sinks their values reached and the repo lines
  that reached them, loop bounds;
- the static code leads.

It answers with at most five differences between the paper and the code. Each is grounded before use:
- the file must exist and the line be in range;
- a "literal" difference must name a number that the line assigns or passes (the patch hook can only swap a
  literal), and the paper's value must parse.

Grounded literal differences become patch-knob leads, tried first in the patch round with the paper's value
first. Structural differences (a step in another order, a sum where the paper says a mean) are reported as
leads and never tested: rewriting code structure until the number fits would explain nothing, which is what
the diff guard is for. A patch that fits is reported as a code change, never as "Explained".
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

CONTRAST_PROMPT = """You compare a paper with its released code as the code actually ran.

No setting of the program makes all the paper's numbers match, so the difference is probably in the code:
a hard-coded value, a step done differently, an evaluation detail. Find where the code, as traced below,
differs from what the paper says it does.

## What the paper says (training and evaluation details, hyperparameter tables)
{paper}

## What the code did in one traced run
Settings each process saw (from argparse, flags and config files):
{config}

Values that reached known library calls, with the repo line that made the call:
{sinks}

Loop bounds in the repo's code (file:line -> bound):
{loops}

## Hard-coded values a static scan flagged
{leads}

List at most 5 differences, most likely to explain the gap first. For each:
- file and line: a repo file and line from the lists above, where the code does the thing;
- paper_says / code_does: short, concrete;
- kind: "literal" when the difference is one hard-coded number on that line (give `name`, the variable,
  keyword or function parameter that holds it, and `paper_value`, the number the paper states); otherwise
  "structural";
- quote: the paper's own words that state it, copied exactly (one sentence or table cell).
Only differences the paper text supports. If you find none, return an empty list.
"""


class Difference(BaseModel):
    file: str
    line: int
    paper_says: str
    code_does: str
    kind: Literal["literal", "structural"]
    name: str | None = None
    paper_value: str | None = None
    quote: str | None = None  # the paper's words, verbatim: grounded against the paper before use


class Differences(BaseModel):
    differences: list[Difference] = Field(default_factory=list)


def _excerpt(paper_text: str, max_chars: int = 9000) -> str:
    from gapfinder.ledger.assumptions import hyperparameter_tables

    low = paper_text.lower()
    parts = []
    for key in ("implementation detail", "experimental setup", "training detail", "hyper-parameter",
                "hyperparameter", "evaluation protocol", "experiment"):
        i = low.find(key)
        if i >= 0:
            parts.append(paper_text[i: i + 2500])
            if sum(map(len, parts)) > max_chars // 2:
                break
    parts += hyperparameter_tables(paper_text)
    return "\n\n".join(parts)[:max_chars] or paper_text[:max_chars]


def _summaries(records: list[dict], max_lines: int = 60) -> tuple[str, str, str]:
    config, sinks, loops = [], [], []
    for rec in records:
        argv = " ".join(rec.get("argv", [])[:6])
        for c in rec.get("config", [])[:3]:
            vals = ", ".join(f"{k}={v}" for k, v in list(c.get("values", {}).items())[:40])
            config.append(f"[{argv}] {c.get('src')}: {vals}")
        for s in rec.get("sinks", []):
            site = f"{s['site'][0]}:{s['site'][1]}" if s.get("site") else "?"
            sinks.append(f"{site}  {s['kind']} {s['cls']}({', '.join(f'{k}={v}' for k, v in s['args'].items())})")
        for site, stops in (rec.get("ranges") or {}).items():
            loops.append(f"{site} -> {', '.join(map(str, stops))}")
    uniq = lambda xs: list(dict.fromkeys(xs))[:max_lines]  # noqa: E731
    return "\n".join(uniq(config)) or "none", "\n".join(uniq(sinks)) or "none", "\n".join(uniq(loops)) or "none"


async def contrast(router, paper_text: str, records: list[dict], leads: list[dict]) -> list[Difference]:
    config, sinks, loops = _summaries(records)
    lead_text = "\n".join(f"{x.get('file')}:{x.get('line')}  {x.get('name')} = {x.get('value')}" for x in leads[:20]) or "none"
    msg = CONTRAST_PROMPT.format(paper=_excerpt(paper_text), config=config, sinks=sinks, loops=loops, leads=lead_text)
    out = await router.structured("super", [{"role": "user", "content": msg}], Differences)
    return out.differences[:5]


_NUM = re.compile(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")


def _literal_on_line(path: Path, line: int, name: str | None) -> str | None:
    """The literal that `name` gets on `line` (an assignment, or a keyword in a call), as written."""
    try:
        src = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except (OSError, SyntaxError, ValueError):
        return None
    for node in ast.walk(tree):
        if getattr(node, "lineno", None) != line:
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):  # a parameter default on the def line
            a = node.args
            pos = a.args[len(a.args) - len(a.defaults):] if a.defaults else []
            pairs = list(zip(pos, a.defaults)) + [(x, y) for x, y in zip(a.kwonlyargs, a.kw_defaults) if y is not None]
            for arg, dflt in pairs:
                if arg.arg == name and isinstance(dflt, ast.Constant) and isinstance(dflt.value, (int, float)):
                    return ast.get_source_segment(src, dflt)
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if name in (None, node.targets[0].id) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, (int, float)):
                return ast.get_source_segment(src, node.value)
        if isinstance(node, ast.Call):
            for kw in node.keywords:
                if kw.arg and name in (None, kw.arg) and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, (int, float)):
                    return ast.get_source_segment(src, kw.value)
    return None


def ground(diffs: list[Difference], root: Path, paper_text: str | None = None) -> tuple[list[dict], list[dict], list[str]]:
    """(patch leads, structural leads, rejections). A patch lead has the shape of a static lead plus the
    paper's value, and the paper's quote when it is verbatim in the paper and contains that number (then it
    is evidence for the value); anything that doesn't check out against the repo is rejected with a reason."""
    from gapfinder.ledger.grounding import Grounder, _numbers, _same_num

    g = Grounder(paper_text, root) if paper_text else None
    patch, structural, rejected = [], [], []
    for d in diffs:
        path = root / d.file
        if not path.is_file():
            rejected.append(f"{d.file}:{d.line}: no such file")
            continue
        n = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
        if not 1 <= d.line <= n:
            rejected.append(f"{d.file}:{d.line}: line out of range")
            continue
        entry = {"file": d.file, "line": d.line, "paper_says": d.paper_says, "code_does": d.code_does}
        if d.kind == "literal":
            lit = _literal_on_line(path, d.line, d.name)
            if lit is None or not d.name:
                rejected.append(f"{d.file}:{d.line}: no literal {d.name!r} on that line; kept as a structural lead")
                structural.append(entry)
                continue
            pv = _NUM.search(d.paper_value or "")
            quote = None
            if pv and d.quote and g is not None and g.quote_in_paper(d.quote) and any(
                    _same_num(float(pv.group(0)), n) for n in _numbers(d.quote)):
                quote = d.quote.strip()
            elif d.quote:
                rejected.append(f"{d.file}:{d.line}: the quote is not in the paper or lacks {d.paper_value!r}; "
                                "kept as a lead without evidence")
            patch.append({**entry, "name": d.name, "value": lit, "paper_value": pv.group(0) if pv else None,
                          "quote": quote, "family": "unexposed_setting", "source": "contrast"})
        else:
            structural.append(entry)
    return patch, structural, rejected
