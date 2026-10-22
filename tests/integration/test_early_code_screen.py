"""Plan F2: when no screened setting fits every claim, the code rounds' first tests run before confirmation and
combining spend the budget on settings.

A new instance of the class the planted curriculum found (out of space, the mutation round left with no room):
twelve settings that each move the metric a little, and a metric helper that halves what is printed where the
paper's numbers don't; claims at two other list lengths. With the early screen the mutation round's first mutants
(the output slice first, plan F1) run right after the screen, and the halving is found; without it, the mutation
round has no room. A module literal is a second case: found either way (the out-of-space patch reserve), and the
early screen must not lose it."""

import textwrap

from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec

KNOBS = {f"w{i}": "1.0" for i in range(12)} | {"n": "30"}
CONFIG = "TEMPERATURE = 0.5\n"
BENCH = textwrap.dedent('''\
    import argparse, hashlib, os
    import config
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=30)
    for i in range(12):
        p.add_argument("--w%d" % i, type=float, default=1.0)
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 200000.0
    vals = [((i * 7) % 11) / 10.0 for i in range(a.n)]
    nudge = sum(0.002 * (getattr(a, "w%d" % i) - 1.0) / (1.0 + abs(getattr(a, "w%d" % i) - 1.0)) for i in range(12))
    s = (sum(vals) / a.n) * (0.1 / config.TEMPERATURE) * (1.0 + nudge)
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("mean_score=%.6f\\n" % (s + noise))
    ''')


def _paper(n, temperature=0.25):
    vals = [((i * 7) % 11) / 10.0 for i in range(n)]
    return (sum(vals) / n) * (0.1 / temperature)


METRICS = "def score_per_item(total, n):\n    return total / n / 2\n"
BENCH_MUT = BENCH.replace("import config", "import metrics").replace(
    "s = (sum(vals) / a.n) * (0.1 / config.TEMPERATURE) * (1.0 + nudge)",
    "s = metrics.score_per_item(sum(vals), a.n) * (1.0 + nudge)").replace(
    'open("out/run.log", "w").write("mean_score=%.6f\\n" % (s + noise))',
    'print("mean_score: %.6f" % (s + noise))\nopen("out/run.log", "w").write("mean_score=%.6f\\n" % (s + noise))')


def _search(tmp_path, early: bool, max_runs: int = 150, case: str = "literal"):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    if case == "literal":
        (art / "bench.py").write_text(BENCH, encoding="utf-8")
        (art / "config.py").write_text(CONFIG, encoding="utf-8")
    else:
        (art / "bench.py").write_text(BENCH_MUT, encoding="utf-8")
        (art / "metrics.py").write_text(METRICS, encoding="utf-8")
    flags = " ".join(f"--{k} {{{k}}}" for k in KNOBS)
    ks = "\n".join(f'  {k}: {{layer: config, default: "{v}"}}' for k, v in KNOBS.items())
    (tmp_path / "s.yaml").write_text(
        f'name: early\nbase: "local:{art.as_posix()}"\nrun:\n  command: \'"${{PYTHON:-python3}}" bench.py {flags}\'\n'
        f"  output: out/run.log\n  format: kv\n  timeout: 30\nknobs:\n{ks}\n"
        'allowed_paths: ["out/"]\nmetrics: [mean_score]\n', encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    paper = _paper if case == "literal" else (lambda n: _paper(n, 0.1))  # the mean: the halving undone
    targets = [Target("C1", "mean_score", paper(30))] + [
        Target(f"N{n}", "mean_score", paper(n), held_out=True, at={"n": str(n)}) for n in (20, 44)]
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=max_runs, trace=False, hm_disc=0.005,
                                                      mutations=case != "literal", patch_knobs=case == "literal",
                                                      early_code_screen=early, value_interval=False,
                                                      class_scheduler=False))  # the early screen's own effect


def _found(r):
    return any(k.endswith(":TEMPERATURE") and abs(float(v) - 0.25) < 1e-9 for k, v in r.changes.items())


async def test_the_code_defect_is_screened_early_and_found(tmp_path):
    s = _search(tmp_path, early=True, case="mutant")
    [r] = await s.run()
    assert any("@mut." in k for k in r.changes), (r.changes, r.notes)
    assert s.runs_used <= 150


async def test_without_the_early_screen_the_mutation_round_has_no_room(tmp_path):
    s = _search(tmp_path, early=False, case="mutant")
    [r] = await s.run()
    assert not any("@mut." in k for k in r.changes), (r.changes, r.notes)
    assert any("mutation round: no room left" in n for n in r.notes), r.notes


async def test_the_literal_is_still_found_with_the_early_screen(tmp_path):
    s = _search(tmp_path, early=True, max_runs=80)
    [r] = await s.run()
    assert _found(r), (r.changes, r.notes)
