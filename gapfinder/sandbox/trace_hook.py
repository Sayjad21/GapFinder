"""Runtime sink tracing: learn what each setting *does* by watching where its value lands in one dry run.

Name rules (`_UNBOUNDED_NAME`, `_MULT_NAME`) and argparse scraping guess a knob's kind from its name; that
failed on FastGCN (tf.app.flags) and can't see a constant like `batch_size = 128` inside a module. Before a
search, GapFinder can run the harness command once with this hook (`.gf_trace/sitecustomize.py`, uploaded
next to the artifact like the patch hook; no artifact file changes) and record:

- config sources: what argparse returned, absl/tf.app.flags values, dicts loaded by yaml or json;
- sinks, with the repo call site that reached them: optimizer hyperparameters (lr, weight_decay, momentum,
  betas), dropout probabilities, DataLoader batch sizes, scheduler arguments, seeds, layer widths, and
  `range()` bounds called from the repo's own files.

`gapfinder/search/trace.py` matches config values to sink arguments by value and gives each knob a role
(rate, fraction, size, count, seed); a literal at a sink's call site with no config behind it becomes a
patch-knob lead. A dry run stops itself after GF_TRACE_STEPS optimizer steps or GF_TRACE_SECONDS seconds.

The hook is written for Python 3.6+ (the oldest artifact image) and must never break the artifact: every
hook body is wrapped, and a failure inside it only loses that record.
"""

from __future__ import annotations

HOOK_DIR = ".gf_trace"
OUT_DIR = ".gf_trace_out"
MARKER = "GF_TRACE_JSON:"

HOOK_SOURCE = r'''
# GapFinder trace hook (gapfinder/sandbox/trace_hook.py). Records config values and the arguments that reach
# known sinks during one dry run; writes $GF_TRACE_DIR/<pid>.json at exit. Never raises into the artifact.
import atexit, builtins, json, os, sys, threading, time

_ROOT = os.path.realpath(os.environ.get("GF_TRACE_ROOT") or os.getcwd())
_OUT = os.environ.get("GF_TRACE_DIR") or os.path.join(_ROOT, ".gf_trace_out")
_STEPS = int(os.environ.get("GF_TRACE_STEPS") or "0")
_SECONDS = float(os.environ.get("GF_TRACE_SECONDS") or "0")
_MAX = 400  # records kept per kind
_rec = {"pid": os.getpid(), "argv": list(sys.argv), "config": [], "sinks": [], "ranges": {}, "steps": 0}
_seen = set()
_done = [False]
_real_range = builtins.range


def _site(depth=2):
    """The nearest caller frame inside the repo (not the hook, not site-packages)."""
    try:
        f = sys._getframe(depth)
    except ValueError:
        return None
    while f is not None:
        fn = f.f_code.co_filename
        if fn and not fn.startswith("<"):
            p = os.path.realpath(fn)
            if p.startswith(_ROOT + os.sep) and os.sep + ".gf_trace" not in p and "site-packages" not in p:
                return [os.path.relpath(p, _ROOT).replace(os.sep, "/"), f.f_lineno]
        f = f.f_back
    return None


def _plain(v):
    if isinstance(v, (bool, int, float, str)) or v is None:
        return v
    if isinstance(v, (list, tuple)) and len(v) <= 8 and all(isinstance(x, (bool, int, float, str)) for x in v):
        return list(v)
    try:
        import numbers
        if isinstance(v, numbers.Number):
            return float(v)
    except Exception:
        pass
    return None


def _sink(kind, cls, args, site=None):
    try:
        args = {k: _plain(v) for k, v in args.items()}
        args = {k: v for k, v in args.items() if v is not None}
        site = site or _site(3)
        key = (kind, cls, json.dumps(args, sort_keys=True, default=str), tuple(site or ()))
        if key in _seen or len(_rec["sinks"]) >= _MAX:
            return
        _seen.add(key)
        _rec["sinks"].append({"kind": kind, "cls": cls, "args": args, "site": site})
    except Exception:
        pass


def _config(src, values, where=None):
    try:
        flat = {}

        def walk(prefix, v, depth=0):
            if isinstance(v, dict) and depth < 4:
                for k, x in list(v.items())[:200]:
                    walk(prefix + [str(k)], x, depth + 1)
            else:
                p = _plain(v)
                if p is not None and prefix:
                    flat[".".join(prefix)] = p
        walk([], values)
        if flat and len(_rec["config"]) < _MAX:
            _rec["config"].append({"src": src, "where": where, "values": flat})
    except Exception:
        pass


def _dump():
    if _done[0]:
        return
    _done[0] = True
    try:
        try:  # absl / tf.app.flags: the parsed values, if any
            fl = sys.modules.get("absl.flags")
            if fl is not None and fl.FLAGS.is_parsed():
                _config("absl", fl.FLAGS.flag_values_dict())
        except Exception:
            pass
        _rec["ranges"] = {"%s:%s" % k: v for k, v in list(_rec["ranges"].items())[:_MAX]}
        os.makedirs(_OUT, exist_ok=True)
        with open(os.path.join(_OUT, "%d.json" % os.getpid()), "w") as f:
            json.dump(_rec, f, default=str)
    except Exception:
        pass


def _stop():
    _dump()
    sys.stdout.flush(); sys.stderr.flush()
    os._exit(0)


atexit.register(_dump)
if _SECONDS > 0:
    t = threading.Timer(_SECONDS, _stop)
    t.daemon = True
    t.start()


# ---- stdlib sources and sinks (patched now)
def _range(*a):
    try:  # only the direct caller, and only repo files: library code calls range() constantly
        fn = sys._getframe(1).f_code.co_filename
        if fn and not fn.startswith(("/", "<")) and ":" not in fn[:3]:
            fn = os.path.abspath(fn)  # a script run by a relative path has a relative co_filename
        site = None
        if fn.startswith(_ROOT) and "site-packages" not in fn and ".gf_trace" not in fn:
            site = [os.path.relpath(fn, _ROOT).replace(os.sep, "/"), sys._getframe(1).f_lineno]
        if site is not None and a:
            stop = a[1] if len(a) > 1 else a[0]
            if isinstance(stop, int):
                key = (site[0], site[1])
                vals = _rec["ranges"].setdefault(key, [])
                if stop not in vals and len(vals) < 5:
                    vals.append(stop)
    except Exception:
        pass
    return _real_range(*a)


builtins.range = _range

try:
    import argparse as _ap
    _orig_pka = _ap.ArgumentParser.parse_known_args

    def _pka(self, *a, **k):
        res = _orig_pka(self, *a, **k)
        try:
            ns = res[0]
            flags = {}
            for act in self._actions:
                if act.dest and act.option_strings:
                    flags[act.dest] = act.option_strings[0]
            _config("argparse", dict(vars(ns)), where={"flags": flags, "site": _site(2)})
        except Exception:
            pass
        return res
    _ap.ArgumentParser.parse_known_args = _pka
except Exception:
    pass

try:
    import json as _json
    _orig_jload, _orig_jloads = _json.load, _json.loads

    def _jload(fp, *a, **k):
        v = _orig_jload(fp, *a, **k)
        name = str(getattr(fp, "name", "") or "")
        in_repo = os.path.realpath(name).startswith(_ROOT + os.sep) if name else False
        if isinstance(v, dict) and (in_repo or _site(2) is not None) and "site-packages" not in name:
            _config("json", v, where=name or None)  # the artifact's own config, not a library's metadata
        return v

    def _jloads(s, *a, **k):
        v = _orig_jloads(s, *a, **k)
        if isinstance(v, dict) and _site(2) is not None:
            _config("json", v)
        return v
    _json.load, _json.loads = _jload, _jloads
except Exception:
    pass

try:
    import random as _random
    _orig_rseed = _random.seed

    def _rseed(a=None, *x, **k):
        _sink("seed", "random.seed", {"seed": a})
        return _orig_rseed(a, *x, **k)
    _random.seed = _rseed
except Exception:
    pass


# ---- third-party sinks: patched right after their module is imported
def _wrap_init(cls, kind, names):
    try:
        import inspect
        orig = cls.__init__
        sig = inspect.signature(orig)

        def init(self, *a, **k):
            try:
                b = sig.bind_partial(self, *a, **k)
                vals = {n: b.arguments[n] for n in names if n in b.arguments}
                for n in names:  # defaults the caller didn't pass
                    if n not in vals and n in sig.parameters and sig.parameters[n].default is not inspect._empty:
                        vals[n] = sig.parameters[n].default
                _sink(kind, cls.__name__, vals)
            except Exception:
                pass
            return orig(self, *a, **k)
        cls.__init__ = init
    except Exception:
        pass


def _wrap_fn(mod, name, kind, names):
    try:
        import inspect
        orig = getattr(mod, name)
        try:
            sig = inspect.signature(orig)
        except (TypeError, ValueError):
            sig = None

        def fn(*a, **k):
            try:
                if sig is not None:
                    b = sig.bind_partial(*a, **k)
                    _sink(kind, mod.__name__ + "." + name, {n: b.arguments[n] for n in names if n in b.arguments})
                else:
                    _sink(kind, mod.__name__ + "." + name, {"arg0": a[0] if a else None})
            except Exception:
                pass
            return orig(*a, **k)
        setattr(mod, name, fn)
    except Exception:
        pass


_OPT = ["lr", "learning_rate", "weight_decay", "momentum", "betas", "eps", "alpha", "rho", "dampening"]


def _after(name, mod):
    try:
        if name == "torch.optim.optimizer":
            O = mod.Optimizer
            orig_init = O.__init__

            def oinit(self, params, defaults, *a, **k):
                try:
                    _sink("optimizer", type(self).__name__, {n: defaults.get(n) for n in _OPT if n in defaults})
                except Exception:
                    pass
                return orig_init(self, params, defaults, *a, **k)
            O.__init__ = oinit
            orig_zero = O.zero_grad

            def zero(self, *a, **k):  # zero_grad marks one optimizer step (step() itself is often re-wrapped)
                _rec["steps"] += 1
                if _STEPS and _rec["steps"] > _STEPS:
                    _stop()
                return orig_zero(self, *a, **k)
            O.zero_grad = zero
        elif name == "torch.optim.lr_scheduler":
            for n in dir(mod):
                c = getattr(mod, n)
                if isinstance(c, type) and n.endswith(("LR", "LR_", "Plateau")) and n not in ("_LRScheduler", "LRScheduler"):
                    _wrap_init(c, "scheduler", ["step_size", "gamma", "T_max", "milestones", "eta_min", "patience", "factor"])
        elif name == "torch.nn.modules.dropout":
            _wrap_init(mod._DropoutNd, "dropout", ["p"])
        elif name == "torch.nn.functional":
            _wrap_fn(mod, "dropout", "dropout", ["p"])
        elif name == "torch.nn.modules.linear":
            _wrap_init(mod.Linear, "width", ["in_features", "out_features"])
        elif name == "torch.utils.data.dataloader":
            _wrap_init(mod.DataLoader, "batch", ["batch_size", "shuffle"])
        elif name == "torch.random" or name == "torch":
            if hasattr(mod, "manual_seed"):
                _wrap_fn(mod, "manual_seed", "seed", ["seed"])
        elif name == "numpy.random":
            _wrap_fn(mod, "seed", "seed", ["seed"])
        elif name == "sklearn.model_selection._search":
            _wrap_init(mod.GridSearchCV, "grid_search", ["param_grid", "cv"])
        elif name.startswith("tensorflow") and name.endswith(".training.optimizer"):
            # subclasses set self._lr after the base __init__, so read it when the graph is built
            for meth in ("minimize", "apply_gradients"):
                orig = getattr(mod.Optimizer, meth)

                def tmeth(self, *a, _orig=orig, **k):
                    try:
                        vals = {"learning_rate": getattr(self, "_lr", None)}
                        for attr, key in (("_beta1", "beta1"), ("_beta2", "beta2"), ("_momentum", "momentum")):
                            if hasattr(self, attr):
                                vals[key] = getattr(self, attr)
                        _sink("optimizer", type(self).__name__, vals)
                    except Exception:
                        pass
                    return _orig(self, *a, **k)
                setattr(mod.Optimizer, meth, tmeth)
        elif name == "keras.optimizers" or name.endswith("keras.optimizers"):
            for n in ("SGD", "Adam", "RMSprop", "Adagrad", "Adadelta", "Adamax", "Nadam"):
                if hasattr(mod, n):
                    _wrap_init(getattr(mod, n), "optimizer", ["lr", "learning_rate", "decay", "momentum"])
    except Exception:
        pass


_WATCH = {"torch", "torch.optim.optimizer", "torch.optim.lr_scheduler", "torch.nn.modules.dropout", "torch.nn.functional",
          "torch.nn.modules.linear", "torch.utils.data.dataloader", "torch.random", "numpy.random",
          "sklearn.model_selection._search", "keras.optimizers"}

try:
    import importlib.abc, importlib.machinery

    class _Finder(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path, target=None):
            if not (fullname in _WATCH or (fullname.startswith("tensorflow") and fullname.endswith(".training.optimizer"))):
                return None
            for f in sys.meta_path:
                if f is self:
                    continue
                try:
                    spec = f.find_spec(fullname, path, target)
                except Exception:
                    spec = None
                if spec is not None and spec.loader is not None and hasattr(spec.loader, "exec_module"):
                    orig = spec.loader.exec_module

                    def exec_module(module, _orig=orig, _name=fullname):
                        _orig(module)
                        _after(_name, module)
                    spec.loader.exec_module = exec_module
                    return spec
            return None
    sys.meta_path.insert(0, _Finder())
except Exception:
    pass

# modules imported before this hook ran (e.g. by a .pth file at interpreter start) get their sinks now
for _name, _mod in list(sys.modules.items()):
    try:
        if _mod is not None and (_name in _WATCH or (_name.startswith("tensorflow") and _name.endswith(".training.optimizer"))):
            _after(_name, _mod)
    except Exception:
        pass

try:
    import yaml as _yaml  # yaml is often imported before the code reads its config: patch now if present
except Exception:
    _yaml = None
if _yaml is not None:
    try:
        for _n in ("load", "safe_load", "full_load"):
            if hasattr(_yaml, _n):
                def _mk(orig):
                    def f(stream, *a, **k):
                        v = orig(stream, *a, **k)
                        if isinstance(v, dict):
                            _config("yaml", v, where=getattr(stream, "name", None))
                        return v
                    return f
                setattr(_yaml, _n, _mk(getattr(_yaml, _n)))
    except Exception:
        pass
'''


def run_parts(steps: int = 30, seconds: float = 900) -> tuple[dict[str, str], dict[str, bytes], str, str]:
    """(env, files to upload, shell prefix, shell suffix) for a dry run with the trace hook."""
    env = {"GF_TRACE_STEPS": str(steps), "GF_TRACE_SECONDS": str(seconds)}
    files = {f"{HOOK_DIR}/sitecustomize.py": HOOK_SOURCE.encode()}
    prefix = (f'export GF_TRACE_ROOT="${{WORK:-$PWD}}" GF_TRACE_DIR="${{WORK:-$PWD}}/{OUT_DIR}"; '
              f'mkdir -p "$GF_TRACE_DIR"; '
              f'export PYTHONPATH="${{WORK:-$PWD}}/{HOOK_DIR}${{PYTHONPATH:+:$PYTHONPATH}}"; ')
    suffix = f'; for f in "${{WORK:-$PWD}}"/{OUT_DIR}/*.json; do [ -f "$f" ] && printf "{MARKER}%s\\n" "$(cat "$f")"; done; true'
    return env, files, prefix, suffix


def parse_output(text: str) -> list[dict]:
    """The per-process trace records printed by the dry run."""
    import json

    out = []
    for line in text.splitlines():
        if line.startswith(MARKER):
            try:
                out.append(json.loads(line[len(MARKER):]))
            except ValueError:
                continue
    return out
