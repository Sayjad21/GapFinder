"""The no-keys quick start (scripts/try_it.py) completes offline from the committed model cache."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "try_it.py"

pytestmark = pytest.mark.skipif(not (ROOT / "demo" / "cache" / "llm").is_dir(), reason="demo/cache is not present")


def _run(*args: str, out: Path | None = None) -> subprocess.CompletedProcess:
    # A clean environment: no credentials, no cache or spend settings from the developer's shell.
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("GF_", "TOKEN_FACTORY", "NVIDIA", "NEBIUS", "TAVILY"))}
    cmd = [sys.executable, str(SCRIPT), *args] + (["--out", str(out)] if out else [])
    return subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8", timeout=300, cwd=ROOT)


def test_list_and_unknown_task():
    listed = _run("--list")
    assert listed.returncode == 0
    assert "dev-ml-threshold" in listed.stdout.split()
    assert _run("--task", "no-such-task").returncode == 2


def test_quick_start_runs_offline(tmp_path):
    r = _run("--task", "dev-ml-threshold", out=tmp_path / "report")
    assert r.returncode == 0, r.stderr[-2000:]
    report = (tmp_path / "report" / "gap_report.md").read_text(encoding="utf-8")
    assert "C1 (test_accuracy)" in report
    assert "0.00 USD spent" in r.stdout
    assert "cache miss" not in r.stderr
