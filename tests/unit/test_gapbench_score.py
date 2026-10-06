import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "eval" / "gapbench"))

from score import same_knobs, score_claim, summarise  # noqa: E402

KEY = {"id": "t", "type": "single_unstated", "hidden": {"normalize": "zscore", "threshold": "0.3"}}


def test_same_knobs_normalises_names_and_numbers():
    assert same_knobs({"--normalize": "zscore", "threshold": "0.30"}, KEY["hidden"])
    assert same_knobs({"normalize": "z-score", "threshold": 0.3}, KEY["hidden"])
    assert not same_knobs({"normalize": "zscore"}, KEY["hidden"])  # missing a knob
    assert not same_knobs({"normalize": "zscore", "threshold": "0.3", "lr": "0.1"}, KEY["hidden"])  # extra knob


def test_score_claim_cases():
    ok = score_claim(KEY, {"label": "Explained", "knobs": {"normalize": "zscore", "threshold": "0.3"}})
    assert ok["correct"] and not ok["false_attr"]
    wrong = score_claim(KEY, {"label": "Attributed", "knobs": {"lr": "0.5"}})
    assert not wrong["correct"] and wrong["false_attr"]
    hedged = score_claim(KEY, {"label": "Fits but unsupported", "knobs": {"lr": "0.5"}})
    assert not hedged["correct"] and not hedged["false_attr"]  # hedged and wrong: not an overclaim
    found = score_claim(KEY, {"label": "Fits but unsupported", "knobs": {"normalize": "zscore", "threshold": "0.3"}})
    assert found["correct"] and not found["confident"]  # right knobs, honestly hedged: still found
    nocause = {**KEY, "type": "no_cause", "hidden": {}}
    assert score_claim(nocause, {"label": "Unexplained", "knobs": {}})["correct"]
    assert score_claim(nocause, {"label": "Fits but unsupported", "knobs": {"lr": "0.5"}})["correct"]
    assert score_claim(nocause, {"label": "Explained", "knobs": {"lr": "0.5"}})["false_attr"]
    assert not score_claim(KEY, None)["correct"]  # missing answer


def test_summarise_median_and_best():
    rows = [{"arm": "a", "task": "t1", "correct": c, "false_attr": False, "cost_usd": 0.1, "wall_s": 5}
            for c in (True, False, True)] + [{"arm": "a", "task": "t2", "correct": False, "false_attr": True,
                                              "cost_usd": 0.2, "wall_s": 9}]
    s = summarise(rows)["a"]
    assert s["solved_median_run"] == 1 and s["solved_best_run"] == 1 and s["false_attribution_rate"] == 0.25
