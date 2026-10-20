"""Plan D1.2/D7.1: reporting rules from the runs already made, and the calibration gate.

A toy trainer prints validation and test metrics every epoch; the harness's real emitter summarises the trajectory.
The paper's numbers are, in turn: each metric's best epoch (a flaw: chosen with the test labels), the test metrics at
the best validation epoch (a legitimate protocol the code doesn't implement), and the numbers at the end with a
different learning rate (a setting: the gate must stay out of the way)."""

import textwrap

from gapfinder.harness_build import TRAJECTORY_STATS, emit_script
from gapfinder.ledger.schemas import Assumption, Evidence
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target

TEST_ACC = [0.60, 0.66, 0.70, 0.73, 0.75, 0.77, 0.78, 0.79, 0.80, 0.79, 0.785, 0.78, 0.775, 0.77, 0.765, 0.76, 0.755,
            0.75, 0.745, 0.74]  # peaks at epoch 8, ends at 0.74
VAL_ACC = [0.58, 0.64, 0.69, 0.72, 0.74, 0.76, 0.755, 0.75, 0.745, 0.74, 0.735, 0.73, 0.725, 0.72, 0.715, 0.71,
           0.705, 0.70, 0.695, 0.69]  # peaks at epoch 5
TEST_F1 = [0.50, 0.55, 0.58, 0.60, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.70, 0.69, 0.685, 0.68, 0.675,
           0.67, 0.665, 0.66]  # peaks at epoch 12

BENCH = textwrap.dedent(f'''\
    import argparse, hashlib, os
    p = argparse.ArgumentParser()
    p.add_argument("--lr", type=float, default=0.01)
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 25000.0
    shift = 0.03 if a.lr == 0.1 else 0.0
    T, V, F = {TEST_ACC!r}, {VAL_ACC!r}, {TEST_F1!r}
    for e in range(20):
        print("epoch %d val acc: %.4f test acc: %.4f test f1: %.4f" % (e, V[e] + shift + noise, T[e] + shift + noise,
                                                                       F[e] + shift + noise))
    ''')
NAMES = {"c1_acc": "test acc", "c2_f1": "test f1"}


def _search(tmp_path, paper: dict[str, float]) -> GapSearch:
    art = tmp_path / "art"
    art.mkdir(parents=True)
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    traj = {"c1_acc": {"label": "test acc", "scale": 100.0, "dir": 1, "val": "val acc", "target": True},
            "c2_f1": {"label": "test f1", "scale": 100.0, "dir": 1, "val": None, "target": False}}
    (art / "emit.py").write_text(emit_script({k: (v, 100.0) for k, v in NAMES.items()}, traj), encoding="utf-8")
    metrics = list(NAMES) + [f"{n}__x_{k}" for n in NAMES for k in TRAJECTORY_STATS] + ["gf_runs"]
    (tmp_path / "s.yaml").write_text(textwrap.dedent(f"""\
        name: reporting
        base: "local:{art.as_posix()}"
        run:
          command: 'mkdir -p out; rm -f out/run*.log; ("${{PYTHON:-python3}}" bench.py --lr {{lr}}) > out/run1.log 2>&1; "${{PYTHON:-python3}}" emit.py'
          output: stdout
          format: kv
          timeout: 60
        knobs:
          lr: {{layer: config, default: "0.01"}}
        allowed_paths: ["out/"]
        metrics: {metrics}
        """), encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm = [Assumption(id="A1", knob="lr", layer="config", paper_value="unstated", candidate_values=["0.1"],
                      evidence=[Evidence(kind="code", ref="toy", quote="lr is sometimes 0.1")], prior_score=0.6,
                      status="unstated")]
    targets = [Target("C1", "c1_acc", paper["C1"]), Target("C2", "c2_f1", paper["C2"], held_out=True)]
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=40, trace=False, hm_disc=0.01, coverage=False,
                                                      screen_spec_knobs=False, patch_knobs=False))


async def test_best_epoch_chosen_with_the_test_labels_is_found_without_a_search(tmp_path):
    s = _search(tmp_path, {"C1": 80.0, "C2": 70.0})  # each metric's best epoch
    [r] = await s.run()
    assert r.attribution.confidence_label == "Explained by the reporting rule", r.notes
    assert r.reporting["rule"] == "best" and r.reporting["flaw"] is True
    assert s.runs_used == 5  # the naive runs only: no settings search
    assert r.differential["ranked"][0]["id"] == "reporting:best"
    assert any("flaw" in n for n in r.notes)


async def test_early_stopping_on_validation_is_a_protocol_not_a_flaw(tmp_path):
    s = _search(tmp_path, {"C1": 77.0, "C2": 62.0})  # the test metrics at the best validation epoch
    [r] = await s.run()
    assert r.attribution.confidence_label == "Explained by the reporting rule", r.notes
    assert r.reporting["rule"] == "bestval" and r.reporting["flaw"] is False


async def test_a_setting_cause_is_not_taken_for_a_reporting_rule(tmp_path):
    s = _search(tmp_path, {"C1": 77.0, "C2": 69.0})  # lr = 0.1, read at the end: no reading of the naive runs fits
    [r] = await s.run()
    assert r.reporting is None and r.changes == {"lr": "0.1"}, (r.notes, r.changes)
    ranked = [h["id"] for h in r.differential["ranked"]]
    assert ranked[0] == "settings:lr=0.1", ranked
