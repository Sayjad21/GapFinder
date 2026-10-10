import hashlib
import importlib.util
from pathlib import Path

import pytest

from gapfinder.report.provenance import prompt_hashes

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("freeze_record", ROOT / "scripts" / "freeze_record.py")
fr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fr)


def record(**kw):
    return fr.build_record(tag="ext-eval-test", max_runs=30, budget_usd=5, seed=7, root=ROOT, allow_dirty=True, **kw)


def test_record_has_commit_models_prompt_hashes_inputs_arms_and_budget():
    text = record()
    assert "ext-eval-test" in text and "--max-runs 30" in text and "--cap 5" in text
    for name, h in prompt_hashes().items():
        assert name in text and h in text
    for rel in ("mcd.yaml", "targets_mcd.json"):
        assert hashlib.sha256((ROOT / fr.CASE / rel).read_bytes()).hexdigest() in text
    for arm in ("normal", "evidence off", "no README", "all flags, random"):
        assert f"| {arm} |" in text
    assert "nemotron" in text.lower()  # model IDs come from the config
    assert "answer_key.sha256" in text and "answer_key.md" not in text  # only the hash is read


def test_arm_commands_are_exact():
    text = record()
    assert "--no-evidence-gate" in text
    assert "--hypotheses repomap --rank random --seed 7" in text
    assert "--assumptions runs/mcd-ledger-nodocs/assumptions.json" in text  # the no-README arm's own ledger
    normal = next(l for l in text.splitlines() if l.startswith("GF_SPEND_TAG") and "run-normal" in l)
    assert "--no-evidence-gate" not in normal and "--hypotheses" not in normal and "--backend local" in normal
    rand = next(l for l in text.splitlines() if "run-all-flags-random" in l)
    assert "--assumptions" not in rand


def test_dirty_tree_is_refused_and_main_writes_the_file(tmp_path, monkeypatch):
    monkeypatch.setattr(fr, "git_state", lambda: {"commit": "a" * 40, "dirty": True})
    with pytest.raises(SystemExit):
        fr.build_record(tag="t", max_runs=1, budget_usd=1, seed=0, root=ROOT, allow_dirty=False)
    out = tmp_path / "sub" / "FROZEN.md"
    assert fr.main(["--tag", "t", "--out", str(out), "--max-runs", "9", "--budget-usd", "2.5", "--allow-dirty"]) == 0
    assert "`" + "a" * 40 + "`" in out.read_text(encoding="utf-8") and "(working tree was dirty)" in out.read_text(encoding="utf-8")


def test_candidates_per_knob_is_recorded_for_every_arm_and_defaults_to_the_products():
    from gapfinder.search.engine import SearchConfig

    text = record()
    cmds = [l for l in text.splitlines() if l.startswith("GF_SPEND_TAG")]
    assert len(cmds) == 4
    assert all(f"--candidates-per-knob {SearchConfig().candidates_per_knob}" in c for c in cmds)
    assert "Values tried per knob in the screen" in text
    assert "--candidates-per-knob 3" in record(candidates_per_knob=3)


def test_record_scope_is_energy_and_yacht_only():
    text = record()
    assert "Concrete is not searched" in text and "--max-runs 30" in text
    assert "GF_MAX_CONCURRENCY=6" in text
    assert hashlib.sha256((ROOT / fr.CASE / "harness" / "run_cell.sh").read_bytes()).hexdigest() in text
