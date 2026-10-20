"""Plan D6.4-D6.7 on new toys: the README's procedure (train, then evaluate) as one cell; a binder's tie settled by the
paper's sentence; module constants as patch knobs when the script has few flags; memory-aware parallelism."""

import textwrap

import yaml

from gapfinder.harness_auto import Binding, bind_by_quote
from gapfinder.harness_build import build_harness, chain_steps, literal_knobs, memory_parallel, template_command
from gapfinder.harness_auto import Command
from gapfinder.sandbox.backend import LocalBackend

README = textwrap.dedent('''\
    # Toy
    ## Train, then evaluate
        python train.py --epochs 3 --lr 0.1 --save model.pkl
        python evaluate.py --ckpt model.pkl --dataset beta
    ''')
TRAIN = textwrap.dedent('''\
    import argparse, pickle
    p = argparse.ArgumentParser()
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--save", default="model.pkl")
    a = p.parse_args()
    w = 0.5 + 0.1 * a.epochs - abs(a.lr - 0.1)
    pickle.dump({"w": w}, open(a.save, "wb"))
    print("train loss: %.4f" % (1 - w))
    ''')
EVALUATE = textwrap.dedent('''\
    import argparse, pickle
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt", default="model.pkl")
    p.add_argument("--dataset", default="alpha")
    a = p.parse_args()
    w = pickle.load(open(a.ckpt, "rb"))["w"]
    print("test acc: %.4f" % (w - 0.1 * (a.dataset == "beta")))
    ''')
LEDGER = {"claims": [{"id": "C1", "metric": "Accuracy", "reported_value": 70.0, "unit": "%", "type": "absolute",
                      "figure_or_table": "Table 1", "conditions": {"dataset": "Beta", "model": "Toy"}}]}


def _repo(root):
    root.mkdir(parents=True)
    (root / "README.md").write_text(README, encoding="utf-8")
    (root / "train.py").write_text(TRAIN, encoding="utf-8")
    (root / "evaluate.py").write_text(EVALUATE, encoding="utf-8")
    return root


def test_the_procedure_chains_the_training_that_writes_what_the_evaluation_reads(tmp_path):
    repo = _repo(tmp_path / "toy")
    picked = Command("python evaluate.py --ckpt model.pkl --dataset beta", "README.md:5")
    steps = chain_steps(repo, picked)
    assert [s.cmd for s in steps] == ["python train.py --epochs 3 --lr 0.1 --save model.pkl", picked.cmd]
    assert chain_steps(repo, Command("python train.py --epochs 3 --lr 0.1 --save model.pkl", "README.md:4")) == [
        Command("python train.py --epochs 3 --lr 0.1 --save model.pkl", "README.md:4")]


async def test_the_chain_runs_as_one_cell(tmp_path):
    repo = _repo(tmp_path / "toy")
    backend = LocalBackend(tmp_path / "sbx")
    env = await backend.base("local:" + str(repo))
    out = tmp_path / "h"
    r = await build_harness(None, backend, repo=None, commit=None, local=repo, ledger=LEDGER, target="C1", out=out,
                            repeats=1, smoke_timeout=120, env_checkpoint=env)
    md = (out / "HARNESS.md").read_text(encoding="utf-8")
    assert r.ok, md
    spec = yaml.safe_load((out / "spec.yaml").read_text(encoding="utf-8"))
    cmd = spec["run"]["command"]
    assert "train.py" in cmd and "evaluate.py" in cmd and cmd.index("train.py") < cmd.index("evaluate.py")
    assert {"epochs", "lr"} <= set(spec["knobs"])  # the training's settings are knobs of the evaluated cell
    assert r.bindings[0].label == "test acc" and abs(r.bindings[0].value * 100 - 70.0) < 1e-6
    assert any("procedure:" in n for n in r.notes)


def test_a_tie_settled_by_the_papers_sentence():
    log = "epoch 9 Z acc: 0.7100 Q acc: 0.6900\n"
    tied = Binding("C1", None, alternatives=["Z acc", "Q acc"], refused="tie", tied=["Z acc", "Q acc"])
    b = bind_by_quote(tied, log, "We use Q as the reference. For evaluation we choose distribution Z, as in [3].")
    assert b is None  # both labels have a reporting sentence: still a refusal
    b = bind_by_quote(tied, log, "Results are averaged over seeds. For evaluation we choose distribution Z, as in [3].")
    assert b is not None and b.label == "Z acc" and abs(b.value - 0.71) < 1e-9 and "choose distribution Z" in b.quote
    assert bind_by_quote(tied, log, "Distribution Z is drawn from a Gaussian.") is None  # no reporting verb


def test_module_constants_become_patch_knobs_when_the_script_has_few_flags(tmp_path):
    (tmp_path / "main.py").write_text(textwrap.dedent('''\
        import argparse
        import config
        p = argparse.ArgumentParser()
        p.add_argument("--dataset", default="cora")
        a = p.parse_args()
        print(config.EPOCHS * config.LR)
        '''), encoding="utf-8")
    (tmp_path / "config.py").write_text("EPOCHS = 30\nLR = 0.01\nNAME_LEN = 4\nSEED = 0\n", encoding="utf-8")
    t = template_command(tmp_path, "python main.py --dataset cora", [{"metric": "acc", "conditions": {"dataset": "Cora"}}])
    knobs = literal_knobs(tmp_path, t, t.command)
    names = {k.split(":")[-1]: v["default"] for k, v in knobs.items()}
    assert names == {"EPOCHS": "30", "LR": "0.01"}, names  # settings, not every number (SEED, NAME_LEN are not)
    assert all(k.startswith("@ast:config.py:") for k in knobs)


def test_memory_aware_parallelism():
    assert memory_parallel(1500) == 2 and memory_parallel(700) == 4 and memory_parallel(4000) == 1
    assert memory_parallel(None) == 4
