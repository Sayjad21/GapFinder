"""Alternative settings the repo keeps (a commented-out argparse block) are tested as one configuration: their
settings may only work together (batch-4 RippleNet: lr 1e-3 and l2_weight 1e-5, from a block "default settings for
Book-Crossing"; l2_weight alone did nothing, so pairs of single leads never tried it)."""

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
    p.add_argument("--lr", type=float, default=0.02, help="learning rate")
    p.add_argument("--l2", type=float, default=1e-7, help="weight of the l2 regularization term")
    p.add_argument("--hops", type=int, default=2, help="maximum hops")
    """
    # default settings for the other dataset
    p.add_argument("--lr", type=float, default=1e-3, help="learning rate")
    p.add_argument("--l2", type=float, default=1e-5, help="weight of the l2 regularization term")
    """
    a = p.parse_args()
    noise = int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 / 2e4
    # a low learning rate helps a little alone; the block's exact pair is what the 'paper' ran
    score = 0.65 + (0.02 if a.lr < 0.005 else 0) + (0.06 if 8e-4 < a.lr < 1.2e-3 and 8e-6 < a.l2 < 1.2e-5 else 0) + noise
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("auc=%.4f\\nacc=%.4f\\n" % (score, score - 0.07))
    ''')


async def test_a_commented_out_settings_block_is_tested_as_one_configuration(tmp_path):
    art = tmp_path / "art"
    art.mkdir()
    (art / "main.py").write_text(BENCH, encoding="utf-8")
    spec_path = tmp_path / "spec.yaml"
    spec_path.write_text(textwrap.dedent(f"""\
        name: alt-toy
        base: "local:{art.as_posix()}"
        run:
          command: '"${{PYTHON:-python3}}" main.py --lr {{lr}} --l2 {{l2}} --hops {{hops}}'
          output: out/run.log
          format: kv
          timeout: 30
        knobs:
          lr: {{layer: config, default: "0.02"}}
          l2: {{layer: config, default: "1e-7"}}
          hops: {{layer: config, default: "2", max: 4}}
        allowed_paths: ["out/"]
        metrics: [auc, acc]
        """), encoding="utf-8")
    spec = HarnessSpec.load_yaml(spec_path)
    spec.source = str(art)
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    s = GapSearch(orch, [Target("C1", "auc", 0.73), Target("C2", "acc", 0.66, held_out=True)], asm,
                  SearchConfig(max_runs=150, trace=False))
    assert s._alternative_configs() == [{"lr": "1e-3", "l2": "1e-5"}]
    [r] = await s.run()
    assert {k: float(v) for k, v in r.changes.items()} == {"lr": 1e-3, "l2": 1e-5}, (r.changes, r.notes)
