"""The automatic harness, end to end (docs/CONTEXT_v11.md section 4, plan items 3-9).

    gapfinder harness <github url> --commit <sha> --local <checkout> --ledger <ledger dir> --target C7 --out dir/

One command, from a repo and a ledger to a spec a person approves. Only the environment step calls a model
(env-build, one shell command at a time); every other step is a fixed rule that refuses rather than guesses:
  0. static blockers (GPU-only packages, huge files) stop it before anything is spent (item 9);
  1. claims: the target plus every other cell of its table row (same conditions, other metrics) as held-outs;
  2. the command: the README or shell-script command that best matches the claims' words (item 3); a dataset
     flag set to another dataset is set to the claim's when exactly one of its known values matches;
  3. knobs: every flag of that script, parsed from its code, at the command's value or the code default;
     how-to-run flags (paths, devices, logging), the dataset and repeat-count flags stay fixed; seed flags get a
     new value every run; `type=bool` flags can't be set from a command line and are left out (with the reason);
  4. the environment (env-build), with the repo's data scripts and preprocessing commands in its goal (item 4);
  5. data: the data scripts and preprocessing run once more and the smoke run follows; then every new file that is
     data (under a data directory or a dataset loader's cache) is kept in the base checkpoint and every other new
     file (outputs, logs, model checkpoints) is deleted, so later runs don't download again and can't resume from
     the smoke run's model (item 7); sizes and checksums are recorded;
  6. metrics: which printed number is which claim, from the smoke run's log (item 5);
  7. fit: the smoke run's time against the 3600 s operation limit, with the fixed shrink rule (item 6);
  8. the spec, targets.json and HARNESS.md for the person who approves the commands (item 9 of section 4).
"""

from __future__ import annotations

import ast
import json
import math
import os
import re
import shlex
from dataclasses import dataclass, field
from pathlib import Path

from gapfinder.harness_auto import (_PAIR, _PREFIX, _QUAL, Binding, Command, ShrinkPlan, _family, bind_metrics,
                                    claim_words, compute_blockers, download_steps, pick_commands, shrink_plan)

HARNESS_DIR = "gf_harness"
PARALLEL = 4  # runs of one cell at once in a 4-vCPU VM, one thread each
VM_MB = 3900  # the Sandboxes VM's memory (3.9 GB, no swap)
# plan D6.4: a smoke copy's peak memory (the largest descendant's resident set; Python 2 and 3)
PEAK = r'''import subprocess, sys
rc = subprocess.call(sys.argv[1:])
try:
    import resource  # Linux (the VMs); a local Windows run has no peak to report
    print("GF_PEAK_KB=%d" % resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
except Exception:
    pass
sys.exit(rc)
'''


def memory_parallel(peak_mb: float | None, cap: int = PARALLEL) -> int:
    """Copies of a run that fit the VM at once: 80% of its memory over one copy's peak (at least one)."""
    if not peak_mb or peak_mb <= 0:
        return cap
    return max(1, min(cap, int(0.8 * VM_MB / peak_mb)))

# ------------------------------------------------------------------------ claims


def _metric_name(c: dict) -> str:
    fam = _family(str(c.get("metric", ""))) or re.sub(r"\W+", "_", str(c.get("metric", ""))).strip("_").lower()[:20]
    k = re.search(r"@\s*(\d+)", str(c.get("metric", "")))
    fam = f"{fam}{k.group(1) if k else ''}"
    cid = re.sub(r"\W+", "_", c["id"]).lower()
    return cid if cid.endswith(fam) else f"{cid}_{fam}"


def select_claims(ledger: dict | list, target_id: str) -> list[dict]:
    """The target, then every other cell of the same table row: same table, same conditions (dataset, model,
    setting), another metric. A held-out of this kind comes from the same run, so it costs nothing extra."""
    claims = ledger["claims"] if isinstance(ledger, dict) else ledger
    by_id = {c["id"]: c for c in claims}
    if target_id not in by_id:
        raise KeyError(f"no claim {target_id} in the ledger")
    t = by_id[target_id]
    if t.get("reported_value") is None:
        raise ValueError(f"claim {target_id} has no reported value")
    out, metrics = [], set()
    for c in [t] + [c for c in claims if c["id"] != target_id]:
        if c.get("reported_value") is None or c.get("type") != t.get("type"):
            continue
        if c is not t and (c.get("figure_or_table") != t.get("figure_or_table")
                           or (c.get("conditions") or {}) != (t.get("conditions") or {})):
            continue
        if c["metric"].lower() in metrics:
            continue
        metrics.add(c["metric"].lower())
        out.append({"claim_id": c["id"], "metric": c["metric"], "paper_value": float(c["reported_value"]),
                    "conditions": dict(c.get("conditions") or {}), "figure": c.get("figure_or_table"),
                    "held_out": c is not t, "name": _metric_name(c)})
    return out


# "epoch 50" is a point of a curve; "epochs: 50" (trained for 50) is a setting: with a schedule tied to the
# length of training, epoch 50 of a 200-epoch run is not a 50-epoch run
_EPOCH_KEY = re.compile(r"(?i)^(epoch|at_epoch|iteration|step)$")
_IDENTITY_KEYS = {"dataset", "model", "method", "task", "data", "benchmark"}


def extra_claims(ledger: dict | list, target_id: str, knobs: dict, limit: int = 4) -> tuple[list, list, list]:
    """Other cells that test the same setup at one other setting (plan items 14 and 15): the target's metric and
    conditions with exactly one more or different condition. That condition is
    - an epoch: a point of a learning curve, read from the same run's per-epoch log (no extra run);
    - a setting whose name maps to a knob (exact or the same core words): a claim at a fixed knob value (`at`);
    - anything else: listed for a person to map (a sensitivity table's "ripple set size" is RippleNet's
      `n_memory`; no rule here guesses that).
    Returns (points, curve points, unmapped)."""
    from gapfinder.search.engine import map_knob_name

    claims = ledger["claims"] if isinstance(ledger, dict) else ledger
    t = next(c for c in claims if c["id"] == target_id)
    tc = {k: str(v) for k, v in (t.get("conditions") or {}).items()}
    fam = _family(t["metric"])
    points, curves, unmapped = [], [], []
    for c in claims:
        if c["id"] == target_id or c.get("reported_value") is None or _family(c["metric"]) != fam:
            continue
        cond = {k: str(v) for k, v in (c.get("conditions") or {}).items()}
        if any(cond.get(k) != v for k, v in tc.items() if k in cond) or any(
                k not in cond for k in tc if k in _IDENTITY_KEYS - {"model", "method"}):
            continue  # another dataset or model
        extra = {k: v for k, v in cond.items() if k not in tc}
        if len(extra) != 1:
            continue
        (k, v), = extra.items()
        num = re.fullmatch(r"\s*[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?\s*", v)
        row = {"claim_id": c["id"], "metric": c["metric"], "paper_value": float(c["reported_value"]),
               "conditions": cond, "figure": c.get("figure_or_table"), "held_out": True}
        if _EPOCH_KEY.match(k) and num and re.fullmatch(r"\s*\d+\s*", v):
            curves.append({**row, "epoch": int(v)})
            continue
        knob = map_knob_name(k, knobs) if num else None
        if knob is None:
            unmapped.append({**row, "setting": k, "value": v})
            continue
        points.append({**row, "at": {knob: v.strip()}})
    # spread over the range: every other point when there are more than `limit`
    thin = lambda xs: xs if len(xs) <= limit else [xs[round(i * (len(xs) - 1) / (limit - 1))] for i in range(limit)]  # noqa: E731
    return thin(points), thin(sorted(curves, key=lambda x: x["epoch"])), unmapped


def condition_points(ledger: dict | list, target_id: str, t: "Templated", root: str | Path,
                     limit: int = 3) -> tuple[list[dict], list[dict]]:
    """Plan D2.1: the target's cell on other datasets (the same metric family, model and other conditions), as
    claims at a fixed dataset. `at` holds the dataset flag's value there and the settings the README's command for
    that dataset passes (what the authors ran there). A dataset with no README command of the same script, or whose
    name maps to no single value, is listed instead: its settings would be guesses. Returns (points, not used)."""

    if t.dataset is None:
        return [], []
    claims = ledger["claims"] if isinstance(ledger, dict) else ledger
    t0 = next(c for c in claims if c["id"] == target_id)
    tc = {k: str(v) for k, v in (t0.get("conditions") or {}).items()}
    key = next((k for k in tc if k.lower() in ("dataset", "data", "benchmark")), None)
    if key is None:
        return [], []
    fam = _family(t0["metric"])
    points, skipped, seen = [], [], set()
    for c in claims:
        if c["id"] == target_id or c.get("reported_value") is None or _family(c["metric"]) != fam:
            continue
        cond = {k: str(v) for k, v in (c.get("conditions") or {}).items()}
        if set(cond) != set(tc) or cond[key] == tc[key] or any(cond[k] != tc[k] for k in tc if k != key):
            continue
        row = {"claim_id": c["id"], "metric": c["metric"], "paper_value": float(c["reported_value"]),
               "conditions": cond, "figure": c.get("figure_or_table"), "held_out": True}
        words = claim_words({"conditions": {key: cond[key]}})
        mine = []
        for x in pick_commands(root, [{"metric": c["metric"], "conditions": {key: cond[key]}}], limit=12):
            cd, argv = _split_command(x.cmd)
            i = next((j for j, a in enumerate(argv) if a.endswith(".py")), None)
            if i is None or ((Path(cd) / argv[i]) if cd else Path(argv[i])).as_posix() != t.script:
                continue  # another script
            passed = {k.lstrip("-").replace("-", "_"): v for k, v in _parse_args(argv[i + 1:])}
            v = passed.get(t.dataset["name"])
            if v is not None and _matches(v, words):
                mine.append((x, passed, v))
        values = sorted({v for _, _, v in mine})
        if len(values) != 1:
            skipped.append({**row, "setting": key, "value": cond[key],
                            "why": ("no README command of the same script runs it: its settings would be guesses"
                                    if not values else f"several values match it: {values}")})
            continue
        x, passed, v = mine[0]
        if v in seen:
            continue
        seen.add(v)
        at = {t.dataset["name"]: v}
        for k, val in passed.items():
            if k in t.knobs and val is not None and str(val) != str(t.knobs[k]["default"]):
                at[k] = str(val)  # the README's own setting for this dataset
        points.append({**row, "at": at, "condition": v, "source": x.source})
        if len(points) >= limit:
            break
    return points, skipped


def make_condition_knob(t: "Templated") -> None:
    """The dataset flag as a condition knob: its value in the command becomes a placeholder (plan D2.1)."""
    d = t.dataset
    lit = f"{d['option']} {_q(d['value'])}"
    if lit not in t.command or d["name"] in t.knobs:
        return
    t.command = t.command.replace(lit, f"{d['option']} {{{d['name']}}}", 1)
    t.knobs[d["name"]] = {"layer": "config", "default": d["value"], "line": d.get("line", 0), "condition": True}
    t.fixed.pop(d["name"], None)


# ------------------------------------------------------------------------ the command's script and its flags


@dataclass
class ScriptFlag:
    name: str  # without dashes
    option: str  # as written: --lr, -l
    default: str | None
    kind: str  # value | store_true | store_false | bool_type | expr
    choices: list[str] = field(default_factory=list)
    line: int = 0


def _literal(src: str, node: ast.AST) -> str | None:
    try:
        v = ast.literal_eval(node)
    except (ValueError, SyntaxError):
        return None
    if isinstance(v, str):
        return v
    if v is None or isinstance(v, (list, tuple, dict, set)):
        return None
    if isinstance(v, bool):
        return str(v)
    return ast.get_source_segment(src, node) or str(v)  # 1e-7 stays "1e-7", not "1e-07"


def script_flags(path: str | Path) -> list[ScriptFlag]:
    """argparse `add_argument` calls and absl/gflags `DEFINE_*` calls in the script, from its syntax tree (a
    commented-out block of settings is a string, not a call: RippleNet's main.py has one)."""
    src = Path(path).read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []
    out, seen = [], set()
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call) or not isinstance(n.func, ast.Attribute):
            continue
        kw = {k.arg: k.value for k in n.keywords if k.arg}
        strs = [a.value for a in n.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]
        if n.func.attr == "add_argument":
            opts = [s for s in strs if s.startswith("-")]
            if not opts:
                continue
            opt = next((s for s in opts if s.startswith("--")), opts[0])
            name = (kw["dest"].value if isinstance(kw.get("dest"), ast.Constant) else opt.lstrip("-")).replace("-", "_")
            action = kw.get("action")
            action = action.value if isinstance(action, ast.Constant) else None
            typ = kw.get("type")
            if action in ("store_true", "store_false"):
                kind, default = action, "1" if action == "store_false" else "0"
            elif isinstance(typ, ast.Name) and typ.id == "bool":
                kind, default = "bool_type", None
            elif "default" in kw:
                default = _literal(src, kw["default"])
                kind = "value" if default is not None else "expr"
            else:
                kind, default = "expr", None
            choices = []
            if isinstance(kw.get("choices"), (ast.List, ast.Tuple)):
                choices = [str(_literal(src, e)) for e in kw["choices"].elts if _literal(src, e) is not None]
        elif n.func.attr.startswith("DEFINE_") and strs:
            name, opt = strs[0], "--" + strs[0]
            node = n.args[1] if len(n.args) > 1 else kw.get("default")
            default = _literal(src, node) if node is not None else None
            kind = "value" if default is not None else "expr"
            choices = []
            if n.func.attr == "DEFINE_bool" or n.func.attr == "DEFINE_boolean":
                kind = "value"
                default = "true" if default == "True" else "false" if default == "False" else default
        else:
            continue
        if name in seen:
            continue
        seen.add(name)
        out.append(ScriptFlag(name, opt, default, kind, choices, n.lineno))
    return out


# how-to-run settings, not the method's: paths, devices, logging, bookkeeping
_HOW_TO_RUN = re.compile(
    r"(?i)^(.*_)?(gpu|gpus|gpu_id|cuda|no_cuda|device|devices|workers|num_workers|n_workers|threads|num_threads|log|logs|"
    r"logdir|log_dir|log_every|log_interval|log_freq|print|print_every|print_freq|verbose|save|save_dir|save_path|"
    r"save_model|output|output_dir|out|outdir|out_dir|path|dir|root|data_dir|data_path|data_root|ckpt|checkpoint|"
    r"checkpoint_dir|resume|load|load_model|pretrained_path|tensorboard|wandb|debug|profile|port|local_rank|rank|"
    r"world_size|dist_url|dist_backend|name|exp_name|exp|tag|comment|note|plot|vis|visualize)$")
_DATASET = re.compile(r"(?i)^(dataset|data|data_name|dataset_name|data_set|dataname|ds)$")
_REPEATS = re.compile(r"(?i)^(runs|n_runs|num_runs|repeat|repeats|n_repeats|trials|n_trials|num_trials|n_exp|times)$")
_SEED = re.compile(r"(?i)^(seed|random_seed|rng_seed|manual_seed|torch_seed|np_seed|numpy_seed|global_seed)$")
_EPOCHS = re.compile(r"(?i)^(n_?epochs?|num_epochs?|max_epochs?|epochs?|n_iter|num_iters?|iterations|max_iters?|"
                     r"train_steps|num_steps|max_steps|steps)$")


@dataclass
class Templated:
    command: str  # the run command with {knob} placeholders (one run, from the work directory)
    naive: str  # the same at every default: what a person would run
    script: str  # repo-relative path of the script
    knobs: dict[str, dict] = field(default_factory=dict)
    fixed: dict[str, str] = field(default_factory=dict)  # flag -> why it is not a knob
    seed_flag: str | None = None
    epochs_knob: str | None = None
    repeats_flag: str | None = None
    note: str = ""
    dataset: dict | None = None  # the dataset flag: {"name", "option", "value", "values"} (plan D2.1)


def _split_command(cmd: str) -> tuple[str | None, list[str]]:
    """(directory it runs in, argv of the python invocation): `cd src && python -u main.py --a 1`."""
    parts = [p.strip() for p in re.split(r"\s*(?:&&|;)\s*", cmd) if p.strip()]
    cd = None
    for p in parts[:-1]:
        m = re.match(r"^cd\s+([\w./-]+)$", p)
        if m:
            cd = m.group(1)
    try:
        argv = shlex.split(parts[-1]) if parts else []
    except ValueError:
        argv = parts[-1].split()
    return cd, argv


def _parse_args(argv: list[str]) -> list[tuple[str, str | None]]:
    out, i = [], 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("-") and not re.match(r"^-\d", a):
            if "=" in a:
                k, v = a.split("=", 1)
                out.append((k, v))
            elif i + 1 < len(argv) and not (argv[i + 1].startswith("-") and not re.match(r"^-\d", argv[i + 1])):
                out.append((a, argv[i + 1]))
                i += 1
            else:
                out.append((a, None))
        i += 1
    return out


def _matches(value: str, words: set[str]) -> bool:
    v = value.lower()
    return v in words or any(len(w) >= 4 and (w in v or v in w) for w in words) or any(
        p in words for p in re.split(r"[-_]", v) if len(p) >= 3)


def dataset_values(root: Path, flag: ScriptFlag | None) -> list[str]:
    """What a dataset flag may be set to: its argparse choices, else the directory names under the repo's data
    directories."""
    if flag and flag.choices:
        return list(flag.choices)
    out = []
    for d in [root / n for n in ("data", "dataset", "datasets")] + list(root.glob("*/data")):
        if d.is_dir():
            out += [p.name for p in sorted(d.iterdir()) if p.is_dir() and not p.name.startswith((".", "_"))]
    return sorted(set(out))


def _alternatives(value: str) -> list[str] | None:
    """`[a|b|c]`, `{a,b,c}`, `a|b|c`, `(a/b)`: the values a README offers for one flag."""
    m = re.fullmatch(r"\s*[\[{(<]?\s*([\w.-]+(?:\s*[|,/]\s*[\w.-]+)+)\s*[\]})>]?\s*", value)
    if not m:
        return None
    return [v.strip() for v in re.split(r"[|,/]", m.group(1)) if v.strip()]


def _q(v: str) -> str:
    return v if re.fullmatch(r"[\w@%+=:,./-]+", v) else shlex.quote(v)


def template_command(root: str | Path, cmd: str, claims: list[dict]) -> Templated:
    """The picked command as a template: every flag of its script a knob at its default, except the fixed ones."""
    root = Path(root)
    cd, argv = _split_command(cmd)
    i = next((j for j, a in enumerate(argv) if a.endswith(".py")), None)
    if i is None or not argv[0].startswith("python"):
        raise ValueError(f"not a python command: {cmd!r}")
    script = ((Path(cd) / argv[i]) if cd else Path(argv[i])).as_posix()
    if not (root / script).is_file():
        raise ValueError(f"the command's script {script} is not in the repo")
    flags = {f.name: f for f in script_flags(root / script)}
    passed = {k.lstrip("-").replace("-", "_"): v for k, v in _parse_args(argv[i + 1:])}
    words = set().union(*(claim_words(c) for c in claims[:1]))
    t = Templated("", "", script)
    parts, naive = [], []
    order = list(passed) + [n for n in flags if n not in passed]
    for name in order:
        f = flags.get(name)
        opt = f.option if f else "--" + name
        value = passed.get(name, None) if name in passed else (f.default if f else None)
        if name in passed and value is not None and value.strip("<>[]{}").lower() == name.lower():
            value = f.default if f else None  # a placeholder (`--model MODEL`, `--dataset <dataset>`)
            passed.pop(name)
        alts = _alternatives(value) if name in passed and value is not None else None
        if alts:  # `--name [usps|hhar|reut|acm|dblp|cite]` (SDCN): the claim's, which defines the claim
            hits = [v for v in alts if _matches(v, words)]
            if len(hits) == 1:
                t.note += f"the README lists {alts} for {opt}; the claim's is {hits[0]!r}; "
                parts.append(f"{opt} {_q(hits[0])}")
                naive.append(parts[-1])
                t.fixed[name] = "one of the README's alternatives: the claim's"
                continue
            t.note += f"the README lists {alts} for {opt} and none or several match the claim; the code default is used; "
            passed.pop(name)
            value = f.default if f else None
            if value is None:
                continue
        if _DATASET.match(name):
            vals = dataset_values(root, f)
            if value is not None and not _matches(value, words):
                hits = [v for v in vals if _matches(v, words)]
                if len(hits) == 1:
                    t.note += f"dataset set from {value!r} to {hits[0]!r} (the claim's); "
                    value = hits[0]
                else:
                    t.note += (f"the command's dataset {value!r} isn't the claim's and no single known value "
                               f"matches it ({vals}); ")
            if value is not None:
                parts.append(f"{opt} {_q(value)}")
                naive.append(f"{opt} {_q(value)}")
                t.dataset = {"name": name, "option": opt, "value": str(value), "values": vals, "line": f.line if f else 0}
            t.fixed[name] = "dataset: defines the claim"
            continue
        if (value is not None and not re.fullmatch(r"(?i)[-+]?\d*\.?\d+(e[-+]?\d+)?|true|false|none", str(value))
                and _matches(str(value), words)):
            # `--model dominant` for a DOMINANT claim, `--method PGD` for a CE-PGD one: what the claim is about
            t.fixed[name] = f"its value {value!r} is one of the claim's conditions: defines the claim"
            parts.append(f"{opt} {_q(str(value))}")
            naive.append(parts[-1])
            continue
        if name in passed and f is None:  # passed but not declared in the script (e.g. a config file's keys)
            t.fixed[name] = "passed by the command but not declared in the script: kept as written"
            parts.append(opt if value is None else f"{opt} {_q(value)}")
            naive.append(parts[-1])
            continue
        if f is None:
            continue
        if f.kind == "bool_type":
            t.fixed[name] = ("declared type=bool: any value given on a command line, 'False' included, parses as "
                             "True, so it can't be set by a flag")
            if name in passed:
                parts.append(f"{opt} {_q(value)}" if value is not None else opt)
                naive.append(parts[-1])
            continue
        if _SEED.match(name):
            t.seed_flag = name
            t.fixed[name] = "seed: a new value every run (the runs' differences are the noise)"
            parts.append(f"{opt} $GF_SEED")
            naive.append(f"{opt} $GF_SEED")
            continue
        if _REPEATS.match(name):
            t.repeats_flag = name
            t.fixed[name] = "repeat count of the reported mean: the protocol, not a setting"
            if value is not None:
                parts.append(f"{opt} {_q(value)}")
                naive.append(parts[-1])
            continue
        if _HOW_TO_RUN.match(name):
            t.fixed[name] = "how to run (paths, devices, logging), not the method"
            if name in passed:
                parts.append(opt if value is None else f"{opt} {_q(value)}")
                naive.append(parts[-1])
            continue
        if f.kind in ("store_true", "store_false"):
            on = "1" if (name in passed) == (f.kind == "store_true") else "0"
            if f.kind == "store_false":
                on = "0" if name in passed else "1"
            t.knobs[name] = {"layer": "config", "default": on, "choices": ["0", "1"], "line": f.line,
                             "note": "store_true" if f.kind == "store_true" else "store_false (1 = not passed)"}
            flag_on = "1" if f.kind == "store_true" else "0"
            parts.append(f'$([ "{{{name}}}" = {flag_on} ] && echo {opt})')
            if on == flag_on:
                naive.append(opt)
            continue
        if value is None:
            t.fixed[name] = "no literal default in the code" if f.kind == "expr" else "no default"
            continue
        if not str(value).strip():
            t.fixed[name] = "empty default"
            continue
        t.knobs[name] = {"layer": "config", "default": str(value), "line": f.line}
        if f.choices:
            t.knobs[name]["choices"] = list(f.choices)
        if _EPOCHS.match(name) and t.epochs_knob is None and re.fullmatch(r"\d+", str(value)):
            t.epochs_knob = name
        parts.append(f"{opt} {{{name}}}")
        naive.append(f"{opt} {_q(str(value))}")
    # `python` is the environment's interpreter in a VM; the local backend sets $PYTHON to its own
    head = " ".join((['"${PYTHON:-python}"'] if argv[0] == "python" else [argv[0]]) + argv[1: i + 1])
    t.command = (f"cd {cd} && " if cd else "") + " ".join([head] + parts)
    t.naive = (f"cd {cd} && " if cd else "") + " ".join([head] + naive)
    return t


_EVAL_SCRIPT = re.compile(r"(?i)(^|/)(eval\w*|test\w*|infer\w*|predict\w*|attack\w*|inference\w*|score\w*|"
                          r"benchmark\w*|robust\w*)\.py$")
_TRAIN_SCRIPT = re.compile(r"(?i)(^|/)(train\w*|main\w*|run\w*|fit\w*|pretrain\w*|finetune\w*|learn\w*)\.py$")
_PATH_FLAG = re.compile(r"(?i)(save|ckpt|checkpoint|model_?path|model_?dir|out(put)?_?(dir|path)?|load|resume|weights?|"
                        r"pretrained|restore|log_?dir|exp_?dir)")


def _script_of(cmd: str) -> str:
    cd, argv = _split_command(cmd)
    s = next((a for a in argv if a.endswith(".py")), "")
    return ((Path(cd) / s) if cd else Path(s)).as_posix() if s else ""


def _paths(cmd: str) -> set[str]:
    """The file paths a command passes (checkpoints, output directories): what links one step to the next."""
    _, argv = _split_command(cmd)
    i = next((j for j, a in enumerate(argv) if a.endswith(".py")), None)
    out = set()
    for k, v in _parse_args(argv[i + 1:] if i is not None else []):
        if v and (_PATH_FLAG.search(k) or re.search(r"[/\\]|\.(pt|pth|ckpt|h5|pkl|bin|npz|model)$", v)):
            out.add(v.rstrip("/").split("/")[-1])
    return out


def chain_steps(root: str | Path, picked: Command) -> list[Command]:
    """Plan D6.5: the README's procedure up to the picked command. When the picked command evaluates or attacks a
    model (by its script's name) or reads a checkpoint, the nearest earlier README command that trains one (by name,
    or by writing the path the picked one reads) runs first in the same cell. Data preparation stays a data step."""
    from gapfinder.harness_auto import _commands_in

    root = Path(root)
    rel, _, line = picked.source.rpartition(":")
    p = root / rel
    if not p.is_file() or not line.isdigit():
        return [picked]
    script = _script_of(picked.cmd)
    reads = _paths(picked.cmd)
    if not (_EVAL_SCRIPT.search(script) or reads):
        return [picked]
    before = [c for c in _commands_in(p, rel) if int(c.source.rpartition(":")[2]) < int(line)
              and re.match(r"^(cd [\w./-]+ *(&&|;) *)?python", c.cmd)]
    for c in reversed(before):
        s2 = _script_of(c.cmd)
        if not s2 or s2 == script or _PREP.search(s2):
            continue
        linked = bool(reads & _paths(c.cmd))
        if linked or (_EVAL_SCRIPT.search(script) and _TRAIN_SCRIPT.search(s2)):
            return [c, picked]
    return [picked]


def template_chain(root: str | Path, steps: list[Command], claims: list[dict]) -> "Templated":
    """The steps as one cell: each templated, run in order (`&&`); a flag both scripts take with the same default is
    one knob (a hidden size the checkpoint must match), one with different defaults is two (prefixed by script)."""
    ts = [template_command(root, c.cmd, claims) for c in steps]
    if len(ts) == 1:
        return ts[0]
    last = ts[-1]
    merged = Templated("", "", last.script)
    commands, naives = [], []
    for t in ts:
        stem = Path(t.script).stem
        cmd = t.command
        for k, v in t.knobs.items():
            other = next((u.knobs[k] for u in ts if u is not t and k in u.knobs), None)
            if other is not None and str(other["default"]) != str(v["default"]):
                new = f"{stem}_{k}"
                cmd = cmd.replace("{" + k + "}", "{" + new + "}")
                merged.knobs[new] = v
            else:
                merged.knobs.setdefault(k, v)
        commands.append(cmd)
        naives.append(t.naive)
        merged.fixed.update({f"{stem}:{k}": why for k, why in t.fixed.items()})
        merged.seed_flag = merged.seed_flag or t.seed_flag
        merged.epochs_knob = merged.epochs_knob or (t.epochs_knob if t.epochs_knob in merged.knobs else None)
        merged.repeats_flag = merged.repeats_flag or t.repeats_flag
        merged.note += t.note
        merged.dataset = merged.dataset or t.dataset
    merged.command = " && ".join(commands)
    merged.naive = " && ".join(naives)
    merged.note += f"the cell runs {' then '.join(t.script for t in ts)} (the README's procedure); "
    return merged


_PREP = re.compile(r"(?i)(^|/)(pre_?process\w*|prepare\w*|process_?data\w*|build_?(data|dataset|graph)\w*|"
                   r"make_?(data|dataset)\w*|split\w*|gen(erate)?_?data\w*|download\w*|setup_?data\w*)\.py$")


def prep_commands(root: str | Path, picked: Command, claims: list[dict]) -> list[str]:
    """Data-preparation commands written before the picked one in the same file (RippleNet's README:
    `python preprocess.py --dataset movie`, then `python main.py --dataset movie`), the dataset set as in the
    picked command."""
    from gapfinder.harness_auto import _commands_in

    root = Path(root)
    rel, _, line = picked.source.rpartition(":")
    p = root / rel
    if not p.is_file():
        return []
    out = []
    for c in _commands_in(p, rel):
        if int(c.source.rpartition(":")[2]) >= int(line or 0):
            break
        cd, argv = _split_command(c.cmd)
        script = next((a for a in argv if a.endswith(".py")), "")
        if not _PREP.search(script):
            continue
        try:
            out.append(template_command(root, c.cmd, claims).naive.replace(" $GF_SEED", " 0"))
        except ValueError:
            out.append(c.cmd)
    return out


# ------------------------------------------------------------------------ scripts that run in the VM
# Python 2 and 3 alike: a 2016 repo runs on python:2.7-slim.

EMIT_TEMPLATE = r'''# written by `gapfinder harness`: each claim's number from every run's log (out/run*.log), averaged over the
# cell's runs. The labels were bound from the smoke run (HARNESS.md); a label a run doesn't print is left out.
from __future__ import print_function
import glob, io, re
BIND = %(bind)s
TRAJ = %(traj)s  # claim metric -> {"label", "scale", "dir": 1 higher is better / -1 lower, "val": validation label}
PAIR = re.compile(%(pair)r)
QUAL = re.compile(%(qual)r)
PREFIX = re.compile(%(prefix)r)
BARE = re.compile(%(bare)r)
LINE_TAG = re.compile(%(line_tag)r)
SYNONYMS = %(synonyms)s


def family(label):
    low = label.lower().replace("-", " ")
    if re.search(r"\bmean\s+average\s+precision\b", low):
        return "map"
    text = re.sub(r"\b(average|avg)\s+precision\b", "averageprecision", low)
    toks = re.findall(r"[a-z0-9@]+", text)
    for fam, syn in SYNONYMS:
        if any(t in syn or t.split("@")[0] in syn for t in toks):
            return fam
    return None


def qual_of(w):
    w = w.lower()
    return "test" if w.startswith("test") else "train" if w.startswith("train") else "best" if w == "best" else "val"


def labelled(log, tail_lines=40):
    found = {}
    for line in log.splitlines()[-tail_lines:]:
        best = bool(re.search(r"(?i)\bbest\b", line))
        t = LINE_TAG.match(line)
        tag = t.group(1) if t and t.group(1) and not QUAL.match(t.group(1) + "$") else None
        if tag:
            line = line[t.end():]
        spans = []
        for m in BARE.finditer(line):
            if family(m.group(1)) is None:
                continue
            spans.append((m.start(), m.end()))
            quals = [qual_of(q.group(1)) for q in QUAL.finditer(line[: m.end(1)]) if q.group(1).lower() != "best"]
            key = " ".join((["best"] if best else []) + ([quals[-1]] if quals else []) + ([tag] if tag else [])
                           + [m.group(1)])
            found[key] = float(m.group(2)) / (100 if m.group(3) else 1)
        for m in PAIR.finditer(line):
            if any(a <= m.start(2) < b for a, b in spans):
                continue
            raw = PREFIX.sub("", " ".join(m.group(1).split()).strip(" -"))
            quals = [qual_of(q.group(1)) for q in QUAL.finditer(line[: m.end(1)]) if q.group(1).lower() != "best"]
            base = " ".join(QUAL.sub("", raw).split()).strip(" -_:")
            if not base:
                continue
            key = " ".join((["best"] if best else []) + ([quals[-1]] if quals else []) + ([tag] if tag else [])
                           + [base])
            found[key] = float(m.group(2)) / (100 if m.group(3) else 1)
    return found


EPOCH = re.compile(r"(?i)\bepoch\s*[:#\[]?\s*(\d+)")


def per_epoch(log):
    """epoch -> labels printed on that epoch's lines (a learning curve's points)."""
    out = {}
    for line in log.splitlines():
        m = EPOCH.search(line)
        if m:
            out.setdefault(int(m.group(1)), {}).update(labelled(line, 1))
    return out


def series(log):
    """label -> every value it printed, in order (one per epoch when the program prints per epoch)."""
    out = {}
    for line in log.splitlines():
        for k, v in labelled(line, 1).items():
            out.setdefault(k, []).append(v)
    return out


def trajectory_stats(s, t):
    """One run's trajectory of a claim's label: the final value, the best (in the metric's direction) and where,
    the test value at the best validation value, the mean of the last five."""
    xs = [v * t["scale"] for v in s.get(t["label"], [])]
    if not xs:
        return None
    d = t["dir"]
    i = max(range(len(xs)), key=lambda j: d * xs[j])
    out = {"best": xs[i], "argbest": i + 1, "len": len(xs), "last5": sum(xs[-5:]) / len(xs[-5:]), "final": xs[-1],
           "_xs": xs, "_i": i}
    vs = s.get(t["val"] or "", [])
    if t["val"] and len(vs) == len(xs) and len(xs) > 1:
        k = max(range(len(vs)), key=lambda j: d * vs[j])
        out["bestval"] = xs[k]
        out["_k"] = k
    return out


vals = {}
stats = {}
curve_acc = {}
runs = 0
for f in sorted(glob.glob("out/run*.log")):
    text = io.open(f, encoding="utf-8", errors="replace").read()
    found = labelled(text)
    if TRAJ:
        ser = series(text)
        got = dict((name, trajectory_stats(ser, TRAJ[name])) for name in TRAJ)
        tname = [n for n in TRAJ if TRAJ[n].get("target")]
        tst = got.get(tname[0]) if tname else None
        for name in TRAJ:
            st = got[name]
            if st is None:
                continue
            if tst is not None and name != tname[0] and st["len"] == tst["len"] and st["len"] > 1:
                st["attarget"] = st["_xs"][tst["_i"]]  # this claim at the epoch where the target is best
                if "_k" in tst:  # ... and where the target's validation score is best (early stopping)
                    st["atbestval"] = st["_xs"][tst["_k"]]
            stats.setdefault(name, []).append(st)
            if TRAJ[name].get("target"):  # the target per epoch (plan D7.7)
                for e, x in enumerate(st["_xs"], 1):
                    if e <= 100 or (e <= 1000 and e %% 10 == 0) or e %% 100 == 0:
                        curve_acc.setdefault((name, e), []).append(x)
    curve = None
    hit = False
    for name in sorted(BIND):
        b = BIND[name]
        if len(b) == 3:  # (label, scale, epoch): the paper's epoch e, counted from 1
            if curve is None:
                curve = per_epoch(text)
            e = b[2] - (1 if curve and min(curve) == 0 else 0)
            if e in curve and b[0] in curve[e]:
                vals.setdefault(name, []).append(curve[e][b[0]] * b[1])
        elif b[0] in found:
            vals.setdefault(name, []).append(found[b[0]] * b[1])
            hit = True
    runs += hit
for name in sorted(vals):
    print("%%s=%%.6g" %% (name, sum(vals[name]) / len(vals[name])))
for name in sorted(stats):  # reporting-rule statistics (plan D1.2): the cell's mean of each, and across its runs
    rs = stats[name]
    for key in ("best", "argbest", "len", "last5", "bestval", "attarget", "atbestval"):
        xs = [r[key] for r in rs if key in r]
        if xs:
            print("%%s__x_%%s=%%.6g" %% (name, key, sum(xs) / len(xs)))
    finals = sorted(r["final"] for r in rs)
    print("%%s__x_maxrun=%%.6g" %% (name, finals[-1]))
    print("%%s__x_minrun=%%.6g" %% (name, finals[0]))
    m = len(finals)
    print("%%s__x_medrun=%%.6g" %% (name, (finals[m // 2] + finals[(m - 1) // 2]) / 2.0))
for (name, e) in sorted(curve_acc):  # a run cut early is compared with the as-run curve at its last epoch
    xs = curve_acc[(name, e)]
    print("%%s__x_e%%d=%%.6g" %% (name, e, sum(xs) / len(xs)))
print("gf_runs=%%d" %% runs)
'''


def emit_script(bindings: dict[str, tuple], trajectories: dict[str, dict] | None = None) -> str:
    """`bindings`: metric name -> (printed label, scale to the paper's unit[, the paper's epoch for a point of a
    learning curve, counted from 1]). `trajectories`: claim metric -> {"label", "scale", "dir", "val"}, for the
    reporting-rule statistics (`<name>__x_best`, `__x_bestval`, `__x_last5`, `__x_maxrun`, `__x_medrun`, ...)."""
    bind = "{" + ", ".join(f"{k!r}: ({v[0]!r}, {float(v[1])!r}" + (f", {int(v[2])!r})" if len(v) > 2 else ")")
                           for k, v in sorted(bindings.items())) + "}"
    from gapfinder.harness_auto import _BARE, _LINE_TAG, _METRIC_SYNONYMS

    syn = "[" + ", ".join(f"({k!r}, {sorted(v)!r})" for k, v in _METRIC_SYNONYMS.items()) + "]"  # ordered
    traj = repr({k: {"label": v["label"], "scale": float(v["scale"]), "dir": int(v["dir"]), "val": v.get("val"),
                     "target": bool(v.get("target"))} for k, v in sorted((trajectories or {}).items())})
    return EMIT_TEMPLATE % {"bind": bind, "pair": _PAIR.pattern, "qual": _QUAL.pattern, "prefix": _PREFIX.pattern,
                            "bare": _BARE.pattern, "line_tag": _LINE_TAG.pattern, "synonyms": syn, "traj": traj}


KEEP_DATA = r'''# written by `gapfinder harness` (plan item 7). `before`: list the work directory. `after` (once the data steps
# and the smoke run are done): keep every new file that is data, delete every other new file, print a manifest.
from __future__ import print_function
import hashlib, io, json, os, re, sys
LIST = "gf_harness/before.json"
DATA = re.compile(r"(^|/)(data|dataset|datasets|raw|processed|cache|\.cache)(/|$)", re.I)
OUT = re.compile(r"(^|/)(out|output|outputs|result|results|log|logs|checkpoint|checkpoints|ckpt|ckpts|save|saved|"
                 r"saved_models?|models?_saved|runs|wandb|lightning_logs|mlruns|tensorboard|__pycache__|gf_harness|"
                 r"\.gf_runtime)(/|$)", re.I)
MODEL = re.compile(r"(?i)(^|/)[^/]*(ckpt|checkpoint|model|best|epoch|weights?)[^/]*\.(pt|pth|ckpt|h5|hdf5|pkl|bin|npz|"
                   r"safetensors|index|meta)$")
CACHES = [".cache/torch", ".cache/huggingface", "scikit_learn_data", ".keras/datasets", "nltk_data", "gensim-data",
          "tensorflow_datasets", ".dgl", ".ogb", ".torch", "torch_datasets"]


def walk(top):
    for d, dirs, files in os.walk(top):
        for f in files:
            yield os.path.join(d, f)


def rel(p):
    return os.path.relpath(p, ".").replace(os.sep, "/")


def sha(p, limit=512 * 2 ** 20):
    if os.path.getsize(p) > limit:
        return None
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(2 ** 20), b""):
            h.update(chunk)
    return h.hexdigest()


def stamp(p):
    st = os.stat(p)
    return [st.st_size, int(st.st_mtime)]


home = os.path.expanduser("~")
caches = [os.path.join(home, c) for c in CACHES] if sys.platform.startswith("linux") else []
if sys.argv[1] == "before":
    listing = dict((rel(p), stamp(p)) for p in walk("."))
    listing.update(dict((p, stamp(p)) for c in caches for p in walk(c)))
    with io.open(LIST, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(listing).decode("utf-8") if bytes is str else json.dumps(listing))
    print("GF_LISTED %d" % len(listing))
    sys.exit(0)
before = json.load(io.open(LIST, encoding="utf-8"))
kept, dropped, changed = [], [], []
for p in walk("."):
    r = rel(p)
    if r.startswith("gf_harness/") or r.startswith(".gf_runtime/"):
        continue
    if r in before:
        if before[r] != stamp(p):
            changed.append(r)
        continue
    if DATA.search(r) and not OUT.search(r) and not MODEL.search(r):
        kept.append(r)
    else:
        os.remove(p)
        dropped.append(r)
for c in caches:
    for p in walk(c):
        if p not in before:
            kept.append(p)
files = [{"path": r, "bytes": os.path.getsize(r), "sha256": sha(r)} for r in sorted(kept)]
print("GF_DATA_MANIFEST " + json.dumps({"kept": files, "dropped": sorted(dropped), "changed": sorted(changed),
                                        "kept_bytes": sum(f["bytes"] for f in files)}))
'''


# ------------------------------------------------------------------------ time


def progress_estimate(log: str, elapsed_s: float, total_epochs: int | None) -> float | None:
    """A run that hit the smoke timeout: its time at full length, from the last epoch it printed."""
    if not total_epochs:
        return None
    eps = [int(x) for x in re.findall(r"(?i)\bepoch\s*[:#\[]?\s*(\d+)", log)]
    if not eps:
        return None
    done = max(eps) + (1 if min(eps) == 0 else 0)
    if done <= 0:
        return None
    return elapsed_s * total_epochs / done


# ------------------------------------------------------------------------ the spec


SEED_PREFIX = ('GF_SEED=$("${PYTHON:-python}" -c "import os, zlib; print(zlib.crc32(os.environ.get(\'RUN_TAG\', \'x\')'
               '.encode(\'utf-8\')) % 100000)"); ')


def run_command(t: Templated, repeats: int, shards: bool, parallel: int = PARALLEL) -> str:
    """One cell: `repeats` runs of the templated command, PARALLEL at a time with one thread each (or one run per
    shard), each with its own seed, then the emitter."""
    threads = "export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 TF_NUM_INTRAOP_THREADS=1 " \
              "TF_NUM_INTEROP_THREADS=1; " if repeats > 1 and not shards and parallel > 1 else ""
    one = t.command.replace("$GF_SEED", "$((GF_SEED + r))")
    # plan D7.7: a screening run may be cut at GF_TIME_CUT seconds (0: never); the emitter runs after it either way
    one = f'timeout ${{GF_TIME_CUT:-0}} "${{GF_BASH:-bash}}" -c {shlex.quote(one)}'
    if shards:
        body = f"r={{shard}}; ({one}) > out/run{{shard}}.log 2>&1"
    elif repeats == 1:
        body = f"r=1; ({one}) > out/run1.log 2>&1"
    else:
        body = (f"n=0; for r in $(seq 1 {repeats}); do ({one}) > out/run$r.log 2>&1 & n=$((n+1)); "
                f"if [ $((n % {parallel})) -eq 0 ]; then wait; fi; done; wait")
    return f'mkdir -p out; rm -f out/run*.log; {threads}{SEED_PREFIX}{body}; "${{PYTHON:-python}}" {HARNESS_DIR}/emit.py'


def spec_dict(name: str, base: str, source: str, t: Templated, claims: list[dict], bound: dict[str, Binding],
              repeats: int, plan: ShrinkPlan, per_run_s: float | None, curves: list[dict] = (),
              parallel: int = PARALLEL, trajectories: dict[str, dict] | None = None) -> dict:
    knobs = {k: {kk: vv for kk, vv in v.items() if kk in ("layer", "default", "choices", "condition")}
             for k, v in t.knobs.items()}
    shards = plan.action == "shards" or (plan.action == "shrink" and repeats > 1)
    if plan.action == "shrink" and t.epochs_knob:
        d = int(knobs[t.epochs_knob]["default"])
        knobs[t.epochs_knob]["default"] = str(max(1, round(d * plan.factor)))
    if t.epochs_knob and per_run_s:
        fit = int(OPERATION_S * 0.8 / max(per_run_s / max(int(t.knobs[t.epochs_knob]["default"]), 1), 1e-9))
        knobs[t.epochs_knob]["max"] = max(int(knobs[t.epochs_knob]["default"]), fit)
    run = {"command": run_command(t, repeats, shards, parallel), "output": "stdout", "format": "kv",
           "timeout": int(OPERATION_S - 300)}
    if shards:
        run["shards"] = [str(i) for i in range(1, repeats + 1)]
        run["shard_mean"] = True
    if any(v.get("target") for v in (trajectories or {}).values()):
        run["time_cut"] = True  # the emitter writes the target per epoch: a cut run can be compared (plan D7.7)
    spec = {"name": name, "base": base, "source": source, "run": run, "knobs": knobs, "allowed_paths": ["out/"],
            "metrics": [c["name"] for c in claims if c["claim_id"] in bound]
            + [f"{c['name']}__{i}" for c in claims if c["claim_id"] in bound
               for i, _ in enumerate(bound[c["claim_id"]].alternatives[:3])] + [c["name"] for c in curves]
            + [f"{n}__x_{k}" for n in sorted(trajectories or {}) for k in TRAJECTORY_STATS] + ["gf_runs"]}
    if plan.discrepancy is not None:
        spec["discrepancy"] = plan.discrepancy
    return spec


OPERATION_S = 3600


def bindings_for_emit(claims: list[dict], bound: dict[str, Binding], curves: list[dict] = ()) -> dict[str, tuple]:
    """metric name -> (label, scale), with up to three alternatives per claim as extra metrics (`name__0`, ...),
    so a best-epoch or validation protocol stays visible in every run; a learning-curve point adds its epoch."""
    out = {c["name"]: (c["label"], c["scale"], c["epoch"]) for c in curves}
    for c in claims:
        b = bound.get(c["claim_id"])
        if b is None:
            continue
        out[c["name"]] = (b.label, b.scale)
        for i, alt in enumerate(b.alternatives[:3]):
            out[f"{c['name']}__{i}"] = (alt, b.scale)
    return out


LOWER_IS_BETTER = {"loss", "mse", "mae", "rmse", "ppl"}
TRAJECTORY_STATS = ("best", "argbest", "len", "last5", "bestval", "attarget", "atbestval", "maxrun", "minrun", "medrun")


def trajectories_for_emit(claims: list[dict], bound: dict[str, Binding], log: str) -> dict[str, dict]:
    """claim metric -> what the emitter needs to summarise its trajectory: the label, the scale, the direction (from
    the metric family) and the validation label printed alongside a test label ("test acc" -> "val acc"), if any."""
    from gapfinder.harness_auto import labelled_numbers

    printed = labelled_numbers(log, tail_lines=10 ** 9)
    out = {}
    for c in claims:
        b = bound.get(c["claim_id"])
        if b is None:
            continue
        words = b.label.split()
        val = None
        if "test" in words:
            cand = " ".join("val" if w == "test" else w for w in words)
            val = cand if cand in printed else None
        out[c["name"]] = {"label": b.label, "scale": b.scale, "val": val, "target": c is claims[0],
                          "dir": -1 if _family(c["metric"]) in LOWER_IS_BETTER else 1}
    return out


def targets_json(claims: list[dict], bound: dict[str, Binding], points: list[dict] = (),
                 curves: list[dict] = ()) -> list[dict]:
    def row(c):
        return {"claim_id": c["claim_id"], "metric": c["name"], "paper_value": c["paper_value"],
                "held_out": c["held_out"], "figure": f"{c.get('figure') or ''} ({c['metric']}, "
                + ", ".join(f"{k}={v}" for k, v in c["conditions"].items()) + ")"}
    return ([row(c) for c in claims if c["claim_id"] in bound] + [{**row(p), "at": p["at"]} for p in points]
            + [row(c) for c in curves])


# ------------------------------------------------------------------------ the report


@dataclass
class HarnessResult:
    ok: bool
    stage: str  # where it stopped: blockers | claims | command | template | env | data | smoke | metrics | done
    reason: str = ""
    blockers: list[str] = field(default_factory=list)
    claims: list[dict] = field(default_factory=list)
    commands: list[Command] = field(default_factory=list)
    templated: Templated | None = None
    downloads: list[str] = field(default_factory=list)
    prep: list[str] = field(default_factory=list)
    env: dict | None = None
    manifest: dict | None = None
    smoke: dict | None = None
    bindings: list[Binding] = field(default_factory=list)
    plan: ShrinkPlan | None = None
    spec: dict | None = None
    cost_usd: float = 0.0
    points: list[dict] = field(default_factory=list)  # claims at fixed knob values (Target.at)
    curves: list[dict] = field(default_factory=list)  # learning-curve points, from the per-epoch log
    unmapped: list[dict] = field(default_factory=list)  # one-setting variants whose setting maps to no knob
    paper_year: dict | None = None  # the paper-year environment knob: pins, skipped, used
    paper_era: dict | None = None  # the repository's last commit before the paper (the paper-era code knob)
    notes: list[str] = field(default_factory=list)


_HYPER = re.compile(r"(?i)^(lr|learning_rate|.*_lr|weight_decay|wd|l2.*|.*dropout.*|drop_?rate|.*epochs?|n_?iters?|"
                    r"max_?iter.*|steps|max_steps|batch_?size|bs|hidden.*|.*_dim|dim|n_?layers?|num_layers|layers|"
                    r"n_?heads|num_heads|heads|momentum|alpha|beta\d?|gamma|lambda_?\w*|lam\w*|tau|temperature|"
                    r"eps(ilon)?|patience|.*_rate|k|top_?k|n_?neighbors|window\w*|seq_len|.*_size)$")


def literal_knobs(root: Path, t: "Templated", command: str, few: int = 3, limit: int = 12) -> dict[str, dict]:
    """Plan D6.7: when the script exposes fewer than `few` flags, the named literals that look like settings (lr,
    epochs, hidden, dropout, batch size ...) in the files the run imports become patch knobs (the in-memory hook;
    the entry script only when the command runs it directly). Their defaults are the literals as written."""
    if len(t.knobs) >= few:
        return {}
    from gapfinder.harness_auto import _import_closure
    from gapfinder.ingest.code_checks import named_literals
    from gapfinder.sandbox import ast_patch

    files = {p.relative_to(root.resolve()).as_posix() for p, _ in _import_closure(root.resolve())
             if p.is_relative_to(root.resolve())}
    out = {}
    for x in named_literals(root):
        if x.file not in files or not _HYPER.match(x.name or "") or x.name in t.knobs:
            continue
        if "add_argument" in x.detail or "DEFINE_" in x.detail or x.name == "default":
            continue
        if ast_patch.entry_script(root / x.file) and not ast_patch.direct_entry(command, x.file):
            continue
        k = ast_patch.knob_name(x.file, x.line, x.name)
        out.setdefault(k, {"layer": "environment", "default": str(x.value), "env": True})
        if len(out) >= limit:
            break
    return out


def harness_markdown(r: HarnessResult) -> str:
    L = ["# HARNESS.md (written by `gapfinder harness`)", "",
         f"**Status:** {'ready for approval' if r.ok else 'stopped at ' + r.stage}" + (f": {r.reason}" if r.reason else ""),
         "", "A person reads the commands below and approves them (about 5 minutes). The knobs are mechanical: every "
         "flag of the script at its default, so they need no approval.", ""]
    if r.blockers:
        L += ["## Blockers (static)", ""] + [f"- {b}" for b in r.blockers] + [""]
    if r.claims:
        L += ["## Claims", "", "Rule: the target, then every other cell of its table row (same conditions, another "
              "metric) as held-outs.", "", "| claim | role | metric | paper | spec metric |", "|---|---|---|---|---|"]
        L += [f"| {c['claim_id']} | {'held-out' if c['held_out'] else 'target'} | {c['metric']} | {c['paper_value']:g} "
              f"| `{c['name']}` |" for c in r.claims]
        if len(r.claims) < 2:
            L += ["", "Only one claim: history matching can't tell configurations apart, so labels stay cautious."]
        L.append("")
    if r.points or r.curves or r.unmapped:
        L += ["## Claims at other settings (identifiability)", "",
              "Cells with the target's setup and one other setting. A claim at a fixed knob value is run with that "
              "value on top of each candidate; a learning-curve point is read from the same run's per-epoch log.", ""]
        L += [f"- {p['claim_id']}: {p['metric']} {p['paper_value']:g} at "
              + ", ".join(f"`{k}={v}`" for k, v in p["at"].items())
              + (f" (another dataset; its settings from the README command at {p['source']})" if p.get("condition") else "")
              for p in r.points]
        L += [f"- {c['claim_id']}: {c['metric']} {c['paper_value']:g} at epoch {c['epoch']}" + (f" (`{c['name']}`)" if c.get("name") else " (not bound yet)")
              for c in r.curves]
        if r.unmapped:
            L += ["", "Not used (the setting's name maps to no knob; add `at` in targets.json by hand if it is one):"]
            L += [f"- {u['claim_id']}: {u['metric']} {u['paper_value']:g} at {u['setting']} = {u['value']}"
                  + (f" ({u['why']})" if u.get("why") else "") for u in r.unmapped[:12]]
        L.append("")
    if r.commands:
        L += ["## Command", "", "Picked by the claims' words in the command's arguments (README and shell scripts):", ""]
        L += [f"{'**picked**' if i == 0 else '-'} `{c.cmd}` ({c.source}; matched {', '.join(c.matched) or 'nothing'})"
              for i, c in enumerate(r.commands)]
        L.append("")
    t = r.templated
    if t:
        L += ["One run, at every default:", "", "```", t.naive, "```", ""]
        if t.note:
            L += [f"Note: {t.note.strip('; ')}", ""]
        L += ["### Knobs", "", "| knob | default | declared at |", "|---|---|---|"]
        L += [f"| {k} | `{v['default']}`" + (f" (choices {', '.join(v['choices'])})" if v.get("choices") else "")
              + f" | {t.script}:{v.get('line', '?')} |" for k, v in t.knobs.items()]
        L += ["", "### Fixed (not knobs)", ""] + [f"- `{k}`: {why}" for k, why in t.fixed.items()] + [""]
    if r.downloads or r.prep:
        L += ["## Data steps", ""] + [f"- `{c}`" for c in r.downloads + r.prep] + [""]
    if r.env:
        L += ["## Environment", "", f"Image `{r.env.get('image')}`; checkpoint `{r.env.get('checkpoint')}`; recipe:", "",
              "```"] + (r.env.get("recipe") or ["(none needed)"]) + ["```", ""]
    if r.manifest:
        m = r.manifest
        L += ["## Data kept in the base checkpoint", "",
              f"{len(m['kept'])} files, {m['kept_bytes'] / 2**20:.1f} MB (new since the environment: downloads, "
              f"preprocessing, dataset loaders' caches). {len(m['dropped'])} other new files deleted (outputs, logs, "
              "model checkpoints)." + (f" The smoke run modified repo files: {', '.join(m['changed'][:8])}."
                                       if m["changed"] else ""), ""]
        L += [f"- `{f['path']}` {f['bytes']} B" + (f" sha256 {f['sha256'][:16]}..." if f["sha256"] else "")
              for f in m["kept"][:25]]
        L.append("")
    if r.smoke:
        s = r.smoke
        L += ["## Smoke run", "", f"{s['copies']} run(s) in parallel; exit {s['rc']} after {s['seconds']} s"
              + (" (stopped at the smoke timeout)" if s.get("timed_out") else "")
              + (f"; peak memory {s['peak_mb']:.0f} MB a run, {s.get('parallel')} at a time in the cell"
                 if s.get("peak_mb") else ""), ""]
        if s.get("per_run_values"):
            L += [f"- `{k}`: {', '.join(f'{x:.4g}' for x in v)}" for k, v in s["per_run_values"].items()]
            L += ["", "Seeds vary: " + ("unknown (one copy)" if s.get("seeds_vary") is None else "yes"
                                        if s.get("seeds_vary") else "**no: identical runs; the noise band "
                                        "will be zero**"), ""]
    if r.bindings:
        L += ["## Metric binding", "", "Test before unqualified before validation before train; final before best; "
              "on the paper's scale. A tie is a refusal.", "", "| claim | printed label | value | scale | alternatives |",
              "|---|---|---|---|---|"]
        for b in r.bindings:
            L.append(f"| {b.claim_id} | {('`' + b.label + '`') if b.label else '**refused**: ' + b.refused} | "
                     f"{'' if b.value is None else f'{b.value:.4g}'} | {b.scale:g} | "
                     f"{', '.join('`' + a + '`' for a in b.alternatives[:5])} |")
        L.append("")
    if r.paper_year:
        y = r.paper_year
        own = y.get("own") or {}
        L += ["## Paper-year environment (knob `gf_paper_year_env`)", "",
              f"Packages as of {y['date']} (Python {y['python']}), each in its own directory under `/opt/gf_py`: "
              + (", ".join(f"`{d}=={v}`" + (" (the repository's own package)" if d == own.get("dist") else "")
                           for d, v in sorted(y["pins"].items())) or "none older than installed")
              + (f". Used: {'yes' if y['used'] else 'no, ' + y.get('why_not', 'nothing to pin')}." if y["pins"] else "."),
              ""]
        if y.get("used"):
            L += ["Values: `0` (as installed), " + ("`all`, " if y.get("all_ok") else "")
                  + "one directory, a comma list, or `dist==version` (installed on demand by the run). The runtime "
                  "shim imports those packages from there whatever sys.path says.", ""]
            if y.get("failed"):
                L += [f"Failed to install: {', '.join(y['failed'])}.", ""]
            if not y.get("all_ok") and y.get("pins"):
                L += ["Not importable all together; each listed value imports alone.", ""]
        if y.get("deps"):
            L += ["Dependencies the old releases need at other versions (date-bounded, from their own requirements):", ""]
            L += [f"- `{d}=={v}`: {y['dep_why'].get(d, '')}" for d, v in sorted(y["deps"].items())] + [""]
        L += [f"- {d}: {w}" for d, w in sorted({**y["skipped"], **{k: v for k, v in (y.get("dep_why") or {}).items()
                                                                  if k not in (y.get("deps") or {})}}.items())] + [""]
    if r.paper_era:
        e = r.paper_era
        L += ["## Paper-era code (knob `gf_paper_era_code`)", "",
              f"The repository's last commit before the paper's date: `{e['sha'][:12]}` ({e['date']}: {e['message']}); "
              f"{e.get('files', 0)} code files in `/opt/gf_paper_era`, copied over the checkout when the knob is 1. "
              f"{len(e.get('commits') or [])} commits from it to the given one (history before the given commit "
              "only) for the binary search.", ""]
    if r.plan:
        L += ["## Fit in one Sandboxes operation (3600 s)", "", f"{r.plan.action}: {r.plan.note}"
              + (f"; discrepancy allowance {r.plan.discrepancy}" if r.plan.discrepancy is not None else ""), ""]
    if r.notes:
        L += ["## Notes", ""] + [f"- {n}" for n in r.notes] + [""]
    L += [f"Model spend: ${r.cost_usd:.4f}", ""]
    return "\n".join(L)


# ------------------------------------------------------------------------ end to end


def _per_epoch(log: str) -> dict[int, dict[str, float]]:
    """As the emitter's per_epoch: epoch -> the labels printed on that epoch's lines."""
    from gapfinder.harness_auto import labelled_numbers

    out: dict[int, dict[str, float]] = {}
    for line in log.splitlines():
        m = re.search(r"(?i)\bepoch\s*[:#\[]?\s*(\d+)", line)
        if m:
            out.setdefault(int(m.group(1)), {}).update(labelled_numbers(line, 1))
    return out


def _manifest(stdout: str) -> dict | None:
    m = re.search(r"GF_DATA_MANIFEST (\{.*\})", stdout or "")
    return json.loads(m.group(1)) if m else None


async def build_harness(router, backend, *, repo: str | None, commit: str | None, local: str | Path, ledger: dict,
                        target: str, out: str | Path, repeats: int = 1, smoke_timeout: float = 2400,
                        max_steps: int = 12, image: str | None = None, force: bool = False,
                        fetch_cmd: str | None = None, env_checkpoint: str | None = None,
                        paper_date=None, command: str | None = None,
                        bind: dict[str, str] | None = None, paper_text: str | None = None) -> HarnessResult:
    """Steps 0-8 of the module docstring. `env_checkpoint`: an environment already built (skips env-build).
    `paper_date` (a date): also install the imported packages as they were then, behind one knob (item 19).
    The two choices a person approving the harness makes, given up front (recorded in HARNESS.md): `command`, the
    experiment command when the picker can't choose (two scripts, a chain); `bind`, claim id -> printed label, when
    the binder refuses a tie (only a label the run printed is accepted)."""
    from gapfinder.env_build import build_env, fetch, short_run_goal
    from gapfinder.sandbox import runtime_shim

    root, out = Path(local), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    r = HarnessResult(False, "blockers", blockers=compute_blockers(root))
    before = router.meter.total_cost() if router is not None else 0.0

    def finish(stage: str, reason: str = "") -> HarnessResult:
        r.stage, r.reason = stage, reason
        r.cost_usd = (router.meter.total_cost() - before) if router is not None else 0.0
        (out / "HARNESS.md").write_text(harness_markdown(r), encoding="utf-8")
        return r

    from gapfinder.sandbox.backend import InfraError

    step = {"at": "blockers"}

    async def run() -> HarnessResult:
        nonlocal env_checkpoint
        if r.blockers and not force:
            return finish("blockers", "the repo can't run on a CPU-only 3.9 GB VM (--force to try anyway)")
        try:
            step["at"] = "claims"
            r.claims = select_claims(ledger, target)
        except (KeyError, ValueError) as e:
            return finish("claims", str(e))
        cmds = [Command(command, "given by the runner")] if command else \
            [c for c in pick_commands(root, r.claims, limit=12) if re.match(r"^(cd [\w./-]+ *(&&|;) *)?python", c.cmd)]
        # a data-preparation script is a data step, not the experiment (RippleNet's preprocess.py comes first)
        experiments = [c for c in cmds if not _PREP.search(next((a for a in _split_command(c.cmd)[1] if a.endswith(".py")), ""))]
        cmds = (experiments or cmds)[:5]
        r.commands = cmds
        if command:
            r.notes.append(f"command given by the runner: `{command}`")
        for cid, label in (bind or {}).items():
            r.notes.append(f"{cid} bound to the printed label `{label}` by the runner")
        if not cmds:
            return finish("command", "no python command in the README or shell scripts")
        if len(cmds) > 1 and cmds[0].score == cmds[1].score and cmds[0].score > 0 and \
                _split_command(cmds[0].cmd)[1][:2] != _split_command(cmds[1].cmd)[1][:2]:
            return finish("command", "two commands with different scripts match the claims equally well; pick one "
                                     "with --command")
        steps = chain_steps(root, cmds[0])
        try:
            r.templated = t = template_chain(root, steps, r.claims)
        except ValueError as e:
            return finish("template", str(e))
        if len(steps) > 1:
            r.notes.append("procedure: " + " then ".join(f"`{c.cmd}` ({c.source})" for c in steps))
        r.points, r.curves, r.unmapped = extra_claims(ledger, target, t.knobs)
        conds, not_used = condition_points(ledger, target, t, root)
        r.unmapped += not_used
        r.downloads, r.prep = download_steps(root), prep_commands(root, cmds[0], r.claims)
        if conds:  # other datasets: the dataset flag becomes a condition knob, and their data is prepared too
            make_condition_knob(t)
            r.points += conds
            for p in conds:
                r.prep += [x for x in prep_commands(root, cmds[0], [{"metric": p["metric"], "conditions": p["conditions"]}])
                           if x not in r.prep]
        data_steps = [d.replace("cd /work && ", "").replace("cd /work/", "cd ") for d in r.downloads] + r.prep
        data_sh = " && ".join(f"({d})" for d in data_steps)
        senv, sfiles, sprefix = runtime_shim.run_parts()
        shim_env = "export " + " ".join(f"{k}={v}" for k, v in senv.items()) + "; " + sprefix
        if env_checkpoint is None:
            naive_one = SEED_PREFIX + t.naive.replace("$GF_SEED", "$((GF_SEED + 1))")
            goal = shim_env + (f"cd /work && {data_sh} && " if data_sh else "") + short_run_goal(naive_one)
            step["at"] = "env"
            env = await build_env(router, backend, root, fetch=fetch_cmd or (fetch(repo, commit, root) if repo else None),
                                  image=image, max_steps=max_steps, goal=goal, goal_files=sfiles)
            r.env = env.to_dict()
            from gapfinder.env_build import write_result

            write_result(env, out / "env_build.json")  # the recipe, every step and its output, failed or not
            if not env.ok:
                return finish("env", env.reason)
            env_checkpoint = env.checkpoint
        else:
            r.env = {"image": image or "(given)", "checkpoint": env_checkpoint, "recipe": []}
        files = {**sfiles, f"{HARNESS_DIR}/keep_data.py": KEEP_DATA.encode(), f"{HARNESS_DIR}/peak.py": PEAK.encode(),
                 f"{HARNESS_DIR}/emit.py": emit_script({}).encode()}
        from gapfinder import env_year

        step_a = (f'"${{PYTHON:-python}}" {HARNESS_DIR}/keep_data.py before' + (f" && {sprefix}{data_sh}" if data_sh else "")
                  + (f"; {env_year.FREEZE}" if paper_date else ""))
        step["at"] = "data"
        a = await backend.run(env_checkpoint, step_a, env=senv, timeout=OPERATION_S - 100, disposable=False, files=files)
        if a.exit_code != 0 or not a.checkpoint:
            return finish("data", f"the data steps failed (exit {a.exit_code}): {((a.stdout or '') + (a.stderr or ''))[-800:]}")
        one = sprefix + t.naive.replace("$GF_SEED", "$((GF_SEED + r))")

        async def smoke_run(copies: int):
            threads = "export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1; " if copies > 1 else ""
            # `copies` runs at once (the cell's own pattern), each stopped at the smoke timeout (`timeout` exits 124)
            smoke = (f"mkdir -p out; {threads}{SEED_PREFIX}s0=$(date +%s); pids=''; for r in $(seq 1 {copies}); do "
                     f"(export r GF_SEED; timeout {int(smoke_timeout)} \"${{PYTHON:-python}}\" {HARNESS_DIR}/peak.py "
                     f"\"${{GF_BASH:-bash}}\" -c {shlex.quote(one)}) > out/run$r.log 2>&1 & "
                     f"pids=\"$pids $!\"; done; rc=0; for p in $pids; do wait $p || rc=$?; done; echo GF_SMOKE_RC=$rc; "
                     f"echo GF_SMOKE_S=$(( $(date +%s) - s0 )); for r in $(seq 1 {copies}); do echo GF_LOG_$r; "
                     f"tail -c 20000 out/run$r.log; echo; done; \"${{PYTHON:-python}}\" {HARNESS_DIR}/keep_data.py after")
            b = await backend.run(a.checkpoint, smoke, env={**senv, "RUN_TAG": "gf-harness-smoke"},
                                  timeout=OPERATION_S - 60, disposable=False, files=None)
            so = b.stdout or ""
            rc = int((re.search(r"GF_SMOKE_RC=(\d+)", so) or [0, 1])[1])
            secs = float((re.search(r"GF_SMOKE_S=(\d+)", so) or [0, 0])[1])
            logs = re.split(r"(?m)^GF_LOG_\d+\s*$", so.split("GF_DATA_MANIFEST")[0])[1:]
            peaks = [int(x) / 1024 for x in re.findall(r"GF_PEAK_KB=(\d+)", so)]
            smoke_peak["mb"] = max(peaks) if peaks else None
            return b, so, rc, secs, logs

        step["at"] = "smoke"
        smoke_peak: dict = {}
        parallel = copies = max(1, min(repeats, PARALLEL))
        b, so, rc, secs, logs = await smoke_run(copies)
        if copies > 1 and (not b.checkpoint or not logs or rc not in (0, 124)):
            # copies in parallel failed (b5a: 4 TensorFlow attacks on dense 2708 x 2708 matrices, exit 120, while one
            # copy runs): one at a time, and the cell runs its repeats one at a time too
            failed_rc, parallel = rc, 1
            b, so, rc, secs, logs = await smoke_run(1)
            copies = 1
            r.notes.append(f"{min(repeats, PARALLEL)} copies in parallel failed (exit {failed_rc}); one copy passed, so "
                           "the cell runs its repeats one at a time")
        r.manifest = _manifest(so)
        r.smoke = {"copies": copies, "rc": rc, "seconds": secs, "timed_out": rc == 124, "peak_mb": smoke_peak.get("mb")}
        fit = memory_parallel(smoke_peak.get("mb"))
        if smoke_peak.get("mb") and fit < parallel:  # plan D6.4: what fits the VM's memory, not the vCPU count
            r.notes.append(f"one run peaks at {smoke_peak['mb']:.0f} MB: {fit} fit the VM's {VM_MB} MB at once (not "
                           f"{parallel}), so the cell runs its repeats {fit} at a time")
            parallel = fit
        r.smoke["parallel"] = parallel
        if not b.checkpoint or not logs or (rc not in (0, 124)):
            return finish("smoke", f"the smoke run failed (exit {rc}): {(logs[0] if logs else so + (b.stderr or ''))[-1200:]}")
        r.bindings = bind_metrics(logs[0], [{"claim_id": c["claim_id"], "metric": c["metric"],
                                             "paper_value": c["paper_value"]} for c in r.claims])
        if paper_text:  # plan D6.6: a tie settled by the paper's own sentence, never by closeness to its number
            from gapfinder.harness_auto import bind_by_quote

            for i, bb in enumerate(r.bindings):
                if bb.label is None and bb.tied:
                    q = bind_by_quote(bb, logs[0], paper_text)
                    if q is not None:
                        c = next(x for x in r.claims if x["claim_id"] == bb.claim_id)
                        ratio = abs(c["paper_value"]) / abs(q.value) if q.value else 1.0
                        q.scale = 100.0 if 30 < ratio < 300 else 0.01 if 0.003 < ratio < 0.03 else 1.0
                        r.bindings[i] = q
                        r.notes.append(f"{bb.claim_id}: the tie {', '.join(bb.tied)} settled by the paper: "
                                       f"\"{q.quote[:160]}\"")
        if bind:
            from gapfinder.harness_auto import labelled_numbers as _ln

            printed = _ln(logs[0])
            for cid, label in bind.items():
                if label not in printed:
                    return finish("metrics", f"--bind {cid}={label!r}: the run printed no such label; it printed "
                                             + ", ".join(repr(k) for k in printed))
                c = next((x for x in r.claims if x["claim_id"] == cid), None)
                if c is None:
                    return finish("metrics", f"--bind {cid}: no such claim")
                v = printed[label]
                ratio = abs(c["paper_value"]) / abs(v) if v else 1.0
                scale = 100.0 if 30 < ratio < 300 else 0.01 if 0.003 < ratio < 0.03 else 1.0
                old = next((x for x in r.bindings if x.claim_id == cid), None)
                r.bindings = [x for x in r.bindings if x.claim_id != cid] + [Binding(
                    cid, label, v, scale, alternatives=old.alternatives if old else [],
                    refused=f"(given by the runner{'; the binder had refused: ' + old.refused if old and old.refused else ''})")]
        bound = {bb.claim_id: bb for bb in r.bindings if bb.label}
        if r.claims[0]["claim_id"] not in bound:
            return finish("metrics", "the target's number can't be bound: "
                          + next(bb.refused for bb in r.bindings if bb.claim_id == r.claims[0]["claim_id"]))
        from gapfinder.harness_auto import labelled_numbers

        per = {}
        for log in logs:
            found = labelled_numbers(log)
            for c in r.claims:
                if c["claim_id"] in bound and bound[c["claim_id"]].label in found:
                    per.setdefault(c["name"], []).append(found[bound[c["claim_id"]].label] * bound[c["claim_id"]].scale)
        r.smoke["per_run_values"] = per
        # claims at fixed knob values and learning-curve points read the label of the row claim with their metric
        by_fam = {_family(c["metric"]): (c, bound[c["claim_id"]]) for c in reversed(r.claims) if c["claim_id"] in bound}
        for p in r.points:
            hit = by_fam.get(_family(p["metric"]))
            p["name"] = hit[0]["name"] if hit else None
        r.points = [p for p in r.points if p["name"]]
        logged = _per_epoch(logs[0])
        off = 1 if logged and min(logged) == 0 else 0
        for c in r.curves:
            hit = by_fam.get(_family(c["metric"]))
            c["label"], c["scale"] = (hit[1].label, hit[1].scale) if hit else (None, 1.0)
            c["name"] = f"{hit[0]['name']}_e{c['epoch']}" if hit else None
            c["logged"] = bool(hit) and hit[1].label in logged.get(c["epoch"] - off, {})
        r.curves = [c for c in r.curves if c["logged"]]
        r.smoke["seeds_vary"] = any(len(set(v)) > 1 for v in per.values()) if copies > 1 else None
        per_run = secs if rc == 0 else progress_estimate(logs[0], secs, int(t.knobs[t.epochs_knob]["default"])
                                                         if t.epochs_knob else None)
        if per_run is None:
            return finish("smoke", f"the run didn't finish in {int(smoke_timeout)} s and its length can't be estimated "
                                   "(no epoch counter in its output); set the scale by hand")
        # in one VM the cell runs PARALLEL at a time (the smoke run measured exactly that); as shards, each repeat is a job
        cell = per_run * math.ceil(repeats / parallel)
        r.plan = shrink_plan(cell) if cell <= OPERATION_S * 0.8 or repeats == 1 else \
            shrink_plan(per_run * repeats, independent_jobs=repeats)
        if r.plan.action == "shrink" and not t.epochs_knob:
            return finish("smoke", f"one run takes about {per_run:.0f} s, more than an operation allows, and the script "
                                   "has no epochs or steps flag to shrink")
        # the base checkpoint: the smoke run's, with the data kept and its outputs deleted; the emitter bound now
        traj = trajectories_for_emit(r.claims, bound, logs[0])
        em = emit_script(bindings_for_emit(r.claims, bound, r.curves), traj)
        final = "rm -rf out; ls gf_harness"
        final_files = {f"{HARNESS_DIR}/emit.py": em.encode()}
        era = None
        if paper_date:
            from gapfinder.env_build import third_party_imports

            py, installed = env_year.parse_freeze(a.stdout or "")
            mods = third_party_imports(root)
            own = env_year.own_package(root)
            releases: dict[str, list[str]] = {}
            cache = Path(os.environ.get("GF_PYPI_CACHE") or Path(".gf_cache") / "pypi")
            pins, why = env_year.paper_year_pins(mods, installed, paper_date, py or "3.10", cache=cache, own=own,
                                                 releases=releases)
            deps, dep_why, brought = (env_year.dependency_pins(pins, installed, paper_date, py or "3.10", cache=cache)
                                      if pins else ({}, {}, {}))
            r.paper_year = {"date": str(paper_date), "python": py, "pins": pins, "skipped": why, "used": False,
                            "own": own, "releases": releases, "deps": deps, "dep_why": dep_why, "brought": brought}
            if pins:
                every = {**pins, **deps}
                check_mods = mods + ([own["module"]] if own and own["dist"] in pins else [])
                final += (f"; {env_year.install_command(every)}; "
                          f"{sprefix}{env_year.import_check(every, check_mods, brought)}")
            if repo and commit:
                era = env_year.commit_before(repo, commit, paper_date)
                if era:
                    era["commits"] = env_year.commits_between(repo, commit, era["date"])
                    final += f"; {env_year.era_fetch_command(era['sha'])}"
                    final_files[env_year.ERA_SCRIPT] = env_year.era_fetch_script(repo).encode()
        w = await backend.run(b.checkpoint, final, env=senv, timeout=OPERATION_S - 100, disposable=False,
                              files={**final_files, **(sfiles if r.paper_year and r.paper_year["pins"] else {})})
        if w.exit_code != 0 or not w.checkpoint:
            return finish("data", "writing the emitter into the base checkpoint failed")
        if r.paper_year and r.paper_year["pins"]:
            y = r.paper_year
            failed = sorted(set(re.findall(r"GF_PIN_FAIL (\S+)", w.stdout or "")))
            imports = env_year.parse_import_check(w.stdout or "")
            all_ok = not failed and imports.get("all", False)
            direct = sorted(y["pins"])
            # a package whose bundle (it and the dependencies it brought) installed; alone: it imports by itself too
            installed_ok = [d for d in direct if not ({d, *y["brought"].get(d, [])} & set(failed))]
            alone = ([d for d in installed_ok if imports.get(env_year.dirname(d), False)] if len(direct) > 1
                     else (installed_ok if all_ok else []))
            y.update(failed=failed, imports=imports, all_ok=all_ok, alone=alone,
                     usable=installed_ok if all_ok else alone)
            y["used"] = bool(y["usable"])
            if not y["used"]:
                y["why_not"] = ("the old versions don't import" if not failed
                                else f"{len(failed)} of {len(y['pins']) + len(y['deps'])} pins failed to install")
        if era:
            n_files = int((re.search(r"GF_ERA_FILES (\d+)", w.stdout or "") or [0, 0])[1])
            era["files"] = n_files
            r.paper_era = era
        (out / HARNESS_DIR).mkdir(exist_ok=True)
        (out / HARNESS_DIR / "emit.py").write_text(em, encoding="utf-8")
        r.spec = spec_dict(out.name, w.checkpoint, str(root.resolve()), t, r.claims, bound, repeats, r.plan, per_run,
                           r.curves, parallel, traj)
        lits = literal_knobs(root, t, r.spec["run"]["command"])
        if lits:  # plan D6.7: a script with few flags has its settings in the code
            r.spec["knobs"].update(lits)
            r.notes.append(f"the script exposes {len(t.knobs)} flag(s): {len(lits)} named literal(s) it runs became "
                           "patch knobs (in memory, no file edited): " + ", ".join(k.split(":", 3)[-1] for k in lits))
        library: dict = {}
        if r.paper_year and r.paper_year["used"]:
            y = r.paper_year
            r.spec["run"]["command"] = env_year.run_prefix() + r.spec["run"]["command"]
            r.spec["knobs"][env_year.KNOB] = {"layer": "environment", "default": "0", "choices": env_year.knob_choices(
                [env_year.bundle(d, y["brought"]) for d in y["alone"]], y["all_ok"])}
            own = y.get("own") or {}
            library["pins"] = {d: {"old": y["pins"][d], "installed": (own.get("version") if d == own.get("dist") else
                                                                      None) or y["releases"].get(d, [None])[-1],
                                   "dir": env_year.dirname(d), "bundle": env_year.bundle(d, y["brought"]),
                                   "deps": {x: y["deps"][x] for x in y["brought"].get(d, [])},
                                   "releases": y["releases"].get(d, []), "own": d == own.get("dist"),
                                   "imports_alone": d in y["alone"],
                                   "modules": [own["module"]] if d == own.get("dist") else
                                   [m for m in mods if env_year.DIST.get(m, m) == d],
                                   "path": own.get("path") if d == own.get("dist") else None}
                               for d in y["usable"]}
            library["date"], library["python"] = y["date"], y["python"]
        if era and era.get("files"):
            r.spec["run"]["command"] = env_year.era_prefix() + r.spec["run"]["command"]
            r.spec["knobs"][env_year.ERA_KNOB] = {"layer": "environment", "default": "0", "choices": ["0", "1"]}
            library["era"] = {"repo": repo, "commit": commit, **era}
        if library:
            r.spec["library"] = library
        import yaml

        (out / "spec.yaml").write_text("# written by `gapfinder harness`; read HARNESS.md and approve the commands\n"
                                       + yaml.safe_dump(r.spec, sort_keys=False, width=200), encoding="utf-8")
        (out / "targets.json").write_text(json.dumps(targets_json(r.claims, bound, r.points, r.curves), indent=1), encoding="utf-8")
        r.ok = True
        return finish("done")

    try:
        return await run()
    except InfraError as exc:  # a Sandboxes failure at any step: say where, keep what was built
        return finish(step["at"], f"infrastructure error (re-run unchanged): {str(exc)[:300]}")
