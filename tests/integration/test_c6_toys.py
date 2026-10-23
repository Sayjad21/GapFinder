"""Plan I (c6): new instances of the classes seed 6's misses showed.

(I1) A setting matches the target and the held-out claim at the default condition by coincidence, but not the
     claims at other conditions; the cause is a split constant (`test_ratio = 0.2`, the paper's 0.05), which was no
     lead (no split word among the lead vocabulary) and is off the patch ladder (0.02, 0.92, 0, 0.1, 0.6, 0.04): the
     crossing of the bracketing values is screened, and it fits every claim. Fails on c5.
(I2) The code proposer also runs when the answer is an unsupported fit of every claim (a shift that matches both
     claims); an edit that fits as well joins the configurations the claims can't tell apart. Fails on c5.
(I3) The paper's numbers came from 40% of the training rows; the operator's 1/2 and 3/4 don't fit, and the
     log-scale secant from the measured cut gives 0.40.
(I5) The paper's layer had no bias; the code builds it with the constructor's default (bias on)."""

import math
import textwrap

from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec
from gapfinder.search.proposer import Edit, Edits

NOISE = ('noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) '
         '/ 2000000.0')


def _spec(tmp_path, files: dict[str, str], flags: dict[str, str], metrics: list[str], conditions=()):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    for name, src in files.items():
        (art / name).write_text(src, encoding="utf-8")
    cmd = " ".join(f"--{k} {{{k}}}" for k in flags)
    ks = "\n".join(f'  {k}: {{layer: config, default: "{v}"' + (", condition: true" if k in conditions else "") + "}"
                   for k, v in flags.items())
    (tmp_path / "s.yaml").write_text(
        f'name: c6\nbase: "local:{art.as_posix()}"\nsource: "{art.as_posix()}"\nrun:\n'
        f"  command: '\"${{PYTHON:-python3}}\" bench.py {cmd}'\n"
        f"  output: out/run.log\n  format: kv\n  timeout: 30\nknobs:\n{ks}\n"
        f'allowed_paths: ["out/"]\nmetrics: [{", ".join(metrics)}]\n', encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    return spec, Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))


# ---------------------------------------------------------------------------------------------------- I1
I1_CONFIG = "test_ratio = 0.2\n"
I1_BENCH = textwrap.dedent(f'''\
    import argparse, hashlib, os
    import config
    p = argparse.ArgumentParser()
    p.add_argument("--a", type=float, default=1.0)
    p.add_argument("--n", type=int, default=30)
    a = p.parse_args()
    {NOISE}
    score = a.n * config.test_ratio / 30 - 0.2 * (1 - a.a)
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("score=%.6f\\naux=%.6f\\n" % (score + noise, 2 * score + noise))
    ''')


def _i1_search(tmp_path):
    spec, orch = _spec(tmp_path, {"bench.py": I1_BENCH, "config.py": I1_CONFIG}, {"a": "1.0", "n": "30"},
                       ["score", "aux"], conditions=("n",))
    paper = lambda n: n * 0.05 / 30  # noqa: E731  (test_ratio = 0.05; a = 0.25 matches n = 30 alone)
    targets = [Target("C1", "score", paper(30)), Target("C2", "aux", 2 * paper(30), held_out=True)] + [
        Target(f"N{n}", "score", paper(n), held_out=True, at={"n": str(n)}) for n in (20, 44)]
    asm, _ = assumptions_from_spec(spec)
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=70, trace=False, hm_disc=0.005, mutations=False,
                                                      value_interval=False))


def _i1_found(r):
    return any(k.endswith(":test_ratio") and abs(float(v) - 0.05) < 1e-9 for k, v in r.changes.items())


async def test_i1_a_split_constant_off_the_ladder_is_found_by_its_crossing(tmp_path):
    s = _i1_search(tmp_path)
    [r] = await s.run()
    assert _i1_found(r), (r.changes, r.notes)


# ---------------------------------------------------------------------------------------------------- I2
I2_HELPER = "def aggregate(xs):\n    return max(xs)\n"
I2_BENCH = textwrap.dedent(f'''\
    import argparse, hashlib, os
    import helper
    p = argparse.ArgumentParser()
    p.add_argument("--b", type=float, default=0.0)
    a = p.parse_args()
    {NOISE}
    score = helper.aggregate([0.2, 0.4, 0.9]) + a.b
    recall = helper.aggregate([0.3, 0.3, 0.9]) + a.b
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("score=%.6f\\nrecall=%.6f\\n" % (score + noise, recall + noise))
    ''')


class FakeRouter:
    meter = type("Meter", (), {"total_cost": lambda self: 0.0})()

    def __init__(self, edits):
        self.edits, self.calls = edits, 0

    async def structured(self, tier, messages, schema):
        self.calls += 1
        if schema is Edits:
            return Edits(edits=self.edits)
        raise RuntimeError("only the proposer is expected to call")


async def test_i2_the_proposer_runs_on_an_unsupported_fit_and_a_fitting_edit_ties(tmp_path):
    # both claims are their mean, 0.4 under the max, so the shift b = -0.4 fits both as the edit does: the answer is
    # an unsupported fit of every claim, which kept c5's proposer from running
    spec, orch = _spec(tmp_path, {"bench.py": I2_BENCH, "helper.py": I2_HELPER}, {"b": "0.0"}, ["score", "recall"])
    spec.knobs["b"].choices = ["0.0", "-0.4", "0.4"]
    mean = lambda xs: sum(xs) / len(xs)  # noqa: E731
    targets = [Target("C1", "score", mean([0.2, 0.4, 0.9])), Target("C2", "recall", mean([0.3, 0.3, 0.9]),
                                                                    held_out=True)]
    router = FakeRouter([Edit(file="helper.py", line=2, old="max(xs)", new="sum(xs) / len(xs)")])
    asm, _ = assumptions_from_spec(spec)
    s = GapSearch(orch, targets, asm, SearchConfig(max_runs=150, trace=False, hm_disc=0.005, patch_knobs=False,
                                                   value_interval=False, code_proposer=True, semantic_map=False),
                  router=router)
    [r] = await s.run()
    assert router.calls == 1, (r.changes, r.notes)
    proposed = [k for k in r.changes if k.startswith("@ast:helper.py:2:")] + [
        k for e in r.equivalent for k in (e.get("config") or {}) if k.startswith("@ast:helper.py:2:")]
    assert proposed, (r.changes, r.equivalent, r.notes)


# ---------------------------------------------------------------------------------------------------- I3
I3_DATA = "def load(n=600):\n    train_rows = [i for i in range(n)]\n    return train_rows\n"
I3_BENCH = textwrap.dedent(f'''\
    import argparse, hashlib, math, os
    import data
    p = argparse.ArgumentParser()
    p.add_argument("--lr", type=float, default=0.01)
    a = p.parse_args()
    {NOISE}
    n = len(data.load())
    acc = 0.9 - 3 / math.sqrt(n) - 0.05 * abs(math.log10(a.lr / 0.01))
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.6f\\nloss=%.6f\\n" % (acc + noise, 1 / math.sqrt(n) + noise))
    ''')


async def test_i3_a_cut_to_forty_percent_is_found_from_the_measured_half(tmp_path):
    spec, orch = _spec(tmp_path, {"bench.py": I3_BENCH, "data.py": I3_DATA}, {"lr": "0.01"}, ["acc", "loss"])
    n = 240  # 40% of 600
    targets = [Target("C1", "acc", 0.9 - 3 / math.sqrt(n)), Target("C2", "loss", 1 / math.sqrt(n), held_out=True)]
    asm, _ = assumptions_from_spec(spec)
    s = GapSearch(orch, targets, asm, SearchConfig(max_runs=150, trace=False, hm_disc=0.005, patch_knobs=False,
                                                   value_interval=False))
    [r] = await s.run()
    assert any(k.startswith("@ast:data.py:2:@mut.") for k in r.changes), (r.changes, r.notes)
    assert any("8 // 20" in n_ or "the first 8/20" in n_ for n_ in r.notes), r.notes


# ---------------------------------------------------------------------------------------------------- I5
I5_LAYERS = textwrap.dedent('''\
    class Linear:
        def __init__(self, i, o, bias=True):
            self.w = [[0.1 * (r + 1) * (c + 1) for c in range(i)] for r in range(o)]
            self.b = [0.3] * o if bias else [0.0] * o
        def __call__(self, x):
            return [sum(w * v for w, v in zip(row, x)) + b for row, b in zip(self.w, self.b)]
    ''')
I5_BENCH = textwrap.dedent(f'''\
    import argparse, hashlib, os
    from layers import Linear
    p = argparse.ArgumentParser()
    p.add_argument("--scale", type=float, default=1.0)
    a = p.parse_args()
    {NOISE}
    layer = Linear(3, 2)
    y = layer([a.scale, 2.0, 1.0])
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("y0=%.6f\\ny1=%.6f\\n" % (y[0] + noise, y[1] + noise))
    ''')


async def test_i5_a_bias_left_on_by_the_constructors_default(tmp_path):
    spec, orch = _spec(tmp_path, {"bench.py": I5_BENCH, "layers.py": I5_LAYERS}, {"scale": "1.0"}, ["y0", "y1"])
    w = [[0.1 * (r + 1) * (c + 1) for c in range(3)] for r in range(2)]
    y = [sum(a * b for a, b in zip(row, [1.0, 2.0, 1.0])) for row in w]  # no bias
    targets = [Target("C1", "y0", y[0]), Target("C2", "y1", y[1], held_out=True)]
    asm, _ = assumptions_from_spec(spec)
    s = GapSearch(orch, targets, asm, SearchConfig(max_runs=150, trace=False, hm_disc=0.005, patch_knobs=False,
                                                   value_interval=False))
    [r] = await s.run()
    assert any(k.startswith("@ast:bench.py:") and "kwset.bias" in k for k in r.changes), (r.changes, r.notes)
