"""The runtime shim every run gets (plan item 8): GPU-written code runs on the CPU-only Sandboxes VM.

Two dev-set harnesses needed the same hand-made shim, a class: Anomaly Transformer calls `Tensor.cuda()`
unconditionally, and SparseTSF reloads its checkpoint with `map_location="cuda:0"`. When CUDA is unavailable, this
hook, loaded as `sitecustomize` from `.gf_runtime/` on PYTHONPATH, makes `.cuda()` a no-op on tensors and modules
and maps `torch.load` to the CPU. It patches torch only after the program imports it, and chains to the next
sitecustomize (the environment's own). Nothing changes when a GPU is present or torch is never imported.

The run also gets glibc allocator settings (fewer malloc arenas, earlier trimming): memory only, not results
(Anomaly Transformer's batch 32 needed jemalloc to fit 3.9 GB). Thread counts are left to the spec, because they can
change floating-point sums.

Large arrays are memory-mapped (plan F6): `numpy.load` of a `.npy` file over 50 MB maps it copy-on-write (pages
are read from the file on demand and count against memory only once written; read-only mode would break code that
writes into the array), and `torch.load` of a file over 50 MB passes `mmap=True` (torch 2.1 and later; a file that
can't be mapped is loaded as before). Same values, less resident memory on a 3.9 GB VM with no swap.
GF_NO_MMAP=1 turns it off.
"""

from __future__ import annotations

from gapfinder.sandbox.hook_chain import CHAIN_SOURCE

HOOK_DIR = ".gf_runtime"
ENV = {"MALLOC_ARENA_MAX": "2", "MALLOC_TRIM_THRESHOLD_": "65536"}

HOOK_BODY = r'''
# GapFinder runtime shim (gapfinder/sandbox/runtime_shim.py): CPU fallbacks for GPU-written code. Never raises.
import sys

_GF_MMAP_MIN = 50 * 2 ** 20


def _gf_big_file(f):
    import os
    try:
        if os.environ.get("GF_NO_MMAP") == "1" or not isinstance(f, (str, bytes, os.PathLike)):
            return False
        least = float(os.environ.get("GF_MMAP_MIN_MB", "")) * 2 ** 20 if os.environ.get("GF_MMAP_MIN_MB") else _GF_MMAP_MIN
        return os.path.getsize(os.fspath(f)) > least
    except Exception:
        return False


def _gf_patch_torch(torch):
    try:
        _load = torch.load
        cpu = not torch.cuda.is_available()
        if cpu:
            torch.Tensor.cuda = lambda self, *a, **k: self
            torch.nn.Module.cuda = lambda self, *a, **k: self
        try:
            major, minor = (int(x) for x in torch.__version__.split(".")[:2])
            can_mmap = (major, minor) >= (2, 1)
        except Exception:
            can_mmap = False

        def _gf_load(*a, **k):
            if cpu:
                k["map_location"] = "cpu"
            if can_mmap and "mmap" not in k and a and _gf_big_file(a[0]):
                try:
                    return _load(*a, mmap=True, **k)
                except Exception:
                    pass  # an old (non-zip) file can't be mapped: load it as before
            return _load(*a, **k)
        torch.load = _gf_load
    except Exception:
        pass


def _gf_patch_numpy(np):
    try:
        _load = np.load

        def _gf_np_load(file, mmap_mode=None, *a, **k):
            if mmap_mode is None and str(getattr(file, "__fspath__", lambda: file)()).endswith(".npy") \
                    and _gf_big_file(file):
                mmap_mode = "c"  # copy-on-write: writable, the file never changes
            return _load(file, mmap_mode, *a, **k)
        np.load = _gf_np_load
    except Exception:
        pass


_GF_PATCHES = {"torch": _gf_patch_torch, "numpy": _gf_patch_numpy}

try:
    import importlib.abc, importlib.machinery

    class _GfTorchLoader(importlib.abc.Loader):
        def __init__(self, inner, patch=_gf_patch_torch):
            self.inner = inner
            self.patch = patch
        def create_module(self, spec):
            return self.inner.create_module(spec)
        def exec_module(self, module):
            self.inner.exec_module(module)
            self.patch(module)

    class _GfTorchFinder(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path, target=None):
            if name not in _GF_PATCHES or name in sys.modules:
                return None
            spec = importlib.machinery.PathFinder.find_spec(name, path)
            if spec is not None and spec.loader is not None:
                spec.loader = _GfTorchLoader(spec.loader, _GF_PATCHES[name])
            return spec

    for _gf_name, _gf_patch in _GF_PATCHES.items():
        if _gf_name in sys.modules:
            _gf_patch(sys.modules[_gf_name])
    if any(n not in sys.modules for n in _GF_PATCHES):
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
                if spec is not None and name in _GF_PATCHES and spec.loader is not None and loader is not None:
                    spec.loader = loader(spec.loader, _GF_PATCHES[name])
                return spec

        sys.meta_path.insert(0, _GfLibFinder())
except Exception:
    pass
'''
HOOK_SOURCE = HOOK_BODY + CHAIN_SOURCE  # alone on PYTHONPATH: chain to the environment's own sitecustomize


def run_parts() -> tuple[dict[str, str], dict[str, bytes], str]:
    """(env, files to upload, shell prefix) for every run."""
    prefix = f'export PYTHONPATH="${{PYTHONPATH:+$PYTHONPATH${{GF_PATHSEP:-:}}}}${{WORK:-$PWD}}/{HOOK_DIR}"; '
    return dict(ENV), {f"{HOOK_DIR}/sitecustomize.py": HOOK_SOURCE.encode()}, prefix
