"""Static out-of-space checks on a small synthetic repo."""

from gapfinder.ingest.code_checks import code_checks

TRAIN = '''
import argparse
import numpy as np
p = argparse.ArgumentParser()
p.add_argument("--lr", type=float, default=0.1)
a = p.parse_args()
np.random.seed(3)
n_epochs = np.loadtxt("data/n_epochs.txt")
batch_size = 128
lr = 0.5  # shadowed by the flag: not a lead
best_acc, best_c, best_model = 0, None, None
for c in [0.1, 1.0, 10.0]:
    acc = fit(c).score(X_test, y_test)
    if acc > best_acc:
        best_acc = acc
        best_c = c
        best_model = None
n_train = int(0.9 * len(X))
model.predict(X_test, batch_size=500)
'''


def _repo(tmp_path):
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "n_epochs.txt").write_text("40\n")
    (tmp_path / "train.py").write_text(TRAIN)
    (tmp_path / "py2.py").write_text("print 'old syntax'\n")  # unparseable: skipped
    return tmp_path


def test_leads_cover_each_family_and_skip_flags(tmp_path):
    leads = code_checks(_repo(tmp_path), {"lr"}, limit=50)
    by = {}
    for x in leads:
        by.setdefault(x.family, []).append(x.detail)
    assert any("best_c" in d and "TEST" in d for d in by["selection_in_code"])  # scored on test: leakage
    assert leads[0].family == "selection_in_code"  # leakage ranks first
    assert any("batch_size = 128" in d for d in by["unexposed_setting"])
    assert any("batch_size=500" in d and "evaluation" in d for d in by["unexposed_setting"])
    assert not any("`lr =" in d for d in by["unexposed_setting"])  # a flag sets it
    assert any("n_epochs" in d and "40" in d for d in by["file_setting"])
    assert by["fixed_seed"] and by["split_fraction"]


def test_flag_only_artifact_has_no_leads(tmp_path):
    (tmp_path / "t.py").write_text('import argparse\np = argparse.ArgumentParser()\np.add_argument("--epochs", default=5)\n')
    assert code_checks(tmp_path, {"epochs"}) == []


def test_a_parameter_default_no_call_overrides_is_a_lead(tmp_path):
    """Devset VGAE: `def mask_test_edges(adj, test_percent=30., val_percent=20.)` is always called as
    `mask_test_edges(adj)`, so its defaults are constants in disguise (the paper held out 10% and 5%)."""
    from gapfinder.ingest.code_checks import code_checks
    from gapfinder.sandbox.ast_patch import apply_source

    (tmp_path / "prep.py").write_text("def mask(adj, test_percent=30., val_percent=20.):\n    return adj\n"
                                      "def other(x, scale=2.5):\n    return x\n")
    (tmp_path / "train.py").write_text("from prep import mask, other\nmask(1)\nother(1, 3.0)\n")
    leads = code_checks(tmp_path)
    got = {(x.file, x.line, x.name, x.value) for x in leads}
    assert ("prep.py", 1, "test_percent", "30.0") in got and ("prep.py", 1, "val_percent", "20.0") in got
    assert not any(x.name == "scale" for x in leads)  # other() is called with it: not a hidden constant
    assert "test_percent=10.0" in apply_source((tmp_path / "prep.py").read_text(), 1, "test_percent", "10.")
