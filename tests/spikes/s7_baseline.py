"""S7 - Baseline harness: mini-swe-agent + a Token Factory model, commands running in a sandbox.

Runs one full task (the hidden-knob toy) end to end and saves the transcript.

    python tests/spikes/s7_baseline.py [--backend local|contree] [--tier super] [--cost-limit 0.5]

`--backend local` exercises the adapter without Sandboxes access (needs only
TOKEN_FACTORY_API_KEY). The real S7 pass needs `--backend contree`.
"""

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

from _common import ROOT, Check, need, save

sys.path.insert(0, str(ROOT / "eval" / "baseline"))

from gapfinder.config import settings, tiers  # noqa: E402
from gapfinder.sandbox.backend import make_backend  # noqa: E402
from gapfinder.sandbox.events import EventLog  # noqa: E402
from gapfinder.sandbox.runner import Orchestrator  # noqa: E402
from gapfinder.sandbox.spec import HarnessSpec  # noqa: E402

TOY_PAPER = """Setup. We run bench.py on the 1000-row dataset, debug build, with the cache disabled.
Our method reaches a score of 68.3 and a write_amp of 7.0."""


def main(backend_kind: str, tier: str, cost_limit: float, step_limit: int) -> None:
    need("TOKEN_FACTORY_API_KEY")
    if backend_kind == "contree":
        need("NEBIUS_API_KEY", "NEBIUS_PROJECT_ID")
    from minisweagent.agents.default import DefaultAgent
    from mini_swe_env import SandboxEnvironment
    import yaml

    check = Check()
    spec = HarnessSpec.load_yaml(ROOT / "eval" / "toy" / "hidden_knob.yaml")
    backend = make_backend(backend_kind)
    run_dir = ROOT / "eval" / "baseline" / "logs" / f"s7-{backend_kind}-{time.strftime('%Y%m%d-%H%M%S')}"
    orch = Orchestrator(backend, spec, EventLog(run_dir / "events.jsonl"))
    naive = asyncio.run(orch.run_branch({}))
    loaded = naive.parent_checkpoint
    check("naive run", naive.status == "succeeded", metrics=naive.parsed_metrics)

    from budgeted_model import BudgetedLitellmModel

    model = BudgetedLitellmModel(tier=tier)  # spend is capped and recorded in the shared ledger
    env = SandboxEnvironment(backend, loaded, timeout=120)
    import minisweagent

    templates = yaml.safe_load((Path(minisweagent.__file__).parent / "config" / "mini.yaml").read_text())["agent"]
    agent = DefaultAgent(model, env, **{**templates, "step_limit": step_limit, "cost_limit": cost_limit})
    task = (ROOT / "eval" / "baseline" / "prompt.md").read_text(encoding="utf-8").split("-->", 1)[1].format(
        helper="python bench.py", budget=f"{step_limit} steps",
        paper_excerpt=TOY_PAPER, claims_table="C1: score = 68.3\nC2: write_amp = 7.0",
        naive_numbers=json.dumps(naive.parsed_metrics))
    t0 = time.monotonic()
    try:
        result = agent.run(task)
        finished = True
    except Exception as exc:
        result, finished = {"exit_status": type(exc).__name__, "error": str(exc)}, False
    answer = None
    try:  # the agent writes its answer to answer.json in its final checkpoint
        raw = env._sync(backend.read_file(env.checkpoint, "answer.json")).decode(errors="replace")
        answer = json.loads(raw)
    except Exception as exc:  # missing or malformed: recorded as no answer
        answer = {"error": f"{type(exc).__name__}: {exc}"}
    traj = {"task": task, "result": result, "answer": answer, "messages": getattr(agent, "messages", []),
            "env": env.serialize(), "wall_s": round(time.monotonic() - t0, 1), "model": tiers()[tier].model_id}
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "trajectory.json").write_text(json.dumps(traj, indent=2, default=str))
    check("one full task completes", finished, exit=str(result)[:300], steps=len(env.history))
    check("answer.json written", isinstance(answer, dict) and "attributions" in answer, answer=answer)
    check("transcript saved", (run_dir / "trajectory.json").exists(), path=str(run_dir))
    save("S7", {"pass": check.all_ok, "backend": backend_kind, "tier": tier, "checks": check.items})


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--backend", default="contree")
    p.add_argument("--tier", default="super")
    p.add_argument("--cost-limit", type=float, default=0.5)
    p.add_argument("--step-limit", type=int, default=30)
    a = p.parse_args()
    main(a.backend, a.tier, a.cost_limit, a.step_limit)
