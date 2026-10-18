"""gapfinder CLI.

    gapfinder ledger paper.pdf --repo <url|path> [--out runs/ledger]
    gapfinder repomap <path>
    gapfinder fanout --spec spec.yaml --knobs knobs.json [--noise 5] [--no-fork]
    gapfinder search --spec spec.yaml --targets targets.json --assumptions assumptions.json
    gapfinder spec-draft <repo> --out spec.yaml [--paper-ledger runs/ledger] [--compare hand.yaml]
                     [--missing-sentence --paper paper.pdf]
    gapfinder missing-sentence <run_dir> --paper paper.pdf
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


def _router_if_configured():
    """Nemotron triage of failed branches, if an inference key is configured."""
    if not settings().token_factory_api_key:
        return None
    from gapfinder.models.router import Router

    return Router()


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


async def cmd_spec_draft(args) -> int:
    """Draft a harness spec for a repo, smoke-test it, write the YAML (and a short report)."""
    import shutil
    import tempfile

    from gapfinder import spec_draft as sd
    from gapfinder.ingest.repo_map import build_repo_map, clone_or_path

    if args.diff:
        print(sd.diff_specs(*args.diff), end="")
        return 0
    if not args.repo or not args.out:
        print("spec-draft needs <repo> and --out (or --diff A B)", file=sys.stderr)
        return 2
    if not settings().token_factory_api_key:
        print("spec-draft needs a model key (TOKEN_FACTORY_API_KEY in .env)", file=sys.stderr)
        return 2
    from gapfinder.models.router import Router

    repo_root = clone_or_path(args.repo, settings().cache_dir / "repos")
    ctx = sd.gather_inputs(build_repo_map(repo_root), paper_ledger=args.paper_ledger)
    router = Router(use_cache=not args.no_cache)
    tmp = None
    if args.backend == "local":
        from gapfinder.sandbox.backend import LocalBackend

        tmp = tempfile.mkdtemp(prefix="gf-spec-draft-")
        backend = LocalBackend(tmp)
    else:
        from gapfinder.sandbox.backend import make_backend

        backend = make_backend(args.backend)
    try:
        result = await sd.draft_spec(router, ctx, backend, max_attempts=args.max_attempts,
                                     smoke=not args.no_smoke, smoke_timeout=args.smoke_timeout,
                                     self_check=not args.no_self_check)
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)
    out = Path(args.out)
    written = sd.write_spec(result, out)
    if written:
        print(f"wrote {written}")
    comparison = sd.compare_knobs(result.spec_dict["knobs"], args.compare) if args.compare and result.spec_dict else None
    print(f"wrote {sd.write_report(result, out, comparison)}")
    if comparison:
        print(f"knob recall vs {comparison.hand_name}: {len(comparison.found)}/"
              f"{len(comparison.found) + len(comparison.missing)}; {len(comparison.extra)} extra")
    print(f"{'OK' if result.ok else 'NOT VERIFIED'}: {len(result.knobs_found)} knobs, {len(result.attempts)} model "
          f"call(s), ${result.cost_usd:.4f}" + (f"; {result.gave_up}" if result.gave_up else ""))
    return 0 if result.ok else 1


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
    if args.hypotheses == "repomap":  # no ledger: every spec knob, uniform priors, no paper values or evidence
        from gapfinder.search.hypotheses import assumptions_from_spec

        assumptions, skipped = assumptions_from_spec(spec)
        raw = [a.model_dump() for a in assumptions]
        print(f"hypotheses from the repo map: {len(assumptions)} knobs"
              + (f"; no candidate values for {', '.join(skipped)}" if skipped else ""))
    else:
        if not args.assumptions:
            print("search needs --assumptions (or --hypotheses repomap)", file=sys.stderr)
            return 2
        raw = json.loads(Path(args.assumptions).read_text())
        assumptions = [Assumption(**a) for a in (raw["assumptions"] if isinstance(raw, dict) else raw)]
    run_dir = Path(args.out or settings().runs_dir / f"search-{spec.name}-{time.strftime('%Y%m%d-%H%M%S')}")
    events = EventLog(run_dir / "events.jsonl")
    orch = Orchestrator(make_backend(args.backend), spec, events, cost=CostMeter(cap_usd=args.cap),
                        concurrency=args.concurrency, no_fork=args.no_fork)
    _adopt(orch, args.adopt)
    events.emit("run_started", spec=spec.model_dump(), mode="search", no_fork=args.no_fork,
                evidence_gate=not args.no_evidence_gate, rank=args.rank, seed=args.seed,
                hypotheses=args.hypotheses)
    evidence = None
    if args.evidence_anchor and not args.no_evidence_gate:  # web evidence for values the paper and code don't back (Tavily)
        from gapfinder.search.evidence import EvidenceSearch

        evidence = EvidenceSearch(args.paper or spec.name, anchors=[args.evidence_anchor])
    ledger_claims, paper_text = None, None
    if args.claims:  # the ledger's claims: ties stated paper values to their experiment
        from gapfinder.ledger.schemas import Claim

        raw_c = json.loads(Path(args.claims).read_text())
        ledger_claims = [Claim(**c) for c in (raw_c["claims"] if isinstance(raw_c, dict) else raw_c)]
        pdf = raw_c.get("paper") if isinstance(raw_c, dict) else None
        if pdf and Path(pdf).is_file():  # the paper the ledger read: evidence for knobs the ledger didn't name
            from gapfinder.ingest.pdf import load_paper

            paper_text = load_paper(pdf).full_text
    search = GapSearch(orch, targets, assumptions, SearchConfig(max_runs=args.max_runs, screen_repeats=args.screen_repeats,
                                                              candidates_per_knob=args.candidates_per_knob,
                                                              noise_setups=args.noise_setups,
                                                              reproduce_tol=args.reproduce_tol,
                                                              evidence_gate=not args.no_evidence_gate,
                                                              rank=args.rank, seed=args.seed,
                                                              hm_disc=spec.discrepancy if spec.discrepancy is not None else 0.01),
                       evidence=evidence, claims=ledger_claims, router=_router_if_configured(), paper_text=paper_text)
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
    if args.missing_sentence:
        await _missing_sentence(run_dir, args.paper, raw, args.repo)
    return 0


async def _missing_sentence(run_dir: Path, paper_path, assumptions, repo) -> None:
    """Draft the missing methods sentence for confirmed causes (paid: a few Super calls)."""
    from gapfinder.ingest.pdf import load_paper
    from gapfinder.models.router import Router
    from gapfinder.report.missing_sentence import add_to_run_dir

    if not paper_path or not Path(paper_path).is_file():
        print("missing sentence: needs the paper file (PDF or text) via --paper; skipped", file=sys.stderr)
        return
    items = assumptions["assumptions"] if isinstance(assumptions, dict) else (assumptions or [])
    meta = await add_to_run_dir(run_dir, load_paper(paper_path), Router(), items, repo)
    print(f"missing sentence: {meta['drafted']} drafted, {len(meta['skipped'])} skipped, ${meta['cost_usd']:.4f}"
          f"{'; issue draft: ' + str(run_dir / 'issue_draft.md') if meta['drafted'] else ''}")


async def cmd_missing_sentence(args) -> int:
    run_dir = Path(args.run_dir)
    if not (run_dir / "gap_report.json").exists():
        print(f"no gap_report.json in {run_dir}", file=sys.stderr)
        return 1
    raw = json.loads(Path(args.assumptions).read_text()) if args.assumptions else None
    await _missing_sentence(run_dir, args.paper, raw, args.repo)
    return 0


async def cmd_diff(args) -> int:
    import statistics

    from gapfinder.report.gap_report import GapReport
    from gapfinder.sandbox.backend import make_backend
    from gapfinder.sandbox.events import EventLog
    from gapfinder.sandbox.runner import Orchestrator
    from gapfinder.sandbox.spec import HarnessSpec, Knob
    from gapfinder.search.difftrace import diff, hypotheses, report_markdown
    from gapfinder.search.engine import GapSearch, SearchConfig, Target

    out = Path(args.out)
    mine_spec, ref_spec = HarnessSpec.load_yaml(args.spec), HarnessSpec.load_yaml(args.ref_spec)
    backend = make_backend(args.backend)
    mine = Orchestrator(backend, mine_spec, EventLog(out / "events.jsonl"), concurrency=args.concurrency)
    ref = Orchestrator(backend, ref_spec, EventLog(out / "reference" / "events.jsonl"), concurrency=args.concurrency)
    ref_recs, my_recs = await asyncio.gather(ref.trace_run(), mine.trace_run())
    if not ref_recs or not my_recs:
        print("diff: a trace came back empty (not a Python program, or the hook didn't load); nothing to compare",
              file=sys.stderr)
    diffs = diff(ref_recs, my_recs)
    plan = hypotheses(diffs, my_recs, mine_spec.knobs, mine_spec.code_root())
    pairs = ([(m.split("=")[0], m.split("=")[-1]) for m in args.metric] if args.metric else
             [(m, m) for m in mine_spec.metrics if m in ref_spec.metrics])
    if not pairs:
        print("diff: no metric to compare (give --metric MINE=REF)", file=sys.stderr)
        return 2
    runs = await ref.fanout([{}] * args.ref_runs, [f"reference-{i}" for i in range(args.ref_runs)])
    ok = [b.parsed_metrics for b in runs if b.status == "succeeded"]
    targets = []
    for i, (m, r) in enumerate(pairs):
        vals = [x[r] for x in ok if r in x]
        if vals:
            targets.append(Target(f"R_{m}", m, statistics.mean(vals), held_out=i > 0))
    if not targets:
        print("diff: the reference runs produced none of the metrics", file=sys.stderr)
        return 1
    for k, lit in plan.patch_knobs.items():
        mine_spec.knobs.setdefault(k, Knob(layer="environment", default=lit, env=True))
    _write(out / "diff.json", {"differences": [d.__dict__ for d in diffs], "plan": plan.to_dict(),
                               "reference_targets": [t.__dict__ for t in targets]})
    (out / "differences.md").write_text(report_markdown(diffs, plan) + "\n", encoding="utf-8")
    print(f"{len(diffs)} difference(s) from the reference; {len(plan.assumptions)} testable, "
          f"{len(plan.untestable)} reported only")
    for d in diffs:
        print("  " + d.text())
    if not plan.assumptions:
        print(f"nothing testable; see {out / 'differences.md'}")
        return 0
    # only the reference's values are candidates (no value coverage): the differences are the hypotheses, and
    # combine plus bisect shrink them to the ones that matter
    search = GapSearch(mine, targets, plan.assumptions,
                       SearchConfig(max_runs=args.max_runs, semantic_map=False, coverage=False))
    results = await search.run()
    md, _ = GapReport.from_search(search, results, paper=f"reference {ref_spec.name}").write(out)
    for r in results:
        label = r.attribution.confidence_label if r.attribution else "Reproduced"
        print(f"{r.target.claim_id}: {label}  {r.changes or ''}")
    print("(here the reference plays the paper's part: \"paper\" in the labels means the reference run)")
    print(f"report: {md}; differences: {out / 'differences.md'}")
    return 0


async def cmd_env_build(args) -> int:
    from gapfinder.env_build import build_env, fetch, write_result
    from gapfinder.models.router import Router
    from gapfinder.sandbox.backend import ContreeBackend

    res = await build_env(Router(), ContreeBackend(), args.local, fetch=fetch(args.repo, args.commit), image=args.image,
                          date=args.date, max_steps=args.max_steps)
    out = write_result(res, args.out)
    print(f"{'ok' if res.ok else 'FAILED'}: image {res.image}, checkpoint {res.checkpoint}, {len(res.recipe)} of "
          f"{len(res.steps)} commands kept, ${res.cost_usd:.4f}" + (f"; {res.reason}" if res.reason else ""))
    print(f"result: {out}")
    return 0 if res.ok else 1


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

    pd = sub.add_parser("spec-draft", help="draft a harness spec for a repo, smoke-test it (P1-0)")
    pd.add_argument("repo", nargs="?", help="local path or git URL")
    pd.add_argument("--out", help="where to write the spec YAML (a .md report goes next to it)")
    pd.add_argument("--paper-ledger", help="a `gapfinder ledger` output dir: adds the paper's setup values")
    pd.add_argument("--backend", default="local", help="local | contree (smoke test; default local)")
    pd.add_argument("--max-attempts", type=int, default=3, help="drafts that get a smoke test")
    pd.add_argument("--no-smoke", action="store_true", help="validate the draft only, no build/run")
    pd.add_argument("--no-self-check", action="store_true",
                    help="skip the second smoke run (seeds vary?) and the memory/time check against a Sandboxes VM")
    pd.add_argument("--smoke-timeout", type=float, default=900, help="cap in seconds on each smoke-test stage")
    pd.add_argument("--compare", metavar="HAND.yaml", help="hand-written spec: report knob recall against it")
    pd.add_argument("--diff", nargs=2, metavar=("DRAFT.yaml", "EDITED.yaml"),
                    help="print what a person changed in a drafted spec (no model call)")
    pd.add_argument("--no-cache", action="store_true")

    pf = sub.add_parser("fanout",help="fork branches from the loaded checkpoint (M2)")
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
    ps.add_argument("--assumptions", help="assumptions.json from `gapfinder ledger`, or a list "
                                          "(required unless --hypotheses repomap)")
    ps.add_argument("--hypotheses", choices=("ledger", "repomap"), default="ledger",
                    help="where hypotheses come from: the ledger's assumption list (default), or every knob of "
                         "the harness spec with generated candidate values, uniform priors and no paper "
                         "values (with --rank random: the random arm over all flags)")
    ps.add_argument("--candidates-per-knob", type=int, default=2,
                    help="values tried per knob in the screen (default 2)")
    ps.add_argument("--paper", help="paper name for the report title")
    ps.add_argument("--max-runs", type=int, default=None, help="branch-run budget")
    ps.add_argument("--screen-repeats", type=int, default=1, help="runs per hypothesis in the screen round")
    ps.add_argument("--reproduce-tol", type=float, default=0.10,
                    help="call a claim Reproduced only if the noise band is at most this fraction of the "
                         "paper value; otherwise Inconclusive")
    ps.add_argument("--noise-setups", type=int, default=1,
                    help="naive noise runs on that many independent builds/loads (checks the setup reproduces)")
    ps.add_argument("--claims", help="claim_ledger.json from `gapfinder ledger` (ties paper values to figures)")
    ps.add_argument("--resume", action="append", help="events.jsonl of an earlier search on the same spec "
                    "(repeatable): reuse its branch results")
    ps.add_argument("--evidence-anchor", help="enable web evidence; sources must mention this name (e.g. RusKey)")
    ps.add_argument("--no-evidence-gate", action="store_true",
                    help="ablation: skip the evidence step (no web/Tavily call); a closing value is at most "
                         "'Fits but unsupported'")
    ps.add_argument("--rank", choices=("ledger", "random"), default="ledger",
                    help="hypothesis order: the ledger's priors (default) or the random-search arm "
                         "(shuffled with --seed, no strong-lead skip)")
    ps.add_argument("--seed", type=int, default=0, help="seed for --rank random")
    ps.add_argument("--missing-sentence", action="store_true",
                    help="after the report, draft the methods sentence the paper was missing for Explained / "
                         "Paper-artifact inconsistency cards, plus issue_draft.md (paid, off by default; "
                         "needs --paper to be the paper file)")
    ps.add_argument("--repo", help="artifact repository URL, for the issue draft's header only")
    ps.add_argument("--no-fork", action="store_true", help="ablation: rebuild and reload for every branch")
    ps.add_argument("--backend", default=None)
    ps.add_argument("--concurrency", type=int, default=settings().max_concurrency)
    ps.add_argument("--cap", type=float, default=None, help="dollar cap for this run")
    ps.add_argument("--out")
    ps.add_argument("--adopt", action="append", metavar="STAGE=UUID",
                    help="reuse an existing checkpoint: source=, built=, loaded= (e.g. from spike S3)")

    pm = sub.add_parser("missing-sentence", help="add the drafted missing methods sentence and issue draft "
                                                 "to a finished run (paid: a few Super calls)")
    pm.add_argument("run_dir", help="directory holding gap_report.json")
    pm.add_argument("--paper", required=True, help="the paper file (PDF or .txt/.md)")
    pm.add_argument("--assumptions", help="assumptions.json from `gapfinder ledger` (adds paper/code values)")
    pm.add_argument("--repo", help="artifact repository URL, for the issue draft's header only")

    pe = sub.add_parser("env-build", help="build a runnable environment in Sandboxes, one command at a time")
    pe.add_argument("repo", help="GitHub URL of the repository")
    pe.add_argument("--commit", required=True)
    pe.add_argument("--local", required=True, help="a local checkout at that commit (read for imports and build files)")
    pe.add_argument("--image", help="base image (default: the model picks from a fixed list)")
    pe.add_argument("--date", help="the commit date, when --local is not a git clone")
    pe.add_argument("--max-steps", type=int, default=12)
    pe.add_argument("--out", required=True, help="where to write the result JSON (checkpoint, recipe, steps)")

    pq = sub.add_parser("diff", help="your reproduction vs a reference implementation: trace both runs, test where "
                                     "they differ against the reference's measured numbers")
    pq.add_argument("--spec", required=True, help="harness spec of your reproduction")
    pq.add_argument("--ref-spec", required=True, help="harness spec of the reference implementation")
    pq.add_argument("--metric", action="append", metavar="MINE[=REF]",
                    help="metrics to compare (the first is the target); default: the metrics both specs declare")
    pq.add_argument("--ref-runs", type=int, default=3, help="reference runs whose mean is the target")
    pq.add_argument("--max-runs", type=int, default=60)
    pq.add_argument("--backend", default=None)
    pq.add_argument("--concurrency", type=int, default=settings().max_concurrency)
    pq.add_argument("--out", required=True)

    args = p.parse_args(argv)
    if args.cmd == "repomap":
        return cmd_repomap(args)
    coro = {"ledger": cmd_ledger, "fanout": cmd_fanout, "search": cmd_search, "spec-draft": cmd_spec_draft,
            "missing-sentence": cmd_missing_sentence, "env-build": cmd_env_build,
            "diff": cmd_diff}[args.cmd](args)
    return asyncio.run(coro)


if __name__ == "__main__":
    sys.exit(main())
