"""Plan G1 and G4: the scale probe on new instances of the classes seed 4 showed.

(G1) A window the code counts in half-steps, whose effect is a few percent: far beyond the run noise, inside the
5% model-discrepancy allowance. The swept claims are off as run, so the convention is labelled a paper-artifact
inconsistency (c3 judged "off as run" with the allowance and called it 0 of 3).
(G4) A learning rate the paper states as a percent of the code's (the paper's v is the code's 0.01 x v), on a
model whose accuracy is log-linear in the rate (15 points a decade). A straight line through the measured rates puts
g(v) far off and rejects the factor; a log scale doesn't. When the curve can't reach g(v) at all, the factor is run."""

import textwrap

from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec

BENCH = textwrap.dedent('''\
    import argparse, hashlib, math, os
    p = argparse.ArgumentParser()
    p.add_argument("--window", type=int, default=8)
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--dropout", type=float, default=0.5)
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 100000.0
    acc = 80 + 0.3 * a.window + 15 * math.log10(a.lr / 0.01) - 0.2 * abs(a.dropout - 0.5)
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.5f\\n" % (acc + noise))
    ''')


def _acc(window=8, lr=0.01):
    import math

    return 80 + 0.3 * window + 15 * math.log10(lr / 0.01)


def _search(tmp_path, targets):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    (tmp_path / "s.yaml").write_text(textwrap.dedent(f"""\
        name: scale4
        base: "local:{art.as_posix()}"
        run:
          command: '"${{PYTHON:-python3}}" bench.py --window {{window}} --lr {{lr}} --dropout {{dropout}}'
          output: out/run.log
          format: kv
          timeout: 30
        knobs:
          window: {{layer: config, default: "8"}}
          lr: {{layer: config, default: "0.01"}}
          dropout: {{layer: config, default: "0.5"}}
        allowed_paths: ["out/"]
        metrics: [acc]
        """), encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=150, trace=False, patch_knobs=False))  # default hm_disc


async def test_a_small_convention_beyond_the_noise_is_labelled(tmp_path):
    # the paper's window w is the code's w / 2; each claim is 0.7-3% off as run, at a run spread of 0.0003
    targets = [Target("C1", "acc", _acc(window=4))] + [
        Target(f"P{w}", "acc", _acc(window=w // 2), held_out=True, at={"window": str(w)}) for w in (4, 16)]
    s = _search(tmp_path, targets)
    [r] = await s.run()
    assert r.changes == {"window": "4"}, (r.changes, r.notes)
    assert r.attribution.confidence_label == "Paper-artifact inconsistency", r.notes


async def _probe(tmp_path, measured: tuple[str, ...]):
    """The scale probe alone on a learning-rate curve measured at `measured` (the settings search on seed 4 had closed
    the target with other knobs before it measured small rates)."""
    from gapfinder.search.engine import ClaimResult

    # the paper's learning rate v is the code's 0.01 x v: its numbers are the code's at 1e-4, 5e-5 and 2e-4
    targets = [Target("C1", "acc", _acc(lr=1e-4))] + [
        Target(f"P{v}", "acc", _acc(lr=v * 0.01), held_out=True, at={"lr": str(v)}) for v in (0.005, 0.02)]
    s = _search(tmp_path, targets)
    await s.calibrate()
    for v in measured:
        await s.measure({"lr": v}, 1)
    t = s.targets[0]
    res = ClaimResult(target=t, status="searched", gap_before=s.gap(t, {}), band=s.band(t))
    await s._scale_probe(t, res)
    return s, res


async def test_a_percent_convention_on_a_log_scale(tmp_path):
    s, res = await _probe(tmp_path, ("0.001", "0.004", "0.02", "0.05"))
    assert any(x["knob"] == "lr" and x["c"] == 0.01 and x["verified"] for x in s.scale_relations), (
        s.scale_relations, res.notes)
    assert res.changes == {"lr": "0.0001"}, (res.changes, res.notes)
    assert res.attribution.confidence_label == "Paper-artifact inconsistency", res.notes


async def test_a_convention_beyond_the_measured_curve_is_run(tmp_path):
    # rates measured over about one decade: 0.01 x the paper's lies outside what the curve can say, so it is run
    s, res = await _probe(tmp_path, ("0.004", "0.02", "0.05"))
    assert any(x["knob"] == "lr" and x["c"] == 0.01 and x["verified"] for x in s.scale_relations), (
        s.scale_relations, res.notes)
    assert res.changes == {"lr": "0.0001"}, (res.changes, res.notes)
