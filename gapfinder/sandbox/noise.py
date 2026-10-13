"""Noise calibration from identical forks.

Noise band per metric = 2 x median absolute deviation of >= 5 identical runs.
A branch effect is real only if its median moves by more than the band.
Runs starved of CPU (involuntary context switches far above the batch median)
are flagged so the caller can re-run them.
"""

from __future__ import annotations

import math
import random
import statistics
from dataclasses import dataclass

MAD_TO_SIGMA = 1.4826  # MAD of a normal sample x this ~= sigma


def mad(xs: list[float]) -> float:
    m = statistics.median(xs)
    return statistics.median(abs(x - m) for x in xs)


@dataclass
class NoiseBand:
    metric: str
    n: int
    median: float
    band: float  # 2 x MAD
    cv: float  # coefficient of variation (stdev / mean), for the S4 gate

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def noise_band(metric: str, values: list[float], *, floor_frac: float = 0.0) -> NoiseBand:
    """`floor_frac` sets a minimum band as a fraction of |median| -- with 5 runs
    MAD can be exactly 0 for discrete metrics, which would call any change real."""
    if len(values) < 3:
        raise ValueError("need at least 3 repeats to estimate noise")
    med = statistics.median(values)
    band = 2 * mad(values)
    band = max(band, floor_frac * abs(med))
    mean = statistics.fmean(values)
    cv = statistics.stdev(values) / abs(mean) if mean else float("inf")
    return NoiseBand(metric, len(values), med, band, cv)


# two-sided 0.05 and one-sided 0.2 Student t quantiles, by degrees of freedom (no scipy dependency)
_T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 8: 2.306, 10: 2.228, 15: 2.131, 20: 2.086,
         30: 2.042, 60: 2.0, 1000: 1.96}
_T80 = {1: 1.376, 2: 1.061, 3: 0.978, 4: 0.941, 5: 0.920, 6: 0.906, 8: 0.889, 10: 0.879, 15: 0.866, 20: 0.860,
        30: 0.854, 60: 0.848, 1000: 0.842}


def _t(table: dict[int, float], df: int) -> float:
    keys = sorted(table)
    return table[min((k for k in keys if k >= df), default=keys[-1])]


def mde(sigma: float, n: int) -> float:
    """Minimum detectable effect for comparing two configurations with n runs each:
    (t_{1-a/2, df} + t_{1-b, df}) * sigma * sqrt(2 / n), a = 0.05, power 1 - b = 0.8, df = 2n - 2."""
    df = max(1, 2 * n - 2)
    return (_t(_T975, df) + _t(_T80, df)) * sigma * math.sqrt(2 / n)


def effect_in_noise_units(naive_gap: float, branch_gap: float, band: float) -> float:
    """(|naive gap| - |branch gap|) / band. Positive = branch closes the gap."""
    if band <= 0:
        return float("inf") if abs(branch_gap) < abs(naive_gap) else 0.0
    return (abs(naive_gap) - abs(branch_gap)) / band


def is_real_effect(baseline_values: list[float], branch_values: list[float], band: float) -> bool:
    return abs(statistics.median(branch_values) - statistics.median(baseline_values)) > band


def bootstrap_diff_ci(base: list[float], cand: list[float], *, n: int = 2000, alpha: float = 0.05,
                      seed: int = 0) -> tuple[float, float]:
    """Percentile bootstrap interval for mean(cand) - mean(base), resampling each group separately.
    Deterministic (fixed seed), so a search replays to the same verdict."""
    if not base or not cand:
        raise ValueError("need runs in both groups")
    rng = random.Random(seed)
    diffs = sorted(statistics.fmean(rng.choices(cand, k=len(cand))) - statistics.fmean(rng.choices(base, k=len(base)))
                   for _ in range(n))
    lo = diffs[int(alpha / 2 * (n - 1))]
    hi = diffs[int((1 - alpha / 2) * (n - 1))]
    return lo, hi


def starved(involuntary_switches: list[int], factor: float = 3.0) -> list[bool]:
    """Flag runs whose involuntary context switches exceed `factor` x the batch median."""
    if not involuntary_switches:
        return []
    med = statistics.median(involuntary_switches) or 1
    return [s > factor * med for s in involuntary_switches]
