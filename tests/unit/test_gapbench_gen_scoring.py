"""score.py scores the generator's exact output format correctly, for all six categories.

Tasks are written with gen_tasks.write_outputs (task folders plus sealed/), so the key fields
(category, type, hidden, unexposed, decoy) are exactly what a real generation produces."""
import asyncio
import json
import sys
from pathlib import Path

import pytest

GB = Path(__file__).resolve().parents[2] / "eval" / "gapbench"
sys.path.insert(0, str(GB))

import gen_tasks as g  # noqa: E402
import score  # noqa: E402

PLANS = {
    "known_cause": g.Plan("known_cause", "single_unstated", "mlbench", 0, 0, hidden={"normalize": "zscore"},
                          omitted=["normalize"]),
    "interaction": g.Plan("interaction", "interaction", "mlbench", 0, 0,
                          hidden={"normalize": "zscore", "threshold": "0.3"}, omitted=["normalize", "threshold"]),
    "decoy": g.Plan("decoy", "single_unstated", "mlbench", 0, 0, hidden={"lr_schedule": "cosine"},
                    decoy={"normalize": "minmax"}, omitted=["lr_schedule", "normalize"]),
    "no_cause": g.Plan("no_cause", "no_cause", "mlbench", 0, 0, offset={"test_accuracy": 1.3,
                                                                       "balanced_accuracy": 0.9}),
    "noise_only": g.Plan("noise_only", "no_cause", "mlbench", 0, 0,
                         noise_u={"test_accuracy": 0.1, "balanced_accuracy": -0.1}),
    "incomplete": g.Plan("incomplete", "single_unstated", "mlbench", 0, 0, hidden={"epochs": "75"},
                         omitted=["epochs"], unexposed=["epochs"]),
}
CALIB = {"repeats": 7, "metrics": {
    "test_accuracy": {"naive": 0.5, "paper": 0.8, "band": 0.01, "units": 30.0},
    "balanced_accuracy": {"naive": 0.5, "paper": 0.75, "band": 0.01, "units": 25.0}}}


@pytest.fixture(scope="module")
def generated(tmp_path_factory):
    root = tmp_path_factory.mktemp("gen")
    staged = tmp_path_factory.mktemp("staged")
    done = []
    for i, (cat, plan) in enumerate(PLANS.items(), 1):
        d = staged / f"test-gen-{i:02d}"
        d.mkdir()
        (d / "paper.md").write_text("# paper\n", encoding="utf-8")
        (d / "targets.json").write_text(json.dumps([
            {"claim_id": "C1", "metric": "test_accuracy", "paper_value": 0.8, "held_out": False},
            {"claim_id": "C2", "metric": "balanced_accuracy", "paper_value": 0.75, "held_out": True}]), encoding="utf-8")
        (d / "calibration.json").write_text(json.dumps(CALIB), encoding="utf-8")
        done.append(g.Done(d.name, plan, d, 1, {}))
    g.write_outputs(root, done)
    return root, {cat: root / "tasks" / f"test-gen-{i:02d}" for i, cat in enumerate(PLANS, 1)}


def _outcome(generated, cat, label, knobs):
    root, tasks = generated
    key = score.load_key(tasks[cat], root / "sealed")
    assert score.category_of(key) == cat
    return score.score_claim(key, {"label": label, "knobs": knobs})["outcome"]


TRUE = {"known_cause": {"normalize": "zscore"}, "interaction": {"normalize": "zscore", "threshold": "0.3"},
        "decoy": {"lr_schedule": "cosine"}}


@pytest.mark.parametrize("cat", ["no_cause", "noise_only", "incomplete"])
def test_abstention_categories_score_an_honest_no_answer_as_correct(generated, cat):
    for label in ("Unexplained", "Inconclusive", "Reproduced"):
        assert _outcome(generated, cat, label, {}) == "correct_abstention"
    assert _outcome(generated, cat, "Fits but unsupported", {"lr": "0.5"}) == "correct_abstention"  # hedged


@pytest.mark.parametrize("cat", ["no_cause", "noise_only", "incomplete"])
def test_abstention_categories_score_a_confident_knob_as_confidently_wrong(generated, cat):
    assert _outcome(generated, cat, "Explained", {"lr": "0.5"}) == "confidently_wrong"
    assert _outcome(generated, cat, "Attributed", {"lr": "0.5"}) == "confidently_wrong"


def test_incomplete_naming_the_unexposed_knob_confidently_is_still_wrong(generated):
    """PROTOCOL.md: the correct answer on an incomplete task is not to attribute, even to the real knob."""
    assert _outcome(generated, "incomplete", "Explained", {"epochs": "75"}) == "confidently_wrong"
    assert _outcome(generated, "incomplete", "Fits but unsupported", {"epochs": "75"}) == "correct_abstention"


def test_missing_prediction_is_missed_never_an_abstention(generated):
    root, tasks = generated
    for cat in PLANS:
        key = score.load_key(tasks[cat], root / "sealed")
        assert score.score_claim(key, None)["outcome"] == "missed"


def test_known_cause_outcomes(generated):
    assert _outcome(generated, "known_cause", "Explained", {"normalize": "zscore"}) == "correct"
    assert _outcome(generated, "known_cause", "Paper-artifact inconsistency", {"normalize": "ZScore"}) == "correct"
    assert _outcome(generated, "known_cause", "Explained", {"normalize": "minmax"}) == "confidently_wrong"
    assert _outcome(generated, "known_cause", "Unexplained", {}) == "missed"


def test_interaction_partial_versus_full(generated):
    both = {"normalize": "zscore", "threshold": 0.3}
    assert _outcome(generated, "interaction", "Explained", both) == "correct"
    assert _outcome(generated, "interaction", "Explained", {"normalize": "zscore"}) == "partial"
    assert _outcome(generated, "interaction", "Explained", {**both, "lr": "0.5"}) == "confidently_wrong"
    assert _outcome(generated, "interaction", "Explained", {"lr": "0.5"}) == "confidently_wrong"


def test_decoy_true_knob_correct_decoy_confidently_wrong(generated):
    assert _outcome(generated, "decoy", "Explained", TRUE["decoy"]) == "correct"
    assert _outcome(generated, "decoy", "Explained", {"normalize": "minmax"}) == "confidently_wrong"
    assert _outcome(generated, "decoy", "Explained", {**TRUE["decoy"], "normalize": "minmax"}) == "confidently_wrong"


def test_score_run_reads_gap_info_from_sealed_calibration(generated, tmp_path, monkeypatch):
    root, tasks = generated

    async def fake_remeasure(task_dir, knobs, n, cache):
        return {"test_accuracy": 0.79, "balanced_accuracy": 0.74}

    monkeypatch.setattr(score, "remeasure", fake_remeasure)
    run = tmp_path / "run1"
    run.mkdir()
    pred = {"task": "test-gen-01", "arm": "gapfinder", "run": 1,
            "claims": {"C1": {"label": "Explained", "knobs": {"normalize": "zscore"}}},
            "cost_usd": 0.01, "wall_s": 1.0, "runs": 3, "setup_runs": 0}
    (run / "prediction.json").write_text(json.dumps(pred), encoding="utf-8")
    row = asyncio.run(score.score_run(tasks["known_cause"], run, 1, root / "sealed"))
    assert row["category"] == "known_cause" and row["outcome"] == "correct" and row["column"] == "correct_cause"
    assert row["gap_closed"] == pytest.approx(0.967, abs=1e-3)  # 1 - |0.79 - 0.8| / |0.5 - 0.8|
    assert row["source"] == "generator"
