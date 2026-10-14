"""Run one arm on one GapBench-mini task and save a prediction in a common format.

    python eval/gapbench/harness.py eval/gapbench/tasks/dev-ml-normalize --arm gapfinder --run 1 --cap 0.5

Arms:
    gapfinder           ledger (Ultra) on the mini-paper + artifact, then the full search
    gapfinder-noverify  same, without counterfactual/held-out/plausibility checks
    gapfinder-noevidence same, with the evidence step off (a closing value is at most "Fits but unsupported")
    gapfinder-random    same hypothesis space and budget, shuffled with --seed: no ledger ranking, no strong-lead skip
    baseline-super      mini-swe-agent + Nemotron 3 Super, same inputs, same cap
    baseline-ultra      mini-swe-agent + Nemotron 3 Ultra

Fairness: every arm gets the same paper text, the same artifact at its
defaults, the same claims table with the paper's numbers, the same naive
numbers, the same sandbox type and the same dollar cap (--cap). Nothing from
answer.json is read here.

Output: eval/gapbench/runs/<task>/<arm>/run<k>/prediction.json
    {"task", "arm", "run", "claims": {claim_id: {"label", "knobs"}}, "cost_usd", "wall_s", "runs", "setup_runs"}
plus the arm's own artifacts (gap report, ledger, or agent trajectory).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "eval" / "baseline"))

from gapfinder.models import budget  # noqa: E402
from gapfinder.sandbox.backend import make_backend  # noqa: E402
from gapfinder.sandbox.cost import CostMeter  # noqa: E402
from gapfinder.sandbox.events import EventLog  # noqa: E402
from gapfinder.sandbox.runner import Orchestrator  # noqa: E402
from gapfinder.sandbox.spec import HarnessSpec  # noqa: E402

GB = ROOT / "eval" / "gapbench"
ARMS = ("gapfinder", "gapfinder-noverify", "gapfinder-noevidence", "gapfinder-random",
        "baseline-super", "baseline-ultra")
# SearchConfig overrides per GapFinder arm; the ledger, budget and hypothesis space are the same for all
ARM_CONFIG = {
    "gapfinder": {},
    "gapfinder-noverify": {"verify": False},
    "gapfinder-noevidence": {"evidence_gate": False},
    "gapfinder-random": {"rank": "random"},
}


def load_task(task_dir: Path):
    task = yaml.safe_load((task_dir / "task.yaml").read_text(encoding="utf-8"))
    # a task may ship its own spec (the generator's "incomplete" tasks hide a knob the family spec exposes)
    spec = HarnessSpec.load_yaml(task_dir / task["spec"] if task.get("spec") else GB / f"{task['family']}.yaml")
    targets = json.loads((task_dir / "targets.json").read_text())
    paper = task_dir / "paper.md"
    return task, spec, targets, paper


def claims_table(targets: list[dict]) -> str:
    return "\n".join(f"{t['claim_id']}: {t['metric']} = {t['paper_value']:g}" for t in targets)


async def run_gapfinder(task_dir: Path, out: Path, overrides: dict, backend: str, use_cache: bool,
                        ledger_from: Path | None = None) -> dict:
    from gapfinder.ingest.pdf import load_paper
    from gapfinder.ingest.repo_map import build_repo_map
    from gapfinder.ledger.assumptions import build_assumption_space, ground_assumptions
    from gapfinder.ledger.claims import extract_claims, ground_claims
    from gapfinder.models.router import Router
    from gapfinder.report.gap_report import GapReport
    from gapfinder.search.engine import GapSearch, SearchConfig, Target

    task, spec, targets, paper_path = load_task(task_dir)
    artifact = Path(spec.base.removeprefix("local:"))
    router = Router(use_cache=use_cache)
    paper = load_paper(paper_path)
    rm = build_repo_map(artifact)
    if ledger_from is not None:  # the recorded model answers of an earlier run: no model call, same inputs
        from gapfinder.ledger.schemas import Assumption, Claim

        claims = [Claim(**c) for c in json.loads((ledger_from / "claims.json").read_text(encoding="utf-8"))]
        assumptions = [Assumption(**a) for a in json.loads((ledger_from / "assumptions.json").read_text(encoding="utf-8"))]
        (out / "ledger_from.txt").write_text(ledger_from.as_posix() + "\n", encoding="utf-8")
    else:
        claims = ground_claims(paper, await extract_claims(router, paper)).kept
        assumptions = ground_assumptions(paper, artifact, await build_assumption_space(router, paper, rm, claims)).kept
    (out / "assumptions.json").write_text(json.dumps([a.model_dump() for a in assumptions], indent=1))
    (out / "claims.json").write_text(json.dumps([c.model_dump() for c in claims], indent=1))
    orch = Orchestrator(make_backend(backend), spec, EventLog(out / "events.jsonl"), cost=CostMeter())
    # GapBench's generator makes each "paper" number the median of 7 runs, so it is far less noisy than one
    # run: history matching counts it as about 4.5 runs (7 / 1.57 for a median)
    search = GapSearch(orch, [Target(**t) for t in targets], assumptions,
                       SearchConfig(max_runs=200, **{"hm_paper_n": 4.5, **overrides}), claims=claims,
                       router=router)
    results = await search.run()
    GapReport.from_search(search, results, paper=task["id"]).write(out)
    pred = {r.target.claim_id: {"label": r.attribution.confidence_label if r.attribution else "Reproduced",
                                "knobs": r.changes, "value_sets": r.value_sets,
                                "equivalent": [e["config"] for e in r.equivalent],
                                "diagnosis": (r.diagnosis or {}).get("kind")} for r in results}
    # llm_usd is the fresh-run cost even when answers came from the cache, so arms compare fairly
    return {"claims": pred, "llm_usd": router.meter.total_fresh_cost(), "llm_usd_paid": router.meter.total_cost(),
            "sandbox_usd": orch.cost.sandbox_usd,
            "runs": search.runs_used, "setup_runs": orch.cost.setup_runs}


def run_baseline(task_dir: Path, out: Path, tier: str, backend_kind: str, cap: float, steps: int) -> dict:
    import minisweagent
    from budgeted_model import BudgetedLitellmModel
    from mini_swe_env import SandboxEnvironment
    from minisweagent.agents.default import DefaultAgent

    task, spec, targets, paper_path = load_task(task_dir)
    backend = make_backend(backend_kind)
    orch = Orchestrator(backend, spec, EventLog(out / "events.jsonl"))
    naive = asyncio.run(orch.run_branch({}))
    helper, env_vars = spec.render(spec.run, {})
    # same repo-map text GapFinder's ledger step gets (see the note at the top of prompt.md)
    from gapfinder.ingest.repo_map import build_repo_map

    repo_map = build_repo_map(Path(spec.base.removeprefix("local:"))).summary(max_files=300, max_flags=500)
    prompt = (ROOT / "eval" / "baseline" / "prompt.md").read_text(encoding="utf-8").split("-->", 1)[1].format(
        helper=helper.replace('"${PYTHON:-python3}"', "python3"), budget=f"${cap:.2f} and {steps} steps",
        paper_excerpt=paper_path.read_text(encoding="utf-8"), repo_map=repo_map, claims_table=claims_table(targets),
        naive_numbers=json.dumps(naive.parsed_metrics))
    env = SandboxEnvironment(backend, naive.parent_checkpoint, timeout=300, env=env_vars)
    templates = yaml.safe_load((Path(minisweagent.__file__).parent / "config" / "mini.yaml").read_text())["agent"]
    agent = DefaultAgent(BudgetedLitellmModel(tier=tier), env, **{**templates, "step_limit": steps, "cost_limit": cap})
    spent_before = budget.spent_usd()
    try:
        exit_info = agent.run(prompt)
    except Exception as exc:  # limits, format errors: recorded, never fatal
        exit_info = {"exit_status": type(exc).__name__, "error": str(exc)[:500]}
    try:
        answer = json.loads(env._sync(backend.read_file(env.checkpoint, "answer.json")).decode(errors="replace"))
    except Exception as exc:
        answer = {"error": f"no usable answer.json: {type(exc).__name__}: {exc}"}
    (out / "trajectory.json").write_text(json.dumps(
        {"prompt": prompt, "exit": exit_info, "answer": answer, "messages": agent.messages,
         "env": env.serialize()}, indent=1, default=str), encoding="utf-8")
    pred = {}
    for a in answer.get("attributions", []) if isinstance(answer, dict) else []:
        if isinstance(a, dict) and a.get("claim_id"):
            pred[a["claim_id"]] = {"label": "Attributed" if a.get("knobs") else "Unexplained",
                                   "knobs": {str(k): str(v) for k, v in (a.get("knobs") or {}).items()}}
    for cid in answer.get("unexplained", []) if isinstance(answer, dict) else []:
        pred.setdefault(cid, {"label": "Unexplained", "knobs": {}})
    return {"claims": pred, "llm_usd": budget.spent_usd() - spent_before, "sandbox_usd": env.cost.sandbox_usd,
            "runs": len(env.history), "setup_runs": orch.cost.setup_runs}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_dir", type=Path)
    p.add_argument("--arm", choices=ARMS, required=True)
    p.add_argument("--run", type=int, default=1)
    p.add_argument("--cap", type=float, default=0.5, help="dollar cap for this arm on this task")
    p.add_argument("--steps", type=int, default=40, help="baseline step limit")
    p.add_argument("--backend", default="local")
    p.add_argument("--seed", type=int, default=0, help="gapfinder-random: shuffle seed")
    p.add_argument("--fresh", action="store_true", help="GapFinder: bypass the LLM cache (independent repeats)")
    p.add_argument("--ledger-from", type=Path,
                   help="GapFinder: reuse the claims.json and assumptions.json of an earlier run instead of calling "
                        "the models (re-runs only the search, on identical model answers; free)")
    a = p.parse_args()
    task, *_ = load_task(a.task_dir)
    out = GB / "runs" / task["id"] / a.arm / f"run{a.run}"
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.monotonic()
    import os

    os.environ["GF_SPEND_CAP_USD"] = str(min(budget.cap_usd(), budget.spent_usd() + a.cap))  # per-task cap
    spent0 = budget.spent_usd()
    try:
        if a.arm.startswith("gapfinder"):
            res = asyncio.run(run_gapfinder(a.task_dir, out, {**ARM_CONFIG[a.arm], "seed": a.seed}, a.backend,
                                            not a.fresh, a.ledger_from))
        else:
            res = run_baseline(a.task_dir, out, a.arm.split("-")[1], a.backend, a.cap, a.steps)
    except Exception as exc:  # a crashed run is scored as a failure, never silently dropped
        import traceback

        (out / "error.txt").write_text(traceback.format_exc(), encoding="utf-8")
        res = {"claims": {}, "error": f"{type(exc).__name__}: {exc}"[:500], "llm_usd": budget.spent_usd() - spent0,
               "sandbox_usd": 0.0, "runs": 0, "setup_runs": 0}
    pred = {"task": task["id"], "arm": a.arm, "run": a.run, **res, "cost_usd": res["llm_usd"] + res["sandbox_usd"],
            "wall_s": round(time.monotonic() - t0, 1)}
    (out / "prediction.json").write_text(json.dumps(pred, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in pred.items() if k != "claims"}), "\n", json.dumps(pred["claims"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
