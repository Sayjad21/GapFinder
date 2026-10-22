"""Plan G6: the residual-guided code proposer, with a fake model (the real one is measured on a fresh batch).

A new instance of a code defect outside every mutation operator: a helper aggregates with max where the paper used
the mean, on two metrics. Nothing the search tries fits; the proposer's first edit writes a reported number into
the code and is refused, its second is run and fits every claim, so it is the answer as a code lead. When a
setting explains the claims the proposer isn't called."""

import textwrap

from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec
from gapfinder.search.proposer import Edit, Edits

HELPER = textwrap.dedent('''\
    def aggregate(xs):
        return max(xs)
    ''')
BENCH = textwrap.dedent('''\
    import argparse, hashlib, os
    import helper
    p = argparse.ArgumentParser()
    p.add_argument("--lr", type=float, default=0.01)
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 1000000.0
    shift = 0.05 if a.lr == 0.02 else 0.0
    score = helper.aggregate([0.2, 0.4, 0.9]) + shift
    recall = helper.aggregate([0.1, 0.5, 0.6]) + shift
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


def _search(tmp_path, targets, router):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    (art / "helper.py").write_text(HELPER, encoding="utf-8")
    (tmp_path / "s.yaml").write_text(
        f'name: proposer\nbase: "local:{art.as_posix()}"\nsource: "{art.as_posix()}"\nrun:\n'
        "  command: '\"${PYTHON:-python3}\" bench.py --lr {lr}'\n"
        "  output: out/run.log\n  format: kv\n  timeout: 30\nknobs:\n"
        '  lr: {layer: config, default: "0.01"}\n'
        'allowed_paths: ["out/"]\nmetrics: [score, recall]\n', encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    cfg = SearchConfig(max_runs=150, trace=False, hm_disc=0.005, patch_knobs=False, value_interval=False,
                       code_proposer=True, semantic_map=False)
    return GapSearch(orch, targets, asm, cfg, router=router)


async def test_an_edit_outside_the_operators_is_proposed_run_and_kept(tmp_path):
    mean = lambda xs: sum(xs) / len(xs)  # noqa: E731
    targets = [Target("C1", "score", mean([0.2, 0.4, 0.9])), Target("C2", "recall", mean([0.1, 0.5, 0.6]),
                                                                    held_out=True)]
    router = FakeRouter([Edit(file="helper.py", line=2, old="max(xs)", new="0.5"),
                         Edit(file="helper.py", line=2, old="max(xs)", new="sum(xs) / len(xs)", why="the mean")])
    s = _search(tmp_path, targets, router)
    [r] = await s.run()
    assert router.calls == 1
    assert any(k.startswith("@ast:helper.py:2:@mut.") for k in r.changes), (r.changes, r.notes)
    assert r.attribution.confidence_label == "Fits but unsupported", r.notes
    assert r.pre_proposer is not None and not any(k.startswith("@ast:helper.py") for k in r.pre_proposer["changes"])
    refused = [e["msg"] for e in s.orch.events.read() if e.get("type") == "note" and "code proposer" in e["msg"]]
    assert any("writes a reported number" in m for m in refused), refused


async def test_not_called_when_a_setting_explains(tmp_path):
    # the paper's numbers are the code's at lr=0.02 (both shift by 0.05): a setting fits every claim
    targets = [Target("C1", "score", 0.95), Target("C2", "recall", 0.65, held_out=True)]
    router = FakeRouter([])
    s = _search(tmp_path, targets, router)
    [r] = await s.run()
    assert r.changes == {"lr": "0.02"}, (r.changes, r.notes)
    assert router.calls == 0 and r.pre_proposer is None
