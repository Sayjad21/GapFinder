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

from pydantic import BaseModel

from gapfinder.ledger.schemas import Assumption, AssumptionStatus, Evidence, Attribution, Branch, BranchStatus, ConfidenceLabel
from gapfinder.models import budget
from gapfinder.sandbox.noise import NoiseBand, bootstrap_diff_ci, mde, noise_band
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.search.bisect import minimal_set
from gapfinder.search.hypotheses import _NUM, _same_number, coverage_values, fill_choices, mark_multipliers_from_flow
from gapfinder.ledger.assumptions import derive_status
from gapfinder.search.verify import Plausibility, gap_returns, held_out_ok, plausible

Changes = dict[str, str]
HM_TIE = 2.0  # history matching: a repeated fit may be named only within this many implausibility units of the best fit
LL_EQUIVALENT = 2.0  # log-likelihood units: within this of the best, the target can't tell two fits apart
_LABEL_RANK = {
    ConfidenceLabel.explained.value: 0,
    ConfidenceLabel.inconsistency.value: 0,
    ConfidenceLabel.reporting_rule.value: 0,
    ConfidenceLabel.fits_but_unsupported.value: 1,
    ConfidenceLabel.stated_value_refuted.value: 1,
    ConfidenceLabel.partially_explained.value: 2,
    ConfidenceLabel.unexplained.value: 3,
}


class _LibraryBudget(RuntimeError):
    """The library probe's share of the run budget is used."""


class RunBudgetExceeded(RuntimeError):
    pass


@dataclass(frozen=True)
class Target:
    """A claim GapFinder can measure: which metric, and the paper's number for it."""

    claim_id: str
    metric: str
    paper_value: float = float("nan")  # a relation claim (below) states a direction, not a number
    held_out: bool = False  # only used to check explanations, never to choose them
    # a held-out row the paper tuned on its own (another method or dataset with its own sweep; blind-1:
    # FastGCN's inductive rows): measured and reported, but one shared setting isn't expected to fit it, so
    # a conflict with it is a note, not a rejection, and it is left out of the joint history-matching fit
    tuned_separately: bool = False
    figure: str | None = None
    # a relation the paper states over a setting: {"knob", "from", "to", "direction": "up"|"down"}, e.g. "the
    # leave-unchanged strategy harms GraphMAE" -> replace_rate 0.0 -> 0.1, down. A candidate under which the
    # relation reverses beyond noise fails like a broken held-out claim; it breaks ties the numbers can't
    relation: dict | None = field(default=None, hash=False, compare=False)
    quote: str | None = None  # e.g. "Figure 6": which experiment's stated settings apply
    # a number the paper reports with some settings fixed (a sensitivity table's cell: RippleNet's AUC at ripple
    # set size 8, {"n_memory": "8"}): a held-out claim measured with these values on top of each configuration.
    # Configurations that fit the target equally well often differ here (plan item 14: identifiability)
    at: dict | None = field(default=None, hash=False, compare=False)


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
    # secant step: where the paper's number lies between two measured values of a numeric knob, interpolate
    # the crossing (log scale for rates, sizes and counts; logit for fractions), snap it to a round value and
    # screen it. Finds a x4 or x25 the fixed ladder never tries. At most this many per knob:
    secant_per_knob: int = 2
    # a confident label needs a complete search: not partial, every knob screened, support beyond code (blind-2)
    complete_for_confidence: bool = True
    # A knob whose stated paper value matches the naive run: True screens it last in the first pass (that cost
    # the dev suite 8 of 10 interaction runs in an ablation: GapBench papers state many values that match);
    # False leaves it out of the first pass and adds it to the fallback round, so it is never dropped for good
    demote_stated: bool = False
    relation_repeats: int = 2  # runs at each end of a relation claim, per candidate checked
    point_repeats: int = 1  # runs of a claim at fixed knob values (Target.at), per configuration checked
    # plan D1.2/D7.1: right after the naive runs, the zero-run reporting rules (best epoch, best validation epoch,
    # best seed...) are scored on every claim; rules that fit them all (each within 2 sigma, at least two claims) and
    # together hold gate_posterior of the posterior, against the numbers as printed, end the search there
    reporting_gate: bool = True
    gate_posterior: float = 0.8
    differential: bool = True  # rank every class's explanations at the end (diagnose.core)
    # plan D2.4: when claims sweep a knob, test "the paper's v is the code's g(v)" (g = c*v, v+c, a percent): one c
    # for every swept point, estimated from the measured curve, then verified by runs at g(v) for every claim
    scale_probe: bool = True
    scale_repeats: int = 2
    # plan D5: mutation-based localisation, when no setting fits every claim or a scale relation needs its code site;
    # at most mutation_max mutants, in three stages (one run each; the best mutation_keep at every claim's condition;
    # the best two repeated), within mutation_budget_frac of the run budget
    mutations: bool = True
    mutation_max: int = 24
    mutation_keep: int = 6
    mutation_budget_frac: float = 0.35
    # plans D1.3-D1.5, D7.2: when the paper-year packages (or the paper-era code) change the numbers, which package
    # (delta debugging), which release or commit (binary search) and which call site (API and source diff); at most
    # library_budget_frac of the run budget; two configurations give "the same numbers" within library_z standard
    # errors on every claim
    library_probe: bool = True
    library_budget_frac: float = 0.25
    library_z: float = 3.0
    # plan D2.2: when configurations fit the target equally well, runs at the paper's other reported conditions
    # (claims at fixed values, other datasets) chosen by expected information per run (gapfinder/diagnose/
    # discriminate.py), in batches, until one holds discriminate_stop of the posterior; within
    # discriminate_budget_frac of the run budget
    discriminate: bool = True
    discriminate_rounds: int = 4
    discriminate_batch: int = 4
    discriminate_stop: float = 0.9
    discriminate_budget_frac: float = 0.15
    max_points: int = 4  # such claims used per search (each costs runs for every configuration checked)
    point_configs: int = 3  # before history matching: the best joint fits also measured at those claims
    # out of space: one Super call compares the paper with the traced run (gapfinder/search/contrast.py);
    # grounded literal differences are tried first in the patch round, structural ones are reported only
    contrast: bool = True
    # with it, a deterministic matcher ($0, search/matcher.py): a setting the paper states, whose name matches no
    # knob, against the code's named literals with the same core words; a differing literal is a patch lead
    match_constants: bool = True
    # with them, grounded operation swaps ($0, search/op_swaps.py): the paper names one operation of a family of
    # drop-in replacements (ELU, mean pooling, min-max scaling, SGD) and the code uses another; tried in the
    # patch round with the paper's choice only
    op_swaps: bool = True
    # protocol tests, after the claims (gapfinder/search/audit.py): code that selects its result by the test score,
    # or edits predictions using the ground truth, is run once more with that logic switched off (an @if patch), so
    # "the reported number depends on this protocol" is measured, not only pointed at. devbatch-2: NCF (best epoch
    # by test HR) and Anomaly Transformer (point adjustment) reproduced their numbers, protocol included.
    protocol_tests: bool = True
    # split variance (Bouthillier et al., MLSys 2021): when the harness has a split or fold seed knob, two more naive
    # runs at other split seeds measure how much the split moves each claim. Reported always; added to the noise
    # band only with split_noise (right when the paper uses random splits, wrong for a fixed split such as Planetoid)
    split_variance: bool = True
    split_noise: bool = False
    protocol_tests_max: int = 3
    protocol_repeats: int = 3
    # also look for a code cause when the answer isn't confident (in space only through settings nothing
    # supports: devset VGAE fitted with hidden2=1600, while the paper states the 10%/5% edge split the code
    # changed): leads, contrast and the patch round run then too, and a patch replaces the answer only if better
    patch_when_unsupported: bool = True
    # ledger names that match no knob are mapped by meaning (one cached Super call), to a knob that exists or to
    # none: a class seen on FastGCN (num_epochs for epochs) and GAT (num_attention_heads, l2_reg_lambda and
    # early_stopping_patience for n_heads, l2_coef and patience), where the paper's own values never became
    # evidence. Grounded: only the spec's knob names are accepted. Skipped without a router or offline.
    semantic_map: bool = True
    # combine in waves, confirming a pair that fits within noise as soon as it appears (anytime budget use)
    early_confirm: bool = True
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
    # at most this share of max_runs goes to the race's first stage (2 runs per survivor); above it, only the
    # strongest survivors race (0 = no cap)
    race_budget_frac: float = 0.25
    race_min: int = 8
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
    relations: dict[str, dict] = field(default_factory=dict)  # relation claim id -> check under the answer
    # every explanation of every class, ranked by the likelihood of all the claims (diagnose.core): the top three are
    # what a person checks first, whatever the headline label
    differential: dict | None = None
    reporting: dict | None = None  # the reporting rule that explains the claims, when one does
    library: dict | None = None  # the library probe: culprit packages, change points, API leads (plan D1.3-D1.5)
    discrimination: dict | None = None  # equally good fits told apart at other conditions (plan D2.2)


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


_NICE = (1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0)


def _snap(x: float, integer: bool, fraction: bool) -> float:
    """A value a person would write: 1, 1.5, 2, 2.5, 3, 4, 5, 6 or 8 times a power of ten (0.0025, 40, 250);
    a fraction to 2 decimals; an integer below 10 to the nearest integer, and always at least 1."""
    if fraction:
        return min(0.99, max(0.01, round(x, 2)))
    if x <= 0:
        return x
    if integer and x < 10:
        return float(max(1, int(x + 0.5)))
    e = math.floor(math.log10(x))
    cands = [m * 10 ** k for k in (e - 1, e, e + 1) for m in _NICE]
    best = min(cands, key=lambda c: abs(math.log(c) - math.log(x)))
    return float(max(1, int(best + 0.5))) if integer else best


def secant_values(points: list[tuple[str, float | None]], target: float, role: str | None, default: str) -> list[str]:
    """Interpolated values where the measured metric crosses the paper's number, between neighbouring measured
    values of one knob: log scale for positive rates, sizes, counts and multipliers, logit for fractions.
    Nearest crossing to the default first."""
    num = []
    for v, y in points:
        try:
            num.append((float(v), y))
        except (TypeError, ValueError):
            return []
    num = [(x, y) for x, y in num if y is not None and math.isfinite(y)]
    if len(num) < 2:
        return []
    integer = re.fullmatch(r"[-+]?\d+", default.strip()) is not None
    fraction = role == "fraction" or (role is None and all(0 < x < 1 for x, _ in num) and not integer)
    if fraction and all(0 < x < 1 for x, _ in num):
        fwd, back = (lambda x: math.log(x / (1 - x))), (lambda u: 1 / (1 + math.exp(-u)))
    elif all(x > 0 for x, _ in num):
        fwd, back = math.log, math.exp
    else:
        fwd, back = (lambda x: x), (lambda u: u)
    pts = sorted((fwd(x), y) for x, y in num)
    d = float(default) if _NUM.fullmatch(default.strip()) else None
    out = []
    for (u1, y1), (u2, y2) in zip(pts, pts[1:]):
        if u1 == u2 or (y1 - target) * (y2 - target) > 0 or y1 == y2:
            continue
        u = u1 + (target - y1) * (u2 - u1) / (y2 - y1)
        x = _snap(back(u), integer, fraction)
        s = str(int(x)) if integer else f"{x:.6g}"
        if s not in out:
            out.append(s)
    if d is not None:  # the crossing nearest the default first

        def dist(s):
            x = float(s)
            return abs(math.log(x / d)) if x > 0 and d > 0 else abs(x - d)
        out.sort(key=dist)
    return out


NAME_MAP_PROMPT = """A paper reading produced setting names that don't match the program's own knob names. For each
reading, name the program knob it refers to, or null if none does. Only use knob names from the list, exactly.
Match by meaning (what the setting controls), not by spelling; when unsure, answer null.

Program knobs:
{knobs}

Readings from the paper:
{items}
"""


class _NameMapping(BaseModel):
    assumption: str
    knob: str | None = None


class NameMap(BaseModel):
    mappings: list[_NameMapping] = []


def ast_patch_is_patch(k: str) -> bool:
    return k.startswith("@ast:")


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


def knob_family(name: str, knobs) -> list[str]:
    """The knobs one program flag was split into: every knob named `<prefix>_<flag>` (`kmeans_synthetic_lmbda`,
    `gat_lr`), when there are at least two and the flag itself is not a knob."""
    flag = _norm_knob(re.sub(r"^(?:[A-Za-z_]\w*\.)+", "", re.sub(r"\s*\(.*$", "", name.strip())).replace(" ", "_"))
    if not flag or flag in {_norm_knob(k) for k in knobs}:
        return []
    fam = [k for k in knobs if _norm_knob(k).endswith("_" + flag)]
    return sorted(fam) if len(fam) >= 2 else []


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
        self.relations = [t for t in targets if t.relation]  # checked under candidates, never explained
        # claims at fixed knob values, checked under candidates like held-outs, never explained
        self.points = [t for t in targets if t.at and not t.relation][: (cfg or SearchConfig()).max_points]
        conditions = {k for k, kn in orch.spec.knobs.items() if kn.condition}
        if conditions:  # the dataset or a sweep's axis is set by the claims at fixed values, never searched (D2.1)
            assumptions = [a for a in assumptions if a.knob not in conditions]
        targets = [t for t in targets if not t.relation and not t.at]
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
        self._stated_skipped: set[str] = set()  # stated and matching the naive run: out of the first pass
        self._include_stated = False  # the fallback round brings them back
        self.audit_report: dict | None = None  # gapfinder/search/audit.py, after the claims
        self.protocol_results: list[dict] = []
        self.split_report: dict[str, dict] = {}  # claim -> noise band across seeds, and across seeds and splits
        self.differentials: dict = {}  # claim id -> diagnose.Differential
        self.scale_relations: list[dict] = []  # verified "the code's knob is g(the paper's)" (feeds the mutation round)
        self.code_leads: dict[str, list[dict]] = {}  # claim id -> the mutation round's fitting groups
        self._library_out: dict[str, dict] = {}  # claim id -> the library probe's findings and notes  # protocol tests: a selection or label edit, switched off and measured
        self.trace_records: list[dict] = []  # the raw dry-run records (for the paper-to-trace contrast)
        self.paper_text = paper_text
        if self.cfg.coverage and self.spec.code_root() is not None:  # a local base, or the spec's `source`
            self._fill_choices_from_artifact()
        # assumption -> spec knob; assumptions about knobs the harness can't set are skipped (and reported)
        self.assumptions: dict[str, Assumption] = {}
        self.all_for: dict[str, list[Assumption]] = {}  # every ledger entry per knob (papers state some twice)
        self.unmapped: list[str] = []
        self.renamed: dict[str, str] = {}  # ledger name -> spec knob, when they differ (`num_epochs` -> `epochs`)
        self._unmapped_assumptions: list[Assumption] = []
        for a in sorted(assumptions, key=lambda a: -a.prior_score):
            k = map_knob_name(a.knob, self.spec.knobs)
            if k is None and (family := knob_family(a.knob, self.spec.knobs)):
                # one program flag run as several knobs (batch-3 b3a: `--lmbda` as kmeans_synthetic_lmbda, ...; PyG:
                # `--lr` as gat_lr and gcn_lr): the paper's reading of the flag applies to each of them
                for k2 in family:
                    self.renamed.setdefault(a.knob, ", ".join(family))
                    self.all_for.setdefault(k2, []).append(a.model_copy(update={"knob": k2}))
                continue
            if k is None:
                self.unmapped.append(a.knob)
                self._unmapped_assumptions.append(a)
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
        # a precise candidate is judged by its own (narrower) band; a noisy one never gets a wider band than the
        # naive run's, or a scattered configuration could "close" the gap by its spread alone (planted pygcn
        # hidden=4: runs from 56 to 76; GapBench test-v11-01: max_steps=2000 with a spread of 147)
        return min(own, self.band(t))

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
        if self.cfg.split_variance:
            await self._split_variance(runs)

    async def _split_variance(self, runs: list[Branch]) -> None:
        """Two naive runs at other values of the harness's split or fold seed knob: the claims' spread across
        splits, against their spread across seeds alone. The name must say it is a seed or an index (data_seed,
        split_seed, fold_idx): a bare `split` or `fold` is as often a fraction or a mode (dev suite run 4000).
        The runs are measurements, not candidates: they are kept out of the search's configurations, or a lucky
        split could be reported as the explanation."""
        knob = next((k for k, kn in self.spec.knobs.items()
                     if re.fullmatch(r"(?i)(split|fold|data|partition|cv|kfold)_?(seed|idx|index|id|num|no)", k)
                     and re.fullmatch(r"\d+", str(kn.default).strip())), None)
        if knob is None:
            return
        d = int(self.spec.knobs[knob].default)
        others = [{knob: str(d + 1)}, {knob: str(d + 2)}]
        if self.cfg.max_runs is not None and self.runs_used + len(others) > self.cfg.max_runs:
            return
        try:
            self.runs_used += len(others)
            extra = await self.orch.fanout(others, ["noise (split)"] * len(others))
        except budget.BudgetExceeded:
            return
        self.split_report = {}
        for t in self.targets:
            seed_vals = [b.parsed_metrics[t.metric] for b in runs if t.metric in b.parsed_metrics]
            split_vals = seed_vals + [b.parsed_metrics[t.metric] for b in extra
                                      if b.status == BranchStatus.succeeded and t.metric in b.parsed_metrics]
            if len(split_vals) <= len(seed_vals):
                continue
            # a plain spread, not the median-based band: two split runs among five seed runs are exactly what a
            # robust estimator discounts
            seed_band = self.bands[t.metric].band
            both = max(seed_band, 2 * statistics.pstdev(split_vals))
            self.split_report[t.claim_id] = {"seed_band": seed_band, "seed_and_split_band": both}
            if self.cfg.split_noise and both > seed_band:
                nb = self.bands[t.metric]
                self.bands[t.metric] = NoiseBand(**{**nb.to_dict(), "band": both})
        widest = max(self.split_report.items(), key=lambda kv: kv[1]["seed_and_split_band"] / max(kv[1]["seed_band"], 1e-12),
                     default=None)
        if widest:
            cid, r = widest
            self.orch.events.emit("note", msg=f"split variance ({knob} at {d + 1}, {d + 2}): {cid}'s band is "
                                              f"{r['seed_band']:.3g} across seeds, {r['seed_and_split_band']:.3g} with "
                                              "the split varied too" + (" (used)" if self.cfg.split_noise else
                                                                         " (reported only)"))

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
        if self.cfg.semantic_map:
            await self._map_names()
        await self.calibrate()
        results = []
        for t in self.targets:
            if not t.held_out:
                results.append(await self.explain(t))
        if self.cfg.protocol_tests:
            try:
                await self._protocol_tests()
            except budget.BudgetExceeded:
                raise
            except Exception as exc:  # an aid: a failure leaves the claims' results as they are
                self.orch.events.emit("note", msg=f"protocol tests: skipped ({type(exc).__name__}: {str(exc)[:160]})")
        # what a matching number doesn't show (devbatch-2: three reproduced targets, three silent reports)
        from gapfinder.search.audit import audit
        try:
            self.audit_report = audit(self, results)
        except Exception as exc:  # an aid: a failure leaves the report as it was
            self.audit_report = None
            self.orch.events.emit("note", msg=f"audit: skipped ({type(exc).__name__}: {str(exc)[:160]})")
        return results

    def _alternative_configs(self, max_configs: int = 3) -> list[Changes]:
        """Settings the repo declares a second time with other values, as whole configurations: a flag block that
        sits again elsewhere in the code (batch-4 RippleNet: a commented-out argparse block "default settings for
        Book-Crossing" in src/main.py, with lr 1e-3 and l2_weight 1e-5, while the active defaults are MovieLens').
        One block is one configuration: its settings may only work together (l2_weight alone did nothing there)."""
        if getattr(self, "_alt_configs", None) is not None:
            return self._alt_configs
        self._alt_configs = []
        flags = getattr(self._artifact_flags, "flags", None) or []
        blocks: dict[tuple[str, int], dict[str, str]] = {}
        where: dict[tuple[str, int], str] = {}
        for f in flags:
            k = map_knob_name(f.name, self.spec.knobs)
            if k is None or f.default in (None, "None") or ast_patch_is_patch(k):
                continue
            if _same_value(str(f.default), self.spec.knobs[k].default):
                continue  # the declaration the harness runs (or one that agrees with it)
            others = [g for g in flags if g.name == f.name and g.file == f.file and g.line != f.line]
            if not others:
                continue  # declared once: the spec's default comes from elsewhere, not an alternative block
            key = (f.file, f.line // 40)  # declarations within a few dozen lines form one block
            blocks.setdefault(key, {})[k] = str(f.default)
            where.setdefault(key, f"{f.file}:{f.line}")
        for key, c in sorted(blocks.items(), key=lambda kv: -len(kv[1]))[:max_configs]:
            self._alt_configs.append(c)
            self.orch.events.emit("note", msg=f"alternative settings declared in the repo at {where[key]}: "
                                              + ", ".join(f"{k}={v}" for k, v in sorted(c.items()))
                                              + " (tested together in the combine round)")
        return self._alt_configs

    def _race_cap(self, extra: int) -> int:
        """How many screen survivors the confirmation race can take without crowding out the combine round."""
        if not self.cfg.race_budget_frac or not self.cfg.max_runs:
            return 0
        return max(self.cfg.race_min, int(self.cfg.max_runs * self.cfg.race_budget_frac / (2 + extra)))

    def _refuted_label(self, t: Target, res: ClaimResult) -> None:
        """"Fits but unsupported" becomes "Paper's stated value refuted; unique fit" only when every one holds:
        - the search finished, and every knob with candidate values was screened;
        - the answer closes the target, passes the counterfactual, and fits every claim (at least two, none of
          them tuned separately) jointly in history matching;
        - history matching finds a single island of fits (no other explanation);
        - for a changed knob, the paper states another value, and that value was run and is implausible (> 3)."""
        a = res.attribution
        if a is None or a.confidence_label != ConfidenceLabel.fits_but_unsupported.value or res.status == "partial":
            return
        if not self.closes(t, res.changes) or a.counterfactual_ok is not True:
            return
        claims = [t] + [h for h in self.targets if h.held_out and not getattr(h, "tuned_separately", False)
                        and not getattr(h, "relation", None) and h.metric in self.bands]
        if len(claims) < 2:
            return
        d = res.diagnosis or {}
        joint = d.get("joint") or []
        if len(d.get("islands") or []) != 1:
            return
        if not any(j["config"] == res.changes and max(j["I"].values()) <= 2 for j in joint):
            return
        knobs_with_values = {h.knob for h in self.hypotheses()}
        screened = {next(iter(k))[0] for k in self._runs if len(k) == 1 and self.measure_ok(dict(k))}
        if knobs_with_values - screened:
            return
        refuted = []
        for k, v in res.changes.items():
            for sv in self._stated_values(k):
                m = _NUM.search(str(sv))
                if m is None or _same_value(m.group(0), v):
                    continue
                at = {} if _same_value(m.group(0), self.spec.knobs[k].default) else {k: m.group(0)}
                worst = [self.implausibility(c, at) for c in claims]
                if all(x is not None for x in worst) and max(worst) > 3:
                    refuted.append(f"{k} = {m.group(0)} (implausibility {max(worst):.1f})")
        if not refuted:
            return
        res.attribution = a.model_copy(update={"confidence_label": ConfidenceLabel.stated_value_refuted.value})
        res.notes.append("labelled Paper's stated value refuted; unique fit: the paper's " + "; ".join(refuted)
                         + f" was run and doesn't fit the claims, while {dict(res.changes)} fits all "
                         f"{len(claims)} and is the only island of fits")

    def _stated_value_notes(self, res: ClaimResult) -> None:
        """When the answer changes a knob whose value the paper states, and the stated value itself was run and
        doesn't fit, say so: the paper's stated value is likely not the one behind its numbers (batch-3 b3a: the
        paper says lambda = 10 for Synthetic; the code's 10 gives balance 0.5, and 100 gives the paper's 1.00)."""
        for k, v in (res.changes or {}).items():
            a = self.assumptions.get(k)
            if a is None or str(a.paper_value).strip().lower().startswith("unstated"):
                continue
            stated = next((x for x in self._stated_values(k) if not _same_value(x, v)), None)
            if stated is None:
                continue
            at = {} if _same_value(stated, self.spec.knobs[k].default) else {k: stated}
            g = self.gap(res.target, at)
            if g is None or abs(g) <= self.band_at(res.target, at):
                continue  # the stated value wasn't measured, or it fits too
            q = next((e.quote for e in a.evidence if e.kind == "paper" and e.quote), "")
            res.notes.append(f"the paper states {k} = {stated}" + (f' ("{q[:140]}")' if q else "")
                             + f", but {stated} leaves the gap at {g:+.1%} (beyond noise); {v} closes it: the stated "
                             "value is likely not the one behind the paper's numbers")

    async def _protocol_tests(self) -> None:
        """Each code lead that selects by the test score or edits predictions with the labels, switched off and
        measured: every claim's naive value against its value without that logic, with a bootstrap interval."""
        root = self.spec.code_root()
        if root is None:
            return
        from gapfinder.ingest.code_checks import code_checks
        from gapfinder.sandbox import ast_patch
        from gapfinder.sandbox.spec import Knob

        leads = [x for x in code_checks(root, set(self.spec.knobs), limit=80)
                 if ((x.family in ("selection_in_code", "label_in_prediction") and x.name == "@if")
                     or (x.family == "eval_switch" and x.name and x.value))
                 and (not ast_patch.entry_script(root / x.file) or ast_patch.direct_entry(self.spec.run.command, x.file))]
        leads = leads[: self.cfg.protocol_tests_max]
        for x in leads:
            k = ast_patch.knob_name(x.file, x.line, x.name)
            self.spec.knobs.setdefault(k, Knob(layer="environment", default="as written", env=True))
            try:
                await self.measure({k: x.value}, self.cfg.protocol_repeats, "protocol test")
            except RunBudgetExceeded as exc:
                self.orch.events.emit("note", msg=f"protocol tests: run budget reached before {x.file}:{x.line} ({exc})")
                break
            claims = []
            for t in self.targets:
                if getattr(t, "relation", None) or t.metric not in self.bands:
                    continue
                v = self.value({k: x.value}, t.metric)
                if v is None:
                    continue
                base = [b.parsed_metrics[t.metric] for b in self.measure_ok({}) if t.metric in b.parsed_metrics]
                cand = [b.parsed_metrics[t.metric] for b in self.measure_ok({k: x.value}) if t.metric in b.parsed_metrics]
                ci = bootstrap_diff_ci(base, cand, alpha=0.05) if len(base) >= 2 and len(cand) >= 2 else None
                claims.append({"claim": t.claim_id, "metric": t.metric, "paper": t.paper_value,
                               "naive": self.naive.get(t.metric), "without": v,
                               "ci": list(ci) if ci else None, "held_out": t.held_out,
                               "depends": bool(ci and (ci[0] > 0 or ci[1] < 0))})
            runs = self.measure_ok({k: x.value})
            failed = [b for b in self._runs.get(frozenset({k: x.value}.items()), []) if b.status != BranchStatus.succeeded]
            self.protocol_results.append({"failed": len(failed), "failure": (failed[0].note or "")[-300:] if failed else "","family": x.family, "file": x.file, "line": x.line, "code": x.code,
                                          "detail": x.detail, "knob": k, "value": x.value, "runs": len(runs),
                                          "claims": claims})
            moved = [c for c in claims if c["depends"]]
            self.orch.events.emit("note", msg=f"protocol test {x.file}:{x.line} ({x.family}) switched off: "
                                              + ("; ".join(f"{c['metric']} {c['naive']:.4g} -> {c['without']:.4g}"
                                                           for c in moved) if moved else "no claim moved beyond noise"))

    async def _map_names(self) -> None:
        """Map unmatched ledger names to the spec's knobs by meaning, then absorb those assumptions."""
        pending = [a for a in self._unmapped_assumptions if a.knob in self.unmapped]
        if not pending or self.router is None:
            return
        knobs = []
        for k, kn in self.spec.knobs.items():
            if ast_patch_is_patch(k):
                continue
            role = f", role {kn.role}" if kn.role else ""
            knobs.append(f"- {k} (default {kn.default}{role})")
        items = []
        for a in pending:
            q = next((e.quote for e in a.evidence if e.kind == "paper"), "")
            items.append(f"- {a.knob}: paper value {a.paper_value!r}; code default {a.code_default!r}"
                         + (f'; paper says "{q[:160]}"' if q else ""))
        msg = NAME_MAP_PROMPT.format(knobs="\n".join(knobs), items="\n".join(items))
        try:
            out = await self.router.structured("super", [{"role": "user", "content": msg}], NameMap)
        except budget.BudgetExceeded:
            raise
        except Exception as exc:  # offline, cache-only, or a malformed answer: keep the names as they were
            self.orch.events.emit("note", msg=f"knob-name mapping skipped ({type(exc).__name__}: {str(exc)[:120]})")
            return
        by_name = {a.knob: a for a in pending}
        mapped = {}
        for m in out.mappings:
            if m.assumption in by_name and m.knob and m.knob in self.spec.knobs and not ast_patch_is_patch(m.knob):
                mapped[m.assumption] = m.knob
        for name, k in mapped.items():
            self._absorb(by_name[name].model_copy(update={"knob": k}), k)
            self.renamed[name] = k
            self.unmapped = [u for u in self.unmapped if u != name]
        if mapped:
            self.orch.events.emit("note", msg="knob names mapped by meaning: "
                                              + ", ".join(f"{a} -> {k}" for a, k in mapped.items()))

    def _absorb(self, a: Assumption, k: str) -> None:
        """Add a ledger assumption to knob k: merged into its entry, or promoted from the fallback list."""
        if k in self._fallback:  # a spec-only knob now has a ledger reading: it joins the first pass
            self._fallback.pop(k)
            self.spec_only = [x for x in self.spec_only if x != k]
            self.all_for[k] = []
        self.all_for.setdefault(k, []).append(a)
        self.all_for[k].sort(key=lambda x: -x.prior_score)
        self._check_code_defaults()
        entries = self.all_for[k]
        head = entries[0]
        self.assumptions[k] = head.model_copy(update={
            "evidence": [e for x in entries for e in x.evidence],
            "candidate_values": list(dict.fromkeys(str(v) for x in entries for v in x.candidate_values))})

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
        self.trace_report, self.trace_records = rep, recs
        changed = apply_roles(self.spec, rep)
        self.orch.events.emit("trace", **rep.to_dict(), applied=changed)
        self.orch.events.emit("note", msg="trace: " + rep.summary())

    def hypotheses(self) -> list[Hypothesis]:
        """One hypothesis per (knob, candidate value). A knob whose value the paper states and the
        code already uses can't cause the gap (the naive run already matches the paper there)."""
        out = []
        open_knobs = []
        last = []  # stated by the paper and matching the naive run: screened last, never dropped (blind-2)
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
                # the ledger's stated value may be wrong (blind-2: it wrote alpha_l's code default, 2, as the
                # paper's value, and the true cause was dropped before a single run): demote, don't drop
                if self.cfg.demote_stated:
                    last.append((k, a, stated))
                elif not self._include_stated:
                    self._stated_skipped.add(k)  # tested in the fallback round if the first pass isn't confident
                else:
                    last.append((k, a, stated))
                continue
            open_knobs.append((k, a, stated))
        open_knobs += last
        rng = random.Random(self.cfg.seed)
        if self.cfg.rank == "random":
            rng.shuffle(open_knobs)  # the top-k cut must not keep the ledger's favourites
        for knob, a, stated in open_knobs[: self.cfg.screen_top_k]:
            spec_knob = self.spec.knobs[knob]
            default = spec_knob.default
            # the default itself is the naive run, in any spelling ("0" for 0.0: test-v11-01 proposed init_q=0)
            # ...and in any case: "False" is the default false (blind-2 spent screen runs on deg4feat=False)
            is_default = lambda v: _same_value(str(v), default)  # noqa: E731
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
        gate = self._calibration_gate(t, res)
        if gate is not None:
            self.orch.events.emit("attribution", claim=t.claim_id, status=gate.status,
                                  label=gate.attribution.confidence_label, changes={}, gap_before=g0,
                                  gap_after=gate.gap_after, reporting=gate.reporting["rule"])
            return gate
        if self.cfg.library_probe:
            # before the settings search: a release-localised library effect is evidence for the paper-year knob
            # (the paper predates the release that changed the numbers), which the search's labels then use
            lib_out: dict = {"notes": []}
            try:
                await self._library_probe(t, lib_out)
                await self._era_probe(t, lib_out)
            except (RunBudgetExceeded, budget.BudgetExceeded, _LibraryBudget) as exc:
                lib_out["notes"].append(f"library probe stopped early: {exc}")
            self._library_out[t.claim_id] = lib_out
        tried: set[frozenset] = set()
        try:
            await self._search(t, res, tried)
        except (RunBudgetExceeded, budget.BudgetExceeded) as exc:
            res.status = "partial"
            res.notes.append(f"stopped early: {exc}")
            await self._label_partial(t, res)
        confident = {ConfidenceLabel.explained.value, ConfidenceLabel.inconsistency.value}
        if (self._fallback or (self._stated_skipped and not self._include_stated)) and not (
                res.attribution and res.attribution.confidence_label in confident):
            await self._spec_knob_round(t, res, tried)
        self._cap_confidence(t, res)
        res.hypotheses_tested = len(tried)
        if self.cfg.mde_inconclusive:
            self._mde_check(t, res)
        if self.cfg.history_matching:
            if self._usable_points():
                await self._points_for_fits(t, res)
                try:
                    await self._discriminate(t, res)
                except (RunBudgetExceeded, budget.BudgetExceeded) as exc:
                    res.notes.append(f"discrimination stopped early: {exc}")
            self._history_match(t, res)
            if self._usable_points():
                await self._scale_probe(t, res)
            if self.cfg.patch_knobs and self._wants_patch(res):
                await self._contrast(res)
                self._match_constants(res)
                self._match_ops(res)
                try:
                    await self._patch_round(t, res)
                except (RunBudgetExceeded, budget.BudgetExceeded) as exc:
                    res.notes.append(f"patch round stopped early: {exc}")
        if self.cfg.history_matching and self.cfg.mutations:
            try:
                await self._mutation_round(t, res)
            except (RunBudgetExceeded, budget.BudgetExceeded) as exc:
                res.notes.append(f"mutation round stopped early: {exc}")
        self._refuted_label(t, res)
        if res.attribution is not None:
            res.attribution.hypotheses_tested = len(tried)
        lib_out = self._library_out.get(t.claim_id)
        if lib_out:  # kept outside `res`: the spec-knob round may replace res's fields
            res.notes += [n for n in lib_out["notes"] if n not in res.notes]
            body = {k: v for k, v in lib_out.items() if k != "notes"}
            res.library = body or None
        self._stated_value_notes(res)
        self._finish_differential(t, res)
        self.orch.events.emit("attribution", claim=t.claim_id, status=res.status,
                              label=res.attribution.confidence_label if res.attribution else None,
                              changes=res.changes, gap_before=g0, gap_after=res.gap_after)
        return res

    # ------------------------------------------------------------ the differential (plan D1)
    def _diag_claims(self, t: Target) -> list[Target]:
        return [t] + [h for h in self.targets if h.held_out and not h.tuned_separately and h.claim_id != t.claim_id
                      and h.metric in self.bands]

    def _new_differential(self, t: Target):
        from gapfinder.diagnose import ClaimSpec, Differential

        naive = self.measure_ok({})
        specs = []
        for c in self._diag_claims(t):
            vals = [b.parsed_metrics[c.metric] for b in naive if c.metric in b.parsed_metrics]
            if len(vals) < 2:
                continue
            sd = max(statistics.stdev(vals), self.cfg.noise_floor_frac * abs(c.paper_value))
            specs.append(ClaimSpec(c.claim_id, c.metric, c.paper_value, statistics.fmean(vals), sd, target=c is t))
        return Differential(specs, paper_n=self.cfg.hm_paper_n, disc=self.cfg.hm_disc)

    def _add_point_claims(self, diff) -> None:
        """The claims at fixed knob values (Target.at) join the differential once their naive runs exist."""
        from gapfinder.diagnose import ClaimSpec

        for p in self._usable_points():
            if p.claim_id in diff.claims:
                continue
            vals = [b.parsed_metrics[p.metric] for b in self.measure_ok(self._point_config(p, {}))
                    if p.metric in b.parsed_metrics]
            if not vals:
                continue
            sd = max(statistics.stdev(vals) if len(vals) >= 2 else 0.0, self.bands[p.metric].band / 2,
                     self.cfg.noise_floor_frac * abs(p.paper_value))
            diff.claims[p.claim_id] = ClaimSpec(p.claim_id, p.metric, p.paper_value, statistics.fmean(vals), sd)
        for h in diff.hypotheses.values():  # rescored on the larger claim set
            diff.score(h)
        diff._normalise()

    def _config_hypothesis(self, diff, changes: Changes, prior: float, title: str | None = None,
                           cls: str | None = None):
        """A configuration as a hypothesis: its measured values on every claim (claims it wasn't measured on keep
        the naive prediction)."""
        from gapfinder.diagnose import Hypothesis, Prediction
        from gapfinder.sandbox import ast_patch

        preds = {}
        points = {p.claim_id: p for p in self.points}
        for cid, c in diff.claims.items():
            at = self._point_config(points[cid], changes) if cid in points else changes  # a claim at a fixed value
            vals = [b.parsed_metrics[c.metric] for b in self.measure_ok(at) if c.metric in b.parsed_metrics]
            if vals:
                preds[cid] = Prediction.from_values(vals, c.naive_sd)
        code = any(ast_patch.is_patch(k) for k in changes)
        cfg = ", ".join(f"{k}={v}" for k, v in sorted(changes.items()))
        if cls is None:
            from gapfinder import env_year

            cls = "code" if code else "library" if set(changes) & {env_year.KNOB, env_year.ERA_KNOB} else "settings"
        return Hypothesis(f"{cls}:" + cfg, cls,
                          title or (f"a code change: {cfg}" if code else f"the setting {cfg}"), prior, preds,
                          detail={"changes": dict(changes)}, runs=len(self.measure_ok(changes)),
                          check=f"run with {cfg}" + (" (an in-memory code patch)" if code else ""))

    def _calibration_gate(self, t: Target, res: ClaimResult) -> ClaimResult | None:
        """The zero-run reporting rules, right after the naive runs: does a different reading of the same runs fit
        every claim? If so the settings search is not needed (b5b-type papers: the best epoch, 40 minutes a run)."""
        if not self.cfg.reporting_gate:
            return None
        from gapfinder.diagnose import FIT_I, STRICT_I, Hypothesis, Prediction
        from gapfinder.diagnose.reporting import reporting_hypotheses

        diff = self._new_differential(t)
        if t.claim_id not in diff.claims:
            return None
        self.differentials[t.claim_id] = diff
        as_run = Hypothesis("as-run", "settings", "no difference in reporting: the numbers as printed at the end of the "
                            "run", 0.3, {cid: Prediction(c.naive_mean, c.naive_sd, len(self.measure_ok({})))
                                         for cid, c in diff.claims.items()},
                            check="the settings search and the other classes")
        diff.add(as_run)
        hyps = reporting_hypotheses(self.measure_ok({}), [(c.claim_id, c.metric, c.target) for c in diff.claims.values()],
                                    {cid: c.naive_sd for cid, c in diff.claims.items()})
        for h in hyps:
            diff.add(h)
        if not hyps:
            return None
        self.orch.events.emit("note", msg=f"{t.claim_id}: reporting rules scored on {len(diff.claims)} claim(s): "
                                          + "; ".join(f"{h.detail['rule']} (worst {h.max_I:.1f} sigma, "
                                                      f"{h.posterior:.0%})" for h in hyps))
        fitting = [h for h in hyps if h.max_I <= STRICT_I and len(h.predictions) == len(diff.claims)]
        mass = sum(h.posterior for h in fitting)
        # the comparison decides (the rules against the numbers as printed, in the posterior); the as-printed numbers
        # fitting every claim would leave nothing to explain
        if len(diff.claims) < 2 or not fitting or as_run.fits_all or mass < self.cfg.gate_posterior:
            return None
        top = max(fitting, key=lambda h: h.posterior)
        pred = top.per_claim[t.claim_id]["pred"]
        res.gap_after = (pred - t.paper_value) / abs(t.paper_value)
        res.closes = True
        res.attribution = self._attribution(t, {}, res.gap_after, ConfidenceLabel.reporting_rule, [])
        flaws = {h.detail["flaw"] for h in fitting}
        res.reporting = {"rule": top.detail["rule"], "title": top.title, "flaw": top.detail["flaw"],
                         "equivalent": [h.detail["rule"] for h in fitting if h is not top],
                         "statistics": top.detail["statistics"], "posterior": round(mass, 3),
                         "per_claim": {cid: {"paper": v["paper"], "pred": v["pred"], "I": round(v["I"], 2)}
                                       for cid, v in top.per_claim.items()}}
        for cid, v in top.per_claim.items():
            if cid != t.claim_id:
                c = diff.claims[cid]
                res.held_out[cid] = {"gap_before": (c.naive_mean - c.paper) / abs(c.paper),
                                     "gap_after": (v["pred"] - c.paper) / abs(c.paper), "ok": v["I"] <= FIT_I}
        fits = ", ".join("%s %.4g vs %.4g" % (cid, v["pred"], v["paper"]) for cid, v in top.per_claim.items())
        res.notes.append(f"{top.title}: every claim fits within {STRICT_I:g} sigma under this reading of the naive "
                         f"runs ({fits}), "
                         f"while the numbers as printed at the end miss the target by "
                         f"{as_run.per_claim[t.claim_id]['I']:.1f} sigma; no settings search was needed")
        if len(fitting) > 1:
            res.notes.append("equally good readings: " + "; ".join(h.title for h in fitting if h is not top))
        if top.detail["flaw"]:
            res.notes.append("a flaw in the paper's evaluation, not a reproduction error"
                             + (" (or a legitimate protocol: the fitting rules include both)" if len(flaws) > 1 else ""))
        res.differential = diff.to_dict()
        return res

    def _finish_differential(self, t: Target, res: ClaimResult) -> None:
        """Every class's explanations on one scale at the end: the reporting rules (scored after the naive runs),
        the settings search's answer and its equally good configurations, history matching's joint fits, and the
        patch round's code changes."""
        if not self.cfg.differential:
            return
        diff = self.differentials.get(t.claim_id) or self._new_differential(t)
        if t.claim_id not in diff.claims:
            return
        self.differentials[t.claim_id] = diff
        configs = []
        if res.changes:
            configs.append(dict(res.changes))
        configs += [dict(e["config"]) for e in res.equivalent if e.get("config")]
        configs += [dict(j["config"]) for j in (res.diagnosis or {}).get("joint") or [] if j.get("config")]
        seen = set()
        for i, c in enumerate(configs):
            key = frozenset(c.items())
            if key in seen or not self.measure_ok(c):
                continue
            seen.add(key)
            diff.add(self._config_hypothesis(diff, c, prior=0.15 if i == 0 else 0.05))
            if len(seen) >= 8:
                break
        res.differential = diff.to_dict()

    def _point_config(self, p: Target, changes: Changes) -> Changes:
        """`changes` with the claim's fixed values on top (a value equal to the default is left out)."""
        c = dict(changes)
        for k, v in (p.at or {}).items():
            if _same_value(str(v), self.spec.knobs[k].default):
                c.pop(k, None)
            else:
                c[k] = str(v)
        return c

    def _usable_points(self) -> list[Target]:
        return [p for p in self.points if p.metric in self.bands and set(p.at or {}) <= set(self.spec.knobs)]

    async def _measure_points(self, configs: list[Changes], label: str = "point") -> None:
        """Every usable fixed-value claim under each configuration (and the naive one), point_repeats runs each.
        Out of budget it measures what it can."""
        cs = [{}] + [c for c in configs if c]
        try:
            await _all(*(self.measure(self._point_config(p, c), self.cfg.point_repeats, f"{label} {p.claim_id}")
                         for p in self._usable_points() for c in cs))
        except (RunBudgetExceeded, budget.BudgetExceeded):
            pass

    # ------------------------------------------------------------ scale conventions (plan D2.4)
    SCALE_FACTORS = (0.1, 0.2, 0.25, 1 / 3, 0.5, 2 / 3, 1.5, 2.0, 3.0, 4.0, 5.0, 10.0)  # c in "code = c x paper"
    UNIT_FACTORS = (0.01, 100.0)  # a percent against a fraction
    OFFSETS = (-1.0, 1.0)  # off by one (an epoch, a layer, a hop counted from 0 or 1)

    def _curve(self, knob: str, metric: str) -> dict[float, tuple[float, int]]:
        """value of the knob -> (median of the metric, runs) over the measured configurations that change only it."""
        out = {}
        d = _num(self.spec.knobs[knob].default)
        for key, branches in self._runs.items():
            cfg = dict(key)
            if set(cfg) - {knob}:
                continue
            v = d if not cfg else _num(cfg[knob])
            vals = [b.parsed_metrics[metric] for b in branches if b.status == BranchStatus.succeeded
                    and metric in (b.parsed_metrics or {})]
            if v is not None and vals:
                out[v] = (statistics.median(vals), len(vals))
        return out

    @staticmethod
    def _interp(curve: dict[float, tuple[float, int]], x: float, extrapolate: float = 0.5) -> float | None:
        """The measured curve at x: linear between measured points, and linear beyond the ends up to `extrapolate` x
        the measured span (a screening estimate only: the scale probe's verification runs decide)."""
        xs = sorted(curve)
        if len(xs) < 2:
            return curve[xs[0]][0] if xs and abs(x - xs[0]) < 1e-12 else None
        span = xs[-1] - xs[0]
        if x < xs[0] - extrapolate * span - 1e-12 or x > xs[-1] + extrapolate * span + 1e-12:
            return None
        if x <= xs[0]:
            a, b = xs[0], xs[1]
        elif x >= xs[-1]:
            a, b = xs[-2], xs[-1]
        else:
            a, b = next((a, b) for a, b in zip(xs, xs[1:]) if a - 1e-12 <= x <= b + 1e-12)
        ya, yb = curve[a][0], curve[b][0]
        return ya if b == a else ya + (yb - ya) * (x - a) / (b - a)

    @staticmethod
    def _snap_value(v: float, like: str) -> str:
        """A knob value written like the default (an integer stays an integer)."""
        if re.fullmatch(r"[-+]?\d+", like.strip()) and abs(v - round(v)) < 1e-9:
            return str(int(round(v)))
        return f"{v:.6g}"

    async def _scale_probe(self, t: Target, res: ClaimResult) -> None:
        """Claims that sweep one knob (the target at its default, the others at fixed values): is the paper's knob a
        rescaled version of the code's? The factor is the one meaningful value (2, 1/2, 10, 100, +-1...) that makes the
        measured curve match every swept claim; it is then verified by running the code at g(v) for every claim.
        A setting's unit or convention differing between paper and code (an edge counted twice, a percent against a
        fraction, an epoch counted from 0) is a paper-code inconsistency the plain value search cannot express."""
        if not self.cfg.scale_probe:
            return
        from gapfinder.diagnose import FIT_I, STRICT_I

        by_knob: dict[str, list[Target]] = {}
        for p in self._usable_points():
            if len(p.at) == 1 and p.metric == t.metric:
                by_knob.setdefault(next(iter(p.at)), []).append(p)
        await self._measure_points([])  # the naive run at every point's value: the code's curve
        diff = self.differentials.get(t.claim_id) or self._new_differential(t)
        self.differentials[t.claim_id] = diff
        self._add_point_claims(diff)
        for knob, pts in by_knob.items():
            v0 = _num(self.spec.knobs[knob].default)
            if len(pts) < 2 or v0 is None:
                continue
            sweep = [(v0, t.paper_value, t)] + [(_num(p.at[knob]), p.paper_value, p) for p in pts]
            if any(v is None for v, _, _ in sweep):
                continue
            curve = self._curve(knob, t.metric)
            if len(curve) < 3:
                continue
            sd = max(self.bands[t.metric].band / 2, self.cfg.noise_floor_frac * abs(t.paper_value))
            fams = ([("x", c) for c in self.SCALE_FACTORS] + [("x", c) for c in self.UNIT_FACTORS]
                    + [("+", c) for c in self.OFFSETS])
            scored = []
            for fam, c in fams:
                g = (lambda v, c=c: v * c) if fam == "x" else (lambda v, c=c: v + c)
                preds = [self._interp(curve, g(v)) for v, _, _ in sweep]
                if any(y is None for y in preds):
                    continue
                zs = [abs(z - y) / math.sqrt(sd ** 2 + (self.cfg.hm_disc * z) ** 2) for (_, z, _), y in zip(sweep, preds)]
                scored.append((max(zs), sum(x * x for x in zs), fam, c, g))
            if not scored:
                continue
            scored.sort(key=lambda x: (x[0], x[1]))
            worst, _, fam, c, g = scored[0]
            ident = [x for x in self._interp_identity(curve, sweep, sd)]
            self.orch.events.emit("note", msg=f"{t.claim_id}: scale probe on {knob}: best g(v) = "
                                              f"{'%g*v' % c if fam == 'x' else 'v%+g' % c} (worst claim {worst:.1f} "
                                              f"sigma on the measured curve; as is {max(ident):.1f})")
            if worst > FIT_I or worst >= max(ident):
                continue
            # verify: run the code at g(v) for every claim
            configs = []
            for v, _, claim in sweep:
                gv = self._snap_value(g(v), self.spec.knobs[knob].default)
                cfg = {} if _same_value(gv, self.spec.knobs[knob].default) else {knob: gv}
                configs.append((claim, cfg))
            try:
                await _all(*(self.measure(cfg, self.cfg.scale_repeats, f"scale {knob}") for _, cfg in configs))
            except (RunBudgetExceeded, budget.BudgetExceeded):
                pass
            from gapfinder.diagnose import Hypothesis, Prediction

            preds = {}
            for claim, cfg in configs:
                vals = [b.parsed_metrics[t.metric] for b in self.measure_ok(cfg) if t.metric in b.parsed_metrics]
                if vals and claim.claim_id in diff.claims:
                    preds[claim.claim_id] = Prediction.from_values(vals, diff.claims[claim.claim_id].naive_sd)
            rel = "%g x the paper's" % c if fam == "x" else "the paper's %+g" % c
            h = diff.add(Hypothesis(f"code:scale:{knob}:{fam}{c:g}", "code",
                                    f"the code's {knob} is {rel} (a unit or convention differs between paper and code)",
                                    0.08, preds, detail={"knob": knob, "family": fam, "c": c},
                                    runs=sum(len(self.measure_ok(cfg)) for _, cfg in configs),
                                    check=f"find where {knob} enters the computation and compare its unit with the paper's"))
            v_target = configs[0][1]
            swept = [claim.claim_id for _, _, claim in sweep]
            fits = all(cid in h.per_claim and h.per_claim[cid]["I"] <= STRICT_I and cid in preds for cid in swept)
            self.scale_relations.append({"knob": knob, "family": fam, "c": c, "verified": bool(fits),
                                         "claims": len(sweep)})
            res.notes.append(f"scale probe: the code's {knob} as {rel} {'fits every swept claim' if fits else 'does not fit every swept claim'} "
                             f"after {h.runs} runs at g(v) (" + ", ".join(
                                 f"{claim.claim_id} at {knob}={cfg.get(knob, self.spec.knobs[knob].default)}"
                                 for claim, cfg in configs) + ")")
            if fits and len(sweep) >= 3 and _rank(res) > _LABEL_RANK[ConfidenceLabel.inconsistency.value]:
                old = dict(res.changes)
                res.changes, res.gap_after = dict(v_target), self.gap(t, v_target)
                res.closes = True
                res.attribution = self._attribution(t, v_target, res.gap_after, ConfidenceLabel.inconsistency,
                                                    [b.result_checkpoint for b in self.measure_ok(v_target)
                                                     if b.result_checkpoint])
                res.held_out = {claim.claim_id: {"gap_before": self.gap(claim, {}) if claim is t else None,
                                                 "gap_after": (self.value(cfg, t.metric) - claim.paper_value)
                                                 / abs(claim.paper_value), "ok": True, "at": {knob: cfg.get(knob, self.spec.knobs[knob].default)}}
                                for claim, cfg in configs[1:]}
                res.notes.append(f"labelled Paper-artifact inconsistency: one factor ({rel}) makes every one of the "
                                 f"{len(sweep)} swept claims fit" + (f"; it replaces {old}" if old and old != res.changes
                                                                      else ""))

    # ------------------------------------------------------------ mutation-based localisation (plan D5)
    def _wants_mutations(self, t: Target, res: ClaimResult) -> bool:
        rel = [r for r in self.scale_relations if r.get("verified")]
        label = res.attribution.confidence_label if res.attribution else ConfidenceLabel.unexplained.value
        out_of_space = (res.diagnosis or {}).get("kind", "").startswith("out_of_space")
        return bool(rel) or out_of_space or label in (ConfidenceLabel.unexplained.value,
                                                      ConfidenceLabel.conflicts_held_out.value)

    async def _mutation_round(self, t: Target, res: ClaimResult) -> None:
        """Small code edits at sites on the data flow of the knobs the claims depend on, scored on every claim.
        Stages: one run each (target); the best `mutation_keep` at every claim's condition; the best two repeated.
        Mutants that predict the same numbers form one group (behaviour can't tell them apart); the group is
        reported with its origin (the deepest site on the data flow) first. Never "Explained": a fitting mutant is a
        code lead, a paper-code inconsistency only when a verified scale relation implies it."""
        root = self.spec.code_root()
        if root is None or not self._wants_mutations(t, res):
            return
        from gapfinder.diagnose import FIT_I, STRICT_I
        from gapfinder.sandbox.spec import Knob
        from gapfinder.search.mutation import find_mutants

        knobs = sorted({k for p in self._usable_points() for k in p.at} | {r["knob"] for r in self.scale_relations}
                       | {k for k in res.changes if not k.startswith("@")}
                       | {x["knob"] for x in (res.screen or [])[:3] if x.get("units", 0) > 1 and not x["knob"].startswith("@")})
        executed = self.trace_report.executed if getattr(self, "trace_report", None) is not None else None
        hints: dict[str, set[int]] = {}
        try:  # lines a static check flagged (split fractions, evaluation switches, selection on test data)
            from gapfinder.ingest.code_checks import code_checks

            for x in code_checks(root, set(self.spec.knobs), limit=80):
                if x.family in ("split_fraction", "eval_switch", "selection_in_code", "label_in_prediction"):
                    hints.setdefault(x.file, set()).add(x.line)
        except Exception:  # noqa: BLE001 (a hint only)
            hints = {}
        ms = find_mutants(root, knobs, executed, self.scale_relations, limit=self.cfg.mutation_max, hints=hints)
        if not ms:
            return
        room = (self.cfg.max_runs or 10 ** 6) - self.runs_used
        cap = int((self.cfg.max_runs or 10 ** 6) * self.cfg.mutation_budget_frac)
        n_pts = len(self._usable_points())
        per_kept = (1 + n_pts) * 2
        n_first = max(0, min(len(ms), min(room, cap) - self.cfg.mutation_keep * per_kept))
        ms = ms[:n_first]
        if not ms:
            res.notes.append("mutation round: no room left in the run budget")
            return
        for m in ms:
            self.spec.knobs.setdefault(m.name, Knob(layer="environment", default="0", env=True, choices=["0", "1"]))
        self.orch.events.emit("note", msg=f"{t.claim_id}: mutation round: {len(ms)} mutants on the data flow of "
                                          f"{', '.join(knobs) or 'the metric code'} (top: {ms[0].describe()})")
        await _all(*(self.measure({m.name: "1"}, 1, "mutation screen") for m in ms))
        ran = [m for m in ms if self.measure_ok({m.name: "1"})]
        if not ran:
            res.notes.append(f"mutation round: none of {len(ms)} mutants ran")
            return
        g0 = abs(self.gap(t, {}))

        def target_score(m):
            i = self.implausibility(t, {m.name: "1"})
            g = self.gap(t, {m.name: "1"})
            return (i if i is not None else float("inf"), abs(g) if g is not None else float("inf"))
        moved = [m for m in ran if target_score(m)[1] < g0 - self.band(t)]
        moved.sort(key=lambda m: (target_score(m), -m.priority))
        kept = moved[: self.cfg.mutation_keep]
        if not kept:
            res.notes.append(f"mutation round: none of {len(ran)} mutants moved {t.claim_id} toward the paper")
            return
        diff = self.differentials.get(t.claim_id) or self._new_differential(t)
        self.differentials[t.claim_id] = diff
        self._add_point_claims(diff)
        await self._measure_points([{m.name: "1"} for m in kept], "mutation point")
        hyps = {}
        for m in kept:
            hyps[m.name] = diff.add(self._config_hypothesis(diff, {m.name: "1"}, 0.02 if not m.tags else 0.05,
                                                            title=f"a code change: {m.describe()}"))
        best = sorted(kept, key=lambda m: (-hyps[m.name].posterior, hyps[m.name].max_I))[:2]
        for m in best:  # repeats at the target and at every claim's condition
            await self.measure({m.name: "1"}, self.confirm_repeats(t), "mutation confirm")
            for p in self._usable_points():
                await self.measure(self._point_config(p, {m.name: "1"}), self.cfg.scale_repeats, "mutation confirm")
            hyps[m.name] = diff.add(self._config_hypothesis(diff, {m.name: "1"}, 0.02 if not m.tags else 0.05,
                                                            title=f"a code change: {m.describe()}"))
        fitting = [m for m in kept if hyps[m.name].fits_all]
        if not fitting:
            res.notes.append("mutation round: no mutant fits every claim (" + "; ".join(
                f"{m.describe()}: worst {hyps[m.name].max_I:.1f} sigma" for m in kept[:3]) + ")")
            return
        # one group per set of mutants with the same predictions (within one band on every claim)
        groups: list[list] = []
        for m in sorted(fitting, key=lambda m: hyps[m.name].max_I):
            pm = hyps[m.name].per_claim
            for g in groups:
                pg = hyps[g[0].name].per_claim
                if all(abs(pm[c]["pred"] - pg[c]["pred"]) <= max(diff.claims[c].naive_sd, 1e-9) * 2 for c in pm):
                    g.append(m)
                    break
            else:
                groups.append([m])
        top = groups[0]
        origin = max(top, key=lambda m: (m.dist, m.kind == "num"))  # the deepest site: where the quantity comes from
        top.sort(key=lambda m: m is not origin)
        h = hyps[origin.name]
        self.code_leads[t.claim_id] = [{"group": [m.describe() for m in g], "worst_sigma": round(hyps[g[0].name].max_I, 2),
                                        "grounded": any(x.tags and "relation" in " ".join(x.tags) for x in g)} for g in groups]
        grounded = any("relation" in " ".join(m.tags) for m in top)
        res.notes.append(f"mutation round: {len(top)} equivalent code change(s) fit every claim (worst "
                         f"{h.max_I:.1f} sigma): " + "; ".join(m.describe() for m in top[:5])
                         + (" (implied by the verified scale relation)" if grounded else ""))
        strict = h.max_I <= STRICT_I and len(diff.claims) >= 3
        label = (ConfidenceLabel.inconsistency if grounded and strict else ConfidenceLabel.fits_but_unsupported)
        current = res.attribution.confidence_label if res.attribution else ConfidenceLabel.unexplained.value
        keep_scale = current == ConfidenceLabel.inconsistency.value and res.changes and not any(
            k.startswith("@") for k in res.changes)
        if keep_scale:  # the scale relation is the answer; the mutant is where it lives in the code
            res.notes.append(f"the code site of that relation: {origin.describe()}")
            return
        if _rank(res) <= _LABEL_RANK[label.value] and current != ConfidenceLabel.unexplained.value and res.changes:
            return
        cfg = {origin.name: "1"}
        res.changes, res.gap_after = cfg, self.gap(t, cfg)
        res.closes = res.gap_after is not None and abs(res.gap_after) <= self.band_at(t, cfg)
        res.attribution = self._attribution(t, cfg, res.gap_after, label,
                                            [b.result_checkpoint for b in self.measure_ok(cfg) if b.result_checkpoint])
        res.notes.append(f"explained with a code change (tested in memory, no file edited): {origin.describe()}; "
                         "a code lead, not a confirmed cause")

    # ------------------------------------------------------------ library drift and the paper-era code (D1.3-D1.5, D7.2)
    def _claim_sd(self, c: Target) -> float:
        vals = [b.parsed_metrics[c.metric] for b in self.measure_ok({}) if c.metric in b.parsed_metrics]
        return max(statistics.stdev(vals) if len(vals) >= 2 else 0.0, self.cfg.noise_floor_frac * abs(c.paper_value),
                   1e-12)

    async def _lib_same(self, t: Target, a: Changes, b: Changes, label: str, max_n: int = 3) -> bool:
        """Whether two configurations give the same numbers on every claim (the target and its held-outs) within
        library_z standard errors. Sequential: one run each, another when the comparison is borderline, up to max_n.
        A configuration that doesn't run gives no numbers, so it is never "the same"."""
        z, worst = self.cfg.library_z, float("inf")
        for n in range(1, max_n + 1):
            await _all(self.measure(a, n, label), self.measure(b, n, label))
            worst, compared = 0.0, 0
            for c in self._diag_claims(t):
                va = [x.parsed_metrics[c.metric] for x in self.measure_ok(a) if c.metric in x.parsed_metrics]
                vb = [x.parsed_metrics[c.metric] for x in self.measure_ok(b) if c.metric in x.parsed_metrics]
                if not va or not vb:
                    continue
                se = self._claim_sd(c) * math.sqrt(1 / len(va) + 1 / len(vb))
                worst = max(worst, abs(statistics.fmean(va) - statistics.fmean(vb)) / se)
                compared += 1
            if not compared:
                return False
            if worst <= 0.6 * z or worst >= 1.5 * z:
                break
        return worst <= z

    def _lib_room(self, start: int) -> None:
        cap = int((self.cfg.max_runs or 10 ** 6) * self.cfg.library_budget_frac)
        if self.runs_used - start >= cap:
            raise _LibraryBudget(f"its share of the run budget ({cap} runs) is used")

    async def _vm_probe(self, cmd: str, files: dict[str, bytes], timeout: float = 900) -> str:
        """One command in a disposable VM from the loaded checkpoint, with the runtime shim (not a branch)."""
        from gapfinder.sandbox.backend import InfraError

        parent = await self.orch.stage("loaded", {})
        cmd, env, files = self.orch._with_runtime_shim(cmd, {}, files)
        try:
            r = await self.orch._exec(parent, cmd, {**env, "RUN_TAG": "gf-library-probe"}, timeout, disposable=True,
                                      files=files)
        except InfraError as exc:
            self.orch.events.emit("note", msg=f"library probe: the API probe failed to start ({str(exc)[:200]})")
            return ""
        self.orch.cost.add_run(r.resources.cost_usd)
        return (r.stdout or "") + "\n" + (r.stderr or "")

    async def _library_probe(self, t: Target, out: dict) -> None:
        """Which old package changes the numbers (delta debugging), from which release (binary search over its
        releases), and at which call site (the API and source diff of what the repository calls, each signature
        lead verified by an in-memory code edit on the newer release). gapfinder/diagnose/library.py."""
        from gapfinder import env_year
        from gapfinder.diagnose import library as lib
        from gapfinder.sandbox import ast_patch
        from gapfinder.sandbox.spec import Knob

        info = getattr(self.spec, "library", None) or {}
        pins = info.get("pins") or {}
        K = env_year.KNOB
        if not pins or K not in self.spec.knobs:
            return
        start = self.runs_used
        choices = self.spec.knobs[K].choices
        by_dir = {p["dir"]: d for d, p in pins.items()}
        dirs = sorted(by_dir)
        has_all = "all" in choices
        bundles = {p["dir"]: set(p.get("bundle") or [p["dir"]]) for p in pins.values()}
        every = set().union(*bundles.values())

        def cfg(sub, extra=()) -> Changes:
            """A set of pinned packages, each with the dependencies it brought in, as the knob's value."""
            on = set().union(*(bundles[x] for x in sub)) if sub else set()
            if not on and not extra:
                return {}
            if has_all and on == every and not extra:
                return {K: "all"}
            return {K: ",".join(sorted(on) + list(extra))}

        out.update({"packages": {d: p["old"] for d, p in pins.items()}, "culprits": [], "change_points": []})
        note = out["notes"].append
        independent = False
        if has_all:
            ref = {K: "all"}
            self._lib_room(start)
            out["effect"] = not await self._lib_same(t, ref, {}, "library: all")
            if not out["effect"]:
                note("library: the packages as of the paper's date give the same numbers as today's "
                                 "(no effect beyond noise)")
                return
            if len(dirs) == 1:
                culprits = dirs
            else:
                await _all(*(self.measure(cfg([d]), 1, "library: one package") for d in dirs))
                alone = []
                for d in dirs:
                    self._lib_room(start)
                    if await self._lib_same(t, cfg([d]), ref, "library: one package"):
                        alone.append(d)
                if alone:
                    culprits = alone[:1]
                    out["ddmin"] = {"tests": 0, "minimal": True, "note": "one package alone gives every old package's numbers"}
                else:
                    async def test(sub):
                        self._lib_room(start)
                        return await self._lib_same(t, cfg(sub), ref, "library: delta debugging")

                    culprits, n_tests, minimal = await lib.ddmin(dirs, test, known={frozenset([d]): False for d in dirs},
                                                                 max_tests=16)
                    out["ddmin"] = {"tests": n_tests, "minimal": minimal}
        else:  # the old packages don't import together: each alone
            culprits = []
            for d in dirs:
                self._lib_room(start)
                if not await self._lib_same(t, cfg([d]), {}, "library: one package"):
                    culprits.append(d)
            out["effect"] = bool(culprits)
            independent = True
            if not culprits:
                note("library: no old package changes the numbers beyond noise")
                return
        out["culprits"] = [by_dir[d] for d in culprits]
        note("library: " + (" and ".join(f"{by_dir[d]} {pins[by_dir[d]]['old']}" for d in culprits))
                         + (" together" if len(culprits) > 1 and not independent else "")
                         + " gives the numbers of every package as of the paper's date" if not independent else
                         "library: " + ", ".join(f"{by_dir[d]} {pins[by_dir[d]]['old']}" for d in culprits)
                         + " change the numbers (each alone)")
        diff = self.differentials.get(t.claim_id) or self._new_differential(t)
        self.differentials[t.claim_id] = diff
        c_cfg = cfg(culprits) if not independent else cfg(culprits[:1])
        if self.measure_ok(c_cfg):
            diff.add(self._config_hypothesis(diff, c_cfg, 0.1, title="library drift: " + ", ".join(
                f"{by_dir[d]}=={pins[by_dir[d]]['old']}" for d in culprits) + " (as of the paper's date)", cls="library"))
        root = self.spec.code_root()
        executed = self.trace_report.executed if getattr(self, "trace_report", None) is not None else None
        for P in culprits[:2]:
            dist, pin = by_dir[P], pins[by_dir[P]]
            others = [] if independent else [d for d in culprits if d != P]
            rel = list(pin.get("releases") or [])

            def at(ver, rel=rel, others=others, P=P, dist=dist) -> Changes:
                if ver == rel[0]:
                    return cfg(others + [P])
                if ver == rel[-1]:
                    return cfg(others)
                # a release between: installed on demand, beside the dependencies the paper-era one brought
                held = set().union(*(bundles[x] for x in others)) if others else set()
                return cfg(others, extra=sorted(bundles[P] - {P} - held) + [f"{dist}=={ver}"])

            if len(rel) < 2:
                continue

            async def same_v(va, vb, at=at, dist=dist):
                self._lib_room(start)
                return await self._lib_same(t, at(va), at(vb), f"library: {dist} releases")

            cps = await lib.change_points(rel, same_v, max_points=2)
            if cps:
                self._library_evidence(K, [cfg(culprits if not independent else [P])[K]]
                                       + (["all"] if has_all and not independent else []),
                                       f"The paper ({info.get('date', 'its date')}) predates {dist} {cps[0][1]}, the "
                                       f"first release that gives today's numbers ({cps[0][0]} gives the paper-era "
                                       "ones)")
            for va, vb in cps:
                cp = {"package": dist, "before": va, "after": vb, "leads": []}
                out["change_points"].append(cp)
                note(f"library: {dist} {vb} changed the numbers ({va} gives the older ones)")
                if root is None:
                    continue
                sites = lib.call_sites(root, pin.get("modules") or [dist.replace("-", "_")],
                                       [pin["path"]] if pin.get("path") else None, executed)
                if not sites:
                    cp["note"] = "no call into the package found in the repository's code"
                    continue
                quals = list(dict.fromkeys(x.qual for x in sites))[:150]
                pre = env_year.run_prefix()
                pa = pre.replace("{%s}" % K, at(va).get(K, "0"))
                pb = pre.replace("{%s}" % K, at(vb).get(K, "0"))
                text = await self._vm_probe(lib.probe_command(pa, pb), lib.probe_files(quals))
                A, B = lib.parse_probe(text, "A"), lib.parse_probe(text, "B")
                if not A or not B:
                    cp["note"] = "the API probe returned nothing: " + text[-300:]
                    continue
                top = (pin.get("modules") or [dist])[0].split(".")[0]
                cp["loaded"] = {"before": (A.get("versions") or {}).get(top), "after": (B.get("versions") or {}).get(top)}
                leads = lib.compare(sites, A, B, va, vb)
                tried = []
                for x in [x for x in leads if x.op][:4]:
                    if ast_patch.entry_script(root / x.file) and not ast_patch.direct_entry(self.spec.run.command, x.file):
                        continue
                    name = f"@ast:{x.file}:{x.line}:@mut.{x.col}.Call.{x.op}"
                    self.spec.knobs.setdefault(name, Knob(layer="environment", default="0", env=True, choices=["0", "1"]))
                    self._lib_room(start)
                    ok = await self._lib_same(t, {**at(vb), name: "1"}, at(va), "library: API lead")
                    tried.append((x, name, ok))
                if tried and not any(ok for _, _, ok in tried) and len(tried) > 1:
                    together = {**at(vb), **{name: "1" for _, name, _ in tried}}
                    self._lib_room(start)
                    if await self._lib_same(t, together, at(va), "library: API leads together"):
                        cp["together"] = [x.site + " " + x.op for x, _, _ in tried]
                        note(f"library: with {dist} {vb}, the {len(tried)} API edits together ("
                                         + "; ".join(x.detail for x, _, _ in tried) + f") give {va}'s numbers")
                verified = {id(x): ok for x, _, ok in tried}
                cp["leads"] = [{**x.to_dict(), "verified": verified.get(id(x))} for x in leads[:10]]
                for x, name, ok in tried:
                    if ok:
                        note(f"library: verified at the call site {x.site}: {x.detail}; with {dist} {vb} "
                                         f"and the call changed (in memory: {x.op}), the numbers are {va}'s")
                        diff.add(self._config_hypothesis(diff, {**at(vb), name: "1"}, 0.08,
                                                         title=f"library API change at {x.site}: {x.detail}",
                                                         cls="library"))
                if not any(ok for _, _, ok in tried):
                    top_leads = [x for x in leads if x.kind != "source"][:2] or leads[:2]
                    if top_leads:
                        note(f"library: leads for {dist} {va} -> {vb} (unverified): "
                                         + "; ".join(f"{x.site} {x.detail}" for x in top_leads))

    def _library_evidence(self, knob: str, values: list[str], fact: str) -> None:
        """Evidence for the paper-year or paper-era knob at these values: what the paper's date says it ran."""
        a = self.assumptions.get(knob)
        if a is None:
            return
        quote = fact + ": " + ", ".join(f"{knob}={v}" for v in values)
        if any(e.quote == quote for e in a.evidence):
            return
        self.assumptions[knob] = a.model_copy(update={"evidence": [*a.evidence, Evidence(
            kind="measurement", ref="library probe (PyPI upload dates, the paper's date, release search)", quote=quote)]})

    async def _era_probe(self, t: Target, lib_out: dict) -> None:
        """The paper-era code: does the repository's last commit before the paper give other numbers, and which later
        commit changed them (binary search over the commits up to the given one; their diff from GitHub)."""
        import asyncio as _asyncio

        from gapfinder import env_year
        from gapfinder.diagnose import library as lib

        info = (getattr(self.spec, "library", None) or {}).get("era")
        K = env_year.ERA_KNOB
        if not info or K not in self.spec.knobs:
            return
        start = self.runs_used
        ref = {K: "1"}
        self._lib_room(start)
        moved = not await self._lib_same(t, ref, {}, "paper-era code")
        out = {"sha": info["sha"], "date": info["date"], "effect": moved, "change_points": []}
        lib_out["era"] = out
        note = lib_out["notes"].append
        if not moved:
            note(f"paper-era code: the commit {info['sha'][:10]} ({info['date']}) gives the same numbers")
            return
        shas = [c["sha"] for c in info.get("commits") or []]
        if info["sha"] in shas:
            shas = shas[shas.index(info["sha"]):]
        else:
            shas = [info["sha"]] + shas
        given = info.get("commit") or ""
        if not shas or not (shas[-1].startswith(given) or given.startswith(shas[-1])):
            shas.append(given)

        def at(sha: str) -> Changes:
            return ref if sha == shas[0] else {} if sha == shas[-1] else {K: sha}

        async def same(a, b):
            self._lib_room(start)
            return await self._lib_same(t, at(a), at(b), "paper-era commits")

        note(f"paper-era code: the commit {info['sha'][:10]} ({info['date']}) gives other numbers")
        self._library_evidence(K, ["1"], f"The repository's last commit before the paper ({info['sha'][:10]}, "
                                         f"{info['date']}) gives other numbers than the given commit")
        if len(shas) > 2:
            for a, b in await lib.change_points(shas, same, max_points=2):
                d = await _asyncio.to_thread(env_year.commit_diff, info["repo"], b) if info.get("repo") else None
                msg = next((c.get("message", "") for c in info.get("commits") or [] if c["sha"] == b), "")
                out["change_points"].append({"before": a, "after": b, "message": msg, "diff": d})
                files = [f["file"] for f in (d or {}).get("files") or [] if f["code"]][:6]
                note(f"paper-era code: commit {b[:10]} ({msg}) changed the numbers"
                                 + (f"; it changed {', '.join(files)}" if files else ""))
        diff = self.differentials.get(t.claim_id) or self._new_differential(t)
        self.differentials[t.claim_id] = diff
        diff.add(self._config_hypothesis(diff, ref, 0.08, title=f"the code as of the paper (commit {info['sha'][:10]})",
                                         cls="code"))

    def _interp_identity(self, curve, sweep, sd) -> list[float]:
        """The swept claims against the measured curve as is (g = identity), in sigma."""
        out = []
        for v, z, _ in sweep:
            y = self._interp(curve, v)
            out.append(float("inf") if y is None else abs(z - y) / math.sqrt(sd ** 2 + (self.cfg.hm_disc * z) ** 2))
        return out

    def _point_check(self, p: Target, changes: Changes) -> dict:
        """Like a held-out claim: no worse under the candidate than under the naive configuration, beyond noise."""
        v0, v = self.value(self._point_config(p, {}), p.metric), self.value(self._point_config(p, changes), p.metric)
        if v0 is None or v is None:
            return {"ok": True, "checked": False, "at": dict(p.at), "why": "not measured"}
        before, after = (v0 - p.paper_value) / abs(p.paper_value), (v - p.paper_value) / abs(p.paper_value)
        return {"gap_before": before, "gap_after": after, "ok": held_out_ok(before, after, self.band(p)),
                "checked": True, "at": dict(p.at)}

    def _hm_inputs(self, t: Target) -> tuple[dict, list, dict]:
        """History matching's runs and claims: the target, its held-outs, and the claims at fixed knob values
        (each read from the runs at the configuration with its values on top; optional per configuration)."""
        claims = [(t.claim_id, t.metric, t.paper_value)] + [
            (h.claim_id, h.metric, h.paper_value) for h in self.targets if h.held_out
            and not h.tuned_separately and h.metric != t.metric]
        runs = {tuple(sorted(k)): [b.parsed_metrics for b in v if b.status == BranchStatus.succeeded]
                for k, v in self._runs.items()}
        runs = {k: v for k, v in runs.items() if v}
        pts = self._usable_points()
        if not pts:
            return runs, claims, {}
        aug = {}
        for key, ms in runs.items():
            extra = []
            for p in pts:
                pk = tuple(sorted(self._point_config(p, dict(key)).items()))
                extra += [{f"{p.metric}@{p.claim_id}": m[p.metric]} for m in runs.get(pk, []) if p.metric in m]
            aug[key] = ms + extra
        claims += [(p.claim_id, f"{p.metric}@{p.claim_id}", p.paper_value) for p in pts]
        return aug, claims, {"optional": {p.claim_id for p in pts},
                             "sd_alias": {f"{p.metric}@{p.claim_id}": p.metric for p in pts}}

    def _relation_configs(self, rel: Target, changes: Changes) -> tuple[Changes, Changes]:
        knob = rel.relation["knob"]
        default = self.spec.knobs[knob].default

        def at(v):
            c = dict(changes)
            if _same_value(str(v), default):
                c.pop(knob, None)
            else:
                c[knob] = str(v)
            return c
        return at(rel.relation["from"]), at(rel.relation["to"])

    def _relation_result(self, rel: Target, ca: Changes, cb: Changes) -> dict:
        ya, yb = self.value(ca, rel.metric), self.value(cb, rel.metric)
        if ya is None or yb is None:
            return {"checked": False, "why": "not measured under this configuration"}
        band = self.bands[rel.metric].band if rel.metric in self.bands else 0.0
        diff, up = yb - ya, rel.relation.get("direction", "up") == "up"
        broken = diff < -band if up else diff > band
        holds = diff > band if up else diff < -band
        return {"checked": True, "from_value": ya, "to_value": yb, "diff": diff, "band": band,
                "broken": broken, "holds": holds}

    async def _check_relation(self, rel: Target, changes: Changes) -> dict:
        """Measure the relation's two ends under `changes` (relation_repeats runs each, cached runs reused).
        Out of budget, it uses what exists and may report "not checked": never a reason to reject."""
        if rel.relation.get("knob") not in self.spec.knobs:
            return {"checked": False, "why": f"knob {rel.relation.get('knob')!r} is not in the harness"}
        ca, cb = self._relation_configs(rel, changes)
        try:
            await _all(self.measure(ca, self.cfg.relation_repeats, f"relation {rel.claim_id}"),
                       self.measure(cb, self.cfg.relation_repeats, f"relation {rel.claim_id}"))
        except (RunBudgetExceeded, budget.BudgetExceeded):
            pass
        return self._relation_result(rel, ca, cb)

    def _relation_broken_cached(self, c: Changes) -> bool:
        """Some relation reverses under `c`, judged from runs already made (no new runs)."""
        for rel in self.relations:
            if rel.relation.get("knob") in self.spec.knobs and self._relation_result(rel, *self._relation_configs(rel, c)).get("broken"):
                return True
        return False

    def _cap_confidence(self, t: Target, res: ClaimResult) -> None:
        """A confident label must be earned by a complete search (blind-2: "Explained" came from a partial run,
        with a knob never tested and only a code default as evidence). Caps Explained, Paper-artifact
        inconsistency and Partially explained at "Fits but unsupported" when:
        - the run budget ran out before the search finished;
        - a knob with candidate values never got a single screen run;
        - a changed knob's support is only code evidence (a default or a script line: what the code does, not
          what the authors ran for this experiment)."""
        if not self.cfg.complete_for_confidence or res.attribution is None:
            return
        confident = {ConfidenceLabel.explained.value, ConfidenceLabel.inconsistency.value,
                     ConfidenceLabel.partially_explained.value}
        if res.attribution.confidence_label not in confident:
            return
        why = []
        if res.status == "partial":
            why.append("the run budget ran out before the search finished")
        knobs_with_values = {h.knob for h in self.hypotheses()}
        screened = {next(iter(k))[0] for k in self._runs if len(k) == 1 and self.measure_ok(dict(k))}
        if unscreened := sorted(knobs_with_values - screened):
            why.append(f"{len(unscreened)} knob(s) never screened ({', '.join(unscreened[:6])}"
                       f"{', ...' if len(unscreened) > 6 else ''})")
        code_only = [k for k, p in res.plausibility.items() if p.supported and p.source == "code"]
        if code_only:
            why.append(f"the only support for {', '.join(f'{k}={res.changes.get(k)}' for k in code_only)} is code "
                       "evidence, which shows what the code does, not what the authors ran")
        if not why:
            return
        res.notes.append(f"capped at Fits but unsupported (was {res.attribution.confidence_label}): " + "; ".join(why))
        res.attribution = res.attribution.model_copy(update={"confidence_label": ConfidenceLabel.fits_but_unsupported.value})

    def _unsupported(self, res: ClaimResult) -> bool:
        """No confident answer: the patch round may look for a code cause (patch_when_unsupported)."""
        confident = {ConfidenceLabel.explained.value, ConfidenceLabel.inconsistency.value}
        return self.cfg.patch_when_unsupported and not (res.attribution and res.attribution.confidence_label in confident)

    def _wants_patch(self, res: ClaimResult) -> bool:
        kind = (res.diagnosis or {}).get("kind", "")
        return kind.startswith("out_of_space") or (kind in ("in_space", "reproduced") and self._unsupported(res)
                                                    and bool((res.diagnosis or {}).get("leads")))

    async def _contrast(self, res: ClaimResult) -> None:
        """Out of space: ask Super where the code, as traced, differs from the paper; ground the answers."""
        if not self.cfg.contrast or self.router is None or not self.paper_text or not self.trace_records:
            return
        root = self.spec.code_root()
        if root is None:
            return
        from gapfinder.search.contrast import contrast, ground

        try:
            diffs = await contrast(self.router, self.paper_text, self.trace_records, (res.diagnosis or {}).get("leads") or [])
        except budget.BudgetExceeded:
            raise
        except Exception as exc:  # an aid: a failure leaves the patch round as it was
            self.orch.events.emit("note", msg=f"contrast: skipped ({type(exc).__name__}: {str(exc)[:160]})")
            return
        patch, structural, rejected = ground(diffs, root, self.paper_text)
        res.diagnosis["contrast_leads"] = patch
        res.diagnosis["structural_leads"] = structural
        self.orch.events.emit("note", msg=f"contrast: {len(patch)} literal and {len(structural)} structural difference(s) "
                                          f"from the paper" + (f"; rejected: {'; '.join(rejected)}" if rejected else ""))

    def _match_constants(self, res: ClaimResult) -> None:
        """Stated paper values with no knob, against the code's literals of the same name (no model call)."""
        root = self.spec.code_root()
        if not self.cfg.match_constants or root is None:
            return
        from gapfinder.search.matcher import match_constants

        pending = [a for a in self._unmapped_assumptions if a.knob in self.unmapped]
        found = match_constants(pending, root)
        res.diagnosis["matcher_leads"] = found
        if found:
            self.orch.events.emit("note", msg=f"constant matcher: {len(found)} literal(s) differ from the paper: "
                                              + "; ".join(f"{x['name']} {x['value']} -> {x['paper_value']}"
                                                          f" ({x['file']}:{x['line']})" for x in found[:6]))

    def _match_ops(self, res: ClaimResult) -> None:
        """Operations the paper names against the ones the code calls (no model call): swap leads."""
        root = self.spec.code_root()
        if not self.cfg.op_swaps or root is None or not self.paper_text:
            return
        from gapfinder.search.op_swaps import op_swap_leads

        found = op_swap_leads(root, self.paper_text)
        res.diagnosis["swap_leads"] = found
        if found:
            self.orch.events.emit("note", msg=f"operation swaps: {len(found)} the paper grounds: " + "; ".join(
                f"{x['value']} -> {x['paper_value']} ({x['file']}{':' + str(x['line']) if x['line'] else ''})"
                for x in found[:6]))

    async def _secant_step(self, t: Target, hyps: list[Hypothesis], tried: set[frozenset]) -> list[Hypothesis]:
        """Secant iteration on each numeric knob the paper's number is bracketed on: interpolate the crossing,
        snap it to a round value, screen it, and repeat with that point included (up to secant_per_knob
        rounds). Linear-in-log interpolation of a linear response lands short (alpha 2 -> 5, crossing 3:
        2.7 snaps to 2.5); the second round closes it (2.5 -> 5 gives 3)."""
        if self.cfg.secant_per_knob <= 0 or not self.cfg.coverage:  # part of value coverage (off: the v1.0 grid)
            return []
        y0 = self.value({}, t.metric)
        if y0 is None:
            return []
        # only to fill a gap in coverage: with one target number, interpolation can make almost any knob hit it
        # exactly, so when a screened value already fits every claim within noise the secant step would only
        # manufacture decoys (dev suite, runs 3000/3100: lr=0.04, eps_start=0.3 and eps_decay=0.495 beat the
        # true max_steps=100, a ladder value that fit; 102 -> 92 of 138 correct). "Every claim": a value that
        # fits only the target (toy build_mode=release for a planted alpha=3) leaves the gap open
        held = [h for h in self.targets if h.held_out and not h.tuned_separately and h.metric in self.bands]

        def fits_all(c):
            return all((g := self.gap(x, c)) is not None and abs(g) <= self.band(x) for x in [t] + held)
        if any(fits_all(h.changes) for h in hyps):
            return []
        added: list[Hypothesis] = []
        for _ in range(self.cfg.secant_per_knob):
            new: list[Hypothesis] = []
            pool = hyps + added
            for knob in dict.fromkeys(h.knob for h in pool):
                kn = self.spec.knobs.get(knob)
                if kn is None or kn.choices or kn.role == "seed":
                    continue
                pts = [(kn.default, y0)] + [(h.value, self.value(h.changes, t.metric)) for h in pool if h.knob == knob]
                have = {v for v, _ in pts}
                for v in secant_values(pts, t.paper_value, kn.role, kn.default)[:1]:  # the crossing nearest the default
                    if v in have or any(_same_number(v, w) for w in have) or not kn.affordable(v):
                        continue
                    new.append(Hypothesis(knob, v, getattr(self.assumptions.get(knob), "id", None)))
            if self.cfg.max_runs is not None:
                room = (self.cfg.max_runs - self.runs_used - self._patch_reserve
                        - int(self.cfg.escrow_frac * self.cfg.max_runs))
                new = new[: max(0, room // max(1, self.cfg.screen_repeats))]
            if not new:
                break
            self.orch.events.emit("note", msg=f"{t.claim_id}: secant step: the paper's number is bracketed; screening "
                                              + ", ".join(f"{h.knob}={h.value}" for h in new))
            await _all(*(self.measure(h.changes, self.cfg.screen_repeats, f"screen (secant) {h.knob}={h.value}")
                         for h in new))
            tried.update(frozenset(h.changes.items()) for h in new)
            added += new
        return added

    async def _spec_knob_round(self, t: Target, res: ClaimResult, tried: set[frozenset]) -> None:
        """The ledger's knobs gave no confident answer: search again with the spec knobs no assumption names
        added (low prior, code-derived values). Runs already measured are reused. The better result is kept."""
        added = list(self._fallback) + sorted(self._stated_skipped)
        self.orch.events.emit("note", msg=f"{t.claim_id}: no confident answer from the first pass; adding spec "
                                          f"knobs no assumption names and knobs the paper states at the naive value: "
                                          f"{', '.join(added)}")
        self.assumptions.update(self._fallback)
        self._fallback = {}
        self._include_stated = True
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
        hyps += await self._secant_step(t, hyps, tried)
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
        cap = self._race_cap(extra)
        if self.cfg.racing and cap and len(survivors) > cap:
            # successive halving's first cut (Hyperband): a model that reacts to every knob passes dozens of screen
            # values, and two confirmation runs each used the whole budget before any pair was tried (batch-4
            # RippleNet: 96 of 150 runs on confirmation, 0 on combine, so lr + l2_weight never ran). The strongest
            # value of each knob first, round robin over knobs, then strong ledger leads; the rest stay screened
            # (the combine round still pairs every screened value).
            by_knob: dict[str, list[Hypothesis]] = {}
            for h in sorted(survivors, key=lambda h: -score[h]):
                by_knob.setdefault(h.knob, []).append(h)
            first = [hs[i] for i in range(max(map(len, by_knob.values()))) for hs in by_knob.values() if i < len(hs)]
            keep = first[:cap] + [h for h in first[cap:] if self._strong_lead(h)]
            self.orch.events.emit("note", msg=f"{t.claim_id}: {len(survivors)} screen survivors; the {len(keep)} strongest "
                                              f"(by knob) go on to confirmation, to keep runs for the combine round")
            survivors = keep
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
        combos: list[Changes] = [c for c in self._alternative_configs()]  # the repo's own alternatives, as wholes
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
        if self.cfg.early_confirm:
            # in waves: a pair that already fits within noise gets its confirmation repeats right away, so a
            # budget that runs out later cuts unexplored pairs, not the best one (class: the budget ended before
            # the best combination's confirmation on MC Dropout, FastGCN post-hoc and Informer)
            wave = max(4, min(getattr(self.orch, "concurrency", 8), 10))  # parallel, but small enough to react
            for i in range(0, len(combos), wave):
                chunk = combos[i: i + wave]
                await _all(*(self.measure(c, 1, "combine") for c in chunk))
                early = [c for c in chunk if self.closes(t, c)]
                if early:
                    await _all(*(self.measure(c, self.confirm_repeats(t) + (self.cfg.screen_repeats if self.cfg.strict_confirm else 0),
                                              "confirm-combo (early)") for c in early))
        else:
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
        for f in ("attribution", "changes", "gap_after", "held_out", "counterfactual", "plausibility", "replay", "relations"):
            setattr(res, f, getattr(best, f))
        res.notes.extend(best.notes)
        if res.attribution.confidence_label == ConfidenceLabel.unexplained.value and res.changes:
            # nothing explains the gap: don't present the best failed attempt as an explanation
            res.notes.append(f"closest configuration tried: {res.changes} (gap {res.gap_after:+.1%}); "
                             "it did not pass verification")
            res.changes, res.gap_after = {}, res.gap_before
            res.plausibility, res.counterfactual, res.held_out, res.replay, res.relations = {}, {}, {}, [], {}
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
        # spread under the candidate against the naive run's: reported, never used to judge (the true cause
        # often widens the spread too: section 0.6's measured "don't")
        if len(self.measure_ok(changes)) >= 3 and self.band(t) > 0:
            ratio = self.band_at(t, changes) / self.band(t)
            if ratio >= 3 or ratio <= 1 / 3:
                r.notes.append(f"its runs spread {ratio:.1f}x the naive run's noise band (reported, not used to judge)")
        # 5b'. relations the paper states over a setting must not reverse under the candidate
        for rel in self.relations if self.cfg.verify else ():
            r.relations[rel.claim_id] = await self._check_relation(rel, changes)
        # 5b''. claims at fixed knob values: held-outs measured with those values on top of the candidate
        if self.cfg.verify and self._usable_points():
            await self._measure_points([changes], "point check")
            for p in self._usable_points():
                r.held_out[p.claim_id] = self._point_check(p, changes)
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
        ho_ok = all(v["ok"] for v in r.held_out.values()) and not any(v.get("broken") for v in r.relations.values())
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

        runs, claims, extra = self._hm_inputs(t)
        d = diagnose(runs, claims, t.claim_id, paper_n=self.cfg.hm_paper_n, disc=self.cfg.hm_disc, **extra)
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
        contrasted = [x for x in (res.diagnosis or {}).get("contrast_leads") or []]
        have = {(c["file"], c["line"]) for c in contrasted}  # the model's reading first, then the matcher's
        contrasted += [x for x in (res.diagnosis or {}).get("matcher_leads") or [] if (x["file"], x["line"]) not in have]
        contrasted += list((res.diagnosis or {}).get("swap_leads") or [])  # operations the paper names
        if self.trace_report is not None:  # literals seen reaching a sink at runtime come first
            traced = [{"file": x.file, "line": x.line, "name": x.name, "value": x.literal, "family": "unexposed_setting",
                       "source": "trace", "sink": x.sink} for x in self.trace_report.leads]
            have = {(t["file"], t["line"]) for t in traced}
            leads = traced + [x for x in leads if (x["file"], x["line"]) not in have]
        if contrasted:  # differences from the paper, grounded to a literal, come before everything
            have = {(c["file"], c["line"]) for c in contrasted}
            leads = contrasted + [x for x in leads if (x["file"], x["line"]) not in have]
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
            if x.get("quote") and x.get("paper_value") and k not in self.assumptions:
                # the paper states this value, verbatim: evidence like a ledger quote, and a paper-code difference
                self.assumptions[k] = Assumption(
                    id=f"P{len(self.assumptions) + 1}", knob=k, layer="environment", paper_value=str(x["paper_value"]),
                    code_default=str(x["value"]), candidate_values=[str(x["paper_value"])], prior_score=0.9,
                    status=AssumptionStatus.stated_code_differs.value, affects_claims=[],
                    evidence=[Evidence(kind="paper", ref="paper text", quote=x["quote"])])
            role = "size" if str(x.get("sink", "")).startswith(("batch.", "width.")) else None
            vals = ((role_values(role, str(x["value"])) if role else None) or patch_values(x["name"], str(x["value"])))
            pv = x.get("paper_value")  # a contrast lead: the paper's own number first
            if pv and not _same_value(str(pv), str(x["value"])):
                vals = [str(pv)] + [v for v in vals if not _same_value(v, str(pv))]
            if x.get("source") == "swap":  # an operation swap: the paper's choice and nothing else
                vals = [str(pv)]
            vals = vals[: self.cfg.patch_values]
            with_base.append([{**base, k: v} for v in vals] if base else [])
            alone.append([{k: v} for v in vals])

        def rr(groups):  # round robin over leads: every lead gets its first values first
            return [g[i] for i in range(max((len(g) for g in groups), default=0)) for g in groups if i < len(g)]
        configs = rr(with_base) + rr(alone)
        stated = {ast_patch.knob_name(x["file"], x["line"], x["name"]): str(x["paper_value"]) for x in leads
                  if x.get("paper_value") and x.get("source") in ("contrast", "matcher", "swap")}
        if len(stated) > 1:  # every difference the paper states, at the paper's values, together (VGAE: test and val %)
            configs = [stated] + ([{**base, **stated}] if base else []) + [c for c in configs if c != stated]
        if self._patch_reserve:  # leave room for the confirmation repeats
            room = max(0, self.cfg.max_runs - self.runs_used - self.confirm_repeats(t))
            configs = configs[:room]
        self.orch.events.emit("note", msg=f"{t.claim_id}: patch round: {len(leads)} code lead(s), {len(configs)} "
                                          f"configurations (base {base or 'naive'})")
        await _all(*(self.measure(c, 1, "patch screen") for c in configs))

        def rediagnose():
            runs, claims, extra = self._hm_inputs(t)
            return diagnose(runs, claims, t.claim_id, paper_n=self.cfg.hm_paper_n, disc=self.cfg.hm_disc, **extra)

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
        # an in-space answer stands unless the patch earns a strictly better label (VGAE: a paper-backed
        # inconsistency over an unsupported fit); a closer fit alone would let an unsupported patch displace a
        # correct, equally unsupported setting (GapBench answers are mostly "Fits but unsupported")
        if res.changes and not _rank(trial) < _rank(res):
            res.notes.append(f"patch round: {c} also fits every claim ({trial.attribution.confidence_label}), "
                             f"but doesn't beat {res.changes}")
            return
        for f in ("attribution", "changes", "gap_after", "held_out", "counterfactual", "plausibility", "replay", "relations"):
            setattr(res, f, getattr(trial, f))
        res.status = "searched"
        res.diagnosis = {**d.to_dict(), **{k: res.diagnosis.get(k) for k in ("leads", "contrast_leads", "matcher_leads", "structural_leads")
                                           if res.diagnosis.get(k) is not None}}
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

    async def _points_for_fits(self, t: Target, res: ClaimResult) -> None:
        """The configurations that fit every claim so far (and the answer), measured at the claims with fixed knob
        values too, so history matching can tell them apart there."""
        from gapfinder.search.history import diagnose

        runs, claims, extra = self._hm_inputs(t)
        d = diagnose(runs, claims, t.claim_id, paper_n=self.cfg.hm_paper_n, disc=self.cfg.hm_disc, **extra)
        configs = ([dict(res.changes)] if res.changes else []) + [r["config"] for r in d.joint if r["config"]]
        seen, pick = set(), []
        for c in configs:
            if frozenset(c.items()) not in seen:
                seen.add(frozenset(c.items()))
                pick.append(c)
        if pick:
            await self._measure_points(pick[: self.cfg.point_configs + 1], "point (history matching)")
        await self._points_swap(t, res)

    async def _points_swap(self, t: Target, res: ClaimResult) -> None:
        """History matching's rule for the answer: it must fit every claim. When the answer is ruled out by a claim
        at fixed knob values (I > 3 there) and another tested configuration closes the target and fits every claim,
        those included, that one is confirmed and verified, and taken if its label is no worse."""
        from gapfinder.search.history import implausibilities

        if not res.changes or res.status == "partial":
            return
        runs, claims, extra = self._hm_inputs(t)
        pids = extra.get("optional") or set()
        rows = implausibilities(runs, claims, paper_n=self.cfg.hm_paper_n, disc=self.cfg.hm_disc, **extra)
        me = next((r for r in rows if r["config"] == dict(res.changes)), None)
        bad = sorted(c for c in pids if me is not None and me["I"].get(c, 0) > 3)
        if not bad:
            return
        # consistent with the paper as in _order_candidates: closes, or an implausibility of at most 2; a row made to
        # measure a fixed-value claim (its knobs at that claim's values) is a measurement, not a candidate
        at_rows = lambda c: any(all(_same_value(str(c.get(k, "")), str(v)) for k, v in p.at.items())  # noqa: E731
                                for p in self._usable_points())
        alts = sorted((r for r in rows if r["config"] and r["config"] != dict(res.changes) and not at_rows(r["config"])
                       and pids <= set(r["I"]) and max(r["I"].values()) <= 3
                       and (self.closes(t, r["config"]) or r["I"][t.claim_id] <= 2)),
                      key=lambda r: (max(r["I"].values()), len(r["config"])))
        old = dict(res.changes)
        if not alts:
            res.notes.append(f"{old} doesn't fit {', '.join(bad)} (claims at fixed settings); no other tested "
                             "configuration fits every claim")
            return
        c = alts[0]["config"]
        await self._swap_to(t, res, c, f"{old} doesn't fit {', '.join(bad)} (claims at fixed settings); {c} fits every claim",
                            f"{old} fit the target but not {', '.join(bad)} (claims at fixed settings, I > 3); {c} fits "
                            "every claim, those included, so it is the answer (history matching)")

    async def _swap_to(self, t: Target, res: ClaimResult, c: Changes, tried: str, taken: str) -> bool:
        """Take `c` as the answer when, confirmed and verified, its label is no worse than the current one."""
        try:
            await self.measure(c, self.confirm_repeats(t), "point confirm")
            i = self.implausibility(t, c)
            if not (self.closes(t, c) or (i is not None and i <= 2)):
                return False
            trial = await self._verify(t, c, res)
        except (RunBudgetExceeded, budget.BudgetExceeded):
            return False
        if _rank(trial) > _rank(res):
            res.notes.append(f"{tried} but verified worse ({trial.attribution.confidence_label})")
            return False
        for f in ("attribution", "changes", "gap_after", "held_out", "counterfactual", "plausibility", "replay", "relations"):
            setattr(res, f, getattr(trial, f))
        res.notes.extend(trial.notes)
        res.notes.append(taken)
        return True

    def _history_match(self, t: Target, res: ClaimResult) -> None:
        """Score every measured configuration against the target and its held-out claims together."""
        from gapfinder.search.history import diagnose

        runs, claims, extra = self._hm_inputs(t)
        d = diagnose(runs, claims, t.claim_id, paper_n=self.cfg.hm_paper_n, disc=self.cfg.hm_disc, **extra)
        res.diagnosis = d.to_dict()
        root = self.spec.code_root()
        if (d.kind.startswith("out_of_space") or self._unsupported(res)) and root is not None:
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
        # plan D2.3: ties on the target are judged with the model-discrepancy floor, so a candidate that hits the
        # target exactly by chance doesn't beat one within the discrepancy; the tie goes to the other claims (the
        # held-outs and the claims at other conditions), then to the prior (D7.3: what the paper states or
        # mentions, round numbers), then to the fewest and smallest changes
        lld = {frozenset(c.items()): self.loglik(t, c, discrepancy=True) for c in candidates}
        top = max((v for v in lld.values() if v is not None), default=None)

        def tied(c: Changes) -> int:
            v = lld[frozenset(c.items())]
            return 0 if top is not None and v is not None and v >= top - LL_EQUIVALENT else 1
        return sorted(candidates, key=lambda c: (tier(c), not self._supported(c), tied(c), self._others_misfit(t, c),
                                                 -self._cand_prior(c), len(c), self._change_size(c),
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

    def loglik(self, t: Target, changes: Changes, discrepancy: bool = False) -> float | None:
        """Gaussian log-likelihood of the paper's number under the configuration: a noisy configuration
        spreads its probability, so a precise one equally close is likelier (the honest form of 'prefer
        the precise fit'). `discrepancy`: with history matching's model-discrepancy term too (plan D2.3)."""
        x = self._var(t, changes)
        if x is None:
            return None
        m, v = x
        if discrepancy:
            v += (self.cfg.hm_disc * t.paper_value) ** 2
        return -0.5 * (t.paper_value - m) ** 2 / v - 0.5 * math.log(2 * math.pi * v)

    def _others_misfit(self, t: Target, changes: Changes) -> int:
        """1 when a held-out claim or a claim at another condition, measured under the configuration, is implausible
        there (I > 3, history matching's cutoff), else 0: the held-outs break ties on the target (plan D2.3)."""
        from gapfinder.search.history import implausibilities

        runs, claims, extra = self._hm_inputs(t)
        key = dict(changes)
        rows = implausibilities(runs, claims, paper_n=self.cfg.hm_paper_n, disc=self.cfg.hm_disc, **extra)
        me = next((r for r in rows if r["config"] == key), None)
        if me is None:
            return 0
        return int(any(i > 3 for cid, i in me["I"].items() if cid != t.claim_id))

    def _cand_prior(self, changes: Changes) -> float:
        """Plan D7.3: a configuration's prior from what the paper states or mentions (a weight, never a veto)."""
        from gapfinder.diagnose.discriminate import config_prior

        stated: dict[str, set[str]] = {}
        mentioned = {k for p in self._usable_points() for k in p.at}  # knobs the paper sweeps
        documented: dict[str, set[str]] = {}
        for k, v in changes.items():
            a = self.assumptions.get(k)
            if a is None:
                continue
            vals = self._stated_values(k) if hasattr(self, "all_for") else []
            if vals or not a.paper_value.strip().lower().startswith("unstated"):
                mentioned.add(k)
                if any(_same_value(x, v) for x in vals):
                    stated[k] = {v}
            if any(e.kind == "paper" for e in a.evidence):
                mentioned.add(k)
            pl = plausible(a, v, self.spec.knobs[k].default if k in self.spec.knobs else None)
            if pl.supported and pl.source == "docs":
                documented[k] = {v}
        return config_prior(changes, stated, mentioned, documented)

    def _claim_loglik(self, c: Target, changes: Changes) -> float | None:
        """Log-likelihood of one claim's paper number at a configuration (its runs; the naive ones for {}), with the
        discrepancy floor."""
        vals = [b.parsed_metrics[c.metric] for b in self.measure_ok(changes) if c.metric in b.parsed_metrics]
        if not vals:
            return None
        sd = self._claim_sd(c)
        v = sd * sd / len(vals) + sd * sd / self.cfg.hm_paper_n + (self.cfg.hm_disc * c.paper_value) ** 2
        m = statistics.fmean(vals)
        return -0.5 * (c.paper_value - m) ** 2 / v - 0.5 * math.log(2 * math.pi * v)

    async def _discriminate(self, t: Target, res: ClaimResult) -> None:
        """Plan D2.2: configurations the target can't tell apart, run where the paper's other reported conditions
        tell them apart best (gapfinder/diagnose/discriminate.py), until one holds discriminate_stop of the
        posterior; that one is then confirmed and verified like any answer."""
        from gapfinder.diagnose import discriminate as D

        if not self.cfg.discriminate or len(res.equivalent) < 2 or res.status == "partial":
            return
        pts = {p.claim_id: p for p in self._usable_points()}
        if not pts:
            return
        cfgs = [dict(e["config"]) for e in res.equivalent][:8]
        await self._measure_points([], "point (as run)")
        conds = []
        for p in pts.values():
            nv = [b.parsed_metrics[p.metric] for b in self.measure_ok(self._point_config(p, {})) if p.metric in b.parsed_metrics]
            if not nv:
                continue
            sd = max(statistics.stdev(nv) if len(nv) >= 2 else 0.0,
                     self.bands[p.metric].band / 2 if p.metric in self.bands else 0.0,
                     self.cfg.noise_floor_frac * abs(p.paper_value), 1e-12)
            conds.append(D.Condition(p.claim_id, p.paper_value, statistics.fmean(nv), sd,
                                     sd * sd / self.cfg.hm_paper_n + (self.cfg.hm_disc * p.paper_value) ** 2, p.metric))
        if not conds:
            return
        held = self._diag_claims(t)
        metrics = {c.metric for c in conds} | {t.metric}

        def cand(c: Changes) -> "D.Candidate":
            meas = {}
            for p in pts.values():
                vals = [b.parsed_metrics[p.metric] for b in self.measure_ok(self._point_config(p, c)) if p.metric in b.parsed_metrics]
                if vals:
                    meas[p.claim_id] = (statistics.fmean(vals), len(vals))
            eff = {m: (self.value(c, m) - self.naive[m]) for m in metrics
                   if self.value(c, m) is not None and self.naive.get(m) is not None}
            return D.Candidate(frozenset(c.items()), c, self._cand_prior(c), meas, eff.get(t.metric, 0.0), eff)

        base = {}
        for c in cfgs:
            lls = [self._claim_loglik(h, c) for h in held]
            base[frozenset(c.items())] = sum(x for x in lls if x is not None)
        start, cap = self.runs_used, int((self.cfg.max_runs or 10 ** 6) * self.cfg.discriminate_budget_frac)
        target_naive = self.naive.get(t.metric) or 0.0
        tests = []
        for _ in range(self.cfg.discriminate_rounds):
            cands = [cand(c) for c in cfgs]
            w = D.posterior(cands, conds, target_naive, base)
            if max(w.values()) >= self.cfg.discriminate_stop:
                break
            picks = D.choose(cands, conds, target_naive, self.cfg.discriminate_batch, 0.05, base)
            if not picks or self.runs_used - start + len(picks) * self.cfg.point_repeats > cap:
                break
            tests += [{"config": x.config, "condition": p.id, "bits": round(g, 3)} for x, p, g in picks]
            await _all(*(self.measure(self._point_config(pts[p.id], x.config), self.cfg.point_repeats,
                                      f"discriminate {p.id}") for x, p, g in picks))
        cands = [cand(c) for c in cfgs]
        w = D.posterior(cands, conds, target_naive, base)
        ranked = sorted(cands, key=lambda x: -w[x.key])
        res.discrimination = {"posterior": [{"config": x.config, "posterior": round(w[x.key], 4), "prior": round(x.prior, 3)}
                                            for x in ranked], "tests": tests, "runs": self.runs_used - start,
                              "conditions": [p.id for p in conds]}
        lead = ranked[0]
        desc = lambda c: ", ".join(f"{k}={v}" for k, v in sorted(c.items())) or "as run"  # noqa: E731
        if w[lead.key] < self.cfg.discriminate_stop:
            res.notes.append(f"discrimination: the paper's other conditions ({', '.join(p.id for p in conds)}) don't yet "
                             "tell the equally good fits apart: " + "; ".join(
                                 f"{desc(x.config)} {w[x.key]:.0%}" for x in ranked[:3]))
            return
        res.notes.append(f"discrimination: the paper's other conditions favour {desc(lead.config)} "
                         f"(posterior {w[lead.key]:.0%} after {len(tests)} run(s) chosen by expected information)")
        if lead.config != dict(res.changes):
            old = dict(res.changes)
            await self._swap_to(t, res, lead.config,
                                f"discrimination favours {desc(lead.config)} over {desc(old)}",
                                f"{desc(old)} and {desc(lead.config)} fit the target equally well; the paper's other "
                                f"conditions favour {desc(lead.config)} (posterior {w[lead.key]:.0%}), so it is the "
                                "answer")
        order = {frozenset(x.config.items()): i for i, x in enumerate(ranked)}
        res.equivalent.sort(key=lambda e: (e["config"] != dict(res.changes), order.get(frozenset(e["config"].items()), 99)))

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
            if self._relation_broken_cached(c):  # the paper's stated relation reverses under it
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
            for f in ("attribution", "changes", "gap_after", "held_out", "counterfactual", "plausibility", "replay", "relations"):
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


_BOOL = {"true": "true", "yes": "true", "on": "true", "1": "true", "false": "false", "no": "false", "off": "false",
         "0": "false", "none": "none", "null": "none"}


def _same_value(a: str, b: str) -> bool:
    """One value in two spellings: '2' and '2.0', 'False' and 'false', 'none' and 'None'."""
    if a == b or _same_number(a, b):
        return True
    x, y = a.strip().strip("\"'").lower(), b.strip().strip("\"'").lower()
    return x == y or (x in _BOOL and y in _BOOL and _BOOL[x] == _BOOL[y] and not (_NUM.fullmatch(x) and _NUM.fullmatch(y)))


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


def _num(v) -> float | None:
    try:
        return float(str(v).strip())
    except (TypeError, ValueError):
        return None
