"""Plan F4: paired seeds (common random numbers) and adaptive repeats.

A new instance of the class the planted curriculum found (a real effect of a few standard deviations not confirmed
at 3 repeats): each run's noise comes from its seed (derived from RUN_TAG, as the harnesses do), and the planted
learning rate shifts every seed's result by the same amount. Unpaired, the candidate's effect interval includes 0
at 3 repeats; with the j-th run of every configuration on the same seed, the paired differences are the effect
itself, and the candidate is confirmed.

Both are kept behind their flags, off by default (SearchConfig.paired_seeds, adaptive_repeats: on 16 noise draws
per variant, pairing found the planted lr less often and once labelled a wrong answer confidently, and adaptive
repeats showed no gain); the tests check their mechanisms."""

import textwrap

from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec

SIGMA = 0.01
BENCH = textwrap.dedent(f'''\
    import argparse, hashlib, os
    p = argparse.ArgumentParser()
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--wd", type=float, default=0.0005)
    p.add_argument("--n", type=int, default=30)
    a = p.parse_args()
    h = int(hashlib.md5((os.environ.get("RUN_TAG", "") + "SALT").encode()).hexdigest(), 16)
    seed_noise = ((h % 1000) / 1000.0 - 0.5) * {SIGMA} * 3.4  # about sd {SIGMA}, from the seed
    effect = EFFECT if abs(a.lr - 0.02) < 1e-9 else 0.0
    m = 0.70 + effect + seed_noise + 0.001 * a.n / 30.0
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.6f\\n" % m)
    ''')


def _search(tmp_path, paired: bool, adaptive: int = 3, effect: float = 0.06, salt: str = ""):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    (art / "bench.py").write_text(BENCH.replace("EFFECT", repr(effect)).replace("SALT", salt), encoding="utf-8")
    knobs = {"lr": "0.01", "wd": "0.0005", "n": "30"}
    flags = " ".join(f"--{k} {{{k}}}" for k in knobs)
    ks = "\n".join(f'  {k}: {{layer: config, default: "{v}"' + (", condition: true" if k == "n" else "") + "}"
                   for k, v in knobs.items())  # n: the claims' condition, never screened as a cause
    (tmp_path / "s.yaml").write_text(
        f'name: paired\nbase: "local:{art.as_posix()}"\nrun:\n  command: \'"${{PYTHON:-python3}}" bench.py {flags}\'\n'
        f"  output: out/run.log\n  format: kv\n  timeout: 30\nknobs:\n{ks}\n"
        'allowed_paths: ["out/"]\nmetrics: [acc]\n', encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    paper = lambda n: 0.70 + effect + 0.001 * n / 30.0  # noqa: E731
    targets = [Target("C1", "acc", paper(30))] + [
        Target(f"N{n}", "acc", paper(n), held_out=True, at={"n": str(n)}) for n in (20, 44)]
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=150, trace=False, hm_disc=0.005, mutations=False, patch_knobs=False,
                                                      value_interval=False, paired_seeds=paired,
                                                      adaptive_repeats=adaptive))


async def test_the_runs_of_every_configuration_share_seeds_when_paired(tmp_path):
    """The mechanism: the j-th run of the naive configuration and of a candidate carry the same RUN_TAG."""
    s = _search(tmp_path, paired=True, adaptive=0)
    [r] = await s.run()
    tags = {}
    for e in s.orch.events.read():
        if e["type"] == "branch_created":
            tags.setdefault(frozenset(e["branch"]["knob_changes"].items()), []).append(e["branch"]["run_tag"])
    naive, cand = tags[frozenset()], tags.get(frozenset({"lr": "0.02"}.items()), [])
    assert cand and set(cand) <= set(naive) | {f"gf-crn-{j}" for j in range(20)}


async def test_adaptive_repeats_are_bounded_and_never_confident_on_noise(tmp_path):
    """An effect of 3 sd: at most adaptive_repeats extra runs per configuration, and no confident label."""
    s = _search(tmp_path, paired=False, adaptive=3, effect=0.03)
    [r] = await s.run()
    extra = {}
    for e in s.orch.events.read():
        if e["type"] == "branch_created" and "(adaptive)" in (e["branch"].get("note") or ""):
            k = frozenset(e["branch"]["knob_changes"].items())
            extra[k] = extra.get(k, 0) + 1
    assert all(v <= 3 for v in extra.values()), extra
    assert r.attribution.confidence_label not in ("Explained", "Paper-artifact inconsistency"), (r.changes, r.notes)
