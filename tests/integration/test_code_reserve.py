"""code_hold: the code rounds keep their share of the run budget when many settings could use it all.

A new instance of the class the planted curriculum c1 found (a code round cut by the budget the settings search had
spent): twelve settings that each move the metric a little, and a metric helper that halves its result where the
paper's numbers don't, with claims at two other list lengths. No setting fits every claim. With the reserve, the
mutation round runs and a doubling edit is the code lead (the first found is upstream, `/ 10.0` -> `/ 5.0` on the
values, which no run can tell from removing the halving); without it, the settings leave the round no room."""

import textwrap

import pytest

from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec


@pytest.fixture(autouse=True)
def _no_scale_hold(monkeypatch):
    """These toys measure how the settings and code rounds split the budget. Their claims sweep a knob, so since c7
    the scale probe's hold (plan H4; c5 counted it in the wrong list, so always 0) keeps runs that, unused, reach the
    code rounds in both arms. It is held at 0 here, so each comparison stays the feature's own."""
    monkeypatch.setattr(GapSearch, "_scale_hold", lambda self: 0)

KNOBS = {f"w{i}": "1.0" for i in range(12)} | {"n": "30"}
METRICS = textwrap.dedent('''\
    def score_per_item(total, n):
        return total / n / 2
    ''')
BENCH = textwrap.dedent('''\
    import argparse, hashlib, os
    import metrics
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=30)
    for i in range(12):
        p.add_argument("--w%d" % i, type=float, default=1.0)
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 200000.0
    vals = [((i * 7) % 11) / 10.0 for i in range(a.n)]
    nudge = sum(0.002 * (getattr(a, "w%d" % i) - 1.0) / (1.0 + abs(getattr(a, "w%d" % i) - 1.0)) for i in range(12))
    s = metrics.score_per_item(sum(vals), a.n) * (1.0 + nudge)
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("mean_score=%.6f\\n" % (s + noise))
    ''')


def _paper(n):
    vals = [((i * 7) % 11) / 10.0 for i in range(n)]
    return sum(vals) / n  # the paper's helper doesn't halve


def _search(tmp_path, reserve: bool):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    (art / "metrics.py").write_text(METRICS, encoding="utf-8")
    flags = " ".join(f"--{k} {{{k}}}" for k in KNOBS)
    ks = "\n".join(f'  {k}: {{layer: config, default: "{v}"}}' for k, v in KNOBS.items())
    (tmp_path / "s.yaml").write_text(
        f'name: reserve\nbase: "local:{art.as_posix()}"\nrun:\n  command: \'"${{PYTHON:-python3}}" bench.py {flags}\'\n'
        f"  output: out/run.log\n  format: kv\n  timeout: 30\nknobs:\n{ks}\n"
        'allowed_paths: ["out/"]\nmetrics: [mean_score]\n', encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    targets = [Target("C1", "mean_score", _paper(30))] + [
        Target(f"N{n}", "mean_score", _paper(n), held_out=True, at={"n": str(n)}) for n in (20, 44)]
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=150, trace=False, hm_disc=0.005, patch_knobs=False,
                                                      code_hold=reserve, early_code_screen=False,
                                                      value_interval=False, class_scheduler=False))  # its own effect


async def test_the_mutation_round_keeps_its_share(tmp_path):
    s = _search(tmp_path, reserve=True)
    [r] = await s.run()
    assert any("@mut." in k for k in r.changes), (r.changes, r.notes)
    assert s.runs_used <= 150
    assert not any("no room left" in n for n in r.notes), r.notes


async def test_without_the_reserve_the_settings_take_the_budget(tmp_path):
    s = _search(tmp_path, reserve=False)
    [r] = await s.run()
    assert not any("@mut." in k for k in r.changes), (r.changes, r.notes)
    assert any("mutation round: no room left" in n for n in r.notes), r.notes
