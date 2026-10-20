"""`gapfinder harness` end to end on a toy repo (local backend, environment given, no model call): the claims, the
command, the preprocessing step, the data kept and the outputs dropped, the metric binding, the spec, and a
search's naive run on the written spec."""

import json
import textwrap
from datetime import date

import yaml

from gapfinder.harness_build import build_harness
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec

README = textwrap.dedent('''\
    # Toy
    ## Run
        python preprocess.py --dataset alpha
        python main.py --dataset alpha --lr 0.1
    ''')
PREP = textwrap.dedent('''\
    import argparse, os
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", default="alpha")
    a = p.parse_args()
    open(os.path.join("data", a.dataset, "processed.txt"), "w").write("ok")
    ''')
MAIN = textwrap.dedent('''\
    import argparse, os
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", default="alpha")
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--epochs", type=int, default=3)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--save_dir", default="ckpt")
    a = p.parse_args()
    assert open(os.path.join("data", a.dataset, "processed.txt")).read() == "ok"
    cache = os.path.join("data", a.dataset, "cache.bin")
    if not os.path.exists(cache):  # a loader's download
        open(cache, "wb").write(b"x" * 1000)
    os.makedirs(a.save_dir, exist_ok=True)
    open(os.path.join(a.save_dir, "model.pt"), "wb").write(b"m")
    noise = (a.seed % 7) / 1000.0
    for e in range(a.epochs):
        acc = 0.5 + 0.1 * e + noise - abs(a.lr - 0.1)
        print("epoch %d train acc: %.4f test acc: %.4f test f1: %.4f" % (e, acc + 0.2, acc, acc - 0.05))
    ''')


def _toy(root):
    root.mkdir(parents=True)
    (root / "README.md").write_text(README, encoding="utf-8")
    (root / "preprocess.py").write_text(PREP, encoding="utf-8")
    (root / "main.py").write_text(MAIN, encoding="utf-8")
    for d in ("alpha", "beta"):
        (root / "data" / d).mkdir(parents=True)
        (root / "data" / d / "raw.txt").write_text(d, encoding="utf-8")
    return root


LEDGER = {"claims": [
    {"id": "C1", "metric": "Accuracy", "reported_value": 70.0, "unit": "%", "type": "absolute",
     "figure_or_table": "Table 1", "conditions": {"dataset": "Beta", "model": "Toy"}},
    {"id": "C2", "metric": "F1", "reported_value": 65.0, "unit": "%", "type": "absolute",
     "figure_or_table": "Table 1", "conditions": {"dataset": "Beta", "model": "Toy"}},
    {"id": "C3", "metric": "Accuracy", "reported_value": 71.0, "unit": "%", "type": "absolute",
     "figure_or_table": "Table 1", "conditions": {"dataset": "Alpha", "model": "Toy"}},
    # a learning curve's point, a sensitivity cell at a knob's value, and one whose setting is no knob
    {"id": "C4", "metric": "Accuracy", "reported_value": 60.0, "unit": "%", "type": "absolute",
     "figure_or_table": "Figure 2", "conditions": {"dataset": "Beta", "model": "Toy", "epoch": "2"}},
    {"id": "C5", "metric": "Accuracy", "reported_value": 90.0, "unit": "%", "type": "absolute",
     "figure_or_table": "Table 4", "conditions": {"dataset": "Beta", "epochs": "5"}},
    {"id": "C6", "metric": "Accuracy", "reported_value": 66.0, "unit": "%", "type": "absolute",
     "figure_or_table": "Table 5", "conditions": {"dataset": "Beta", "hidden size": "8"}}]}


async def test_harness_end_to_end(tmp_path):
    repo = _toy(tmp_path / "toy")
    backend = LocalBackend(tmp_path / "sbx")
    env = await backend.base("local:" + str(repo))
    out = tmp_path / "h"
    r = await build_harness(None, backend, repo=None, commit=None, local=repo, ledger=LEDGER, target="C1", out=out,
                            repeats=2, smoke_timeout=120, env_checkpoint=env, paper_date=date(2019, 1, 1))
    md = (out / "HARNESS.md").read_text(encoding="utf-8")
    assert r.ok, md
    assert [c["claim_id"] for c in r.claims] == ["C1", "C2"]
    assert any("preprocess.py --dataset beta" in p for p in r.prep)
    assert "--dataset beta" in r.templated.naive
    kept = {f["path"] for f in r.manifest["kept"]}
    assert "data/beta/processed.txt" in kept and "data/beta/cache.bin" in kept
    assert "ckpt/model.pt" in r.manifest["dropped"]
    b = {x.claim_id: x for x in r.bindings}
    assert b["C1"].label == "test acc" and b["C1"].scale == 100.0 and b["C2"].label == "test f1"
    assert r.smoke["seeds_vary"] is True and r.plan.action == "as is"
    spec_d = yaml.safe_load((out / "spec.yaml").read_text(encoding="utf-8"))
    assert set(spec_d["knobs"]) == {"lr", "epochs", "dataset"} and spec_d["knobs"]["lr"]["default"] == "0.1"
    # plan D2.1: the Alpha row (C3) is the target's cell on another dataset whose README command is known, so the
    # dataset flag is a condition knob (never searched) and C3 a claim at dataset=alpha
    assert spec_d["knobs"]["dataset"] == {"layer": "config", "default": "beta", "condition": True}
    assert "--dataset {dataset}" in spec_d["run"]["command"]
    assert any("preprocess.py --dataset alpha" in p for p in r.prep)
    assert r.paper_year["pins"] == {}  # the toy imports no third-party package: no paper-year knob
    assert [p["claim_id"] for p in r.points] == ["C5", "C3"] and r.points[0]["at"] == {"epochs": "5"}
    assert r.points[1]["at"] == {"dataset": "alpha"} and r.points[1]["condition"] == "alpha"
    assert [c["name"] for c in r.curves] == ["c1_acc_e2"] and [u["claim_id"] for u in r.unmapped] == ["C6"]
    targets = json.loads((out / "targets.json").read_text(encoding="utf-8"))
    assert [t["metric"] for t in targets] == ["c1_acc", "c2_f1", "c1_acc", "c1_acc", "c1_acc_e2"] and targets[1]["held_out"]
    assert targets[2]["at"] == {"epochs": "5"} and targets[3]["at"] == {"dataset": "alpha"}

    # the written spec runs: the base checkpoint has the data, so the naive run parses both claims
    spec = HarnessSpec.load_yaml(out / "spec.yaml")
    spec.base = "local:" + str(backend.images / spec.base)  # Sandboxes take a checkpoint id; the local backend a folder
    orch = Orchestrator(backend, spec, EventLog(tmp_path / "ev.jsonl"))
    branch = await orch.run_branch({})
    assert branch.parsed_metrics["gf_runs"] == 2, branch.note
    assert abs(branch.parsed_metrics["c1_acc"] - 70.0) < 2.0
    assert abs(branch.parsed_metrics["c2_f1"] - 65.0) < 2.0
    assert abs(branch.parsed_metrics["c1_acc_e2"] - 60.0) < 2.0  # the paper's epoch 2 is the log's epoch 1
    other = await orch.run_branch({"dataset": "alpha"})  # the condition knob: the other dataset's data is there too
    assert other.status.value == "succeeded" and "c1_acc" in other.parsed_metrics, other.note


async def test_shard_mean_averages_repeats_run_as_shards(tmp_path):
    art = tmp_path / "art"
    art.mkdir()
    (tmp_path / "s.yaml").write_text(textwrap.dedent(f"""\
        name: shards
        base: "local:{art.as_posix()}"
        run:
          command: 'echo acc=0.{{shard}}; echo f1=0.5'
          output: stdout
          format: kv
          shards: ["2", "4"]
          shard_mean: true
        metrics: [acc, f1]
        """), encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    branch = await Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl")).run_branch({})
    assert abs(branch.parsed_metrics["acc"] - 0.3) < 1e-9 and branch.parsed_metrics["f1"] == 0.5


async def test_an_infrastructure_error_writes_harness_md_with_the_step(tmp_path):
    """Plan D6.2: a Sandboxes failure mid-harness (b5c: HTTP 500 in the smoke run) leaves a HARNESS.md that names
    the step, instead of a crash with no record."""
    from gapfinder.sandbox.backend import InfraError

    repo = _toy(tmp_path / "toy")
    backend = LocalBackend(tmp_path / "sbx")
    env = await backend.base("local:" + str(repo))
    real = backend.run
    calls = {"n": 0}

    async def flaky(*a, **k):
        calls["n"] += 1
        if calls["n"] == 2:  # the data step passes, the smoke run fails
            raise InfraError("ApiStatusCodeError(status=500, error='Internal Server Error')")
        return await real(*a, **k)

    backend.run = flaky
    out = tmp_path / "h"
    r = await build_harness(None, backend, repo=None, commit=None, local=repo, ledger=LEDGER, target="C1", out=out,
                            repeats=1, smoke_timeout=60, env_checkpoint=env)
    md = (out / "HARNESS.md").read_text(encoding="utf-8")
    assert not r.ok and r.stage == "smoke" and "infrastructure error" in r.reason and "status=500" in md
