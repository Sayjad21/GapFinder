# devbatch-2 at: CPU-only VM shim, installed into site-packages at build time (an environment change, not a
# repository change). model/attn.py calls Tensor.cuda() unconditionally (lines 29 and 51); with no GPU that
# raises. Here Tensor.cuda() returns the tensor itself when CUDA is unavailable, which is what the rest of the
# code already does on CPU (solver.py picks "cpu" when torch.cuda.is_available() is False).
try:
    import torch
    if not torch.cuda.is_available():
        torch.Tensor.cuda = lambda self, *args, **kwargs: self
except Exception:
    pass
