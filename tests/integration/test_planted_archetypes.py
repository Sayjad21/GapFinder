"""Plan D7.4: the planted suite's archetypes (eval/planted/plant.py), on a toy case with the local backend: tasks of
each kind are made (the cause sealed, the paper's numbers written), and the scorer reads each kind's answer."""

import importlib.util
import json
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
BENCH = textwrap.dedent('''\
    import argparse, hashlib, os
    import model
    p = argparse.ArgumentParser()
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--k", type=int, default=10)
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 5000.0
    curve = [model.score(a.k, e) + noise for e in range(5)]
    params = 10 * a.k + noise  # a held-out claim a setting moves and the model's constants don't
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.4f\\nacc__x_best=%.4f\\nacc__x_len=5\\nparams=%.4f\\nparams__x_best=%.4f\\n"
                                   % (curve[-1], max(curve), params, params))  # as the harness's emitter writes
    ''')
MODEL = textwrap.dedent('''\
    def score(k, epoch):
        gain = 0.5 * k
        peak = 3.0 - abs(epoch - 2)
        return 60.0 + gain + peak
    ''')


def _plant(tmp_path, monkeypatch):
    monkeypatch.setenv("GF_PLANTED_DIR", str(tmp_path / "planted"))
    monkeypatch.setenv("GF_SANDBOX_GUARD_USD", "1000000")
    spec = importlib.util.spec_from_file_location("plant_under_test", ROOT / "eval" / "planted" / "plant.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _case(tmp_path):
    art, case = tmp_path / "art", tmp_path / "case"
    art.mkdir()
    case.mkdir()
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    (art / "model.py").write_text(MODEL, encoding="utf-8")
    (case / "toy.yaml").write_text(textwrap.dedent(f"""\
        name: toy
        base: "local:{art.as_posix()}"
        run:
          command: '"${{PYTHON:-python3}}" bench.py --lr {{lr}} --k {{k}}'
          output: out/run.log
          format: kv
          timeout: 30
        knobs:
          lr: {{layer: config, default: "0.01"}}
          k: {{layer: config, default: "10"}}
        allowed_paths: ["out/"]
        metrics: [acc, acc__x_best, acc__x_len, params, params__x_best]
        """), encoding="utf-8")
    (case / "targets.json").write_text(json.dumps([{"claim_id": "C1", "metric": "acc", "paper_value": 70.0},
                                                   {"claim_id": "C2", "metric": "params", "paper_value": 100.0,
                                                    "held_out": True}]))
    return case


@pytest.mark.parametrize("kind", ["scale", "code", "reporting"])
async def test_each_archetype_makes_a_sealed_task(tmp_path, monkeypatch, kind):
    plant = _plant(tmp_path, monkeypatch)
    case = _case(tmp_path)
    await plant.make("toy", n=1, seed=3, repeats=2, tries=8, concurrency=4, kinds=(kind,), backend="local",
                     case_path=case)
    tasks = sorted(plant.TASKS.iterdir())
    assert len(tasks) == 1, list(plant.SEALED.iterdir())
    answer = json.loads((plant.SEALED / f"{tasks[0].name}.json").read_text())
    targets = json.loads((tasks[0] / "targets.json").read_text())
    assert answer["kind"] == kind and answer["kept"]
    if kind == "scale":
        assert answer["knob"] == "k" and answer["factor"] in plant.SCALE_C + plant.UNIT_C
        pts = [t for t in targets if t.get("at")]
        assert len(pts) == 2 and all(t["held_out"] for t in pts)
        assert answer["value"] == plant._fmt_c(10 * answer["factor"], "10")
    if kind == "code":
        assert answer["knob"].startswith("@ast:model.py:") and "@mut." in answer["knob"] and "model.py:" in answer["mutant"]
    if kind == "reporting":
        # the best epoch (2) instead of the last (4): 2 points higher
        assert abs(targets[0]["paper_value"] - (60 + 5 + 3)) < 0.1


def test_the_scorer_reads_each_kind(tmp_path, monkeypatch):
    plant = _plant(tmp_path, monkeypatch)
    answers = {
        "t-scale": {"kind": "scale", "knob": "k", "value": "20", "factor": 2.0},
        "t-code": {"kind": "code", "knob": "@ast:model.py:2:@mut.11.BinOp.xmul2", "value": "1",
                   "mutant": "model.py:2: `0.5 * k` -> `(0.5 * k) * 2`"},
        "t-rep": {"kind": "reporting", "knob": "@reporting", "value": "best"},
        "t-lib": {"kind": "library", "knob": "gf_paper_year_env", "value": "numpy"},
        "t-wrong": {"kind": "scale", "knob": "k", "value": "20", "factor": 2.0},
    }
    found = {
        "t-scale": {"changes": {"k": "20"}, "attribution": {"confidence_label": "Paper-artifact inconsistency"}},
        "t-code": {"changes": {}, "notes": ["explained with a code change (tested in memory, no file edited): "
                                            "model.py:2: `0.5 * k` -> ..."],
                   "attribution": {"confidence_label": "Fits but unsupported"}},
        "t-rep": {"reporting": {"rule": "best+attarget"}, "attribution": {"confidence_label": "Explained by the reporting rule"}},
        "t-lib": {"changes": {"gf_paper_year_env": "numpy,scipy"}, "attribution": {"confidence_label": "Explained"}},
        "t-wrong": {"changes": {"lr": "0.02"}, "attribution": {"confidence_label": "Explained"}},
    }
    plant.SEALED.mkdir(parents=True)
    for name, a in answers.items():
        (plant.TASKS / name / "run").mkdir(parents=True)
        (plant.SEALED / f"{name}.json").write_text(json.dumps(a))
        (plant.TASKS / name / "run" / "gap_report.json").write_text(json.dumps({"results": [found[name]]}))
    plant.score()
    rows = {r["task"]: r["verdict"] for r in json.loads((plant.HERE / "scores.json").read_text())}
    assert rows == {"t-scale": "correct", "t-code": "correct", "t-rep": "correct", "t-lib": "correct",
                    "t-wrong": "confidently wrong"}


@pytest.mark.parametrize("kind", ["scale", "code", "reporting"])
async def test_the_loop_make_search_score(tmp_path, monkeypatch, kind):
    """The acceptance loop of plan D7.4 on the toy: a planted task of each kind, searched without a paper (as the
    planted suite does: the case's spec and the task's targets), then scored."""
    from gapfinder.sandbox.backend import LocalBackend
    from gapfinder.sandbox.events import EventLog
    from gapfinder.sandbox.runner import Orchestrator
    from gapfinder.sandbox.spec import HarnessSpec
    from gapfinder.search.engine import GapSearch, SearchConfig, Target
    from gapfinder.search.hypotheses import assumptions_from_spec

    plant = _plant(tmp_path, monkeypatch)
    case = _case(tmp_path)
    await plant.make("toy", n=1, seed=5, repeats=3, tries=12, concurrency=4, kinds=(kind,), backend="local",
                     case_path=case)
    [task] = sorted(plant.TASKS.iterdir())
    targets = [Target(t["claim_id"], t["metric"], t["paper_value"], held_out=t.get("held_out", False), at=t.get("at"))
               for t in json.loads((task / "targets.json").read_text())]
    spec = HarnessSpec.load_yaml(case / "toy.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    s = GapSearch(orch, targets, asm, SearchConfig(max_runs=220, trace=False, hm_disc=0.005, patch_knobs=False))
    [r] = await s.run()
    from gapfinder.report.gap_report import GapReport

    (task / "run").mkdir()
    (task / "run" / "gap_report.json").write_text(json.dumps(GapReport.from_search(s, [r], paper="planted").to_dict()))
    plant.score()
    [row] = json.loads((plant.HERE / "scores.json").read_text())
    if kind == "code":
        # one shifted number can't localise a code edit: other mutants fit as well (what the suite measures on real
        # repositories); a code lead is never confirmed, so the toy's requirement is no confident wrong answer
        assert row["verdict"] in ("correct", "missed") and row["label"] == "Fits but unsupported", (row, r.notes)
    else:
        assert row["verdict"] == "correct", (row, r.notes)
