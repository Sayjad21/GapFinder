"""M2 integration tests against the local stand-in backend, on the hidden-knob toy."""

from pathlib import Path

import pytest

from gapfinder.ledger.schemas import BranchStatus
from gapfinder.sandbox.backend import InfraError, LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.sandbox.tree import CheckpointTree

TOY = Path(__file__).resolve().parents[2] / "eval" / "toy" / "hidden_knob.yaml"


@pytest.fixture
def spec():
    return HarnessSpec.load_yaml(TOY)


def make(tmp_path, spec, **kw):
    backend = LocalBackend(tmp_path / "sbx", emulate_dedup=kw.pop("dedup", False))
    return Orchestrator(backend, spec, EventLog(tmp_path / "events.jsonl"), **kw)


async def test_hidden_knob_fanout_parses_every_branch(tmp_path, spec):
    orch = make(tmp_path, spec)
    changes = [{}, {"alpha": "2.0"}, {"beta": "2.0"}, {"CACHE": "on"}, {"build_mode": "release"},
               {"num_rows": "5000"}]
    branches = await orch.fanout(changes)
    assert all(b.status == BranchStatus.succeeded for b in branches), [b.note for b in branches]
    by = {tuple(b.knob_changes.items()): b.parsed_metrics for b in branches}
    base = by[()]["score"]
    assert by[(("alpha", "2.0"),)]["score"] == pytest.approx(2 * base, rel=1e-3)  # planted knob found
    assert by[(("beta", "2.0"),)]["score"] < base  # decoy
    assert by[(("build_mode", "release"),)]["score"] == pytest.approx(3 * base, rel=1e-3)
    # depth planner: config/env branches share one build and one load; build/dataset knobs get their own
    stages = [n.stage for n in orch.tree.nodes.values()]
    assert stages.count("source") == 1
    assert stages.count("built") == 2  # debug (shared) + release
    assert stages.count("loaded") == 3  # default, release, 5000 rows
    assert orch.cost.setup_runs == 5


async def test_no_fork_ablation_rebuilds_every_branch(tmp_path, spec):
    orch = make(tmp_path, spec, no_fork=True)
    await orch.fanout([{}, {"alpha": "2.0"}, {"beta": "2.0"}, {"gamma": "2.0"}])
    assert orch.cost.setup_runs == 8  # 4 builds + 4 loads, vs 2 with forking


async def test_isolation_between_sibling_branches(tmp_path):
    be = LocalBackend(tmp_path / "sbx")
    root = await be.base("empty")
    a = await be.run(root, "echo secret > a.txt")
    b = await be.run(root, "test -f a.txt && echo present || echo absent")
    assert b.stdout.strip() == "absent"
    assert (await be.read_file(a.checkpoint, "a.txt")).strip() == b"secret"


async def test_concurrency_cap_queues_without_dropping(tmp_path, spec):
    orch = make(tmp_path, spec, concurrency=8)
    branches = await orch.fanout([{"alpha": str(1 + i / 100)} for i in range(12)])
    assert len(branches) == 12 and all(b.status == BranchStatus.succeeded for b in branches)
    assert orch.max_running_seen <= 8


async def test_failure_injection_statuses(tmp_path, spec):
    spec.run.timeout = 3
    orch = make(tmp_path, spec)
    crash, hang, garbage = await orch.fanout([{"fault": "--crash"}, {"fault": "--hang"}, {"fault": "--garbage"}])
    assert crash.status == BranchStatus.failed and "segfault" in crash.note
    assert hang.status == BranchStatus.timed_out
    assert garbage.status == BranchStatus.failed and "no metrics" in garbage.note


async def test_dedup_defeated_by_run_tag(tmp_path, spec):
    """With dedup emulated, identical commands would return one cached result;
    distinct RUN_TAGs force re-execution, so noise shows up across repeats."""
    orch = make(tmp_path, spec, dedup=True)
    bands, branches = await orch.calibrate_noise(n=5, changes={"noise": "0.05"})
    scores = {b.parsed_metrics["score"] for b in branches}
    assert len(scores) == 5
    assert bands["score"].band > 0
    be = orch.backend
    root = await be.base("empty")
    r1 = await be.run(root, "echo $RANDOM")
    r2 = await be.run(root, "echo $RANDOM")
    assert r1 is r2  # the dedup emulation itself works


async def test_infra_errors_retried_experiment_failures_not(tmp_path, spec):
    orch = make(tmp_path, spec)
    real_run, calls = orch.backend.run, {"n": 0}

    async def flaky(parent, shell, **kw):
        if "bench.py" in shell:
            calls["n"] += 1
            if calls["n"] < 3:
                raise InfraError("429 too many requests")
        return await real_run(parent, shell, **kw)

    orch.backend.run = flaky
    b = await orch.run_branch({})
    assert b.status == BranchStatus.succeeded and calls["n"] == 3
    calls["n"] = 10
    crash = await orch.run_branch({"fault": "--crash"})
    assert crash.status == BranchStatus.failed and calls["n"] == 11  # ran once, no retry


async def test_event_log_replays_tree(tmp_path, spec):
    orch = make(tmp_path, spec)
    await orch.fanout([{}, {"alpha": "2.0"}, {"build_mode": "release"}])
    assert CheckpointTree.replay(orch.events.read()).to_dict() == orch.tree.to_dict()
    tags = {n.tag for n in orch.tree.nodes.values() if n.tag}
    assert tags == {"gf/toy/source", "gf/toy/built", "gf/toy/loaded"}


async def test_adopted_checkpoints_are_not_rebuilt(tmp_path, spec):
    first = make(tmp_path, spec)
    loaded = await first.stage("loaded", {})
    built = first.tree.find_stage("built")
    second = make(tmp_path, spec)  # a new process: knows nothing about the first one's tree
    second.backend = first.backend
    second.adopt("built", built)
    second.adopt("loaded", loaded, parent=built)
    b = await second.run_branch({"alpha": "2.0"})
    assert b.status == BranchStatus.succeeded and b.parent_checkpoint == loaded
    assert second.cost.setup_runs == 0  # nothing rebuilt or reloaded
