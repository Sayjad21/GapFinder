from gapfinder.sandbox.noise import bootstrap_diff_ci


def test_bootstrap_interval_separates_a_real_shift_from_noise():
    base = [10.0, 10.4, 9.7, 10.1, 9.9]
    lo, hi = bootstrap_diff_ci(base, [10.2, 9.8, 10.0])  # same distribution
    assert lo < 0 < hi
    lo, hi = bootstrap_diff_ci(base, [12.1, 11.8, 12.3])  # shifted by about +2
    assert 1.0 < lo < hi < 3.0
    assert bootstrap_diff_ci(base, [12.1, 11.8, 12.3]) == (lo, hi)  # deterministic


def test_bootstrap_on_identical_runs_is_a_point():
    lo, hi = bootstrap_diff_ci([5.0] * 5, [7.0] * 3)
    assert lo == hi == 2.0
