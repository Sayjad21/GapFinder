# batch-3 b3c: CPU-only VM shim, installed into site-packages with a .pth file at build time (an environment
# change, not a repository change). exp/exp_main.py reloads its best checkpoint with map_location="cuda:0", which
# fails without a GPU; on a CPU-only machine torch.load maps to the CPU instead.
try:
    import torch

    if not torch.cuda.is_available():
        _orig_load = torch.load

        def _cpu_load(*args, **kwargs):
            kwargs["map_location"] = "cpu"
            return _orig_load(*args, **kwargs)

        torch.load = _cpu_load
except Exception:
    pass
