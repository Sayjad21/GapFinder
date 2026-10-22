"""Discriminating experiments (plan D2.2, D2.3, D7.3; docs/CONTEXT_v11.md section 7.2).

When two or more configurations fit the paper's target claim about equally well, the paper's other reported
conditions (a sweep's points, another dataset, another budget) usually tell them apart, but running every candidate
at every condition is what the budget can't afford. This module picks the runs worth making.

- **The question** is which candidate the paper ran. Under candidate h, the paper's number at condition p is what h
  gives at p, so the likelihood of that number uses h's value there (history matching's error model: the runs'
  spread, the paper's own spread over about `paper_n` runs, and a model-discrepancy term).
- **A transfer surrogate** predicts h's value at a condition it hasn't run at, from the runs already made: h's effect
  on the target (its value minus the as-run one) times the condition's transfer slope, fitted through the origin over
  every candidate measured at both, with the fit's residual as the spread. Below two such candidates, the slope is
  the ratio of the as-run values (a multiplicative transfer) with a spread as wide as the effect itself.
- **Expected information gain** of one run (h at p): the entropy of the posterior over the candidates with h's
  prediction at p, minus its expectation once h's value at p is measured (fixed Gauss-Hermite draws from the
  surrogate's predictive distribution). In bits per run; every run costs one.
- **Batches** for parallel runs: greedy, at most one run per candidate and condition, each test's gain computed
  on the posterior as it stands (runs in one batch are near independent: they measure different candidates or
  different conditions).
- **Priors** (plan D7.3) weight the posterior, never veto: a value the paper states (0.9), a knob the paper mentions
  or sweeps (0.6), an unmentioned one (0.4); a round number (x1.2); a value in the code's own documentation (x1.1).
  The data still decide: a held-out the mentioned candidate breaks outweighs any prior.
- **The exact-hit guard** (D2.3): every likelihood carries the model-discrepancy floor, so a candidate that hits the
  target exactly by chance can't beat one within the discrepancy on the target alone; ties go to the other claims.

Box and Hill (1967) and Bayesian optimal design for model discrimination choose experiments by this mutual
information; here the "models" are measured configurations, the predictions come from a surrogate learned from the
same search's runs, and only conditions the paper reports count as evidence.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

# Gauss-Hermite nodes and weights (probabilists', 10 points): E[f(Z)] for Z ~ N(0, 1)
_GH = [(-4.859462828332312, 4.310652630718277e-06), (-3.581823483551927, 7.580709343122176e-04),
       (-2.484325841638955, 1.911158050077029e-02), (-1.465989094391158, 1.354837029802677e-01),
       (-0.484935707515498, 3.446423349320192e-01), (0.484935707515498, 3.446423349320192e-01),
       (1.465989094391158, 1.354837029802677e-01), (2.484325841638955, 1.911158050077029e-02),
       (3.581823483551927, 7.580709343122176e-04), (4.859462828332312, 4.310652630718277e-06)]


@dataclass
class Condition:
    """A claim at a reported condition: the paper's number, the as-run value there and its run-to-run spread."""

    id: str
    paper: float
    naive: float
    sd: float  # run-to-run spread at this condition (the as-run one, floored)
    model_var: float  # the paper's own spread plus the model discrepancy, squared
    metric: str = ""  # the effect that transfers is the candidate's effect on this metric at the base condition


@dataclass
class Candidate:
    key: frozenset
    config: dict
    prior: float = 0.5
    measured: dict[str, tuple[float, int]] = field(default_factory=dict)  # condition id -> (mean, runs)
    effect: float = 0.0  # its value minus the as-run value on the target
    effects: dict[str, float] = field(default_factory=dict)  # metric -> the same at the base condition

    def effect_on(self, cond: "Condition") -> float:
        return self.effects.get(cond.metric, self.effect)


def _normal_logpdf(x: float, mean: float, var: float) -> float:
    var = max(var, 1e-300)
    return -0.5 * (x - mean) ** 2 / var - 0.5 * math.log(2 * math.pi * var)


def transfer(cands: list[Candidate], cond: Condition, target_naive: float) -> tuple[float, float, int]:
    """(slope, residual spread, candidates used): how a candidate's effect on the target carries over to `cond`."""
    pairs = [(c.effect_on(cond), c.measured[cond.id][0] - cond.naive) for c in cands
             if cond.id in c.measured and abs(c.effect_on(cond)) > 0]
    if len(pairs) >= 2:
        sxx = sum(x * x for x, _ in pairs)
        beta = sum(x * y for x, y in pairs) / sxx if sxx > 0 else 0.0
        resid = [y - beta * x for x, y in pairs]
        dof = max(1, len(pairs) - 1)
        return beta, math.sqrt(sum(r * r for r in resid) / dof), len(pairs)
    ratio = cond.naive / target_naive if target_naive else 1.0
    return ratio, float("nan"), len(pairs)


def predict(c: Candidate, cond: Condition, slope: tuple[float, float, int]) -> tuple[float, float]:
    """(mean, variance) of the candidate's value at the condition: measured, else the surrogate's prediction."""
    if cond.id in c.measured:
        m, n = c.measured[cond.id]
        return m, cond.sd ** 2 / max(n, 1)
    beta, resid, used = slope
    e = c.effect_on(cond)
    mean = cond.naive + beta * e
    spread = resid if used >= 2 and not math.isnan(resid) else abs(beta * e)  # unknown: as wide as the effect
    return mean, spread ** 2 + cond.sd ** 2


def _loglik_at(c: Candidate, cond: Condition, slope) -> float:
    m, v = predict(c, cond, slope)
    return _normal_logpdf(cond.paper, m, v + cond.model_var)


def posterior(cands: list[Candidate], conds: list[Condition], target_naive: float,
              base_loglik: dict[frozenset, float] | None = None) -> dict[frozenset, float]:
    """prior x the likelihood of every condition's paper number (predicted where unmeasured), normalised.
    `base_loglik`: each candidate's log-likelihood of the claims outside `conds` (the target and held-outs)."""
    slopes = {p.id: transfer(cands, p, target_naive) for p in conds}
    logs = {}
    for c in cands:
        lp = math.log(max(c.prior, 1e-12)) + (base_loglik or {}).get(c.key, 0.0)
        lp += sum(_loglik_at(c, p, slopes[p.id]) for p in conds)
        logs[c.key] = lp
    top = max(logs.values())
    z = sum(math.exp(v - top) for v in logs.values())
    return {k: math.exp(v - top) / z for k, v in logs.items()}


def _entropy(w: dict) -> float:
    return -sum(p * math.log2(p) for p in w.values() if p > 0)


def expected_gain(cands: list[Candidate], conds: list[Condition], target_naive: float, c: Candidate, p: Condition,
                  base_loglik: dict[frozenset, float] | None = None) -> float:
    """Bits of information about which candidate the paper ran, from one run of `c` at `p`."""
    if p.id in c.measured:
        return 0.0
    before = posterior(cands, conds, target_naive, base_loglik)
    slope = transfer(cands, p, target_naive)
    mean, var = predict(c, p, slope)
    h_after = 0.0
    for z, wz in _GH:
        y = mean + math.sqrt(var) * z
        trial = [Candidate(x.key, x.config, x.prior, {**x.measured, p.id: (y, 1)} if x.key == c.key else x.measured,
                           x.effect, x.effects) for x in cands]
        h_after += wz * _entropy(posterior(trial, conds, target_naive, base_loglik))
    return max(0.0, _entropy(before) - h_after)


def choose(cands: list[Candidate], conds: list[Condition], target_naive: float, batch: int = 4,
           min_bits: float = 0.05, base_loglik: dict[frozenset, float] | None = None) -> list[tuple[Candidate, Condition, float]]:
    """The batch of runs (candidate, condition, bits) with the largest expected gains, at most one per candidate."""
    scored = []
    for c in cands:
        for p in conds:
            g = expected_gain(cands, conds, target_naive, c, p, base_loglik)
            if g >= min_bits:
                scored.append((c, p, g))
    scored.sort(key=lambda x: -x[2])
    out, used = [], set()
    for c, p, g in scored:
        if c.key in used:
            continue
        out.append((c, p, g))
        used.add(c.key)
        if len(out) >= batch:
            break
    return out


# ------------------------------------------------------------------ priors (plan D7.3)

def _round(v: str) -> bool:
    try:
        x = abs(float(v))
    except ValueError:
        return False
    if x == 0:
        return True
    m = x / 10 ** math.floor(math.log10(x))
    return any(abs(m - r) < 1e-9 for r in (1, 2, 2.5, 5, 10))


def config_prior(config: dict, stated: dict[str, set[str]], mentioned: set[str], documented: dict[str, set[str]]) -> float:
    """The prior of a configuration: the product over its changes. `stated`: knob -> values the paper states;
    `mentioned`: knobs the paper mentions or sweeps; `documented`: knob -> values the code's own docs give."""
    p = 1.0
    for k, v in config.items():
        if v in stated.get(k, set()):
            q = 0.9
        elif k in mentioned:
            q = 0.6
        else:
            q = 0.4
        if _round(v):
            q *= 1.2
        if v in documented.get(k, set()):
            q *= 1.1
        p *= min(q, 0.95)
    return p
