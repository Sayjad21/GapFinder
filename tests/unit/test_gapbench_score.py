import asyncio
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "eval" / "gapbench"))

from score import (  # noqa: E402
    answer_signature,
    answer_stability,
    category_of,
    combine_claims,
    load_key,
    same_knobs,
    score_claim,
    score_run,
    source_of,
    summarise,
    summarise_by_source,
    trust_matrix,
    wilson,
)

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


# ---------------------------------------------------------------- Wilson interval


def test_wilson_known_values():
    assert wilson(0, 8) == {"k": 0, "n": 8, "rate": 0.0, "lo": 0.0, "hi": 0.324}
    assert wilson(4, 8) == {"k": 4, "n": 8, "rate": 0.5, "lo": 0.215, "hi": 0.785}
    w = wilson(8, 8)
    assert (w["lo"], w["hi"]) == (0.676, 1.0)
    assert wilson(0, 0)["rate"] is None  # no runs: no rate, no interval


def test_wilson_interval_contains_rate_and_narrows_with_n():
    small, big = wilson(3, 10), wilson(30, 100)
    for w in (small, big):
        assert 0 <= w["lo"] <= w["rate"] <= w["hi"] <= 1
    assert big["hi"] - big["lo"] < small["hi"] - small["lo"]


# ---------------------------------------------------------------- categories


def _key(category, hidden=None, **kw):
    return {"id": "t", "type": "single_unstated", "category": category, "hidden": hidden or {}, **kw}


def test_category_from_field_then_type():
    assert category_of({"type": "stated_code_differs"}) == "known_cause"
    assert category_of({"type": "interaction"}) == "interaction"
    assert category_of({"type": "no_cause"}) == "no_cause"
    assert category_of({"type": "no_cause", "category": "noise_only"}) == "noise_only"  # the field wins
    with pytest.raises(ValueError):
        category_of({"id": "x", "type": "mystery"})


HIDDEN2 = {"normalize": "zscore", "threshold": "0.3"}


def test_interaction_outcomes():
    key = _key("interaction", HIDDEN2)
    both = score_claim(key, {"label": "Explained", "knobs": {"normalize": "zscore", "threshold": "0.30"}})
    assert both["outcome"] == "correct" and both["column"] == "correct_cause"
    half = score_claim(key, {"label": "Explained", "knobs": {"normalize": "zscore"}})
    assert half["outcome"] == "partial" and not half["correct"] and not half["false_attr"]
    hedged_half = score_claim(key, {"label": "Fits but unsupported", "knobs": {"threshold": "0.3"}})
    assert hedged_half["outcome"] == "partial"
    extra = score_claim(key, {"label": "Explained", "knobs": {**HIDDEN2, "lr": "0.5"}})
    assert extra["outcome"] == "confidently_wrong" and extra["column"] == "wrong_confident"
    wrong_value = score_claim(key, {"label": "Explained", "knobs": {"normalize": "minmax"}})
    assert wrong_value["outcome"] == "confidently_wrong"  # right knob, wrong value is not partial


def test_decoy_outcomes():
    key = _key("decoy", {"normalize": "zscore"}, decoy={"threshold": "0.9"})
    assert score_claim(key, {"label": "Explained", "knobs": {"normalize": "zscore"}})["outcome"] == "correct"
    assert score_claim(key, {"label": "Explained", "knobs": {"threshold": "0.9"}})["outcome"] == "confidently_wrong"
    hedged_decoy = score_claim(key, {"label": "Fits but unsupported", "knobs": {"threshold": "0.9"}})
    assert hedged_decoy["outcome"] == "missed" and hedged_decoy["column"] == "missed"


@pytest.mark.parametrize("category", ["no_cause", "noise_only", "incomplete"])
def test_abstention_categories(category):
    key = _key(category)
    for label in ("Unexplained", "Inconclusive", "Reproduced"):
        sc = score_claim(key, {"label": label, "knobs": {}})
        assert sc["outcome"] == "correct_abstention" and sc["column"] == "abstained" and sc["correct"]
    hedge = score_claim(key, {"label": "Fits but unsupported", "knobs": {"lr": "0.5"}})
    assert hedge["outcome"] == "correct_abstention"
    for label in ("Explained", "Attributed", "Partially explained", "Paper-artifact inconsistency"):
        sc = score_claim(key, {"label": label, "knobs": {"lr": "0.5"}})
        assert sc["outcome"] == "confidently_wrong" and sc["false_attr"] and not sc["correct"]
    crashed = score_claim(key, None)
    assert crashed["outcome"] == "missed" and crashed["column"] == "missed" and not crashed["correct"]


def test_cause_task_abstention_vs_missing():
    key = _key("known_cause", {"normalize": "zscore"})
    unexplained = score_claim(key, {"label": "Inconclusive", "knobs": {}})
    assert unexplained["outcome"] == "missed" and unexplained["column"] == "abstained"
    assert score_claim(key, None)["column"] == "missed"  # a crash is not an honest abstention


def test_combine_claims_needs_every_claim_right():
    key = _key("known_cause", {"a": "1"})
    right = score_claim(key, {"label": "Explained", "knobs": {"a": "1"}})
    gone = score_claim(key, None)
    wrong = score_claim(key, {"label": "Explained", "knobs": {"b": "2"}})
    assert combine_claims({"C1": right}) == ("correct", "correct_cause")
    assert combine_claims({"C1": right, "C2": gone}) == ("missed", "missed")
    assert combine_claims({"C1": right, "C2": wrong}) == ("confidently_wrong", "wrong_confident")


# ---------------------------------------------------------------- --answers


def _write_task(root: Path, name: str, answers: Path | None, **answer_fields) -> Path:
    """A task folder (visible files only) and, if `answers` is given, its sealed answer key."""
    task = root / name
    task.mkdir(parents=True)
    (task / "task.yaml").write_text(f"id: {name}\nfamily: rlbench\nsplit: test\ntype: no_cause\n", encoding="utf-8")
    (task / "calibration.json").write_text(json.dumps({"metrics": {"m": {"naive": 1.0}}}), encoding="utf-8")
    (task / "targets.json").write_text(json.dumps([{"claim_id": "C1", "metric": "m", "paper_value": 2.0}]),
                                       encoding="utf-8")
    key = {"id": name, "type": "no_cause", "hidden": {}, "primary_claims": ["C1"], **answer_fields}
    dest = (answers / name) if answers else task
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "answer.json").write_text(json.dumps(key), encoding="utf-8")
    return task


def test_load_key_reads_the_task_folder_by_default(tmp_path):
    task = _write_task(tmp_path, "t1", None, category="noise_only")
    assert load_key(task)["category"] == "noise_only"
    assert load_key(task)["hidden"] == {}


def test_load_key_answers_dir_overrides_and_fills_hidden_fields(tmp_path):
    sealed = tmp_path / "sealed"
    task = _write_task(tmp_path / "tasks", "t2", sealed)
    assert not (task / "answer.json").exists()  # the task folder holds no answer
    (sealed / "t2" / "task.yaml").write_text("hidden: {normalize: zscore}\ncategory: decoy\n", encoding="utf-8")
    key = load_key(task, sealed)
    assert key["category"] == "decoy" and key["type"] == "no_cause"
    assert key["hidden"] == {}  # answer.json is authoritative where it has the field
    with pytest.raises(FileNotFoundError):
        load_key(task)  # without --answers there is nothing to read


def test_load_key_category_falls_back_to_visible_task_yaml_then_type(tmp_path):
    sealed = tmp_path / "sealed"
    task = _write_task(tmp_path / "tasks", "t3", sealed)
    assert load_key(task, sealed)["category"] == "no_cause"  # derived from type
    (task / "task.yaml").write_text("id: t3\nfamily: rlbench\nsplit: test\ntype: no_cause\ncategory: incomplete\n",
                                    encoding="utf-8")
    assert load_key(task, sealed)["category"] == "incomplete"


def test_score_run_with_sealed_answers(tmp_path):
    sealed = tmp_path / "sealed"
    task = _write_task(tmp_path / "tasks", "t4", sealed, category="noise_only")
    run = tmp_path / "run1"
    run.mkdir()
    pred = {"task": "t4", "arm": "gapfinder", "run": 1, "claims": {"C1": {"label": "Inconclusive", "knobs": {}}},
            "cost_usd": 0.01, "wall_s": 2.0, "runs": 5, "setup_runs": 0}
    (run / "prediction.json").write_text(json.dumps(pred), encoding="utf-8")
    row = asyncio.run(score_run(task, run, 1, sealed))
    assert row["category"] == "noise_only" and row["truth"] == "no_cause"
    assert row["outcome"] == "correct_abstention" and row["column"] == "abstained" and row["correct"]
    assert row["gap_closed"] is None and row["answer"] == "C1:abstain"


# ---------------------------------------------------------------- trust matrix and summary


def _row(arm, task, truth, outcome, column, **kw):
    return {"arm": arm, "task": task, "truth": truth, "outcome": outcome, "column": column,
            "correct": outcome in ("correct", "correct_abstention"), "false_attr": outcome == "confidently_wrong",
            "cost_usd": 0.1, "wall_s": 4.0, "runs": 10, "gap_closed": None, **kw}


ROWS = [
    _row("a", "dev-x", "cause", "correct", "correct_cause", gap_closed=1.0, answer="C1:n=z"),
    _row("a", "dev-x", "cause", "correct", "correct_cause", gap_closed=0.8, answer="C1:n=z"),
    _row("a", "dev-x", "cause", "missed", "abstained", gap_closed=0.0, answer="C1:abstain"),
    _row("a", "test-gen-y", "no_cause", "correct_abstention", "abstained", answer="C1:abstain"),
    _row("a", "test-gen-y", "no_cause", "confidently_wrong", "wrong_confident", answer="C1:lr=1"),
    _row("a", "test-ai-z", "cause", "partial", "partial", answer="C1:n=z"),
    _row("a", "test-ai-z", "cause", "confidently_wrong", "wrong_confident", answer="C1:lr=1"),
]


def test_trust_matrix_rows_are_truth_and_sum_to_runs():
    m = trust_matrix(ROWS)
    assert m["cause"] == {"correct_cause": 2, "partial": 1, "wrong_confident": 1, "abstained": 1, "missed": 0,
                          "runs": 5}
    assert m["no_cause"] == {"correct_cause": 0, "partial": 0, "wrong_confident": 1, "abstained": 1, "missed": 0,
                             "runs": 2}
    for row in m.values():
        assert sum(v for k, v in row.items() if k != "runs") == row["runs"]


def test_summarise_counts_rates_and_trust_matrix():
    s = summarise(ROWS)["a"]
    assert s["counts"] == {"correct": 2, "partial": 1, "confidently_wrong": 2, "correct_abstention": 1, "missed": 1}
    assert (s["runs_with_cause"], s["runs_without_cause"]) == (5, 2)
    assert s["rates"]["correct"]["k"] == 2 and s["rates"]["correct"]["n"] == 5
    assert s["rates"]["confidently_wrong"]["n"] == 7  # out of all runs
    assert s["rates"]["correct_abstention"]["n"] == 2
    assert s["trust_matrix"] == trust_matrix(ROWS)
    assert s["median_gap_closed"] == 0.8 and s["total_experiments"] == 70
    assert s["total_cost_usd"] == 0.7 and s["total_wall_s"] == 28.0
    assert s["solved_median_run_ci"]["n"] == 3  # tasks, not runs


def test_answer_stability_is_share_of_most_common_answer():
    st = answer_stability(ROWS)
    assert st["per_task"]["dev-x"] == pytest.approx(0.667, abs=1e-3)
    assert st["per_task"]["test-gen-y"] == 0.5
    assert st["tasks_compared"] == 3
    assert answer_stability([ROWS[0]])["mean"] is None  # one run per task: nothing to compare


def test_answer_signature_ignores_knob_spelling_and_order():
    a = {"C1": {"label": "Explained", "knobs": {"--b": "1.0", "a": "x"}}}
    b = {"C1": {"label": "Attributed", "knobs": {"a": "x", "b": "1"}}}
    assert answer_signature(a) == answer_signature(b)
    assert answer_signature({"C1": {"label": "Inconclusive", "knobs": {"a": "x"}}}) == "C1:abstain"


def test_sources_and_grouping():
    assert [source_of(t) for t in ("test-gen-1", "test-ai-2", "dev-rl-x", "other")] == [
        "generator", "ai_author", "dev", "other"]
    by = summarise_by_source(ROWS)
    assert set(by) == {"dev", "generator", "ai_author"}
    assert by["generator"]["a"]["counts"]["correct_abstention"] == 1
    assert by["dev"]["a"]["runs"] == 3


def test_main_async_runs_filter_scores_only_the_chosen_run_numbers(tmp_path, monkeypatch):
    import score

    sealed = tmp_path / "sealed"
    _write_task(tmp_path / "tasks", "t5", sealed, category="noise_only")
    monkeypatch.setattr(score, "GB", tmp_path)
    for k in (1, 4):
        run = tmp_path / "runs" / "t5" / "gapfinder" / f"run{k}"
        run.mkdir(parents=True)
        pred = {"task": "t5", "arm": "gapfinder", "run": k, "claims": {"C1": {"label": "Inconclusive", "knobs": {}}},
                "cost_usd": 0.01, "wall_s": 2.0, "runs": 5, "setup_runs": 0}
        (run / "prediction.json").write_text(json.dumps(pred), encoding="utf-8")
    out = tmp_path / "out.json"
    asyncio.run(score.main_async("test", 1, out, sealed, {4}))
    assert [r["run"] for r in json.loads(out.read_text())["rows"]] == [4]
    asyncio.run(score.main_async("test", 1, out, sealed))
    assert [r["run"] for r in json.loads(out.read_text())["rows"]] == [1, 4]


def test_clopper_pearson_matches_known_values():
    from score import clopper_pearson

    zero = clopper_pearson(0, 48)
    assert zero["lo"] == 0.0 and abs(zero["hi"] - (1 - 0.025 ** (1 / 48))) < 1e-3  # 0.0740
    mid = clopper_pearson(5, 10)  # textbook: (0.1871, 0.8129)
    assert abs(mid["lo"] - 0.1871) < 1e-3 and abs(mid["hi"] - 0.8129) < 1e-3
    assert clopper_pearson(10, 10)["hi"] == 1.0
