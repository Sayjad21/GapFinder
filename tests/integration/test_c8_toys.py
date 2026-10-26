"""c8 (I, J, L): three ways a search lost its budget or its lead, on new toy instances.

(I) A configuration that fails with no sign of the environment at fault is not run again: the same values crash
again, and each retry is a run the search doesn't have (PatchTST: 27 of 100 runs).
(J) A literal written `30.` or `.5` gets patch values (the ladder didn't parse it, so a lead had none).
(L) A literal difference the contrast names without the paper's number gets it from one short second call."""

import textwrap

from gapfinder.ledger.schemas import BranchStatus
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec, patch_values

BENCH = textwrap.dedent('''\
    import argparse, os
    p = argparse.ArgumentParser()
    p.add_argument("--heads", type=int, default=4)
    x = p.parse_args()
    if 64 % x.heads:
        raise SystemExit("heads must divide the width")
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.5f\\n" % (80 + x.heads / 100))
    ''')


def _search(tmp_path):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    (tmp_path / "s.yaml").write_text(textwrap.dedent(f"""\
        name: c8
        base: "local:{art.as_posix()}"
        run:
          command: '"${{PYTHON:-python3}}" bench.py --heads {{heads}}'
          output: out/run.log
          format: kv
          timeout: 30
        knobs:
          heads: {{layer: config, default: "4"}}
        allowed_paths: ["out/"]
        metrics: [acc]
        """), encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    return GapSearch(orch, [Target("C1", "acc", 81.0)], assumptions_from_spec(spec)[0],
                     SearchConfig(max_runs=40, trace=False))


async def test_i_a_configuration_that_crashes_is_not_run_again(tmp_path):
    s = _search(tmp_path)
    await s.measure({"heads": "12"}, 1, "screen")
    await s.measure({"heads": "12"}, 3, "confirm")  # c7: a second run of the same crash
    runs = s._runs[frozenset({"heads": "12"}.items())]
    assert len(runs) == 1 and runs[0].status != BranchStatus.succeeded
    assert len(await s.measure({"heads": "8"}, 3, "confirm")) == 3  # a configuration that runs gets its repeats


def test_j_a_trailing_dot_literal_gets_patch_values():
    assert patch_values("test_percent", "30.")[:3] == patch_values("test_percent", "30.0")[:3] != []
    assert "0.25" in patch_values("p", ".5")


async def test_l_a_missing_paper_value_is_asked_for():
    from gapfinder.search.contrast import Difference, Differences, PaperValue, PaperValues, contrast

    calls = []

    class FakeRouter:
        async def structured(self, model, messages, schema):
            calls.append(schema.__name__)
            if schema is Differences:
                return Differences(differences=[
                    Difference(file="prep.py", line=3, paper_says="test sets contain 10% of links",
                               code_does="test_percent = 30.", kind="literal", name="test_percent")])
            return PaperValues(values=[PaperValue(name="test_percent", paper_value="10")])

    diffs = await contrast(FakeRouter(), "The test sets contain 10% of links.", [], [])
    assert calls == ["Differences", "PaperValues"] and diffs[0].paper_value == "10"


async def test_m_the_value_interval_keeps_its_runs_until_it_runs(tmp_path):
    # (M) the stages before a claim's value interval leave its runs: a measurement that would take them is refused
    import pytest
    from gapfinder.search.engine import RunBudgetExceeded

    s = _search(tmp_path)
    s.cfg.max_runs = 10
    s._interval_reserve = 2 * s.cfg.interval_steps  # as explain() sets it
    await s.measure({"heads": "8"}, 4, "confirm")
    with pytest.raises(RunBudgetExceeded):
        await s.measure({"heads": "16"}, 1, "confirm")  # 4 used, 6 held: nothing left for other stages
    assert len(await s.measure({"heads": "16"}, 1, "interval heads=16")) == 1  # the interval may use them
