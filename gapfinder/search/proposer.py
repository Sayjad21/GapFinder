"""Plan G6: a residual-guided code proposer. When the deterministic rounds end with no configuration that fits every
claim, one Nemotron 3 Super call reads the code the run executed and the pattern of the gap, and proposes at most
three small code edits; the engine runs them like any other in-memory patch, and a fit is a code lead.

The pattern of localise, propose candidates and validate by execution is the one that works in automated program
repair (Agentless, SWE-bench; LLM fault localisation such as AutoFL on Defects4J). Here the test is the paper's
numbers. To keep the call small and the model's job concrete:
- the code is the executed lines only (from the runtime trace), or the files the claims' metric is computed in;
- the numbers come with their ratios computed here, and each ratio near an integer the run used (a batch count, a
  size, 2, 10, 100) is pointed out: a sum where a mean was meant shows up as a ratio equal to a count;
- each edit is a replacement of text within one line (plan H3: the model writes statements and pieces of
  multi-line expressions, so `old` is any text on that line, not a whole expression); the file is parsed with the
  edit, the one expression that changed becomes the patch, and an edit that writes one of the paper's numbers into
  the code is refused (it would explain nothing).
The proposer is never the evidence: the runs are, and its fits get the mutation round's guards and label.
"""

from __future__ import annotations

import ast
import math
import re
from pathlib import Path

from pydantic import BaseModel, Field

PROMPT = """You localise a defect in research code. The paper reports numbers that this code doesn't reproduce,
and no setting of the program's flags reproduces them, so the difference is probably in the code itself: an
operation, a constant, a data split, a reduction, a unit.

## The numbers (the paper's against this code's, as run)
{claims}

## Integers and settings the run used
{ints}

## The code the run executed (file:line: source)
{code}

Propose at most 3 edits, the likeliest first. Each edit replaces text within one line:
- `file` and `line` from the listing above; `old`: text copied exactly from that line; `new`: the text to put in
  its place, so that the line still parses and one expression on it changes;
- prefer one edit that explains every number at once. A ratio equal to a count the run used suggests a sum where
  a mean was meant (or the reverse); a factor of 2, 10 or 100 suggests a unit or a counting convention; numbers
  that all move the same way suggest the data or the evaluation;
- never change printing, logging or paths, and never write one of the paper's reported numbers into the code.
If nothing in the code plausibly explains the numbers, return no edits.
"""


class Edit(BaseModel):
    file: str
    line: int
    old: str
    new: str
    why: str = ""


class Edits(BaseModel):
    edits: list[Edit] = Field(default_factory=list)


def ratio_lines(claims: list[tuple[str, str, float, float]], ints: dict[str, int]) -> list[str]:
    """One line per claim (id, metric, paper, code): the values, paper / code, and the integers the ratio is near."""
    counts = {"2": 2, "10": 10, "100": 100, **{k: v for k, v in ints.items() if v >= 2}}
    out = []
    for cid, metric, paper, code in claims:
        line = f"- {cid} ({metric}): paper {paper:g}, code {code:g}"
        if code and paper and math.isfinite(paper / code):
            r = paper / code
            line += f", paper / code = {r:.4g}"
            near = [f"{name} ({v})" for name, v in counts.items()
                    for x in (r, 1 / r) if x > 1.5 and abs(x - v) <= 0.03 * v]
            if near:
                line += " - near " + ", ".join(dict.fromkeys(near))
        out.append(line)
    return out


def code_listing(root: Path, executed: dict[str, list[int]], files: list[str], max_chars: int = 14000) -> str:
    """`file:line: source` for the executed lines of each file (all its lines when the trace has none), the
    likeliest files first, cut at `max_chars`."""
    out, used = [], 0
    for rel in files:
        p = root / rel
        if not p.exists():
            continue
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        keep = sorted(set(executed.get(rel) or [])) or list(range(1, len(lines) + 1))
        for n in keep:
            if 1 <= n <= len(lines) and lines[n - 1].strip() and not lines[n - 1].strip().startswith("#"):
                row = f"{rel}:{n}: {lines[n - 1].rstrip()}"
                if used + len(row) > max_chars:
                    return "\n".join(out)
                out.append(row)
                used += len(row) + 1
    return "\n".join(out)


def ground(edits: list[Edit], root: Path, paper_values: list[float]) -> tuple[list[tuple[str, str]], list[str]]:
    """([(patch knob, description)], [why each other edit was refused]). An edit is kept when its file and line
    exist, `old` is text on that line, the file parses with `old` replaced by `new` there, the change is one
    expression (plan H3: the smallest subtree that differs between the two parses), and `new` writes none of the
    paper's numbers. At most 3 edits are read."""
    from gapfinder.sandbox import ast_patch
    from gapfinder.search.mutation import _number

    kept, refused = [], []
    for e in edits[:3]:
        rel = e.file.replace("\\", "/").lstrip("./")
        p = root / rel
        if not p.exists():
            refused.append(f"{e.file}: no such file")
            continue
        src = p.read_text(encoding="utf-8", errors="replace")
        lines = src.splitlines(keepends=True)
        if not 1 <= e.line <= len(lines) or e.old not in lines[e.line - 1]:
            refused.append(f"{rel}:{e.line}: `{e.old}` is not on that line")
            continue
        nums = [float(x) for x in re.findall(r"-?\d+\.?\d*(?:e-?\d+)?", e.new)]
        if any(abs(x - v) <= 1e-6 * max(1.0, abs(v)) for x in nums for v in paper_values if abs(v) >= 1e-9):
            refused.append(f"{rel}:{e.line}: `{e.new}` writes a reported number into the code")
            continue
        edited = "".join(lines[: e.line - 1] + [lines[e.line - 1].replace(e.old, e.new, 1)] + lines[e.line:])
        try:
            before, after = ast.parse(src), ast.parse(edited)
        except SyntaxError:
            refused.append(f"{rel}:{e.line}: the file doesn't parse with `{e.new}`")
            continue
        node, new = _changed(before, after)
        if node is None or not isinstance(node, ast.expr) or getattr(node, "lineno", None) != e.line:
            refused.append(f"{rel}:{e.line}: `{e.old}` -> `{e.new}` changes no single expression on that line")
            continue
        text = ast.unparse(new)
        kind = "num" if _number(node) is not None else type(node).__name__  # "num" matches on every Python version
        knob = f"{ast_patch.PREFIX}{rel}:{node.lineno}:@mut.{node.col_offset}.{kind}.{ast_patch.set_op(text)}"
        kept.append((knob, f"{rel}:{node.lineno}: `{ast.unparse(node)}` -> `{text}`" + (f" ({e.why})" if e.why else "")))
    return kept, refused


def _changed(a: ast.AST, b: ast.AST) -> tuple[ast.AST | None, ast.AST | None]:
    """The smallest subtree of `a` that differs from its counterpart in `b`, and that counterpart: where one child
    differs, descend into it; where the node itself or more than one child differs, the node. (None, None) when
    the trees are the same (positions are not compared)."""
    if ast.dump(a) == ast.dump(b):
        return None, None
    if type(a) is not type(b):
        return a, b
    diffs = []
    for f in a._fields:
        x, y = getattr(a, f, None), getattr(b, f, None)
        if isinstance(x, list) and isinstance(y, list):
            if len(x) != len(y):
                return a, b
            diffs += [(u, v) for u, v in zip(x, y) if ast.dump(u) != ast.dump(v)] if all(
                isinstance(u, ast.AST) for u in x + y) else ([(a, b)] if x != y else [])
        elif isinstance(x, ast.AST) and isinstance(y, ast.AST):
            if ast.dump(x) != ast.dump(y):
                diffs.append((x, y))
        elif x != y:
            return a, b
    if len(diffs) != 1 or diffs[0][0] is a:
        return a, b
    return _changed(*diffs[0])


async def propose(router, claims: list[str], ints: dict[str, int], code: str) -> list[Edit]:
    msg = PROMPT.format(claims="\n".join(claims), ints=", ".join(f"{k}={v}" for k, v in sorted(ints.items())) or "none",
                        code=code or "(no listing)")
    out = await router.structured("super", [{"role": "user", "content": msg}], Edits)
    return list(out.edits)[:3]
