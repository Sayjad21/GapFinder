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
import math
import random
import re
import statistics
from dataclasses import dataclass, field

from gapfinder.ledger.schemas import Assumption, AssumptionStatus, Evidence, Attribution, Branch, BranchStatus, ConfidenceLabel
from gapfinder.models import budget
from gapfinder.sandbox.noise import NoiseBand, bootstrap_diff_ci, mde, noise_band
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.search.bisect import minimal_set
from gapfinder.search.hypotheses import _same_number, coverage_values, fill_choices, mark_multipliers_from_flow
from gapfinder.ledger.assumptions import derive_status
from gapfinder.search.verify import Plausibility, gap_returns, held_out_ok, plausible

Changes = dict[str, str]
HM_TIE = 2.0  # history matching: a repeated fit may be named only within this many implausibility units of the best fit
LL_EQUIVALENT = 2.0  # log-likelihood units: within this of the best, the target can't tell two fits apart
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
    # a held-out row the paper tuned on its own (another method or dataset with its own sweep; blind-1:
    # FastGCN's inductive rows): measured and reported, but one shared setting isn't expected to fit it, so
    # a conflict with it is a note, not a rejection, and it is left out of the joint history-matching fit
    tuned_separately: bool = False
    figure: str | None = None  # e.g. "Figure 6": which experiment's stated settings apply


@dataclass
class SearchConfig:
    screen_top_k: int = 24  # assumptions screened, by prior
    candidates_per_knob: int = 2
    # v1.1 value coverage: also try every accepted choice of a categorical knob, or a coarse-first log
    # ladder around a numeric default, up to this many values per knob (paper and ledger values first).
    # In 14 of v1.0's 18 blind-test misses a true value was never tested at all.
    coverage: bool = True
    # spec knobs that no ledger assumption names are screened too, at a low prior (blind-1)
    screen_spec_knobs: bool = True
    # runtime sink tracing (gapfinder/search/trace.py): one dry run before the search learns each knob's
    # role from the sink its value reaches, and finds literals that reach sinks with no knob behind them
    trace: bool = True
    trace_steps: int = 30  # the dry run stops itself after this many optimizer steps...
    trace_seconds: float = 900  # ...or this many seconds
    coverage_candidates: int = 6  # values per knob at least (the ledger's first, then coverage values)
    # ...and up to this many when the run budget allows: per knob, coverage_budget_frac x max_runs spread
    # over the open knobs (test-v11-05: a fixed 6 cut epochs=75 on a task with few open knobs)
    coverage_max: int = 10
    coverage_budget_frac: float = 0.3
    # the combine round pairs this many of each top knob's best-scoring values (the true value of an
    # interaction half is often not its knob's best single value), at most combine_max_pairs pairs
    combine_values_per_knob: int = 2
    combine_max_pairs: int = 40
    # among equally good fits (gaps within one noise band), prefer the smallest change (see _change_size)
    parsimony: bool = True
    # confirmation as a two-stage race: every screen survivor gets 2 fresh runs, then only the likeliest
    # (top half, at least race_keep, plus ties and strong ledger leads) get the full repeats; the runs
    # saved go to later rounds (test-v11-05: 14 survivors x ~5 runs used a third of the budget)
    racing: bool = True
    race_keep: int = 4
    # forward step in the combine round: the best confirmed singles (anchors) are paired with every
    # screened value of the other top knobs, not just those values that scored well alone. An
    # interaction partner can move the metric the wrong way on its own (test-v11-05: epochs=75 alone moved
    # away from the paper and was never paired with normalize=minmax)
    # confirmation escrow: screening and the combine round may use at most (1 - escrow_frac) of max_runs;
    # the rest is kept for confirming the likeliest configurations (MC Dropout v1.2: the closest pair,
    # +1.3%, had one run when the budget ended; 7 of 15 sealed v1.2 cause runs hit the cap)
    escrow_frac: float = 0.25
    # coarse-flat early stop: a numeric knob whose two coarse ladder rungs (x10, /10) both leave the metric
    # within this many noise bands of the naive run doesn't get its finer rungs screened (0 = off). On the
    # dev tasks no planted value sat behind flat coarse rungs (smallest coarse movement 0.8 bands).
    coarse_stop_bands: float = 0.5
    # patch knobs (gapfinder/sandbox/ast_patch.py): when history matching says out of space, the top
    # static code leads that are literals in imported modules are tested in memory, files untouched
    patch_knobs: bool = True
    patch_top_k: int = 3
    patch_values: int = 6
    # share of max_runs held back for the patch round once the claims already look out of space after the
    # combine round (MC Dropout v1.3: the patch round ran last and got 5 of its 36 configurations)
    patch_budget_frac: float = 0.15
    forward_anchors: int = 2
    forward_max_pairs: int = 30
    # multi-claim history matching after each search (gapfinder/search/history.py): turns a bare
    # Unexplained into "explains target, conflicts with held-out" or an out-of-space diagnosis
    history_matching: bool = True
    # an Unexplained gap smaller than the minimum detectable effect (gapfinder.sandbox.noise.mde, at the
    # confirmation repeats) reads Inconclusive: a cause that closed it couldn't have been confirmed
    mde_inconclusive: bool = True
    hm_paper_n: float = 1.0  # runs behind the paper's number (1 = conservative)
    hm_disc: float = 0.05  # discrepancy fraction for scaled surrogates
    # confirmation counts only runs made after a hypothesis was selected (the screening run that picked
    # it is excluded: winner's curse), with a Bonferroni-corrected bootstrap over the confirm round
    strict_confirm: bool = True
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
    # every measured value of each explaining knob that fits about as well (equifinality): the honest
    # answer when one target claim can't tell e.g. max_steps 400, 500 and 1000 apart
    value_sets: dict[str, list[str]] = field(default_factory=dict)
    diagnosis: dict | None = None  # history matching over every measured configuration (all claims)
    closes: bool = False  # the configuration closes the gap fully (within its noise band)
    # every configuration the target claim can't tell apart from the answer (likelihood within
    # LL_EQUIVALENT of the answer's, held-out claims no worse), the answer first
    equivalent: list[dict] = field(default_factory=list)


def _norm_knob(k: str) -> str:
    return k.strip().lstrip("-").replace("-", "_").lower()


# words that name the kind of quantity, not the quantity: `num_epochs` is `epochs`, `dropout_rate` is
# `dropout`, `early_stopping_patience` is `early_stopping` (blind-1: the ledger named FastGCN's flags so)
_FILLER = {"num", "n", "number", "of", "the", "rate", "size", "dim", "dims", "value", "count", "patience",
           "max", "total", "param"}
_ABBREV = {"lr": "learning", "bs": "batch", "wd": "weight_decay"}


def _core(name: str) -> frozenset[str]:
    """The words of a knob name that say which quantity it is (digits, plurals and filler dropped)."""
    out = set()
    for tok in _norm_knob(name).split("_"):
        tok = re.sub(r"\d+$", "", tok)
        tok = _ABBREV.get(tok, tok)
        for t in tok.split("_"):
            if len(t) > 3 and t.endswith("s"):
                t = t[:-1]
            if t and t not in _FILLER:
                out.add(t)
    return frozenset(out)


def paper_mentions(text: str, knob: str, limit: int = 5) -> list[str]:
    """Sentences of the paper that name the knob's quantity (every core word of its name) and give a
    number, e.g. "We swept learning rate in the set {0.01, 0.001, 0.0001}" for `learning_rate` (blind-1).
    Evidence for a fallback knob: a value it states can count as supported, as a ledger quote would."""
    # the knob's whole name as a phrase ("learning rate", not just "learning", which titles use too)
    words = [_ABBREV.get(t, t) for t in (re.sub(r"\d+$", "", t) for t in _norm_knob(knob).split("_")) if t]
    if not words:
        return []
    phrase = re.compile(r"\b" + r"[\s_-]+".join(re.escape(w) for w in " ".join(words).replace("_", " ").split())
                        + r"s?\b")
    flat = re.sub(r"\s+", " ", text)
    out = []
    for sent in re.split(r"(?<=[.!?;])\s+(?=[A-Z(])", flat):
        if phrase.search(sent.lower()) and re.search(r"\d", sent):
            out.append(sent.strip()[:300])
            if len(out) >= limit:
                break
    return out


def map_knob_name(name: str, knobs) -> str | None:
    """The spec knob an assumption's name refers to: an exact match, else the one knob with the same
    core words. None when nothing or several knobs match (a guess there could test the wrong knob)."""
    by_norm = {_norm_knob(k): k for k in knobs}
    if (k := by_norm.get(_norm_knob(name))) is not None:
        return k
    # "FLAGS.hidden1", "args.lr", "rank1 (sample size top layer)": the name without its namespace or gloss
    name = re.sub(r"\s*\(.*$", "", name.strip())
    name = re.sub(r"^(?:[A-Za-z_]\w*\.)+", "", name).strip().replace(" ", "_")
    if (k := by_norm.get(_norm_knob(name))) is not None:
        return k
    core = _core(name)
    if not core:
        return None
    hits = [k for k in knobs if _core(k) == core]
    return hits[0] if len(hits) == 1 else None


class GapSearch:
    def __init__(self, orch: Orchestrator, targets: list[Target], assumptions: list[Assumption],
                 cfg: SearchConfig | None = None, evidence=None, claims: list | None = None, router=None,
                 paper_text: str | None = None):
        """`evidence`: optional EvidenceSearch (web) consulted when paper and code don't back a value.
        `claims`: the ledger's claims, so a paper value can be tied to the experiment it belongs to."""
        self.orch, self.targets, self.cfg = orch, targets, cfg or SearchConfig()
        self.evidence = evidence
        self.router = router  # optional: Nemotron 3 Super triages failed hypotheses
        self.setup_check: dict | None = None  # filled when noise_setups > 1
        self.triaged: list[dict] = []
        self.claims = {c.id: c for c in (claims or [])}  # carried into the Gap Report (quote, page)
        self.claim_figure = {c.id: c.figure_or_table for c in (claims or [])}
        self.target_figures = {t.figure for t in targets if t.figure}
        self.spec = orch.spec
        self._family = 1  # hypotheses tested together in the current confirm round (multiple comparisons)
        self._artifact_flags = None  # the artifact's repo map, when its code is on this machine
        self.trace_report = None  # set by _trace() when the dry run recorded anything
        if self.cfg.coverage and self.spec.code_root() is not None:  # a local base, or the spec's `source`
            self._fill_choices_from_artifact()
        # assumption -> spec knob; assumptions about knobs the harness can't set are skipped (and reported)
        self.assumptions: dict[str, Assumption] = {}
        self.all_for: dict[str, list[Assumption]] = {}  # every ledger entry per knob (papers state some twice)
        self.unmapped: list[str] = []
        self.renamed: dict[str, str] = {}  # ledger name -> spec knob, when they differ (`num_epochs` -> `epochs`)
        for a in sorted(assumptions, key=lambda a: -a.prior_score):
            k = map_knob_name(a.knob, self.spec.knobs)
            if k is None:
                self.unmapped.append(a.knob)
                continue
            if _norm_knob(k) != _norm_knob(a.knob):
                self.renamed[a.knob] = k
                a = a.model_copy(update={"knob": k})
            self.all_for.setdefault(k, []).append(a)
        # spec knobs no assumption names are a fallback: screened only when the ledger's knobs leave the target
        # without a confident answer (blind-1: FastGCN's epochs, dropout and hidden size were never tested,
        # because the ledger named none of them as the spec does). Screening them up front cost the toy
        # interaction task its combine budget, so they don't compete with the ledger's leads.
        self.spec_only: list[str] = []
        if self.cfg.screen_spec_knobs:
            from gapfinder.search.hypotheses import assumptions_from_spec

            floor = min((a.prior_score for a in assumptions), default=0.5)
            for a in assumptions_from_spec(self.spec)[0]:
                if a.knob not in self.all_for:
                    self.all_for[a.knob] = [a.model_copy(update={"prior_score": round(min(0.1, floor / 2), 4)})]
                    self.spec_only.append(a.knob)
        self._check_code_defaults()
        for k, entries in self.all_for.items():
            # one representative (highest prior) carrying the union of evidence and candidates
            head = entries[0]
            evidence = [e for a in entries for e in a.evidence]
            cands = list(dict.fromkeys(str(v) for a in entries for v in a.candidate_values))
            self.assumptions[k] = head.model_copy(update={"evidence": evidence, "candidate_values": cands})
        self._fallback: dict[str, Assumption] = {k: self.assumptions.pop(k) for k in self.spec_only}
        if paper_text:  # a fallback knob has no ledger evidence: give it the paper's sentences that name it
            for k, a in self._fallback.items():
                quotes = paper_mentions(paper_text, k)
                if quotes:
                    self._fallback[k] = a.model_copy(update={"evidence": [
                        Evidence(kind="paper", ref="paper text", quote=q) for q in quotes]})
        self._runs: dict[frozenset, list[Branch]] = {}
        self.untestable: list[tuple[str, str]] = []  # (knob, value) above the spec's cost limit
        self._patch_reserve = 0  # runs held back for the patch round (set after the combine round)
        self._coarse: set[tuple[str, str]] = set()  # coarse ladder rungs (screened first)
        self._fine: set[tuple[str, str]] = set()  # finer rungs (screened only if the coarse ones move the metric)
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
            cap = self.cfg.max_runs
            if cap is not None and self._patch_reserve and not label.startswith("patch"):
                cap -= self._patch_reserve  # the patch round's share
            if cap is not None and self.runs_used + need > cap:
                raise RunBudgetExceeded(f"run budget of {self.cfg.max_runs} reached "
                                        f"(wanted {need} more run(s) of {dict(changes) or 'naive'} for {label!r})")
            self.runs_used += need
            new = await self.orch.fanout([changes] * need, [label] * need, fresh_setup=fresh)
            have.extend(new)
            from gapfinder.search.triage import looks_like_infra

            flaky = [b for b in new if b.status != BranchStatus.succeeded and looks_like_infra(b)]
            if flaky and (self.cfg.max_runs is None or self.runs_used + len(flaky) <= self.cfg.max_runs):
                # the environment failed, not the configuration: run it again once, same values
                self.runs_used += len(flaky)
                have.extend(await self.orch.fanout([changes] * len(flaky),
                                                   [f"{label} (retry after infra failure)"] * len(flaky),
                                                   fresh_setup=fresh))
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
        runs = self.measure_ok(changes)
        if self.cfg.strict_confirm:
            fresh = [b for b in runs if not (b.note or "").startswith("screen")]
            if len(fresh) >= 2:
                runs = fresh  # the screening run selected this hypothesis; it can't also confirm it
        cand = [b.parsed_metrics[t.metric] for b in runs if t.metric in b.parsed_metrics]
        if len(base) < 2 or len(cand) < 2:
            return None
        alpha = self.cfg.effect_alpha or 0.05
        if self.cfg.strict_confirm:
            alpha /= self._family  # Bonferroni over the hypotheses confirmed together
        return bootstrap_diff_ci(base, cand, alpha=alpha)

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
        for c in self.corrected_defaults:
            self.orch.events.emit("note", msg=f"code default of {c['knob']}: ledger said {c['ledger']!r}, the code "
                                              f"says {c['code']!r} at {c['at']} (status {c['status']})")
        if self.unverified_defaults:
            self.orch.events.emit("note", msg="code defaults the code doesn't confirm (no paper-artifact "
                                              f"inconsistency on them): {', '.join(sorted(self.unverified_defaults))}")
        if self.renamed or self.spec_only:
            self.orch.events.emit("note", msg="knob names: " + ", ".join(f"{a} -> {k}" for a, k in self.renamed.items())
                                  + (f"; spec knobs no assumption names (a fallback round): {', '.join(self.spec_only)}"
                                     if self.spec_only else ""))
        if self.cfg.trace:
            await self._trace()
        await self.calibrate()
        results = []
        for t in self.targets:
            if not t.held_out:
                results.append(await self.explain(t))
        return results

    async def _trace(self) -> None:
        """Dry-run trace: roles for the knobs (candidate values follow the sink a value reaches, not its
        name) and literal leads for the patch round. Nothing changes when nothing was traced."""
        from gapfinder.search.trace import analyze, apply_roles

        try:
            recs = await self.orch.trace_run(self.cfg.trace_steps, self.cfg.trace_seconds)
        except (budget.BudgetExceeded, RunBudgetExceeded):
            raise
        except Exception as exc:  # tracing is an aid: a failure leaves the search as it was
            self.orch.events.emit("note", msg=f"trace: skipped ({type(exc).__name__}: {str(exc)[:160]})")
            return
        if not recs:
            self.orch.events.emit("note", msg="trace: no records (not a Python artifact, or the hook didn't load)")
            return
        rep = analyze(recs, self.spec.knobs, self.spec.code_root())
        self.trace_report = rep
        changed = apply_roles(self.spec, rep)
        self.orch.events.emit("trace", **rep.to_dict(), applied=changed)
        self.orch.events.emit("note", msg="trace: " + rep.summary())

    def hypotheses(self) -> list[Hypothesis]:
        """One hypothesis per (knob, candidate value). A knob whose value the paper states and the
        code already uses can't cause the gap (the naive run already matches the paper there)."""
        out = []
        open_knobs = []
        for k, a in self.assumptions.items():
            if self.spec.knobs[k].role == "seed":
                continue  # traced to a random seed: noise, never a cause
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
            # the default itself is the naive run, in any spelling ("0" for 0.0: test-v11-01 proposed init_q=0)
            is_default = lambda v: str(v) == default or _same_number(str(v), default)  # noqa: E731
            values = []
            for v in [str(v) for v in a.candidate_values if not is_default(v)] or [
                    v for v in spec_knob.candidates if not is_default(v)]:
                if not any(v == w or _same_number(v, w) for w in values):
                    values.append(v)
            if spec_knob.choices:  # a value the program rejects can't be the cause
                values = [v for v in values if v in spec_knob.choices]
            for v in reversed([_stated_value(s) for s in stated]):
                if v is not None and not is_default(v):  # the paper's own values come first
                    if v in values:
                        values.remove(v)
                    values.insert(0, v)
            if self.cfg.coverage:
                ladder = coverage_values(spec_knob, knob)
                plain = not spec_knob.choices and not spec_knob.multiplier
                for i, v in enumerate(ladder):
                    if v not in values and not any(_same_number(v, w) for w in values):
                        values.append(v)
                        if plain:  # numeric ladder: rungs 0-1 are coarse, the rest fine (two-stage screening)
                            (self._coarse if i < 2 else self._fine).add((knob, v))
            affordable = [v for v in values if spec_knob.affordable(v)]
            for v in values:
                if not spec_knob.affordable(v) and (knob, v) not in self.untestable:
                    self.untestable.append((knob, v))
            per_knob = self._per_knob_cap(len(open_knobs[: self.cfg.screen_top_k])) if self.cfg.coverage                 else self.cfg.candidates_per_knob
            for v in affordable[:per_knob]:
                out.append(Hypothesis(knob, v, a.id))
        if self.cfg.rank == "random":
            rng.shuffle(out)
        return out

    def _exploration_room(self) -> int | None:
        """Runs screening and combining may still use before reaching the confirmation escrow."""
        if self.cfg.max_runs is None or not self.cfg.escrow_frac:
            return None
        return max(0, int(self.cfg.max_runs * (1 - self.cfg.escrow_frac)) - self.runs_used)

    def _per_knob_cap(self, n_open: int) -> int:
        """Values per knob: at least coverage_candidates, more when the budget spread over the open knobs
        allows, at most coverage_max."""
        if self.cfg.max_runs is None or n_open <= 0:
            return self.cfg.coverage_candidates
        share = int(self.cfg.coverage_budget_frac * self.cfg.max_runs / n_open)
        return max(self.cfg.coverage_candidates, min(self.cfg.coverage_max, share))

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
        confident = {ConfidenceLabel.explained.value, ConfidenceLabel.inconsistency.value}
        if self._fallback and not (res.attribution and res.attribution.confidence_label in confident):
            await self._spec_knob_round(t, res, tried)
        res.hypotheses_tested = len(tried)
        if self.cfg.mde_inconclusive:
            self._mde_check(t, res)
        if self.cfg.history_matching:
            self._history_match(t, res)
            if self.cfg.patch_knobs and (res.diagnosis or {}).get("kind", "").startswith("out_of_space"):
                try:
                    await self._patch_round(t, res)
                except (RunBudgetExceeded, budget.BudgetExceeded) as exc:
                    res.notes.append(f"patch round stopped early: {exc}")
        if res.attribution is not None:
            res.attribution.hypotheses_tested = len(tried)
        self.orch.events.emit("attribution", claim=t.claim_id, status=res.status,
                              label=res.attribution.confidence_label if res.attribution else None,
                              changes=res.changes, gap_before=g0, gap_after=res.gap_after)
        return res

    async def _spec_knob_round(self, t: Target, res: ClaimResult, tried: set[frozenset]) -> None:
        """The ledger's knobs gave no confident answer: search again with the spec knobs no assumption names
        added (low prior, code-derived values). Runs already measured are reused. The better result is kept."""
        added = list(self._fallback)
        self.orch.events.emit("note", msg=f"{t.claim_id}: no confident answer from the ledger's knobs; adding spec "
                                          f"knobs no assumption names: {', '.join(added)}")
        self.assumptions.update(self._fallback)
        self._fallback = {}
        alt = ClaimResult(target=t, status="searched", gap_before=res.gap_before, band=res.band)
        try:
            await self._search(t, alt, tried)
        except (RunBudgetExceeded, budget.BudgetExceeded) as exc:
            alt.status = "partial"
            alt.notes.append(f"stopped early: {exc}")
            await self._label_partial(t, alt)
        if _better(alt, res):
            notes = alt.notes + [f"found after adding spec knobs no ledger assumption names ({', '.join(added)})"]
            res.__dict__.update(alt.__dict__)
            res.notes = notes
        else:
            res.notes.append(f"spec knobs no ledger assumption names ({', '.join(added)}) were screened too; "
                             "no better answer")

    async def _search(self, t: Target, res: ClaimResult, tried: set[frozenset]) -> None:
        thr = self.cfg.effect_threshold
        hyps = [h for h in self.hypotheses() if self._renderable(h, res)]

        # 1. screen: one knob per branch, one run each (within the exploration share of the budget)
        room = self._exploration_room()
        new = [h for h in hyps if len(self._runs.get(frozenset(h.changes.items()), [])) < self.cfg.screen_repeats]
        if room is not None and len(new) * self.cfg.screen_repeats > room:  # recorded runs (resume) cost nothing
            done_already = [h for h in hyps if h not in new]
            self.orch.events.emit("note", msg=f"{t.claim_id}: escrow: screening {room // max(1, self.cfg.screen_repeats)} "
                                              f"of {len(hyps)} hypotheses, keeping the rest for confirmation")
            by_knob: dict[str, list[Hypothesis]] = {}
            for h in new:  # round robin over knobs: every knob keeps its first (coarse, ledger) values
                by_knob.setdefault(h.knob, []).append(h)
            rr = [lst[i] for i in range(max(map(len, by_knob.values()))) for lst in by_knob.values() if i < len(lst)]
            hyps = done_already + rr[: room // max(1, self.cfg.screen_repeats)]
        if self.cfg.coarse_stop_bands > 0 and any((h.knob, h.value) in self._fine for h in hyps):
            first = [h for h in hyps if (h.knob, h.value) not in self._fine]
            await _all(*(self.measure(h.changes, self.cfg.screen_repeats, f"screen {h.knob}={h.value}")
                         for h in first))
            flat = set()
            for k in {h.knob for h in hyps if (h.knob, h.value) in self._fine}:
                moves = [self._movement(t, {k: v}) for (kk, v) in self._coarse if kk == k
                         and self.value({k: v}, t.metric) is not None]
                if moves and max(moves) < self.cfg.coarse_stop_bands:
                    flat.add(k)
            if flat:
                self.orch.events.emit("note", msg=f"{t.claim_id}: coarse rungs flat (under {self.cfg.coarse_stop_bands:g} "
                                                  f"bands), finer rungs skipped for: {', '.join(sorted(flat))}")
            hyps = first + [h for h in hyps if (h.knob, h.value) in self._fine and h.knob not in flat]
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
        # strict: the confirmation runs come on top of the screening run(s) that selected the hypothesis
        extra = self.cfg.screen_repeats if self.cfg.strict_confirm else 0
        racers = survivors
        if self.cfg.racing and len(survivors) > self.cfg.race_keep and reps > 2:
            await _all(*(self.measure(h.changes, 2 + extra, "confirm (race)") for h in survivors))
            ll = {h: self.loglik(t, h.changes) for h in survivors}
            order = sorted(survivors, key=lambda h: -(ll[h] if ll[h] is not None else float("-inf")))
            best = ll[order[0]]
            n_keep = max(self.cfg.race_keep, (len(order) + 1) // 2)
            racers = [h for i, h in enumerate(order)
                      if i < n_keep or self._strong_lead(h)
                      or (best is not None and ll[h] is not None and ll[h] >= best - LL_EQUIVALENT)]
            dropped = [h for h in survivors if h not in racers]
            if dropped:
                self.orch.events.emit("note", msg=f"{t.claim_id}: race: {len(dropped)} of {len(survivors)} survivors "
                                                  "stop at 2 runs (less likely than the leaders): " + ", ".join(
                                                      f"{h.knob}={h.value}" for h in dropped))
        await _all(*(self.measure(h.changes, reps + extra, "confirm") for h in racers))
        self._family = max(1, len(survivors))  # the correction still counts every hypothesis raced
        confirmed = [h for h in racers if self.units(t, h.changes) >= thr and self._significant(t, h.changes)]
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
        ranked = {h.knob: [x for x in sorted(hyps, key=lambda x: -score[x]) if x.knob == h.knob] for h in top}
        k_vals = self.cfg.combine_values_per_knob if self.cfg.coverage else 1
        if self.cfg.coverage:  # use as many values per knob as the pair budget allows (few open knobs: all)
            def n_pairs(k: int) -> int:
                sizes = [min(k, len(v)) for v in ranked.values()]
                return sum(a * b for i, a in enumerate(sizes) for b in sizes[i + 1:])
            most = max((len(v) for v in ranked.values()), default=1)
            while k_vals < most and n_pairs(k_vals + 1) <= self.cfg.combine_max_pairs:
                k_vals += 1
        values_of = {k: v[:k_vals] for k, v in ranked.items()}
        pairs = []
        for a, b in itertools.combinations(top, 2):
            for va in values_of[a.knob]:
                for vb in values_of[b.knob]:
                    pairs.append((score[va] + score[vb], {a.knob: va.value, b.knob: vb.value}))
        pairs.sort(key=lambda p: -p[0])  # stable: knob-best pairs first, as before
        for _, c in pairs[: self.cfg.combine_max_pairs]:
            if c not in combos:
                combos.append(c)
        # ...only when no confirmed single already explains the target (consistent with the paper): a second
        # knob is then needed, and otherwise the extra pairs only add chances for a spurious fit (dev suite:
        # unconditional, 26 and 24 of 39 against 29 and 25)
        def consistent(h: Hypothesis) -> bool:
            i = self.implausibility(t, h.changes)
            return self.closes(t, h.changes) or (i is not None and i <= 2)
        if self.cfg.coverage and self.cfg.forward_anchors > 0 and confirmed and not any(map(consistent, confirmed)):
            lls = {h: self.loglik(t, h.changes) for h in confirmed}
            anchors = sorted(confirmed, key=lambda h: -(lls[h] if lls[h] is not None else float("-inf")))
            forward = []
            for anchor in anchors[: self.cfg.forward_anchors]:
                for k, vals in ranked.items():
                    if k == anchor.knob:
                        continue
                    for v in vals:
                        c = {anchor.knob: anchor.value, k: v.value}
                        if c not in combos and c not in forward:
                            forward.append(c)
            combos.extend(forward[: self.cfg.forward_max_pairs])
        room = self._exploration_room()
        fresh = [c for c in combos if not self._runs.get(frozenset(c.items()))]
        if room is not None and len(fresh) > room:
            self.orch.events.emit("note", msg=f"{t.claim_id}: escrow: combine tries {room} of {len(fresh)} new pairs, "
                                              "keeping the rest of the budget for confirmation")
            keep = set(map(lambda c: frozenset(c.items()), fresh[:room]))
            combos = [c for c in combos if self._runs.get(frozenset(c.items())) or frozenset(c.items()) in keep]
        await _all(*(self.measure(c, 1, "combine") for c in combos))
        tried.update(frozenset(c.items()) for c in combos)
        good_combos = [c for c in combos if self.units(t, c) >= thr]
        # closest to the paper first: runs take budget in launch order, so when it runs short the likeliest
        # pairs are the ones confirmed (MC Dropout v1.2: the documented pair, +1.3% and the closest of all,
        # had one run when the budget ended while other pairs were being confirmed)
        ll_c = {frozenset(c.items()): self.loglik(t, c) for c in good_combos}
        good_combos.sort(key=lambda c: -(ll_c[frozenset(c.items())] if ll_c[frozenset(c.items())] is not None
                                         else float("-inf")))
        racing_combos = good_combos
        if self.cfg.racing and len(good_combos) > self.cfg.race_keep and reps > 2:
            await _all(*(self.measure(c, 2, "confirm-combo (race)") for c in good_combos))
            ll_c = {frozenset(c.items()): self.loglik(t, c) for c in good_combos}
            order = sorted(good_combos, key=lambda c: -(ll_c[frozenset(c.items())] if ll_c[frozenset(c.items())]
                                                        is not None else float("-inf")))
            best_c = ll_c[frozenset(order[0].items())]
            n_keep = max(self.cfg.race_keep, (len(order) + 1) // 2)
            racing_combos = [c for i, c in enumerate(order)
                             if i < n_keep or (best_c is not None and ll_c[frozenset(c.items())] is not None
                                               and ll_c[frozenset(c.items())] >= best_c - LL_EQUIVALENT)]
        await _all(*(self.measure(c, reps, "confirm-combo") for c in racing_combos))
        self.orch.events.emit("round", name="combine", claim=t.claim_id, tried=len(combos), kept=len(good_combos))
        self._reserve_for_patches(t)

        # candidates: confirmed singles and combos, closest to the paper first
        candidates = [h.changes for h in confirmed] + [c for c in good_combos if self.units(t, c) >= thr
                                                         and self._significant(t, c)]
        candidates = self._order_candidates(t, candidates, res.gap_before)
        best: ClaimResult | None = None
        for c in candidates[: self.cfg.verify_candidates]:
            trial = await self._verify(t, c, res)
            if best is None or _better(trial, best):
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
        if res.changes:
            res.equivalent = self.equivalent_configs(t, res.changes, candidates)
            if len(res.equivalent) > 1:
                res.notes.append("configurations the target claim can't tell apart from the answer: " + "; ".join(
                    ", ".join(f"{k}={v}" for k, v in sorted(e["config"].items())) for e in res.equivalent))
            res.value_sets = self.equivalent_values(t, res.changes)
            wider = {k: v for k, v in res.value_sets.items() if len(v) > 1}
            if wider:
                res.notes.append("equally good values within one noise band (measured): " + "; ".join(
                    f"{k} in {{{', '.join(v)}}}" for k, v in wider.items()))

    async def _verify(self, t: Target, changes: Changes, parent: ClaimResult) -> ClaimResult:
        r = ClaimResult(target=t, status="searched", gap_before=parent.gap_before, band=parent.band)
        band, thr = parent.band, self.cfg.effect_threshold
        closes = lambda c: self.closes(t, c)  # noqa: E731

        # 4. bisect to the minimal set that still closes the gap, or that the dropped knob doesn't beat by
        #    more than one noise band (test-v11-10: a passenger knob that chased noise was kept because the
        #    single knob missed "closes" by one outlier run)
        if len(changes) > 1 and closes(changes):
            full = dict(changes)

            async def still_closes(sub: Changes) -> bool:
                await self.measure(sub, 1, "bisect")
                return closes(sub) or await self._not_worse_by_a_band(t, sub, full)
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
        # a knob whose removal doesn't bring the gap back by more than the noise band is a passenger (the
        # counterfactual's own criterion): once repeats confirm it, verify the configuration without it
        passengers = [k for k, v in r.counterfactual.items() if not v["ok"]]
        if self.cfg.verify and len(passengers) == len(changes) > 1:
            # every knob alone gets most of the way (test-v12-08: max_steps=100 alone 2.1% off, lr=0.5 alone
            # 11.6%, both 1.3%): keep the best single-knob reduction that the extra knobs don't beat by a band
            subs = sorted(({k: v for k, v in changes.items() if k != drop} for drop in changes),
                          key=lambda c: abs(self.gap(t, c)) if self.gap(t, c) is not None else float("inf"))
            for reduced in subs:
                if await self._not_worse_by_a_band(t, reduced, changes):
                    trial = await self._verify(t, reduced, parent)
                    trial.notes.append(f"{sorted(set(changes) - set(reduced))} dropped: each knob of {changes} alone "
                                       f"gets most of the way, and {reduced} is within one noise band of the full set")
                    return trial
        if self.cfg.verify and 0 < len(passengers) < len(changes):
            reduced = {k: v for k, v in changes.items() if k not in passengers}
            if await self._not_worse_by_a_band(t, reduced, changes):
                trial = await self._verify(t, reduced, parent)
                trial.notes.append(f"{', '.join(sorted(passengers))} dropped: with repeats, {changes} fits "
                                   f"{reduced}'s gap by less than one noise band, so it is not needed")
                return trial
        # 5b. held-out: every other claim must not get worse beyond its noise
        for other in self.targets if self.cfg.verify else ():
            if other.claim_id == t.claim_id:
                continue
            before, after = self.gap(other, {}), self.gap(other, changes)
            ok = after is not None and held_out_ok(before, after, self.band(other))
            if other.tuned_separately:
                r.held_out[other.claim_id] = {"gap_before": before, "gap_after": after, "ok": True,
                                              "tuned_separately": True, "worse": not ok}
                if not ok:
                    r.notes.append(f"{other.claim_id} (tuned separately) moves from {_pct(before)} to {_pct(after)} "
                                   f"under {dict(changes)}: reported, not a rejection")
                continue
            r.held_out[other.claim_id] = {"gap_before": before, "gap_after": after, "ok": ok}
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
        r.closes = closes(changes)
        if closes(changes) and cf_ok and ho_ok:
            if not plaus_ok:
                label = ConfidenceLabel.fits_but_unsupported
            elif any(p.partial for p in r.plausibility.values()):
                label = ConfidenceLabel.partially_explained  # only the direction toward the paper was tested
                r.notes.append("closes the gap moving toward the paper's stated value; that value itself is untested")
            elif any(self.assumptions[k].status == AssumptionStatus.stated_code_differs.value
                     and k not in self.unverified_defaults for k in changes if k in self.assumptions):
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
    async def _not_worse_by_a_band(self, t: Target, smaller: Changes, larger: Changes) -> bool:
        """Occam's margin: the extra knobs in `larger` are not needed if they close the gap by less than one
        noise band over `smaller` (|gap(smaller)| - |gap(larger)| <= band). An improvement that small is
        within what repeats of one configuration vary by, so it doesn't justify another change. Both get
        the confirmation repeats first (new runs, within the budget)."""
        n = self.confirm_repeats(t)
        try:
            await _all(self.measure(smaller, n, "occam"), self.measure(larger, n, "occam"))
        except (RunBudgetExceeded, budget.BudgetExceeded):
            pass  # decide on the runs there are
        if len(self.measure_ok(smaller)) < 2 or len(self.measure_ok(larger)) < 2:
            return False
        gs, gl = self.gap(t, smaller), self.gap(t, larger)
        ok = gs is not None and gl is not None and abs(gs) - abs(gl) <= self.band(t)
        self.orch.events.emit("note", msg=f"{t.claim_id}: {larger} vs {smaller}: gap {gl:+.1%} vs {gs:+.1%}, band "
                                          f"+-{self.band(t):.1%}: the extra knob is {'not needed' if ok else 'needed'}")
        return ok

    def confirm_repeats(self, t: Target) -> int:
        """Noisy metrics (run-to-run CV above 5%) get two extra repeats."""
        return self.cfg.confirm_repeats + (2 if self.bands[t.metric].cv > 0.05 else 0)

    async def _triage_failures(self, hyps: list[Hypothesis], tried: set) -> list[Hypothesis]:
        """Super reads why a hypothesis's runs all failed; an invalid value gets one corrected retry. A
        failure whose log shows an environment problem is retried once with the same value (no model call)."""
        from gapfinder.search.triage import looks_like_infra, shows_rejection, triage

        retry, again = [], []
        for h in hyps:
            runs = self._runs.get(frozenset(h.changes.items()), [])
            if not runs or any(b.status == BranchStatus.succeeded for b in runs):
                continue
            if any(x["knob"] == h.knob and x["value"] == h.value for x in self.triaged):
                continue  # already triaged (e.g. while explaining another claim)
            if len(runs) == 1 and looks_like_infra(runs[-1]):  # the environment failed, not the value
                self.triaged.append({"knob": h.knob, "value": h.value, "kind": "infra", "retried": h.value,
                                     "why": "the log shows an environment failure; the same value is run once more"})
                self.orch.events.emit("note", msg=f"triage {h.knob}={h.value}: infra (same value retried)")
                again.append(h)
                continue
            if self.router is None:
                continue
            try:
                tr = await triage(self.router, h.knob, h.value, self.spec.knobs[h.knob].default, runs[-1])
            except Exception as exc:  # triage is best-effort
                self.triaged.append({"knob": h.knob, "value": h.value, "kind": "other", "why": f"triage failed: {exc}"})
                continue
            if tr.kind == "invalid_value" and not shows_rejection(runs[-1]):
                # no rejection message in the log: keep the value rather than lose the hypothesis
                tr = tr.model_copy(update={"kind": "other", "suggestion": None,
                                           "why": f"{tr.why} [not taken as invalid_value: the log shows no rejection]"})
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
        if retry or again:
            await _all(*(self.measure(h.changes, self.cfg.screen_repeats, f"screen {h.knob}={h.value} (triaged)")
                         for h in retry),
                       *(self.measure(h.changes, self.cfg.screen_repeats,
                                      f"screen {h.knob}={h.value} (retry after infra failure)") for h in again))
            tried.update(frozenset(h.changes.items()) for h in retry)
        return retry  # the same-value retries are already in the caller's list

    def _reserve_for_patches(self, t: Target) -> None:
        """If the claims already look out of space and the code has literal leads, hold patch_budget_frac of
        the budget for the patch round, so verification can't spend it first."""
        if not (self.cfg.patch_knobs and self.cfg.history_matching and self.cfg.max_runs and self.cfg.patch_budget_frac):
            return
        root = self.spec.code_root()
        if root is None or self._patch_reserve:
            return
        from gapfinder.ingest.code_checks import code_checks
        from gapfinder.sandbox import ast_patch
        from gapfinder.search.history import diagnose

        claims = [(t.claim_id, t.metric, t.paper_value)] + [
            (h.claim_id, h.metric, h.paper_value) for h in self.targets if h.held_out
            and not h.tuned_separately and h.metric != t.metric]
        runs = {tuple(sorted(k)): [b.parsed_metrics for b in v if b.status == BranchStatus.succeeded]
                for k, v in self._runs.items()}
        d = diagnose({k: v for k, v in runs.items() if v}, claims, t.claim_id,
                     paper_n=self.cfg.hm_paper_n, disc=self.cfg.hm_disc)
        if not d.kind.startswith("out_of_space"):
            return
        leads = [x for x in code_checks(root, set(self.spec.knobs)) if x.family == "unexposed_setting" and x.value
                 and (not ast_patch.entry_script(root / x.file) or ast_patch.direct_entry(self.spec.run.command, x.file))]
        if leads:
            self._patch_reserve = int(self.cfg.max_runs * self.cfg.patch_budget_frac)
            self.orch.events.emit("note", msg=f"{t.claim_id}: out of space after the combine round; {self._patch_reserve} "
                                              f"runs held for a patch round ({len(leads)} literal code leads)")

    async def _patch_round(self, t: Target, res: ClaimResult) -> None:
        """Out of space: test the top static leads (hard-coded literals in imported modules) as patch knobs.
        A configuration with a patch that fits every claim, where no setting did, is confirmed and verified
        like any other; it is reported as a code change."""
        from gapfinder.sandbox import ast_patch
        from gapfinder.sandbox.spec import Knob
        from gapfinder.search.history import diagnose
        from gapfinder.search.hypotheses import patch_values, role_values

        root = self.spec.code_root()
        leads = [x for x in (res.diagnosis or {}).get("leads") or []
                 if x["family"] == "unexposed_setting" and x.get("name") and x.get("value")]
        if self.trace_report is not None:  # literals seen reaching a sink at runtime come first
            traced = [{"file": x.file, "line": x.line, "name": x.name, "value": x.literal, "family": "unexposed_setting",
                       "source": "trace", "sink": x.sink} for x in self.trace_report.leads]
            have = {(t["file"], t["line"]) for t in traced}
            leads = traced + [x for x in leads if (x["file"], x["line"]) not in have]
        # imported modules through the import hook; entry scripts only when the command runs them directly
        leads = [x for x in leads if root is not None and (not ast_patch.entry_script(root / x["file"])
                                                           or ast_patch.direct_entry(self.spec.run.command, x["file"]))]
        leads = leads[: self.cfg.patch_top_k]
        if not leads:
            return
        fits = [r for r in (res.diagnosis.get("per_claim") or {}).get(t.claim_id, []) if r["config"]]
        base = min(fits, key=lambda r: max(r["I"].values()))["config"] if fits else {}
        base = {k: v for k, v in base.items() if not ast_patch.is_patch(k)}
        with_base, alone = [], []
        for x in leads:
            k = ast_patch.knob_name(x["file"], x["line"], x["name"])
            self.spec.knobs.setdefault(k, Knob(layer="environment", default=str(x["value"]), env=True))
            role = "size" if str(x.get("sink", "")).startswith(("batch.", "width.")) else None
            vals = ((role_values(role, str(x["value"])) if role else None) or patch_values(x["name"], str(x["value"])))
            vals = vals[: self.cfg.patch_values]
            with_base.append([{**base, k: v} for v in vals] if base else [])
            alone.append([{k: v} for v in vals])

        def rr(groups):  # round robin over leads: every lead gets its first values first
            return [g[i] for i in range(max((len(g) for g in groups), default=0)) for g in groups if i < len(g)]
        configs = rr(with_base) + rr(alone)
        if self._patch_reserve:  # leave room for the confirmation repeats
            room = max(0, self.cfg.max_runs - self.runs_used - self.confirm_repeats(t))
            configs = configs[:room]
        self.orch.events.emit("note", msg=f"{t.claim_id}: patch round: {len(leads)} code lead(s), {len(configs)} "
                                          f"configurations (base {base or 'naive'})")
        await _all(*(self.measure(c, 1, "patch screen") for c in configs))

        def rediagnose():
            claims = [(t.claim_id, t.metric, t.paper_value)] + [
                (h.claim_id, h.metric, h.paper_value) for h in self.targets if h.held_out
            and not h.tuned_separately and h.metric != t.metric]
            runs = {tuple(sorted(k)): [b.parsed_metrics for b in v if b.status == BranchStatus.succeeded]
                    for k, v in self._runs.items()}
            return diagnose({k: v for k, v in runs.items() if v}, claims, t.claim_id,
                            paper_n=self.cfg.hm_paper_n, disc=self.cfg.hm_disc)

        d = rediagnose()
        joint = [r for r in d.joint if any(ast_patch.is_patch(k) for k in r["config"])]
        if not joint:
            res.notes.append(f"patch round: none of {len(configs)} code-patch configurations fits every claim")
            return
        c = joint[0]["config"]
        await self.measure(c, self.confirm_repeats(t), "patch confirm")
        d = rediagnose()
        if not any(r["config"] == c for r in d.joint):
            res.notes.append(f"patch round: {c} fitted every claim on one run, not after repeats")
            return
        trial = await self._verify(t, c, res)
        if _rank(trial) >= _LABEL_RANK[ConfidenceLabel.unexplained.value]:
            res.notes.append(f"patch round: {c} fits every claim but did not pass verification")
            return
        patches = {k: v for k, v in c.items() if ast_patch.is_patch(k)}
        for f in ("attribution", "changes", "gap_after", "held_out", "counterfactual", "plausibility", "replay"):
            setattr(res, f, getattr(trial, f))
        res.status = "searched"
        res.diagnosis = {**d.to_dict(), "leads": res.diagnosis.get("leads")}
        res.notes.extend(trial.notes)
        res.notes.append("explained with a code patch (tested in memory, no file edited): " + "; ".join(
            f"{ast_patch.parse(k)[0]} line {ast_patch.parse(k)[1]}: {ast_patch.parse(k)[2]} = "
            f"{self.spec.knobs[k].default} -> {v}" for k, v in patches.items()))

    def _mde_check(self, t: Target, res: ClaimResult) -> None:
        """Unexplained -> Inconclusive when the gap is below the minimum detectable effect."""
        if res.attribution is None or res.attribution.confidence_label != ConfidenceLabel.unexplained.value:
            return
        vals = [b.parsed_metrics[t.metric] for b in self.measure_ok({}) if t.metric in b.parsed_metrics]
        if len(vals) < 3 or res.gap_before is None:
            return
        n = self.confirm_repeats(t)
        m = mde(statistics.stdev(vals), n) / abs(t.paper_value)
        if abs(res.gap_before) >= m:
            return
        res.status = "inconclusive"
        res.attribution = self._attribution(t, {}, res.gap_before, ConfidenceLabel.inconclusive, [])
        res.notes.append(f"the gap ({res.gap_before:+.1%}) is below the minimum detectable effect (±{m:.1%} with "
                         f"{n} runs per configuration at 80% power): even a setting that closed it couldn't have "
                         "been confirmed, so 'nothing explains it' can't be claimed either")

    def _history_match(self, t: Target, res: ClaimResult) -> None:
        """Score every measured configuration against the target and its held-out claims together."""
        from gapfinder.search.history import diagnose

        claims = [(t.claim_id, t.metric, t.paper_value)] + [
            (h.claim_id, h.metric, h.paper_value) for h in self.targets if h.held_out
            and not h.tuned_separately and h.metric != t.metric]
        runs = {tuple(sorted(k)): [b.parsed_metrics for b in v if b.status == BranchStatus.succeeded]
                for k, v in self._runs.items()}
        runs = {k: v for k, v in runs.items() if v}
        d = diagnose(runs, claims, t.claim_id, paper_n=self.cfg.hm_paper_n, disc=self.cfg.hm_disc)
        res.diagnosis = d.to_dict()
        root = self.spec.code_root()
        if d.kind.startswith("out_of_space") and root is not None:
            from gapfinder.ingest.code_checks import code_checks

            leads = code_checks(root, set(self.spec.knobs))
            res.diagnosis["leads"] = [x.to_dict() for x in leads]
            if leads:
                self.orch.events.emit("note", msg=f"{t.claim_id}: {len(leads)} static lead(s) outside the settings, "
                                                  f"top: {leads[0].file}:{leads[0].line} {leads[0].detail}")
        self.orch.events.emit("note", msg=f"{t.claim_id}: history matching: {d.text}")
        label = res.attribution.confidence_label if res.attribution else None
        if label != ConfidenceLabel.unexplained.value:
            return
        res.notes.append(f"history matching: {d.text}")
        if d.kind == "out_of_space_suspected":
            fits = [r for r in d.per_claim[t.claim_id] if r["config"]]
            repeated = [r for r in fits if len(self.measure_ok(r["config"])) >= 2]
            if not repeated:  # one screening run is not enough to name a configuration
                res.notes.append(f"closest fit {fits[0]['config']} (I={fits[0]['I'][t.claim_id]:g}) has a single run; "
                                 "not labelled until it is repeated")
                return
            # among the configurations that fit the target, the held-out claims break the tie: take the
            # one whose worst claim is least implausible (the history-matching criterion), not the one
            # closest on the target alone (MC Dropout v1.1: five configurations fit Energy; the
            # documented one broke Yacht least)
            worst = lambda r: (max(r["I"].values()), r["I"][t.claim_id])  # noqa: E731
            best = min(repeated, key=worst)
            top = min(fits, key=worst)
            if max(best["I"].values()) > max(top["I"].values()) + HM_TIE:
                # the only repeated fits are much less consistent than an unrepeated one: naming them would
                # report the wrong configuration (MC Dropout v1.2: epochx=2, worst I 24, over fits at I 6-9)
                leads = sorted(fits, key=worst)[:3]
                res.notes.append("history matching: the most consistent fits have a single run, so none is named; "
                                 "unconfirmed leads: " + "; ".join(
                                     f"{r['config']} (worst I {max(r['I'].values()):g}, "
                                     f"{len(self.measure_ok(r['config']))} run(s))" for r in leads))
                return
            c = best["config"]
            broken = ", ".join(f"{cid} (I={i:g})" for cid, i in best["I"].items() if cid != t.claim_id and i > 3)
            res.changes, res.gap_after = dict(c), self.gap(t, c)
            res.attribution = self._attribution(t, c, res.gap_after, ConfidenceLabel.conflicts_held_out,
                                                [b.result_checkpoint for b in self.measure_ok(c) if b.result_checkpoint])
            res.value_sets = self.equivalent_values(t, c)
            res.notes.append(f"{dict(c)} matches {t.claim_id} (I={best['I'][t.claim_id]:g}) but breaks "
                             f"{broken or 'a held-out claim'}; no tested condition matches all claims, so the rest of "
                             "the gap probably lies in code, data or evaluation, which GapFinder doesn't change")

    def _order_candidates(self, t: Target, candidates: list[Changes], gap_before: float) -> list[Changes]:
        """Best first, the same order on every path (the full search and the budget-exhausted one):
        consistent with the paper > closes at least half > the rest; evidence-backed first within each tier;
        then equally good fits (likelihood within LL_EQUIVALENT of the best) by fewest knobs, smallest change
        from the default, likeliest. "Consistent" is closes() or an implausibility of at most 2 (closes()
        alone favours noisy candidates: test-v11-01, -10). v1.1 rounded |gap|/band into buckets, so two fits
        0.7 points apart could land in different buckets (test-v11-10 run 2)."""
        def tier(c: Changes) -> int:
            g, g0 = abs(self.gap(t, c)), abs(gap_before)
            i = self.implausibility(t, c)
            return (0 if self.closes(t, c) or (i is not None and i <= 2)
                    else 1 if g0 - g >= self.cfg.partial_frac * g0 else 2)
        if not self.cfg.parsimony:
            return sorted(candidates, key=lambda c: (tier(c), not self._supported(c), abs(self.gap(t, c)), len(c),
                                                     sorted(c.items())))
        ll = {frozenset(c.items()): self.loglik(t, c) for c in candidates}
        top = max((v for v in ll.values() if v is not None), default=None)

        def tied(c: Changes) -> int:
            v = ll[frozenset(c.items())]
            return 0 if top is not None and v is not None and v >= top - LL_EQUIVALENT else 1
        return sorted(candidates, key=lambda c: (tier(c), not self._supported(c), tied(c), len(c), self._change_size(c),
                                                 -(ll[frozenset(c.items())] or float("-inf")), sorted(c.items())))

    def _movement(self, t: Target, changes: Changes) -> float:
        """How far a configuration moves the target metric from the naive run, in noise bands, either way."""
        v, v0, band = self.value(changes, t.metric), self.naive.get(t.metric), self.band(t)
        if v is None or v0 is None or not band:
            return 0.0
        return abs(v - v0) / (band * abs(t.paper_value))

    def _sd(self, t: Target, changes: Changes) -> tuple[float, float, int] | None:
        """(mean, run-to-run SD, n) of the target metric at a configuration. The SD is the configuration's
        own with 3+ runs, else the naive one, never below the noise floor."""
        vals = [b.parsed_metrics[t.metric] for b in self.measure_ok(changes) if t.metric in b.parsed_metrics]
        if not vals:
            return None
        naive = [b.parsed_metrics[t.metric] for b in self.measure_ok({}) if t.metric in b.parsed_metrics]
        s0 = statistics.stdev(naive) if len(naive) >= 2 else 0.0
        s = statistics.stdev(vals) if len(vals) >= 3 else s0
        floor = self.cfg.noise_floor_frac * abs(t.paper_value)
        return statistics.fmean(vals), max(s, floor), len(vals)

    def _var(self, t: Target, changes: Changes) -> tuple[float, float] | None:
        """(mean, variance of mean - paper): the configuration's standard error plus the paper's own
        uncertainty (its number is one result of about hm_paper_n runs), plus a noise-floor term."""
        x = self._sd(t, changes)
        if x is None:
            return None
        m, s, n = x
        floor = self.cfg.noise_floor_frac * abs(t.paper_value)
        return m, s * s / n + s * s / self.cfg.hm_paper_n + floor * floor

    def implausibility(self, t: Target, changes: Changes) -> float | None:
        x = self._var(t, changes)
        return None if x is None else abs(x[0] - t.paper_value) / math.sqrt(x[1])

    def loglik(self, t: Target, changes: Changes) -> float | None:
        """Gaussian log-likelihood of the paper's number under the configuration: a noisy configuration
        spreads its probability, so a precise one equally close is likelier (the honest form of 'prefer
        the precise fit')."""
        x = self._var(t, changes)
        if x is None:
            return None
        m, v = x
        return -0.5 * (t.paper_value - m) ** 2 / v - 0.5 * math.log(2 * math.pi * v)

    def equivalent_configs(self, t: Target, answer: Changes, candidates: list[Changes]) -> list[dict]:
        """The answer and every candidate the target can't tell apart from it: likelihood within
        LL_EQUIVALENT of the answer's, consistent with the paper (implausibility <= 3), and no held-out
        claim worse than at the naive run beyond its noise. The answer first, then fewest knobs."""
        base = self.loglik(t, answer)
        if base is None:
            return []
        held = [h for h in self.targets if h.held_out and not h.tuned_separately and h.metric in self.bands]
        out = [{"config": dict(answer), "loglik": round(base, 3)}]
        for c in candidates:
            if c == answer or len(self.measure_ok(c)) < 2:
                continue
            v, i = self.loglik(t, c), self.implausibility(t, c)
            if v is None or v < base - LL_EQUIVALENT or i is None or i > 3:
                continue
            if any((gh := self.gap(h, c)) is not None and abs(gh) > abs(self.gap(h, {})) + self.band(h)
                   for h in held):
                continue
            out.append({"config": dict(c), "loglik": round(v, 3)})
        return out[:1] + sorted(out[1:], key=lambda e: (len(e["config"]), -e["loglik"]))

    def equivalent_values(self, t: Target, changes: Changes) -> dict[str, list[str]]:
        """For each knob of the answer: every measured value (other knobs held at the answer's values)
        whose target gap is within one noise band of the answer's, and whose held-out claims are no
        worse than at the naive run beyond their noise. Includes the answer's own value."""
        best = self.gap(t, changes)
        if best is None:
            return {}
        band = self.band(t)
        held = [h for h in self.targets if h.held_out and not h.tuned_separately and h.metric in self.bands]
        out: dict[str, list[str]] = {}
        for k, v in changes.items():
            vals = {v}
            for key in self._runs:
                c = dict(key)
                if set(c) != set(changes) or any(c[j] != changes[j] for j in changes if j != k) or c[k] == v:
                    continue
                g = self.gap(t, c)
                if g is None or abs(g) > abs(best) + band:
                    continue
                if any((gh := self.gap(h, c)) is not None and abs(gh) > abs(self.gap(h, {})) + self.band(h)
                       for h in held):
                    continue
                vals.add(c[k])
            out[k] = sorted(vals, key=lambda x: (float(x) if _is_num(x) else float("inf"), x))
        return out

    def _change_size(self, changes: Changes) -> float:
        """How far a configuration moves from the defaults: |log10(value/default)| per numeric knob (both
        positive), 1 per other change. Used only to break ties between equally good fits."""
        import math

        size = 0.0
        for k, v in changes.items():
            d = self.spec.knobs[k].default if k in self.spec.knobs else ""
            try:
                x, y = float(v), float(d)
                size += abs(math.log10(x / y)) if x > 0 and y > 0 else 1.0
            except ValueError:
                size += 1.0
        return size

    def _fill_choices_from_artifact(self) -> None:
        """With the artifact's code on this machine, read argparse choices and multipliers into the knobs."""
        from gapfinder.ingest.repo_map import build_repo_map

        root = self.spec.code_root()  # a local base, or the spec's `source` for an image or checkpoint
        if root is not None:
            from gapfinder.ingest.config_flow import flag_scales

            self._artifact_flags = build_repo_map(root)
            n = fill_choices(self.spec, self._artifact_flags.flags)
            n += mark_multipliers_from_flow(self.spec, flag_scales(root))
            if n:
                mult = [k for k, v in self.spec.knobs.items() if v.multiplier]
                self.orch.events.emit("note", msg=f"value coverage: read choices and multipliers for {n} knob(s) "
                                                  f"from the code (multipliers: {mult or 'none'})")

    def _check_code_defaults(self) -> None:
        """A ledger's code default is the model's reading unless the repo map found the flag (blind-1: the
        repo map read no tf.app.flags, and the guesses were wrong: dropout "0.5" for 0.0). With the code on
        this machine, re-derive each default and its paper-vs-code status from the code. A default the code
        can't confirm is unverified, and can't make a label a paper-artifact inconsistency."""
        self.corrected_defaults: list[dict] = []
        self.unverified_defaults: set[str] = set()
        if self._artifact_flags is None and self.spec.code_root() is not None:
            from gapfinder.ingest.repo_map import build_repo_map

            self._artifact_flags = build_repo_map(self.spec.code_root())
        if self._artifact_flags is None:
            return  # no code here: keep the ledger's reading, as before
        for k, entries in self.all_for.items():
            if k in self.spec_only:
                continue
            flags = [f for f in self._artifact_flags.find_flag(k) if f.default not in (None, "None")]
            fixed = []
            for a in entries:
                if flags:
                    d = flags[0].default
                    status = derive_status(a.paper_value, d, a.status)
                    if (a.code_default, a.status) != (d, status):
                        self.corrected_defaults.append({"knob": k, "ledger": a.code_default, "code": d,
                                                        "at": flags[0].ref, "status": status})
                    a = a.model_copy(update={"code_default": d, "status": status})
                elif a.status == AssumptionStatus.stated_code_differs.value:
                    self.unverified_defaults.add(k)
                fixed.append(a)
            self.all_for[k] = fixed

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
        # only configurations with their confirmation runs (a screen run alone is not a confirmation), in the
        # full search's order. v1.2 sorted every measured configuration by |gap| of its median, which let a
        # noisy closest-by-chance one win (test-v12-08: lr=1 over the true max_steps=100); 7 of 15 v1.2
        # cause runs ended on this path
        everything = [dict(k) for k in self._runs if k and self.value(dict(k), t.metric) is not None]
        measured = [c for c in everything if len(self.measure_ok(c)) >= self.confirm_repeats(t)]
        measured = self._order_candidates(t, measured, res.gap_before)
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
            if best is None or _better(trial, best):
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
        # the closest configuration still short of its confirmation runs, if it is closer than every verified one
        pending = sorted((c for c in everything if len(self.measure_ok(c)) < self.confirm_repeats(t)),
                         key=lambda c: (abs(self.gap(t, c)), len(c), sorted(c.items())))
        unverified = pending[:1] or [c for c in measured[: self.cfg.verify_candidates]
                                     if not any(str(c) in r for r in rejected)]
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


def _is_num(x: str) -> bool:
    try:
        float(x)
        return True
    except ValueError:
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


def _pct(x: float | None) -> str:
    return "n/a" if x is None else f"{x:+.1%}"


def _rank(r: ClaimResult) -> int:
    if not r.attribution:
        return 9
    label = r.attribution.confidence_label
    if label == ConfidenceLabel.fits_but_unsupported.value and not r.closes:
        # it only narrowed the gap and has no evidence: no better than an evidence-backed partial
        # (test-v11-10: a worse-fitting pair with a passenger knob outranked the right single knob)
        return _LABEL_RANK[ConfidenceLabel.partially_explained.value]
    return _LABEL_RANK.get(label, _LABEL_RANK[ConfidenceLabel.unexplained.value])


def _better(a: ClaimResult, b: ClaimResult) -> bool:
    """a beats b: a better label rank, then a closer fit. (Keeping the earlier, smaller-change candidate on a
    tie was tried and lost on the dev suite: among tied fits it prefers the smaller change from the default,
    and the truth is often the larger one, test-v12-01; passenger knobs are handled by the Occam steps.)"""
    ga = abs(a.gap_after) if a.gap_after is not None else float("inf")
    gb = abs(b.gap_after) if b.gap_after is not None else float("inf")
    return (_rank(a), ga) < (_rank(b), gb)
