"""Minimum detectable effect, and the engine rule: an Unexplained gap below it reads Inconclusive."""

from types import SimpleNamespace

from gapfinder.ledger.schemas import ConfidenceLabel
from gapfinder.sandbox.noise import mde
from gapfinder.search.engine import ClaimResult, GapSearch, Target


def test_mde_matches_the_t_formula():
    # n=5 per arm: df 8, (2.306 + 0.889) * sqrt(2/5)
    assert abs(mde(1.0, 5) - 3.195 * (2 / 5) ** 0.5) < 1e-9
    assert mde(2.0, 5) == 2 * mde(1.0, 5)
    assert mde(1.0, 20) < mde(1.0, 5)  # more runs, smaller detectable effect


def _engine(naive_values, repeats=3):
    runs = [SimpleNamespace(parsed_metrics={"m": v}) for v in naive_values]
    return SimpleNamespace(
        measure_ok=lambda changes: runs, confirm_repeats=lambda t: repeats,
        _attribution=lambda t, c, g, label, ckpts: SimpleNamespace(confidence_label=label.value))


def _unexplained(gap):
    t = Target("C1", "m", 100.0)
    res = ClaimResult(target=t, status="searched", gap_before=gap, band=0.01)
    res.attribution = SimpleNamespace(confidence_label=ConfidenceLabel.unexplained.value)
    return t, res


def test_small_gap_below_mde_becomes_inconclusive():
    eng = _engine([95.0, 100.0, 105.0, 98.0, 102.0])  # sd ~3.8, MDE(3 runs) ~11.6 -> 11.6%
    t, res = _unexplained(-0.06)
    GapSearch._mde_check(eng, t, res)
    assert res.attribution.confidence_label == "Inconclusive" and res.status == "inconclusive"
    assert "minimum detectable effect" in res.notes[-1]


def test_large_gap_stays_unexplained_and_other_labels_untouched():
    eng = _engine([95.0, 100.0, 105.0, 98.0, 102.0])
    t, res = _unexplained(-0.40)
    GapSearch._mde_check(eng, t, res)
    assert res.attribution.confidence_label == "Unexplained" and res.status == "searched"
    t, res = _unexplained(-0.06)
    res.attribution.confidence_label = "Explained"
    GapSearch._mde_check(eng, t, res)
    assert res.attribution.confidence_label == "Explained"


def test_deterministic_metric_never_inconclusive():
    eng = _engine([100.0] * 5)  # sd 0 -> MDE 0
    t, res = _unexplained(-0.01)
    GapSearch._mde_check(eng, t, res)
    assert res.attribution.confidence_label == "Unexplained"
