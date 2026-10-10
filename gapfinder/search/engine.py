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
import random
import statistics
from dataclasses import dataclass, field

from gapfinder.ledger.schemas import Assumption, AssumptionStatus, Attribution, Branch, BranchStatus, ConfidenceLabel
from gapfinder.models import budget
from gapfinder.sandbox.noise import NoiseBand, bootstrap_diff_ci, noise_band
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
    figure: str | None = None  # e.g. "Figure 6": which experiment's stated settings apply


@dataclass
class SearchConfig:
    screen_top_k: int = 24  # assumptions screened, by prior
    candidates_per_knob: int = 2
    noise_repeats: int = 5
    # >1: that many of the naive noise runs each get a fresh build/load. A setup that isn't
    # reproducible (e.g. a database load whose layout depends on timing) adds its own variance,
    # which runs forked from one shared setup never see.
    noise_setups: int = 1
    screen_repeats: int = 1  # >1 guards against batch effects (one run per config in a crowded batch)
    confirm_repeats: int = 3
    effect_threshold: float = 1.0  # noise units needed to survive screen/confirm
    noise_floor_frac: float = 0.01  # band never below 1% of the metric (MAD can be 0 for discrete metrics)
    combine_top: int = 4
    confirm_prior_min: float = 0.8  # hypotheses this likely (or paper-vs-code mismatches) always get confirmed
    combine_prior_top: int = 2  # also pair the ledger's highest-prior knobs (interactions score ~0 alone)
    partial_frac: float = 0.5  # "partially explained" needs at least this share of the gap closed
    verify_candidates: int = 3  # best configurations taken through verification
    max_runs: int | None = None  # branch-run budget; None = unlimited
    # "Reproduced" only when the noise band is at most this fraction of the paper value; a naive run
    # inside a wider band is "Inconclusive": the measurements can't tell the paper's value from
    # values this far away
    reproduce_tol: float = 0.10
    # a confirmed effect must also have a bootstrap interval on (candidate - naive) that excludes 0;
    # None turns the test off and leaves only the noise-band rule
    effect_alpha: float | None = 0.05
    verify: bool = True  # ablation: False labels any gap-closing config "Explained" without checks
    # ablation: False skips the plausibility/evidence step (no ledger-evidence match, no web call), so a
    # closing value is at most "Fits but unsupported"; only the experiments carry the verdict
    evidence_gate: bool = True
    # "ledger": the ledger's priors order the hypotheses and strong leads skip pruning.
    # "random": the random-search arm. Same hypothesis space and budget, but the order comes from
    # random.Random(seed), `_strong_lead()` is always False, and the combine round ranks knobs by a
    # seeded random number instead of the ledger prior.
    rank: str = "ledger"
    seed: int = 0

    def __post_init__(self):
        if self.rank not in ("ledger", "random"):
            raise ValueError(f"rank must be 'ledger' or 'random', not {self.rank!r}")


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
                 cfg: SearchConfig | None = None, evidence=None, claims: list | None = None, router=None):
        """`evidence`: optional EvidenceSearch (web) consulted when paper and code don't back a value.
        `claims`: the ledger's claims, so a paper value can be tied to the experiment it belongs to."""
        self.orch, self.targets, self.cfg = orch, targets, cfg or SearchConfig()
        self.evidence = evidence
        self.router = router  # optional: Nemotron 3 Super triages failed hypotheses
        self.setup_check: dict | None = None  # filled when noise_setups > 1
        self.triaged: list[dict] = []
        self.claim_figure = {c.id: c.figure_or_table for c in (claims or [])}
        self.target_figures = {t.figure for t in targets if t.figure}
        self.spec = orch.spec
        spec_knobs = {_norm_knob(k): k for k in self.spec.knobs}
        # assumption -> spec knob; assumptions about knobs the harness can't set are skipped (and reported)
        self.assumptions: dict[str, Assumption] = {}
        self.all_for: dict[str, list[Assumption]] = {}  # every ledger entry per knob (papers state some twice)
        self.unmapped: list[str] = []
        for a in sorted(assumptions, key=lambda a: -a.prior_score):
            k = spec_knobs.get(_norm_knob(a.knob))
            if k is None:
                self.unmapped.append(a.knob)
                continue
            self.all_for.setdefault(k, []).append(a)
        for k, entries in self.all_for.items():
            # one representative (highest prior) carrying the union of evidence and candidates
            head = entries[0]
            evidence = [e for a in entries for e in a.evidence]
            cands = list(dict.fromkeys(str(v) for a in entries for v in a.candidate_values))
            self.assumptions[k] = head.model_copy(update={"evidence": evidence, "candidate_values": cands})
        self._runs: dict[frozenset, list[Branch]] = {}
        self.untestable: list[tuple[str, str]] = []  # (knob, value) above the spec's cost limit
        self.runs_used = 0
        self.bands: dict[str, NoiseBand] = {}
        self.naive: dict[str, float] = {}

    # ------------------------------------------------------------ measuring
    async def measure(self, changes: Changes, n: int = 1, label: str = "", fresh: bool = False) -> list[Branch]:
        key = frozenset(changes.items())
        have = self._runs.setdefault(key, [])
        ok = [b for b in have if b.status == BranchStatus.succeeded]
        need, fails = n - len(ok), len(have) - len(ok)
        if need > 0 and fails:
            # a configuration that keeps failing (e.g. a value the program rejects) is not re-run on
            # every call: one retry for a transient failure, none once it failed twice and never ran
            need = 0 if not ok and fails >= 2 else max(0, min(need, n + 1 - len(have)))
        if need > 0:
            if self.cfg.max_runs is not None and self.runs_used + need > self.cfg.max_runs:
                raise RunBudgetExceeded(f"run budget of {self.cfg.max_runs} reached "
                                        f"(wanted {need} more run(s) of {dict(changes) or 'naive'} for {label!r})")
            self.runs_used += need
            have.extend(await self.orch.fanout([changes] * need, [label] * need, fresh_setup=fresh))
            ok = [b for b in have if b.status == BranchStatus.succeeded]
        return ok

    def measure_ok(self, changes: Changes) -> list[Branch]:
        """Successful runs already made at a configuration (no new runs)."""
        return [b for b in self._runs.get(frozenset(changes.items()), []) if b.status == BranchStatus.succeeded]

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
        own = noise_band(t.metric, vals, floor_frac=self.cfg.noise_floor_frac).band / abs(t.paper_value)
        if self.setup_check and self.setup_check["reproducible"] is False:
            return max(own, self.band(t))  # its repeats share one setup; setups themselves vary this much
        return own

    def effect_ci(self, t: Target, changes: Changes) -> tuple[float, float] | None:
        """Bootstrap interval for (candidate - naive) on the target metric, from runs already made."""
        base = [b.parsed_metrics[t.metric] for b in self.measure_ok({}) if t.metric in b.parsed_metrics]
        cand = [b.parsed_metrics[t.metric] for b in self.measure_ok(changes) if t.metric in b.parsed_metrics]
        if len(base) < 2 or len(cand) < 2:
            return None
        return bootstrap_diff_ci(base, cand, alpha=self.cfg.effect_alpha or 0.05)

    def _significant(self, t: Target, changes: Changes) -> bool:
        if self.cfg.effect_alpha is None:
            return True
        ci = self.effect_ci(t, changes)
        ok = ci is not None and (ci[0] > 0 or ci[1] < 0)
        if not ok:
            self.orch.events.emit("note", msg=f"{t.claim_id}: {dict(changes)} not significant "
                                              f"(bootstrap interval {ci and tuple(round(x, 4) for x in ci)} includes 0)")
        return ok

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
        n = self.cfg.noise_repeats
        k = max(1, min(self.cfg.noise_setups, n))
        runs = await self.measure({}, n - k + 1, "noise")
        if k > 1:  # the rest each on a fresh setup: does the build/load itself reproduce?
            runs = await self.measure({}, n, "noise (fresh setup)", fresh=True)
            self._check_setups(runs, k)
        if len(runs) < 3:
            raise RuntimeError(f"naive configuration failed: only {len(runs)} successful runs")
        for t in self.targets:
            vals = [b.parsed_metrics[t.metric] for b in runs if t.metric in b.parsed_metrics]
            nb = noise_band(t.metric, vals, floor_frac=self.cfg.noise_floor_frac)
            self.bands[t.metric], self.naive[t.metric] = nb, nb.median
            self.orch.events.emit("noise_band", **nb.to_dict())

    def _check_setups(self, runs: list[Branch], k: int) -> None:
        parents = {b.parent_checkpoint for b in runs}
        if not getattr(self.orch.backend, "content_addressed", False):
            ok, msg = None, (f"{k} independent setups measured; reproducibility not checked "
                             "(this backend's checkpoint IDs don't name their content)")
        elif len(parents) == 1:
            ok, msg = True, f"setup is reproducible: {k} independent setups gave one identical checkpoint"
        else:
            ok, msg = False, (f"setup is NOT reproducible: {k} identical setups gave {len(parents)} different "
                              "checkpoints, so the noise band includes setup-to-setup variation")
        self.setup_check = {"setups": k, "distinct_checkpoints": len(parents), "reproducible": ok, "note": msg}
        self.orch.events.emit("note", msg=msg)

    async def run(self) -> list[ClaimResult]:
        rank = self.cfg.rank if self.cfg.rank == "ledger" else f"RANDOM (seed {self.cfg.seed})"
        self.orch.events.emit("note", msg=f"search config: evidence gate {'on' if self.cfg.evidence_gate else 'OFF'}, "
                                          f"rank {rank}",
                              evidence_gate=self.cfg.evidence_gate, verify=self.cfg.verify,
                              rank=self.cfg.rank, seed=self.cfg.seed)
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
            stated = self._stated_values(k)
            default = self.spec.knobs[k].default
            # "matches" is judged against what the naive run used (the spec default), not the artifact's
            # default, and only on values the paper states FOR THESE claims' experiment(s). The knob is
            # confirmed only if every such value matches the naive run.
            if stated and all(derive_status(v, default, "stated_code_differs") == AssumptionStatus.stated_matches.value
                              for v in stated):
                continue
            open_knobs.append((k, a, stated))
        rng = random.Random(self.cfg.seed)
        if self.cfg.rank == "random":
            rng.shuffle(open_knobs)  # the top-k cut must not keep the ledger's favourites
        for knob, a, stated in open_knobs[: self.cfg.screen_top_k]:
            spec_knob = self.spec.knobs[knob]
            default = spec_knob.default
            values = [str(v) for v in a.candidate_values if str(v) != default] or [
                v for v in spec_knob.candidates if v != default]
            for v in reversed([_stated_value(s) for s in stated]):
                if v is not None and v != default:  # the paper's own values come first
                    if v in values:
                        values.remove(v)
                    values.insert(0, v)
            affordable = [v for v in values if spec_knob.affordable(v)]
            for v in values:
                if not spec_knob.affordable(v) and (knob, v) not in self.untestable:
                    self.untestable.append((knob, v))
            for v in affordable[: self.cfg.candidates_per_knob]:
                out.append(Hypothesis(knob, v, a.id))
        if self.cfg.rank == "random":
            rng.shuffle(out)
        return out

    async def explain(self, t: Target) -> ClaimResult:
        g0, band = self.gap(t, {}), self.band(t)
        res = ClaimResult(target=t, status="searched", gap_before=g0, band=band)
        if abs(g0) <= band:
            if band <= self.cfg.reproduce_tol:
                res.status = "reproduced"
                res.notes.append("naive run is within the noise band of the paper's value")
            else:
                res.status = "inconclusive"
                res.attribution = self._attribution(t, {}, g0, ConfidenceLabel.inconclusive, [])
                res.gap_after = g0
                res.notes.append(f"naive gap {g0:+.1%} is inside the noise band (±{band:.1%}), but the band is "
                                 f"wider than ±{self.cfg.reproduce_tol:.0%}: these measurements can't tell the "
                                 "paper's value apart from clearly different ones, so neither a reproduction "
                                 "nor an explanation can be claimed")
            self.orch.events.emit("attribution", claim=t.claim_id, status=res.status,
                                  label=res.attribution.confidence_label if res.attribution else None,
                                  changes={}, gap_before=g0, gap_after=g0)
            return res
        tried: set[frozenset] = set()
        try:
            await self._search(t, res, tried)
        except (RunBudgetExceeded, budget.BudgetExceeded) as exc:
            res.status = "partial"
            res.notes.append(f"stopped early: {exc}")
            await self._label_partial(t, res)
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
        await _all(*(self.measure(h.changes, self.cfg.screen_repeats, f"screen {h.knob}={h.value}")
                     for h in hyps))
        tried.update(frozenset(h.changes.items()) for h in hyps)
        hyps += await self._triage_failures(hyps, tried)
        score = {h: self.units(t, h.changes) for h in hyps}
        res.screen = [{"knob": h.knob, "value": h.value, "assumption": h.assumption_id,
                       "units": round(score[h], 2), "gap": self.gap(t, h.changes)} for h in hyps]
        # strong leads from the ledger skip pruning: one noisy screen run shouldn't discard them
        survivors = [h for h in hyps if score[h] >= thr or (self._strong_lead(h) and score[h] > float("-inf"))]
        for h in hyps:
            self.orch.events.emit("survivor" if h in survivors else "pruned", claim=t.claim_id,
                                  knob=h.knob, value=h.value, units=round(score[h], 2), round="screen")
        self.orch.events.emit("round", name="screen", claim=t.claim_id, tested=len(hyps), survivors=len(survivors))

        # 2. confirm: survivors get repeats; effects that fade are pruned
        reps = self.confirm_repeats(t)
        await _all(*(self.measure(h.changes, reps, "confirm") for h in survivors))
        confirmed = [h for h in survivors if self.units(t, h.changes) >= thr and self._significant(t, h.changes)]
        self.orch.events.emit("round", name="confirm", claim=t.claim_id, confirmed=len(confirmed))

        # 3. combine: all confirmed together, plus pairs among the top screened knobs
        #    (top by score even below threshold: two knobs that only matter together score ~0 alone)
        best_value: dict[str, Hypothesis] = {}
        for h in sorted(hyps, key=lambda h: -score[h]):
            best_value.setdefault(h.knob, h)
        prior = {k: self._prior(k) for k in best_value}
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
        await _all(*(self.measure(c, 1, "combine") for c in combos))
        tried.update(frozenset(c.items()) for c in combos)
        good_combos = [c for c in combos if self.units(t, c) >= thr]
        await _all(*(self.measure(c, reps, "confirm-combo") for c in good_combos))
        self.orch.events.emit("round", name="combine", claim=t.claim_id, tried=len(combos), kept=len(good_combos))

        # candidates: confirmed singles and combos, closest to the paper first
        candidates = [h.changes for h in confirmed] + [c for c in good_combos if self.units(t, c) >= thr
                                                         and self._significant(t, c)]
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
            if not self.cfg.evidence_gate:
                r.plausibility[knob] = Plausibility(False, "evidence gate off: no evidence was looked for")
                continue
            naive = self.spec.knobs[knob].default
            r.plausibility[knob] = plausible(self.assumptions.get(knob), value, naive)
            a = self.assumptions.get(knob)
            if not r.plausibility[knob].supported and a is not None and self.evidence is not None:
                ev = await self.evidence.find(knob, value)
                if ev is not None:
                    self.assumptions[knob] = a = a.model_copy(update={"evidence": [*a.evidence, ev]})
                    r.plausibility[knob] = plausible(a, value, naive)
                    self.orch.events.emit("note", msg=f"web evidence for {knob}={value}: {ev.ref}")

        cf_ok = all(v["ok"] for v in r.counterfactual.values())
        ho_ok = all(v["ok"] for v in r.held_out.values())
        # with the gate off nothing is ever supported, even when verify=False leaves no plausibility rows
        plaus_ok = self.cfg.evidence_gate and all(p.supported for p in r.plausibility.values())
        if not self.cfg.evidence_gate:
            r.notes.append("evidence gate off: no evidence was checked, so this cannot be labelled Explained")
        reduced = (abs(r.gap_before) - abs(r.gap_after) >= self.cfg.partial_frac * abs(r.gap_before)
                   and self.units(t, changes) >= thr)
        if closes(changes) and cf_ok and ho_ok:
            if not plaus_ok:
                label = ConfidenceLabel.fits_but_unsupported
            elif any(p.partial for p in r.plausibility.values()):
                label = ConfidenceLabel.partially_explained  # only the direction toward the paper was tested
                r.notes.append("closes the gap moving toward the paper's stated value; that value itself is untested")
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

    async def _triage_failures(self, hyps: list[Hypothesis], tried: set) -> list[Hypothesis]:
        """Super reads why a hypothesis's runs all failed; an invalid value gets one corrected retry."""
        if self.router is None:
            return []
        from gapfinder.search.triage import triage

        retry = []
        for h in hyps:
            runs = self._runs.get(frozenset(h.changes.items()), [])
            if not runs or any(b.status == BranchStatus.succeeded for b in runs):
                continue
            if any(x["knob"] == h.knob and x["value"] == h.value for x in self.triaged):
                continue  # already triaged (e.g. while explaining another claim)
            try:
                tr = await triage(self.router, h.knob, h.value, self.spec.knobs[h.knob].default, runs[-1])
            except Exception as exc:  # triage is best-effort
                self.triaged.append({"knob": h.knob, "value": h.value, "kind": "other", "why": f"triage failed: {exc}"})
                continue
            rec = {"knob": h.knob, "value": h.value, "kind": tr.kind, "why": tr.why, "suggestion": tr.suggestion}
            self.triaged.append(rec)
            self.orch.events.emit("note", msg=f"triage {h.knob}={h.value}: {tr.kind} ({tr.why[:120]})")
            s = (tr.suggestion or "").strip()
            fixed = Hypothesis(h.knob, s, h.assumption_id)
            if (tr.kind == "invalid_value" and s and s != self.spec.knobs[h.knob].default
                    and frozenset(fixed.changes.items()) not in tried and self.spec.knobs[h.knob].affordable(s)
                    and self._renderable(fixed, ClaimResult(target=self.targets[0], status="", gap_before=0, band=0))):
                retry.append(fixed)
                rec["retried"] = s
        if retry:
            await _all(*(self.measure(h.changes, self.cfg.screen_repeats, f"screen {h.knob}={h.value} (triaged)")
                         for h in retry))
            tried.update(frozenset(h.changes.items()) for h in retry)
        return retry

    def _stated_values(self, knob: str) -> list[str]:
        """Paper values for `knob` that apply to the targets' figures. An entry tied only to claims of
        other figures (e.g. Monkey for Figure 8 when Figure 6 is explained) doesn't count."""
        out = []
        for a in self.all_for.get(knob, []):
            if a.paper_value.strip().lower().startswith("unstated"):
                continue
            figs = {self.claim_figure.get(c) for c in a.affects_claims if c in self.claim_figure}
            if self.target_figures and figs and not (figs & self.target_figures):
                continue  # stated for another experiment
            out.append(a.paper_value)
        return out

    def _prior(self, knob: str) -> float:
        """The ledger's prior; in the random arm a seeded random number, so no ledger ranking is used."""
        if self.cfg.rank == "random":
            return random.Random(f"{self.cfg.seed}:{knob}").random()
        return self.assumptions[knob].prior_score

    def _strong_lead(self, h: Hypothesis) -> bool:
        if self.cfg.rank == "random":
            return False  # no ledger leads: every hypothesis must survive the screen on its own effect
        a = self.assumptions.get(h.knob)
        return a is not None and (a.prior_score >= self.cfg.confirm_prior_min
                                  or a.status == AssumptionStatus.stated_code_differs.value)

    def _supported(self, changes: Changes) -> bool:
        if not self.cfg.evidence_gate:
            return False  # candidates are not ordered by evidence either
        return all(plausible(self.assumptions.get(k), v, self.spec.knobs[k].default).supported
                   for k, v in changes.items())

    def _attribution(self, t: Target, changes: Changes, gap_after: float, label: ConfidenceLabel,
                     checkpoints: list[str], held: dict | None = None, cf_ok: bool | None = None) -> Attribution:
        aset = [f"{self.assumptions[k].id if k in self.assumptions else '?'}:{k}={v}" for k, v in changes.items()]
        held_txt = None
        if held:
            held_txt = "; ".join(f"{cid}: {'ok' if v['ok'] else 'WORSE'}" for cid, v in held.items())
        return Attribution(claim_id=t.claim_id, assumption_set=aset, gap_before=self.gap(t, {}),
                           gap_after=gap_after, noise_band=self.band(t), held_out_result=held_txt,
                           counterfactual_ok=cf_ok, checkpoint_ids=checkpoints, confidence_label=label)

    async def _label_partial(self, t: Target, res: ClaimResult) -> None:
        """Budget ran out. Verify the best measured configurations using only runs already made;
        anything that can't be verified that way is NOT given a confident label."""
        measured = [dict(k) for k in self._runs if k and self.value(dict(k), t.metric) is not None]
        measured.sort(key=lambda c: (abs(self.gap(t, c)), len(c), sorted(c.items())))
        best: ClaimResult | None = None
        rejected: list[str] = []
        for c in measured[: self.cfg.verify_candidates]:
            if len(self.measure_ok(c)) < self.confirm_repeats(t):
                continue  # a screen run alone is not a confirmation: the full search would repeat it first
            try:
                trial = await self._verify(t, c, res)  # raises if it would need a new run
            except (RunBudgetExceeded, budget.BudgetExceeded):
                continue
            if _rank(trial) >= _LABEL_RANK[ConfidenceLabel.unexplained.value]:
                why = "; ".join(trial.notes) or "did not pass verification"
                rejected.append(f"{c} (gap {self.gap(t, c):+.1%}) was verified from existing runs and rejected: {why}")
            if best is None or _rank(trial) < _rank(best):
                best = trial
        if best is not None and _rank(best) < _LABEL_RANK[ConfidenceLabel.unexplained.value]:
            for f in ("attribution", "changes", "gap_after", "held_out", "counterfactual", "plausibility", "replay"):
                setattr(res, f, getattr(best, f))
            res.notes.extend(best.notes)
            res.notes.append("verified from runs already made, after the budget ran out")
            return
        res.attribution = self._attribution(t, {}, res.gap_before, ConfidenceLabel.unexplained, [])
        res.gap_after = res.gap_before
        res.notes.extend(rejected)
        unverified = [c for c in measured[: self.cfg.verify_candidates] if not any(str(c) in r for r in rejected)]
        if unverified:
            c = unverified[0]
            res.notes.append(f"closest configuration not verified: {c} (gap {self.gap(t, c):+.1%}, "
                             f"{len(self.measure_ok(c))} of {self.confirm_repeats(t)} confirmation runs); "
                             "the budget ran out first, so no attribution is made")

    def closest_overall(self, top: int = 5, min_runs: int = 2) -> list[dict]:
        """Configurations closest to the paper across ALL claims at once (mean |gap|), for the report.
        Labels judge one claim at a time; this shows when one change moves several claims together."""
        rows = []
        for key in self._runs:
            c = dict(key)
            n = len([b for b in self._runs[key] if b.status == BranchStatus.succeeded])
            gaps = {t.claim_id: self.gap(t, c) for t in self.targets}
            if n < min_runs or any(g is None for g in gaps.values()):
                continue
            rows.append({"changes": c, "runs": n, "gaps": gaps,
                         "mean_abs_gap": sum(abs(g) for g in gaps.values()) / len(gaps)})
        rows.sort(key=lambda r: (r["mean_abs_gap"], len(r["changes"])))
        return rows[:top]

    def seed(self, events: list[dict]) -> int:
        """Resume: reuse branch results from an earlier run's event log (same spec and checkpoints)."""
        n = 0
        for ev in events:
            if ev.get("type") == "branch_finished" and ev["branch"].get("knob_changes") is not None:
                b = Branch(**ev["branch"])
                if b.status in (BranchStatus.succeeded.value, BranchStatus.failed.value, BranchStatus.timed_out.value):
                    self._runs.setdefault(frozenset(b.knob_changes.items()), []).append(b)
                    n += 1
        self.runs_used += n
        return n

    def _renderable(self, h: Hypothesis, res: ClaimResult) -> bool:
        try:
            self.spec.render(self.spec.run, h.changes)
            return True
        except ValueError as exc:
            res.notes.append(f"skipped {h.knob}={h.value!r}: {exc}")
            return False


async def _all(*coros):
    """Measure in parallel. If one measurement hits the run or dollar budget, the others (already
    started and paid for) still finish and are recorded before the error is raised; a plain gather
    would leave them running unattended and lose their results when the search ends."""
    out = await asyncio.gather(*coros, return_exceptions=True)
    for x in out:
        if isinstance(x, BaseException):
            raise x
    return out


def _stated_value(paper_value: str) -> str | None:
    """A plain stated value ('2000', '100000000', 'true'), or None for prose or 'unstated'."""
    v = paper_value.strip().strip("\"'")
    if v.lower().startswith("unstated") or " " in v or not v:
        return None
    return v


def _rank(r: ClaimResult) -> int:
    return _LABEL_RANK[r.attribution.confidence_label] if r.attribution else 9
