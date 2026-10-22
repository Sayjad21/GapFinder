"""A differential diagnosis over cause classes (plan D1.1, docs/CONTEXT_v11.md section 7.2).

GapFinder used to answer one question, "which setting explains the gap?". Half the documented causes on sealed real
papers were something else: a reporting rule, a code defect, a library change, a data-pipeline switch. This module
keeps every candidate explanation, of every class, on one scale: the likelihood of all the paper's claims under it.

- A **hypothesis** predicts each claim's number (a mean, a spread, the runs behind it). Its log-likelihood over the
  claims uses history matching's error model: the runs' spread, the paper's own uncertainty (its number is one result
  of about `paper_n` runs) and a model-discrepancy term (`disc` x the paper's value), so a hypothesis that hits one
  number exactly by luck gains little over one that is close on every claim.
- **"Outside every class"** is always a hypothesis: each claim's number anywhere in a wide interval around the naive
  run. A real explanation must beat it, so the ranking can say "none of these" honestly.
- The **posterior** is prior x likelihood, normalised over the hypotheses tested. The ranked list (the top three
  with their evidence and how to check them) is what the report shows; a confident label still needs the
  verification the engine does for its own class.
- **Choosing the next test:** the mutual information between which hypothesis is the cause and the test's outcome
  (each candidate: its prior of being the cause, the test's power, its false-fit rate), divided by the test's cost
  (sequential diagnosis as in MAI-DxO 2025, with explicit costs as in Singh et al. 2025, and Bayesian bookkeeping
  instead of a panel of models).
"""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass, field

FIT_I = 3.0  # Pukelsheim's rule, as in history matching
STRICT_I = 2.0  # for decisions that skip work (the calibration gate)
CLASSES = ("settings", "reporting", "library", "code", "data", "outside")


@dataclass
class ClaimSpec:
    """A claim as the diagnosis sees it: the paper's number and the naive run's statistics for it."""

    claim_id: str
    metric: str
    paper: float
    naive_mean: float
    naive_sd: float
    target: bool = False
    run_sd: float | None = None  # the naive runs' own spread, before the noise floor (None: fewer than 2 runs)


@dataclass
class Prediction:
    mean: float
    sd: float
    n: int  # runs (cells) behind the mean

    @classmethod
    def from_values(cls, vals: list[float], sd_floor: float) -> "Prediction":
        sd = statistics.stdev(vals) if len(vals) >= 2 else 0.0
        return cls(statistics.fmean(vals), max(sd, sd_floor), len(vals))


@dataclass
class Hypothesis:
    id: str
    cls: str
    title: str  # what it says, in words
    prior: float
    predictions: dict[str, Prediction] = field(default_factory=dict)  # claim id -> prediction
    detail: dict = field(default_factory=dict)  # e.g. {"rule": "best"} or {"changes": {...}}
    evidence: list[str] = field(default_factory=list)
    check: str = ""  # how a person checks it
    runs: int = 0  # runs it took
    # filled by Differential.score
    per_claim: dict[str, dict] = field(default_factory=dict)
    loglik: float | None = None
    posterior: float = 0.0

    @property
    def fits_all(self) -> bool:
        return bool(self.per_claim) and all(v["I"] <= FIT_I for v in self.per_claim.values())

    @property
    def max_I(self) -> float:
        return max((v["I"] for v in self.per_claim.values()), default=float("inf"))

    def to_dict(self) -> dict:
        return {"id": self.id, "class": self.cls, "title": self.title, "prior": round(self.prior, 4),
                "posterior": round(self.posterior, 4), "loglik": None if self.loglik is None else round(self.loglik, 3),
                "fits_all": self.fits_all, "max_I": round(self.max_I, 2) if self.per_claim else None,
                "per_claim": {k: {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items()}
                              for k, v in self.per_claim.items()},
                "detail": self.detail, "evidence": self.evidence, "check": self.check, "runs": self.runs}


class Differential:
    def __init__(self, claims: list[ClaimSpec], *, paper_n: float = 1.0, disc: float = 0.05,
                 outside_prior: float = 0.2):
        self.claims = {c.claim_id: c for c in claims}
        self.paper_n, self.disc = paper_n, disc
        self.hypotheses: dict[str, Hypothesis] = {}
        self.outside = Hypothesis("outside", "outside", "a cause outside every class tested", outside_prior,
                                  check="look for code, data or evaluation differences the classes don't cover")

    # ------------------------------------------------------------------ scoring
    def claim_loglik(self, c: ClaimSpec, p: Prediction) -> tuple[float, float]:
        """(implausibility, log-likelihood) of the paper's number under a prediction."""
        var = p.sd ** 2 / max(p.n, 1) + p.sd ** 2 / self.paper_n + (self.disc * c.paper) ** 2
        var = var or 1e-12
        i = abs(c.paper - p.mean) / math.sqrt(var)
        return i, -0.5 * i * i - 0.5 * math.log(2 * math.pi * var)

    def outside_loglik(self, c: ClaimSpec) -> float:
        """Each claim's number uniform over a wide interval around the naive run (contains the paper's number)."""
        width = 2 * max(3 * abs(c.paper - c.naive_mean), 6 * c.naive_sd, 0.1 * abs(c.paper), 1e-9)
        return -math.log(width)

    def score(self, h: Hypothesis) -> Hypothesis:
        h.per_claim = {}
        ll = 0.0
        for cid, c in self.claims.items():
            p = h.predictions.get(cid) or Prediction(c.naive_mean, c.naive_sd, 1)  # unchanged by the hypothesis
            i, l = self.claim_loglik(c, p)
            h.per_claim[cid] = {"paper": c.paper, "pred": p.mean, "sd": p.sd, "n": p.n, "I": i}
            ll += l
        h.loglik = ll
        return h

    def add(self, h: Hypothesis) -> Hypothesis:
        self.hypotheses[h.id] = self.score(h)
        self._normalise()
        return h

    def _normalise(self) -> None:
        self.outside.loglik = sum(self.outside_loglik(c) for c in self.claims.values())
        hs = list(self.hypotheses.values()) + [self.outside]
        logs = [math.log(max(h.prior, 1e-12)) + (h.loglik if h.loglik is not None else -1e9) for h in hs]
        top = max(logs)
        z = sum(math.exp(x - top) for x in logs)
        for h, x in zip(hs, logs):
            h.posterior = math.exp(x - top) / z

    def ranked(self, k: int | None = None, include_outside: bool = True) -> list[Hypothesis]:
        hs = list(self.hypotheses.values()) + ([self.outside] if include_outside else [])
        hs.sort(key=lambda h: -h.posterior)
        return hs[:k] if k else hs

    # ------------------------------------------------------------------ choosing the next test
    @staticmethod
    def _entropy(ps: list[float]) -> float:
        return -sum(p * math.log(p) for p in ps if p > 0)

    def expected_information(self, candidates: list[tuple[float, float, float]]) -> float:
        """Mutual information between which hypothesis is the cause and the outcome of a test (nats).

        `candidates`: the untested hypotheses the test would score, each as (prior probability that it is the cause,
        power = P(the test shows it fits | it is the cause), false-fit rate = P(it fits | it is not the cause)). The
        hypotheses already tested keep their posterior, scaled to leave the candidates their priors. The outcome is
        one fit/miss per candidate: I(H; O) = H(O) - sum_h P(h) H(O | h), with at most 10 candidates (the likeliest)."""
        cands = sorted(candidates, key=lambda c: -c[0])[:10]
        total = sum(c[0] for c in cands)
        if total >= 0.95:  # priors of "being the cause" can't take all the mass
            cands = [(c[0] * 0.95 / total, c[1], c[2]) for c in cands]
            total = 0.95
        rest = 1.0 - total  # the tested hypotheses (and "outside") together
        k = len(cands)
        if k == 0:
            return 0.0

        def p_outcome(o: int, cause: int | None) -> float:
            pr = 1.0
            for i, (_, power, false) in enumerate(cands):
                q = power if i == cause else false
                pr *= q if (o >> i) & 1 else 1 - q
            return pr

        causes = [(rest, None)] + [(c[0], i) for i, c in enumerate(cands)]
        h_o, h_cond = 0.0, 0.0
        for o in range(2 ** k):
            po = sum(w * p_outcome(o, j) for w, j in causes)
            if po > 0:
                h_o -= po * math.log(po)
        for w, j in causes:
            for o in range(2 ** k):
                q = p_outcome(o, j)
                if q > 0:
                    h_cond -= w * q * math.log(q)
        return max(0.0, h_o - h_cond)

    def next_test(self, tests: list[dict]) -> dict | None:
        """The test with the most expected information per unit cost. Each test: {"name", "cost" (runs; free tests
        count as a small epsilon), "candidates": [(prior of being the cause, power, false-fit rate), ...]}."""
        best, score = None, 0.0
        for t in tests:
            s = self.expected_information(t["candidates"]) / max(t.get("cost", 1.0), 1e-3)
            if s > score:
                best, score = t, s
        return best

    # ------------------------------------------------------------------ the report
    def to_dict(self, k: int = 5) -> dict:
        return {"claims": {cid: {"paper": c.paper, "naive": c.naive_mean, "sd": c.naive_sd, "target": c.target}
                           for cid, c in self.claims.items()},
                "ranked": [h.to_dict() for h in self.ranked(k)], "paper_n": self.paper_n, "disc": self.disc}

    def markdown(self, k: int = 3) -> list[str]:
        out = ["### Differential diagnosis (every class on one scale: the likelihood of all the claims)", "",
               "| rank | explanation | class | posterior | worst claim (sigma) | how to check |", "|---|---|---|---|---|---|"]
        for i, h in enumerate(self.ranked(k), 1):
            worst = "" if not h.per_claim else f"{h.max_I:.1f}" + (" (fits every claim)" if h.fits_all else "")
            out.append(f"| {i} | {h.title} | {h.cls} | {h.posterior:.0%} | {worst} | {h.check} |")
        return out + [""]
