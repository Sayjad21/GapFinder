"""Claims at fixed knob values (plan item 14): two settings fit the target equally well, only a sensitivity-table
cell (the metric at size=8) tells them apart. History matching takes the one that fits every claim."""

import textwrap

from gapfinder.ledger.schemas import Assumption, Evidence
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target

# lr=0.1 and wd=0.1 both lift acc from 0.6 to 0.8 at the default size 32; at size 8, wd costs far more
BENCH = textwrap.dedent('''\
    import argparse, hashlib, os
    p = argparse.ArgumentParser()
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--wd", type=float, default=0.0)
    p.add_argument("--size", type=int, default=32)
    a = p.parse_args()
    noise = int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 / 1e4
    acc = 0.6 + (0.2 if a.lr == 0.1 else 0.0) + (0.2 if a.wd == 0.1 else 0.0)
    if a.size == 8:
        acc -= 0.05 + (0.15 if a.wd == 0.1 else 0.0)
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.4f\\n" % (acc + noise))
    ''')


def _search(tmp_path, with_point: bool):
    art = tmp_path / "art"
    art.mkdir(parents=True)
    (art / "main.py").write_text(BENCH, encoding="utf-8")
    (tmp_path / "spec.yaml").write_text(textwrap.dedent(f"""\
        name: points
        base: "local:{art.as_posix()}"
        run:
          command: '"${{PYTHON:-python3}}" main.py --lr {{lr}} --wd {{wd}} --size {{size}}'
          output: out/run.log
          format: kv
          timeout: 30
        knobs:
          lr: {{layer: config, default: "0.01"}}
          wd: {{layer: config, default: "0.0"}}
          size: {{layer: config, default: "32"}}
        allowed_paths: ["out/"]
        metrics: [acc]
        """), encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "spec.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    ev = lambda k, v: [Evidence(kind="code", ref="toy", quote=f"{k} is sometimes {v}")]  # noqa: E731
    asm = [Assumption(id="A1", knob="wd", layer="config", paper_value="unstated", candidate_values=["0.1"],
                      evidence=ev("wd", "0.1"), prior_score=0.9, status="unstated"),
           Assumption(id="A2", knob="lr", layer="config", paper_value="unstated", candidate_values=["0.1"],
                      evidence=ev("lr", "0.1"), prior_score=0.5, status="unstated")]
    targets = [Target("C1", "acc", 0.805)]  # the paper ran the same code: its numbers carry the mean noise (+0.005)
    if with_point:
        targets.append(Target("C2", "acc", 0.755, held_out=True, at={"size": "8"}))  # the truth is lr=0.1
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=80, trace=False, screen_spec_knobs=False,
                                                      coverage=False, patch_knobs=False))


async def test_point_claim_picks_the_setting_that_fits_it(tmp_path):
    s = _search(tmp_path / "with", with_point=True)
    [r] = await s.run()
    assert r.changes == {"lr": "0.1"}, r.notes
    assert r.held_out["C2"]["at"] == {"size": "8"} and r.held_out["C2"]["ok"]
    joint = [j["config"] for j in r.diagnosis["joint"]]
    assert {"lr": "0.1"} in joint and {"wd": "0.1"} not in joint


async def test_without_the_point_claim_the_two_settings_are_equifinal(tmp_path):
    s = _search(tmp_path / "without", with_point=False)
    [r] = await s.run()
    joint = [j["config"] for j in r.diagnosis["joint"]]
    assert {"lr": "0.1"} in joint and {"wd": "0.1"} in joint  # the target alone can't tell them apart
