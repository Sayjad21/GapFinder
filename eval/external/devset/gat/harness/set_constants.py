"""devset GAT: write a copy of execute_cora_sparse.py with some module-level constants replaced.

    python gf_harness/set_constants.py <out.py> NAME=VALUE [NAME=VALUE ...]

Mechanical: every NAME must be a module-level `NAME = ...` assignment of the shipped script (found with
ast, so a typo fails loudly), and that statement is replaced by `NAME = VALUE`. VALUE is a Python
expression, except where the shipped value is a list literal: then VALUE is comma-separated items
("8,1" -> [8, 1]), since knob values may not contain brackets or spaces. Nothing else in the file changes.
"""
from __future__ import annotations

import ast
import sys

SRC = "execute_cora_sparse.py"


def main(out: str, pairs: list[str]) -> None:
    text = open(SRC, encoding="utf-8").read()
    lines = text.splitlines(keepends=True)
    tree = ast.parse(text)
    stmts = {}
    for node in tree.body:  # module level only
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            stmts.setdefault(node.targets[0].id, []).append(node)
    repl = {}
    for p in pairs:
        name, _, value = p.partition("=")
        if name not in stmts or len(stmts[name]) != 1:
            sys.exit(f"set_constants: {name!r} is not a single module-level assignment of {SRC}")
        node = stmts[name][0]
        if isinstance(node.value, ast.List):
            value = "[" + ", ".join(v.strip() for v in value.split(",") if v.strip()) + "]"
        ast.parse(value, mode="eval")  # must be a valid expression
        end = getattr(node, "end_lineno", None)  # python 3.7's ast has no end_lineno
        if end is None:  # then the statement must be the whole of its line
            ast.parse(lines[node.lineno - 1].strip())
            end = node.lineno
        repl[node.lineno] = (end, f"{name} = {value}\n")
        print(f"set {name} = {value}", file=sys.stderr)
    out_lines, i = [], 1
    while i <= len(lines):
        if i in repl:
            end, new = repl[i]
            out_lines.append(new)
            i = end + 1
        else:
            out_lines.append(lines[i - 1])
            i += 1
    open(out, "w", encoding="utf-8").write("".join(out_lines))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
