"""Patch knobs: the in-memory hook swaps exactly one literal and leaves files untouched."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

from gapfinder.sandbox import ast_patch as ap

MOD = "import math\n\nbatch_size = 128\nlengthscale = 1e-2\n\ndef run():\n    return fit(batch_size=500)\n\ndef fit(batch_size):\n    return batch_size\n"


def _run(tmp_path, patch):
    (tmp_path / "pkg").mkdir(exist_ok=True)
    (tmp_path / "pkg" / "net.py").write_text(MOD, encoding="utf-8")
    (tmp_path / "main.py").write_text("import sys\nsys.path.append('pkg')\nimport net\nprint(net.batch_size, net.run())\n",
                                      encoding="utf-8")
    env, files, prefix = ap.run_parts({ap.knob_name(*k): v for k, v in patch.items()})
    for rel, data in files.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_bytes(data)
    full = {**os.environ, **env, "PYTHONPATH": str(tmp_path / ap.HOOK_DIR)}
    return subprocess.run([sys.executable, "main.py"], cwd=tmp_path, env=full, capture_output=True, text=True)


def test_hook_swaps_the_assigned_literal_and_files_stay_byte_identical(tmp_path):
    r = _run(tmp_path, {("pkg/net.py", 3, "batch_size"): "32"})
    assert r.returncode == 0, r.stderr
    assert r.stdout.split() == ["32", "500"]  # line 3 patched; the keyword on another line is not
    assert (tmp_path / "pkg" / "net.py").read_text(encoding="utf-8") == MOD


def test_hook_swaps_a_keyword_literal_on_its_line(tmp_path):
    r = _run(tmp_path, {("pkg/net.py", 7, "batch_size"): "64"})
    assert r.returncode == 0, r.stderr and r.stdout.split() == ["128", "64"]
    assert r.stdout.split() == ["128", "64"]


def test_a_missing_target_fails_loudly(tmp_path):
    r = _run(tmp_path, {("pkg/net.py", 4, "batch_size"): "32"})  # line 4 assigns lengthscale, not batch_size
    assert r.returncode != 0 and "no literal batch_size on line 4" in r.stderr


def test_no_patch_knobs_means_no_hook():
    assert ap.run_parts({"lr": "0.1"}) == ({}, {}, "")
    assert ap.parse(ap.knob_name("net/net.py", 70, "batch_size")) == ("net/net.py", 70, "batch_size")


def test_entry_scripts_are_recognised(tmp_path):
    (tmp_path / "e.py").write_text("import argparse\na = argparse.ArgumentParser().parse_args()\n", encoding="utf-8")
    (tmp_path / "m.py").write_text("batch_size = 128\n", encoding="utf-8")
    assert ap.entry_script(tmp_path / "e.py") and not ap.entry_script(tmp_path / "m.py")
