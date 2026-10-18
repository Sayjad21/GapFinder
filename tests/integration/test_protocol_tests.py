"""Protocol tests: code that picks its result by the test score is run with the selection switched off, so the
report says how much the paper's number depends on it, as a measurement (no file is edited)."""

import textwrap

from gapfinder.ledger.schemas import Assumption
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target

BENCH = textwrap.dedent("""\
    import argparse, hashlib, os, random
    p = argparse.ArgumentParser()
    p.add_argument("--alpha", type=float, default=1.0)
    a = p.parse_args()
    random.seed(int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 10**6)
    test_data = list(range(100))

    def evaluate(data, epoch):
        return 60.0 + 2.0 * epoch * a.alpha if epoch < 5 else 70.0 - 3.0 * (epoch - 4) + random.random()

    best_acc, best_epoch = -1.0, 0
    for epoch in range(10):
        acc = evaluate(test_data, epoch)
        if acc > best_acc:
            best_acc, best_epoch = acc, epoch
    os.makedirs("out", exist_ok=True)
    with open("out/run.log", "w") as fh:
        fh.write("score=%.4f\\n" % best_acc)
    """)


async def test_selection_by_test_score_is_measured_with_the_selection_switched_off(tmp_path):
    art = tmp_path / "art"
    art.mkdir()
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    spec_path = tmp_path / "spec.yaml"
    spec_path.write_text(textwrap.dedent(f"""\
        name: protocol-toy
        base: "local:{art.as_posix()}"
        run:
          command: '"${{PYTHON:-python3}}" bench.py --alpha {{alpha}}'
          output: out/run.log
          format: kv
          timeout: 30
        knobs:
          alpha: {{layer: config, default: "1.0", candidates: ["1.2"]}}
        allowed_paths: ["out/"]
        metrics: [score]
        """), encoding="utf-8")
    spec = HarnessSpec.load_yaml(spec_path)
    spec.source = str(art)
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    a = Assumption(id="A1", knob="alpha", layer="config", paper_value="unstated", candidate_values=["1.2"],
                   evidence=[], prior_score=0.5, status="unstated")
    # the paper's number is the best-by-test epoch (70.x, epoch 4's score varies a little by seed): reproduced
    s = GapSearch(orch, [Target("C1", "score", 68.0)], [a], SearchConfig(max_runs=60, trace=False))
    [r] = await s.run()
    assert r.attribution is None  # reproduced
    [pt] = s.protocol_results
    assert pt["family"] == "selection_in_code" and pt["file"] == "bench.py" and pt["value"] == "True"
    [c] = pt["claims"]
    # with the selection switched off the script reports its last epoch: 70 - 15 + noise, about 55.5
    assert c["depends"] and c["without"] < 57 and c["naive"] > 66
    from gapfinder.report.gap_report import GapReport
    md = GapReport.from_search(s, [r], paper="toy").to_markdown()
    assert "Measured: the reported numbers depend on this code" in md and "bench.py:14" in md
