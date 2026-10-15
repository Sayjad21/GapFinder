"""Patch knobs: test a hard-coded constant without editing the artifact's files.

A static lead from `gapfinder/ingest/code_checks.py` such as `net/net.py:70  batch_size = 128` becomes a
knob named `@ast:net/net.py:70:batch_size` whose default is the literal (`128`). A run that sets it:

- uploads this package's hook as `.gf_patch/sitecustomize.py` (GapFinder's own file, outside the
  artifact, so the diff guard doesn't apply to it);
- puts `.gf_patch` on PYTHONPATH and sets GF_AST_PATCH="net/net.py:70:batch_size=32";
- the hook installs an import finder: when a module whose file ends in `net/net.py` is imported, its
  source is parsed, the literal assigned to `batch_size` on line 70 (or passed as `batch_size=` in a
  call on that line) is replaced, and the module is compiled from the changed tree in memory.

No file on disk changes, so the diff guard, the repo map and the prompt caches are untouched. Limits:
- Python only;
- literals only (a loop or a grid search is not a literal);
- imported modules only. The entry script (the file the command runs) is not imported, so leads in it
  are left out: `entry_script()`;
- a patch that finds no target raises in the run, so a mistargeted patch fails loudly, never silently.

The hook works on Python 3.6+ (MC Dropout's image is 3.6), so it avoids newer syntax and handles both
ast.Num/Str (3.6-3.7) and ast.Constant (3.8+).
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

PREFIX = "@ast:"
HOOK_DIR = ".gf_patch"
ENV = "GF_AST_PATCH"
_SEP = ";"

HOOK_SOURCE = r'''
# GapFinder patch hook (gapfinder/sandbox/ast_patch.py). Rewrites one literal per entry of
# GF_AST_PATCH="rel/path.py:LINE:NAME=VALUE;..." in memory when the module is imported.
import ast, os, sys
import importlib.abc, importlib.machinery

def _entries():
    out = []
    for part in os.environ.get("GF_AST_PATCH", "").split(";"):
        part = part.strip()
        if not part:
            continue
        loc, val = part.rsplit("=", 1)
        rel, line, name = loc.rsplit(":", 2)
        out.append((rel.replace("\\", "/").lstrip("./"), int(line), name, val))
    return out

def _is_literal(node):
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        return _is_literal(node.operand)
    lit = tuple(t for t in (getattr(ast, "Num", None), getattr(ast, "Str", None),
                            getattr(ast, "NameConstant", None), getattr(ast, "Constant", None)) if t)
    return isinstance(node, lit)

class _Swap(ast.NodeTransformer):
    def __init__(self, line, name, value):
        self.line, self.name, self.raw, self.done = line, name, value, 0

    def _new(self, old):
        return ast.copy_location(ast.parse(self.raw, mode="eval").body, old)  # a fresh node per replacement

    def visit_Assign(self, node):
        self.generic_visit(node)
        if node.lineno == self.line and _is_literal(node.value) and any(
                isinstance(t, ast.Name) and t.id == self.name for t in node.targets):
            node.value = self._new(node.value)
            self.done += 1
        return node

    def visit_Call(self, node):
        self.generic_visit(node)
        if node.lineno == self.line:
            for kw in node.keywords:
                if kw.arg == self.name and _is_literal(kw.value):
                    kw.value = self._new(kw.value)
                    self.done += 1
        return node

def patch_tree(tree, entries):
    for _rel, line, name, val in entries:
        sw = _Swap(line, name, val)
        tree = sw.visit(tree)
        if not sw.done:
            raise RuntimeError("GF_AST_PATCH: no literal %s on line %d" % (name, line))
    return ast.fix_missing_locations(tree)

class _Loader(importlib.abc.Loader):
    def __init__(self, origin, entries):
        self.origin, self.entries = origin, entries
    def create_module(self, spec):
        return None
    def exec_module(self, module):
        with open(self.origin, encoding="utf-8") as fh:
            tree = ast.parse(fh.read(), self.origin)
        module.__file__ = self.origin
        exec(compile(patch_tree(tree, self.entries), self.origin, "exec"), module.__dict__)

class _Finder(importlib.abc.MetaPathFinder):
    def __init__(self, entries):
        self.entries = entries
    def find_spec(self, fullname, path, target=None):
        spec = importlib.machinery.PathFinder.find_spec(fullname, path)
        if spec is None or not spec.origin:
            return spec
        origin = spec.origin.replace("\\", "/")
        mine = [e for e in self.entries if origin == e[0] or origin.endswith("/" + e[0])]
        if mine:
            spec.loader = _Loader(spec.origin, mine)
        return spec

_E = _entries()
if _E:
    sys.meta_path.insert(0, _Finder(_E))
'''


def is_patch(knob: str) -> bool:
    return knob.startswith(PREFIX)


def knob_name(rel: str, line: int, name: str) -> str:
    return f"{PREFIX}{rel}:{line}:{name}"


def parse(knob: str) -> tuple[str, int, str]:
    rel, line, name = knob[len(PREFIX):].rsplit(":", 2)
    return rel, int(line), name


def run_parts(changes: dict[str, str]) -> tuple[dict[str, str], dict[str, bytes], str]:
    """For the patch knobs in `changes`: (env, files to upload, shell prefix). Empty when there are none."""
    patches = {k: v for k, v in changes.items() if is_patch(k)}
    if not patches:
        return {}, {}, ""
    entry = _SEP.join(f"{rel}:{line}:{name}={value}" for k, value in sorted(patches.items())
                      for rel, line, name in [parse(k)])
    prefix = f'export PYTHONPATH="${{WORK:-$PWD}}/{HOOK_DIR}${{PYTHONPATH:+:$PYTHONPATH}}"; '
    return {ENV: entry}, {f"{HOOK_DIR}/sitecustomize.py": HOOK_SOURCE.encode()}, prefix


def apply_source(src: str, line: int, name: str, value: str) -> str:
    """The hook's transform on a source string, for tests and for showing the patch in reports."""
    ns: dict = {}
    exec(compile(HOOK_SOURCE.split("class _Loader")[0], "<gf-hook>", "exec"), ns)  # _Swap and patch_tree only
    tree = ns["patch_tree"](ast.parse(src), [("", line, name, value)])
    return ast.unparse(tree) if hasattr(ast, "unparse") else src


_ENTRY_RE = re.compile(r"parse_args\(|if\s+__name__\s*==\s*['\"]__main__['\"]")


def entry_script(path: Path) -> bool:
    """A file that looks like a program's entry point (parses arguments, or has a __main__ block). The hook
    patches imported modules, so leads in such a file are not offered as patch knobs."""
    try:
        return bool(_ENTRY_RE.search(path.read_text(encoding="utf-8", errors="replace")))
    except OSError:
        return True
