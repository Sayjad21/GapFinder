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
