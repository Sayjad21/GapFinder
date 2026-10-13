"""Sealed random task generator for GapBench-mini.

    python eval/gapbench/gen_tasks.py --seed-file eval/gapbench/sealed/seed.txt

Everything that shapes the tasks is fixed by the constants below, so committing this file before the
seed exists pre-registers the test: the category quotas, the artifacts, the value pool of every knob,
the paper templates, and the validation thresholds. The seed only chooses among them.

Per draw, with one random.Random(seed): category (from the quota), then artifact, then the hidden
knob(s) and their values from the pools. A draw is rejected and redrawn (same category) unless it
passes make_task.py (gap over 3 noise bands), leakage.py (0 leaks) and the category checks in
the category checks in this file. Rejection counts and reasons go to the sealed folder only.

Outputs, under --out-root (default eval/gapbench):
    tasks/<id>/   paper.md, targets.json, calibration.json (repeats and naive medians only), task.yaml
                  (no hidden field), and spec.yaml for "incomplete" tasks. All GapFinder may see.
    sealed/<id>/  answer.json (with `category`), task.yaml (the hidden part) and the full calibration.json
                  (paper values, noise bands, gap in bands). Git-ignored.
    sealed/generation_log.json   attempts and rejections per task
    sealed.sha256 hash of sealed/ (sorted relative paths and contents, seed.txt left out)

The generator prints only the number of tasks and that hash.
"""

from __future__ import annotations

import asyncio
import contextlib
import contextvars
import hashlib
import json
import random
import re
import shutil
import statistics
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# make_task puts the repository root on sys.path, so it has to come before the gapfinder imports
import leakage
import make_task
import variants
from gapfinder.sandbox import runner as runner_mod
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.noise import noise_band
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.verify import held_out_ok

GB = Path(__file__).resolve().parent

# --------------------------------------------------------------------------- pre-registered constants

#: (category, task type, how many). 8 tasks. "known_cause" is one hidden setting, once left
#: unstated in the paper and once stated in words while the code default differs.
QUOTAS: tuple[tuple[str, str | None, int], ...] = (
    ("known_cause", "single_unstated", 1),
    ("known_cause", "stated_code_differs", 1),
    ("interaction", "interaction", 2),
    ("no_cause", "no_cause", 1),
    ("decoy", "single_unstated", 1),
    ("noise_only", "no_cause", 1),
    ("incomplete", "single_unstated", 1),
    ("out_of_space", "out_of_space", 2),
)

#: out_of_space: the paper's numbers come from an older, buggy copy of the artifact (eval/gapbench/variants.py:
#: patched copies, so the artifacts and GapFinder's view of them never change). No setting GapFinder can
#: change should explain them; the rival check still rejects any draw where one does. Only mlbench: see
#: variants.py for the rlbench candidates and why each was rejected.
OOS_VARIANTS: dict[str, list[str]] = {f: sorted(v) for f, v in variants.VARIANTS.items()}
OOS_OMITTED = 3  # knobs the paper leaves unstated, so the search has hypotheses to test and reject
N_TASKS = sum(q[2] for q in QUOTAS)

ARTIFACTS = ("rlbench", "mlbench")
REPEATS = {"rlbench": 11, "mlbench": 7}  # runs per configuration, as in the dev tasks
SPLIT = "test"
TASK_PREFIX = "test-gen-"

#: claims per artifact: C1 is the primary claim, C2 the held-out claim
CLAIMS = {
    "rlbench": [{"claim_id": "C1", "metric": "mean_reward", "figure": "Figure 1"},
                {"claim_id": "C2", "metric": "min_reward", "figure": "Figure 1", "held_out": True}],
    "mlbench": [{"claim_id": "C1", "metric": "test_accuracy", "figure": "Table 1"},
                {"claim_id": "C2", "metric": "balanced_accuracy", "figure": "Table 1", "held_out": True}],
}

#: Value pools: the values a knob may take as the hidden setting. Only values someone could write in a
#: paper or a config: argparse `choices`, common values, or factors of 2, 5 and 10 around the default.
#: Never arbitrary numbers. Seed-like and measurement-protocol knobs (seeds, eval_episodes, data_seed)
#: are not drawn. Every pool value differs from the knob's default.
POOLS: dict[str, dict[str, list[str]]] = {
    "rlbench": {
        "episodes": ["80", "200", "800"],                      # default 400: /5, /2, x2
        "gamma": ["0.9", "0.95", "0.999"],                     # default 0.99: common discounts
        "lr": ["0.02", "0.05", "0.2", "0.5"],                  # default 0.1: /5, /2, x2, x5
        "lr_schedule": ["linear", "inv"],                      # argparse choices
        "eps_start": ["0.5", "0.2", "0.1"],                    # default 1.0: /2, /5, /10
        "eps_end": ["0.01", "0.1", "0.25"],                    # default 0.05: /5, x2, x5
        "eps_decay": ["0.95", "0.98", "0.995", "0.999"],       # default 0.99: common decays
        "theta_bins": ["3", "12"],                             # default 6: /2, x2
        "omega_bins": ["3", "12"],                             # default 6: /2, x2
        "reward_norm": ["on"],                                 # argparse choices
        "max_steps": ["100", "500"],                           # default 200: /2, the CartPole-v1 cap
        "init_q": ["1.0", "10.0", "100.0"],                    # optimistic initialisation
    },
    "mlbench": {
        "n": ["600", "2400", "6000"],                          # default 1200: /2, x2, x5
        "positive_rate": ["0.1", "0.15", "0.5"],               # default 0.3: common class balances
        "label_noise": ["0.0", "0.01", "0.1", "0.25"],         # default 0.05: none, /5, x2, x5
        "split": ["0.7", "0.9"],                               # default 0.8: common train fractions
        "normalize": ["zscore", "minmax"],                     # argparse choices
        "epochs": ["3", "30", "75", "150"],                    # default 15: /5, x2, x5, x10
        "batch_size": ["8", "16", "64", "128"],                # default 32: powers of two
        "lr": ["0.01", "0.1", "0.25", "0.5"],                  # default 0.05: /5, x2, x5, x10
        "lr_schedule": ["step", "cosine"],                     # argparse choices
        "weight_decay": ["0.0001", "0.001", "0.01", "0.1"],    # common values
        "class_weight": ["balanced"],                          # argparse choices
        "threshold": ["0.3", "0.4", "0.6", "0.7"],             # default 0.5: common cut-offs
    },
}

#: no_cause: the paper's numbers are the naive numbers times one of these factors. The primary claim
#: moves one way and the held-out claim the other, so no single knob should fit both.
OFFSET_POOLS: dict[str, dict[str, list[float]]] = {
    "rlbench": {"mean_reward": [0.3, 0.4, 0.5], "min_reward": [1.15, 1.3, 1.5]},
    "mlbench": {"test_accuracy": [1.25, 1.35, 1.45], "balanced_accuracy": [0.8, 0.85, 0.9]},
}

#: noise_only: the paper's numbers sit this many noise bands (uniform in +-) from the naive median
NOISE_ONLY_DRAW_BANDS = 0.8
NOISE_ONLY_MAX_UNITS = 1.0     # validation: every claim within this many bands of naive
MIN_UNITS = 3.0                # a task with a cause needs a primary gap over this many noise bands
SUFFICIENT_CLOSURE = 0.5       # "moves the target": a single knob covers this share of the gap, or lands
                               # within one noise band of the paper's number. Used for "one knob alone is
                               # enough" (interaction) and for decoys. A rival, a second answer that would
                               # also explain the claim, must reproduce it: land within one noise band.
MAX_ATTEMPTS = 250             # draws per task before this round is abandoned (most random draws are
                               # rejected: a knob that does nothing can't make a task)
MAX_RESTARTS = 8               # if a category can't be filled, the whole generation restarts with the
                               # measurement noise re-rolled ("<seed>#retry<k>"). The artifacts are noisy
                               # enough that some noise draws leave a category with no valid task. The
                               # number of restarts is recorded in the sealed log.
DECOY_DRAWS = 30               # random decoy candidates tried per attempt
RIVALS_OVER_SEARCH_SPACE = True  # rivals are checked over every value GapFinder can test (pools plus its
                                 # coverage values: choices, log ladder, multiplier factors), not only the
                                 # pools: on test-gen-05, eps_start=0.0 (a ladder value outside the pool)
                                 # explained both claims better than the planted pair

# --------------------------------------------------------------------------- paper templates


def join_and(items: list[str]) -> str:
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def _pct(v: str) -> str:
    return f"{float(v) * 100:g}%"


def rl_learning_rate(lr: str | None, sched: str | None) -> str | None:
    """Phrase for learning rate + schedule; None when the paper says nothing about either."""
    if lr is None and sched is None:
        return None
    if sched is None:
        return f"a learning rate of {lr}"
    if sched == "const":
        return "a constant learning rate" + (f" of {lr}" if lr else "")
    if sched == "linear":
        start = f"starts at {lr} and " if lr else ""
        return f"a learning rate that {start}decays linearly to nearly zero over training"
    if sched == "inv":
        if lr:
            return f"a learning rate that starts at {lr} and decays as {lr}/(1 + t/50) with training episode t"
        return "a learning rate that decays as its initial value divided by (1 + t/50) with training episode t"
    raise ValueError(sched)


def ml_learning_rate(lr: str | None, sched: str | None) -> str | None:
    if lr is None and sched is None:
        return None
    if sched is None:
        return f"learning rate {lr}"
    if sched == "const":
        return "a constant learning rate" + (f" of {lr}" if lr else "")
    if sched == "step":
        return (f"learning rate {lr}, " if lr else "a learning rate ") + "multiplied by 0.1 for the final third of training"
    if sched == "cosine":
        return (f"learning rate {lr} " if lr else "a learning rate ") + "with cosine decay to zero"
    raise ValueError(sched)


def rl_setup(v: dict[str, str | None]) -> str:
    """Setup section of an rlbench paper. v maps every knob to the value the paper states, or None
    when the paper stays silent about it."""
    out = []
    first = "Classic CartPole dynamics"
    if v["max_steps"] is not None:
        first += f", with episodes capped at {v['max_steps']} steps"
    out.append(first + ".")
    bins = [f"{v[k]} {name} bins" for k, name in (("theta_bins", "pole-angle"), ("omega_bins", "angular-velocity"))
            if v[k] is not None]
    if bins:
        out.append(f"States are discretised into {join_and(bins)}.")
    agent = "The agent is tabular Q-learning"
    if v["gamma"] is not None:
        agent += f" with discount {v['gamma']}"
    out.append(agent + ".")
    eps = []
    if v["eps_start"] is not None:
        eps.append(f"starts at {v['eps_start']}")
    if v["eps_decay"] is not None:
        eps.append(f"decays by a factor of {v['eps_decay']} per episode")
    if v["eps_end"] is not None:
        eps.append(f"is floored at {v['eps_end']}")
    out.append("Exploration is epsilon-greedy" + (f"; epsilon {join_and(eps)}" if eps else "") + ".")
    lr = rl_learning_rate(v["lr"], v["lr_schedule"])
    if lr:
        out.append(f"Q-values are updated with {lr}.")
    if v["init_q"] is not None:
        out.append("Q-values are initialised to " + ("zero" if float(v["init_q"]) == 0 else v["init_q"]) + ".")
    if v["reward_norm"] is not None:
        out.append("Rewards are used unnormalised." if v["reward_norm"] == "off"
                   else "Rewards are divided by the episode step cap.")
    train = f"We train for {v['episodes']} episodes" if v["episodes"] is not None else "We train one agent per seed"
    out.append(f"{train} and evaluate the greedy policy for {v['eval_episodes']} episodes, "
               f"averaging over {v['seeds']} random seeds.")
    return " ".join(out)


_NORMALIZE_TEXT = {
    "none": "Features are used raw, without any scaling.",
    "zscore": "Features are standardised to zero mean and unit variance using training-set statistics.",
    "minmax": "Features are rescaled to the unit interval using training-set minima and maxima.",
}


def ml_setup(v: dict[str, str | None]) -> str:
    out = []
    data = "The synthetic dataset has " + (f"{int(v['n']):,} rows with " if v["n"] is not None else "") + \
        "eight numeric features"
    extras = []
    if v["positive_rate"] is not None:
        extras.append(f"a {_pct(v['positive_rate'])} positive rate")
    if v["label_noise"] is not None:
        extras.append("no label noise" if float(v["label_noise"]) == 0 else f"{_pct(v['label_noise'])} label noise")
    out.append(data + (", " + join_and(extras) if extras else "") + ".")
    if v["split"] is not None:
        part = f"The first {_pct(v['split'])} of rows are used for training and the rest for testing"
    else:
        part = "Rows are divided in order into a training part and a test part"
    out.append(part + f" (data seed {v['data_seed']}).")
    if v["normalize"] is not None:
        out.append(_NORMALIZE_TEXT[v["normalize"]])
    items = []
    if v["batch_size"] is not None:
        items.append(f"batch size {v['batch_size']}")
    lr = ml_learning_rate(v["lr"], v["lr_schedule"])
    if lr:
        items.append(lr)
    if v["weight_decay"] is not None:
        items.append("no weight decay" if float(v["weight_decay"]) == 0 else f"weight decay {v['weight_decay']}")
    if v["class_weight"] is not None:
        items.append("no class weighting" if v["class_weight"] == "none" else "inverse-frequency class weighting")
    model = "The model is logistic regression trained by mini-batch SGD"
    if v["epochs"] is not None:
        model += f" for {v['epochs']} epochs"
    out.append(model + (f" ({join_and(items)})" if items else "") + ".")
    if v["threshold"] is not None:
        out.append(f"Predictions use a decision threshold of {v['threshold']}.")
    return " ".join(out)


TITLES = {
    "rlbench": ["Stable Tabular Control on CartPole", "A Tabular Q-Learner Is Enough for CartPole",
                "Discretised Q-Learning for Pole Balancing"],
    "mlbench": ["Plain Logistic Regression Is a Strong Baseline for Credit Screening",
                "Logistic Regression with SGD for Imbalanced Tabular Screening",
                "A Simple Baseline for Synthetic Credit Data"],
}
ABSTRACTS = {
    "rlbench": ["We show that a small tabular Q-learner balances CartPole for a mean of {mean_reward:.1f} steps, "
                "and that its worst seed still balances for {min_reward:.1f}.",
                "A tabular Q-learner over a coarse state grid reaches a mean reward of {mean_reward:.1f} on "
                "CartPole; the worst of its seeds reaches {min_reward:.1f}."],
    "mlbench": ["We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and "
                "show that it reaches {test_accuracy:.3f} test accuracy.",
                "A plain logistic-regression baseline reaches {test_accuracy:.3f} test accuracy and "
                "{balanced_accuracy:.3f} balanced accuracy on a synthetic screening task."],
}
RESULTS = {
    "rlbench": "Figure 1 (final evaluation): mean reward {mean_reward:.1f}; worst seed {min_reward:.1f}.",
    "mlbench": ("Table 1 reports the main result: test accuracy {test_accuracy:.3f}, balanced accuracy "
                "{balanced_accuracy:.3f}.\n\n| Model | Test accuracy | Balanced accuracy |\n|---|---|---|\n"
                "| Logistic regression (ours) | {test_accuracy:.3f} | {balanced_accuracy:.3f} |"),
}
SETUP = {"rlbench": rl_setup, "mlbench": ml_setup}
RUNS_SENTENCE = {"rlbench": "", "mlbench": " Numbers are medians over {repeats} runs with different shuffling seeds."}


def paper_template(family: str, values: dict[str, str | None], title_i: int, abstract_i: int) -> str:
    """The mini-paper with {metric:.3f}-style placeholders (make_task fills them in). `values` maps
    every knob of the artifact to the value stated in the paper, or None if the paper is silent."""
    setup = SETUP[family](values) + RUNS_SENTENCE[family].format(repeats=REPEATS[family])
    return (f"# {TITLES[family][title_i]}\n\n## Abstract\n{ABSTRACTS[family][abstract_i]}\n\n"
            f"## Experimental setup\n{setup}\n\n## Results\n{RESULTS[family]}\n")


def quota_slots(rng: random.Random, quotas=QUOTAS) -> list[tuple[str, str | None]]:
    """The category of each task, in a seed-dependent order (so task numbers don't reveal categories)."""
    slots = [(cat, typ) for cat, typ, n in quotas for _ in range(n)]
    rng.shuffle(slots)
    return slots


# --------------------------------------------------------------------------- planning one draw

_DEFAULTS: dict[str, dict[str, str]] = {}


def spec_defaults(family: str) -> dict[str, str]:
    if family not in _DEFAULTS:
        spec = HarnessSpec.load_yaml(GB / f"{family}.yaml")
        _DEFAULTS[family] = {k: kn.default for k, kn in spec.knobs.items()}
    return _DEFAULTS[family]


@dataclass
class Plan:
    """One draw: everything the generator chooses before measuring anything."""
    category: str
    type: str                                   # task type for the answer key (known to score.py)
    family: str
    title_i: int
    abstract_i: int
    hidden: dict[str, str] = field(default_factory=dict)   # true setting(s); {} for abstention tasks
    stated: list[str] = field(default_factory=list)        # knobs the paper states in words (hidden value)
    omitted: list[str] = field(default_factory=list)       # knobs the paper stays silent about
    offset: dict[str, float] = field(default_factory=dict)  # paper numbers = naive numbers x factor
    noise_u: dict[str, float] = field(default_factory=dict)  # noise_only: offset in noise bands
    decoy: dict[str, str] = field(default_factory=dict)
    unexposed: list[str] = field(default_factory=list)     # knobs removed from the task's spec
    variant: str = ""                                      # out_of_space: the code-level bug behind the paper

    def paper_values(self) -> dict[str, str | None]:
        vals: dict[str, str | None] = dict(spec_defaults(self.family))
        for k in self.omitted:
            vals[k] = None
        for k in self.stated:
            vals[k] = self.hidden[k]
        return vals

    def paper(self) -> str:
        return paper_template(self.family, self.paper_values(), self.title_i, self.abstract_i)


def draw_plan(rng: random.Random, category: str, typ: str, artifacts=ARTIFACTS) -> Plan:
    """Category is given by the quota; the artifact, then the hidden knob(s) and values come from rng."""
    family = rng.choice([a for a in artifacts if a in OOS_VARIANTS] if category == "out_of_space" else artifacts)
    pools = POOLS[family]
    eligible = sorted(pools)
    plan = Plan(category, typ, family, rng.randrange(len(TITLES[family])), rng.randrange(len(ABSTRACTS[family])))
    metrics = [c["metric"] for c in CLAIMS[family]]
    if category == "interaction":
        for k in rng.sample(eligible, 2):
            plan.hidden[k] = rng.choice(pools[k])
        plan.omitted = list(plan.hidden)
    elif category in ("known_cause", "decoy", "incomplete"):
        k = rng.choice(eligible)
        plan.hidden[k] = rng.choice(pools[k])
        if typ == "stated_code_differs":
            plan.stated = [k]
        else:
            plan.omitted = [k]
        if category == "incomplete":
            plan.unexposed = [k]
    elif category == "no_cause":
        plan.offset = {m: rng.choice(OFFSET_POOLS[family][m]) for m in metrics}
    elif category == "out_of_space":
        plan.variant = rng.choice(OOS_VARIANTS[family])
        plan.omitted = rng.sample(eligible, OOS_OMITTED)
    elif category == "noise_only":
        plan.noise_u = {m: round(rng.uniform(-NOISE_ONLY_DRAW_BANDS, NOISE_ONLY_DRAW_BANDS), 3) for m in metrics}
    else:
        raise ValueError(category)
    return plan


# --------------------------------------------------------------------------- deterministic measuring
# The artifacts seed their randomness from RUN_TAG, which the orchestrator makes a fresh uuid per run.
# For the generator, RUN_TAG is a hash of (seed, artifact, configuration, repeat index) instead, so every
# measurement, and therefore every calibration number, is reproducible from the seed alone.

_DET_TAG: contextvars.ContextVar[str | None] = contextvars.ContextVar("gapbench_gen_tag", default=None)


class DetOrchestrator(Orchestrator):
    salt = ""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._det_counts: dict[str, int] = {}

    async def run_branch(self, changes, **kw):
        key = json.dumps(sorted(changes.items()))
        i = self._det_counts.get(key, 0)
        self._det_counts[key] = i + 1
        tag = hashlib.sha256(f"{self.salt}|{self.spec.name}|{key}|{i}".encode()).hexdigest()[:12]
        token = _DET_TAG.set(tag)
        try:
            return await super().run_branch(changes, **kw)
        finally:
            _DET_TAG.reset(token)


@contextlib.contextmanager
def deterministic_runs(seed: str):
    """Patch the orchestrator for the duration of a generation (and restore it, so tests stay isolated)."""
    orig_tag, orig_orch, orig_salt = runner_mod._tag, make_task.Orchestrator, DetOrchestrator.salt
    runner_mod._tag = lambda: _DET_TAG.get() or orig_tag()
    make_task.Orchestrator = DetOrchestrator
    DetOrchestrator.salt = seed
    try:
        yield
    finally:
        runner_mod._tag, make_task.Orchestrator, DetOrchestrator.salt = orig_tag, orig_orch, orig_salt


def _key(changes: dict[str, str]) -> str:
    return json.dumps(sorted(changes.items()))


class Measurer:
    """Runs configurations on the local backend, once each, and keeps every run's metrics."""

    def __init__(self, tmp: Path):
        self.tmp = tmp
        self._orch: dict[str, DetOrchestrator] = {}
        self._runs: dict[tuple[str, str], dict[str, list[float]]] = {}
        self._pooled: set[str] = set()

    def _orchestrator(self, family: str, variant: str = "") -> DetOrchestrator:
        name = f"{family}-{variant}" if variant else family
        if name not in self._orch:
            spec = HarnessSpec.load_yaml(GB / f"{family}.yaml")
            if variant:  # out_of_space: the buggy copy, same knobs and command
                spec = variants.spec_for(spec, family, variant, self.tmp / "variants")
            self._orch[name] = DetOrchestrator(LocalBackend(self.tmp / f"sbx-{name}"), spec,
                                               EventLog(self.tmp / f"{name}.jsonl"))
        return self._orch[name]

    async def measure(self, family: str, changes: dict[str, str], variant: str = "") -> dict[str, list[float]]:
        key = (family + (f"@{variant}" if variant else ""), _key(changes))
        if key not in self._runs:
            branches = await self._orchestrator(family, variant).fanout([dict(changes)] * REPEATS[family])
            metrics = [c["metric"] for c in CLAIMS[family]]
            self._runs[key] = {m: [b.parsed_metrics[m] for b in branches if m in b.parsed_metrics] for m in metrics}
        return self._runs[key]

    async def ensure_pool(self, family: str) -> None:
        """Measure the naive configuration and every single (knob, value) GapFinder could test."""
        if family in self._pooled:
            return
        configs = [{}] + [{k: v} for k, vs in sorted(rival_values(family).items()) for v in vs]
        await asyncio.gather(*(self.measure(family, c) for c in configs))
        self._pooled.add(family)

    def median(self, family: str, changes: dict[str, str], metric: str) -> float | None:
        vals = self._runs[(family, _key(changes))][metric]
        return statistics.median(vals) if vals else None

    def band(self, family: str, metric: str) -> float:
        return noise_band(metric, self._runs[(family, _key({}))][metric], floor_frac=0.01).band


# --------------------------------------------------------------------------- category checks


def closes_gap(naive: float, paper: float, measured: float, band: float, *, partial: bool = True) -> bool:
    """A configuration closes the gap if it gets within one noise band of the paper's number (the search
    engine's own test) or, with `partial`, covers at least SUFFICIENT_CLOSURE of the distance from the
    naive number."""
    gap0, gap = abs(naive - paper), abs(measured - paper)
    return gap <= band or (partial and gap0 > 0 and 1 - gap / gap0 >= SUFFICIENT_CLOSURE)


def breaks_held_out(naive: float, paper: float, measured: float, band: float) -> bool:
    """The search engine's own rule: a held-out claim must not get worse by more than its noise band."""
    return not held_out_ok(naive - paper, measured - paper, band)


class Screen:
    """The numbers one draw is judged on, read from the measurer's cache."""

    def __init__(self, mz: Measurer, plan: Plan, paper: dict[str, float]):
        self.mz, self.plan, self.paper = mz, plan, paper
        claims = CLAIMS[plan.family]
        self.primary, self.held = claims[0]["metric"], claims[1]["metric"]

    def _naive(self, metric: str) -> float:
        return self.mz.median(self.plan.family, {}, metric)

    def units(self, metric: str) -> float:
        band = self.mz.band(self.plan.family, metric)
        gap = abs(self.paper[metric] - self._naive(metric))
        return gap / band if band else float("inf")

    def single_closes_primary(self, knob: str, value: str, *, partial: bool = True) -> bool:
        m = self.mz.median(self.plan.family, {knob: value}, self.primary)
        return m is not None and closes_gap(self._naive(self.primary), self.paper[self.primary], m,
                                            self.mz.band(self.plan.family, self.primary), partial=partial)

    def single_breaks_held_out(self, knob: str, value: str) -> bool:
        m = self.mz.median(self.plan.family, {knob: value}, self.held)
        return m is not None and breaks_held_out(self._naive(self.held), self.paper[self.held], m,
                                                 self.mz.band(self.plan.family, self.held))

    def single_reproduces_held_out(self, knob: str, value: str) -> bool:
        m = self.mz.median(self.plan.family, {knob: value}, self.held)
        return m is not None and closes_gap(self._naive(self.held), self.paper[self.held], m,
                                            self.mz.band(self.plan.family, self.held), partial=False)

    def rivals(self, skip: set[tuple[str, str]], skip_knobs: set[str] = frozenset()) -> list[tuple[str, str]]:
        """Single pool settings that reproduce both claims (each within one noise band of the paper's
        number): a second, equally good answer the key doesn't name."""
        return [(k, v) for k, vs in sorted(rival_values(self.plan.family).items()) for v in vs
                if (k, v) not in skip and k not in skip_knobs
                and self.single_closes_primary(k, v, partial=False) and self.single_reproduces_held_out(k, v)]


_RIVAL_CACHE: dict[str, dict[str, list[str]]] = {}


def rival_values(family: str) -> dict[str, list[str]]:
    """Per poolable knob: its pool values plus the values GapFinder's search would also try (v1.1 value
    coverage), so a planted answer is only accepted if nothing GapFinder tests explains the claims as well."""
    if family in _RIVAL_CACHE:
        return _RIVAL_CACHE[family]
    out = {k: list(vs) for k, vs in POOLS[family].items()}
    if RIVALS_OVER_SEARCH_SPACE:
        from gapfinder.ingest.config_flow import flag_scales
        from gapfinder.ingest.repo_map import build_repo_map
        from gapfinder.search.hypotheses import coverage_values, fill_choices, mark_multipliers_from_flow

        spec = HarnessSpec.load_yaml(GB / f"{family}.yaml")
        root = Path(str(spec.base).removeprefix("local:"))
        fill_choices(spec, build_repo_map(root).flags)
        mark_multipliers_from_flow(spec, flag_scales(root))
        for k in out:
            knob = spec.knobs[k]
            for v in coverage_values(knob)[:6]:
                if v != knob.default and v not in out[k] and knob.affordable(v):
                    out[k].append(v)
    _RIVAL_CACHE[family] = out
    return out


# --------------------------------------------------------------------------- files of one task


def public_spec(family: str, unexposed: list[str]) -> str:
    """The family spec without the unexposed knobs (flag and placeholder removed from the command)."""
    data = yaml.safe_load((GB / f"{family}.yaml").read_text(encoding="utf-8"))
    cmd = data["run"]["command"]
    for k in unexposed:
        new = re.sub(rf"\s--{re.escape(k)}\s+\{{{re.escape(k)}\}}", "", cmd)
        if new == cmd:
            raise ValueError(f"knob {k} not found in the run command")
        cmd = new
        del data["knobs"][k]
    data["run"]["command"] = cmd
    data["base"] = f"local:../../artifacts/{family}"
    return "# Harness spec for this task. Knobs and defaults only.\n" + _dump(data)


def _dump(obj) -> str:
    return yaml.safe_dump(obj, sort_keys=False, width=10**6, allow_unicode=True)


def public_task(task_id: str, plan: Plan) -> dict:
    t = {"id": task_id, "family": plan.family, "split": SPLIT, "repeats": REPEATS[plan.family],
         "claims": CLAIMS[plan.family]}
    if plan.unexposed:
        t["spec"] = "spec.yaml"
    return t


#: Categories scored as abstention are `no_cause` in the answer key (what score.py understands);
#: `category` carries the real one.
ANSWER_TYPE = {"noise_only": "no_cause", "incomplete": "no_cause", "out_of_space": "no_cause"}


def answer_key(task_id: str, plan: Plan) -> dict:
    atype = ANSWER_TYPE.get(plan.category, plan.type)
    a = {"id": task_id, "type": atype, "category": plan.category, "hidden": plan.hidden,
         "expected_label": "Reproduced" if plan.category == "noise_only" else make_task.EXPECTED[atype],
         "primary_claims": ["C1"]}
    if plan.category == "noise_only":
        a["acceptable_labels"] = ["Reproduced", "Inconclusive"]
    if plan.decoy:
        a["decoy"] = plan.decoy
    if plan.unexposed:
        a["unexposed"] = plan.unexposed
    if plan.variant:
        a["cause_family"] = variants.describe(plan.family, plan.variant)
        a["variant"] = plan.variant
    return a


def sealed_task(task_id: str, plan: Plan) -> dict:
    """The hidden part of task.yaml."""
    t = {"id": task_id, "category": plan.category, "type": plan.type, "hidden": plan.hidden}
    for name in ("stated", "omitted", "offset", "noise_u", "decoy", "unexposed", "variant"):
        if getattr(plan, name):
            t[name] = getattr(plan, name)
    return t


# --------------------------------------------------------------------------- validating and building a draw


class Reject(Exception):
    """A draw failed validation; `reason` is recorded in the sealed log only."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


@dataclass
class Done:
    task_id: str
    plan: Plan
    staged: Path
    attempts: int
    rejections: dict[str, int]


class Generator:
    def __init__(self, seed: str, tmp: Path, artifacts=ARTIFACTS, quotas=QUOTAS):
        self.rng = random.Random(seed)
        self.artifacts, self.quotas = tuple(artifacts), quotas
        self.mz = Measurer(tmp / "measure")
        self.stage = tmp / "stage"

    async def screen(self, plan: Plan) -> dict[str, float]:
        """Cheap checks from cached measurements. Returns the paper's numbers or raises Reject."""
        fam, cat = plan.family, plan.category
        await self.mz.ensure_pool(fam)
        metrics = [c["metric"] for c in CLAIMS[fam]]
        naive = {m: self.mz.median(fam, {}, m) for m in metrics}
        if None in naive.values():
            raise Reject("naive_runs_failed")
        if plan.noise_u:
            plan.offset = {m: round(1 + u * self.mz.band(fam, m) / naive[m], 6) for m, u in plan.noise_u.items()}
        if plan.offset:
            paper = {m: round(naive[m] * plan.offset[m], 4) for m in metrics}
        elif plan.variant:
            runs = await self.mz.measure(fam, {}, plan.variant)
            paper = {m: statistics.median(runs[m]) if runs[m] else None for m in metrics}
            if None in paper.values():
                raise Reject("variant_runs_failed")
            paper = {m: round(v, 4) for m, v in paper.items()}
        else:
            await self.mz.measure(fam, plan.hidden)
            paper = {m: self.mz.median(fam, plan.hidden, m) for m in metrics}
            if None in paper.values():
                raise Reject("hidden_runs_failed")
            paper = {m: round(v, 4) for m, v in paper.items()}
        sc = Screen(self.mz, plan, paper)
        if cat == "noise_only":
            if any(sc.units(m) > NOISE_ONLY_MAX_UNITS for m in metrics):
                raise Reject("paper_value_outside_noise")
            return paper
        if sc.units(sc.primary) < MIN_UNITS:
            raise Reject("gap_under_3_noise_bands")
        if cat == "interaction" and any(sc.single_closes_primary(k, v, partial=False) for k, v in plan.hidden.items()):
            raise Reject("one_knob_alone_closes_gap")
        if sc.rivals(set(plan.hidden.items()), set(plan.unexposed)):
            raise Reject("rival_single_knob_explains_claim")
        if cat == "decoy":
            plan.decoy = self.find_decoy(sc)
            plan.omitted.append(next(iter(plan.decoy)))
        return paper

    def find_decoy(self, sc: Screen) -> dict[str, str]:
        """A random other knob value that closes the primary gap but breaks the held-out claim."""
        pools = POOLS[sc.plan.family]
        others = [k for k in sorted(pools) if k not in sc.plan.hidden]
        for _ in range(DECOY_DRAWS):
            k = self.rng.choice(others)
            v = self.rng.choice(pools[k])
            if sc.single_closes_primary(k, v) and sc.single_breaks_held_out(k, v):
                return {k: v}
        raise Reject("no_decoy_found")

    async def build(self, task_id: str, plan: Plan, paper: dict[str, float]) -> Path:
        """The real checks: make_task.py (gap over 3 noise bands) and leakage.py (0 leaks)."""
        d = self.stage / task_id
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        task = {**public_task(task_id, plan), "type": plan.type, "hidden": plan.hidden}
        if plan.variant:
            task["variant"] = plan.variant
        if plan.offset:
            task["offset"] = plan.offset
        task["paper"] = plan.paper()
        (d / "task.yaml").write_text(_dump(task), encoding="utf-8", newline="\n")
        try:
            await make_task.build(d, 0.0 if plan.category == "noise_only" else MIN_UNITS)
        except SystemExit:
            raise Reject("make_task_rejected_gap") from None
        calib = json.loads((d / "calibration.json").read_text(encoding="utf-8"))["metrics"]
        if any(calib[m]["paper"] != v for m, v in paper.items()):
            raise Reject("make_task_disagrees_with_screen")
        if plan.category == "noise_only" and any(c["units"] > NOISE_ONLY_MAX_UNITS for c in calib.values()):
            raise Reject("paper_value_outside_noise")
        if leakage.check_task(d):
            raise Reject("leakage")
        return d

    async def make_one(self, index: int, category: str, typ: str) -> Done:
        task_id = f"{TASK_PREFIX}{index + 1:02d}"
        rejections: dict[str, int] = {}
        for attempt in range(1, MAX_ATTEMPTS + 1):
            plan = draw_plan(self.rng, category, typ, self.artifacts)
            try:
                if plan.variant and (plan.family, plan.variant) in self.used_variants:
                    raise Reject("variant_already_used")  # two out-of-space tasks must be two different bugs
                paper = await self.screen(plan)
                staged = await self.build(task_id, plan, paper)
            except Reject as r:
                rejections[r.reason] = rejections.get(r.reason, 0) + 1
                continue
            if plan.variant:
                self.used_variants.add((plan.family, plan.variant))
            return Done(task_id, plan, staged, attempt, rejections)
        raise GenerationFailed(task_id, rejections, category)

    async def run(self) -> list[Done]:
        """Fill every slot. Progress goes to stderr and says nothing about categories, knobs or values."""
        slots = quota_slots(self.rng, self.quotas)
        self.used_variants: set[tuple[str, str]] = set()
        done: list[Done] = []
        attempts = 0
        for i, (cat, typ) in enumerate(slots):
            try:
                task = await self.make_one(i, cat, typ)
            except GenerationFailed:
                print(f"task {i + 1}/{len(slots)} could not be filled, attempts so far "
                      f"{attempts + MAX_ATTEMPTS}", file=sys.stderr, flush=True)
                raise
            done.append(task)
            attempts += task.attempts
            print(f"task {i + 1}/{len(slots)} filled, attempts so far {attempts}", file=sys.stderr, flush=True)
        return done


class GenerationFailed(RuntimeError):
    def __init__(self, task_id: str, rejections: dict[str, int], category: str):
        super().__init__(f"{task_id}: no valid draw after {MAX_ATTEMPTS} attempts")
        self.rejections, self.category = rejections, category


# --------------------------------------------------------------------------- writing, hashing, CLI


def hash_tree(root: Path, exclude: tuple[str, ...] = ("seed.txt",)) -> str:
    """sha256 over sorted relative paths and file contents. Top-level files named in `exclude` are
    skipped, so the hash is the same whether the seed came from a file or the command line."""
    h = hashlib.sha256()
    files = sorted((p.relative_to(root).as_posix(), p) for p in root.rglob("*") if p.is_file())
    for rel, p in files:
        if rel in exclude:
            continue
        data = p.read_bytes()
        h.update(rel.encode("utf-8") + b"\0" + str(len(data)).encode() + b"\0" + data)
    return h.hexdigest()


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def existing_outputs(out_root: Path) -> list[Path]:
    return [p for sub in ("tasks", "sealed") if (out_root / sub).is_dir()
            for p in (out_root / sub).glob(f"{TASK_PREFIX}*")]


def write_outputs(out_root: Path, done: list[Done], overwrite: bool = False, restarts: int = 0) -> str:
    """Write task folders and the sealed folder; return the sealed folder's hash."""
    old = existing_outputs(out_root)
    if old and not overwrite:
        raise FileExistsError(f"{out_root} already holds generated tasks; pass --overwrite to replace them")
    for p in old:
        shutil.rmtree(p)
    tasks, sealed = out_root / "tasks", out_root / "sealed"
    log = {}
    for d in done:
        t = tasks / d.task_id
        for name in ("paper.md", "targets.json"):
            t.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(d.staged / name, t / name)
        # make_task's calibration says how far the paper value sits from the naive run in noise bands,
        # which gives away noise_only and no_cause tasks. Only the naive medians stay public.
        calib = json.loads((d.staged / "calibration.json").read_text(encoding="utf-8"))
        public = {"repeats": calib["repeats"],
                  "metrics": {m: {"naive": c["naive"]} for m, c in calib["metrics"].items()}}
        _write(t / "calibration.json", json.dumps(public, indent=1))
        _write(sealed / d.task_id / "calibration.json", (d.staged / "calibration.json").read_text(encoding="utf-8"))
        _write(t / "task.yaml", _dump(public_task(d.task_id, d.plan)))
        if d.plan.unexposed:
            _write(t / "spec.yaml", public_spec(d.plan.family, d.plan.unexposed))
        _write(sealed / d.task_id / "answer.json", json.dumps(answer_key(d.task_id, d.plan), indent=1))
        _write(sealed / d.task_id / "task.yaml", _dump(sealed_task(d.task_id, d.plan)))
        log[d.task_id] = {"category": d.plan.category, "type": d.plan.type, "artifact": d.plan.family,
                          "attempts": d.attempts, "rejections": d.rejections}
    _write(sealed / "generation_log.json", json.dumps({"restarts": restarts, "tasks": log}, indent=1))
    digest = hash_tree(sealed)
    _write(out_root / "sealed.sha256", digest + "\n")
    return digest


async def _generate(seed: str, out_root: Path, artifacts, quotas, overwrite: bool) -> tuple[int, str]:
    if existing_outputs(out_root) and not overwrite:  # fail before the slow part
        raise FileExistsError(f"{out_root} already holds generated tasks; pass --overwrite to replace them")
    failure = None
    for restart in range(MAX_RESTARTS + 1):
        salt = seed if restart == 0 else f"{seed}#retry{restart}"
        with deterministic_runs(salt), tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
            try:
                done = await Generator(salt, Path(tmp), artifacts, quotas).run()
            except GenerationFailed as exc:
                failure = exc
                print(f"restart {restart + 1}/{MAX_RESTARTS}: re-rolling the measurement noise",
                      file=sys.stderr, flush=True)
                continue
            return len(done), write_outputs(out_root, done, overwrite, restart)
    raise failure


def generate(seed: str, out_root: Path = GB, *, artifacts=ARTIFACTS, quotas=QUOTAS, overwrite: bool = False
             ) -> tuple[int, str]:
    """Generate the tasks for `seed` into `out_root`; returns (number of tasks, sha256 of sealed/)."""
    return asyncio.run(_generate(str(seed).strip(), Path(out_root), artifacts, quotas, overwrite))


def main(argv=None) -> int:
    import argparse

    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--seed-file", type=Path, help="file holding the seed, e.g. eval/gapbench/sealed/seed.txt")
    src.add_argument("--seed", help="the seed itself (use --seed-file for the real one)")
    p.add_argument("--n", type=int, default=N_TASKS, help=f"number of tasks; the quotas fix it at {N_TASKS}")
    p.add_argument("--out-root", type=Path, default=GB, help="where tasks/, sealed/ and sealed.sha256 go")
    p.add_argument("--overwrite", action="store_true", help="replace generated tasks already in --out-root")
    p.add_argument("--debug", action="store_true", help="on failure, print the rejection reasons (never with the real seed)")
    a = p.parse_args(argv)
    if a.n != N_TASKS:
        p.error(f"--n must be {N_TASKS}: the category quotas are pre-registered for {N_TASKS} tasks")
    seed = a.seed_file.read_text(encoding="utf-8").strip() if a.seed_file else a.seed
    if not seed:
        p.error("empty seed")
    try:
        n, digest = generate(seed, a.out_root, overwrite=a.overwrite)
    except GenerationFailed as exc:
        print(f"generation failed: {exc}", file=sys.stderr)
        if a.debug:
            print(f"category {exc.category}, rejections: {exc.rejections}", file=sys.stderr)
        return 1
    print(f"{n} tasks, sealed sha256 {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
