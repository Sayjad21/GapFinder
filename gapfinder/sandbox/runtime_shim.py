"""The runtime shim every run gets (plan item 8): GPU-written code runs on the CPU-only Sandboxes VM.

Two dev-set harnesses needed the same hand-made shim, a class: Anomaly Transformer calls `Tensor.cuda()`
unconditionally, and SparseTSF reloads its checkpoint with `map_location="cuda:0"`. When CUDA is unavailable, this
hook, loaded as `sitecustomize` from `.gf_runtime/` on PYTHONPATH, makes `.cuda()` a no-op on tensors and modules
and maps `torch.load` to the CPU. It patches torch only after the program imports it, and chains to the next
sitecustomize (the environment's own). Nothing changes when a GPU is present or torch is never imported.

The run also gets glibc allocator settings (fewer malloc arenas, earlier trimming): memory only, not results
(Anomaly Transformer's batch 32 needed jemalloc to fit 3.9 GB). Thread counts are left to the spec, because they can
change floating-point sums.
"""

from __future__ import annotations

from gapfinder.sandbox.hook_chain import CHAIN_SOURCE

HOOK_DIR = ".gf_runtime"
ENV = {"MALLOC_ARENA_MAX": "2", "MALLOC_TRIM_THRESHOLD_": "65536"}

HOOK_BODY = r'''
# GapFinder runtime shim (gapfinder/sandbox/runtime_shim.py): CPU fallbacks for GPU-written code. Never raises.
import sys

def _gf_patch_torch(torch):
    try:
        if torch.cuda.is_available():
            return
        torch.Tensor.cuda = lambda self, *a, **k: self
        torch.nn.Module.cuda = lambda self, *a, **k: self
        _load = torch.load
        def _cpu_load(*a, **k):
            k["map_location"] = "cpu"
            return _load(*a, **k)
        torch.load = _cpu_load
    except Exception:
        pass

try:
    import importlib.abc, importlib.machinery

    class _GfTorchLoader(importlib.abc.Loader):
        def __init__(self, inner):
            self.inner = inner
        def create_module(self, spec):
            return self.inner.create_module(spec)
        def exec_module(self, module):
            self.inner.exec_module(module)
            _gf_patch_torch(module)

    class _GfTorchFinder(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path, target=None):
            if name != "torch":
                return None
            spec = importlib.machinery.PathFinder.find_spec(name, path)
            if spec is not None and spec.loader is not None:
                spec.loader = _GfTorchLoader(spec.loader)
            return spec

    if "torch" in sys.modules:
        _gf_patch_torch(sys.modules["torch"])
    else:
        sys.meta_path.insert(0, _GfTorchFinder())
except Exception:
    pass

# The paper-year environment's import redirect (gapfinder/env_year.py): GF_LIB_DIRS="dir|dir" (first listed wins);
# each directory's top-level modules are imported from it, whatever sys.path says (an old release then wins even
# over a package beside the script).
try:
    import os as _gf_os
    _gf_dirs = [d for d in _gf_os.environ.get("GF_LIB_DIRS", "").split("|") if d and _gf_os.path.isdir(d)]
    _gf_tops = {}
    for _d in _gf_dirs:
        _names = set()
        for _e in _gf_os.listdir(_d):
            if _e.endswith(".dist-info") or _e.endswith(".egg-info"):
                _tl = _gf_os.path.join(_d, _e, "top_level.txt")
                if _gf_os.path.isfile(_tl):
                    _names.update(x.strip() for x in open(_tl).read().split() if x.strip())
                continue
            if _e in ("bin", "__pycache__") or _e.startswith("."):
                continue
            if _gf_os.path.isdir(_gf_os.path.join(_d, _e)):
                _names.add(_e)
            elif _e.endswith(".py") or _e.endswith(".so") or _e.endswith(".pyd"):
                _names.add(_e.split(".")[0])
        for _n in _names:
            _gf_tops.setdefault(_n, _d)

    if _gf_tops:
        import importlib.machinery as _gf_mach

        class _GfLibFinder(object):
            def find_spec(self, name, path, target=None):
                d = _gf_tops.get(name)
                if d is None:
                    return None
                spec = _gf_mach.PathFinder.find_spec(name, [d])
                loader = globals().get("_GfTorchLoader")
                if spec is not None and name == "torch" and spec.loader is not None and loader is not None:
                    spec.loader = loader(spec.loader)
                return spec

        sys.meta_path.insert(0, _GfLibFinder())
except Exception:
    pass
'''
HOOK_SOURCE = HOOK_BODY + CHAIN_SOURCE  # alone on PYTHONPATH: chain to the environment's own sitecustomize


def run_parts() -> tuple[dict[str, str], dict[str, bytes], str]:
    """(env, files to upload, shell prefix) for every run."""
    prefix = f'export PYTHONPATH="${{PYTHONPATH:+$PYTHONPATH:}}${{WORK:-$PWD}}/{HOOK_DIR}"; '
    return dict(ENV), {f"{HOOK_DIR}/sitecustomize.py": HOOK_SOURCE.encode()}, prefix
