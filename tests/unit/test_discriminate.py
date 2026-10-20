"""The discrimination scheduler (gapfinder/diagnose/discriminate.py, plans D2.2, D2.3, D7.3)."""

import math

from gapfinder.diagnose.discriminate import (Candidate, Condition, choose, config_prior, expected_gain, posterior,
                                             predict, transfer)


def _c(name, effect, prior=0.5, **measured):
    return Candidate(frozenset({name: "1"}.items()), {name: "1"}, prior, dict(measured), effect)


def test_the_transfer_surrogate_learns_the_slope_from_measured_candidates():
    p = Condition("P", paper=60.0, naive=50.0, sd=0.5, model_var=0.25)
    a, b, c = _c("a", 4.0, P=(58.0, 2)), _c("b", 2.0, P=(54.0, 2)), _c("c", 3.0)
    beta, resid, used = transfer([a, b, c], p, target_naive=70.0)
    assert used == 2 and abs(beta - 2.0) < 1e-9 and resid < 1e-9
    m, v = predict(c, p, (beta, resid, used))
    assert abs(m - 56.0) < 1e-9 and abs(v - 0.25) < 1e-9  # 50 + 2 x 3, the run noise left
    m0, v0 = predict(c, p, transfer([c], p, 70.0))  # nothing measured there: the ratio of the as-run values, wide
    assert abs(m0 - (50 + 3 * 50 / 70)) < 1e-9 and v0 > (3 * 50 / 70) ** 2


def test_the_run_that_separates_two_equal_fits_is_chosen_and_decides():
    # a and b fit the target equally; at P the paper says 56, and a's effect transfers there, b's doesn't
    p = Condition("P", paper=56.0, naive=50.0, sd=0.3, model_var=0.1)
    q = Condition("Q", paper=50.0, naive=50.0, sd=0.3, model_var=0.1)  # a condition where nothing moves
    a, b = _c("a", 3.0), _c("b", 3.0)
    w0 = posterior([a, b], [p, q], 70.0)
    assert abs(w0[a.key] - 0.5) < 1e-9  # nothing tells them apart yet
    picks = choose([a, b], [p, q], 70.0)
    assert picks and picks[0][1].id == "P" and picks[0][2] > 0.05
    assert expected_gain([a, b], [p, q], 70.0, a, q) < picks[0][2]
    a.measured["P"] = (56.1, 1)  # the truth: a gives the paper's number at P
    b.measured["P"] = (50.2, 1)
    w = posterior([a, b], [p, q], 70.0)
    assert w[a.key] > 0.99


def test_an_exact_hit_on_the_target_alone_does_not_beat_the_truth():
    # base log-likelihoods from the target carry the discrepancy floor: an exact hit gains little; a held-out decides
    disc_var = 0.5 ** 2
    hit, truth = _c("hit", 2.0), _c("truth", 1.9)
    base = {hit.key: -0.5 * 0.0 ** 2 / disc_var, truth.key: -0.5 * 0.1 ** 2 / disc_var}
    held = Condition("H", paper=42.0, naive=40.0, sd=0.2, model_var=0.05)
    hit.measured["H"], truth.measured["H"] = (40.1, 2), (41.9, 2)
    w = posterior([hit, truth], [held], 50.0, base)
    assert w[truth.key] > 0.99


def test_priors_weight_but_never_veto():
    stated, mentioned = {"lr": {"0.01"}}, {"lr", "dropout"}
    assert config_prior({"lr": "0.01"}, stated, mentioned, {}) > config_prior({"dropout": "0.37"}, stated, mentioned, {})
    assert config_prior({"dropout": "0.5"}, stated, mentioned, {}) > config_prior({"wd": "0.5"}, stated, mentioned, {})
    assert config_prior({"wd": "0.0005"}, {}, set(), {}) > config_prior({"wd": "0.0007"}, {}, set(), {})  # round
    # the mentioned candidate breaks a held-out: the unmentioned truth wins anyway
    m = Candidate(frozenset({"lr": "0.02"}.items()), {"lr": "0.02"}, config_prior({"lr": "0.02"}, stated, mentioned, {}),
                  {"H": (30.0, 2)}, 1.0)
    u = Candidate(frozenset({"wd": "0.001"}.items()), {"wd": "0.001"}, config_prior({"wd": "0.001"}, stated, mentioned, {}),
                  {"H": (35.0, 2)}, 1.0)
    w = posterior([m, u], [Condition("H", 35.0, 33.0, 0.5, 0.1)], 50.0)
    assert m.prior > u.prior and w[u.key] > 0.99
    assert math.isclose(sum(w.values()), 1.0)
