"""Plan F6: the runtime shim memory-maps large arrays (copy-on-write) without changing what the program reads."""

import os
import subprocess
import sys

import numpy as np

from gapfinder.sandbox import runtime_shim

PROBE = """
import numpy as np
big, small = np.load("big.npy"), np.load("small.npy")
print("BIG", type(big).__name__, float(big.sum()))
print("SMALL", type(small).__name__)
big[0] = 99.0  # writable: copy-on-write
print("WROTE", float(big[0]))
"""


def _run(tmp_path, extra_env):
    hook = tmp_path / runtime_shim.HOOK_DIR
    hook.mkdir(exist_ok=True)
    _, files, _ = runtime_shim.run_parts()
    (hook / "sitecustomize.py").write_bytes(files[f"{runtime_shim.HOOK_DIR}/sitecustomize.py"])
    np.save(tmp_path / "big.npy", np.arange(300_000, dtype=np.float64))  # about 2.3 MB
    np.save(tmp_path / "small.npy", np.arange(10, dtype=np.float64))
    (tmp_path / "probe.py").write_text(PROBE, encoding="utf-8")
    env = {**os.environ, "PYTHONPATH": str(hook), "GF_MMAP_MIN_MB": "1", **extra_env}
    out = subprocess.run([sys.executable, "probe.py"], cwd=tmp_path, env=env, capture_output=True, text=True,
                         check=True).stdout
    return dict(line.split(" ", 1) for line in out.strip().splitlines())


def test_a_large_array_is_mapped_copy_on_write(tmp_path):
    got = _run(tmp_path, {})
    assert got["BIG"].startswith("memmap") and float(got["BIG"].split()[1]) == float(np.arange(300_000).sum())
    assert got["SMALL"] == "ndarray"
    assert float(got["WROTE"]) == 99.0
    assert float(np.load(tmp_path / "big.npy")[0]) == 0.0  # the file on disk never changes


def test_it_can_be_turned_off(tmp_path):
    assert _run(tmp_path, {"GF_NO_MMAP": "1"})["BIG"].startswith("ndarray")
