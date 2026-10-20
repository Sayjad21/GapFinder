"""Where in the code could the gap come from? Mutation-based localisation (plan D5.2-D5.3).

The patch round could swap a hard-coded literal. Documented causes on sealed papers were also arithmetic (an edge
counted twice: `x / 2`), loop bounds (`range(200)`), reductions (a mean that should be a sum) and comparisons. This
module proposes small, ML-meaningful edits (mutants) at a few code sites and ranks them; the engine runs them through
the in-memory patch hook (`@ast:...:@mut.COL.KIND.OP`, sandbox/ast_patch.py) and scores each on every claim.

Mutation-based fault localisation (MUSE, Metallaxis) ranks sites by how mutants there change failing tests. Here the
"failing test" is the paper's set of claims, and the search space is kept small and meaningful:
- **sites on the data flow of a knob** the claims depend on: statements that read the knob (distance 0), statements
  that define their other operands or use their results (1), and one more step, including one call into a repo
  function that receives the knob's value (an intraprocedural slice plus one interprocedural step);
- **metric code** (functions named like accuracy, f1, auc, evaluate, test) and the run's **loop bounds**
  (`range()` constants), and boolean keywords of data loaders (`shuffle`, `drop_last`);
- **executed lines only**, when the runtime trace recorded coverage;
- **operators implied by measured relations** first: a verified scale relation ("the code's knob is 0.5 x the
  paper's", plan D2.4) makes the matching factor on that knob's slice the first mutants tried.
Interference mutants (edits on correct code that happen to move the numbers, FLIM 2025) are kept out by the engine:
a mutant must fit every claim, held-outs included, after repeats, and it is never labelled "Explained".
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path

REDUCTIONS = {"mean": "sum", "sum": "mean", "nanmean": "nansum", "nansum": "nanmean", "reduce_mean": "reduce_sum",
              "reduce_sum": "reduce_mean"}
METRIC_FN = re.compile(r"(?i)(acc|accuracy|f1|auc|ndcg|recall|precision|hit|mrr|map|metric|score|eval|evaluate|test)")
SKIP_CALLS = {"print", "format", "write", "info", "debug", "warning", "error", "log", "tqdm", "set_description",
              "add_scalar", "dump", "save"}
LOADER_BOOLS = {"shuffle", "drop_last", "normalize", "bias", "pin_memory", "replacement"}


@dataclass
class Mutant:
    file: str
    line: int
    col: int
    kind: str  # num | bool | Subscript | Attribute | Name | Call | BinOp | Compare
    op: str
    dist: int  # slice distance (0: reads the knob)
    knob: str | None  # the knob whose slice holds it (None: metric code, loops, loaders)
    before: str
    after: str
    priority: float = 0.0
    tags: list[str] = field(default_factory=list)

    @property
    def name(self) -> str:
        return f"@ast:{self.file}:{self.line}:@mut.{self.col}.{self.kind}.{self.op}"

    def describe(self) -> str:
        return f"{self.file}:{self.line}: `{self.before}` -> `{self.after}`"


def _norm(k: str) -> str:
    return k.strip().lstrip("-").replace("-", "_").lower()


def _knob_reads(node: ast.AST, knobs: set[str]) -> set[str]:
    """Knobs a node reads: `args.lr`, `FLAGS.lr`, `opt.lr`, `cfg["lr"]`, `self.args.lr`."""
    out = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Load) and _norm(n.attr) in knobs:
            out.add(_norm(n.attr))
        elif isinstance(n, ast.Subscript):
            key = getattr(n.slice, "value", n.slice)  # Python 3.8 wraps the key in Index
            if isinstance(key, ast.Constant) and isinstance(key.value, str) and _norm(key.value) in knobs:
                out.add(_norm(key.value))
    return out


def _names(node: ast.AST, ctx) -> set[str]:
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name) and isinstance(n.ctx, ctx)}


def _defs(stmt: ast.stmt) -> set[str]:
    out = set()
    targets = []
    if isinstance(stmt, ast.Assign):
        targets = stmt.targets
    elif isinstance(stmt, (ast.AugAssign, ast.AnnAssign)):
        targets = [stmt.target]
    elif isinstance(stmt, (ast.For, ast.AsyncFor)):
        targets = [stmt.target]
    for t in targets:
        out |= _names(t, ast.Store)
        for n in ast.walk(t):  # self.x = ... defines "self.x"
            if isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Store):
                out.add("." + n.attr)
    return out


def _uses(stmt: ast.stmt) -> set[str]:
    out = _names(stmt, ast.Load)
    for n in ast.walk(stmt):
        if isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Load):
            out.add("." + n.attr)
    return out


def _simple_statements(body: list[ast.stmt]) -> list[ast.stmt]:
    """The statements of a scope, flattened through if/for/while/with/try (not into nested functions or classes)."""
    out = []
    for s in body:
        if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        out.append(s)
        for f in ("body", "orelse", "finalbody"):
            out += _simple_statements(getattr(s, f, []) or [])
        for h in getattr(s, "handlers", []) or []:
            out += _simple_statements(h.body)
    return out


def _scopes(tree: ast.Module) -> list[tuple[str, list[ast.stmt], ast.AST]]:
    """(name, statements, node) for the module and every function (methods included)."""
    out = [("<module>", _simple_statements(tree.body), tree)]
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.append((n.name, _simple_statements(n.body), n))
    return out


def _slice(stmts: list[ast.stmt], seeds: list[ast.stmt], depth: int = 2) -> dict[int, int]:
    """id(statement) -> distance from the seeds, within one scope: forward through what a statement defines,
    backward to the definitions of what it uses."""
    dist = {id(s): 0 for s in seeds}
    frontier = list(seeds)
    for d in range(1, depth + 1):
        nxt = []
        for s in frontier:
            d_out, u_in = _defs(s), _uses(s) - {"self", "args", "FLAGS", "opt", "cfg", "config", "flags"}
            for t in stmts:
                if id(t) in dist:
                    continue
                if (d_out & _uses(t)) or (u_in & _defs(t)):
                    dist[id(t)] = d
                    nxt.append(t)
        frontier = nxt
    return dist


def _calls_into(stmt: ast.stmt, names_in_slice: set[str], knobs: set[str]) -> list[tuple[str, int]]:
    """(function name, argument position or -1 for a keyword match) for calls in `stmt` that pass a slice value."""
    out = []
    for n in ast.walk(stmt):
        if isinstance(n, ast.Call):
            fname = n.func.id if isinstance(n.func, ast.Name) else n.func.attr if isinstance(n.func, ast.Attribute) else None
            if not fname:
                continue
            for i, a in enumerate(n.args):
                if (_names(a, ast.Load) & names_in_slice) or _knob_reads(a, knobs):
                    out.append((fname, i))
    return out


def _result_calls(stmt: ast.stmt) -> list[str]:
    """Functions whose return value a statement assigns (`x = f(...)`, `x = mod.f(...)`)."""
    v = getattr(stmt, "value", None) if isinstance(stmt, (ast.Assign, ast.AugAssign, ast.AnnAssign)) else None
    out = []
    for n in ast.walk(v) if v is not None else []:
        if isinstance(n, ast.Call):
            f = n.func.id if isinstance(n.func, ast.Name) else n.func.attr if isinstance(n.func, ast.Attribute) else ""
            if f and f not in SKIP_CALLS:
                out.append(f)
    return out


def _skip(node: ast.AST, parents: dict[int, ast.AST]) -> bool:
    """A print, a log call or a format string (or inside one), or the function of a call (`f` in `f(x)`)."""
    if isinstance(node, ast.Call):
        f = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else ""
        if f in SKIP_CALLS:
            return True
    parent = parents.get(id(node))
    if isinstance(parent, ast.Call) and parent.func is node:
        return True
    p = parents.get(id(node))
    while p is not None:
        if isinstance(p, ast.Call):
            f = p.func.id if isinstance(p.func, ast.Name) else p.func.attr if isinstance(p.func, ast.Attribute) else ""
            if f in SKIP_CALLS:
                return True
        if isinstance(p, ast.JoinedStr):
            return True
        p = parents.get(id(p))
    return False


def _unparse(node: ast.AST) -> str:
    try:
        return ast.unparse(node)
    except Exception:  # noqa: BLE001
        return type(node).__name__


def _number(node) -> float | None:
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    return None


NUM_OPS = ("div2", "mul2", "add1", "sub1", "div10", "mul10")
EXPR_OPS = ("xdiv2", "xmul2", "xdiv10", "xmul10")


def _after(op: str, before: str, node: ast.AST) -> str:
    import copy

    if op.startswith("red.") and isinstance(node, ast.Call):
        n = copy.deepcopy(node)
        if isinstance(n.func, ast.Attribute):
            n.func.attr = op[4:]
        elif isinstance(n.func, ast.Name):
            n.func.id = op[4:]
        return _unparse(n)
    if op == "cmpflip" and isinstance(node, ast.Compare):
        n = copy.deepcopy(node)
        swap = {ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt}
        n.ops = [swap.get(type(o), type(o))() for o in n.ops]
        return _unparse(n)
    if op == "not" and isinstance(node, ast.Constant):
        return repr(not node.value)
    v = _number(node)
    if v is not None and op in NUM_OPS:
        return {"mul2": v * 2, "div2": v // 2 if isinstance(v, int) and v % 2 == 0 else v / 2, "add1": v + 1,
                "sub1": v - 1, "mul10": v * 10, "div10": v / 10}[op].__repr__()
    if op in EXPR_OPS:
        return f"({before}) {'*' if 'mul' in op else '/'} {2 if op.endswith('2') else 10}"
    return before


def find_mutants(root: str | Path, knobs: list[str], executed: dict[str, list[int]] | None = None,
                 relations: list[dict] | None = None, files: list[Path] | None = None, limit: int = 40) -> list[Mutant]:
    """Candidate mutants, best first. `knobs`: the knobs the claims depend on (their slices are searched).
    `executed`: repo file -> executed lines (from the runtime trace). `relations`: verified scale relations
    ({"knob", "family", "c"}): their factor's operators on that knob's slice come first."""
    from gapfinder.harness_auto import _import_closure

    root = Path(root).resolve()
    kset = {_norm(k) for k in knobs if not k.startswith("@")}
    pairs = [(p, ast.parse(p.read_text(encoding="utf-8", errors="replace"))) for p in files] if files else _import_closure(root)
    rel_by_knob: dict[str, list[dict]] = {}
    for r in relations or []:
        if r.get("verified"):
            rel_by_knob.setdefault(_norm(r["knob"]), []).append(r)
    out: list[Mutant] = []
    seen = set()
    funcs: dict[str, tuple[ast.AST, list[ast.stmt], str]] = {}
    trees = []
    for path, tree in pairs:
        if tree is None:
            continue
        rel = path.relative_to(root).as_posix() if path.is_absolute() else path.as_posix()
        trees.append((rel, tree))
        for name, stmts, node in _scopes(tree):
            if name != "<module>":
                funcs.setdefault(name, (node, stmts, rel))

    def executed_line(rel: str, line: int) -> bool | None:
        if not executed:
            return None
        return line in set(executed.get(rel, []))

    def add(rel, node, kind, op, dist, knob, tags, parents):
        key = (rel, node.lineno, node.col_offset, kind, op)
        if key in seen or _skip(node, parents):
            return
        seen.add(key)
        before = _unparse(node)
        m = Mutant(rel, node.lineno, node.col_offset, kind, op, dist, knob, before, _after(op, before, node), tags=tags)
        ex = executed_line(rel, node.lineno)
        if ex is False:
            return
        m.priority = 3 - dist + (1 if ex else 0)
        for r in rel_by_knob.get(knob or "", []):
            c, fam = r["c"], r["family"]
            want = ({"xdiv2", "div2"} if fam == "x" and abs(c - 0.5) < 1e-9 else {"xmul2", "mul2"} if fam == "x" and abs(c - 2) < 1e-9
                    else {"xdiv10", "div10"} if fam == "x" and abs(c - 0.1) < 1e-9 else {"xmul10", "mul10"} if fam == "x" and abs(c - 10) < 1e-9
                    else {"add1"} if fam == "+" and c > 0 else {"sub1"} if fam == "+" else set())
            if op in want:
                m.priority += 6
                m.tags.append(f"implied by the verified relation on {r['knob']}")
        out.append(m)

    for rel, tree in trees:
        parents = {id(c): p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}
        for name, stmts, node in _scopes(tree):
            seeds = [s for s in stmts if _knob_reads(s, kset)]
            if not seeds:
                continue
            dists = _slice(stmts, seeds)
            in_slice = [s for s in stmts if id(s) in dists]
            names = set().union(*(_defs(s) for s in in_slice)) if in_slice else set()
            for s in in_slice:
                knob = next(iter(_knob_reads(s, kset)), None) or next(iter(_knob_reads(seeds[0], kset)))
                d = dists[id(s)]
                _mutants_of(s, d, knob, rel, add, parents, kset)
                for fname in _result_calls(s):  # into the repo function whose return value feeds the slice
                    if fname in funcs and fname != name:
                        fnode, fstmts, frel = funcs[fname]
                        rets = [t for t in fstmts if isinstance(t, ast.Return) and t.value is not None]
                        d2 = _slice(fstmts, rets, depth=1)
                        fparents = next((({id(c): p for p in ast.walk(t2) for c in ast.iter_child_nodes(p)})
                                         for r2, t2 in trees if r2 == frel), parents)
                        for t in fstmts:
                            if id(t) in d2:
                                _mutants_of(t, d + 1 + d2[id(t)], knob, frel, add, fparents, kset)
                for fname, pos in _calls_into(s, names, kset):  # one step into a repo function
                    if fname in funcs and fname != name:
                        fnode, fstmts, frel = funcs[fname]
                        params = [a.arg for a in fnode.args.args]
                        if params and params[0] == "self":
                            params = params[1:]
                        if pos < len(params):
                            seeds2 = [t for t in fstmts if params[pos] in _uses(t)]
                            d2 = _slice(fstmts, seeds2, depth=1)
                            fparents = next((({id(c): p for p in ast.walk(t2) for c in ast.iter_child_nodes(p)})
                                             for r2, t2 in trees if r2 == frel), parents)
                            for t in fstmts:
                                if id(t) in d2:
                                    _mutants_of(t, d + 1 + d2[id(t)], knob, frel, add, fparents, kset)
        # metric code, loop bounds, loader switches
        for name, stmts, node in _scopes(tree):
            metric = name != "<module>" and METRIC_FN.search(name)
            for s in stmts:
                for n in ast.walk(s):
                    if isinstance(n, ast.Call):
                        f = n.func.id if isinstance(n.func, ast.Name) else n.func.attr if isinstance(n.func, ast.Attribute) else ""
                        if f == "range":
                            for a in n.args:
                                if _number(a) is not None:
                                    for op in ("sub1", "add1", "div2", "mul2"):
                                        add(rel, a, "num", op, 2, None, ["loop bound"], parents)
                        if metric and f in REDUCTIONS:
                            add(rel, n, "Call", "red." + REDUCTIONS[f], 0, None, ["metric code"], parents)
                        for kw in n.keywords:
                            if kw.arg in LOADER_BOOLS and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, bool):
                                add(rel, kw.value, "bool", "not", 2, None, ["data pipeline", kw.arg], parents)
                    if metric and isinstance(n, ast.Compare) and len(n.ops) == 1 and isinstance(n.ops[0], (ast.Lt, ast.LtE, ast.Gt, ast.GtE)):
                        add(rel, n, "Compare", "cmpflip", 1, None, ["metric code"], parents)
    out.sort(key=lambda m: (-m.priority, m.dist, m.file, m.line, m.col, m.op))
    return out[:limit]


ARITH = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv)
NUMERIC_CALLS = {"len", "sum", "mean", "max", "min", "float", "int", "abs", "round", "count_nonzero", "numel", "size",
                 "item", "norm", "sqrt", "log", "exp", "nnz", "count", "amax", "amin", "prod"} | set(REDUCTIONS)
NON_NUMERIC_CALLS = {"range", "list", "dict", "set", "tuple", "str", "open", "format", "encode", "decode", "parse_args",
                     "ArgumentParser", "add_argument", "hexdigest", "md5", "sha1", "sha256", "get", "join", "split",
                     "replace", "strip", "zip", "enumerate", "map", "filter", "sorted", "reversed", "isinstance",
                     "type", "getattr", "setattr", "hasattr", "iter", "next", "copy", "deepcopy", "to", "cuda", "cpu",
                     "numpy", "tolist", "reshape", "view", "permute", "transpose", "unsqueeze", "squeeze", "load",
                     "Tensor", "tensor", "array", "zeros", "ones", "empty", "seed", "manual_seed", "DataLoader"}
PLUMBING = re.compile(r"parse_args|ArgumentParser|add_argument|os\.environ|hashlib|RUN_TAG|\.seed\(|manual_seed|"
                      r"random\.seed|logging\.|wandb\.|SummaryWriter|tqdm\(")


def _call_name(n: ast.Call) -> str:
    return n.func.id if isinstance(n.func, ast.Name) else n.func.attr if isinstance(n.func, ast.Attribute) else ""


def _numericish(n: ast.AST, parents: dict[int, ast.AST]) -> bool:
    """An expression that is plausibly a number: arithmetic, a shape lookup, a numeric call, a repo function's
    result, or an operand of arithmetic."""
    if isinstance(n, ast.BinOp) and isinstance(n.op, ARITH + (ast.Pow,)):
        return True
    if isinstance(n, ast.Subscript):
        v = n.value
        return isinstance(v, ast.Attribute) and v.attr in ("shape", "size") or isinstance(_parent(n, parents), ast.BinOp)
    if isinstance(n, ast.Call):
        f = _call_name(n)
        if f in NON_NUMERIC_CALLS or f in SKIP_CALLS:
            return False
        return f in NUMERIC_CALLS or (bool(f) and not f[0].isupper()) and isinstance(_parent(n, parents), (ast.BinOp, ast.Assign, ast.Return))
    if isinstance(n, (ast.Name, ast.Attribute)):
        p = _parent(n, parents)
        return isinstance(p, ast.BinOp) and isinstance(p.op, ARITH)
    return False


def _parent(n, parents):
    return parents.get(id(n))


def _in_test(n: ast.AST, parents: dict[int, ast.AST]) -> bool:
    """Inside a comparison or a condition (`a.lr == 0.1`, the test of an if-expression)."""
    child, p = n, parents.get(id(n))
    while p is not None:
        if isinstance(p, ast.Compare):
            return True
        if isinstance(p, (ast.IfExp, ast.If, ast.While)) and getattr(p, "test", None) is child:
            return True
        child, p = p, parents.get(id(p))
    return False


def _mutants_of(stmt: ast.stmt, dist: int, knob: str | None, rel: str, add, parents, kset: set[str]) -> None:
    """The mutants of one statement on a knob's slice: arithmetic only (the statement's value if it is numeric, the
    operands of its arithmetic, numeric literals used as operands or call arguments), reductions; statements of
    configuration plumbing, seeding and logging are skipped."""
    value = getattr(stmt, "value", None) if isinstance(stmt, (ast.Assign, ast.AugAssign, ast.AnnAssign, ast.Return,
                                                              ast.Expr)) else None
    if value is None:
        return
    try:
        text = ast.unparse(stmt)
    except Exception:  # noqa: BLE001
        text = ""
    if PLUMBING.search(text):
        return
    done: set[int] = set()

    def expr(n):
        if id(n) in done or (isinstance(n, ast.Attribute) and _knob_reads(n, kset)):
            return
        done.add(id(n))
        for op in EXPR_OPS[:2]:
            add(rel, n, type(n).__name__, op, dist, knob, [], parents)

    if _numericish(value, parents) or isinstance(value, ast.BinOp):
        expr(value)  # the statement's whole value: one site for the chain
    for n in ast.walk(value):
        if _in_test(n, parents):
            continue
        if isinstance(n, ast.BinOp) and isinstance(n.op, ARITH):
            for side in (n.left, n.right):
                if _number(side) is None and _numericish(side, parents) and side is not value:
                    expr(side)
        elif _number(n) is not None:
            p = parents.get(id(n))
            if isinstance(p, ast.BinOp) or (isinstance(p, ast.Call) and n in p.args and _call_name(p) != "range"):
                for op in NUM_OPS[:4]:
                    add(rel, n, "num", op, dist, knob, [], parents)
        elif isinstance(n, ast.Call) and _call_name(n) in REDUCTIONS:
            add(rel, n, "Call", "red." + REDUCTIONS[_call_name(n)], dist, knob, [], parents)
