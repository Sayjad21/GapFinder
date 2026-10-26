"""Plan D7.7: multi-fidelity screening on a new toy. Decoys hurt from the first epoch; the true cause (a schedule)
helps only after epoch 14 of 20. Screened with a time cut at a quarter of the run, the decoys are behind the as-run
curve and dropped; the late cause is level with it there, is run in full, and is found. Screening takes less time."""

import statistics
import textwrap

from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec

BENCH = textwrap.dedent('''\
    import argparse, hashlib, os, sys, time
    p = argparse.ArgumentParser()
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--wd", type=float, default=0.0005)
    p.add_argument("--sched", default="none", choices=["none", "late"])
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 50000.0
    pen = (0 if abs(a.lr - 0.01) < 1e-12 else 2) + (0 if abs(a.wd - 0.0005) < 1e-12 else 2)
    acc = None
    for e in range(1, 21):
        time.sleep(0.3)
        acc = 60 + 0.5 * e - pen + (3 if a.sched == "late" and e >= 14 else 0) + noise
        print("acc__x_e%d=%.4f" % (e, acc))
        sys.stdout.flush()
    print("acc=%.4f" % acc)
    ''')


async def test_late_effects_survive_and_early_losers_are_cut(tmp_path):
    art = tmp_path / "art"
    art.mkdir()
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    (tmp_path / "s.yaml").write_text(textwrap.dedent(f"""\
        name: mf
        base: "local:{art.as_posix()}"
        run:
          command: 'timeout ${{GF_TIME_CUT:-0}} "${{PYTHON:-python3}}" bench.py --lr {{lr}} --wd {{wd}} --sched {{sched}}; true'
          output: stdout
          format: kv
          timeout: 60
          time_cut: true
        knobs:
          lr: {{layer: config, default: "0.01"}}
          wd: {{layer: config, default: "0.0005"}}
          sched: {{layer: config, default: "none", choices: ["none", "late"]}}
        allowed_paths: ["out/"]
        metrics: [acc]
        """), encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    cfg = SearchConfig(max_runs=120, trace=False, hm_disc=0.005, patch_knobs=False, mutations=False,
                       library_probe=False, mf_min_seconds=1.0, mf_full_bracket=0.1, mf_fraction=0.45)
    s = GapSearch(orch, [Target("C1", "acc", 73.0)], asm, cfg)
    [r] = await s.run()
    assert r.changes == {"sched": "late"}, (r.changes, r.notes)
    dropped = {(h.knob, h.value) for h in s.mf_dropped}
    assert len(dropped) >= 3 and all(k in ("lr", "wd") for k, _ in dropped), dropped  # decoys only, never the late cause
    cut = s.mf_runs
    full = [b for runs in s._runs.values() for b in runs if (b.note or "").startswith("screen ")]
    # the cut runs stopped early: fewer epochs than any full run, and faster in the median. A wall-clock ratio per run
    # (each cut under 0.6 of the slowest full run) held on a desktop and failed on a CI runner, whose fixed cost per
    # run is a larger share of a 2 s cut
    assert cut and max(len(s._series(b, "acc")) for b in cut) < min(len(s._series(x, "acc")) for x in full)
    assert statistics.median(b.resources.elapsed_s for b in cut) < statistics.median(x.resources.elapsed_s for x in full)
