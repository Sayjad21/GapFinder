"""Plan F7: group screening finds a code defect ranked below the mutants the mutation round tries one by one.

A new instance of the class the planted curriculum found (the planted site ranked 37th to 289th, 24 tried): twenty
statements on the knobs' data flow feed the metric only negligibly (their mutants rank first and move nothing), and
the defect is a loop bound in a helper (`range(10)` where the paper's numbers need `range(20)`), ranked low; claims
at two other list lengths. The first mutants move nothing; in groups, the loop bound's group moves the target, and
halving isolates it."""

import textwrap

from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec

HELPER = textwrap.dedent('''\
    def accumulate(xs):
        total = 0.0
        for i in range(10):
            total += xs[i % len(xs)] * 0.01
        return total
    ''')
# decoys on the knobs' data flow, and decoy loop bounds that add nothing (the mutation round takes its first mutants
# from each operator class in turn, so the planted loop bound is outranked within its own class)
DECOYS = "\n".join(f"    d{i} = a.a * {i + 2} + a.b / {i + 3} - a.c * {i + 1}\n"
                   f"    for _ in range({i + 2}):\n        d{i} += 0.0" for i in range(20))
BENCH = textwrap.dedent('''\
    import argparse, hashlib, os
    import helper
    p = argparse.ArgumentParser()
    p.add_argument("--a", type=float, default=1.0)
    p.add_argument("--b", type=float, default=1.0)
    p.add_argument("--c", type=float, default=1.0)
    p.add_argument("--n", type=int, default=30)
    a = p.parse_args()

    def main():
        DECOYS
        tiny = 1e-9 * (DSUM)
        noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 500000.0
        xs = [i / 10.0 for i in range(a.n)]
        score = 0.5 + helper.accumulate(xs) + 0.001 * a.n / 30.0 + tiny
        os.makedirs("out", exist_ok=True)
        open("out/run.log", "w").write("score=%.6f\\n" % (score + noise))

    main()
    ''').replace("    DECOYS", DECOYS).replace("DSUM", " + ".join(f"d{i}" for i in range(20)))


def _paper(n, bound=20):
    xs = [i / 10.0 for i in range(n)]
    return 0.5 + sum(xs[i % len(xs)] * 0.01 for i in range(bound)) + 0.001 * n / 30.0


def _search(tmp_path, group: bool):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    (art / "helper.py").write_text(HELPER, encoding="utf-8")
    knobs = {"a": "1.0", "b": "1.0", "c": "1.0", "n": "30"}
    flags = " ".join(f"--{k} {{{k}}}" for k in knobs)
    # n is the claims' condition (plan D2.1): set by the claims at fixed values, never screened as a cause
    ks = "\n".join(f'  {k}: {{layer: config, default: "{v}"' + (", condition: true" if k == "n" else "") + "}"
                   for k, v in knobs.items())
    (tmp_path / "s.yaml").write_text(
        f'name: group\nbase: "local:{art.as_posix()}"\nsource: "{art.as_posix()}"\nrun:\n'
        f'  command: \'"${{PYTHON:-python3}}" bench.py {flags}\'\n'
        f"  output: out/run.log\n  format: kv\n  timeout: 30\nknobs:\n{ks}\n"
        'allowed_paths: ["out/"]\nmetrics: [score]\n', encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    targets = [Target("C1", "score", _paper(30))] + [
        Target(f"N{n}", "score", _paper(n), held_out=True, at={"n": str(n)}) for n in (20, 44)]
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=200, trace=False, hm_disc=0.005, patch_knobs=False,
                                                      value_interval=False, group_screen=group))


def _found(r):
    return any("@mut." in k and "helper.py:3" in k for k in r.changes) or any(
        "helper.py:3" in n and "code change" in n for n in r.notes)


async def test_the_loop_bound_is_isolated_by_group_screening(tmp_path):
    s = _search(tmp_path, group=True)
    [r] = await s.run()
    assert _found(r), (r.changes, r.notes)


async def test_one_by_one_it_is_never_tried(tmp_path):
    s = _search(tmp_path, group=False)
    [r] = await s.run()
    assert not _found(r), (r.changes, r.notes)
