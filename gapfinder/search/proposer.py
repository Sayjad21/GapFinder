"""Plan G6: a residual-guided code proposer. When the deterministic rounds end with no configuration that fits every
claim, one Nemotron 3 Super call reads the code the run executed and the pattern of the gap, and proposes at most
three small code edits; the engine runs them like any other in-memory patch, and a fit is a code lead.

The pattern of localise, propose candidates and validate by execution is the one that works in automated program
repair (Agentless, SWE-bench; LLM fault localisation such as AutoFL on Defects4J). Here the test is the paper's
numbers. To keep the call small and the model's job concrete:
- the code is the executed lines only (from the runtime trace), or the files the claims' metric is computed in;
- the numbers come with their ratios computed here, and each ratio near an integer the run used (a batch count, a
  size, 2, 10, 100) is pointed out: a sum where a mean was meant shows up as a ratio equal to a count;
- each edit replaces one expression on one line, copied exactly, and an edit that writes one of the paper's numbers
  into the code is refused (it would explain nothing).
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

Propose at most 3 edits, the likeliest first. Each edit replaces one expression on one line:
- `file` and `line` from the listing above; `old`: the expression, copied exactly from that line; `new`: the
  Python expression to put in its place;
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
    exist, `old` is an expression on that line, `new` parses as an expression, and `new` writes none of the paper's
    numbers."""
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
        try:
            tree = ast.parse(src)
            ast.parse(e.new, mode="eval")
        except SyntaxError:
            refused.append(f"{rel}:{e.line}: `{e.new}` doesn't parse")
            continue
        nums = [float(x) for x in re.findall(r"-?\d+\.?\d*(?:e-?\d+)?", e.new)]
        if any(abs(x - v) <= 1e-6 * max(1.0, abs(v)) for x in nums for v in paper_values if abs(v) >= 1e-9):
            refused.append(f"{rel}:{e.line}: `{e.new}` writes a reported number into the code")
            continue
        want = re.sub(r"\s+", "", e.old)
        nodes = [n for n in ast.walk(tree) if isinstance(n, ast.expr) and getattr(n, "lineno", None) == e.line
                 and re.sub(r"\s+", "", ast.get_source_segment(src, n) or "") == want]
        if not nodes:
            refused.append(f"{rel}:{e.line}: `{e.old}` is not an expression on that line")
            continue
        n = max(nodes, key=lambda x: len(ast.get_source_segment(src, x) or ""))  # the outermost match
        kind = "num" if _number(n) is not None else type(n).__name__  # "num" matches on every Python version
        knob = f"{ast_patch.PREFIX}{rel}:{n.lineno}:@mut.{n.col_offset}.{kind}.{ast_patch.set_op(e.new)}"
        kept.append((knob, f"{rel}:{n.lineno}: `{e.old}` -> `{e.new}`" + (f" ({e.why})" if e.why else "")))
    return kept, refused


async def propose(router, claims: list[str], ints: dict[str, int], code: str) -> list[Edit]:
    msg = PROMPT.format(claims="\n".join(claims), ints=", ".join(f"{k}={v}" for k, v in sorted(ints.items())) or "none",
                        code=code or "(no listing)")
    out = await router.structured("super", [{"role": "user", "content": msg}], Edits)
    return list(out.edits)[:3]
