"""Differential trace: where does a reproduction's run differ from a reference implementation's?

    gapfinder diff --spec mine.yaml --ref-spec reference.yaml --out runs/diff

When there is a reference implementation (the authors' code, or an earlier version that worked), the paper
is not the only witness: the reference's own run says what values reach the optimizer, the dropout layers,
the data loaders and the schedulers. TTrace (2025) localises bugs in a training implementation by comparing
its intermediate values with a reference run; delta debugging (Zeller, 2002) then shrinks the set of
differences to the ones that matter. This module does the first at the level of settings, from one dry run
of each program with the sink-tracing hook (gapfinder/sandbox/trace_hook.py), and hands the differences to
the search, whose bisect step does the second.

- `profile`: per (sink kind, argument), the set of values that reached it in a program's run; and per sink
  kind, the classes used (Adam or SGD).
- `diff`: the keys whose value sets differ. A single value on each side is a value difference; several
  (layer widths) or a key on one side only are reported, not tested; a different class is structural.
- `hypotheses`: for each value difference, the reproduction's knob whose traced value reached that sink, set
  to the reference's value; or, with no knob behind it, the literal at the call site as a patch knob. Each
  carries the reference trace as measurement evidence.

The reference's measured numbers are the targets, so a difference is reported as a cause only when setting
it closes the measured gap, like any other hypothesis.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path

from gapfinder.ledger.schemas import Assumption, AssumptionStatus, Evidence
from gapfinder.search.trace import _ROLE, _fmt, _num, _same, _sink_values, analyze, config_values


@dataclass
class Difference:
    key: str  # "optimizer.lr"
    kind: str  # value | several | missing | structural
    reference: list[str]
    mine: list[str]
    ref_site: str | None = None
    mine_site: str | None = None

    def text(self) -> str:
        where = f" (reference at {self.ref_site}; yours at {self.mine_site})" if self.ref_site or self.mine_site else ""
        return f"{self.key}: reference {', '.join(self.reference) or 'never reached'}; yours " \
               f"{', '.join(self.mine) or 'never reached'}{where}"


@dataclass
class Profile:
    values: dict[str, set[float]] = field(default_factory=dict)
    sites: dict[str, str] = field(default_factory=dict)
    classes: dict[str, set[str]] = field(default_factory=dict)


def profile(records: list[dict]) -> Profile:
    p = Profile()
    for rec in records:
        for s, arg, x in _sink_values(rec):
            if (s["kind"], arg) not in _ROLE or _ROLE[(s["kind"], arg)] == "seed":
                continue  # seeds are noise, not a setting to align
            key = f"{s['kind']}.{arg}"
            p.values.setdefault(key, set()).add(x)
            if s.get("site"):
                p.sites.setdefault(key, f"{s['site'][0]}:{s['site'][1]}")
        for s in rec.get("sinks", []):
            if s["kind"] in ("optimizer", "scheduler"):
                p.classes.setdefault(s["kind"], set()).add(s["cls"])
    return p


def _uniq(vals: set[float]) -> list[float]:
    out: list[float] = []
    for v in sorted(vals):
        if not any(_same(v, u) for u in out):
            out.append(v)
    return out


def diff(reference: list[dict], mine: list[dict]) -> list[Difference]:
    r, m = profile(reference), profile(mine)
    out = []
    for kind in sorted(set(r.classes) | set(m.classes)):
        if r.classes.get(kind, set()) != m.classes.get(kind, set()):
            out.append(Difference(f"{kind} class", "structural", sorted(r.classes.get(kind, ())),
                                  sorted(m.classes.get(kind, ()))))
    for key in sorted(set(r.values) | set(m.values)):
        a, b = _uniq(r.values.get(key, set())), _uniq(m.values.get(key, set()))
        if len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b)):
            continue
        kind = "missing" if not a or not b else "value" if len(a) == 1 and len(b) == 1 else "several"
        out.append(Difference(key, kind, [_fmt(x) for x in a], [_fmt(x) for x in b], r.sites.get(key), m.sites.get(key)))
    return out


@dataclass
class Plan:
    """What the search will test: assumptions on existing knobs, and literal leads as patch knobs."""
    assumptions: list[Assumption] = field(default_factory=list)
    patch_knobs: dict[str, str] = field(default_factory=dict)  # @ast knob -> its literal (the default)
    untestable: list[Difference] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"assumptions": [a.model_dump() for a in self.assumptions], "patch_knobs": self.patch_knobs,
                "untestable": [asdict(d) for d in self.untestable]}


def hypotheses(diffs: list[Difference], mine: list[dict], knobs: dict, root: Path | None) -> Plan:
    rep = analyze(mine, knobs, root)
    runtime: dict[str, set[float]] = {}
    for rec in mine:
        for k, vs in config_values(rec, knobs).items():
            runtime.setdefault(k, set()).update(vs)
    plan = Plan()
    for d in diffs:
        if d.kind != "value":
            plan.untestable.append(d)
            continue
        ref_v, my_v = _num(d.reference[0]), _num(d.mine[0])
        ev = Evidence(kind="measurement", ref="reference trace",
                      quote=f"reference run: {d.key} = {d.reference[0]}" + (f" at {d.ref_site}" if d.ref_site else ""))
        owners = [k for k, role in rep.roles.items() if role.sink.startswith(d.key + " ")
                  and any(_same(v, my_v) for v in runtime.get(k, ()))]
        if len(owners) == 1:
            k = owners[0]
            plan.assumptions.append(Assumption(
                id=f"D{len(plan.assumptions) + 1}", knob=k, layer=knobs[k].layer, paper_value=d.reference[0],
                code_default=knobs[k].default, candidate_values=[d.reference[0]], evidence=[ev], prior_score=0.9,
                status=AssumptionStatus.stated_code_differs.value))
            continue
        leads = [x for x in rep.leads if x.sink.startswith(d.key + " ") and _same(_num(x.literal), my_v)]
        if len(leads) == 1:
            k = leads[0].knob
            plan.patch_knobs[k] = leads[0].literal
            plan.assumptions.append(Assumption(
                id=f"D{len(plan.assumptions) + 1}", knob=k, layer="environment", paper_value=d.reference[0],
                code_default=leads[0].literal, candidate_values=[_fmt(ref_v)], evidence=[ev], prior_score=0.9,
                status=AssumptionStatus.stated_code_differs.value))
            continue
        plan.untestable.append(d)  # no single knob or literal behind it: reported for a person to look at
    return plan


def report_markdown(diffs: list[Difference], plan: Plan) -> str:
    lines = ["# Where your run differs from the reference", "",
             "From one traced dry run of each program: the values that reached the same library calls.", ""]
    if not diffs:
        return "\n".join(lines + ["No difference in any traced setting."])
    tested = {a.knob: a for a in plan.assumptions}
    lines += ["| setting | reference | yours | tested as |", "|---|---|---|---|"]
    for d in diffs:
        knob = next((a.knob for a in plan.assumptions if f"= {d.reference[0]}" in a.evidence[0].quote
                     and d.key in a.evidence[0].quote), None) if d.kind == "value" else None
        lines.append(f"| `{d.key}` | {', '.join(d.reference) or '-'} | {', '.join(d.mine) or '-'} | "
                     f"{f'`{knob}` = {tested[knob].paper_value}' if knob else 'not tested (' + d.kind + ')'} |")
    return "\n".join(lines)
