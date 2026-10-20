"""The automatic harness's fixed rules (gapfinder/harness_build.py): claims, templating, the in-VM emitter."""

import subprocess
import sys
import textwrap

from gapfinder.harness_auto import labelled_numbers
from gapfinder.harness_build import emit_script, progress_estimate, select_claims, template_command

MAIN = textwrap.dedent('''\
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", type=str, default="alpha")
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--epochs", type=int, default=20)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--use_bn", action="store_true")
    p.add_argument("--gpu", type=int, default=0)
    p.add_argument("--all_hops", type=bool, default=True)
    p.add_argument("--save_dir", default="ckpt")
    p.add_argument("--mode", default="sum", choices=["sum", "mean"])
    """
    p.add_argument("--lr", type=float, default=0.5)   # an old setting in a string block: not a call
    """
    ''')


def _repo(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text(MAIN, encoding="utf-8")
    for d in ("alpha", "beta"):
        (tmp_path / "data" / d).mkdir(parents=True)
    return tmp_path


CLAIM = {"claim_id": "C1", "metric": "Accuracy", "conditions": {"dataset": "Beta-Set", "model": "Toy"}}


def test_template_every_flag_a_knob_except_the_fixed_ones(tmp_path):
    t = template_command(_repo(tmp_path), "cd src && python main.py --dataset alpha --lr 0.01", [CLAIM])
    assert set(t.knobs) == {"lr", "epochs", "use_bn", "mode"}
    assert t.knobs["lr"]["default"] == "0.01"  # the command's value, not the code's
    assert t.knobs["mode"]["choices"] == ["sum", "mean"]
    assert t.knobs["use_bn"] == {**t.knobs["use_bn"], "default": "0", "choices": ["0", "1"]}
    assert {"dataset", "seed", "gpu", "all_hops", "save_dir"} <= set(t.fixed)
    assert "--dataset beta" in t.naive and "'beta'" not in t.naive  # the claim's dataset, from data/
    assert "--seed $GF_SEED" in t.command and "--lr {lr}" in t.command and t.epochs_knob == "epochs"
    assert t.command.startswith("cd src && ")


def test_select_claims_takes_the_row_and_skips_other_conditions():
    ledger = {"claims": [
        {"id": "C1", "metric": "AUC", "reported_value": 0.73, "conditions": {"dataset": "Book", "model": "R"},
         "figure_or_table": "Table 3", "type": "absolute"},
        {"id": "C2", "metric": "Accuracy", "reported_value": 0.66, "conditions": {"dataset": "Book", "model": "R"},
         "figure_or_table": "Table 3", "type": "absolute"},
        {"id": "C3", "metric": "AUC", "reported_value": 0.92, "conditions": {"dataset": "Movie", "model": "R"},
         "figure_or_table": "Table 3", "type": "absolute"},
        {"id": "C4", "metric": "AUC", "reported_value": 0.70, "conditions": {"dataset": "Book", "model": "CKE"},
         "figure_or_table": "Table 3", "type": "absolute"}]}
    got = select_claims(ledger, "C1")
    assert [c["claim_id"] for c in got] == ["C1", "C2"] and got[1]["held_out"] and not got[0]["held_out"]
    assert got[0]["name"] == "c1_auc" and got[1]["name"] == "c2_acc"


def test_emitter_reads_labels_exactly_as_the_binder(tmp_path):
    log = "epoch 0 train auc: 0.91 acc: 0.80 test auc: 0.70 acc: 0.62\nEnd. best test auc = 71.5%\nloss: 0.3\n"
    found = labelled_numbers(log)
    best = next(k for k in found if k.startswith("best test"))  # "best test End. auc"
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / "run1.log").write_text(log, encoding="utf-8")
    (tmp_path / "out" / "run2.log").write_text(log.replace("0.62", "0.64"), encoding="utf-8")
    (tmp_path / "emit.py").write_text(emit_script({"c1_auc": ("test auc", 1.0), "c2_acc": ("test acc", 100.0),
                                                   "c1_auc__0": (best, 1.0)}), encoding="utf-8")
    out = subprocess.run([sys.executable, "emit.py"], cwd=tmp_path, capture_output=True, text=True).stdout
    vals = dict(line.split("=", 1) for line in out.splitlines())
    assert float(vals["c1_auc"]) == found["test auc"] == 0.70
    assert abs(float(vals["c2_acc"]) - 63.0) < 1e-9  # mean of 0.62 and 0.64, on the paper's percent scale
    assert float(vals["c1_auc__0"]) == found[best] == 0.715
    assert vals["gf_runs"] == "2"


def test_progress_estimate_extrapolates_from_the_epoch_counter():
    log = "\n".join(f"epoch {i} loss: 1" for i in range(5))  # 0-based: 5 of 20 epochs done
    assert progress_estimate(log, 100.0, 20) == 400.0
    assert progress_estimate("no counter", 100.0, 20) is None


def test_emitter_matches_the_binder_on_bare_metrics_and_line_tags(tmp_path):
    log = ("198Z :acc 0.9000 , nmi 0.6800 , ari 0.7300 , f1 0.9000\n"
           "199Q :acc 0.8695 , nmi 0.5890 , ari 0.6525 , f1 0.8684\n"
           "199Z :acc 0.9045 , nmi 0.6831 , ari 0.7391 , f1 0.9042\n"
           "inj_cora DOMINANT AUC: 0.8270+-0.0560 (0.8430)\tAP: 0.2000+-0.0300 (0.2080)\tRecall: 0.2380+-0.0400 (0.2610)\n"
           "batch 64 lr 0.001\n")
    found = labelled_numbers(log)
    assert found["Z acc"] == 0.9045 and found["Q acc"] == 0.8695 and found["AP"] == 0.2
    assert "batch" not in found and "lr" not in found  # not metric names
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / "run1.log").write_text(log, encoding="utf-8")
    labels = ["Z acc", "Q nmi", "inj_cora DOMINANT AUC", "AP", "Recall"]
    (tmp_path / "emit.py").write_text(emit_script({f"m{i}": (k, 1.0) for i, k in enumerate(labels)}), encoding="utf-8")
    out = subprocess.run([sys.executable, "emit.py"], cwd=tmp_path, capture_output=True, text=True).stdout
    vals = dict(line.split("=", 1) for line in out.splitlines())
    assert [float(vals[f"m{i}"]) for i in range(len(labels))] == [found[k] for k in labels]


def test_short_options_and_the_repo_root(tmp_path):
    """`-d Synthetic` stays `-d` (not `--d`, which argparse rejects as ambiguous with --dataset and --data_dir); a
    script in a subfolder gets the repository's root on its import path (pygcn/train.py imports pygcn.utils)."""
    from gapfinder.harness_build import template_command

    (tmp_path / "pk").mkdir()
    (tmp_path / "pk" / "main.py").write_text(
        "import argparse\np = argparse.ArgumentParser()\np.add_argument('-d', '--dataset', default='Adult')\n"
        "p.add_argument('--data_dir', default='x')\np.add_argument('--seed', type=int, default=0)\na = p.parse_args()\n",
        encoding="utf-8")
    t = template_command(tmp_path, "cd pk && python main.py -d Synthetic --seed 0",
                         [{"metric": "acc", "conditions": {"dataset": "Synthetic"}}])
    assert "--dataset Synthetic" in t.naive and "--d " not in t.naive
    assert t.naive.startswith('cd pk && PYTHONPATH="$OLDPWD')
