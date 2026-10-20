"""Plan D4.4: the engine links a ledger name that is not a knob by retrieval, with no model, and the paper's stated
value under that name then explains the gap (a new toy)."""

import textwrap

from gapfinder.ledger.schemas import Assumption, Evidence
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target

BENCH = textwrap.dedent('''\
    import argparse, hashlib, os
    p = argparse.ArgumentParser()
    p.add_argument("--l2_coef", type=float, default=0.0005, help="Weight for L2 loss on the parameters.")
    p.add_argument("--hid_units", type=int, default=8, help="number of hidden units per head")
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 5000.0
    acc = 80.0 - 4000 * abs(a.l2_coef - 0.001) + 0.1 * (a.hid_units == 8)
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.4f\\n" % (acc + noise))
    ''')


async def test_a_ledger_name_linked_without_a_model(tmp_path):
    art = tmp_path / "art"
    art.mkdir()
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    (tmp_path / "s.yaml").write_text(textwrap.dedent(f"""\
        name: links
        base: "local:{art.as_posix()}"
        run:
          command: '"${{PYTHON:-python3}}" bench.py --l2_coef {{l2_coef}} --hid_units {{hid_units}}'
          output: out/run.log
          format: kv
          timeout: 30
        knobs:
          l2_coef: {{layer: config, default: "0.0005"}}
          hid_units: {{layer: config, default: "8"}}
        allowed_paths: ["out/"]
        metrics: [acc]
        """), encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm = [Assumption(id="A1", knob="l2_reg_lambda", layer="config", paper_value="0.001", code_default="0.0005",
                      candidate_values=["0.001"], prior_score=0.8, status="stated_code_differs",
                      evidence=[Evidence(kind="paper", ref="p.5", quote="we apply L2 regularization with lambda = 0.001")])]
    s = GapSearch(orch, [Target("C1", "acc", 80.0)], asm,
                  SearchConfig(max_runs=80, trace=False, hm_disc=0.005, patch_knobs=False, mutations=False,
                               library_probe=False))
    assert s.router is None  # no model at all
    [r] = await s.run()
    assert s.renamed == {"l2_reg_lambda": "l2_coef"}
    assert r.changes == {"l2_coef": "0.001"}, (r.changes, r.notes)
    assert r.attribution.confidence_label in ("Explained", "Paper-artifact inconsistency")
