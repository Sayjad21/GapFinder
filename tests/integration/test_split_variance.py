"""Split variance (Bouthillier et al.): with a split-seed knob, the naive run at other splits is measured and reported;
the noise band changes only with split_noise."""

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
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--split_seed", type=int, default=0)
    a = p.parse_args()
    seed_noise = int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 / 1e4
    split_effect = {0: 0.0, 1: 0.03, 2: -0.03}.get(a.split_seed, 0.0)  # the split moves the score far more
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.4f\\n" % (0.80 + seed_noise + split_effect))
    ''')


def _search(tmp_path, knob="split_seed", **cfg):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    (art / "main.py").write_text(BENCH, encoding="utf-8")
    sp = tmp_path / "spec.yaml"
    sp.write_text(textwrap.dedent(f"""\
        name: split-toy
        base: "local:{art.as_posix()}"
        run:
          command: '"${{PYTHON:-python3}}" main.py --lr {{lr}} --split_seed {{{knob}}}'
          output: out/run.log
          format: kv
          timeout: 30
        knobs:
          lr: {{layer: config, default: "0.01"}}
          {knob}: {{layer: config, default: "0"}}
        allowed_paths: ["out/"]
        metrics: [acc]
        """), encoding="utf-8")
    spec = HarnessSpec.load_yaml(sp)
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    return GapSearch(orch, [Target("C1", "acc", 0.80)], asm, SearchConfig(max_runs=30, trace=False, **cfg))


async def test_split_variance_is_reported_and_used_only_when_asked(tmp_path):
    s = _search(tmp_path / "a")
    await s.calibrate()
    r = s.split_report["C1"]
    assert r["seed_and_split_band"] > 3 * r["seed_band"]
    assert s.bands["acc"].band == r["seed_band"]  # reported only
    # measurements, not candidates: a lucky split must never become the explanation
    assert not any(dict(k).get("split_seed") not in (None, "0") for k in s._runs)
    s2 = _search(tmp_path / "b", split_noise=True)
    await s2.calibrate()
    assert s2.bands["acc"].band == s2.split_report["C1"]["seed_and_split_band"]


async def test_a_bare_split_knob_is_not_a_seed(tmp_path):
    s = _search(tmp_path / "c", knob="split")  # `--split 0`: a fraction or a mode as often as a seed
    await s.calibrate()
    assert s.split_report == {}
