"""What a dry-run trace says about each knob: its role, from the sink its value reached.

Input: the per-process records of `gapfinder/sandbox/trace_hook.py` (config values and sink arguments with
their repo call sites). Output: a `TraceReport`:

- `roles`: knob -> role, when the knob's runtime value reached exactly one kind of sink and no other knob
  has the same value there. Roles: `rate` (optimizer step size: a log-scale number, never a fraction or 0),
  `rate0` (weight decay: log-scale, 0 meaningful), `fraction` (dropout, momentum, a decay factor),
  `size` (batch size, layer width: a positive integer, powers of two natural), `count` (a loop bound, a
  scheduler step: a positive integer), `multiplier` (a loop bound is this knob times another setting's
  value), `seed` (random seeds: noise, not a cause).
- `ambiguous`: sink arguments whose value several knobs share (no role is guessed).
- `leads`: sink arguments with no knob behind them whose value is a literal in the repo, at the call site
  or in a same-file assignment of the name passed there. Each can become a patch knob
  (`@ast:file:line:name`).

Matching is by value, which is why ambiguity is reported rather than resolved: two knobs both at 0.5 can't be
told apart from one trace. A knob's runtime value is taken from the trace's config records (argparse, absl,
yaml, json) when they name it, so a config file that overrides a flag (GraphMAE's configs.yml) is seen as it
runs; otherwise the spec default is used.
"""

from __future__ import annotations

import ast
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path

# (sink kind, argument) -> role
_ROLE = {
    ("optimizer", "lr"): "rate", ("optimizer", "learning_rate"): "rate",
    ("optimizer", "weight_decay"): "rate0", ("optimizer", "eps"): "rate0",
    ("optimizer", "momentum"): "fraction", ("optimizer", "betas"): "fraction", ("optimizer", "beta1"): "fraction",
    ("optimizer", "beta2"): "fraction", ("optimizer", "alpha"): "fraction", ("optimizer", "rho"): "fraction",
    ("dropout", "p"): "fraction",
    ("batch", "batch_size"): "size",
    ("width", "out_features"): "size",
    ("scheduler", "step_size"): "count", ("scheduler", "T_max"): "count", ("scheduler", "patience"): "count",
    ("scheduler", "gamma"): "fraction", ("scheduler", "factor"): "fraction", ("scheduler", "eta_min"): "rate0",
    ("seed", "seed"): "seed", ("seed", "arg0"): "seed",
}


@dataclass
class KnobRole:
    knob: str
    role: str
    sink: str  # e.g. "optimizer.lr (Adam)" or "range() bound"
    site: str | None  # repo file:line that reached the sink
    value: str


@dataclass
class Lead:
    file: str
    line: int
    name: str
    literal: str
    sink: str

    @property
    def knob(self) -> str:
        from gapfinder.sandbox.ast_patch import knob_name

        return knob_name(self.file, self.line, self.name)


@dataclass
class TraceReport:
    processes: int = 0
    roles: dict[str, KnobRole] = field(default_factory=dict)
    ambiguous: list[dict] = field(default_factory=list)
    leads: list[Lead] = field(default_factory=list)
    runtime_values: dict[str, str] = field(default_factory=dict)  # knob -> every value its config records gave
    steps: int = 0

    def to_dict(self) -> dict:
        return {"processes": self.processes, "steps": self.steps,
                "roles": {k: asdict(v) for k, v in self.roles.items()}, "ambiguous": self.ambiguous,
                "leads": [asdict(x) | {"knob": x.knob} for x in self.leads], "runtime_values": self.runtime_values}

    def summary(self) -> str:
        r = ", ".join(f"{k}={v.role}" for k, v in sorted(self.roles.items())) or "none"
        return (f"trace of {self.processes} process(es): roles {r}; {len(self.leads)} literal lead(s); "
                f"{len(self.ambiguous)} ambiguous sink value(s)")


def _num(v) -> float | None:
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        try:
            return float(v)
        except ValueError:
            return None
    return None


def _same(a: float, b: float) -> bool:
    return a == b or (a != 0 and abs(a - b) <= 1e-9 * max(abs(a), abs(b)))


def _norm(name: str) -> str:
    return name.strip().lstrip("-").replace("-", "_").lower()


def config_values(rec: dict, knobs: dict) -> dict[str, set[float]]:
    """Every numeric value the process's config records give each knob (argparse, absl, every yaml/json path
    ending in the knob's name), plus the spec default. A config file that holds several experiments
    (GraphMAE's configs.yml, one entry per dataset) gives several values; the sink tells which one ran."""
    want = {_norm(k): k for k in knobs}
    out: dict[str, set[float]] = {k: set() for k in knobs}
    for k, kn in knobs.items():
        if (x := _num(kn.default)) is not None:
            out[k].add(x)
    for c in rec.get("config", []):
        for key, v in c.get("values", {}).items():
            k = want.get(_norm(key.split(".")[-1]))
            if k is not None and (x := _num(v)) is not None:
                out[k].add(x)
    return out


def _sink_values(rec: dict):
    for s in rec.get("sinks", []):
        for arg, v in (s.get("args") or {}).items():
            vals = v if isinstance(v, list) else [v]
            for i, x in enumerate(vals):
                x = _num(x)
                if x is None:
                    continue
                if arg == "betas":  # (beta1, beta2)
                    yield s, f"beta{i + 1}", x
                else:
                    yield s, arg, x


def analyze(records: list[dict], knobs: dict, repo_root: Path | None = None) -> TraceReport:
    """`knobs`: the spec's knobs (name -> Knob). `repo_root`: the artifact's code, to read literal leads."""
    rep = TraceReport(processes=len(records), steps=sum(r.get("steps", 0) for r in records))
    roles: dict[str, set] = {}
    where: dict[str, KnobRole] = {}
    unmatched: list[tuple[dict, str, float]] = []
    seen_vals: dict[str, set[float]] = {}

    def hit(k, role, label, site):
        roles.setdefault(k, set()).add(role)
        where.setdefault(k, KnobRole(k, role, label, site, knobs[k].default))

    for rec in records:
        cand = config_values(rec, knobs)
        for k, vs in cand.items():
            seen_vals.setdefault(k, set()).update(vs)
        for s, arg, x in _sink_values(rec):
            role = _ROLE.get((s["kind"], arg))
            if role is None:
                continue
            hits = [k for k, vs in cand.items() if any(_same(v, x) for v in vs)]
            if len(hits) > 1:  # break a tie only by name: the knob named like the argument
                named = [k for k in hits if _norm(k).endswith(_norm(arg)) or _norm(arg).endswith(_norm(k))]
                hits = named if len(named) == 1 else hits
            site = f"{s['site'][0]}:{s['site'][1]}" if s.get("site") else None
            label = f"{s['kind']}.{arg} ({s['cls']})"
            if len(hits) == 1:
                hit(hits[0], role, label, site)
            elif len(hits) > 1:
                rep.ambiguous.append({"sink": label, "site": site, "value": x, "knobs": sorted(hits)})
            elif role != "seed":
                unmatched.append((s, arg, x))
        # range() bounds in repo code: a loop count, or a multiplier when the bound is a product
        for site, stops in (rec.get("ranges") or {}).items():
            for stop in stops:
                hits = [k for k, vs in cand.items() if any(_same(v, float(stop)) and v >= 2 for v in vs)]
                if len(hits) == 1:
                    hit(hits[0], "count", "range() bound", site)
                    continue
                if hits:
                    continue
                for k, vs in cand.items():
                    for v in vs:
                        if v < 2 or v != int(v) or stop % int(v):
                            continue
                        other = stop // int(v)
                        partners = [j for j, ws in cand.items() if j != k and any(_same(w, float(other)) for w in ws)]
                        if len(partners) == 1 and other >= 2:
                            hit(k, "multiplier", f"range() bound = {k} x {partners[0]}", site)
    for k, rs in roles.items():
        if len(rs) == 1:  # a knob that reaches two kinds of sink gets no role (it isn't one thing)
            rep.roles[k] = where[k] if where[k].role in rs else KnobRole(k, next(iter(rs)), where[k].sink,
                                                                           where[k].site, where[k].value)
    rep.runtime_values = {k: ", ".join(_fmt(v) for v in sorted(vs)[:6]) for k, vs in seen_vals.items() if vs}
    if repo_root is not None:
        rep.leads = _literal_leads(unmatched, Path(repo_root))
    return rep


def _literal_leads(unmatched, root: Path) -> list[Lead]:
    out, seen = [], set()
    for s, arg, x in unmatched:
        if not s.get("site"):
            continue
        rel, line = s["site"]
        path = root / rel
        try:
            src = path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(src)
        except (OSError, SyntaxError, ValueError):
            continue
        lead = _find_literal(tree, line, arg, x)
        if lead is None:
            continue
        name, at = lead
        key = (rel, at, name)
        if key not in seen:
            seen.add(key)
            out.append(Lead(rel, at, name, _fmt(x), f"{s['kind']}.{arg} ({s['cls']})"))
    return out


def _lit(node) -> float | None:
    v = getattr(node, "value", None) if isinstance(node, ast.Constant) else getattr(node, "n", None)
    return _num(v)


def _find_literal(tree, line: int, arg: str, x: float):
    """(name, line) of the literal `x` that reaches the sink called on `line`: a keyword literal in that call,
    or the same-file assignment of the name passed there."""
    passed = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node, "lineno", None) == line:
            for kw in node.keywords:
                if kw.arg is None:
                    continue
                if (v := _lit(kw.value)) is not None and _same(v, x):
                    return kw.arg, line
                if isinstance(kw.value, ast.Name) and _norm(kw.arg) == _norm(arg):
                    passed = kw.value.id
            for a in node.args:
                if isinstance(a, ast.Name):
                    passed = passed or a.id
    if passed is None:
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id == passed and (v := _lit(node.value)) is not None and _same(v, x):
                return passed, node.lineno
    return None


def _fmt(x: float) -> str:
    return str(int(x)) if x == int(x) and not math.isinf(x) else f"{x:g}"


def apply_roles(spec, report: TraceReport) -> list[str]:
    """Write traced roles onto the spec's knobs (knob.role; multiplier knobs also get knob.multiplier).
    Returns the knobs that changed."""
    changed = []
    for k, r in report.roles.items():
        kn = spec.knobs.get(k)
        if kn is None or kn.role == r.role:
            continue
        kn.role = r.role
        if r.role == "multiplier":
            kn.multiplier = True
        changed.append(k)
    return changed

