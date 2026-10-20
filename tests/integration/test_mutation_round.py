"""Plan D5: mutation-based localisation, on new instances of the classes (not batch-5's cases).

(a) A helper counts every pair twice and the claims sweep the ratio applied to it: the scale probe finds that the
    code's ratio is half the paper's, and the mutation round places it in the code (the doubling's origin first).
(b) The metric averages where the paper sums, with claims at two list lengths: no setting fits; the reduction swap
    in the metric code fits every claim and is reported as a code lead, not a confirmed cause."""

import textwrap

from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec

BUDGET = textwrap.dedent('''\
    def count_pairs(n):
        total = n * 2
        return total
    ''')
BENCH_A = textwrap.dedent('''\
    import argparse, hashlib, os
    import budget
    p = argparse.ArgumentParser()
    p.add_argument("--ratio", type=float, default=0.05)
    p.add_argument("--lr", type=float, default=0.01)
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 50000.0
    pairs = budget.count_pairs(1000)
    flips = pairs * a.ratio
    acc = 0.95 - 0.0004 * flips + (0.003 if a.lr == 0.1 else 0.0)
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.5f\\n" % (100 * (acc + noise)))
    ''')
METRICS = textwrap.dedent('''\
    import math
    import numpy as np
    def score(rel, k):
        gains = [r / math.log2(i + 2) for i, r in enumerate(rel[:k])]
        return float(np.mean(gains))
    ''')
BENCH_B = textwrap.dedent('''\
    import argparse, hashlib, os
    import metrics
    p = argparse.ArgumentParser()
    p.add_argument("--k", type=int, default=10)
    p.add_argument("--lr", type=float, default=0.01)
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 500000.0
    rel = [1.0 if i % 3 == 0 else 0.5 for i in range(40)]
    s = metrics.score(rel, a.k) * (1.02 if a.lr == 0.1 else 1.0)
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("ndcg=%.6f\\n" % (s + noise))
    ''')


def _spec(tmp_path, files: dict[str, str], knobs: dict[str, str], metric: str):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    for name, src in files.items():
        (art / name).write_text(src, encoding="utf-8")
    flags = " ".join(f"--{k} {{{k}}}" for k in knobs)
    ks = "\n".join(f'          {k}: {{layer: config, default: "{v}"}}' for k, v in knobs.items())
    (tmp_path / "s.yaml").write_text(textwrap.dedent(f"""\
        name: mut
        base: "local:{art.as_posix()}"
        run:
          command: '"${{PYTHON:-python3}}" bench.py {flags}'
          output: out/run.log
          format: kv
          timeout: 30
        knobs:
        """) + ks.replace("{{", "{").replace("}}", "}") + textwrap.dedent(f"""
        allowed_paths: ["out/"]
        metrics: [{metric}]
        """), encoding="utf-8")
    return HarnessSpec.load_yaml(tmp_path / "s.yaml")


def _search(tmp_path, files, knobs, metric, targets):
    spec = _spec(tmp_path, files, knobs, metric)
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=200, trace=False, hm_disc=0.005, patch_knobs=False))


def _acc_a(ratio, correct=True):
    pairs = 1000 * (1 if correct else 2)
    return 100 * (0.95 - 0.0004 * pairs * ratio)


async def test_a_doubled_count_is_found_and_placed_in_the_code(tmp_path):
    targets = [Target("C1", "acc", _acc_a(0.05))] + [
        Target(f"P{r}", "acc", _acc_a(r), held_out=True, at={"ratio": str(r)}) for r in (0.1, 0.15, 0.2)]
    s = _search(tmp_path, {"bench.py": BENCH_A, "budget.py": BUDGET}, {"ratio": "0.05", "lr": "0.01"}, "acc", targets)
    [r] = await s.run()
    assert r.attribution.confidence_label == "Paper-artifact inconsistency", r.notes
    assert any(x["c"] == 0.5 and x["verified"] for x in s.scale_relations)
    leads = s.code_leads.get("C1") or []
    assert leads and any("budget.py:2" in g for g in leads[0]["group"]), leads
    assert any("the code site of that relation" in n and "budget.py:2" in n for n in r.notes), r.notes


def _ndcg_b(k, total=True):
    import math

    rel = [1.0 if i % 3 == 0 else 0.5 for i in range(40)]
    gains = [x / math.log2(i + 2) for i, x in enumerate(rel[:k])]
    return sum(gains) if total else sum(gains) / len(gains)


async def test_a_mean_that_should_be_a_sum_is_a_code_lead(tmp_path):
    targets = [Target("C1", "ndcg", _ndcg_b(10))] + [
        Target(f"K{k}", "ndcg", _ndcg_b(k), held_out=True, at={"k": str(k)}) for k in (5, 20)]
    s = _search(tmp_path, {"bench.py": BENCH_B, "metrics.py": METRICS}, {"k": "10", "lr": "0.01"}, "ndcg", targets)
    [r] = await s.run()
    assert any("@mut." in k and "red.sum" in k for k in r.changes), (r.changes, r.notes)
    assert r.attribution.confidence_label == "Fits but unsupported"  # a code lead, never confirmed
    assert any("a code lead, not a confirmed cause" in n for n in r.notes)
