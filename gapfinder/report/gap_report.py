"""Gap Report: one card per claim, with the label, evidence, noise and a replay recipe."""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from gapfinder.search.engine import ClaimResult, GapSearch


def _pct(x: float | None) -> str:
    return "n/a" if x is None else f"{x * 100:+.1f}%"


@dataclass
class GapReport:
    paper: str
    artifact: str
    results: list[ClaimResult]
    noise: dict[str, dict]
    naive: dict[str, float]
    runs: int
    setup_runs: int
    cost: dict
    unmapped_assumptions: list[str] = field(default_factory=list)
    untestable: list[tuple[str, str]] = field(default_factory=list)
    closest: list[dict] = field(default_factory=list)
    triaged: list[dict] = field(default_factory=list)
    setup_check: dict | None = None
    generated: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M"))

    @classmethod
    def from_search(cls, search: GapSearch, results: list[ClaimResult], paper: str) -> "GapReport":
        return cls(paper=paper, artifact=search.spec.name, results=results,
                   noise={m: b.to_dict() for m, b in search.bands.items()}, naive=dict(search.naive),
                   runs=search.runs_used, setup_runs=search.orch.cost.setup_runs, cost=search.orch.cost.summary(),
                   unmapped_assumptions=search.unmapped, untestable=list(search.untestable),
                   closest=search.closest_overall(), triaged=list(search.triaged),
                   setup_check=search.setup_check)

    @property
    def partial(self) -> bool:
        return any(r.status == "partial" for r in self.results)

    def to_dict(self) -> dict:
        def claim(r: ClaimResult) -> dict:
            d = {k: v for k, v in asdict(r).items() if k not in ("attribution", "plausibility", "target")}
            d["target"] = asdict(r.target)
            d["attribution"] = r.attribution.model_dump() if r.attribution else None
            d["plausibility"] = {k: asdict(p) for k, p in r.plausibility.items()}
            return d
        return {"paper": self.paper, "artifact": self.artifact, "generated": self.generated,
                "partial": self.partial, "runs": self.runs, "setup_runs": self.setup_runs, "cost": self.cost,
                "naive": self.naive, "noise": self.noise, "unmapped_assumptions": self.unmapped_assumptions,
                "untestable": [{"knob": k, "value": v} for k, v in self.untestable],
                "closest_overall": self.closest,
                "triaged_failures": self.triaged,
                "setup_check": self.setup_check,
                "claims": [claim(r) for r in self.results]}

    def to_markdown(self) -> str:
        out = [f"# Gap Report: {self.paper}", "",
               f"Artifact `{self.artifact}` · generated {self.generated} · {self.runs} branch runs "
               f"({self.setup_runs} build/load setups) · sandbox ${self.cost.get('sandbox_usd', 0):.4f}"]
        if self.partial:
            out += ["", "> **Partial report:** the run or dollar budget ran out before every claim was verified."]
        if self.setup_check:
            out += ["", f"> **Setup check:** {self.setup_check['note']}."]
        out += ["", "| Claim | Label | Gap before | Gap after | Noise band | Explained by |", "|---|---|---|---|---|---|"]
        for r in self.results:
            label = r.attribution.confidence_label if r.attribution else "Reproduced"
            by = ", ".join(f"`{k}={v}`" for k, v in r.changes.items()) or "—"
            out.append(f"| {r.target.claim_id} ({r.target.metric}) | {label} | {_pct(r.gap_before)} | "
                       f"{_pct(r.gap_after)} | ±{r.band * 100:.1f}% | {by} |")
        for r in self.results:
            out += ["", f"## {r.target.claim_id}: {r.target.metric} (paper {r.target.paper_value:g})"]
            if r.status == "reproduced":
                out.append(f"Reproduces: naive gap {_pct(r.gap_before)} is inside the noise band ±{r.band * 100:.1f}%.")
                continue
            if r.status == "inconclusive":
                out.append(f"**Inconclusive** · naive gap {_pct(r.gap_before)} is inside the noise band "
                           f"±{r.band * 100:.1f}%, but the band is too wide to call it a reproduction.")
                out += [""] + [f"- {n}" for n in r.notes]
                continue
            a = r.attribution
            out.append(f"**{a.confidence_label}** · gap {_pct(r.gap_before)} → {_pct(r.gap_after)} · "
                       f"{r.hypotheses_tested} hypotheses tested")
            if r.plausibility:
                out += ["", "Evidence:"]
                out += [f"- `{k}={r.changes[k]}`: {'supported' if p.supported else 'UNSUPPORTED'}, {p.reason}"
                        for k, p in r.plausibility.items()]
            if r.counterfactual:
                out += ["", "Counterfactual (revert one knob; the gap must come back):"]
                out += [f"- without `{k}`: gap {_pct(v['gap_without'])} ({'ok' if v['ok'] else 'gap did NOT return'})"
                        for k, v in r.counterfactual.items()]
            if r.held_out:
                out += ["", "Held-out claims (must not get worse beyond noise):"]
                out += [f"- {cid}: {_pct(v['gap_before'])} → {_pct(v['gap_after'])} ({'ok' if v['ok'] else 'WORSE'})"
                        for cid, v in r.held_out.items()]
            if r.replay:
                x = r.replay[0]
                out += ["", "Replay: fork checkpoint `" + str(x["parent_checkpoint"]) + "` and run",
                        "```", " ".join(f"{k}={v}" for k, v in x["env"].items()) + f" {x['command']}", "```",
                        f"(result checkpoint `{x['result_checkpoint']}`; {len(r.replay)} repeat(s) recorded)"]
            if r.notes:
                out += ["", "Notes:"] + [f"- {n}" for n in r.notes]
        if self.closest:
            ids = list(self.closest[0]["gaps"])
            out += ["", "## Closest configurations across all claims",
                    "Not an attribution: the labels above judge one claim at a time and require the held-out "
                    "claims not to get worse. This table shows which measured changes bring several claims "
                    "toward the paper together (gap per claim, mean of absolute gaps).", "",
                    "| Configuration | Runs | " + " | ".join(ids) + " | Mean |gap| |",
                    "|---|---|" + "---|" * len(ids) + "---|"]
            naive = {r.target.claim_id: r.gap_before for r in self.results}
            for row in self.closest:
                cfg = ", ".join(f"`{k}={v}`" for k, v in row["changes"].items()) or "naive (reproduction as run)"
                out.append(f"| {cfg} | {row['runs']} | " + " | ".join(_pct(row["gaps"][i]) for i in ids)
                           + f" | {row['mean_abs_gap'] * 100:.1f}% |")
        if self.triaged:
            out += ["", "## Failed hypotheses (triaged by Nemotron 3 Super)"]
            for x in self.triaged:
                tail = (f"; retried as `{x['knob']}={x['retried']}`" if x.get("retried") else
                        f"; suggested `{x['suggestion']}`, already measured" if x.get("suggestion") else "")
                out.append(f"- `{x['knob']}={x['value']}`: {x['kind']}, {x['why'].rstrip('. ')}{tail}")
        if self.untestable:
            out += ["", "## Not testable within the budget",
                    "Candidate values above the harness spec's cost limits (e.g. the paper's full scale). "
                    "A gap that only these could close stays Unexplained here: " +
                    ", ".join(f"`{k}={v}`" for k, v in self.untestable)]
        if self.unmapped_assumptions:
            out += ["", "## Not testable with this harness",
                    "Assumptions about knobs the harness spec can't set: " +
                    ", ".join(f"`{k}`" for k in self.unmapped_assumptions)]
        return "\n".join(out) + "\n"

    def write(self, out_dir: str | Path) -> tuple[Path, Path]:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        md, js = out_dir / "gap_report.md", out_dir / "gap_report.json"
        md.write_text(self.to_markdown(), encoding="utf-8")
        js.write_text(json.dumps(self.to_dict(), indent=2, default=str), encoding="utf-8")
        return md, js
