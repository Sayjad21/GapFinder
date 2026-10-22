"""Plan F3: the answer's value as an interval, and every choice of a categorical knob of the answer.

New instances of the class the planted curriculum found (the right knob at a value off the candidate grid read as
another answer): a width whose effect is flat near the paper's value 23, which no ladder rung hits; a mode knob
whose two choices give the same numbers, the paper's being the one the screen didn't pick first."""

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
    p.add_argument("--width", type=int, default=10)
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--mode", default="plain", choices=["plain", "fast", "slow", "fast_tuned"])
    p.add_argument("--n", type=int, default=30)
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 500000.0
    m = 1.0 / (1.0 + a.width / 200.0)
    m *= {"plain": 1.0, "fast": 1.06, "slow": 0.97, "fast_tuned": 1.06}[a.mode]
    m *= 1.0 + 0.001 * a.n / 30.0
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("score=%.6f\\n" % (m + noise))
    ''')


def _m(width=10, mode="plain", n=30):
    return 1.0 / (1.0 + width / 200.0) * {"plain": 1.0, "fast": 1.06, "slow": 0.97, "fast_tuned": 1.06}[mode] * (
        1.0 + 0.001 * n / 30.0)


def _search(tmp_path, paper: dict, interval: bool = True):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    knobs = {"width": "10", "lr": "0.01", "mode": "plain", "n": "30"}
    flags = " ".join(f"--{k} {{{k}}}" for k in knobs)
    ks = "\n".join(f'  {k}: {{layer: config, default: "{v}"' + (', choices: [plain, fast, slow, fast_tuned]'
                                                                 if k == "mode" else "") + "}" for k, v in knobs.items())
    (tmp_path / "s.yaml").write_text(
        f'name: interval\nbase: "local:{art.as_posix()}"\nrun:\n  command: \'"${{PYTHON:-python3}}" bench.py {flags}\'\n'
        f"  output: out/run.log\n  format: kv\n  timeout: 30\nknobs:\n{ks}\n"
        'allowed_paths: ["out/"]\nmetrics: [score]\n', encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    targets = [Target("C1", "score", _m(**paper))] + [
        Target(f"N{n}", "score", _m(**paper, n=n), held_out=True, at={"n": str(n)}) for n in (20, 44)]
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=150, trace=False, hm_disc=0.005, mutations=False,
                                                      patch_knobs=False, value_interval=interval))


async def test_an_off_grid_value_lies_in_the_reported_interval(tmp_path):
    s = _search(tmp_path, {"width": 23})
    [r] = await s.run()
    assert "width" in r.changes, (r.changes, r.notes)
    lo, hi = r.value_intervals["width"]
    assert float(lo.lstrip("<>")) <= 23 <= float(hi.lstrip("<>")), (lo, hi, r.changes)
    assert float(hi.lstrip("<>")) / float(lo.lstrip("<>")) < 2.5  # narrower than the ladder's steps
    assert any("fit every claim (a bisection" in n for n in r.notes)


async def test_every_choice_of_the_answers_categorical_knob_is_run(tmp_path):
    s = _search(tmp_path, {"mode": "fast_tuned"})
    [r] = await s.run()
    assert r.changes.get("mode") in ("fast", "fast_tuned"), (r.changes, r.notes)
    assert {"fast", "fast_tuned"} <= set(r.value_sets.get("mode", [])), (r.value_sets, r.notes)
