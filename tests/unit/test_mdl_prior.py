"""Plan F9: paper priors from description lengths."""

from gapfinder.diagnose.discriminate import config_prior, config_prior_mdl


def test_stated_mentioned_unmentioned_order_like_the_fixed_weights():
    stated, mentioned = {"lr": {"0.001"}}, {"lr", "l2"}
    s = config_prior_mdl({"lr": "0.001"}, stated, mentioned, {}, n_open=10)
    m = config_prior_mdl({"l2": "0.0003"}, stated, mentioned, {}, n_open=10)
    u = config_prior_mdl({"dropout": "0.3"}, stated, mentioned, {}, n_open=10)
    assert s > m > u
    assert (config_prior({"lr": "0.001"}, stated, mentioned, {}) > config_prior({"l2": "0.0003"}, stated, mentioned, {})
            > config_prior({"dropout": "0.3"}, stated, mentioned, {}))


def test_an_unmentioned_knob_among_many_costs_more_and_round_values_less():
    few = config_prior_mdl({"dropout": "0.3"}, {}, set(), {}, n_open=3)
    many = config_prior_mdl({"dropout": "0.3"}, {}, set(), {}, n_open=40)
    assert few > many
    assert config_prior_mdl({"dropout": "0.5"}, {}, set(), {}, n_open=3) > few  # 0.5 is round
    assert config_prior_mdl({"lr": "0.001", "dropout": "0.3"}, {"lr": {"0.001"}}, {"lr"}, {}, 3) == few  # stated: free
