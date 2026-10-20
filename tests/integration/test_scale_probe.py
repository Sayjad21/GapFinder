"""Plan D2.4: claims that sweep a knob whose unit or convention differs between the paper and the code.

New instances of the class (not batch-5's case): a window the code counts in half-steps (the paper's w is the code's
w/2, an integer knob), and layers the code counts from the input (the paper's L is the code's L + 1). A negative
control: a sweep where the code matches the paper except for an unrelated shift."""

import textwrap

from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec

BENCH = textwrap.dedent('''\
    import argparse, hashlib, os
    p = argparse.ArgumentParser()
    p.add_argument("--window", type=int, default=8)
    p.add_argument("--layers", type=int, default=3)
    p.add_argument("--lr", type=float, default=0.01)
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 50000.0
    acc = 0.95 - (0.015 if a.lr == 0.1 else 0.02) * a.window + 0.03 * a.layers - 0.09
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.5f\\n" % (100 * (acc + noise)))
    ''')


def _code_acc(window=8, layers=3, lr=0.01):
    return 100 * (0.95 - (0.015 if lr == 0.1 else 0.02) * window + 0.03 * layers - 0.09)


def _search(tmp_path, targets):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    (tmp_path / "s.yaml").write_text(textwrap.dedent(f"""\
        name: scale
        base: "local:{art.as_posix()}"
        run:
          command: '"${{PYTHON:-python3}}" bench.py --window {{window}} --layers {{layers}} --lr {{lr}}'
          output: out/run.log
          format: kv
          timeout: 30
        knobs:
          window: {{layer: config, default: "8"}}
          layers: {{layer: config, default: "3"}}
          lr: {{layer: config, default: "0.01"}}
        allowed_paths: ["out/"]
        metrics: [acc]
        """), encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=120, trace=False, hm_disc=0.005, patch_knobs=False))


async def test_a_knob_counted_in_half_steps(tmp_path):
    # the paper's window w is the code's w / 2: the paper's numbers are the code's at 4, 2, 6, 8
    targets = [Target("C1", "acc", _code_acc(window=4))] + [
        Target(f"P{w}", "acc", _code_acc(window=w // 2), held_out=True, at={"window": str(w)}) for w in (4, 12, 16)]
    s = _search(tmp_path, targets)
    [r] = await s.run()
    assert r.attribution.confidence_label == "Paper-artifact inconsistency", r.notes
    assert r.changes == {"window": "4"} and any("0.5 x the paper's" in n for n in r.notes), r.notes
    assert any(x["knob"] == "window" and x["c"] == 0.5 and x["verified"] for x in s.scale_relations)


async def test_layers_counted_from_the_input(tmp_path):
    # the paper's L is the code's L + 1
    targets = [Target("C1", "acc", _code_acc(layers=4))] + [
        Target(f"P{L}", "acc", _code_acc(layers=L + 1), held_out=True, at={"layers": str(L)}) for L in (1, 2, 5)]
    s = _search(tmp_path, targets)
    [r] = await s.run()
    assert r.attribution.confidence_label == "Paper-artifact inconsistency", r.notes
    assert r.changes == {"layers": "4"} and any("the paper's +1" in n for n in r.notes), r.notes


async def test_a_sweep_that_matches_except_a_setting_is_not_a_scale(tmp_path):
    # the paper's numbers are the code's sweep with lr = 0.1, which changes the slope over window (a constant shift
    # would be indistinguishable from a window off by one on these claims)
    targets = [Target("C1", "acc", _code_acc(lr=0.1))] + [
        Target(f"P{w}", "acc", _code_acc(window=w, lr=0.1), held_out=True, at={"window": str(w)}) for w in (4, 12, 16)]
    s = _search(tmp_path, targets)
    [r] = await s.run()
    assert not any(x.get("verified") for x in s.scale_relations), s.scale_relations
    assert r.changes == {"lr": "0.1"}, (r.changes, r.notes)
