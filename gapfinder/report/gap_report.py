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
    generated: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M"))

    @classmethod
    def from_search(cls, search: GapSearch, results: list[ClaimResult], paper: str) -> "GapReport":
        return cls(paper=paper, artifact=search.spec.name, results=results,
                   noise={m: b.to_dict() for m, b in search.bands.items()}, naive=dict(search.naive),
                   runs=search.runs_used, setup_runs=search.orch.cost.setup_runs, cost=search.orch.cost.summary(),
                   unmapped_assumptions=search.unmapped, untestable=list(search.untestable))

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
                "claims": [claim(r) for r in self.results]}

    def to_markdown(self) -> str:
        out = [f"# Gap Report: {self.paper}", "",
               f"Artifact `{self.artifact}` · generated {self.generated} · {self.runs} branch runs "
               f"({self.setup_runs} build/load setups) · sandbox ${self.cost.get('sandbox_usd', 0):.4f}"]
        if self.partial:
            out += ["", "> **Partial report:** the run or dollar budget ran out before every claim was verified."]
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
