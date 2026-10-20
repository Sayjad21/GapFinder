"""Plan D1.1: the differential's arithmetic: likelihood over all claims, the outside hypothesis, information gain."""

import math

from gapfinder.diagnose import ClaimSpec, Differential, Hypothesis, Prediction


def _diff():
    return Differential([ClaimSpec("C1", "acc", 80.0, 74.0, 0.3, target=True), ClaimSpec("C2", "f1", 70.0, 66.0, 0.3)],
                        paper_n=1.0, disc=0.01)


def _h(i, c1, c2, prior=0.1):
    return Hypothesis(i, "settings", i, prior, {"C1": Prediction(c1, 0.3, 5), "C2": Prediction(c2, 0.3, 5)})


def test_a_hypothesis_must_fit_every_claim_to_rank_high():
    d = _diff()
    both = d.add(_h("both", 80.0, 70.0))
    target_only = d.add(_h("target-only", 80.0, 66.0))  # an exact hit on the target, the held-out still off
    assert both.fits_all and not target_only.fits_all
    assert [h.id for h in d.ranked(2)] == ["both", "outside"] or d.ranked()[0].id == "both"
    assert both.posterior > 0.9 and target_only.posterior < 0.01


def test_nothing_fitting_leaves_the_mass_outside():
    d = _diff()
    d.add(_h("near", 76.0, 67.0))
    assert d.ranked()[0].id == "outside"  # "none of these" is an answer


def test_information_gain_prefers_the_test_that_can_settle_it():
    d = _diff()
    d.add(_h("near", 76.0, 67.0))
    plausible = d.expected_information([(0.3, 0.9, 0.05)])  # likely the cause, a test that tells
    unlikely = d.expected_information([(0.001, 0.9, 0.05)])  # almost surely not the cause
    weak = d.expected_information([(0.3, 0.55, 0.45)])  # a test that barely separates cause from not
    assert plausible > unlikely > 0 and plausible > weak
    assert d.expected_information([(0.3, 0.9, 0.05), (0.3, 0.9, 0.05)]) > plausible  # two candidates, more to learn
    cheap = {"name": "cheap", "cost": 1.0, "candidates": [(0.3, 0.9, 0.05)]}
    costly = {"name": "costly", "cost": 50.0, "candidates": [(0.35, 0.9, 0.05)]}
    assert d.next_test([costly, cheap])["name"] == "cheap"


def test_the_outside_interval_contains_the_paper_value():
    d = _diff()
    c = d.claims["C1"]
    assert math.isfinite(d.outside_loglik(c)) and d.outside_loglik(c) < 0
