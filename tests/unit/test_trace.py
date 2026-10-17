"""Runtime sink tracing (gapfinder/sandbox/trace_hook.py + gapfinder/search/trace.py).

The hook runs for real, in a subprocess, on a small "artifact" that uses argparse, a YAML config, numpy's
seed, range() loops and a fake `torch` package laid out like the real one (the hook watches module names
such as torch.optim.optimizer, so the fake keeps them)."""

import json
import os
import subprocess
import sys
import textwrap

import pytest

from gapfinder.sandbox.spec import Knob
from gapfinder.sandbox.trace_hook import HOOK_DIR, HOOK_SOURCE, MARKER, parse_output
from gapfinder.search.hypotheses import coverage_values
from gapfinder.search.trace import analyze, apply_roles

FAKE_TORCH = {
    "torch/__init__.py": "from torch import optim, nn, utils\ndef manual_seed(seed):\n    return seed\n",
    "torch/optim/__init__.py": "from torch.optim.optimizer import Optimizer\nfrom torch.optim.adam import Adam\n"
                               "from torch.optim import lr_scheduler\n",
    "torch/optim/optimizer.py": "class Optimizer:\n    def __init__(self, params, defaults):\n"
                                "        self.defaults = defaults\n    def zero_grad(self):\n        pass\n",
    "torch/optim/adam.py": "from torch.optim.optimizer import Optimizer\nclass Adam(Optimizer):\n"
                           "    def __init__(self, params, lr=1e-3, betas=(0.9, 0.999), weight_decay=0):\n"
                           "        super().__init__(params, dict(lr=lr, betas=betas, weight_decay=weight_decay))\n",
    "torch/optim/lr_scheduler.py": "class StepLR:\n    def __init__(self, optimizer, step_size, gamma=0.1):\n"
                                   "        self.step_size = step_size\n",
    "torch/nn/__init__.py": "from torch.nn.modules.dropout import Dropout\n",
    "torch/nn/modules/__init__.py": "",
    "torch/nn/modules/dropout.py": "class _DropoutNd:\n    def __init__(self, p=0.5, inplace=False):\n"
                                   "        self.p = p\nclass Dropout(_DropoutNd):\n    pass\n",
    "torch/utils/__init__.py": "from torch.utils import data\n",
    "torch/utils/data/__init__.py": "from torch.utils.data.dataloader import DataLoader\n",
    "torch/utils/data/dataloader.py": "class DataLoader:\n    def __init__(self, dataset, batch_size=1, shuffle=False):\n"
                                      "        self.batch_size = batch_size\n",
}

ARTIFACT = {
    "cfg.yml": "batch_size: 64\nbase_epochs: 40\n",
    "model.py": textwrap.dedent("""\
        import torch
        EVAL_BATCH = 128

        def loaders(ds, bs):
            train = torch.utils.data.DataLoader(ds, batch_size=bs, shuffle=True)
            test = torch.utils.data.DataLoader(ds, batch_size=EVAL_BATCH)
            return train, test
        """),
    "train.py": textwrap.dedent("""\
        import argparse, yaml, numpy as np, torch
        from model import loaders
        p = argparse.ArgumentParser()
        p.add_argument("--lr", type=float, default=0.01)
        p.add_argument("--dropout", type=float, default=0.3)
        p.add_argument("--epochs", type=int, default=7)
        p.add_argument("--epochx", type=int, default=3)
        p.add_argument("--seed", type=int, default=12345)
        a = p.parse_args()
        cfg = yaml.safe_load(open("cfg.yml"))
        np.random.seed(a.seed)
        torch.manual_seed(a.seed)
        drop = torch.nn.Dropout(a.dropout)
        opt = torch.optim.Adam([], lr=a.lr)
        sched = torch.optim.lr_scheduler.StepLR(opt, step_size=a.epochs)
        train, test = loaders(list(range(10)), cfg["batch_size"])
        for i in range(a.epochx * cfg["base_epochs"]):
            pass
        for e in range(a.epochs):
            opt.zero_grad()
        print("done")
        """),
}

KNOBS = {"lr": "0.01", "dropout": "0.3", "epochs": "7", "epochx": "3", "seed": "12345", "batch_size": "64",
         "base_epochs": "40"}


def _write(root, files):
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)


def _trace(tmp_path, steps=0, seconds=0):
    art, lib = tmp_path / "work", tmp_path / "lib"
    _write(art, ARTIFACT)
    _write(lib, FAKE_TORCH)
    (art / HOOK_DIR).mkdir()
    (art / HOOK_DIR / "sitecustomize.py").write_text(HOOK_SOURCE)
    out = art / ".gf_trace_out"
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(art / HOOK_DIR), str(lib)]),
           "GF_TRACE_ROOT": str(art), "GF_TRACE_DIR": str(out), "GF_TRACE_STEPS": str(steps),
           "GF_TRACE_SECONDS": str(seconds)}
    r = subprocess.run([sys.executable, "train.py"], cwd=art, env=env, capture_output=True, text=True, timeout=120)
    recs = [json.loads(p.read_text()) for p in out.glob("*.json")]
    return r, recs, art


@pytest.fixture
def traced(tmp_path):
    r, recs, art = _trace(tmp_path)
    assert r.returncode == 0, r.stderr
    assert "done" in r.stdout and len(recs) == 1
    return recs, art


def test_the_hook_records_config_and_sinks_without_changing_the_run(traced):
    recs, _ = traced
    rec = recs[0]
    srcs = {c["src"] for c in rec["config"]}
    assert {"argparse", "yaml"} <= srcs
    kinds = {s["kind"] for s in rec["sinks"]}
    assert {"optimizer", "dropout", "batch", "scheduler", "seed"} <= kinds
    lr = next(s for s in rec["sinks"] if s["kind"] == "optimizer")
    assert lr["args"]["lr"] == 0.01 and lr["site"] == ["train.py", 14]  # the repo line, not the fake library
    assert rec["steps"] == 7


def test_roles_come_from_sinks_not_names(traced):
    recs, art = traced
    knobs = {k: Knob(layer="config", default=v) for k, v in KNOBS.items()}
    rep = analyze(recs, knobs, repo_root=art)
    roles = {k: r.role for k, r in rep.roles.items()}
    assert roles["lr"] == "rate"
    assert roles["dropout"] == "fraction"
    assert roles["batch_size"] == "size"  # a YAML value reaching DataLoader(batch_size=...)
    assert roles["seed"] == "seed"
    assert roles["epochx"] == "multiplier"  # range(epochx * base_epochs): the bound is a product
    assert roles["epochs"] == "count"  # range(epochs), and StepLR(step_size=epochs): both counts
    # the hard-coded EVAL_BATCH = 128 has no knob: it becomes a patch-knob lead at its assignment
    assert [(x.file, x.line, x.name, x.literal) for x in rep.leads] == [("model.py", 2, "EVAL_BATCH", "128")]
    assert rep.leads[0].knob == "@ast:model.py:2:EVAL_BATCH"


def test_a_shared_value_is_ambiguous_not_guessed(tmp_path):
    knobs = {"lr": Knob(layer="config", default="0.01"), "eps": Knob(layer="config", default="0.01")}
    recs = [{"config": [], "sinks": [{"kind": "optimizer", "cls": "Adam", "args": {"weight_decay": 0.01},
                                      "site": ["t.py", 3]}], "ranges": {}}]
    rep = analyze(recs, knobs)
    assert rep.roles == {} and rep.ambiguous[0]["knobs"] == ["eps", "lr"]


def test_a_config_file_that_overrides_a_flag_is_seen_as_it_runs():
    """GraphMAE: configs.yml overrides the flags; the traced runtime value is what matches the sink."""
    knobs = {"lr": Knob(layer="config", default="0.005")}  # the flag's default; the config sets 0.00015
    recs = [{"config": [{"src": "argparse", "values": {"lr": 0.005}}, {"src": "yaml", "values": {"COLLAB.lr": 0.00015}}],
             "sinks": [{"kind": "optimizer", "cls": "Adam", "args": {"lr": 0.00015}, "site": ["m.py", 9]}], "ranges": {}}]
    rep = analyze(recs, knobs)
    assert rep.runtime_values == {"lr": "0.00015, 0.005"} and rep.roles["lr"].role == "rate"


def test_roles_drive_candidate_values():
    lr = Knob(layer="config", default="0.1")
    assert "0.91" in coverage_values(lr, "alpha")  # untraced, a name the rules don't know: fraction steps
    lr.role = "rate"
    vals = coverage_values(lr, "alpha")
    assert "0.91" not in vals and "0.0" not in vals and "1" in vals  # log scale, no fraction steps, no zero
    assert coverage_values(Knob(layer="config", default="12345", role="seed"), "seed") == []
    bs = coverage_values(Knob(layer="config", default="128", role="size"), "bsz")
    assert bs[:4] == ["64", "256", "32", "512"]
    spec_like = type("S", (), {"knobs": {"m": Knob(layer="config", default="3")}})()
    from gapfinder.search.trace import KnobRole, TraceReport
    rep = TraceReport(roles={"m": KnobRole("m", "multiplier", "range()", "t.py:1", "3")})
    assert apply_roles(spec_like, rep) == ["m"] and spec_like.knobs["m"].multiplier


def test_a_dry_run_stops_itself_and_still_writes_the_trace(tmp_path):
    r, recs, _ = _trace(tmp_path, steps=2)
    assert r.returncode == 0 and "done" not in r.stdout  # stopped after 2 optimizer steps
    assert len(recs) == 1 and recs[0]["steps"] == 3


def test_parse_output_reads_marker_lines():
    text = "noise\n" + MARKER + json.dumps({"pid": 1, "sinks": []}) + "\n" + MARKER + "{broken\n"
    assert parse_output(text) == [{"pid": 1, "sinks": []}]
