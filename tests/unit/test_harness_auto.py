"""Deterministic harness pieces (gapfinder/harness_auto.py): commands, data scripts, metric binding, fitting."""

from gapfinder.harness_auto import bind_metrics, download_steps, labelled_numbers, pick_commands, shrink_plan

RIPPLE = ("epoch 8    train auc: 0.9951  acc: 0.9700    eval auc: 0.6481  acc: 0.6185    test auc: 0.6495  acc: 0.6190\n"
          "epoch 9    train auc: 0.9957  acc: 0.9712    eval auc: 0.6489  acc: 0.6192    test auc: 0.6497  acc: 0.6195\n")
NCF = ("Iteration 18 [8.1 s]: HR = 0.6790, NDCG = 0.4071, loss = 0.2531 [1.2 s]\n"
       "Iteration 19 [8.0 s]: HR = 0.6779, NDCG = 0.4060, loss = 0.2522 [1.1 s]\n"
       "End. Best Iteration 3:  HR = 0.6877, NDCG = 0.4118.\n")
TSF = "mse:0.31066837906837463, mae:0.3720840513706207, rse:0.5011\n"


def test_labels_take_their_qualifier_from_the_line():
    got = labelled_numbers(RIPPLE)
    assert got["test auc"] == 0.6497 and got["test acc"] == 0.6195 and got["val auc"] == 0.6489
    assert got["train acc"] == 0.9712
    n = labelled_numbers(NCF)
    assert n["HR"] == 0.6779 and n["best HR"] == 0.6877  # the last epoch, and the best one, kept apart


def test_binding_prefers_test_and_final_and_matches_the_papers_scale():
    claims = [{"claim_id": "C1", "metric": "AUC", "paper_value": 0.729},
              {"claim_id": "C2", "metric": "ACC", "paper_value": 66.2}]
    b = {x.claim_id: x for x in bind_metrics(RIPPLE, claims)}
    assert (b["C1"].label, b["C1"].scale) == ("test auc", 1.0)
    assert (b["C2"].label, b["C2"].scale) == ("test acc", 100.0)  # printed as a fraction, the paper's in %
    assert "train auc" in b["C1"].alternatives
    hr = bind_metrics(NCF, [{"claim_id": "C3", "metric": "HR@10", "paper_value": 0.688}])
    assert hr[0].refused  # the log never says @10: no guess
    hr = bind_metrics(NCF, [{"claim_id": "C3", "metric": "HR", "paper_value": 0.688}])[0]
    assert hr.label == "HR" and "best HR" in hr.alternatives  # final first; best kept visible
    assert bind_metrics(TSF, [{"claim_id": "C4", "metric": "MSE", "paper_value": 0.312}])[0].label == "mse"


def test_binding_refuses_when_two_labels_fit_equally():
    log = "model A acc: 0.81\nmodel B acc: 0.79\n"
    [b] = bind_metrics(log, [{"claim_id": "C", "metric": "accuracy", "paper_value": 81.0}])
    assert b.label is None and "several" in b.refused


def test_commands_are_ranked_by_the_claims_words(tmp_path):
    (tmp_path / "README.md").write_text("## Run\n```\n$ cd src\n$ python preprocess.py --dataset movie (or --dataset book)\n"
                                        "$ python main.py --dataset movie\n```\n", encoding="utf-8")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "book.sh").write_text("python -u main.py --dataset book \\\n  --lr 1e-3 --n_hop 3\n",
                                                  encoding="utf-8")
    top = pick_commands(tmp_path, [{"metric": "AUC", "conditions": {"dataset": "Book-Crossing"}}])
    assert top[0].source.startswith("scripts/book.sh") and "book" in top[0].matched
    assert "--lr 1e-3 --n_hop 3" in top[0].cmd  # the continuation line joined


def test_data_scripts_are_found(tmp_path):
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "download_datasets.sh").write_text("wget ...", encoding="utf-8")
    (tmp_path / "get_data.py").write_text("print(1)", encoding="utf-8")
    assert download_steps(tmp_path) == ["cd /work && python get_data.py", "cd /work/data && bash download_datasets.sh"]


def test_the_shrink_rule_splits_before_it_shrinks():
    assert shrink_plan(900).action == "as is"
    assert shrink_plan(7000, independent_jobs=8).action == "shards"
    assert shrink_plan(7000, resumable=True).action == "segments"
    p = shrink_plan(10000)
    assert p.action == "shrink" and p.factor == 0.25 and p.discrepancy == 0.05


def test_gpu_only_packages_and_huge_files_are_blockers(tmp_path):
    from gapfinder.harness_auto import compute_blockers

    (tmp_path / "model.py").write_text("import torch\nfrom flash_attn import flash_attn_func\n", encoding="utf-8")
    (tmp_path / "requirements.txt").write_text("torch\nbitsandbytes==0.41\n", encoding="utf-8")
    got = compute_blockers(tmp_path)
    assert got == ["imports flash_attn (model.py:2)", "requires bitsandbytes (requirements.txt)"]
    (tmp_path / "model.py").write_text("import torch\n", encoding="utf-8")
    (tmp_path / "requirements.txt").write_text("torch\n", encoding="utf-8")
    assert compute_blockers(tmp_path) == []
