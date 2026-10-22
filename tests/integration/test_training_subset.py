"""Plan G5: the paper's numbers came from part of the training data (DeepCrime's TRD, a fault class from real
deep-learning bugs). A new instance: the training rows are a list the loader returns; the paper used half of them.
A learning rate can match the accuracy but not the loss, so no setting fits both claims; the training subset does."""

import textwrap

from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec

DATA = textwrap.dedent('''\
    def load(n=600):
        train_rows = [i for i in range(n)]
        return train_rows
    ''')
BENCH = textwrap.dedent('''\
    import argparse, hashlib, math, os
    import data
    p = argparse.ArgumentParser()
    p.add_argument("--lr", type=float, default=0.01)
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 1000000.0
    rows = data.load()
    n = len(rows)
    acc = 0.9 - 3 / math.sqrt(n) - 0.05 * abs(math.log10(a.lr / 0.01))
    loss = 1 / math.sqrt(n)
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.6f\\nloss=%.6f\\n" % (acc + noise, loss + noise))
    ''')


async def test_half_the_training_rows(tmp_path):
    import math

    art = tmp_path / "art"
    art.mkdir(parents=True)
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    (art / "data.py").write_text(DATA, encoding="utf-8")
    (tmp_path / "s.yaml").write_text(textwrap.dedent(f"""\
        name: subset
        base: "local:{art.as_posix()}"
        run:
          command: '"${{PYTHON:-python3}}" bench.py --lr {{lr}}'
          output: out/run.log
          format: kv
          timeout: 30
        knobs:
          lr: {{layer: config, default: "0.01"}}
        allowed_paths: ["out/"]
        metrics: [acc, loss]
        """), encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    targets = [Target("C1", "acc", 0.9 - 3 / math.sqrt(300)), Target("C2", "loss", 1 / math.sqrt(300), held_out=True)]
    s = GapSearch(orch, targets, asm, SearchConfig(max_runs=150, trace=False, hm_disc=0.005, patch_knobs=False,
                                                   value_interval=False))
    [r] = await s.run()
    assert any(k.startswith("@ast:data.py:2:@mut.") for k in r.changes), (r.changes, r.notes)
    assert r.attribution.confidence_label not in ("Explained", "Paper-artifact inconsistency"), r.notes
