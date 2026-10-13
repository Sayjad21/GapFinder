"""Static config flow for Python artifacts (plain code, no LLM): what does each command-line flag scale?

For every argparse flag it follows simple aliases (`m = args.epochx`, `epochs_multiplier = args.epochx`)
and records the other operand of each multiplication or division the flag takes part in:

    epochs_multiplier = args.epochx
    best = net(..., n_epochs=int(n_epochs * epochs_multiplier))   ->  epochx scales n_epochs

That marks `epochx` as a multiplier, and tells a resolver that "10x more epochs" maps to epochx = 10
(the paper states the factor; the code applies it to n_epochs). Only Python is handled; it's a
best-effort pass, and anything it can't parse is skipped.
"""

from __future__ import annotations

import ast
from pathlib import Path


def _flag_dest(call: ast.Call) -> str | None:
    """The attribute name argparse stores a flag under: --epochx -> epochx, dest= wins."""
    for kw in call.keywords:
        if kw.arg == "dest" and isinstance(kw.value, ast.Constant):
            return str(kw.value.value)
    for a in call.args:
        if isinstance(a, ast.Constant) and isinstance(a.value, str) and a.value.startswith("--"):
            return a.value[2:].replace("-", "_")
    return None


def _name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    if isinstance(node, ast.Call) and node.args:  # int(x), float(x), len(x)
        return _name(node.args[0])
    if isinstance(node, ast.Subscript):
        return _name(node.value)
    return None


def scales_in_file(path: Path) -> dict[str, set[str]]:
    """flag dest -> names of the quantities it multiplies or divides, in one Python file."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except (SyntaxError, ValueError):
        return {}
    flags = {d for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
             and n.func.attr == "add_argument" and (d := _flag_dest(n))}
    if not flags:
        return {}
    alias: dict[str, str] = {}  # variable name -> flag dest
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            v = n.value
            src = v.attr if isinstance(v, ast.Attribute) else _name(v) if isinstance(v, ast.Call) else None
            if src in flags:
                alias[n.targets[0].id] = src
    out: dict[str, set[str]] = {}

    def flag_of(node: ast.AST) -> str | None:
        if isinstance(node, ast.Attribute) and node.attr in flags:
            return node.attr
        if isinstance(node, ast.Name) and node.id in alias:
            return alias[node.id]
        if isinstance(node, ast.Call) and node.args:
            return flag_of(node.args[0])
        return None

    for n in ast.walk(tree):
        if isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Mult, ast.Div)):
            for this, other in ((n.left, n.right), (n.right, n.left)):
                f = flag_of(this)
                o = _name(other)
                if f and o and flag_of(other) != f and not (isinstance(other, ast.Constant)):
                    out.setdefault(f, set()).add(alias.get(o, o))
    return out


def flag_scales(root: Path) -> dict[str, list[str]]:
    """flag dest -> sorted quantities it scales, over every .py file under `root`."""
    merged: dict[str, set[str]] = {}
    for p in sorted(Path(root).rglob("*.py")):
        if any(part in {".git", "__pycache__", ".venv", "venv", "node_modules"} for part in p.parts):
            continue
        for f, names in scales_in_file(p).items():
            merged.setdefault(f, set()).update(names)
    return {f: sorted(v) for f, v in merged.items()}
