"""Plan F8: the code rounds' share of the budget follows the evidence after the screen.

Two new instances: (a) twelve weak settings and a metric helper that halves what is printed (no setting comes
near: P(a setting explains) is low, so runs are kept for the code rounds, and the mutation round finds the halving
with the early code screen off); (b) a learning rate that alone explains every claim (P near 1: nothing is held)."""

import textwrap

import test_code_reserve as cr

from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec

LR_BENCH = textwrap.dedent('''\
    import argparse, hashlib, os
    p = argparse.ArgumentParser()
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--wd", type=float, default=0.0005)
    p.add_argument("--n", type=int, default=30)
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 500000.0
    m = 0.70 + (0.06 if abs(a.lr - 0.02) < 1e-9 else 0.0) + 0.001 * a.n / 30.0
    print("acc: %.6f" % (m + noise))
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.6f\\n" % (m + noise))
    ''')


def _code_search(tmp_path, scheduler: bool):
    s = cr._search(tmp_path, reserve=False)
    s.cfg.class_scheduler = scheduler
    return s


def _lr_search(tmp_path):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    (art / "bench.py").write_text(LR_BENCH, encoding="utf-8")
    knobs = {"lr": "0.01", "wd": "0.0005", "n": "30"}
    flags = " ".join(f"--{k} {{{k}}}" for k in knobs)
    ks = "\n".join(f'  {k}: {{layer: config, default: "{v}"' + (", condition: true" if k == "n" else "") + "}"
                   for k, v in knobs.items())
    (tmp_path / "s.yaml").write_text(
        f'name: sched\nbase: "local:{art.as_posix()}"\nsource: "{art.as_posix()}"\nrun:\n'
        f'  command: \'"${{PYTHON:-python3}}" bench.py {flags}\'\n'
        f"  output: out/run.log\n  format: kv\n  timeout: 30\nknobs:\n{ks}\n"
        'allowed_paths: ["out/"]\nmetrics: [acc]\n', encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    paper = lambda n: 0.76 + 0.001 * n / 30.0  # noqa: E731
    targets = [Target("C1", "acc", paper(30))] + [
        Target(f"N{n}", "acc", paper(n), held_out=True, at={"n": str(n)}) for n in (20, 44)]
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=150, trace=False, hm_disc=0.005, patch_knobs=False,
                                                      value_interval=False, early_code_screen=False))


def _held(s):
    return [e["msg"] for e in s.orch.events.read() if e.get("type") == "note" and "class scheduler" in e.get("msg", "")]


async def test_no_setting_near_keeps_runs_for_the_code_rounds(tmp_path):
    s = _code_search(tmp_path, scheduler=True)
    [r] = await s.run()
    assert _held(s), r.notes
    assert any("@mut." in k for k in r.changes), (r.changes, r.notes)


async def test_without_the_scheduler_the_mutation_round_has_no_room(tmp_path):
    s = _code_search(tmp_path, scheduler=False)
    [r] = await s.run()
    assert not any("@mut." in k for k in r.changes), (r.changes, r.notes)


async def test_a_setting_that_fits_takes_nothing_from_the_settings(tmp_path):
    s = _lr_search(tmp_path)
    [r] = await s.run()
    assert r.changes.get("lr") == "0.02", (r.changes, r.notes)
    held = [int(m.split("; ")[1].split()[0]) for m in _held(s)]
    assert all(h <= 2 for h in held), held  # P(a setting explains) near 1
