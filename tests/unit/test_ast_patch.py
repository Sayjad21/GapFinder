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


def test_an_entry_script_run_after_cd_is_found_relative_to_the_repo():
    from gapfinder.sandbox.ast_patch import direct_entry, wrap_command

    c = 'mkdir -p out; cd pygcn && PYTHONPATH="/work" python train.py --no-cuda > ../out/run.log; cd ..; python bench.py'
    assert direct_entry(c, "pygcn/train.py") and not direct_entry(c, "train.py") and direct_entry(c, "bench.py")
    assert "python -m gf_patch_run train.py --no-cuda" in wrap_command(c, {"pygcn/train.py"})
    assert "gf_patch_run bench.py" not in wrap_command(c, {"pygcn/train.py"})


def test_the_hooks_run_the_environments_own_sitecustomize_too(tmp_path):
    """devbatch-2 (Anomaly Transformer): a CPU shim in the environment's sitecustomize was shadowed by
    GapFinder's hook on PYTHONPATH. Both hooks now chain to the next sitecustomize on sys.path."""
    import os
    import subprocess
    import sys

    from gapfinder.sandbox import ast_patch, trace_hook

    env_dir = tmp_path / "env"
    env_dir.mkdir()
    (env_dir / "sitecustomize.py").write_text("import os\nos.environ['GF_ENV_SHIM'] = 'ran'\n", encoding="utf-8")
    for name, src in (("patch", ast_patch.HOOK_SOURCE), ("trace", trace_hook.HOOK_SOURCE)):
        hook = tmp_path / name
        hook.mkdir()
        (hook / "sitecustomize.py").write_text(src, encoding="utf-8")
        out = subprocess.run([sys.executable, "-c", "import os, sitecustomize; print(os.environ.get('GF_ENV_SHIM'), "
                              "os.path.basename(os.path.dirname(sitecustomize.__file__)))"],
                             env={**os.environ, "PYTHONPATH": os.pathsep.join([str(hook), str(env_dir)]),
                                  "GF_TRACE_DIR": str(tmp_path / "tr")},
                             capture_output=True, text=True, timeout=60)
        assert out.stdout.split() == ["ran", name], (name, out.stdout, out.stderr)


def test_the_runtime_shim_runs_gpu_written_code_on_the_cpu(tmp_path):
    """Anomaly Transformer (Tensor.cuda) and SparseTSF (torch.load(map_location="cuda:0")) needed this by hand."""
    import os
    import subprocess
    import sys

    from gapfinder.sandbox import runtime_shim

    fake = tmp_path / "lib" / "torch"
    (fake / "nn").mkdir(parents=True)
    (fake / "__init__.py").write_text(
        "from torch import nn\n"
        "class _Cuda:\n    @staticmethod\n    def is_available():\n        return False\n"
        "cuda = _Cuda()\n"
        "class Tensor:\n    def cuda(self):\n        raise RuntimeError('Found no NVIDIA driver')\n"
        "def load(path, map_location=None):\n    return map_location\n", encoding="utf-8")
    (fake / "nn" / "__init__.py").write_text(
        "class Module:\n    def cuda(self):\n        raise RuntimeError('Found no NVIDIA driver')\n", encoding="utf-8")
    hook = tmp_path / runtime_shim.HOOK_DIR
    hook.mkdir()
    (hook / "sitecustomize.py").write_text(runtime_shim.HOOK_SOURCE, encoding="utf-8")
    prog = ("import torch\nt = torch.Tensor()\nassert t.cuda() is t\nm = torch.nn.Module()\nassert m.cuda() is m\n"
            "print(torch.load('ckpt.pth', map_location='cuda:0'))\n")
    out = subprocess.run([sys.executable, "-c", prog], capture_output=True, text=True, timeout=60,
                         env={**os.environ, "PYTHONPATH": os.pathsep.join([str(hook), str(tmp_path / "lib")])})
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == "cpu"
