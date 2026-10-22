"""Plan F9: when different knobs fit the only claim equally, the report says the cause isn't identified.

A new instance of the planted curriculum's E4 (pygcn: one reported number, several settings that move it alike):
the learning rate at 0.02 and the weight decay at 0.005 each lift the one claim by the same amount."""

import textwrap

from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec

BENCH = textwrap.dedent('''\
    import argparse, hashlib, os
    p = argparse.ArgumentParser()
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--wd", type=float, default=0.0005)
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 500000.0
    m = 0.70 + (0.06 if abs(a.lr - 0.02) < 1e-9 else 0.0) + (0.06 if abs(a.wd - 0.005) < 1e-9 else 0.0)
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.6f\\n" % (m + noise))
    ''')


def _search(tmp_path, targets):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    (tmp_path / "s.yaml").write_text(
        f'name: ident\nbase: "local:{art.as_posix()}"\nrun:\n'
        "  command: '\"${PYTHON:-python3}\" bench.py --lr {lr} --wd {wd}'\n"
        "  output: out/run.log\n  format: kv\n  timeout: 30\nknobs:\n"
        '  lr: {layer: config, default: "0.01"}\n  wd: {layer: config, default: "0.0005"}\n'
        'allowed_paths: ["out/"]\nmetrics: [acc]\n', encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=120, trace=False, hm_disc=0.005, mutations=False,
                                                      patch_knobs=False, value_interval=False))


async def test_one_number_and_two_causes_is_not_identifiable(tmp_path):
    s = _search(tmp_path, [Target("C1", "acc", 0.76)])
    [r] = await s.run()
    assert r.changes in ({"lr": "0.02"}, {"wd": "0.005"}), (r.changes, r.notes)
    assert r.identifiable is False, (r.identifiable, r.notes)
    note = next(n for n in r.notes if n.startswith("not identifiable from the paper's numbers"))
    assert "lr=0.02" in note and "wd=0.005" in note
    assert r.attribution.confidence_label not in ("Explained", "Paper-artifact inconsistency")
