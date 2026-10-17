"""Gap Report: one card per claim, with the label, evidence, noise and a replay recipe."""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from gapfinder.ledger.schemas import Attribution
from gapfinder.search.engine import ClaimResult, GapSearch, Target
from gapfinder.report.provenance import collect as collect_provenance
from gapfinder.search.verify import Plausibility


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
    renamed_assumptions: dict[str, str] = field(default_factory=dict)  # ledger name -> spec knob
    spec_only_knobs: list[str] = field(default_factory=list)  # screened though no assumption named them
    corrected_defaults: list[dict] = field(default_factory=list)  # ledger code defaults the code contradicts
    unverified_defaults: list[str] = field(default_factory=list)  # "code differs" the code can't confirm
    trace: dict | None = None  # the dry-run trace (gapfinder/search/trace.py): roles, literal leads
    untestable: list[tuple[str, str]] = field(default_factory=list)
    closest: list[dict] = field(default_factory=list)
    triaged: list[dict] = field(default_factory=list)
    setup_check: dict | None = None
    # what each card needs beyond the search result, keyed by claim id; absent in reports
    # recorded before these existed, and every reader treats a missing entry as "not recorded"
    paper_claims: dict[str, dict] = field(default_factory=dict)  # quote, page, figure of the ledger claim
    measured: dict[str, dict] = field(default_factory=dict)  # the naive runs: repeats, spread
    experiments: dict[str, dict] = field(default_factory=dict)  # branch ids, config vs default, outputs
    effects: dict[str, dict] = field(default_factory=dict)  # candidate minus naive, its interval, run counts
    effect_threshold: float = 1.0  # noise units a screened hypothesis needed to count as a lead
    provenance: dict | None = None  # code commit, models, prompt and spec hashes, cost; None if not recorded
    generated: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M"))

    @classmethod
    def from_search(cls, search: GapSearch, results: list[ClaimResult], paper: str) -> "GapReport":
        return cls(paper=paper, artifact=search.spec.name, results=results,
                   noise={m: b.to_dict() for m, b in search.bands.items()}, naive=dict(search.naive),
                   runs=search.runs_used, setup_runs=search.orch.cost.setup_runs, cost=search.orch.cost.summary(),
                   unmapped_assumptions=search.unmapped, renamed_assumptions=dict(search.renamed),
                   spec_only_knobs=list(search.spec_only),
                   corrected_defaults=list(search.corrected_defaults),
                   unverified_defaults=sorted(search.unverified_defaults),
                   trace=search.trace_report.to_dict() if search.trace_report else None, untestable=list(search.untestable),
                   closest=search.closest_overall(), triaged=list(search.triaged),
                   setup_check=search.setup_check,
                   paper_claims={r.target.claim_id: c for r in results if (c := _paper_claim(search, r.target))},
                   measured={r.target.claim_id: _measured(search, r.target) for r in results},
                   experiments={r.target.claim_id: e for r in results if (e := _experiment(search, r))},
                   effects={r.target.claim_id: e for r in results if (e := _effect(search, r))},
                   effect_threshold=search.cfg.effect_threshold, provenance=collect_provenance(search))

    @classmethod
    def from_dict(cls, d: dict) -> "GapReport":
        """Rebuild a report from its JSON, including reports recorded before the card fields existed."""
        def claim(c: dict) -> ClaimResult:
            t = c.get("target") or {}
            a = c.get("attribution")
            return ClaimResult(
                target=Target(claim_id=t.get("claim_id", "?"), metric=t.get("metric", "?"),
                              paper_value=t.get("paper_value", float("nan")), held_out=t.get("held_out", False),
                              figure=t.get("figure"), tuned_separately=t.get("tuned_separately", False)),
                status=c.get("status", "searched"), gap_before=c.get("gap_before", float("nan")),
                band=c.get("band", 0.0), attribution=Attribution(**a) if a else None,
                changes=c.get("changes") or {}, gap_after=c.get("gap_after"), held_out=c.get("held_out") or {},
                counterfactual=c.get("counterfactual") or {},
                plausibility={k: Plausibility(**p) for k, p in (c.get("plausibility") or {}).items()},
                screen=c.get("screen") or [], hypotheses_tested=c.get("hypotheses_tested", 0),
                replay=c.get("replay") or [], notes=c.get("notes") or [], value_sets=c.get("value_sets") or {},
                diagnosis=c.get("diagnosis"), equivalent=c.get("equivalent") or [], relations=c.get("relations") or {})
        claims = d.get("claims") or []
        return cls(paper=d.get("paper", "?"), artifact=d.get("artifact", "?"), results=[claim(c) for c in claims],
                   noise=d.get("noise") or {}, naive=d.get("naive") or {}, runs=d.get("runs", 0),
                   setup_runs=d.get("setup_runs", 0), cost=d.get("cost") or {},
                   unmapped_assumptions=d.get("unmapped_assumptions") or [],
                   renamed_assumptions=d.get("renamed_assumptions") or {},
                   spec_only_knobs=d.get("spec_only_knobs") or [],
                   corrected_defaults=d.get("corrected_defaults") or [],
                   unverified_defaults=d.get("unverified_defaults") or [],
                   trace=d.get("trace"),
                   untestable=[(x["knob"], x["value"]) for x in d.get("untestable") or []],
                   closest=d.get("closest_overall") or [], triaged=d.get("triaged_failures") or [],
                   setup_check=d.get("setup_check"),
                   paper_claims={c["target"]["claim_id"]: c["paper_claim"] for c in claims if c.get("paper_claim")},
                   measured={c["target"]["claim_id"]: c["measured"] for c in claims if c.get("measured")},
                   experiments={c["target"]["claim_id"]: c["experiment"] for c in claims if c.get("experiment")},
                   effects={c["target"]["claim_id"]: c["effect"] for c in claims if c.get("effect")},
                   effect_threshold=d.get("effect_threshold", 1.0), provenance=d.get("provenance"),
                   generated=d.get("generated", "not recorded"))

    @property
    def partial(self) -> bool:
        return any(r.status == "partial" for r in self.results)

    def to_dict(self) -> dict:
        def claim(r: ClaimResult) -> dict:
            d = {k: v for k, v in asdict(r).items() if k not in ("attribution", "plausibility", "target")}
            d["target"] = asdict(r.target)
            d["attribution"] = r.attribution.model_dump() if r.attribution else None
            d["plausibility"] = {k: asdict(p) for k, p in r.plausibility.items()}
            d.update(self.card(r))
            return d
        return {"paper": self.paper, "artifact": self.artifact, "generated": self.generated,
                "partial": self.partial, "runs": self.runs, "setup_runs": self.setup_runs, "cost": self.cost,
                "naive": self.naive, "noise": self.noise, "unmapped_assumptions": self.unmapped_assumptions,
                "renamed_assumptions": self.renamed_assumptions, "spec_only_knobs": self.spec_only_knobs,
                "corrected_defaults": self.corrected_defaults, "unverified_defaults": self.unverified_defaults,
                "trace": self.trace,
                "untestable": [{"knob": k, "value": v} for k, v in self.untestable],
                "closest_overall": self.closest,
                "triaged_failures": self.triaged,
                "setup_check": self.setup_check, "effect_threshold": self.effect_threshold,
                "provenance": self.provenance,
                "claims": [claim(r) for r in self.results]}

    # ------------------------------------------------------------ the five questions
    def card(self, r: ClaimResult) -> dict:
        """The five answers every card gives, as plain data that Markdown and the web page both render.
        Every field has a "not recorded" form, so a report saved before a field existed still builds."""
        return {"paper_claim": self._paper_claim(r), "measured": self._measured(r),
                "experiment": self._experiment(r), "belief": self._belief(r),
                "unknown": self._unknown(r), "cause": self._cause(r), "effect": self._effect(r)}

    def _paper_claim(self, r: ClaimResult) -> dict:
        c = self.paper_claims.get(r.target.claim_id) or {}
        return {"quote": c.get("quote"), "page": c.get("page"), "figure": c.get("figure") or r.target.figure,
                "unit": c.get("unit"), "headline": c.get("headline"), "metric": r.target.metric,
                "paper_value": r.target.paper_value, "recorded": bool(c.get("quote"))}

    def _measured(self, r: ClaimResult) -> dict:
        m = self.measured.get(r.target.claim_id) or {}
        nb = self.noise.get(r.target.metric) or {}
        return {"metric": r.target.metric, "median": m.get("median", self.naive.get(r.target.metric)),
                "repeats": m.get("repeats"), "n": m.get("n", nb.get("n")), "min": m.get("min"), "max": m.get("max"),
                "band": m.get("band", nb.get("band")), "cv": m.get("cv", nb.get("cv")),
                "gap": r.gap_before, "band_rel": r.band, "status": r.status, "setup_check": self.setup_check}

    def _experiment(self, r: ClaimResult) -> dict:
        label = r.attribution.confidence_label if r.attribution else "Reproduced"
        if not r.changes:
            why = {"Reproduced": "none was needed: the naive run is inside the noise band of the paper's value",
                   "Inconclusive": "none could be tested: the noise band is too wide to tell values apart",
                   "Unexplained": f"none: no tested change moved the gap ({r.hypotheses_tested} hypotheses tested)"
                   }.get(label, "none was recorded")
            return {"found": False, "note": why}
        e = self.experiments.get(r.target.claim_id) or {}
        first = r.replay[0] if r.replay else {}
        config = e.get("config") or [{"knob": k, "naive": None, "candidate": v} for k, v in r.changes.items()]
        branches = e.get("branches")
        return {"found": True, "changes": dict(r.changes), "config": config,
                "branches": branches,  # None for a report recorded before branch ids were kept
                "command": first.get("command"), "env": first.get("env"),
                "parent_checkpoint": first.get("parent_checkpoint"),
                "result_checkpoint": first.get("result_checkpoint"),
                "repeats": len(r.replay) or (len(branches) if branches else None),
                "metric": r.target.metric, "gap_after": r.gap_after}

    def _effect(self, r: ClaimResult) -> dict | None:
        """Candidate minus naive on the claim's metric, with its bootstrap interval and run counts.
        A report saved before intervals were kept still gives the difference (it follows from the two
        gaps) and the run counts, with the interval marked as not recorded."""
        if not r.changes or r.gap_after is None:
            return None
        e = self.effects.get(r.target.claim_id)
        if e is None:
            nb = self.noise.get(r.target.metric) or {}
            p = abs(r.target.paper_value)
            naive, diff = self.naive.get(r.target.metric), (r.gap_after - r.gap_before) * p
            e = {"metric": r.target.metric, "naive": naive, "candidate": None if naive is None else naive + diff,
                 "diff": diff, "ci": None, "alpha": None,
                 "n_naive": nb.get("n"), "n_candidate": len(r.replay) or None}
        lo, hi = e["ci"] or (None, None)
        return {**e, "excludes_zero": None if lo is None else (lo > 0 or hi < 0),
                "diff_of_paper": e["diff"] / abs(r.target.paper_value) if r.target.paper_value else None}

    def _belief(self, r: ClaimResult) -> dict:
        """Reversal test, held-out claims and evidence, one pass/fail line each."""
        if not r.changes:
            return {"checks": [], "note": "nothing to verify: no explanation was proposed"}
        checks = []
        for k, v in r.counterfactual.items():
            checks.append({"kind": "reversal", "ok": bool(v["ok"]),
                           "text": f"without `{k}` the gap is {_pct(v['gap_without'])}"
                                   + (" (it comes back)" if v["ok"] else " (it did NOT come back)")})
        if not r.counterfactual:
            checks.append({"kind": "reversal", "ok": None, "text": "no reversal test recorded"})
        for cid, v in r.held_out.items():
            if v.get("tuned_separately"):
                checks.append({"kind": "held_out_separate", "ok": None,
                               "text": f"{cid}: {_pct(v['gap_before'])} to {_pct(v['gap_after'])}"
                                       + (" (worse beyond noise; reported, not a constraint)" if v.get("worse")
                                          else " (not worse beyond noise)")})
                continue
            checks.append({"kind": "held_out", "ok": bool(v["ok"]),
                           "text": f"{cid}: {_pct(v['gap_before'])} to {_pct(v['gap_after'])}"
                                   + (" (not worse beyond noise)" if v["ok"] else " (WORSE beyond noise)")})
        if not r.held_out:
            checks.append({"kind": "held_out", "ok": None, "text": "no held-out claims were checked"})
        for cid, v in (r.relations or {}).items():
            if not v.get("checked"):
                checks.append({"kind": "relation", "ok": None, "text": f"{cid}: {v.get('why', 'not checked')}"})
                continue
            verdict = "holds" if v["holds"] else "REVERSED beyond noise" if v["broken"] else "within noise (not decisive)"
            checks.append({"kind": "relation", "ok": not v["broken"],
                           "text": f"{cid}: {v['from_value']:.4g} -> {v['to_value']:.4g} ({verdict})"})
        for k, p in r.plausibility.items():
            checks.append({"kind": "evidence", "ok": bool(p.supported),
                           "text": f"`{k}={r.changes.get(k)}`: {p.reason}"
                                   + (" (direction only; the value itself is untested)" if p.partial else "")})
        if not r.plausibility:
            checks.append({"kind": "evidence", "ok": None, "text": "no evidence check recorded"})
        eff = self._effect(r)
        if eff is not None and eff["excludes_zero"] is not None:
            checks.append({"kind": "effect", "ok": eff["excludes_zero"],
                           "text": f"candidate minus naive is {eff['diff']:+.4g} with a {1 - eff['alpha']:.0%} "
                                   "bootstrap interval "
                                   + ("that excludes 0" if eff["excludes_zero"] else "that includes 0")})
        return {"checks": checks, "note": None}

    def _unknown(self, r: ClaimResult) -> dict:
        """What the report can't tell: values it couldn't test, flags it couldn't set, leads it dropped."""
        taken = set(r.changes.items())
        leads = [{"knob": x["knob"], "value": x["value"], "units": x.get("units"), "gap": x.get("gap")}
                 for x in r.screen if (x.get("units") or 0) >= self.effect_threshold
                 and (x["knob"], x["value"]) not in taken]
        alts = [{"changes": row["changes"], "runs": row["runs"], "gap": (row.get("gaps") or {}).get(r.target.claim_id),
                 "mean_abs_gap": row.get("mean_abs_gap")}
                for row in self.closest if row["changes"] and row["changes"] != r.changes][:3]
        return {"untestable": [{"knob": k, "value": v} for k, v in self.untestable],
                "unmapped": list(self.unmapped_assumptions), "setup": self.setup_check,
                "leads": leads, "alternatives": alts}

    def _cause(self, r: ClaimResult) -> dict:
        """Confirmed cause, plausible explanation or interacting factors: three different claims to make."""
        label = r.attribution.confidence_label if r.attribution else "Reproduced"
        if not r.changes or label in ("Reproduced", "Unexplained", "Inconclusive"):
            return {"kind": None, "text": None, "confirmed": None}
        confirmed = label in ("Explained", "Paper-artifact inconsistency")
        if len(r.changes) > 1:
            return {"kind": "interacting_factors", "confirmed": confirmed,
                    "text": "Interacting factors: these changes close the gap only together, and "
                            + ("every check passes" if confirmed else "not every check passes")}
        if confirmed:
            return {"kind": "confirmed_cause", "confirmed": True,
                    "text": "Confirmed cause: reverting it brings the gap back, held-out claims hold, "
                            "and the value has evidence"}
        why = ("it closes only part of the gap, or the paper's own value was not tested"
               if label == "Partially explained" else "it fits the number, but nothing says the authors used it")
        return {"kind": "plausible_explanation", "confirmed": False,
                "text": f"Plausible explanation (fits but unsupported): {why}"}

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
            out += self._card_markdown(r)
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
        if self.renamed_assumptions or self.spec_only_knobs or self.corrected_defaults or self.unverified_defaults:
            out += ["", "## Knob names"]
            if self.renamed_assumptions:
                out.append("- Ledger names mapped to spec knobs: " +
                           ", ".join(f"`{a}` → `{k}`" for a, k in self.renamed_assumptions.items()))
            if self.spec_only_knobs:
                out.append("- Screened though no assumption named them (low prior, code-derived values): " +
                           ", ".join(f"`{k}`" for k in self.spec_only_knobs))
            if self.corrected_defaults:
                out.append("- Code defaults read from the code instead of the ledger: " + ", ".join(
                    f"`{c['knob']}` {c['code']} at {c['at']} (ledger said {c['ledger']})" for c in self.corrected_defaults))
            if self.unverified_defaults:
                out.append("- Code defaults the code doesn't confirm, so no paper-artifact inconsistency is claimed "
                           "on them: " + ", ".join(f"`{k}`" for k in self.unverified_defaults))
        if self.trace:
            tr = self.trace
            out += ["", "## Runtime trace (one dry run)",
                    f"{tr.get('processes', 0)} process(es) traced. Each role comes from the sink the knob's value "
                    "reached, not from its name."]
            for k, r in sorted((tr.get("roles") or {}).items()):
                out.append(f"- `{k}`: {r['role']} ({r['sink']}" + (f" at {r['site']}" if r.get("site") else "") + ")")
            for x in tr.get("leads") or []:
                out.append(f"- literal `{x['name']} = {x['literal']}` at {x['file']}:{x['line']} reaches {x['sink']}, "
                           "with no knob behind it: a patch-knob lead")
            if tr.get("ambiguous"):
                out.append(f"- {len(tr['ambiguous'])} sink value(s) shared by several knobs: no role assigned")
        if self.unmapped_assumptions:
            out += ["", "## Not testable with this harness",
                    "Assumptions about knobs the harness spec can't set: " +
                    ", ".join(f"`{k}`" for k in self.unmapped_assumptions)]
        out += self._provenance_markdown()
        return "\n".join(out) + "\n"

    def _card_markdown(self, r: ClaimResult) -> list[str]:
        """One card: the label and cause first, then the five questions, then notes."""
        c = self.card(r)
        label = r.attribution.confidence_label if r.attribution else "Reproduced"
        out = ["", f"## {r.target.claim_id}: {r.target.metric} (paper {r.target.paper_value:g})"]
        if r.status == "reproduced":
            out.append(f"**{label}**: naive gap {_pct(r.gap_before)} is inside the noise band ±{r.band * 100:.1f}%.")
        elif r.status == "inconclusive":
            out.append(f"**Inconclusive** · naive gap {_pct(r.gap_before)} is inside the noise band "
                       f"±{r.band * 100:.1f}%, but the band is too wide to call it a reproduction.")
        else:
            out.append(f"**{label}** · gap {_pct(r.gap_before)} → {_pct(r.gap_after)} · "
                       f"{r.hypotheses_tested} hypotheses tested")
        if c["cause"]["text"]:
            out.append(f"> {c['cause']['text']}")
        # the experiment goes first after the label: it is what a reader can rerun
        out += ["", "### Which experiment changed it?"] + _experiment_lines(c["experiment"], c["effect"])
        out += ["", "### What did the paper report?"] + _paper_lines(c["paper_claim"])
        out += ["", "### What did we measure?"] + _measured_lines(c["measured"])
        out += ["", "### Why do we believe it?"] + _belief_lines(c["belief"])
        out += ["", "### What remains unknown?"] + _unknown_lines(c["unknown"])
        if len(r.equivalent) > 1:  # the target claim can't separate these: report the set, not just the pick
            out += ["", "### Equally good configurations",
                    f"The target claim can't tell these {len(r.equivalent)} apart (likelihood of the paper's number "
                    "within 2 log units, held-out claims no worse). The first is reported above, as the simplest:"]
            out += [f"- `{', '.join(f'{k}={v}' for k, v in sorted(e['config'].items()))}`"
                    + (" (reported)" if i == 0 else "") for i, e in enumerate(r.equivalent)]
        if r.diagnosis:
            out += ["", "### History matching (every measured configuration, all claims together)",
                    f"- {r.diagnosis['text']}"]
            joint = [j for j in r.diagnosis.get("joint") or [] if j["config"]]
            if len(joint) > 1:  # equifinality map: every fit the data can't rule out, grouped by knobs changed
                groups: dict[str, list[str]] = {}
                for j in joint:
                    key = ", ".join(sorted(j["config"])) or "naive"
                    worst = max(j["I"].values())
                    groups.setdefault(key, []).append(
                        ", ".join(f"{k}={v}" for k, v in sorted(j["config"].items())) + f" (max I {worst:g})")
                out.append(f"- Not ruled out (all claims within 3 sigma): {len(joint)} configurations")
                out += [f"  - `{k}`: " + "; ".join(v[:4]) + (f"; +{len(v) - 4} more" if len(v) > 4 else "")
                        for k, v in groups.items()]
                isl = [i for i in r.diagnosis.get("islands") or [] if any(i)]
                if len(isl) > 1:  # separate explanations, not one explanation with neighbours
                    out.append(f"- {len(isl)} separate islands (no single-knob move joins them): " + " | ".join(
                        "; ".join(", ".join(f"{k}={v}" for k, v in sorted(c.items())) or "naive" for c in i[:3])
                        for i in isl[:4]))
            tid = r.target.claim_id
            fits = [x for x in (r.diagnosis.get("per_claim") or {}).get(tid, []) if x["config"]]
            if r.diagnosis.get("kind", "").startswith("out_of_space") and len(fits) > 1:
                # every configuration that matches the target alone: they can't be told apart on it
                out.append(f"- Fit {tid} alone ({len(fits)}; worst claim's implausibility in brackets, lowest is "
                           "the least inconsistent): " + "; ".join(
                               ", ".join(f"{k}={v}" for k, v in sorted(x["config"].items()))
                               + f" ({max(x['I'].values()):g})" for x in sorted(fits, key=lambda x: max(x["I"].values()))[:6]))
            leads = r.diagnosis.get("leads") or []
            if leads:  # where a cause outside the settings could hide; static reading only
                out.append("- Leads outside the settings (static code checks, nothing run; check these first):")
                out += [f"  - {x['family'].replace('_', ' ')}: {x['detail']} (`{x['file']}:{x['line']}`)"
                        for x in leads[:8]]
            sets = r.value_sets and {k: v for k, v in r.value_sets.items() if len(v) > 1}
            if sets:
                out.append("- Equally good values: " + "; ".join(f"`{k}` in {{{', '.join(v)}}}" for k, v in sets.items()))
        if r.notes:
            out += ["", "Notes:"] + [f"- {n}" for n in r.notes]
        return out

    def _provenance_markdown(self) -> list[str]:
        out = ["", "## Provenance"]
        p = self.provenance
        if not p:
            return out + ["Not recorded: this report was written before provenance was kept."]
        g = p.get("gapfinder") or {}
        commit = g.get("commit")
        out.append("- GapFinder commit: " + (f"`{commit}`" + (" (working tree had uncommitted changes)"
                                                              if g.get("dirty") else "")
                                             if commit else "not recorded (no git checkout)"))
        out.append("- Models: " + (", ".join(f"{k} `{v}`" for k, v in p["models"].items())
                                   if p.get("models") else "not recorded"))
        if p.get("prompt_sha256"):
            out.append("- Prompt sha256: " + ", ".join(f"{k} `{v}`" for k, v in p["prompt_sha256"].items()))
        else:
            out.append("- Prompt sha256: not recorded")
        out.append("- Harness spec sha256: " + (f"`{p['harness_spec_sha256']}`" if p.get("harness_spec_sha256")
                                                else "not recorded"))
        c = p.get("cost")
        out.append("- Cost: " + (f"Nemotron billed ${c['nemotron_billed_usd']:.4f}, sandbox reported "
                                 f"${c['sandbox_reported_usd']:.4f} (total ${c['total_usd']:.4f}; {c['scope']})"
                                 if c else "not recorded"))
        return out

    def write(self, out_dir: str | Path) -> tuple[Path, Path]:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        md, js = out_dir / "gap_report.md", out_dir / "gap_report.json"
        md.write_text(self.to_markdown(), encoding="utf-8")
        js.write_text(json.dumps(self.to_dict(), indent=2, default=str), encoding="utf-8")
        return md, js


def upgrade_report(d: dict | None) -> dict | None:
    """A report dict saved before the five-question cards existed, rebuilt with the card fields filled in
    ("not recorded" where the old file never kept the value). Anything that can't be rebuilt is returned
    unchanged, so a malformed or minimal report still reaches the page."""
    claims = (d or {}).get("claims")
    if not claims or all("belief" in c for c in claims):
        return d
    try:
        return GapReport.from_dict(d).to_dict()
    except (KeyError, TypeError, ValueError):
        return d


# ----------------------------------------------- what the search knows, per claim


def _paper_claim(search: GapSearch, t: Target) -> dict | None:
    """The ledger claim a target was made from: its quote and page, for "what did the paper report?"."""
    c = search.claims.get(t.claim_id)
    if c is None:
        return None
    return {"quote": c.quote, "page": c.page, "figure": c.figure_or_table, "unit": c.unit,
            "reported_value": c.reported_value, "headline": c.headline}


def _measured(search: GapSearch, t: Target) -> dict:
    """The naive runs of the claim's metric: the repeats the noise band came from."""
    vals = [b.parsed_metrics[t.metric] for b in search.measure_ok({}) if t.metric in b.parsed_metrics]
    nb = search.bands.get(t.metric)
    return {"metric": t.metric, "repeats": vals, "n": len(vals), "median": search.naive.get(t.metric),
            "min": min(vals) if vals else None, "max": max(vals) if vals else None,
            "band": nb.band if nb else None, "cv": nb.cv if nb else None}


def _effect(search: GapSearch, r: ClaimResult) -> dict | None:
    """How far the explaining configuration moved the metric from the naive run, with its bootstrap
    interval (the same test the confirm round applies) and how many runs each side rests on."""
    cand = search.value(r.changes, r.target.metric) if r.changes else None
    naive = search.naive.get(r.target.metric)
    if cand is None or naive is None:
        return None
    ci = search.effect_ci(r.target, r.changes)
    return {"metric": r.target.metric, "naive": naive, "candidate": cand, "diff": cand - naive,
            "ci": list(ci) if ci else None, "alpha": search.cfg.effect_alpha or 0.05,
            "n_naive": len(search.measure_ok({})), "n_candidate": len(search.measure_ok(r.changes))}


def _experiment(search: GapSearch, r: ClaimResult) -> dict | None:
    """The branch that changed the result: ids, what differs from the naive run, and what it printed."""
    if not r.changes:
        return None
    branches = search.measure_ok(r.changes)
    knobs = search.spec.knobs
    return {"changes": dict(r.changes),
            "config": [{"knob": k, "naive": knobs[k].default if k in knobs else None, "candidate": v}
                       for k, v in r.changes.items()],
            "branches": [{"id": b.id, "run_tag": b.run_tag, "result_checkpoint": b.result_checkpoint,
                          "value": b.parsed_metrics.get(r.target.metric)} for b in branches]}


# ------------------------------------------------------ Markdown for the five answers

NOT_RECORDED = "not recorded"
LEADS_SHOWN = 5


def _g(x: float | None) -> str:
    return NOT_RECORDED if x is None else f"{x:.4g}"


def _knobs(d: dict) -> str:
    return ", ".join(f"`{k}={v}`" for k, v in d.items()) or "naive"


def _experiment_lines(e: dict, eff: dict | None) -> list[str]:
    if not e.get("found"):
        return [f"- {e['note'].capitalize()}."]
    out = []
    ids = e.get("branches")
    if ids:
        out.append("- Branch: " + ", ".join(f"`{b['id']}`" for b in ids) + f" ({len(ids)} run(s) of the same config)")
    else:
        out.append(f"- Branch: id {NOT_RECORDED}" + (f" ({e['repeats']} run(s))" if e.get("repeats") else ""))
    for k in e["config"]:
        naive = NOT_RECORDED if k["naive"] is None else f"`{k['naive']}`"
        out.append(f"- Config: `{k['knob']}` naive {naive}, changed to `{k['candidate']}`")
    if e.get("command"):
        env = " ".join(f"{k}={v}" for k, v in (e.get("env") or {}).items())
        out += ["- Command:", "", f"  Replay: fork checkpoint `{e['parent_checkpoint']}` and run", "  ```",
                f"  {(env + ' ' if env else '')}{e['command']}", "  ```"]
    else:
        out.append(f"- Command: {NOT_RECORDED}")
    vals = [b["value"] for b in ids or [] if b.get("value") is not None]
    out.append(f"- Output: `{e['metric']}` " + (", ".join(f"{v:.4g}" for v in vals) if vals else f"values {NOT_RECORDED}")
               + f"; gap after {_pct(e['gap_after'])}"
               + (f"; result checkpoint `{e['result_checkpoint']}`" if e.get("result_checkpoint") else ""))
    if eff is not None:
        out.append("- Effect: " + _effect_text(eff))
    return out


def _effect_text(eff: dict) -> str:
    """candidate minus naive, its interval and run counts, in one line."""
    cand = _g(eff.get("candidate"))
    ci = eff.get("ci")
    interval = (f", {1 - eff['alpha']:.0%} bootstrap interval [{ci[0]:+.4g}, {ci[1]:+.4g}]"
                if ci else f", bootstrap interval {NOT_RECORDED}")
    runs = (f"{eff['n_candidate'] if eff.get('n_candidate') is not None else NOT_RECORDED} candidate runs vs "
            f"{eff['n_naive'] if eff.get('n_naive') is not None else NOT_RECORDED} naive runs")
    return f"candidate {cand} minus naive {_g(eff.get('naive'))} = {eff['diff']:+.4g}{interval} ({runs})"


def _paper_lines(p: dict) -> list[str]:
    where = ", ".join(x for x in (f"p. {p['page']}" if p.get("page") else None, p.get("figure")) if x)
    value = f"`{p['metric']}` = {p['paper_value']:g}" + (f" {p['unit']}" if p.get("unit") else "")
    if not p.get("recorded"):
        return [f"- Quote {NOT_RECORDED} (the report has no linked ledger claim); the value used was {value}."]
    return [f"> {p['quote']}", "", f"- {where or 'location ' + NOT_RECORDED}; value used: {value}"
            + (" (headline claim)" if p.get("headline") else "")]


def _measured_lines(m: dict) -> list[str]:
    n = m.get("n")
    out = [f"- Naive median {_g(m.get('median'))} over {n if n is not None else NOT_RECORDED} runs; repeats: "
           + (", ".join(f"{v:.4g}" for v in m["repeats"]) if m.get("repeats") else NOT_RECORDED)]
    spread = (f"range {_g(m.get('min'))} to {_g(m.get('max'))}, " if m.get("min") is not None else "")
    cv = f", CV {m['cv'] * 100:.1f}%" if m.get("cv") is not None else ""
    out.append(f"- Spread: {spread}noise band ±{_g(m.get('band'))} (2 x MAD){cv}")
    sc = m.get("setup_check")
    out.append("- Setup check: " + (sc["note"] if sc else "none in this report (the band comes from forks of one setup)"))
    out.append(f"- Discrepancy from the paper: {_pct(m['gap'])} (noise band ±{m['band_rel'] * 100:.1f}% of the paper value)")
    return out


def _belief_lines(b: dict) -> list[str]:
    if not b["checks"]:
        return [f"- {b['note']}"]
    names = {"reversal": "Counterfactual (reversal test)", "held_out": "Held-out claim", "evidence": "Evidence",
             "effect": "Effect vs noise", "held_out_separate": "Held-out claim, tuned separately",
             "relation": "Paper's stated relation"}
    mark = {True: "PASS", False: "FAIL", None: "NOT CHECKED"}
    return [f"- {'NOTE' if x['kind'] == 'held_out_separate' else mark[x['ok']]} · {names[x['kind']]}: {x['text']}"
            for x in b["checks"]]


def _unknown_lines(u: dict) -> list[str]:
    out = ["- Untestable within the budget: " + (", ".join(f"`{x['knob']}={x['value']}`" for x in u["untestable"])
                                                  or "none")]
    out.append("- Not settable with this harness: " + (", ".join(f"`{k}`" for k in u["unmapped"]) or "none"))
    sc = u.get("setup")
    out.append("- Setup reproducibility: " + (sc["note"] if sc else "not checked"))
    leads = sorted(u["leads"], key=lambda x: -(x.get("units") or 0))
    out.append("- Unconfirmed leads (moved the gap in the screen, not part of the explanation): "
               + ("; ".join(f"`{x['knob']}={x['value']}` ({_g(x['units'])} noise units, gap {_pct(x['gap'])})"
                            for x in leads[:LEADS_SHOWN]) or "none")
               + (f" (and {len(leads) - LEADS_SHOWN} more in the JSON)" if len(leads) > LEADS_SHOWN else ""))
    if u["alternatives"]:
        out.append("- Near alternatives (closest across all claims):")
        out += [f"  - {_knobs(a['changes'])}: this claim {_pct(a['gap'])}, mean |gap| "
                f"{a['mean_abs_gap'] * 100:.1f}% ({a['runs']} runs)" for a in u["alternatives"]]
    else:
        out.append("- Near alternatives: none recorded")
    return out
