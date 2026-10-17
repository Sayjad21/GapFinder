"""Patch knobs end to end: an out-of-space cause (a literal in an imported module) is found and verified
without editing any file."""

import os
import subprocess
import sys
from pathlib import Path

from gapfinder.ledger.schemas import Assumption
from gapfinder.sandbox import ast_patch
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "eval" / "toy" / "patch_knob"
SPEC = ROOT / "eval" / "toy" / "patch_knob.yaml"


def _paper(tmp_path) -> dict[str, float]:
    """The 'paper': the toy run with model.py's lengthscale at 0.1 instead of 0.01 (through the hook)."""
    env, files, _ = ast_patch.run_parts({ast_patch.knob_name("model.py", 2, "lengthscale"): "0.1"})
    hook = tmp_path / ast_patch.HOOK_DIR
    hook.mkdir()
    (hook / "sitecustomize.py").write_bytes(files[f"{ast_patch.HOOK_DIR}/sitecustomize.py"])
    work = tmp_path / "paper"
    work.mkdir()
    subprocess.run([sys.executable, str(ART / "bench.py")], cwd=work, check=True,
                   env={**os.environ, **env, "PYTHONPATH": f"{hook}{os.pathsep}{ART}"})
    return {k: float(v) for k, v in (line.split("=") for line in (work / "out" / "run.log").read_text().split())}


async def test_an_out_of_space_literal_is_found_as_a_patch_knob(tmp_path):
    before = (ART / "model.py").read_bytes()
    paper = _paper(tmp_path)
    assert paper == {"score": 200.0, "aux": 150.0}
    spec = HarnessSpec.load_yaml(SPEC)
    spec.source = str(ART)  # the code to read leads from (a local base is used anyway)
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    targets = [Target("C1", "score", paper["score"]), Target("C2", "aux", paper["aux"], held_out=True)]
    a = Assumption(id="A1", knob="alpha", layer="config", paper_value="unstated", candidate_values=["2.0"],
                   evidence=[], prior_score=0.5, status="unstated")
    s = GapSearch(orch, targets, [a], SearchConfig(max_runs=120))
    [r] = await s.run()
    knob = ast_patch.knob_name("model.py", 2, "lengthscale")
    assert r.changes == {knob: "0.1"}, (r.changes, r.notes)
    assert r.attribution.confidence_label in ("Fits but unsupported", "Partially explained", "Explained")
    assert any("explained with a code patch" in n and "lengthscale = 0.01 -> 0.1" in n for n in r.notes)
    assert (ART / "model.py").read_bytes() == before  # nothing on disk changed


async def test_the_patch_round_keeps_its_budget_share_when_runs_are_tight(tmp_path):
    paper = _paper(tmp_path)
    spec = HarnessSpec.load_yaml(SPEC)
    spec.source = str(ART)
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    targets = [Target("C1", "score", paper["score"]), Target("C2", "aux", paper["aux"], held_out=True)]
    a = Assumption(id="A1", knob="alpha", layer="config", paper_value="unstated", candidate_values=["2.0"],
                   evidence=[], prior_score=0.5, status="unstated")
    s = GapSearch(orch, targets, [a], SearchConfig(max_runs=40))
    [r] = await s.run()
    notes = [e.get("msg", "") for e in orch.events.read() if e.get("type") == "note"]
    assert any("held for a patch round" in n for n in notes)
    assert r.changes == {ast_patch.knob_name("model.py", 2, "lengthscale"): "0.1"}, (r.changes, r.notes)


async def test_a_literal_in_the_entry_script_is_patched_through_the_runner(tmp_path):
    """The command runs bench.py directly, so its own literal (tau = 1.5) can be patched via gf_patch_run."""
    art = ROOT / "eval" / "toy" / "patch_main"
    before = (art / "bench.py").read_bytes()
    spec = HarnessSpec.load_yaml(ROOT / "eval" / "toy" / "patch_main.yaml")
    spec.source = str(art)
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    targets = [Target("C1", "score", 300.0), Target("C2", "aux", 450.0, held_out=True)]  # tau = 3.0
    a = Assumption(id="A1", knob="alpha", layer="config", paper_value="unstated", candidate_values=["2.0"],
                   evidence=[], prior_score=0.5, status="unstated")
    s = GapSearch(orch, targets, [a], SearchConfig(max_runs=120))
    [r] = await s.run()
    assert r.changes == {ast_patch.knob_name("bench.py", 4, "tau"): "3"}, (r.changes, r.notes)
    assert (art / "bench.py").read_bytes() == before


async def test_a_paper_to_trace_difference_leads_the_patch_round(tmp_path):
    """Part 4: out of space, Super compares the paper with the traced run. A difference grounded to a literal
    is tried first, with the paper's value first; a structural one is only reported."""
    from gapfinder.search.contrast import Difference, Differences

    calls = []

    class FakeRouter:
        meter = type("Meter", (), {"total_cost": lambda self: 0.0})()

        async def structured(self, model, messages, schema):
            calls.append(messages[0]["content"])
            return Differences(differences=[
                Difference(file="model.py", line=2, paper_says="a length scale of 0.1", code_does="0.01",
                           kind="literal", name="lengthscale", paper_value="0.1"),
                Difference(file="bench.py", line=1, paper_says="scores averaged over 5 seeds",
                           code_does="one seed", kind="structural"),
                Difference(file="nope.py", line=3, paper_says="x", code_does="y", kind="structural")])

    paper = _paper(tmp_path)
    spec = HarnessSpec.load_yaml(SPEC)
    spec.source = str(ART)
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    targets = [Target("C1", "score", paper["score"]), Target("C2", "aux", paper["aux"], held_out=True)]
    a = Assumption(id="A1", knob="alpha", layer="config", paper_value="unstated", candidate_values=["2.0"],
                   evidence=[], prior_score=0.5, status="unstated")
    s = GapSearch(orch, targets, [a], SearchConfig(max_runs=120), router=FakeRouter(),
                  paper_text="We use a kernel length scale of 0.1 and average scores over 5 seeds.")
    [r] = await s.run()
    knob = ast_patch.knob_name("model.py", 2, "lengthscale")
    assert calls and "length scale of 0.1" in calls[0] and "Values that reached known library calls" in calls[0]
    assert r.diagnosis["contrast_leads"][0]["file"] == "model.py" and r.diagnosis["contrast_leads"][0]["paper_value"] == "0.1"
    assert [x["file"] for x in r.diagnosis["structural_leads"]] == ["bench.py"]  # nope.py was rejected
    first_patch = next(e["branch"]["knob_changes"] for e in orch.events.read()
                       if e["type"] == "branch_created" and knob in e["branch"]["knob_changes"])
    assert first_patch[knob] == "0.1"  # the paper's value is tried first
    assert r.changes == {knob: "0.1"}
    from gapfinder.report.gap_report import GapReport
    md = GapReport.from_search(s, [r], paper="toy").to_markdown()
    assert "Where the code differs from the paper" in md and "bench.py:1" in md
