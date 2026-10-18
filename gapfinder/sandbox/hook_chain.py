"""Chain GapFinder's hooks to the environment's own `sitecustomize`.

The trace hook and the patch hook are each a `sitecustomize.py` on PYTHONPATH. Python imports only the first
`sitecustomize` it finds, so an environment that customises startup through its own (devbatch-2's Anomaly
Transformer harness: a CPU shim for `Tensor.cuda()` in site-packages) lost it under tracing and patching. This
tail, appended to both hooks, runs the next `sitecustomize` on sys.path after the hook's own directory.
Written for Python 2.7 and 3.6+ (the oldest artifact images); a failure only loses the chained file.
"""

CHAIN_SOURCE = r'''

def _gf_chain_next_sitecustomize():
    try:
        import os as _os, sys as _sys
        here = _os.path.dirname(_os.path.abspath(__file__))
        for d in _sys.path:
            if not d or _os.path.abspath(d) == here:
                continue
            f = _os.path.join(d, "sitecustomize.py")
            if _os.path.isfile(f) and _os.path.dirname(_os.path.abspath(f)) != here:
                g = {"__name__": "_gf_next_sitecustomize", "__file__": f}
                with open(f, "rb") as fh:
                    exec(compile(fh.read(), f, "exec"), g)
                break
    except Exception:
        pass

_gf_chain_next_sitecustomize()
'''
