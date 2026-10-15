"""Static out-of-space checks (plain code, no LLM, no runs): where could a cause hide that no flag reaches?

When history matching says a gap is out of the exposed settings' reach, these checks list leads in the
artifact's code, each with file:line evidence:

- unexposed_setting: a hyperparameter-like literal (`batch_size = 128`, `T = 10000`,
  `predict(..., batch_size=500)`) that no command-line flag sets;
- file_setting: a setting read from a data file (`np.loadtxt(".../n_epochs.txt")`), with the values the
  repo's copies of that file hold;
- selection_in_code: a loop that keeps the best of several settings (grid search, best-of-k), and
  whether it scores on test data, which is leakage;
- fixed_seed: a hard-coded random seed;
- split_fraction: a hard-coded train/validation fraction.

They are leads, not findings: nothing here was run. Only Python is parsed; files that don't parse are
skipped. Validated on MC Dropout (eval/results/code_checks_mcdropout.md): the documented out-of-flag
differences (batch size 128, T = 10000, grid search instead of Bayesian optimisation) are all listed.
"""

from __future__ import annotations

import ast
import re
from dataclasses import asdict, dataclass
from pathlib import Path

# identifier tokens that name a training setting (weight 2) or an evaluation setting (weight 1)
_TRAIN = {"batch", "lr", "learning", "momentum", "decay", "l2", "lengthscale", "dropout", "tau", "epoch",
          "epochs", "iter", "iters", "iterations", "steps", "warmup", "clip", "hidden", "units", "layers",
          "temperature", "eps", "epsilon", "beta1", "beta2", "gamma", "alpha", "lambda", "reg", "patience",
          "prior", "noise", "precision", "width", "depth"}
_EVAL = {"samples", "mc", "passes", "draws", "topk", "beam", "threshold"}
_EXACT = {"T": 1, "K": 1}  # single-letter names used for sample counts
_EVAL_CALLS = {"predict", "evaluate", "eval", "test", "score", "sample"}
_SKIP_PREFIX = ("best_", "n_split", "num_split", "split_num")
_SETTING_FILE_RE = re.compile(r"""['"]([\w./-]*?(\w+)\.(?:txt|json|ya?ml|cfg|ini))['"]""")


@dataclass
class Lead:
    family: str
    file: str
    line: int
    code: str
    detail: str
    weight: int = 1
    name: str = ""  # unexposed_setting: the variable or keyword, and its literal (a patch knob can set it)
    value: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def _tokens(name: str) -> set[str]:
    parts = re.split(r"_|(?<=[a-z])(?=[A-Z])", name)
    return {p.lower() for p in parts if p}


def _weight(name: str) -> int:
    if name in _EXACT:
        return _EXACT[name]
    if name.lower().startswith(_SKIP_PREFIX):
        return 0
    t = _tokens(name)
    return 2 if t & _TRAIN else 1 if t & _EVAL else 0


def _number(node: ast.AST) -> float | None:
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        v = _number(node.operand)
        return None if v is None else -v
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return float(node.value)
    return None


def _flag_dests(tree: ast.AST) -> set[str]:
    out = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "add_argument":
            for a in n.args:
                if isinstance(a, ast.Constant) and isinstance(a.value, str) and a.value.startswith("-"):
                    out.add(a.value.lstrip("-").replace("-", "_"))
            out |= {str(k.value.value) for k in n.keywords if k.arg == "dest" and isinstance(k.value, ast.Constant)}
    return out


def _call_name(call: ast.Call) -> str:
    f = call.func
    return f.attr if isinstance(f, ast.Attribute) else f.id if isinstance(f, ast.Name) else ""


def _mentions_test(node: ast.AST) -> bool:
    return any(isinstance(n, ast.Name) and "test" in n.id.lower() for n in ast.walk(node))


def _file_leads(path: Path, rel: str, flags: set[str], root: Path) -> list[Lead]:
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return []
    lines = text.splitlines()
    src = lambda n: lines[n.lineno - 1].strip()[:160] if 0 < n.lineno <= len(lines) else ""  # noqa: E731
    flags = flags | _flag_dests(tree)
    out: list[Lead] = []
    parents = {c: p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}
    for n in ast.walk(tree):
        # name = <number>
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            name, v = n.targets[0].id, _number(n.value)
            w = _weight(name)
            if v is not None and w and name not in flags and v not in (0.0, 1.0, -1.0):
                lit = ast.unparse(n.value)
                out.append(Lead("unexposed_setting", rel, n.lineno, src(n),
                                f"`{name} = {n.value.value if isinstance(n.value, ast.Constant) else v:g}` is fixed in "
                                "the code; no flag sets it", w, name=name, value=lit))
        if isinstance(n, ast.Call):
            cname = _call_name(n)
            # f(..., batch_size=500)
            for kw in n.keywords:
                v = _number(kw.value) if kw.arg else None
                w = _weight(kw.arg) if kw.arg else 0
                if v is not None and w and kw.arg not in flags and v not in (0.0, 1.0, -1.0):
                    where = "evaluation" if cname.lower() in _EVAL_CALLS else "the call"
                    out.append(Lead("unexposed_setting", rel, n.lineno, src(n),
                                    f"`{cname}(..., {kw.arg}={v:g})`: fixed in {where}; no flag sets it",
                                    1 if where == "evaluation" else w, name=kw.arg, value=ast.unparse(kw.value)))
            # np.random.seed(1), torch.manual_seed(0), random_state=42
            if cname in ("seed", "manual_seed", "set_seed") and n.args and _number(n.args[0]) is not None:
                out.append(Lead("fixed_seed", rel, n.lineno, src(n), f"random seed fixed to {_number(n.args[0]):g}"))
            for kw in n.keywords:
                if kw.arg == "random_state" and _number(kw.value) is not None:
                    out.append(Lead("fixed_seed", rel, n.lineno, src(n), f"random_state fixed to {_number(kw.value):g}"))
        # x = int(0.8 * X.shape[0])
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            name = n.targets[0].id.lower()
            if any(t in name for t in ("train", "val", "test", "split", "holdout")):
                for b in ast.walk(n.value):
                    if isinstance(b, ast.BinOp) and isinstance(b.op, ast.Mult):
                        for side in (b.left, b.right):
                            v = _number(side)
                            if v is not None and 0 < v < 1:
                                out.append(Lead("split_fraction", rel, n.lineno, src(n),
                                                f"`{n.targets[0].id}` uses a fixed fraction {v:g}; no flag sets it"))
        # selection: if <metric> > best_<metric>: best_x = ...
        if isinstance(n, ast.If) and isinstance(n.test, ast.Compare) and any(
                isinstance(o, (ast.Gt, ast.Lt, ast.GtE, ast.LtE)) for o in n.test.ops):
            names = {x.id for x in ast.walk(n.test) if isinstance(x, ast.Name)}
            kept = [t.id for s in n.body if isinstance(s, ast.Assign) for t in s.targets
                    if isinstance(t, ast.Name) and t.id.startswith("best")]
            if any(x.startswith("best") for x in names) and len(kept) >= 2:
                loops, p = [], parents.get(n)
                while p is not None:
                    if isinstance(p, ast.For):
                        loops.append(ast.unparse(p.target) + " in " + ast.unparse(p.iter)[:60])
                    p = parents.get(p)
                body = parents.get(n)
                on_test = body is not None and _mentions_test(body) and not any("val" in x.lower() for x in names)
                detail = (f"the code selects {', '.join(kept)} by comparing {ast.unparse(n.test)[:80]}"
                          + (f" over {'; '.join(reversed(loops))}" if loops else "")
                          + (": it scores on TEST data (leakage)" if on_test else
                             ": a tuning protocol the paper may describe differently (e.g. a different search, grid "
                             "or budget)"))
                out.append(Lead("selection_in_code", rel, n.lineno, src(n), detail, 3 if on_test else 2))
    # settings read from files: string literals naming a setting file
    seen = set()
    for m in _SETTING_FILE_RE.finditer(text):
        fname, stem = m.group(1), m.group(2)
        if not _weight(stem) or stem in seen or stem.startswith("_") or "result" in fname.lower():
            continue  # a fragment of a built path, or an output file
        if any(f == stem or f.startswith(stem + "_") for f in flags):
            continue  # the harness sets it (e.g. knob tau_values_energy for tau_values.txt)
        seen.add(stem)
        line = text[: m.start()].count("\n") + 1
        base = Path(fname).name
        vals = sorted({"/".join(p.read_text(encoding="utf-8", errors="replace").split())[:40]
                       for p in list(root.rglob(base))[:50] if p.is_file() and p.stat().st_size < 400})
        shown = ", ".join(vals[:6]) + (f" (+{len(vals) - 6} more)" if len(vals) > 6 else "")
        out.append(Lead("file_setting", rel, line, lines[line - 1].strip()[:160],
                        f"`{stem}` is read from {base}" + (f" (values in the repo: {shown})" if vals else "")
                        + "; no flag sets it", _weight(stem)))
    return out


def code_checks(root: str | Path, flags: set[str] | None = None, limit: int = 12) -> list[Lead]:
    """Leads for causes outside the exposed settings, best first. `flags`: knob names the harness sets."""
    root = Path(root)
    norm = {f.lstrip("-").replace("-", "_") for f in (flags or set())}
    out: list[Lead] = []
    for p in sorted(root.rglob("*.py")):
        if any(part.startswith(".") or part in ("tests", "test", "venv", ".venv", "site-packages") for part in p.parts):
            continue
        out += _file_leads(p, str(p.relative_to(root)).replace("\\", "/"), norm, root)
    seen, uniq = set(), []
    for lead in sorted(out, key=lambda x: (-x.weight, x.family != "selection_in_code", x.file, x.line)):
        key = (lead.file, lead.line, lead.family)
        if key not in seen:
            seen.add(key)
            uniq.append(lead)
    return uniq[:limit]
