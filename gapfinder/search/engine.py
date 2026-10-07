"""Search loop: screen -> confirm -> combine -> bisect -> verify, once per divergent claim.

Units. A claim's gap is relative: (measured - paper) / |paper|. Its noise band
is the metric's noise band (2 x MAD over identical forks, with a floor) in the
same relative units. A branch's effect is measured in noise units:
(|naive gap| - |branch gap|) / band. Positive means the branch closes the gap.

Every measurement goes through `measure`, which reuses earlier runs of the
same configuration, counts runs against `max_runs`, and lets the dollar cap
stop the search. Hitting either limit produces a partial report, never a crash.
"""

from __future__ import annotations

import asyncio
import itertools
import statistics
from dataclasses import dataclass, field

from gapfinder.ledger.schemas import Assumption, AssumptionStatus, Attribution, Branch, BranchStatus, ConfidenceLabel
from gapfinder.models import budget
from gapfinder.sandbox.noise import NoiseBand, noise_band
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.search.bisect import minimal_set
from gapfinder.ledger.assumptions import derive_status
from gapfinder.search.verify import Plausibility, gap_returns, held_out_ok, plausible

Changes = dict[str, str]
_LABEL_RANK = {
    ConfidenceLabel.explained.value: 0,
    ConfidenceLabel.inconsistency.value: 0,
    ConfidenceLabel.fits_but_unsupported.value: 1,
    ConfidenceLabel.partially_explained.value: 2,
    ConfidenceLabel.unexplained.value: 3,
}


class RunBudgetExceeded(RuntimeError):
    pass


@dataclass(frozen=True)
class Target:
    """A claim GapFinder can measure: which metric, and the paper's number for it."""

    claim_id: str
    metric: str
    paper_value: float
    held_out: bool = False  # only used to check explanations, never to choose them


@dataclass
class SearchConfig:
    screen_top_k: int = 24  # assumptions screened, by prior
    candidates_per_knob: int = 2
    noise_repeats: int = 5
    confirm_repeats: int = 3
    effect_threshold: float = 1.0  # noise units needed to survive screen/confirm
    noise_floor_frac: float = 0.01  # band never below 1% of the metric (MAD can be 0 for discrete metrics)
    combine_top: int = 4
    confirm_prior_min: float = 0.8  # hypotheses this likely (or paper-vs-code mismatches) always get confirmed
    combine_prior_top: int = 2  # also pair the ledger's highest-prior knobs (interactions score ~0 alone)
    partial_frac: float = 0.5  # "partially explained" needs at least this share of the gap closed
    verify_candidates: int = 3  # best configurations taken through verification
    max_runs: int | None = None  # branch-run budget; None = unlimited
    verify: bool = True  # ablation: False labels any gap-closing config "Explained" without checks


@dataclass(frozen=True)
class Hypothesis:
    knob: str
    value: str
    assumption_id: str | None

    @property
    def changes(self) -> Changes:
        return {self.knob: self.value}


@dataclass
class ClaimResult:
    target: Target
    status: str  # "reproduced" | "searched" | "partial"
    gap_before: float
    band: float
    attribution: Attribution | None = None
    changes: Changes = field(default_factory=dict)
    gap_after: float | None = None
    held_out: dict[str, dict] = field(default_factory=dict)
    counterfactual: dict[str, dict] = field(default_factory=dict)
    plausibility: dict[str, Plausibility] = field(default_factory=dict)
    screen: list[dict] = field(default_factory=list)
    hypotheses_tested: int = 0
    replay: list[dict] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def _norm_knob(k: str) -> str:
    return k.strip().lstrip("-").replace("-", "_").lower()


class GapSearch:
    def __init__(self, orch: Orchestrator, targets: list[Target], assumptions: list[Assumption],
                 cfg: SearchConfig | None = None, evidence=None):
        """`evidence`: optional EvidenceSearch (web) consulted when paper and code don't back a value."""
        self.orch, self.targets, self.cfg = orch, targets, cfg or SearchConfig()
        self.evidence = evidence
        self.spec = orch.spec
        spec_knobs = {_norm_knob(k): k for k in self.spec.knobs}
        # assumption -> spec knob; assumptions about knobs the harness can't set are skipped (and reported)
        self.assumptions: dict[str, Assumption] = {}
        self.unmapped: list[str] = []
        for a in sorted(assumptions, key=lambda a: -a.prior_score):
            k = spec_knobs.get(_norm_knob(a.knob))
            if k is None:
                self.unmapped.append(a.knob)
            elif k not in self.assumptions:
                self.assumptions[k] = a
        self._runs: dict[frozenset, list[Branch]] = {}
        self.untestable: list[tuple[str, str]] = []  # (knob, value) above the spec's cost limit
        self.runs_used = 0
        self.bands: dict[str, NoiseBand] = {}
        self.naive: dict[str, float] = {}

    # ------------------------------------------------------------ measuring
    async def measure(self, changes: Changes, n: int = 1, label: str = "") -> list[Branch]:
        key = frozenset(changes.items())
        have = self._runs.setdefault(key, [])
        ok = [b for b in have if b.status == BranchStatus.succeeded]
        need = n - len(ok)
        if need > 0:
            if self.cfg.max_runs is not None and self.runs_used + need > self.cfg.max_runs:
                raise RunBudgetExceeded(f"run budget of {self.cfg.max_runs} reached")
            self.runs_used += need
            have.extend(await self.orch.fanout([changes] * need, [label] * need))
            ok = [b for b in have if b.status == BranchStatus.succeeded]
        return ok

    def value(self, changes: Changes, metric: str) -> float | None:
        vals = [b.parsed_metrics[metric] for b in self._runs.get(frozenset(changes.items()), [])
                if b.status == BranchStatus.succeeded and metric in b.parsed_metrics]
        return statistics.median(vals) if vals else None

    def gap(self, t: Target, changes: Changes) -> float | None:
        v = self.naive.get(t.metric) if not changes else self.value(changes, t.metric)
        return None if v is None else (v - t.paper_value) / abs(t.paper_value)

    def band(self, t: Target) -> float:
        return self.bands[t.metric].band / abs(t.paper_value)

    def band_at(self, t: Target, changes: Changes) -> float:
        """Noise band at a configuration, from its own repeats when it has 3+; else the naive band.
        Noise isn't constant across configs (unstable training at the default can be 50x noisier
        than a normalised run), so 'closes the gap' must use the candidate's own spread."""
        vals = [b.parsed_metrics[t.metric] for b in self._runs.get(frozenset(changes.items()), [])
                if b.status == BranchStatus.succeeded and t.metric in b.parsed_metrics]
        if not changes or len(vals) < 3:
            return self.band(t)
        return noise_band(t.metric, vals, floor_frac=self.cfg.noise_floor_frac).band / abs(t.paper_value)

    def closes(self, t: Target, changes: Changes) -> bool:
        g = self.gap(t, changes)
        return g is not None and abs(g) <= self.band_at(t, changes)

    def units(self, t: Target, changes: Changes) -> float:
        g, g0 = self.gap(t, changes), self.gap(t, {})
        if g is None or g0 is None:
            return float("-inf")
        return (abs(g0) - abs(g)) / self.band(t)

    # -------------------------------------------------------------- driver
    async def calibrate(self) -> None:
        runs = await self.measure({}, self.cfg.noise_repeats, "noise")
        if len(runs) < 3:
            raise RuntimeError(f"naive configuration failed: only {len(runs)} successful runs")
        for t in self.targets:
            vals = [b.parsed_metrics[t.metric] for b in runs if t.metric in b.parsed_metrics]
            nb = noise_band(t.metric, vals, floor_frac=self.cfg.noise_floor_frac)
            self.bands[t.metric], self.naive[t.metric] = nb, nb.median
            self.orch.events.emit("noise_band", **nb.to_dict())

    async def run(self) -> list[ClaimResult]:
        await self.calibrate()
        results = []
        for t in self.targets:
            if not t.held_out:
                results.append(await self.explain(t))
        return results

    def hypotheses(self) -> list[Hypothesis]:
        """One hypothesis per (knob, candidate value). A knob whose value the paper states and the
        code already uses can't cause the gap (the naive run already matches the paper there)."""
        out = []
        open_knobs = []
        for k, a in self.assumptions.items():
            # "matches" must be judged against what the naive run used (the spec default), not the
            # artifact's own default: a scaled reproduction differs from the paper exactly there
            if derive_status(a.paper_value, self.spec.knobs[k].default, a.status) == AssumptionStatus.stated_matches.value:
                continue
            open_knobs.append((k, a))
        for knob, a in open_knobs[: self.cfg.screen_top_k]:
            spec_knob = self.spec.knobs[knob]
            default = spec_knob.default
            values = [str(v) for v in a.candidate_values if str(v) != default] or [
                v for v in spec_knob.candidates if v != default]
            stated = _stated_value(a.paper_value)
            if stated is not None and stated != default and stated not in values:
                values.insert(0, stated)  # the paper's own value is always a candidate
            affordable = [v for v in values if spec_knob.affordable(v)]
            for v in values:
                if not spec_knob.affordable(v) and (knob, v) not in self.untestable:
                    self.untestable.append((knob, v))
            for v in affordable[: self.cfg.candidates_per_knob]:
                out.append(Hypothesis(knob, v, a.id))
        return out

    async def explain(self, t: Target) -> ClaimResult:
        g0, band = self.gap(t, {}), self.band(t)
        res = ClaimResult(target=t, status="searched", gap_before=g0, band=band)
        if abs(g0) <= band:
            res.status = "reproduced"
            res.notes.append("naive run is within the noise band of the paper's value")
            return res
        tried: set[frozenset] = set()
        try:
            await self._search(t, res, tried)
        except (RunBudgetExceeded, budget.BudgetExceeded) as exc:
            res.status = "partial"
            res.notes.append(f"stopped early: {exc}")
            self._label_partial(t, res)
        res.hypotheses_tested = len(tried)
        if res.attribution is not None:
            res.attribution.hypotheses_tested = len(tried)
        self.orch.events.emit("attribution", claim=t.claim_id, status=res.status,
                              label=res.attribution.confidence_label if res.attribution else None,
                              changes=res.changes, gap_before=g0, gap_after=res.gap_after)
        return res

    async def _search(self, t: Target, res: ClaimResult, tried: set[frozenset]) -> None:
        thr = self.cfg.effect_threshold
        hyps = [h for h in self.hypotheses() if self._renderable(h, res)]

        # 1. screen: one knob per branch, one run each
        await asyncio.gather(*(self.measure(h.changes, 1, f"screen {h.knob}={h.value}") for h in hyps))
        tried.update(frozenset(h.changes.items()) for h in hyps)
        score = {h: self.units(t, h.changes) for h in hyps}
        res.screen = [{"knob": h.knob, "value": h.value, "assumption": h.assumption_id,
                       "units": round(score[h], 2), "gap": self.gap(t, h.changes)} for h in hyps]
        # strong leads from the ledger skip pruning: one noisy screen run shouldn't discard them
        survivors = [h for h in hyps if score[h] >= thr or self._strong_lead(h)]
        for h in hyps:
            self.orch.events.emit("survivor" if h in survivors else "pruned", claim=t.claim_id,
                                  knob=h.knob, value=h.value, units=round(score[h], 2), round="screen")
        self.orch.events.emit("round", name="screen", claim=t.claim_id, tested=len(hyps), survivors=len(survivors))

        # 2. confirm: survivors get repeats; effects that fade are pruned
        reps = self.confirm_repeats(t)
        await asyncio.gather(*(self.measure(h.changes, reps, "confirm") for h in survivors))
        confirmed = [h for h in survivors if self.units(t, h.changes) >= thr]
        self.orch.events.emit("round", name="confirm", claim=t.claim_id, confirmed=len(confirmed))

        # 3. combine: all confirmed together, plus pairs among the top screened knobs
        #    (top by score even below threshold: two knobs that only matter together score ~0 alone)
        best_value: dict[str, Hypothesis] = {}
        for h in sorted(hyps, key=lambda h: -score[h]):
            best_value.setdefault(h.knob, h)
        prior = {k: self.assumptions[k].prior_score for k in best_value}
        top = sorted(best_value.values(), key=lambda h: (-score[h], -prior[h.knob], h.knob))[: self.cfg.combine_top]
        # knobs that matter only together score ~0 alone, so also pair the ledger's highest-prior knobs
        for h in sorted(best_value.values(), key=lambda h: (-prior[h.knob], h.knob))[: self.cfg.combine_prior_top]:
            if h not in top:
                top.append(h)
        combos: list[Changes] = []
        conf_knobs = {}
        for h in sorted(confirmed, key=lambda h: -self.units(t, h.changes)):
            conf_knobs.setdefault(h.knob, h.value)
        if len(conf_knobs) >= 2:
            combos.append(dict(conf_knobs))
        for a, b in itertools.combinations(top, 2):
            c = {a.knob: a.value, b.knob: b.value}
            if c not in combos:
                combos.append(c)
        await asyncio.gather(*(self.measure(c, 1, "combine") for c in combos))
        tried.update(frozenset(c.items()) for c in combos)
        good_combos = [c for c in combos if self.units(t, c) >= thr]
        await asyncio.gather(*(self.measure(c, reps, "confirm-combo") for c in good_combos))
        self.orch.events.emit("round", name="combine", claim=t.claim_id, tried=len(combos), kept=len(good_combos))

        # candidates: confirmed singles and combos, closest to the paper first
        candidates = [h.changes for h in confirmed] + [c for c in good_combos if self.units(t, c) >= thr]
        # closes fully > closes at least half > the rest; evidence-backed first within each tier
        def tier(c: Changes) -> int:
            g, g0 = abs(self.gap(t, c)), abs(res.gap_before)
            return 0 if self.closes(t, c) else 1 if g0 - g >= self.cfg.partial_frac * g0 else 2
        candidates.sort(key=lambda c: (tier(c), not self._supported(c), abs(self.gap(t, c)), len(c),
                                       sorted(c.items())))
        best: ClaimResult | None = None
        for c in candidates[: self.cfg.verify_candidates]:
            trial = await self._verify(t, c, res)
            if best is None or _rank(trial) < _rank(best):
                best = trial
            if _rank(best) == 0:
                break
        if best is None:
            res.gap_after = res.gap_before
            res.attribution = self._attribution(t, {}, res.gap_before, ConfidenceLabel.unexplained, [])
            res.notes.append(f"no hypothesis moved the gap by more than {thr:g} noise units")
            return
        for f in ("attribution", "changes", "gap_after", "held_out", "counterfactual", "plausibility", "replay"):
            setattr(res, f, getattr(best, f))
        res.notes.extend(best.notes)
        if res.attribution.confidence_label == ConfidenceLabel.unexplained.value and res.changes:
            # nothing explains the gap: don't present the best failed attempt as an explanation
            res.notes.append(f"closest configuration tried: {res.changes} (gap {res.gap_after:+.1%}); "
                             "it did not pass verification")
            res.changes, res.gap_after = {}, res.gap_before
            res.plausibility, res.counterfactual, res.held_out, res.replay = {}, {}, {}, []
            res.attribution.assumption_set, res.attribution.gap_after = [], res.gap_before
            res.attribution.checkpoint_ids, res.attribution.counterfactual_ok = [], None

    async def _verify(self, t: Target, changes: Changes, parent: ClaimResult) -> ClaimResult:
        r = ClaimResult(target=t, status="searched", gap_before=parent.gap_before, band=parent.band)
        band, thr = parent.band, self.cfg.effect_threshold
        closes = lambda c: self.closes(t, c)  # noqa: E731

        # 4. bisect to the minimal set that still closes the gap
        if len(changes) > 1 and closes(changes):
            async def still_closes(sub: Changes) -> bool:
                await self.measure(sub, 1, "bisect")
                return closes(sub)
            changes = await minimal_set(changes, still_closes)
            await self.measure(changes, self.confirm_repeats(t), "confirm-minimal")
        r.changes, r.gap_after = dict(changes), self.gap(t, changes)

        # The no-verification ablation skips 5a-5c and accepts whatever closes the gap.
        # 5a. counterfactual: revert each knob; the gap must come back
        for knob in changes if self.cfg.verify else ():
            without = {k: v for k, v in changes.items() if k != knob}
            if without:
                await self.measure(without, 1, "counterfactual")
            g_without = self.gap(t, without)
            r.counterfactual[knob] = {"gap_without": g_without, "ok": gap_returns(r.gap_after, g_without, band)}
        # 5b. held-out: every other claim must not get worse beyond its noise
        for other in self.targets if self.cfg.verify else ():
            if other.claim_id == t.claim_id:
                continue
            before, after = self.gap(other, {}), self.gap(other, changes)
            r.held_out[other.claim_id] = {"gap_before": before, "gap_after": after,
                                          "ok": after is not None and held_out_ok(before, after, self.band(other))}
        # 5c. plausibility: the value needs evidence, not just a good fit
        for knob, value in changes.items() if self.cfg.verify else ():
            r.plausibility[knob] = plausible(self.assumptions.get(knob), value)
            a = self.assumptions.get(knob)
            if not r.plausibility[knob].supported and a is not None and self.evidence is not None:
                ev = await self.evidence.find(knob, value)
                if ev is not None:
                    self.assumptions[knob] = a = a.model_copy(update={"evidence": [*a.evidence, ev]})
                    r.plausibility[knob] = plausible(a, value)
                    self.orch.events.emit("note", msg=f"web evidence for {knob}={value}: {ev.ref}")

        cf_ok = all(v["ok"] for v in r.counterfactual.values())
        ho_ok = all(v["ok"] for v in r.held_out.values())
        plaus_ok = all(p.supported for p in r.plausibility.values())
        reduced = (abs(r.gap_before) - abs(r.gap_after) >= self.cfg.partial_frac * abs(r.gap_before)
                   and self.units(t, changes) >= thr)
        if closes(changes) and cf_ok and ho_ok:
            if not plaus_ok:
                label = ConfidenceLabel.fits_but_unsupported
            elif any(self.assumptions[k].status == AssumptionStatus.stated_code_differs.value
                     for k in changes if k in self.assumptions):
                label = ConfidenceLabel.inconsistency
            else:
                label = ConfidenceLabel.explained
        elif reduced and ho_ok and not plaus_ok:
            label = ConfidenceLabel.fits_but_unsupported
        elif reduced and ho_ok:
            label = ConfidenceLabel.partially_explained
            if closes(changes) and not cf_ok:
                r.notes.append(f"{sorted(changes)}: closes the gap but reverting a knob does not reopen it")
        else:
            label = ConfidenceLabel.unexplained
            if not ho_ok:
                r.notes.append(f"{changes} closes this claim but makes held-out claims worse; rejected")
        branches = self._runs.get(frozenset(changes.items()), [])
        env = self.spec.render(self.spec.run, changes)[1]  # env-var knobs aren't in the command line
        r.replay = [{"parent_checkpoint": b.parent_checkpoint, "result_checkpoint": b.result_checkpoint,
                     "command": b.command, "env": {**env, "RUN_TAG": b.run_tag}, "run_tag": b.run_tag}
                    for b in branches if b.status == BranchStatus.succeeded]
        r.attribution = self._attribution(t, changes, r.gap_after, label,
                                          [x["result_checkpoint"] for x in r.replay if x["result_checkpoint"]],
                                          held=r.held_out, cf_ok=cf_ok)
        self.orch.events.emit("verified", claim=t.claim_id, changes=changes, label=label.value,
                              counterfactual_ok=cf_ok, held_out_ok=ho_ok, plausible=plaus_ok)
        return r

    # -------------------------------------------------------------- helpers
    def confirm_repeats(self, t: Target) -> int:
        """Noisy metrics (run-to-run CV above 5%) get two extra repeats."""
        return self.cfg.confirm_repeats + (2 if self.bands[t.metric].cv > 0.05 else 0)

    def _strong_lead(self, h: Hypothesis) -> bool:
        a = self.assumptions.get(h.knob)
        return a is not None and (a.prior_score >= self.cfg.confirm_prior_min
                                  or a.status == AssumptionStatus.stated_code_differs.value)

    def _supported(self, changes: Changes) -> bool:
        return all(plausible(self.assumptions.get(k), v).supported for k, v in changes.items())

    def _attribution(self, t: Target, changes: Changes, gap_after: float, label: ConfidenceLabel,
                     checkpoints: list[str], held: dict | None = None, cf_ok: bool | None = None) -> Attribution:
        aset = [f"{self.assumptions[k].id if k in self.assumptions else '?'}:{k}={v}" for k, v in changes.items()]
        held_txt = None
        if held:
            held_txt = "; ".join(f"{cid}: {'ok' if v['ok'] else 'WORSE'}" for cid, v in held.items())
        return Attribution(claim_id=t.claim_id, assumption_set=aset, gap_before=self.gap(t, {}),
                           gap_after=gap_after, noise_band=self.band(t), held_out_result=held_txt,
                           counterfactual_ok=cf_ok, checkpoint_ids=checkpoints, confidence_label=label)

    def _label_partial(self, t: Target, res: ClaimResult) -> None:
        """Budget ran out: report the best configuration measured so far, unverified."""
        measured = [dict(k) for k in self._runs if k and self.value(dict(k), t.metric) is not None]
        if not measured:
            res.attribution = self._attribution(t, {}, res.gap_before, ConfidenceLabel.unexplained, [])
            return
        best = min(measured, key=lambda c: abs(self.gap(t, c)))
        g = self.gap(t, best)
        reduced = abs(res.gap_before) - abs(g) >= self.cfg.partial_frac * abs(res.gap_before)
        label = ConfidenceLabel.partially_explained if reduced else ConfidenceLabel.unexplained
        res.changes, res.gap_after = best, g
        res.attribution = self._attribution(t, best, g, label, [])
        res.notes.append("best configuration so far, NOT verified (no counterfactual or held-out check)")

    def _renderable(self, h: Hypothesis, res: ClaimResult) -> bool:
        try:
            self.spec.render(self.spec.run, h.changes)
            return True
        except ValueError as exc:
            res.notes.append(f"skipped {h.knob}={h.value!r}: {exc}")
            return False


def _stated_value(paper_value: str) -> str | None:
    """A plain stated value ('2000', '100000000', 'true'), or None for prose or 'unstated'."""
    v = paper_value.strip().strip("\"'")
    if v.lower().startswith("unstated") or " " in v or not v:
        return None
    return v


def _rank(r: ClaimResult) -> int:
    return _LABEL_RANK[r.attribution.confidence_label] if r.attribution else 9
