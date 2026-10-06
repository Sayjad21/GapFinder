"""M3 toy suite: nine search behaviours, each with a planted answer.

The "paper numbers" are produced by running the toy with a hidden
configuration; the search starts from the defaults and must recover it.
Toy model (eval/toy/hidden_knob/bench.py):
    score     = 100 * alpha * (3 if release else 1) * mean(rows) / (1 + beta) * (gamma if CACHE=on else 1)
    write_amp = 10 / alpha + (0.5 if CACHE=on else 2.0)
threads and LOG_LEVEL have no effect on anything.
"""

from pathlib import Path

import pytest

from gapfinder.ledger.schemas import Assumption, BranchStatus, Evidence
from gapfinder.report.gap_report import GapReport
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.bisect import minimal_set
from gapfinder.search.engine import GapSearch, SearchConfig, Target

TOY = Path(__file__).resolve().parents[2] / "eval" / "toy" / "hidden_knob.yaml"


def A(aid, knob, cands, supported=(), prior=0.5, status="unstated", layer="config"):
    """An assumption whose evidence mentions only the `supported` values."""
    ev = [Evidence(kind="code", ref="eval/toy/README", quote=f"{knob} is sometimes set to {v}") for v in supported]
    return Assumption(id=aid, knob=knob, layer=layer, paper_value="unstated", candidate_values=list(cands),
                      evidence=ev, prior_score=prior, status=status)


ALL = [
    A("A1", "alpha", ["2.0", "50.0"], supported=["2.0"], prior=0.9),
    A("A2", "beta", ["2.0"], supported=["2.0"], prior=0.6),
    A("A3", "CACHE", ["on"], supported=["on"], prior=0.5, layer="environment"),
    A("A4", "build_mode", ["release"], supported=["release"], prior=0.4, layer="build"),
    A("A5", "gamma", ["2.0"], supported=["2.0"], prior=0.3),
    A("A6", "threads", ["4"], supported=["4"], prior=0.2),
]


def orch(tmp_path, name="search"):
    spec = HarnessSpec.load_yaml(TOY)
    return Orchestrator(LocalBackend(tmp_path / f"sbx-{name}"), spec, EventLog(tmp_path / f"{name}.jsonl"))


async def paper(tmp_path, hidden):
    """The 'paper's numbers': the toy run under the hidden configuration."""
    b = await orch(tmp_path, "paper").run_branch(hidden)
    assert b.status == BranchStatus.succeeded
    return b.parsed_metrics


def targets(m, held_out_metric="write_amp"):
    return [Target("C1", "score", m["score"]), Target("C2", held_out_metric, m[held_out_metric], held_out=True)]


async def search(tmp_path, hidden, assumptions=ALL, **cfg):
    m = await paper(tmp_path, hidden)
    s = GapSearch(orch(tmp_path), targets(m), assumptions, SearchConfig(**cfg))
    return s, await s.run()


# 1. single cause ------------------------------------------------------------
async def test_single_cause_found_and_explained(tmp_path):
    s, [r] = await search(tmp_path, {"alpha": "2.0"})
    assert r.changes == {"alpha": "2.0"}
    assert r.attribution.confidence_label == "Explained"
    assert r.held_out["C2"]["ok"]  # write_amp also matches once alpha is right


# 3. decoy -------------------------------------------------------------------
async def test_decoy_pruned_in_screen(tmp_path):
    s, [r] = await search(tmp_path, {"alpha": "2.0"})
    beta = next(x for x in r.screen if x["knob"] == "beta")
    assert beta["units"] < 0  # moves the score the wrong way
    pruned = [e for e in s.orch.events.read() if e["type"] == "pruned" and e["knob"] == "beta"]
    assert pruned


# 7. counterfactual ------------------------------------------------------------
async def test_counterfactual_gap_reappears(tmp_path):
    s, [r] = await search(tmp_path, {"alpha": "2.0"})
    cf = r.counterfactual["alpha"]
    assert cf["ok"] and cf["gap_without"] == pytest.approx(r.gap_before)


# 2. interaction ---------------------------------------------------------------
async def test_interaction_found_in_combine_round(tmp_path):
    no_alpha = [a for a in ALL if a.knob != "alpha"]  # otherwise alpha alone could fake the score
    s, [r] = await search(tmp_path, {"gamma": "2.0", "CACHE": "on"}, assumptions=no_alpha)
    assert r.changes == {"gamma": "2.0", "CACHE": "on"}
    assert r.attribution.confidence_label == "Explained"
    assert r.replay[0]["env"]["CACHE"] == "on"  # env knobs must be in the replay recipe
    solo = {x["knob"]: x["units"] for x in r.screen}
    assert abs(solo["gamma"]) < 1 and abs(solo["CACHE"]) < 1  # neither matters alone


# 4. overfit trap --------------------------------------------------------------
async def test_overfit_trap_labelled_fits_but_unsupported(tmp_path):
    s, [r] = await search(tmp_path, {"alpha": "50.0"})
    assert r.changes == {"alpha": "50.0"}
    assert r.attribution.confidence_label == "Fits but unsupported"
    assert not r.plausibility["alpha"].supported


# 5. minimal set ---------------------------------------------------------------
async def test_minimal_set_pure():
    async def closes(c):
        return {"a", "c"} <= set(c)
    assert await minimal_set({"a": "1", "b": "1", "c": "1", "d": "1"}, closes) == {"a": "1", "c": "1"}


async def test_bisect_drops_knobs_that_do_not_matter(tmp_path):
    hidden = {"alpha": "2.0", "build_mode": "release"}
    m = await paper(tmp_path, hidden)
    s = GapSearch(orch(tmp_path), targets(m), ALL, SearchConfig())
    await s.calibrate()
    four = {**hidden, "threads": "4", "LOG_LEVEL": "debug"}  # the last two change nothing
    await s.measure(four, 1)
    from gapfinder.search.engine import ClaimResult
    t = s.targets[0]
    parent = ClaimResult(target=t, status="searched", gap_before=s.gap(t, {}), band=s.band(t))
    r = await s._verify(t, four, parent)
    assert r.changes == hidden


# 6. no cause ------------------------------------------------------------------
async def test_no_cause_is_unexplained(tmp_path):
    m = await paper(tmp_path, {})
    offset = [Target("C1", "score", m["score"] * 1.37), Target("C2", "write_amp", m["write_amp"], held_out=True)]
    s = GapSearch(orch(tmp_path), offset, ALL, SearchConfig())
    [r] = await s.run()
    assert r.attribution.confidence_label == "Unexplained"
    assert r.changes == {}


# 8. diff guard ----------------------------------------------------------------
async def test_diff_guard_rejects_source_edit(tmp_path):
    o = orch(tmp_path)
    bad = await o.run_branch({}, files={"src/compaction.cc": b"// tuned to match the paper\n"})
    assert bad.status == BranchStatus.rejected and "src/compaction.cc" in bad.note
    ok = await o.run_branch({}, files={"configs/override.ini": b"x=1\n"})
    assert ok.status == BranchStatus.succeeded


# 9. budget cap ----------------------------------------------------------------
async def test_budget_cap_writes_partial_report(tmp_path):
    s, [r] = await search(tmp_path, {"alpha": "2.0"}, max_runs=8)
    assert r.status == "partial"
    rep = GapReport.from_search(s, [r], paper="toy")
    md, js = rep.write(tmp_path / "report")
    assert rep.partial and "Partial report" in md.read_text()


async def test_report_renders_full_card(tmp_path):
    s, results = await search(tmp_path, {"alpha": "2.0"})
    md = GapReport.from_search(s, results, paper="toy").to_markdown()
    assert "Explained" in md and "Counterfactual" in md and "Replay: fork checkpoint" in md


async def test_no_verify_ablation_accepts_overfit(tmp_path):
    """Without the checks, the absurd value that merely fits is called 'Explained'."""
    s, [r] = await search(tmp_path, {"alpha": "50.0"}, verify=False)
    assert r.changes == {"alpha": "50.0"} and r.attribution.confidence_label == "Explained"
    assert r.counterfactual == {} and r.plausibility == {}
