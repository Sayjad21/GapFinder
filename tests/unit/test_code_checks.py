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


def test_switches_and_label_edits_are_leads(tmp_path):
    from gapfinder.ingest.code_checks import code_checks

    (tmp_path / "data.py").write_text(
        "def loaders(ds, DataLoader):\n"
        "    train = DataLoader(ds, batch_size=32, shuffle=True, pin_memory=True)\n"
        "    test = DataLoader(ds, batch_size=32, shuffle=False, drop_last=True)\n"
        "    return train, test\n", encoding="utf-8")
    (tmp_path / "evaluate.py").write_text(
        "def adjust(gt, pred):\n"
        "    for i in range(len(gt)):\n"
        "        if gt[i] == 1 and pred[i] == 1:\n"
        "            for j in range(i, 0, -1):\n"
        "                pred[j] = 1\n"
        "    return pred\n", encoding="utf-8")
    leads = code_checks(tmp_path, limit=50)
    switches = {(x.line, x.name, x.value) for x in leads if x.family == "unexposed_setting" and x.value in ("True", "False")}
    assert (3, "drop_last", "True") in switches and (2, "shuffle", "True") in switches
    assert not any(n == "pin_memory" for _, n, _ in switches)  # how-to-run, not what is computed
    [lab] = [x for x in leads if x.family == "label_in_prediction"]
    assert (lab.file, lab.line, lab.name, lab.value) == ("evaluate.py", 3, "@if", "False")


def test_a_switch_patch_value_is_its_opposite_and_an_if_patch_replaces_the_condition():
    from gapfinder.sandbox.ast_patch import apply_source
    from gapfinder.search.hypotheses import patch_values

    assert patch_values("drop_last", "True") == ["False"] and patch_values("shuffle", "False") == ["True"]
    src = "best = 0\nfor x in [3, 1, 2]:\n    if x > best:\n        best = x\n"
    out = apply_source(src, 3, "@if", "True")
    ns: dict = {}
    exec(out, ns)
    assert ns["best"] == 2  # the last value, not the best


def test_preprocessing_fitted_on_test_data_or_before_the_split_is_leakage(tmp_path):
    """Yang et al. (ASE 2022), preprocessing leakage, in its two common forms; a clean pipeline has none."""
    from gapfinder.ingest.code_checks import code_checks

    (tmp_path / "leaky.py").write_text(
        "from sklearn.preprocessing import StandardScaler\n"
        "from sklearn.model_selection import train_test_split\n"
        "def run(X, y):\n"
        "    scaler = StandardScaler()\n"
        "    X = scaler.fit_transform(X)\n"
        "    X_tr, X_te, y_tr, y_te = train_test_split(X, y)\n"
        "    sc2 = StandardScaler()\n"
        "    sc2.fit(X_te)\n"
        "    return X_tr, X_te\n", encoding="utf-8")
    (tmp_path / "clean.py").write_text(
        "from sklearn.preprocessing import StandardScaler\n"
        "from sklearn.model_selection import train_test_split\n"
        "def run(X, y):\n"
        "    X_tr, X_te, y_tr, y_te = train_test_split(X, y)\n"
        "    scaler = StandardScaler().fit(X_tr)\n"
        "    return scaler.transform(X_tr), scaler.transform(X_te)\n", encoding="utf-8")
    leaks = [(x.file, x.line) for x in code_checks(tmp_path, limit=50) if x.family == "preprocessing_leakage"]
    assert leaks == [("leaky.py", 5), ("leaky.py", 8)]
