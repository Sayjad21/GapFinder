"""Noise calibration from identical forks.

Noise band per metric = 2 x median absolute deviation of >= 5 identical runs.
A branch effect is real only if its median moves by more than the band.
Runs starved of CPU (involuntary context switches far above the batch median)
are flagged so the caller can re-run them.
"""

from __future__ import annotations

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
