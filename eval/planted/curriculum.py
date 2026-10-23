"""A progressive planted-gap curriculum on papers GapFinder already reproduces (plan D7.4, docs/CONTEXT_v11.md 7.2).

    python eval/planted/curriculum.py make   --level 1 --cases pygcn,fastgcn,b3a --per-case 2 --seed 1
    python eval/planted/curriculum.py search --level 1 --code <frozen worktree> [--parallel 3]
    python eval/planted/curriculum.py score  [--level 1]
    python eval/planted/curriculum.py run    --cases ... --code <frozen worktree>     # levels in turn, gated

Each task is a real paper's container and harness with hidden changes: the "paper's" numbers are the mean of runs
with them, the reproduction runs without. GapFinder searches with the case's spec and the task's targets, no paper
and no ledger (`--hypotheses repomap`, no model call). Causes are drawn by a seeded generator before any search,
from the families below; the answers are sealed (eval/planted/curriculum/sealed/) and read only by `score`.

Levels (each mixes in gap-free controls, about one task in five):
1. one clear cause (>= 5 pooled standard deviations; a draw between 3 and 5 is banked as a level-2 task): a setting,
   a scale or unit convention, a code defect, a data-pipeline defect, and on a rebuilt harness (`<case>-h`:
   eval/planted/rebuild_harnesses.py) a reporting rule (each metric's best epoch), the paper-era code, or a package
   release from the paper's time;
2. one subtle cause (3 to 5 standard deviations), the same families;
3. two causes of one family, each moving the target by >= 2 standard deviations alone, the gap closed only by both;
4. two causes of different families (a setting and a code defect, a scale convention and a data defect, ...);
5. adversarial: a cause outside every family GapFinder searches (a string choice in the code: `relu` -> `tanh`,
   `mean` -> `sum`), alone (the right answer is to say it can't explain it) or with a setting (the right answer is
   the setting and "partially explained"); and gap-free controls.
A level opens only when the previous one's gap tasks reach `--pass` correct (0.7), with no confidently wrong answer
on a gap task or a control (controls are scored apart: saying nothing is right on them).

Verdicts: correct (every planted part found), partial (some), missed, confidently wrong (Explained, Paper-artifact
inconsistency or a reporting rule without the planted parts; for a control or an outside cause, any of those).
These are development measurements: the builder knows every family. They are never blind evidence, and no change
is judged on a planted task (a failure counts when its family keeps failing on fresh draws).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import random
import statistics
import subprocess
import sys
from pathlib import Path

HERE_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE_ROOT))
import plant  # noqa: E402  (the draws, the scorer's matching)

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(os.environ.get("GF_CURRICULUM_DIR") or HERE_ROOT / "curriculum")
TASKS, SEALED, WORK = HERE / "tasks", HERE / "sealed", HERE / "work"
# each task's search output folder; another name keeps a second engine version's searches of the same tasks apart
# (`--run run-c2`: two frozen versions compared on one fresh batch)
RUN = os.environ.get("GF_CURRICULUM_RUN", "run")
SCRATCH = os.environ.get("GF_SCRATCH", "")
EXT = ROOT / "eval" / "external"
CASES = {  # name -> (spec, a recorded run whose events hold the base checkpoint and the local source)
    "pygcn": ("devset/pygcn/pygcn.yaml", "devset/pygcn/run"),
    "fastgcn": ("blind-1/fastgcn.yaml", "blind-1/run"),
    "b3a": ("batch3/b3a/b3a.yaml", "batch3/b3a/run"),
    "b3c": ("batch3/b3c/b3c.yaml", "batch3/b3c/run"),
    "b4a": ("batch4/b4a/b4a.yaml", "batch4/b4a/run"),
    "vgae": ("devset/vgae/vgae.yaml", "devset/vgae/run"),
}
CONFIDENT = ("Explained", "Paper-artifact inconsistency", "Explained by the reporting rule")
LEVELS = {
    1: {"families": ["setting", "scale", "code", "data", "reporting", "era", "library"], "causes": 1, "min_sd": 5.0,
        "max_sd": None},
    2: {"families": ["setting", "scale", "code", "data", "reporting", "era", "library"], "causes": 1, "min_sd": 3.0,
        "max_sd": 5.0},
    3: {"families": ["setting", "code"], "causes": 2, "same": True, "min_sd": 5.0, "each_sd": 2.0},
    4: {"families": ["setting", "scale", "code", "data"], "causes": 2, "same": False, "min_sd": 5.0, "each_sd": 2.0},
    5: {"families": ["outside", "outside+setting"], "causes": 1, "min_sd": 5.0},
}
# string choices a program makes that no GapFinder family searches (they are neither flags nor numbers)
ACTIVATIONS = {"relu", "elu", "tanh", "sigmoid", "leaky_relu", "selu", "softplus"}
# the families only a rebuilt harness (`<case>-h`) can plant: a `<case>-h` draws from these alone, so its tasks are
# the ones the hand harness can't make; the hand harness draws the others
HARNESS_FAMILIES = {"reporting", "era", "library"}
CHOICE_GROUPS = [{"relu", "tanh", "elu", "sigmoid", "gelu", "leaky_relu", "selu"}, {"mean", "sum", "max", "add"},
                 {"adam", "sgd", "adagrad", "rmsprop", "adamw"}, {"both", "right", "left", "none"},
                 {"xavier", "kaiming", "normal", "uniform", "orthogonal"}, {"l1", "l2", "max"}]


# ------------------------------------------------------------------ the case's container

def case_env(name: str) -> dict[str, str]:
    """GF_DEV_BASE and GF_DEV_SOURCE from the case's recorded run (the checkpoint its spec ran on)."""
    spec_rel, run_rel = CASES[name]
    ev = EXT / run_rel / "events.jsonl"
    for line in ev.read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        if d.get("type") == "run_started":
            s = d["spec"]
            src = (s.get("source") or "").replace("<scratch>", SCRATCH).replace("\\", "/")
            return {"GF_DEV_BASE": s["base"], "GF_DEV_SOURCE": src}
    raise SystemExit(f"{name}: no run_started event in {ev}")


def rebuilt(name: str) -> Path | None:
    """`<case>-h`: the case's harness rebuilt by `gapfinder harness` (eval/planted/rebuild_harnesses.py), whose spec
    has per-epoch values, the paper-year packages and the paper-era commit (the reporting, library and era families)."""
    if not name.endswith("-h"):
        return None
    p = HERE / "harness" / name[:-2] / "spec.yaml"
    return p if p.exists() else None


def resolved_spec(name: str) -> Path:
    """The case's spec with the recorded base checkpoint and local source written in (specs name their variables
    differently: GF_DEV_BASE, GF_B1_BASE, ...)."""
    import yaml

    if (h := rebuilt(name)) is not None:
        return h  # its base and source are written in already
    spec_rel, _ = CASES[name]
    d = yaml.safe_load((EXT / spec_rel).read_text(encoding="utf-8"))
    e = case_env(name)
    d["base"], d["source"] = e["GF_DEV_BASE"], e["GF_DEV_SOURCE"]
    out = WORK / "specs" / f"{name}.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(d, sort_keys=False, width=400), encoding="utf-8")
    return out


def load_case(name: str):
    from gapfinder.sandbox.spec import HarnessSpec

    p = resolved_spec(name)
    spec = HarnessSpec.load_yaml(p)
    if rebuilt(name) is not None:
        targets = json.loads((p.parent / "targets.json").read_text(encoding="utf-8"))
    else:
        spec_rel, _ = CASES[name]
        targets = json.loads(((EXT / spec_rel).parent / "targets.json").read_text(encoding="utf-8"))
    return spec, targets, p


# ------------------------------------------------------------------ the families

def draw_data(rng: random.Random, root: Path, spec) -> tuple[str, str, str] | None:
    from gapfinder.sandbox import ast_patch

    ms = [m for m in plant.frozen_mutants(root, [k for k in spec.knobs if not k.startswith("@")], limit=400)
          if "data pipeline" in m.tags
          and not (ast_patch.entry_script(root / m.file) and not ast_patch.direct_entry(spec.run.command, m.file))]
    if not ms:
        return None
    m = rng.choice(ms)
    return "data", m.name, m.describe()


def draw_code_only(rng: random.Random, root: Path, spec) -> tuple[str, str, str] | None:
    """A code defect that is not a data-pipeline edit (those are their own family)."""
    for _ in range(30):
        c = plant.draw_code(rng, root, spec)
        if c is None:
            return None
        if "data pipeline" not in c[2]:
            return c
    return None


# plan F10: DeepCrime's mutation operators (Humbatova, Jahangirova & Tonella, ISSTA 2021), drawn from a taxonomy of
# real deep-learning faults: the ones that are code edits, not settings (learning rate, epochs, batch size, dropout
# and patience are the setting family). They are the curriculum's own, not GapFinder's mutation operators, so a code
# or data task is not always a fault GapFinder itself generates. RRW removes weights regularisation, RAW adds it,
# WRB removes a layer's bias (WAB adds it), TRD removes part of the training data.
TORCH_OPTIM = {"Adam", "AdamW", "SGD", "Adagrad", "RMSprop", "Adadelta", "Adamax", "NAdam", "RAdam"}
LAYER_CALL = ("Linear", "Dense", "Conv1d", "Conv2d", "Conv3d", "Conv", "GraphConvolution", "GraphConv", "GCNConv",
              "SAGEConv", "GATConv", "ChebConv", "Bilinear")
TRAIN_IDX = ("idx_train", "train_idx", "train_index", "train_indices", "train_ids", "train_nodes", "train_edges")
# the share of the training data kept, spread over it (every i with 7i mod 10 below k): not the first half or three
# quarters, which is the engine's own operator since c4 (plan H5: the engine must find the class, not its expression)
TRD_KEEP = (4, 6)
_DC_SITES: dict[tuple[str, str], list] = {}


def deepcrime_sites(fam: str, root: Path, spec) -> list[tuple[str, str, str, dict]]:
    """(knob, description, operator, equivalent settings) for each DeepCrime site the patch hook reaches. The
    equivalent settings are the flags the edit amounts to (the optimizer's weight_decay=args.weight_decay removed is
    weight_decay=0): the scorer accepts them."""
    key = (fam, str(root))
    if key in _DC_SITES:
        return _DC_SITES[key]
    import ast

    from gapfinder.harness_auto import _import_closure
    from gapfinder.sandbox import ast_patch
    from gapfinder.search.mutation import _knob_reads, _norm

    names = {_norm(k): k for k in spec.knobs if not k.startswith("@")}
    trees = [(p, t) for p, t in _import_closure(root.resolve()) if t is not None and p.is_relative_to(root.resolve())]
    reached = _reached({p.relative_to(root.resolve()).as_posix(): t for p, t in trees}, spec)
    trees = [(p, t) for p, t in trees if p.relative_to(root.resolve()).as_posix() in reached]
    params = {}  # a repo function's or class's parameters, with their defaults
    for _, tree in trees:
        for n in ast.walk(tree):
            fn = n if isinstance(n, ast.FunctionDef) else next(
                (b for b in n.body if isinstance(b, ast.FunctionDef) and b.name == "__init__"), None) \
                if isinstance(n, ast.ClassDef) else None
            if fn is not None:
                a = fn.args
                ds = [None] * (len(a.args) - len(a.defaults)) + list(a.defaults)
                params[n.name] = [(x.arg, d) for x, d in zip(a.args, ds) if x.arg != "self"]
    equiv = lambda node, v: {names[k]: v for k in _knob_reads(node, set(names))}  # noqa: E731
    out = []
    for p, tree in trees:
        rel = p.relative_to(root.resolve()).as_posix()
        if ast_patch.entry_script(p) and not ast_patch.direct_entry(spec.run.command, rel):
            continue
        torch = any("torch" in ast.unparse(x) for x in tree.body if isinstance(x, (ast.Import, ast.ImportFrom)))
        parents = {id(c): q for q in ast.walk(tree) for c in ast.iter_child_nodes(q)}
        for n in ast.walk(tree):
            at = lambda node, op: f"@ast:{rel}:{node.lineno}:@mut.{node.col_offset}.{type(node).__name__}.{op}"  # noqa: E731
            if fam == "code" and isinstance(n, ast.Call):
                f = n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", "")
                kws = {k.arg: k.value for k in n.keywords}
                if f in TORCH_OPTIM and torch:
                    wd = kws.get("weight_decay")
                    if wd is not None and not (isinstance(wd, ast.Constant) and not wd.value):
                        out.append((at(n, ast_patch.kwset_op("weight_decay", "0")),
                                    f"{rel}:{n.lineno}: `{ast.unparse(n)}` without its weight decay (DeepCrime RRW)",
                                    "RRW", equiv(wd, "0")))
                    elif wd is None:
                        out.append((at(n, ast_patch.kwset_op("weight_decay", "5e-4")),
                                    f"{rel}:{n.lineno}: `{ast.unparse(n)}` with weight_decay=5e-4 (DeepCrime RAW)",
                                    "RAW", {}))
                if f == "l2_loss":  # TensorFlow: loss += weight_decay * tf.nn.l2_loss(w)
                    q = parents.get(id(n))
                    node = q if isinstance(q, ast.BinOp) and isinstance(q.op, ast.Mult) else n
                    out.append((at(node, ast_patch.set_op("0.0")),
                                f"{rel}:{node.lineno}: `{ast.unparse(node)}` -> `0.0` (DeepCrime RRW)", "RRW",
                                equiv(node, "0")))
                if f in LAYER_CALL and not (isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name)
                                            and n.func.value.id == "self"):  # self.linear(x) calls a layer built
                    ps = params.get(f)
                    if ps is not None:
                        pname = next((x for x, _ in ps if x in ("bias", "use_bias")), None)
                        idx = [x for x, _ in ps].index(pname) if pname else 0
                        default = dict(ps).get(pname)
                        if pname is None or len(n.args) > idx:
                            continue
                    elif "keras" in ast.unparse(n.func) or f == "Dense":
                        pname, default = "use_bias", None
                    elif torch and not (f == "Linear" and len(n.args) > 2):
                        pname, default = "bias", None
                    else:
                        continue
                    cur = kws.get(pname, default)
                    on = not (isinstance(cur, ast.Constant) and cur.value is False)
                    out.append((at(n, ast_patch.kwset_op(pname, "False" if on else "True")),
                                f"{rel}:{n.lineno}: `{ast.unparse(n)}` with {pname}={not on} "
                                f"(DeepCrime {'WRB' if on else 'WAB'})", "WRB" if on else "WAB", {}))
            if fam == "data" and isinstance(n, ast.Assign) and len(n.targets) == 1 \
                    and isinstance(n.targets[0], ast.Name) and n.targets[0].id.lower() in TRAIN_IDX:
                v = n.value
                for k in TRD_KEEP:
                    keep = f"[i for i in range(len(_v)) if (i * 7) % 10 < {k}]"
                    expr = (f"(lambda _v: _v[__import__('numpy').array({keep})] if hasattr(_v, 'shape') "
                            f"else [_v[i] for i in {keep}])({ast.unparse(v)})")
                    out.append((at(v, ast_patch.set_op(expr)),
                                f"{rel}:{v.lineno}: `{n.targets[0].id}` keeps {k}0% of the training data, spread "
                                "over it (DeepCrime TRD)", "TRD", {}))
    _DC_SITES[key] = out
    return out


def _reached(trees: dict, spec) -> set[str]:
    """The repo files a run reaches: the import graph from the scripts the run command starts, not through a module
    that is one of several alternatives in its folder when the command or a knob's default names another (a repo of
    many models, the run naming one: SparseTSF's models/Informer.py, and the layers only it imports, never run).
    Every file when the command starts no script of the repo."""
    import ast
    import re

    cmd = spec.run.command
    scripts = set(re.findall(r"([\w.-]+)\.py\b", cmd))  # the scripts the command starts (python -u x.py too)
    entries = [r for r in trees if r.rsplit("/", 1)[-1][:-3] in scripts]
    # a value the command passes (--model SparseTSF) or a knob's default, never a flag's name (--model: gae/model.py)
    named = set(re.findall(r"--?[\w-]+[ =]['\"]?([A-Za-z_]\w{2,})", cmd)) | {str(k.default) for k in spec.knobs.values()}
    by_dir: dict[str, list[str]] = {}
    for rel in trees:
        d, _, f = rel.rpartition("/")
        if f != "__init__.py":
            by_dir.setdefault(d, []).append(rel)
    skip = set()
    for d, rels in by_dir.items():
        chosen = [r for r in rels if r.rsplit("/", 1)[-1][:-3] in named]
        if len(rels) >= 3 and chosen:
            skip |= set(rels) - set(chosen)

    def edges(rel, tree):
        d = rel.rpartition("/")[0]
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom):
                up = d.split("/")[:len(d.split("/")) - (n.level - 1)] if n.level and d else []
                bases = ["/".join(up)] if n.level else ["", d]
                mod = (n.module or "").replace(".", "/")
                for b in bases:
                    stem = "/".join(x for x in (b, mod) if x)
                    yield from (f"{stem}.py", f"{stem}/__init__.py")
                    yield from (f"{stem}/{a.name}.py" for a in n.names)
            elif isinstance(n, ast.Import):
                for a in n.names:
                    for b in ("", d):
                        stem = "/".join(x for x in (b, a.name.replace(".", "/")) if x)
                        yield from (f"{stem}.py", f"{stem}/__init__.py")

    todo = list(entries)
    if not todo:
        return set(trees)
    seen = set(todo)
    while todo:
        rel = todo.pop()
        for e in edges(rel, trees[rel]):
            if e in trees and e not in seen and e not in skip:
                seen.add(e)
                todo.append(e)
    return seen


def unplantable(fam: str, spec, root: Path, flags, lits, spec_p: Path) -> str | None:
    """Plan F10: why a family can't be planted on this case (None: it can be drawn). Printed once per case, so a
    family missing from a batch has its reason in the log."""
    from gapfinder import env_year

    base = fam.split("+")[0]
    r = random.Random(0)
    if base == "setting":
        return None if flags or lits else "no flag or named literal to change"
    if base == "scale":
        return None if plant.draw_scale(r, flags) else "no numeric flag whose values stay valid at x2, x0.5 or x0.01"
    if base == "code":
        return None if (plant.draw_code(r, root, spec) or deepcrime_sites("code", root, spec)) else \
            "no mutant or DeepCrime site (optimizer, layer, l2 loss) the patch hook reaches"
    if base == "data":
        return None if (draw_data(r, root, spec) or deepcrime_sites("data", root, spec)) else \
            "no data-pipeline site (split fraction, filter threshold, loader switch, normalisation fit, training " \
            "indices) the patch hook reaches"
    if base == "outside":
        return None if draw_outside(r, root, spec) else "no string choice (activation, reduction, optimizer) to swap"
    if base == "era":
        if env_year.ERA_KNOB in spec.knobs:
            return None
        h = spec_p.parent / "HARNESS.md"
        why = next((ln.strip(" -*") for ln in (h.read_text(encoding="utf-8").splitlines() if h.exists() else [])
                    if "no paper-era code knob" in ln), "")
        return why or "the harness has no paper-era code knob"
    if base == "library":
        pins = (spec.library or {}).get("pins") or {}
        kn = spec.knobs.get(env_year.KNOB)
        if not pins:
            return "the harness pins no package release from the paper's time"
        return None if kn and [c for c in kn.choices if c != "0"] else "no paper-era release installs"
    if base == "reporting":
        return None if any(m.endswith("__x_best") for m in spec.metrics) else "the run prints no per-epoch values"
    return None


def draw_outside(rng: random.Random, root: Path, spec) -> tuple[str, str, str] | None:
    """A string choice in the code swapped for another of its kind (no GapFinder family changes strings)."""
    import ast

    from gapfinder.harness_auto import _import_closure
    from gapfinder.sandbox import ast_patch

    sites = []
    for p, tree in _import_closure(root.resolve()):
        if tree is None or not p.is_relative_to(root.resolve()):
            continue
        rel = p.relative_to(root.resolve()).as_posix()
        if ast_patch.entry_script(p) and not ast_patch.direct_entry(spec.run.command, rel):
            continue
        parents = {id(c): q for q in ast.walk(tree) for c in ast.iter_child_nodes(q)}
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in ACTIVATIONS:
                # an activation called by name (F.relu, tf.nn.relu): renamed to another (GapFinder's operators rename
                # reductions only)
                sites.append((rel, n, sorted(ACTIVATIONS - {n.func.attr}), "call"))
                continue
            if isinstance(n, ast.Attribute) and n.attr in ACTIVATIONS and not (
                    isinstance(parents.get(id(n)), ast.Call) and parents[id(n)].func is n):
                # an activation passed as a value (act=tf.nn.relu): the reference replaced
                sites.append((rel, n, sorted(ACTIVATIONS - {n.attr}), "ref"))
                continue
            if not (isinstance(n, ast.Constant) and isinstance(n.value, str)):
                continue
            p = parents.get(id(n))
            if not (isinstance(p, ast.keyword) or (isinstance(p, ast.Call) and n in p.args)
                    or isinstance(p, (ast.Assign, ast.Compare))):
                continue  # a choice passed or assigned, not a message or a path
            v = n.value.lower()
            group = next((g for g in CHOICE_GROUPS if v in g), None)
            if group is None or n.value != v:
                continue
            sites.append((rel, n, sorted(group - {v}), "string"))
    if not sites:
        return None
    rel, n, others, how = rng.choice(sites)
    new = rng.choice(others)
    if how == "call":
        knob = f"@ast:{rel}:{n.lineno}:@mut.{n.col_offset}.Call.red.{new}"
        return "outside", knob, f"{rel}:{n.lineno}: {n.func.attr}() -> {new}()"
    if how == "ref":
        expr = ast.unparse(n.value) + "." + new
        knob = f"@ast:{rel}:{n.lineno}:@mut.{n.col_offset}.Attribute.{ast_patch.set_op(expr)}"
        return "outside", knob, f"{rel}:{n.lineno}: {ast.unparse(n)} -> {expr}"
    knob = f"@ast:{rel}:{n.lineno}:@mut.{n.col_offset}.Constant.{ast_patch.set_op(repr(new))}"
    return "outside", knob, f"{rel}:{n.lineno}: {n.value!r} -> {new!r}"


def draw_family(fam: str, rng, spec, root, flags, lits):
    """(family, knob, value, description, extra) for one cause of a family, or None."""
    if fam == "setting":
        c = plant.draw(rng, flags, lits)
        if c is None:
            return None
        kind, k, v = c
        return ("setting", k, v, f"{k} = {v}", {"literal": kind == "literal", "default": dict(lits).get(k)})
    if fam == "scale":
        c = plant.draw_scale(rng, flags)
        if c is None:
            return None
        _, k, factor = c
        d0 = spec.knobs[k].default
        return ("scale", k, plant._fmt_c(plant._num(d0) * factor, d0), f"{k}: the paper's v is the code's {factor:g} x v",
                {"factor": factor})
    if fam in ("code", "data"):  # half from DeepCrime's operators where the code has their sites (plan F10)
        dc = deepcrime_sites(fam, root, spec)
        c = None if dc and rng.random() < 0.5 else draw_code_only(rng, root, spec) if fam == "code" \
            else draw_data(rng, root, spec)
        if c is not None:
            return (fam, c[1], "1", c[2], {})
        if not dc:
            return None
        k, desc, op, eq = rng.choice(dc)
        return (fam, k, "1", desc, {"source": "deepcrime", "op": op, "equiv": eq})
    if fam == "outside":
        c = draw_outside(rng, root, spec)
        return None if c is None else ("outside", c[1], "1", c[2], {})
    from gapfinder import env_year

    if fam == "era":  # the paper ran the repository's code as of its date; the reproduction runs a later commit
        if env_year.ERA_KNOB not in spec.knobs:
            return None
        return ("era", env_year.ERA_KNOB, "1", "the paper-era commit's code", {})
    if fam == "library":  # the paper ran package releases from its time: one, or all of them
        pins = (spec.library or {}).get("pins") or {}
        kn = spec.knobs.get(env_year.KNOB)
        values = [c for c in (kn.choices if kn else []) if c != "0"]
        if not pins or not values:
            return None
        v = rng.choice(values)
        dists = [d for d, x in pins.items() if v == "all" or x.get("dir", d) in v.split(",")]
        return ("library", env_year.KNOB, v,
                ", ".join(f"{d}=={pins[d]['old']}" for d in dists) + " (as of the paper's date)", {"dists": dists})
    if fam == "reporting":  # the paper reports each metric's best epoch (chosen on the test labels)
        if not any(m.endswith("__x_best") for m in spec.metrics):
            return None
        return ("reporting", "@reporting", "best", "each metric's best epoch, chosen with the test labels", {})
    raise ValueError(fam)


# ------------------------------------------------------------------ making tasks

API_HOST = "api.tokenfactory.nebius.com"


def _online() -> bool:
    import socket

    try:
        socket.getaddrinfo(API_HOST, 443)
        return True
    except OSError:
        return False


async def _wait_online(name: str) -> None:
    """A run started while the machine is offline fails at once (2026-10-21: DNS gone for several minutes; a
    whole case's draws failed in a row): wait for the Sandboxes API's name to resolve."""
    if _online():
        return
    print(f"  {name}: offline; waiting", flush=True)
    while not _online():
        await asyncio.sleep(30)


def _infra(runs) -> bool:
    """Every run of a draw ended in a Sandboxes or network error: the draw was never measured."""
    return bool(runs) and all(str(getattr(b.status, "value", b.status)) == "infra_error" for b in runs)


def _band_ok(level: int, moved: float) -> bool:
    lv = LEVELS[level]
    return moved >= lv["min_sd"] and (lv.get("max_sd") is None or moved < lv["max_sd"])


def _sweep_knob(rng: random.Random, flags) -> tuple[str, str] | None:
    """(knob, default) of a numeric flag with two valid sweep values, for a single-claim case's paper sweep."""
    pool = [(k, kn.default) for k, kn in flags if plant._num(kn.default) and not kn.choices
            and plant._bool(kn.default) is None
            and len(plant.scale_values(plant._num(kn.default), 1.0, plant._is_int(kn.default))) == 2]
    return rng.choice(pool) if pool else None


async def _sweep(orch, changes: dict, main: dict, k: str, d0: str, factor: float, tag: str, repeats: int,
                 best: bool = False) -> list[dict]:
    """The paper's numbers at two more values u of knob k (held-out claims at k=u, in the paper's units), run at
    factor x u in the code's, with the task's changes (each run's best epoch for a reporting task)."""
    m, out = main["metric"], []
    for u in plant.scale_values(plant._num(d0), factor, plant._is_int(d0)):
        pv = plant._fmt_c(u, d0)
        pr = await orch.fanout([{**changes, k: plant._fmt_c(u * factor, d0)}] * repeats,
                               [f"{tag}-{pv}-{j}" for j in range(repeats)])
        mk = f"{m}__x_best" if best else m
        pg = [b.parsed_metrics for b in pr if b.status == "succeeded" and mk in b.parsed_metrics]
        if len(pg) >= 2:
            out.append({**main, "claim_id": f"{main['claim_id']}@{k}={pv}", "held_out": True, "at": {k: pv},
                        "paper_value": round(statistics.mean(x[mk] for x in pg), 4)})
    return out


def _made(level: int, name: str, seed: int) -> int:
    return len(list(TASKS.glob(f"L{level}-{name}-s{seed}-*"))) if TASKS.exists() else 0


def _next_tag(level: int, name: str, seed: int) -> str:
    """One past the highest task number of the level on the case (a removed task's number is not reused)."""
    nums = [int(d.name.rsplit("-", 1)[1]) for d in TASKS.glob(f"L{level}-{name}-s{seed}-*")
            if d.name.rsplit("-", 1)[1].isdigit()] if TASKS.exists() else []
    return f"L{level}-{name}-s{seed}-{max(nums, default=0) + 1}"


def _controls(name: str, seed: int, levels: list[int]) -> int:
    """Controls already made on the case at these levels (the maker's own bookkeeping; nothing is printed)."""
    n = 0
    for lv_ in levels:
        for f in SEALED.glob(f"L{lv_}-{name}-s{seed}-*.json") if SEALED.exists() else []:
            n += json.loads(f.read_text(encoding="utf-8")).get("kind") == "control"
    return n


async def make(level: int, cases: list[str], per_case: int, seed: int, repeats: int = 3, tries: int = 10,
               concurrency: int = 8, control_rate: float = 0.2, parallel: int = 3) -> None:
    """Tasks for `level` on each case, `parallel` cases at a time. The single-cause levels (1 and 2) share one
    stream of draws: each draw is measured, then banked at the level whose band holds its effect (a setting drawn
    for level 1 that moves the target 3.5 sd is a level-2 task), so a measured draw is not wasted; a level's tasks
    made earlier count toward its `per_case`."""
    from gapfinder.sandbox.backend import InfraError

    sem = asyncio.Semaphore(parallel)

    async def one(name):
        async with sem:
            for attempt in range(4):  # a case resumes: made tasks count, measured draws are not measured again
                try:
                    await _make_case(level, name, per_case, seed, repeats, tries, concurrency, control_rate)
                    return
                except InfraError as exc:
                    print(f"{name}: Sandboxes error (attempt {attempt + 1} of 4): {str(exc)[:160]}", flush=True)
                    await asyncio.sleep(60 * (attempt + 1))
                except Exception as exc:  # noqa: BLE001 (one case's failure doesn't stop the others)
                    print(f"{name}: failed: {type(exc).__name__}: {str(exc)[:300]}", flush=True)
                    return

    await asyncio.gather(*(one(n) for n in cases))


async def _make_case(level, name, per_case, seed, repeats, tries, concurrency, control_rate) -> None:
    from gapfinder.sandbox.backend import make_backend
    from gapfinder.sandbox.events import EventLog
    from gapfinder.sandbox.runner import Orchestrator
    from gapfinder.sandbox.spec import Knob

    lv = LEVELS[level]
    bank = [1, 2] if level == 1 else [level]
    if all(_made(lv_, name, seed) >= per_case for lv_ in bank):
        print(f"{name}: its level {'/'.join(map(str, bank))} tasks are made", flush=True)
        return
    SEALED.mkdir(parents=True, exist_ok=True)
    spec, targets, spec_p = load_case(name)
    root = spec.code_root()
    if root is None or not root.exists():
        print(f"{name}: no local source ({spec.source}); skipped", flush=True)
        return
    main = next(t for t in targets if not t.get("held_out"))
    m = main["metric"]
    flags, lits = plant.candidates(spec, root)
    rng = random.Random(f"curriculum:{level}:{name}:{seed}")
    fams = [f for f in lv["families"] if (f.split("+")[0] in HARNESS_FAMILIES) == (rebuilt(name) is not None)]
    for f in list(fams):
        if why := unplantable(f, spec, root, flags, lits, spec_p):
            print(f"{name}: family {f} can't be planted: {why}", flush=True)
            fams.remove(f)
    if not fams:
        print(f"{name}: no family of level {level} applies", flush=True)
        return
    # plan F10: a case with one reported number can't tell causes that move it alike apart (E4), so each of its
    # tasks, controls too, also reports the number at two values of a flag (the paper's sweep, as papers report
    # sensitivity to a setting): the scale family's sweep is its own
    single = len(targets) == 1
    orch = Orchestrator(make_backend("contree"), spec, EventLog(WORK / f"L{level}-{name}-s{seed}.jsonl"),
                        concurrency=concurrency)
    base = await orch.fanout([{}] * 6, [f"base-{i}" for i in range(6)])
    good = [b for b in base if b.status == "succeeded" and m in b.parsed_metrics]
    if len(good) < 3:
        print(f"{name}: baseline failed ({len(good)} of 6 ran); skipped", flush=True)
        return
    ok = [b.parsed_metrics for b in good]
    mu0, sd0 = statistics.mean(x[m] for x in ok), statistics.stdev([x[m] for x in ok])
    # a drawn setting can make a run far slower (Fair Clustering's lmbda_tune runs a grid of fits): cut at five times
    # the slowest baseline run, and a cut draw is redrawn
    slow = max(b.resources.elapsed_s for b in good)
    spec.run.timeout = min(spec.run.timeout, max(120.0, 5 * slow))
    if "reporting" in fams:
        # plan G8: the reporting rule (each metric's best epoch) moves the numbers only where training ends past its
        # best; on the naive runs, best minus final in pooled standard deviations must reach the lowest band
        best = [x.get(f"{m}__x_best") for x in ok]
        gaps = [abs(b - x[m]) for b, x in zip(best, ok) if b is not None]
        lowest = min(LEVELS[lv_]["min_sd"] for lv_ in bank)
        if gaps and (statistics.mean(gaps) < lowest * max(sd0, 1e-12) or statistics.mean(gaps) <= 0.005 * abs(mu0)):
            print(f"{name}: family reporting can't be planted: the runs' best and final {m} differ by "
                  f"{statistics.mean(gaps):.3g}, under {lowest:g} sd ({sd0:.3g})", flush=True)
            fams.remove("reporting")
            if not fams:
                print(f"{name}: no family of level {level} applies", flush=True)
                return
    if sd0 == 0:  # a deterministic target: no subtle band in standard deviations, and two runs show a change
        bank = [lv_ for lv_ in bank if LEVELS[lv_].get("max_sd") is None]
        repeats = 2
    need = {lv_: per_case - _made(lv_, name, seed) for lv_ in bank}
    # controls are about one task in five of the case's tasks, however many real draws are redrawn
    quota = max(1, round(control_rate * per_case * len(bank))) - _controls(name, seed, bank)
    print(f"L{level} {name}: baseline {m} {mu0:.4g} +- {sd0:.3g} (slowest run {slow:.0f} s, cut at "
          f"{spec.run.timeout:.0f} s); to make: " + ", ".join(f"L{k} {v}" for k, v in need.items() if v > 0), flush=True)
    # each drawn change set is measured once (the era knob is a single draw), across resumed attempts: the kept
    # ones from the case's sealed answers, the rest from the maker's file (its own bookkeeping; nothing is printed)
    mfile = WORK / f"measured-L{level}-{name}-s{seed}.json"
    measured: set[tuple] = {tuple(tuple(x) for x in k) for k in
                            (json.loads(mfile.read_text(encoding="utf-8")) if mfile.exists() else [])}
    for lv_ in bank:
        for f in SEALED.glob(f"L{lv_}-{name}-s{seed}-*.json") if SEALED.exists() else []:
            a = json.loads(f.read_text(encoding="utf-8"))
            if a.get("parts"):
                measured.add(tuple(sorted((q["family"], q["knob"], q["value"]) for q in a["parts"])))
    i, lost, tried = 0, 0, {}
    while i < tries * per_case * len(bank) and lost < 20:
        i += 1
        open_ = [lv_ for lv_ in bank if need[lv_] > 0]
        if not open_:
            break
        await _wait_online(name)
        if quota > 0 and rng.random() < control_rate:  # a gap-free control: another draw of the same runs
            lc = rng.choice(open_)
            tag = _next_tag(lc, name, seed)
            runs = await orch.fanout([{}] * repeats, [f"{tag}-c{j}" for j in range(repeats)])
            got = [b.parsed_metrics for b in runs if b.status == "succeeded" and m in b.parsed_metrics]
            if _infra(runs):
                i, lost = i - 1, lost + 1
                await asyncio.sleep(60)
                continue
            if len(got) < 2:
                continue
            sw = _sweep_knob(rng, flags) if single else None
            extra = await _sweep(orch, {}, main, sw[0], sw[1], 1.0, tag, repeats) if sw else []
            _write(tag, name, lc, plant._paper(targets, got) + extra, {"kind": "control", "parts": []})
            need[lc] -= 1
            quota -= 1
            print(f"  {name} draw {i}: kept as {tag}", flush=True)  # the log never says what a task is
            continue
        if lv["causes"] == 2:
            f1 = rng.choice(fams)
            others = [f for f in fams if f != f1]
            if not lv.get("same") and not others:
                print(f"{name}: one family applies; level {level} needs two", flush=True)
                break
            f2 = f1 if lv.get("same") else rng.choice(others)
            picks = [f1, f2]
        else:
            picks = rng.choice(fams).split("+")
        parts = []
        for f in picks:
            c = draw_family(f, rng, spec, root, flags, lits)
            if c is None or any(c[1] == q[1] for q in parts):
                break
            parts.append(c)
        if len(parts) != len(picks):
            continue
        key = tuple(sorted((q[0], q[1], q[2]) for q in parts))
        if key in measured:
            continue
        measured.add(key)
        mfile.write_text(json.dumps(sorted(measured)), encoding="utf-8")
        changes = {}
        for fam, k, v, desc, extra in parts:
            if fam == "reporting":
                continue  # a reading of the runs, not a change to them
            if k.startswith("@ast:"):
                spec.knobs.setdefault(k, Knob(layer="environment", default=extra.get("default") or "0", env=True,
                                              choices=[] if extra.get("literal") else ["0", "1"]))
            changes[k] = v
        tag0 = f"L{level}-{name}-s{seed}-d{i}-{lost}"
        runs = await orch.fanout([changes] * repeats, [f"{tag0}-{j}" for j in range(repeats)])
        got = [b.parsed_metrics for b in runs if b.status == "succeeded" and m in b.parsed_metrics]
        if _infra(runs):  # not measured: drawn again later, and not counted as a try
            measured.discard(key)
            mfile.write_text(json.dumps(sorted(measured)), encoding="utf-8")
            print(f"  {name} draw {i}: Sandboxes or network error; not counted", flush=True)
            i, lost = i - 1, lost + 1
            await asyncio.sleep(60)
            continue
        if any(q[0] == "reporting" for q in parts):  # the paper's numbers: each run's best epoch, per metric
            got = [{**x, **{t["metric"]: x[f"{t['metric']}__x_best"] for t in targets
                            if f"{t['metric']}__x_best" in x}} for x in got]
        if len(got) < 2:
            print(f"  {name} draw {i}: runs failed", flush=True)
            continue
        mu = statistics.mean(x[m] for x in got)
        pooled = math.sqrt((sd0 ** 2 + statistics.stdev([x[m] for x in got]) ** 2) / 2) or 1e-12
        moved = abs(mu - mu0) / pooled
        tried.setdefault("+".join(q[0] for q in parts), []).append(moved)
        fits = [lv_ for lv_ in open_ if _band_ok(lv_, moved)] if abs(mu - mu0) > 0.005 * abs(mu0) else []
        if fits and len(parts) == 2:  # each cause must matter alone, and both are needed
            for fam, k, v, desc, extra in parts:
                one = await orch.fanout([{k: v}] * 2, [f"{tag0}-alone-{j}" for j in range(2)])
                g1 = [b.parsed_metrics[m] for b in one if b.status == "succeeded" and m in b.parsed_metrics]
                if not g1 or abs(statistics.mean(g1) - mu0) / pooled < lv["each_sd"] or \
                        abs(statistics.mean(g1) - mu) / pooled < lv["each_sd"]:
                    fits = []
                    break
        if not fits:
            print(f"  {name} draw {i}: moved {moved:.1f} sd: redrawn", flush=True)
            continue
        lk = fits[0]
        tag = _next_tag(lk, name, seed)
        extra_targets = []
        for fam, k, v, desc, extra in parts:
            if fam == "scale":  # the paper's sweep in its own units, run in the code's
                extra_targets += await _sweep(orch, changes, main, k, spec.knobs[k].default, extra["factor"], tag,
                                              repeats)
        if single and not extra_targets and (sw := _sweep_knob(rng, flags)):
            extra_targets += await _sweep(orch, changes, main, sw[0], sw[1], 1.0, tag, repeats,
                                          best=any(q[0] == "reporting" for q in parts))
        kind = "+".join(q[0] for q in parts)
        _write(tag, name, lk, plant._paper(targets, got) + extra_targets,
               {"kind": kind, "moved_sd": round(moved, 2),
                "parts": [{"family": f, "knob": k, "value": v, "desc": desc, **ex} for f, k, v, desc, ex in parts]})
        need[lk] -= 1
        print(f"  {name} draw {i}: kept as {tag}", flush=True)
    left = {k: v for k, v in need.items() if v > 0}
    if left:
        print(f"{name}: short of tasks after {i} draws ({lost} lost to the infrastructure): "
              + ", ".join(f"L{k} {v}" for k, v in left.items()), flush=True)
    # plan F10: a family whose draws never reach a level's band can't be planted on this case either: its draws
    # change the numbers too little (E7). Written to the maker's own file, not the log: which families a case's
    # draws missed says something about its tasks
    low = min(LEVELS[lv_]["min_sd"] for lv_ in bank)
    lines = [f"family {f} can't be planted: {len(ms)} draws measured, none moved {m} {low:g} sd (largest {max(ms):.1f})"
             for f, ms in sorted(tried.items()) if max(ms) < low]
    if lines:
        (WORK / f"families-L{level}-{name}-s{seed}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write(tag: str, case: str, level: int, targets: list[dict], answer: dict) -> None:
    d = TASKS / tag
    d.mkdir(parents=True, exist_ok=True)
    (d / "targets.json").write_text(json.dumps(targets, indent=1), encoding="utf-8")
    (d / "task.json").write_text(json.dumps({"case": case, "level": level}, indent=1), encoding="utf-8")
    (SEALED / f"{tag}.json").write_text(json.dumps({**answer, "case": case, "level": level}, indent=1), encoding="utf-8")


# ------------------------------------------------------------------ searching

def _score_sfx() -> str:
    return ("" if RUN == "run" else "-" + RUN) + ("" if SEED is None else f"-s{SEED}")


def _sfx() -> str:
    return "" if RUN == "run" else "-" + RUN


def search_one(tag: str, code: Path, max_runs: int, concurrency: int) -> int:
    """One task's search; a search that ended on a Sandboxes or network error (InfraError) is started again from
    scratch, up to four times, once the API's name resolves."""
    import shutil
    import time

    for attempt in range(4):
        while not _online():
            time.sleep(30)
        rc = _search_once(tag, code, max_runs, concurrency)
        err = (TASKS / tag / f"search{_sfx()}.err").read_text(encoding="utf-8", errors="replace")[-4000:]
        if rc == 0 or "InfraError" not in err:
            return rc
        shutil.copy(TASKS / tag / f"search{_sfx()}.err", TASKS / tag / f"search{_sfx()}.err.infra{attempt + 1}")
        time.sleep(120 * (attempt + 1))  # the next attempt resumes from this one's runs (_search_once)
    return rc


def _search_once(tag: str, code: Path, max_runs: int, concurrency: int) -> int:
    """A search cut off before its report (a lost machine, a Sandboxes error) is kept as `run.cut<k>`, and the new
    one resumes from every such event log (`--resume`: its succeeded, failed and timed-out runs are reused and count
    toward the run budget; infrastructure errors are not)."""
    t = json.loads((TASKS / tag / "task.json").read_text(encoding="utf-8"))
    spec_p = resolved_spec(t["case"])
    run = TASKS / tag / RUN
    cut = f"{RUN}.cut"
    if (run / "events.jsonl").exists() and not (run / "gap_report.json").exists():
        k = 1 + max((int(x.name[len(cut):]) for x in TASKS.joinpath(tag).glob(cut + "*")
                     if x.name[len(cut):].isdigit()), default=0)
        run.rename(TASKS / tag / f"{cut}{k}")
    elif run.exists() and not (run / "gap_report.json").exists():
        import shutil

        shutil.rmtree(run, ignore_errors=True)  # nothing ran in it
    resume = []
    for c in sorted(TASKS.joinpath(tag).glob(cut + "*")):
        if (c / "events.jsonl").exists():
            resume += ["--resume", str(c / "events.jsonl")]
    env = {**os.environ, "PYTHONPATH": str(code), "PYTHONIOENCODING": "utf-8"}
    py = str(ROOT / ".venv" / "Scripts" / "python.exe") if os.name == "nt" else sys.executable
    cmd = [py, "-P", "-m", "gapfinder.cli", "search", "--spec", str(spec_p), "--targets",
           str(TASKS / tag / "targets.json"), "--hypotheses", "repomap", "--backend", "contree", "--concurrency",
           str(concurrency), "--max-runs", str(max_runs), "--paper", f"planted {tag}", "--out", str(run)] + resume
    if os.environ.get("GF_CODE_PROPOSER") == "1":  # plan G6, on an engine that has it (c4 and later)
        cmd.append("--code-proposer")
    with open(TASKS / tag / f"search{_sfx()}.log", "w", encoding="utf-8") as out, \
            open(TASKS / tag / f"search{_sfx()}.err", "w", encoding="utf-8") as err:
        return subprocess.call(cmd, env=env, cwd=str(code), stdout=out, stderr=err)


SEED: int | None = None  # search only this seed's tasks (`search --seed`): a version judged on a batch made after it


def _unsearched(level: int | None, started: set[str]) -> list[str]:
    return [d.name for d in sorted(TASKS.iterdir()) if (level is None or d.name.startswith(f"L{level}-"))
            and (SEED is None or f"-s{SEED}-" in d.name)
            and (d / "task.json").exists() and d.name not in started
            and not (d / RUN / "gap_report.json").exists()] if TASKS.exists() else []


def search(level: int | None, code: Path, max_runs: int, concurrency: int, parallel: int,
           watch: Path | None = None) -> None:
    """Each task without a report, `parallel` at a time. With `watch`, tasks made meanwhile are searched too,
    until the file `watch` exists and nothing is left."""
    import time
    from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait

    started: set[str] = set()
    running = {}
    with ThreadPoolExecutor(parallel) as ex:
        while True:
            for tag in _unsearched(level, started)[: max(0, parallel - len(running))]:
                started.add(tag)
                running[ex.submit(search_one, tag, code, max_runs, concurrency)] = tag
                print(f"  {tag}: searching", flush=True)
            if not running and (watch is None or (watch.exists() and not _unsearched(level, started))):
                break
            done, _ = wait(list(running), timeout=60, return_when=FIRST_COMPLETED) if running else (set(), None)
            for f in done:
                print(f"  {running.pop(f)}: exit {f.result()}", flush=True)
            if not running and not done:
                time.sleep(30)


# ------------------------------------------------------------------ scoring

def _part_found(p: dict, res: dict) -> bool:
    changes, sets = res.get("changes") or {}, res.get("value_sets") or {}
    notes = " ".join(res.get("notes") or [])
    fam = p["family"]
    if fam == "reporting":
        return (res.get("reporting") or {}).get("rule") in ("best", "best+attarget")
    if fam == "era":
        return str(changes.get(p["knob"], "0")) not in ("0", "")
    if fam == "library":
        v = str(changes.get(p["knob"], "0"))
        if p["value"] == "all":  # every old release planted: the library probe's minimal subset is the answer
            return v not in ("0", "")
        return v == "all" or bool(set(p["value"].split(",")) & set(v.split(",")))
    if fam in ("code", "data"):
        site = p["desc"].split(": ", 1)[0]
        if any(plant._same(str(changes.get(k, "")), v) for k, v in (p.get("equiv") or {}).items()):
            return True  # a DeepCrime edit found as the setting it amounts to (weight_decay=0 for RRW)
        return p["knob"] in changes or bool(site and site in notes and "code change" in notes)
    if any(plant._knob_matches(k, p["knob"]) and (plant._same(v, p["value"]) or
                                                   any(plant._same(s, p["value"]) for s in sets.get(k, [])))
           for k, v in changes.items()):
        return True
    # plan F3: the planted value inside the interval GapFinder reports for that knob ("<v" / ">v": open past v)
    try:
        x = float(p["value"])
    except (TypeError, ValueError):
        return False
    for k, (lo, hi) in (res.get("value_intervals") or {}).items():
        if not (plant._knob_matches(k, p["knob"]) and k in changes):
            continue
        low = float("-inf") if str(lo).startswith("<") else float(str(lo).lstrip(">"))
        high = float("inf") if str(hi).startswith(">") else float(str(hi).lstrip("<"))
        if low <= x <= high:
            return True
    return False


def verdict(a: dict, res: dict) -> str:
    attr = res.get("attribution") or {}
    label = attr.get("confidence_label") or ("Reproduced" if res.get("status") == "reproduced" else "Unexplained")
    if a["kind"] == "control":
        return "confidently wrong" if label in CONFIDENT else "correct"
    if a["kind"] == "outside":
        return "confidently wrong" if label in CONFIDENT else "correct"
    parts = [p for p in a["parts"] if p["family"] != "outside"]
    found = [p for p in parts if _part_found(p, res)]
    if "outside" in a["kind"]:  # a setting plus a cause outside every family: the setting, and not fully explained
        if label == "Explained" and found:
            return "partial"
        if found:
            return "correct"
        return "confidently wrong" if label in CONFIDENT else "missed"
    if len(found) == len(parts) and label not in ("Unexplained", "Inconclusive", "Reproduced"):
        return "correct"
    if found:
        return "partial"
    return "confidently wrong" if label in CONFIDENT else "missed"


def _tied(a: dict, res: dict) -> bool:
    """A planted knob is among the configurations GapFinder says the target can't tell apart from its answer
    (`equivalent`): the search reached the cause and one number couldn't single it out. Reported beside the
    verdict, never counted as correct."""
    eq = [c.get("config") or {} for c in res.get("equivalent") or []]
    return any(plant._knob_matches(k, p["knob"]) for p in a["parts"] if p["family"] not in ("reporting", "outside")
               for c in eq for k in c)


def _credible(a: dict, res: dict) -> tuple[bool, float]:
    """Plan G7: (the planted cause is in the answer's credible set and the set has at most 3 members, its reciprocal
    rank there). The set is the answer, then the configurations GapFinder reports the claims can't tell apart from
    it, without the answer plus passengers (a configuration that holds the answer's changes is the same
    explanation). Scored beside the verdict, for ties no search can break: it rewards a small set that holds the
    cause, not a guess among them. A control or an outside cause has no planted set: (False, 0.0)."""
    parts = [q for q in a.get("parts") or [] if q["family"] != "outside"]
    if a["kind"] == "control" or not parts:
        return False, 0.0
    answer = res.get("changes") or {}
    holds = lambda x, y: all(k in x and plant._same(str(x[k]), str(v)) for k, v in y.items())  # noqa: E731
    cs = [answer] + [c for c in (e.get("config") or {} for e in res.get("equivalent") or [])
                     if c and not (answer and holds(c, answer))]
    seen, uniq = set(), []
    for c in cs:
        key = tuple(sorted((k, str(v)) for k, v in c.items()))
        if c and key not in seen:
            seen.add(key)
            uniq.append(c)
    for i, c in enumerate(uniq):
        if all(_part_found(q, {**res, "changes": c, "value_sets": {}, "value_intervals": {}}) for q in parts):
            return len(uniq) <= 3, 1.0 / (i + 1)
    return False, 0.0


def _knob_named(a: dict, res: dict) -> bool:
    """Every planted setting, scale or code knob is in GapFinder's answer, whatever value it gives (FastGCN:
    hidden1=160 for a planted hidden1=4, both lowering the target alike). Reported beside the verdict."""
    parts = [p for p in a["parts"] if p["family"] not in ("reporting", "outside")]
    changes = res.get("changes") or {}
    return bool(parts) and all(any(plant._knob_matches(k, p["knob"]) for k in changes) for p in parts)


def score(level: int | None = None) -> dict:
    rows = []
    for d in sorted(TASKS.iterdir()) if TASKS.exists() else []:
        if level is not None and not d.name.startswith(f"L{level}-"):
            continue
        if SEED is not None and f"-s{SEED}-" not in d.name:
            continue
        rep, ans = d / RUN / "gap_report.json", SEALED / f"{d.name}.json"
        if not rep.exists() or not ans.exists():
            continue
        a = json.loads(ans.read_text(encoding="utf-8"))
        r = json.loads(rep.read_text(encoding="utf-8"))
        res = (r.get("results") or r.get("claims") or [{}])[0]
        rows.append({"task": d.name, "level": a["level"], "case": a["case"], "kind": a["kind"],
                     "verdict": verdict(a, res), "tied": _tied(a, res), "knob": _knob_named(a, res),
                     "identifiable": res.get("identifiable"),
                     "in_set3": _credible(a, res)[0], "rr": round(_credible(a, res)[1], 3),
                     # plan G6: the verdict of the answer before the code proposer ran (the arm without it)
                     "verdict_pre": verdict(a, {**res, "changes": res["pre_proposer"]["changes"],
                                                "attribution": {"confidence_label": res["pre_proposer"]["label"]}})
                     if res.get("pre_proposer") else None,
                     "label": (res.get("attribution") or {}).get("confidence_label"),
                     "found": res.get("changes") or {}, "planted": [f"{p['family']}: {p['desc']}" for p in a["parts"]]})
    by = {}
    for x in rows:
        by.setdefault((x["level"], x["kind"]), []).append(x["verdict"])
    for (lv, kind), vs in sorted(by.items()):
        print(f"L{lv} {kind:22s} " + ", ".join(f"{v} {vs.count(v)}" for v in
                                              ("correct", "partial", "missed", "confidently wrong") if vs.count(v)))
    # gap tasks and controls apart: a control is easier (saying nothing is right), so a level's pass rate is the
    # gap tasks' alone, and the controls only have to stay free of confident answers
    lv_sum = {}
    for x in rows:
        blank = {"n": 0, "correct": 0, "partial": 0, "missed": 0, "confidently wrong": 0, "tied": 0, "knob": 0,
                 "in_set3": 0, "rr": 0.0}
        s = lv_sum.setdefault(x["level"], {**blank, "controls": dict(blank)})
        t = s["controls"] if x["kind"] == "control" else s
        t["n"] += 1
        t[x["verdict"]] += 1
        t["tied"] += x["verdict"] != "correct" and x["tied"]
        t["knob"] += x["verdict"] != "correct" and x["knob"]
        t["in_set3"] += bool(x.get("in_set3"))
        t["rr"] += x.get("rr") or 0.0
    for lv, s in sorted(lv_sum.items()):
        c = s["controls"]
        print(f"level {lv}: gap tasks {s['correct']}/{s['n']} correct, {s['partial']} partial, {s['missed']} missed, "
              f"{s['confidently wrong']} confidently wrong; of the rest, {s['knob']} name the planted knob at "
              f"another value, {s['tied']} have it among the configurations the target can't tell apart; "
              f"controls {c['correct']}/{c['n']} correct, "
              f"{c['confidently wrong']} confidently wrong")
    HERE.mkdir(parents=True, exist_ok=True)
    (HERE / f"scores{_score_sfx()}.json").write_text(
        json.dumps({"rows": rows, "levels": lv_sum, "run": RUN}, indent=1), encoding="utf-8")
    return lv_sum


def report(out: Path) -> None:
    """eval/results/planted_curriculum.md from the scorer's rows: per level and family, the verdicts, how many of
    the rest name the planted knob or tie it, and each task's line (planted cause, GapFinder's answer, label)."""
    data = json.loads((HERE / f"scores{_score_sfx()}.json").read_text(encoding="utf-8"))
    rows = data["rows"]
    L = ["# Planted-gap curriculum: results", "",
         "Generated by `eval/planted/curriculum.py report` from the scorer's output (eval/planted/curriculum/"
         "scores.json). Development measurements on papers GapFinder already reproduces: the builder knows every "
         "family, so these are never blind evidence, and no engine change is judged on them.", "",
         "Verdicts: correct (every planted part found, at the planted value within 10%), partial, missed, "
         "confidently wrong (a confident label without the planted cause; on a control, any confident label). "
         "\"Right knob\": GapFinder's answer changes the planted knob, at another value. \"Tied\": the planted "
         "knob is among the configurations GapFinder reports the target can't tell apart from its answer.", ""]
    for lv in sorted({x["level"] for x in rows}):
        rs = [x for x in rows if x["level"] == lv]
        gaps, ctl = [x for x in rs if x["kind"] != "control"], [x for x in rs if x["kind"] == "control"]
        L += [f"## Level {lv}", "",
              f"Gap tasks: {sum(x['verdict'] == 'correct' for x in gaps)}/{len(gaps)} correct, "
              f"{sum(x['verdict'] == 'confidently wrong' for x in gaps)} confidently wrong. Controls: "
              f"{sum(x['verdict'] == 'correct' for x in ctl)}/{len(ctl)} correct, "
              f"{sum(x['verdict'] == 'confidently wrong' for x in ctl)} confidently wrong.", "",
              "| Family | Tasks | Correct | Partial | Missed | Confidently wrong | Right knob, other value | Tied | "
              "In a credible set of at most 3 | Mean reciprocal rank |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for kind in sorted({x["kind"] for x in rs}):
            k = [x for x in rs if x["kind"] == kind]
            bad = [x for x in k if x["verdict"] != "correct"]
            L.append(f"| {kind} | {len(k)} | " + " | ".join(str(sum(x["verdict"] == v for x in k)) for v in
                     ("correct", "partial", "missed", "confidently wrong"))
                     + f" | {sum(bool(x.get('knob')) for x in bad)} | {sum(bool(x.get('tied')) for x in bad)} | "
                     f"{sum(bool(x.get('in_set3')) for x in k)} | {sum(x.get('rr') or 0 for x in k) / len(k):.2f} |")
        L += ["", "| Task | Planted | GapFinder's answer | Label | Verdict |", "|---|---|---|---|---|"]
        for x in rs:
            ans = ", ".join(f"`{k}={v}`" for k, v in (x.get("found") or {}).items()) or "none"
            L.append(f"| {x['task']} | {'; '.join(x['planted']) or 'nothing (control)'} | {ans} | "
                     f"{x.get('label') or '-'} | {x['verdict']} |")
        L.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {out}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("make", "run"):
        p = sub.add_parser(name)
        p.add_argument("--cases", default=",".join(CASES))
        p.add_argument("--per-case", type=int, default=2)
        p.add_argument("--seed", type=int, default=1)
        p.add_argument("--repeats", type=int, default=3)
        p.add_argument("--concurrency", type=int, default=8)
        p.add_argument("--tries", type=int, default=10)
        p.add_argument("--case-parallel", type=int, default=3)
        p.add_argument("--control-rate", type=float, default=0.2, help="0: gap tasks only (controls made earlier)")
        if name == "make":
            p.add_argument("--level", type=int, required=True)
        else:
            p.add_argument("--start", type=int, default=1)
            p.add_argument("--code", type=Path, required=True)
            p.add_argument("--max-runs", type=int, default=150)
            p.add_argument("--parallel", type=int, default=3)
            p.add_argument("--pass", dest="pass_rate", type=float, default=0.7)
    ps = sub.add_parser("search")
    ps.add_argument("--level", type=int)
    ps.add_argument("--seed", type=int, help="only this seed's tasks")
    ps.add_argument("--code", type=Path, required=True)
    ps.add_argument("--max-runs", type=int, default=150)
    ps.add_argument("--concurrency", type=int, default=8)
    ps.add_argument("--parallel", type=int, default=3)
    ps.add_argument("--watch", type=Path, help="keep searching new tasks until this file exists")
    pr = sub.add_parser("report")
    pr.add_argument("--out", type=Path, default=ROOT / "eval" / "results" / "planted_curriculum.md")
    pr.add_argument("--seed", type=int, help="the scores of this seed's tasks (`score --seed`)")
    pc = sub.add_parser("score")
    pc.add_argument("--level", type=int)
    pc.add_argument("--seed", type=int, help="only this seed's tasks")
    a = ap.parse_args()
    global SEED
    SEED = getattr(a, "seed", None) if a.cmd in ("search", "score", "report") else None
    if a.cmd == "make":
        asyncio.run(make(a.level, a.cases.split(","), a.per_case, a.seed, a.repeats, a.tries, a.concurrency,
                         control_rate=a.control_rate, parallel=a.case_parallel))
    elif a.cmd == "search":
        search(a.level, a.code.resolve(), a.max_runs, a.concurrency, a.parallel, a.watch)
    elif a.cmd == "report":
        report(a.out)
    elif a.cmd == "score":
        score(a.level)
    else:
        for level in range(a.start, 6):
            asyncio.run(make(level, a.cases.split(","), a.per_case, a.seed, a.repeats, a.tries, a.concurrency,
                             control_rate=a.control_rate, parallel=a.case_parallel))
            search(level, a.code.resolve(), a.max_runs, a.concurrency, a.parallel)
            s = score(level).get(level) or {"n": 0, "controls": {"confidently wrong": 0}}
            if not s["n"] or s["correct"] / s["n"] < a.pass_rate or s["confidently wrong"]                     or s["controls"]["confidently wrong"]:
                print(f"level {level} not passed: the curriculum stops here", flush=True)
                break
            print(f"level {level} passed: next level", flush=True)


if __name__ == "__main__":
    main()
