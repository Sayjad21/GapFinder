"""Plan F10: the curriculum's DeepCrime operators (real-fault code and data edits), the files a run reaches, why a
family can't be planted, and the scorer accepting the setting a DeepCrime edit amounts to."""

import importlib.util
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
TRAIN = textwrap.dedent('''\
    import argparse
    import torch
    from models import mlp, cnn, rnn
    from data import load
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="mlp")
    p.add_argument("--wd", type=float, default=0.0005)
    args = p.parse_args()
    net = (mlp if args.model == "mlp" else cnn).Net()
    opt = torch.optim.Adam(net.parameters(), lr=0.01, weight_decay=args.wd)
    idx = load()
    ''')
MLP = textwrap.dedent('''\
    import torch.nn as nn
    class Net(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc = nn.Linear(4, 2)
        def forward(self, x):
            return self.fc(x)
    ''')
CNN = MLP.replace("nn.Linear(4, 2)", "nn.Linear(8, 2)")
DATA = textwrap.dedent('''\
    def load():
        idx_train = range(100)
        return idx_train
    ''')


@pytest.fixture()
def cu(tmp_path, monkeypatch):
    monkeypatch.setenv("GF_CURRICULUM_DIR", str(tmp_path / "cur"))
    sys.path.insert(0, str(ROOT / "eval" / "planted"))
    spec = importlib.util.spec_from_file_location("curriculum_under_test", ROOT / "eval" / "planted" / "curriculum.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    yield mod
    sys.path.remove(str(ROOT / "eval" / "planted"))


def _case(tmp_path):
    from gapfinder.sandbox.spec import HarnessSpec

    art = tmp_path / "art"
    (art / "models").mkdir(parents=True)
    (art / "train.py").write_text(TRAIN, encoding="utf-8")
    (art / "data.py").write_text(DATA, encoding="utf-8")
    (art / "models" / "mlp.py").write_text(MLP, encoding="utf-8")
    (art / "models" / "cnn.py").write_text(CNN, encoding="utf-8")
    (art / "models" / "rnn.py").write_text(CNN, encoding="utf-8")
    (tmp_path / "s.yaml").write_text(
        f'name: dc\nbase: "local:{art.as_posix()}"\nsource: "{art.as_posix()}"\nrun:\n'
        "  command: 'python train.py --model mlp --wd {wd}'\n  output: out/run.log\n  format: kv\n"
        '  timeout: 30\nknobs:\n  wd: {layer: config, default: "0.0005"}\nallowed_paths: ["out/"]\nmetrics: [acc]\n',
        encoding="utf-8")
    return HarnessSpec.load_yaml(tmp_path / "s.yaml"), art


def test_code_sites_are_on_the_run_path_with_their_equivalent_setting(cu, tmp_path):
    spec, art = _case(tmp_path)
    sites = cu.deepcrime_sites("code", art, spec)
    ops = {(op, d.split(":", 1)[0]) for _, d, op, _ in sites}
    assert ("RRW", "train.py") in ops and ("WRB", "models/mlp.py") in ops, ops
    assert not any(d.startswith("models/cnn.py") for _, d, _, _ in sites)  # the command names mlp, not cnn
    rrw = next(s for s in sites if s[2] == "RRW")
    assert rrw[3] == {"wd": "0"}


def test_training_data_removed_keeps_a_share(cu, tmp_path):
    from gapfinder.sandbox import ast_patch

    spec, art = _case(tmp_path)
    sites = cu.deepcrime_sites("data", art, spec)
    assert {op for _, _, op, _ in sites} == {"TRD"} and len(sites) == 2
    rel, line, name = ast_patch.parse(sites[0][0])
    src = ast_patch.apply_source(DATA, line, name, "1")
    ns = {}
    exec(src, ns)
    assert len(ns["load"]()) == 50


def test_a_family_that_cant_be_planted_says_why(cu, tmp_path):
    import plant

    spec, art = _case(tmp_path)
    flags, lits = plant.candidates(spec, art)
    assert cu.unplantable("era", spec, art, flags, lits, tmp_path / "s.yaml") == "the harness has no paper-era code knob"
    assert "per-epoch" in cu.unplantable("reporting", spec, art, flags, lits, tmp_path / "s.yaml")
    assert cu.unplantable("code", spec, art, flags, lits, tmp_path / "s.yaml") is None


def test_the_scorer_takes_the_setting_a_deepcrime_edit_amounts_to(cu):
    part = {"family": "code", "knob": "@ast:train.py:10:@mut.6.Call.kwset.weight_decay.MA", "value": "1",
            "desc": "train.py:10: `torch.optim.Adam(...)` without its weight decay (DeepCrime RRW)",
            "equiv": {"wd": "0"}}
    assert cu._part_found(part, {"changes": {"wd": "0.0"}})
    assert not cu._part_found(part, {"changes": {"wd": "0.001"}})
