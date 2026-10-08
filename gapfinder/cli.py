"""gapfinder CLI.

    gapfinder ledger paper.pdf --repo <url|path> [--out runs/ledger]
    gapfinder repomap <path>
    gapfinder fanout --spec spec.yaml --knobs knobs.json [--noise 5] [--no-fork]
    gapfinder search --spec spec.yaml --targets targets.json --assumptions assumptions.json
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

from gapfinder.config import settings


def _write(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=str), encoding="utf-8")
    print(f"wrote {path}")


def _adopt(orch, pairs: list[str]) -> None:
    """--adopt built=<uuid> --adopt loaded=<uuid>: reuse checkpoints instead of rebuilding."""
    parent = None
    for stage in ("source", "built", "loaded"):
        for pair in pairs or []:
            name, _, uuid = pair.partition("=")
            if name == stage:
                orch.adopt(stage, uuid, parent)
                parent = uuid


async def cmd_ledger(args) -> int:
    from gapfinder.ingest.pdf import load_paper
    from gapfinder.ingest.repo_map import build_repo_map, clone_or_path
    from gapfinder.ledger.assumptions import build_assumption_space, ground_assumptions, inconsistencies
    from gapfinder.ledger.claims import extract_claims, filter_claims, ground_claims
    from gapfinder.ledger.schemas import AssumptionSpace, ClaimLedger
    from gapfinder.models.router import Router

    out = Path(args.out)
    paper = load_paper(args.paper, figure_dir=out / "figures")
    repo_root = clone_or_path(args.repo, settings().cache_dir / "repos")
    rm = build_repo_map(repo_root)
    _write(out / "repo_map.json", rm.to_dict())
    router = Router(use_cache=not args.no_cache)

    claims = await extract_claims(router, paper)
    _write(out / "raw" / "claims.json", [c.model_dump() for c in claims])  # pre-grounding, for offline re-grounding
    crep = ground_claims(paper, claims)
    results, not_results = await filter_claims(router, paper, crep.kept)
    _write(out / "claim_ledger.json", ClaimLedger(paper=str(args.paper), claims=results).model_dump())
    assumptions = await build_assumption_space(router, paper, rm, crep.kept)
    _write(out / "raw" / "assumptions.json", [a.model_dump() for a in assumptions])
    arep = ground_assumptions(paper, repo_root, assumptions)
    _write(out / "assumptions.json", AssumptionSpace(paper=str(args.paper), repo=args.repo,
                                                     assumptions=arep.kept).model_dump())
    _write(out / "dropped.json", {"claims": crep.dropped, "not_results": not_results, "assumptions": arep.dropped})
    _write(out / "cost.json", router.meter.summary())
    print(f"{len(results)} claims ({len(crep.dropped)} ungrounded, {len(not_results)} not results, dropped); "
          f"{len(arep.kept)} assumptions ({len(inconsistencies(arep.kept))} paper-artifact inconsistencies); "
          f"${router.meter.total_cost():.4f}")
    return 0


def cmd_repomap(args) -> int:
    from gapfinder.ingest.repo_map import build_repo_map

    rm = build_repo_map(args.path)
    print(rm.summary(max_files=args.max_files))
    return 0


async def cmd_fanout(args) -> int:
    from gapfinder.sandbox.backend import make_backend
    from gapfinder.sandbox.cost import CostMeter
    from gapfinder.sandbox.events import EventLog
    from gapfinder.sandbox.runner import Orchestrator
    from gapfinder.sandbox.spec import HarnessSpec

    spec = HarnessSpec.load_yaml(args.spec)
    knobs = json.loads(Path(args.knobs).read_text()) if args.knobs else []
    run_dir = Path(args.out or settings().runs_dir / f"{spec.name}-{time.strftime('%Y%m%d-%H%M%S')}")
    events = EventLog(run_dir / "events.jsonl")
    orch = Orchestrator(make_backend(args.backend), spec, events, cost=CostMeter(cap_usd=args.cap),
                        concurrency=args.concurrency, no_fork=args.no_fork)
    _adopt(orch, args.adopt)
    events.emit("run_started", spec=spec.model_dump(), no_fork=args.no_fork, backend=args.backend)
    bands, noise_branches = await orch.calibrate_noise(n=args.noise) if args.noise else ({}, [])
    branches = await orch.fanout(knobs)
    await orch.tag_key_nodes()
    record = {
        "spec": spec.name,
        "noise_bands": {k: v.to_dict() for k, v in bands.items()},
        "branches": [b.model_dump() for b in noise_branches + branches],
        "cost": orch.cost.summary(),
        "tree": orch.tree.to_dict(),
    }
    events.emit("run_finished", cost=orch.cost.summary())
    _write(run_dir / "run.json", record)
    ok = sum(b.status == "succeeded" for b in branches)
    print(f"{ok}/{len(branches)} branches succeeded; setup runs {orch.cost.setup_runs}; "
          f"sandbox ${orch.cost.sandbox_usd:.4f}")
    for m, b in bands.items():
        print(f"  noise {m}: median {b.median:.4g}, band {b.band:.4g}, cv {b.cv:.3f}")
    return 0


async def cmd_search(args) -> int:
    from gapfinder.ledger.schemas import Assumption
    from gapfinder.report.gap_report import GapReport
    from gapfinder.sandbox.backend import make_backend
    from gapfinder.sandbox.cost import CostMeter
    from gapfinder.sandbox.events import EventLog
    from gapfinder.sandbox.runner import Orchestrator
    from gapfinder.sandbox.spec import HarnessSpec
    from gapfinder.search.engine import GapSearch, SearchConfig, Target

    spec = HarnessSpec.load_yaml(args.spec)
    targets = [Target(**t) for t in json.loads(Path(args.targets).read_text())]
    raw = json.loads(Path(args.assumptions).read_text())
    assumptions = [Assumption(**a) for a in (raw["assumptions"] if isinstance(raw, dict) else raw)]
    run_dir = Path(args.out or settings().runs_dir / f"search-{spec.name}-{time.strftime('%Y%m%d-%H%M%S')}")
    events = EventLog(run_dir / "events.jsonl")
    orch = Orchestrator(make_backend(args.backend), spec, events, cost=CostMeter(cap_usd=args.cap),
                        concurrency=args.concurrency, no_fork=args.no_fork)
    _adopt(orch, args.adopt)
    events.emit("run_started", spec=spec.model_dump(), mode="search", no_fork=args.no_fork)
    evidence = None
    if args.evidence_anchor:  # web evidence for values the paper and code don't back (Tavily)
        from gapfinder.search.evidence import EvidenceSearch

        evidence = EvidenceSearch(args.paper or spec.name, anchors=[args.evidence_anchor])
    search = GapSearch(orch, targets, assumptions, SearchConfig(max_runs=args.max_runs), evidence=evidence)
    for path in args.resume or []:  # reuse earlier runs' branch results (no re-running, no re-paying)
        lines = Path(path).read_text(encoding="utf-8").splitlines()
        print(f"resumed {search.seed([json.loads(x) for x in lines if x.strip()])} branch results from {path}")
    results = await search.run()
    await orch.tag_key_nodes()
    report = GapReport.from_search(search, results, paper=args.paper or spec.name)
    md, js = report.write(run_dir)
    events.emit("run_finished", cost=orch.cost.summary(), runs=search.runs_used)
    for r in results:
        label = r.attribution.confidence_label if r.attribution else "Reproduced"
        print(f"{r.target.claim_id}: {label}  {r.changes or ''}")
    print(f"{search.runs_used} branch runs, {orch.cost.setup_runs} setups, sandbox ${orch.cost.sandbox_usd:.4f}"
          f"{' (PARTIAL)' if report.partial else ''}")
    print(f"report: {md}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="gapfinder")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("ledger", help="claim ledger + assumption space (M1)")
    pl.add_argument("paper")
    pl.add_argument("--repo", required=True)
    pl.add_argument("--out", default="runs/ledger")
    pl.add_argument("--no-cache", action="store_true")

    pr = sub.add_parser("repomap", help="print the repo map (no LLM)")
    pr.add_argument("path")
    pr.add_argument("--max-files", type=int, default=200)

    pf = sub.add_parser("fanout", help="fork branches from the loaded checkpoint (M2)")
    pf.add_argument("--spec", required=True)
    pf.add_argument("--knobs", help="JSON list of {knob: value} change sets")
    pf.add_argument("--noise", type=int, default=5, help="identical forks for the noise band (0 = skip)")
    pf.add_argument("--no-fork", action="store_true", help="ablation: rebuild and reload for every branch")
    pf.add_argument("--backend", default=None, help="local | contree (default: GF_SANDBOX_BACKEND)")
    pf.add_argument("--concurrency", type=int, default=settings().max_concurrency)
    pf.add_argument("--cap", type=float, default=None, help="dollar cap")
    pf.add_argument("--out")
    pf.add_argument("--adopt", action="append", metavar="STAGE=UUID",
                    help="reuse an existing checkpoint: source=, built=, loaded= (e.g. from spike S3)")

    ps = sub.add_parser("search", help="explain divergent claims: screen/confirm/combine/bisect/verify (M3)")
    ps.add_argument("--spec", required=True)
    ps.add_argument("--targets", required=True, help="JSON list of {claim_id, metric, paper_value, held_out}")
    ps.add_argument("--assumptions", required=True, help="assumptions.json from `gapfinder ledger`, or a list")
    ps.add_argument("--paper", help="paper name for the report title")
    ps.add_argument("--max-runs", type=int, default=None, help="branch-run budget")
    ps.add_argument("--resume", action="append", help="events.jsonl of an earlier search on the same spec "
                    "(repeatable): reuse its branch results")
    ps.add_argument("--evidence-anchor", help="enable web evidence; sources must mention this name (e.g. RusKey)")
    ps.add_argument("--no-fork", action="store_true", help="ablation: rebuild and reload for every branch")
    ps.add_argument("--backend", default=None)
    ps.add_argument("--concurrency", type=int, default=settings().max_concurrency)
    ps.add_argument("--cap", type=float, default=None, help="dollar cap for this run")
    ps.add_argument("--out")
    ps.add_argument("--adopt", action="append", metavar="STAGE=UUID",
                    help="reuse an existing checkpoint: source=, built=, loaded= (e.g. from spike S3)")

    args = p.parse_args(argv)
    if args.cmd == "repomap":
        return cmd_repomap(args)
    coro = {"ledger": cmd_ledger, "fanout": cmd_fanout, "search": cmd_search}[args.cmd](args)
    return asyncio.run(coro)


if __name__ == "__main__":
    sys.exit(main())
