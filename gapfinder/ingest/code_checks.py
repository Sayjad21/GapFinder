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
# keyword switches that only say how to run, never what is computed (left out of the switch leads)
_HOW_TO_RUN = {"verbose", "inplace", "pin_memory", "non_blocking", "exist_ok", "keepdim", "keepdims", "parents",
               "persistent_workers", "flush", "copy", "sort_keys", "ensure_ascii", "allow_pickle", "strict",
               "requires_grad", "retain_graph", "create_graph", "save", "log", "show", "debug", "quiet", "force"}
# names that hold ground truth (a prediction edited under a test on these uses the labels)
_LABEL_NAMES = {"gt", "label", "labels", "y_true", "ytrue", "target", "targets", "truth", "ground_truth", "test_labels"}
_PRED_NAMES = ("pred", "y_pred", "prediction", "predict", "yhat", "y_hat", "output", "detect")
# what well-known library switches do to an evaluation (library semantics, not one paper's): shown with the lead
SWITCH_EFFECT = {
    "drop_last": "drops the last incomplete batch, so part of the evaluation data is never scored and the "
                 "metric depends on the batch size",
}
# switches whose value doesn't change an aggregate evaluation metric (left out of the protocol tests)
_EVAL_NEUTRAL = {"shuffle", "pin_memory", "persistent_workers", "non_blocking"}


def _in_eval_branch(node, parents) -> bool:
    """Inside the body (not the else) of `if flag == 'test':`, or of an if testing a test/eval name."""
    child, p = node, parents.get(node)
    while p is not None:
        if isinstance(p, ast.If) and any(child is b or _contains(b, child) for b in p.body):
            for x in ast.walk(p.test):
                if isinstance(x, ast.Constant) and isinstance(x.value, str) and x.value.lower() in ("test", "eval", "evaluation"):
                    return True
                if isinstance(x, ast.Name) and any(w in x.id.lower() for w in ("test", "eval")):
                    return True
        child, p = p, parents.get(p)
    return False


def _contains(tree, node) -> bool:
    return any(x is node for x in ast.walk(tree))


def _neutral(name: str) -> bool:
    return any(w in name.lower() for w in _EVAL_NEUTRAL)
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
    # names passed on as a keyword (`DataLoader(..., drop_last=drop_last)`): a true/false assigned to one is a switch
    passed = {kw.value.id for c in ast.walk(tree) if isinstance(c, ast.Call) for kw in c.keywords
              if kw.arg and isinstance(kw.value, ast.Name)}
    for n in ast.walk(tree):
        # drop_last = True (PatchTST's test loader, set under `if flag == 'test'` and passed to the DataLoader)
        if (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
                and isinstance(n.value, ast.Constant) and isinstance(n.value.value, bool)
                and n.targets[0].id in passed and n.targets[0].id not in flags
                and n.targets[0].id.lower() not in _HOW_TO_RUN):
            out.append(Lead("unexposed_setting", rel, n.lineno, src(n),
                            f"`{n.targets[0].id} = {n.value.value}` is a switch passed on to a call; no flag sets it",
                            1, name=n.targets[0].id, value=str(n.value.value)))
            if _in_eval_branch(n, parents) and not _neutral(n.targets[0].id):  # a protocol, tested like one
                name = n.targets[0].id
                effect = SWITCH_EFFECT.get(name.lower(), "changes how the evaluation is computed")
                out.append(Lead("eval_switch", rel, n.lineno, src(n),
                                f"`{name} = {n.value.value}` is fixed in the evaluation branch: it {effect}", 3,
                                name=name, value=str(not n.value.value)))
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
            # f(..., drop_last=True): a true/false switch fixed in a call (PatchTST: the test loader's drop_last=True
            # drops the last batch, so the test set is not the whole test set; the numbers-only leads missed it)
            for kw in n.keywords:
                if (kw.arg and kw.arg not in flags and kw.arg.lower() not in _HOW_TO_RUN
                        and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, bool)):
                    out.append(Lead("unexposed_setting", rel, n.lineno, src(n),
                                    f"`{cname}(..., {kw.arg}={kw.value.value})`: a switch fixed in the call; no flag "
                                    "sets it", 1, name=kw.arg, value=str(kw.value.value)))
                    if not _neutral(kw.arg) and (
                            _in_eval_branch(n, parents) or _mentions_test(ast.Tuple(elts=list(n.args), ctx=ast.Load()))):
                        effect = SWITCH_EFFECT.get(kw.arg.lower(), "changes how the evaluation is computed")
                        out.append(Lead("eval_switch", rel, n.lineno, src(n),
                                        f"`{cname}(..., {kw.arg}={kw.value.value})` on evaluation data: it {effect}", 3,
                                        name=kw.arg, value=str(not kw.value.value)))
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
        # predictions edited under a test on the ground truth: `if gt[i] == 1 and pred[i] == 1: ... pred[j] = 1`
        # (point adjustment in time-series anomaly detection: a detected point marks its whole true segment as found,
        # Kim et al. AAAI 2022). The label decides the prediction, so the score uses the answer.
        if isinstance(n, ast.If):
            test_names = {x.id.lower() for x in ast.walk(n.test) if isinstance(x, ast.Name)}
            if test_names & _LABEL_NAMES:
                edits = [t for s in ast.walk(n) if isinstance(s, ast.Assign) for t in s.targets
                         if isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name)
                         and t.value.id.lower().startswith(_PRED_NAMES)]
                if edits:
                    out.append(Lead("label_in_prediction", rel, n.lineno, src(n),
                                    f"`{edits[0].value.id}` is changed under a test on the ground truth "
                                    f"({', '.join(sorted(test_names & _LABEL_NAMES))}): the score then uses the labels "
                                    "(e.g. point adjustment)", 3, name="@if", value="False"))
        # selection: if <metric> > best_<metric>: best_x = ...
        if isinstance(n, ast.If) and isinstance(n.test, ast.Compare) and any(
                isinstance(o, (ast.Gt, ast.Lt, ast.GtE, ast.LtE)) for o in n.test.ops):
            names = {x.id for x in ast.walk(n.test) if isinstance(x, ast.Name)}
            # `best_x = ...` or `best_hr, best_ndcg, best_iter = ...` (a tuple target names several at once)
            kept = [x.id for s in n.body if isinstance(s, ast.Assign) for t in s.targets
                    for x in (t.elts if isinstance(t, (ast.Tuple, ast.List)) else [t])
                    if isinstance(x, ast.Name) and x.id.startswith("best")]
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
                out.append(Lead("selection_in_code", rel, n.lineno, src(n), detail, 3 if on_test else 2,
                                name="@if" if on_test else "", value="True" if on_test else ""))
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


def _default_leads(files: list[tuple[Path, str]]) -> list[Lead]:
    """A numeric parameter default that no call in the repo overrides is a constant in disguise
    (devset VGAE: `def mask_test_edges(adj, test_percent=30., val_percent=20.)`, always called as
    `mask_test_edges(adj)`; the paper held out 10% and 5%)."""
    defs: list[tuple[str, int, str, str, str, int, str, float]] = []  # fn, line, rel, param, literal, position, code, value
    calls: dict[str, list[ast.Call]] = {}
    for path, rel in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(text)
        except (OSError, SyntaxError, ValueError):
            continue
        lines = text.splitlines()
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                a = n.args
                pos = a.args[len(a.args) - len(a.defaults):] if a.defaults else []
                start = len(a.args) - len(pos)
                pairs = [(arg, d, start + i) for i, (arg, d) in enumerate(zip(pos, a.defaults))]
                pairs += [(arg, d, None) for arg, d in zip(a.kwonlyargs, a.kw_defaults) if d is not None]
                for arg, d, idx in pairs:
                    v = _number(d)
                    if v is not None and v not in (0.0, 1.0, -1.0):
                        code = lines[n.lineno - 1].strip()[:160] if 0 < n.lineno <= len(lines) else ""
                        defs.append((n.name, n.lineno, rel, arg.arg, ast.unparse(d), -1 if idx is None else idx, code, v))
            elif isinstance(n, ast.Call):
                calls.setdefault(_call_name(n), []).append(n)
    out = []
    for fn, line, rel, param, lit, idx, code, v in defs:
        sites = calls.get(fn, [])
        if not sites:
            continue  # never called in the repo: not this program's constant
        if any(any(kw.arg == param for kw in c.keywords) or (idx >= 0 and len(c.args) > idx) for c in sites):
            continue  # some call sets it
        out.append(Lead("unexposed_setting", rel, line, code,
                        f"`{fn}(..., {param}={v:g})`: a default no call in the repo overrides ({len(sites)} call(s))",
                        max(2, _weight(param)), name=param, value=lit))
    return out


def _outermost_label_edits(leads: list[Lead], root: Path) -> list[Lead]:
    """A label-edit if nested in another (point adjustment: the outer test and its inner loops) is one finding."""
    spans: dict[str, list[tuple[int, int]]] = {}
    for x in leads:
        if x.family != "label_in_prediction":
            continue
        try:
            tree = ast.parse((root / x.file).read_text(encoding="utf-8", errors="replace"))
        except (OSError, SyntaxError, ValueError):
            continue
        for n in ast.walk(tree):
            if isinstance(n, ast.If) and n.lineno == x.line:
                spans.setdefault(x.file, []).append((n.lineno, getattr(n, "end_lineno", n.lineno)))
    def inside(x: Lead) -> bool:
        return any(a < x.line <= b for a, b in spans.get(x.file, []))
    return [x for x in leads if not (x.family == "label_in_prediction" and inside(x))]


def code_checks(root: str | Path, flags: set[str] | None = None, limit: int = 12) -> list[Lead]:
    """Leads for causes outside the exposed settings, best first. `flags`: knob names the harness sets."""
    root = Path(root)
    norm = {f.lstrip("-").replace("-", "_") for f in (flags or set())}
    out: list[Lead] = []
    files = []
    for p in sorted(root.rglob("*.py")):
        if any(part.startswith(".") or part in ("tests", "test", "venv", ".venv", "site-packages") for part in p.parts):
            continue
        rel = str(p.relative_to(root)).replace("\\", "/")
        files.append((p, rel))
        out += _file_leads(p, rel, norm, root)
    out += [x for x in _default_leads(files) if x.name not in norm]
    out = _outermost_label_edits(out, root)
    seen, uniq = set(), []
    for lead in sorted(out, key=lambda x: (-x.weight, x.family != "selection_in_code", x.file, x.line)):
        key = (lead.file, lead.line, lead.family, lead.name)  # two defaults on one def line are two leads
        if key not in seen:
            seen.add(key)
            uniq.append(lead)
    return uniq[:limit]


def named_literals(root: str | Path) -> list[Lead]:
    """Every named numeric literal in the repo's Python, unfiltered: `name = 5`, `self.name = 5`, `f(name=5)`
    and `def f(name=5)`. The inventory a paper's stated values are compared against (search/matcher.py)."""
    root = Path(root)
    out: list[Lead] = []
    for p in sorted(root.rglob("*.py")):
        if any(part.startswith(".") or part in ("tests", "test", "venv", ".venv", "site-packages") for part in p.parts):
            continue
        rel = str(p.relative_to(root)).replace("\\", "/")
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(text)
        except (OSError, SyntaxError, ValueError):
            continue
        lines = text.splitlines()
        src = lambda ln: lines[ln - 1].strip()[:160] if 0 < ln <= len(lines) else ""  # noqa: E731

        def add(name: str, node: ast.AST, line: int, how: str) -> None:
            if _number(node) is not None:
                out.append(Lead("named_literal", rel, line, src(line), how, 0, name=name, value=ast.unparse(node)))

        for n in ast.walk(tree):
            if isinstance(n, ast.Assign) and len(n.targets) == 1:
                t = n.targets[0]
                if isinstance(t, ast.Name):
                    add(t.id, n.value, n.lineno, "assignment")
                elif isinstance(t, ast.Attribute):
                    add(t.attr, n.value, n.lineno, "attribute")
            elif isinstance(n, ast.Call):
                for kw in n.keywords:
                    if kw.arg:
                        add(kw.arg, kw.value, n.lineno, f"keyword of {_call_name(n)}()")
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                a = n.args
                pos = a.args[len(a.args) - len(a.defaults):] if a.defaults else []
                for arg, d in list(zip(pos, a.defaults)) + [(x, d) for x, d in zip(a.kwonlyargs, a.kw_defaults) if d is not None]:
                    add(arg.arg, d, n.lineno, f"default of {n.name}()")
    return out
