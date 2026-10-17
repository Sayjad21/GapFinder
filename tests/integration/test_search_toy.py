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
    s = GapSearch(orch(tmp_path), offset, ALL, SearchConfig(coverage=False))  # v1.0 value grid
    [r] = await s.run()
    assert r.attribution.confidence_label == "Unexplained"
    assert r.changes == {}
    assert r.attribution.assumption_set == [] and r.gap_after == r.gap_before
    GapReport.from_search(s, [r], paper="toy").to_markdown()  # must render (regression: KeyError)
    # v1.1 coverage reaches beta=0.05, which moves the score most of the way without touching the
    # held-out claim (equifinality). That may be reported, but never as a confident attribution.
    s2 = GapSearch(orch(tmp_path, "cov"), offset, ALL, SearchConfig())
    [r2] = await s2.run()
    assert r2.attribution.confidence_label not in ("Explained", "Paper-artifact inconsistency", "Partially explained")


# 8. diff guard ----------------------------------------------------------------
async def test_diff_guard_rejects_source_edit(tmp_path):
    o = orch(tmp_path)
    bad = await o.run_branch({}, files={"src/compaction.cc": b"// tuned to match the paper\n"})
    assert bad.status == BranchStatus.rejected and "src/compaction.cc" in bad.note
    ok = await o.run_branch({}, files={"configs/override.ini": b"x=1\n"})
    assert ok.status == BranchStatus.succeeded


# 9. budget cap ----------------------------------------------------------------
async def test_budget_cap_writes_partial_report(tmp_path):
    s, [r] = await search(tmp_path, {"alpha": "2.0"}, max_runs=8, escrow_frac=0)
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


async def test_web_evidence_upgrades_fits_but_unsupported(tmp_path):
    """The overfit-trap value becomes Explained once a (fake) web source states it."""
    from gapfinder.search.evidence import EvidenceSearch

    async def fake(payload):
        return {"results": [{"url": "https://example.org/errata", "title": "errata",
                             "content": "Erratum: all runs used alpha 50.0, not the value in the paper."}]}

    m = await paper(tmp_path, {"alpha": "50.0"})
    s = GapSearch(orch(tmp_path), targets(m), ALL, SearchConfig(),
                  evidence=EvidenceSearch("toy", transport=fake, cache_dir=tmp_path / "tv"))
    [r] = await s.run()
    assert r.changes == {"alpha": "50.0"} and r.attribution.confidence_label == "Explained"
    assert r.plausibility["alpha"].supported and "example.org" in r.plausibility["alpha"].reason


async def test_costly_values_reported_not_run_and_stated_values_judged_against_naive(tmp_path):
    m = await paper(tmp_path, {"alpha": "2.0"})
    o = orch(tmp_path)
    o.spec.knobs["alpha"].max = 10.0
    many = [A("A1", "alpha", ["50.0", "2.0"], supported=["2.0"], prior=0.9),
            # paper states beta=0.5 and the naive run uses 0.5 -> screened last, not dropped (blind-2: a
            # wrong "stated" value from the ledger dropped the true cause before a single run)
            Assumption(id="A2", knob="beta", layer="config", paper_value="0.5", candidate_values=["2.0"],
                       prior_score=0.6, status="stated_code_differs")]
    s = GapSearch(o, targets(m), many, SearchConfig())
    knob_order = list(dict.fromkeys(h.knob for h in s.hypotheses()))
    assert knob_order.index("beta") == len(knob_order) - 1  # after every other knob, despite its prior
    [r] = await s.run()
    assert ("alpha", "50.0") in s.untestable and r.changes == {"alpha": "2.0"}
    assert any(x["knob"] == "beta" for x in r.screen)
    md = GapReport.from_search(s, [r], paper="toy").to_markdown()
    assert "Not testable within the budget" in md and "alpha=50.0" in md


async def test_budget_exhausted_result_is_not_a_confident_unverified_label(tmp_path):
    """Regression: an unverified best guess used to be labelled 'Partially explained'."""
    s, [r] = await search(tmp_path, {"gamma": "2.0", "CACHE": "on"},
                          assumptions=[a for a in ALL if a.knob != "alpha"], max_runs=12, escrow_frac=0)
    assert r.status == "partial"
    if r.attribution.confidence_label not in ("Unexplained", "Fits but unsupported"):
        assert r.counterfactual and r.held_out  # anything confident was actually verified


async def test_resume_reuses_runs(tmp_path):
    # the same budget on both sides: the per-knob value cap depends on it, so a different budget plans a
    # different search (a resumed run capped at the first run's count wanted alpha=0.0, which the first never
    # tried, and was rightly no longer confident once it couldn't finish)
    s1, [r1] = await search(tmp_path, {"alpha": "2.0"}, max_runs=150)
    events = list(s1.orch.events.read())
    m = await paper(tmp_path, {"alpha": "2.0"})
    s2 = GapSearch(orch(tmp_path, "resumed"), targets(m), ALL, SearchConfig(max_runs=150))
    assert s2.seed(events) == s1.runs_used
    [r2] = await s2.run()  # every successful measurement is cached
    new = [e["branch"]["knob_changes"] for e in s2.orch.events.read() if e["type"] == "branch_created"]
    failed_once = [dict(k) for k, v in s1._runs.items() if v and all(b.status != BranchStatus.succeeded for b in v)]
    assert all(c in failed_once for c in new)  # only a value that failed once gets its one retry (alpha=0.0 here)
    assert r2.changes == r1.changes and r2.attribution.confidence_label == r1.attribution.confidence_label


def test_directional_plausibility():
    from gapfinder.search.verify import plausible

    a = Assumption(id="A1", knob="num_keys", layer="dataset", paper_value="100000000", prior_score=0.5)
    p = plausible(a, "2000000", naive="500000")
    assert p.supported and p.partial
    assert not plausible(a, "100000", naive="500000").supported  # away from the paper's value


def test_paper_values_are_experiment_specific_and_duplicates_merge(tmp_path):
    from gapfinder.ledger.schemas import Claim

    o = orch(tmp_path)
    claims = [Claim(id="L1", figure_or_table="Figure 6", metric="m", type="trend", quote="q1"),
              Claim(id="L2", figure_or_table="Figure 8", metric="m", type="trend", quote="q2")]
    asm = [
        # stated for Figure 8 only, and equal to the naive value: must NOT block the knob for Figure 6
        Assumption(id="A1", knob="beta", layer="config", paper_value="0.5", candidate_values=["2.0"],
                   prior_score=0.9, affects_claims=["L2"]),
        # two entries for one knob: one matches naive (1.0), one states 2.0 -> the knob stays open, 2.0 first
        Assumption(id="A2", knob="alpha", layer="config", paper_value="1.0", candidate_values=["50.0"],
                   prior_score=0.8, affects_claims=["L1"]),
        Assumption(id="A3", knob="alpha", layer="config", paper_value="2.0", candidate_values=[],
                   prior_score=0.2, affects_claims=["L1"]),
    ]
    t = [Target("C1", "score", 68.3, figure="Figure 6")]
    s = GapSearch(o, t, asm, SearchConfig(), claims=claims)
    hyps = [(h.knob, h.value) for h in s.hypotheses()]
    assert ("beta", "2.0") in hyps
    assert hyps.index(("alpha", "2.0")) < hyps.index(("alpha", "50.0"))


async def test_super_triages_an_invalid_value_and_retries_it(tmp_path):
    from gapfinder.models.router import ResponseCache, Router

    async def transport(model, messages, max_tokens, response_format):
        assert "nemotron-3-super" in model  # triage is Super's job
        return {"choices": [{"message": {"content": '{"kind": "invalid_value", "suggestion": "2.0", '
                                                    '"why": "--alpha expects a float"}'}}],
                "usage": {"prompt_tokens": 50, "completion_tokens": 20}}

    m = await paper(tmp_path, {"alpha": "2.0"})
    bad = [A("A1", "alpha", ["two"], supported=["2.0"], prior=0.9)]  # 'two' crashes argparse
    s = GapSearch(orch(tmp_path), targets(m), bad, SearchConfig(),
                  router=Router(transport=transport, cache=ResponseCache(tmp_path / "c")))
    [r] = await s.run()
    assert s.triaged and s.triaged[0]["kind"] == "invalid_value" and s.triaged[0]["retried"] == "2.0"
    assert r.changes == {"alpha": "2.0"}


async def test_budget_exhausted_single_screen_run_is_not_labelled(tmp_path):
    """Regression (RusKey ablation): one lucky screen run and no budget left -> no label from it."""
    s1, [r1] = await search(tmp_path, {"alpha": "2.0"})
    assert r1.changes == {"alpha": "2.0"}
    keep, seen = [], False
    for ev in s1.orch.events.read():  # keep the noise runs and ONE run of the right value
        ch = ev["branch"]["knob_changes"] if ev.get("type") == "branch_finished" else {}
        if ch and (ch != {"alpha": "2.0"} or seen):
            continue
        seen = seen or ch == {"alpha": "2.0"}
        keep.append(ev)
    m = await paper(tmp_path, {"alpha": "2.0"})
    s2 = GapSearch(orch(tmp_path, "resumed"), targets(m), ALL, SearchConfig(escrow_frac=0))  # the exhausted path
    s2.cfg.max_runs = s2.seed(keep)
    [r2] = await s2.run()
    assert r2.status == "partial" and r2.attribution.confidence_label == "Unexplained"
    assert any("1 of" in n and "confirmation runs" in n for n in r2.notes)


async def test_a_value_that_always_fails_is_not_rerun_on_every_call(tmp_path):
    m = await paper(tmp_path, {"alpha": "2.0"})
    s = GapSearch(orch(tmp_path), targets(m), ALL, SearchConfig())
    for _ in range(4):  # e.g. screened, then asked for again while explaining another claim
        assert await s.measure({"alpha": "two"}, 1, "screen") == []
    assert await s.measure({"alpha": "two"}, 5, "confirm") == []  # more repeats asked: still not re-run
    assert len(s._runs[frozenset({"alpha": "two"}.items())]) == 2 and s.runs_used == 2
    # and a value with no successful run never survives the screen, even as a strong ledger lead
    lead = [A("A1", "alpha", ["two"], supported=["two"], prior=0.95)]
    s2 = GapSearch(orch(tmp_path, "lead"), targets(m), lead, SearchConfig(coverage=False))
    [r] = await s2.run()
    assert r.screen and all(x["knob"] != "alpha" or x["units"] == float("-inf") for x in r.screen)
    # (the other spec knobs are screened in the fallback round, since the only lead never ran)
    assert not any(e["type"] == "survivor" and e.get("knob") == "alpha" for e in s2.orch.events.read())


async def test_budget_stop_leaves_no_branch_unrecorded(tmp_path):
    """Regression (RusKey ablation): runs in flight when the budget ran out were never recorded."""
    s, [r] = await search(tmp_path, {"alpha": "2.0"}, max_runs=8, escrow_frac=0)
    assert r.status == "partial"
    ev = list(s.orch.events.read())
    created = {e["branch"]["id"] for e in ev if e["type"] == "branch_created"}
    finished = {e["branch"]["id"] for e in ev if e["type"] == "branch_finished"}
    assert created and created == finished


@pytest.mark.parametrize("flaky", [False, True])
async def test_noise_setups_check_whether_the_load_reproduces(tmp_path, flaky):
    """Content-addressed checkpoints: identical loads dedup to one ID; a load that writes
    something different each time (timing, random state) gives a new ID per load."""
    m = await paper(tmp_path, {"alpha": "2.0"})
    spec = HarnessSpec.load_yaml(TOY)
    if flaky:
        spec.load.command += " && head -c 16 /dev/urandom > data/stamp"
    o = Orchestrator(LocalBackend(tmp_path / "sbx", content_ids=True), spec, EventLog(tmp_path / "e.jsonl"))
    s = GapSearch(o, targets(m), ALL, SearchConfig(noise_setups=3))
    await s.calibrate()
    assert s.setup_check["reproducible"] is (not flaky)
    assert s.setup_check["distinct_checkpoints"] == (3 if flaky else 1)
    shared = o.tree.find_stage("loaded", {})
    # the shared load stays shared (a reproducible load dedups, so then all five share it)
    assert [b.parent_checkpoint for b in s._runs[frozenset()]].count(shared) == (3 if flaky else 5)



async def test_within_a_wide_band_is_inconclusive_not_reproduced(tmp_path):
    """Naive equals the paper here; with a band wider than the tolerance it can't count as a reproduction."""
    s, [r] = await search(tmp_path, {})
    assert r.status == "reproduced" and r.attribution is None  # band 1% <= 10% tolerance
    s2, [r2] = await search(tmp_path, {}, reproduce_tol=0.001)
    assert r2.status == "inconclusive" and r2.attribution.confidence_label == "Inconclusive"
    assert r2.changes == {} and s2.runs_used == s2.cfg.noise_repeats  # no search inside a band this wide
    md = GapReport.from_search(s2, [r2], paper="toy").to_markdown()
    assert "| Inconclusive |" in md and "too wide" in md


# search switches: the evidence gate ---------------------------------------------------------
async def test_evidence_gate_off_never_reaches_explained_and_makes_no_evidence_call(tmp_path):
    from gapfinder.search.evidence import EvidenceSearch

    calls = []

    async def fake(payload):  # the web source that would upgrade the overfit-trap value if it were asked
        calls.append(payload)
        return {"results": [{"url": "https://example.org/errata", "title": "errata",
                             "content": "Erratum: all runs used alpha 50.0, not the value in the paper."}]}

    def ev(d):
        return EvidenceSearch("toy", transport=fake, cache_dir=tmp_path / d)

    # alpha=2.0 is backed by the ledger's evidence: Explained with the gate on, only a fit without it
    m = await paper(tmp_path, {"alpha": "2.0"})
    on = GapSearch(orch(tmp_path, "on"), targets(m), ALL, SearchConfig(), evidence=ev("tv-on"))
    [r_on] = await on.run()
    assert r_on.attribution.confidence_label == "Explained"
    off = GapSearch(orch(tmp_path, "off"), targets(m), ALL, SearchConfig(evidence_gate=False), evidence=ev("tv-off"))
    [r_off] = await off.run()
    assert r_off.changes == {"alpha": "2.0"}  # the experiments still find it
    assert r_off.attribution.confidence_label == "Fits but unsupported"
    assert not r_off.plausibility["alpha"].supported and "gate off" in r_off.plausibility["alpha"].reason
    assert any("evidence gate off" in n for n in r_off.notes)
    # the web-evidence case: asked with the gate on, never with it off
    m50 = await paper(tmp_path, {"alpha": "50.0"})
    s_on = GapSearch(orch(tmp_path, "on50"), targets(m50), ALL, SearchConfig(), evidence=ev("tv-on50"))
    [r_on50] = await s_on.run()
    assert r_on50.attribution.confidence_label == "Explained" and calls
    calls.clear()
    s_off = GapSearch(orch(tmp_path, "off50"), targets(m50), ALL, SearchConfig(evidence_gate=False),
                      evidence=ev("tv-off50"))
    [r_off50] = await s_off.run()
    assert not calls
    assert r_off50.attribution.confidence_label == "Fits but unsupported"
    assert any(e["type"] == "note" and e.get("evidence_gate") is False for e in s_off.orch.events.read())
    assert not any(e["type"] == "note" and e.get("evidence_gate") is False for e in s_on.orch.events.read())


async def test_evidence_gate_off_also_holds_without_verification(tmp_path):
    """verify=False labels any closing config Explained; with the gate off it cannot."""
    s, [r] = await search(tmp_path, {"alpha": "2.0"}, verify=False, evidence_gate=False)
    assert r.changes == {"alpha": "2.0"} and r.attribution.confidence_label == "Fits but unsupported"


# search switches: the random-search arm ------------------------------------------------------
def _hyps(tmp_path, name, **cfg):
    o = Orchestrator(LocalBackend(tmp_path / f"sbx-{name}"), HarnessSpec.load_yaml(TOY), EventLog(tmp_path / f"{name}.jsonl"))
    s = GapSearch(o, [Target("C1", "score", 68.3)], ALL, SearchConfig(**cfg))
    return s, [(h.knob, h.value) for h in s.hypotheses()]


def test_random_rank_is_deterministic_for_a_seed_and_differs_from_the_ledger_order(tmp_path):
    s_led, ledger = _hyps(tmp_path, "led")
    s_rnd, a1 = _hyps(tmp_path, "a1", rank="random", seed=0)
    _, a2 = _hyps(tmp_path, "a2", rank="random", seed=0)
    assert a1 == a2 == [(h.knob, h.value) for h in s_rnd.hypotheses()]  # the same on every call
    assert sorted(a1) == sorted(ledger) and len(a1) > 2  # same hypothesis space
    assert ledger[0] == ("alpha", "2.0")  # the ledger puts its highest prior first
    assert a1 != ledger  # no ledger order
    orders = {tuple(_hyps(tmp_path, f"s{k}", rank="random", seed=k)[1]) for k in range(1, 6)} | {tuple(a1)}
    assert len(orders) > 1  # another seed, another order
    alpha = next(h for h in s_led.hypotheses() if h.knob == "alpha")
    assert s_led._strong_lead(alpha)  # a prior of 0.9 is a strong lead in the ledger order
    assert not any(s_rnd._strong_lead(h) for h in s_rnd.hypotheses())


async def test_random_rank_still_searches_and_skips_no_strong_leads(tmp_path):
    (tmp_path / "led").mkdir()
    s, [r] = await search(tmp_path, {"alpha": "2.0"}, rank="random", seed=3)
    assert r.changes == {"alpha": "2.0"}  # the experiments find the cause without the ledger's order
    _, [r_led] = await search(tmp_path / "led", {"alpha": "2.0"})
    assert sorted((x["knob"], x["value"]) for x in r.screen) == sorted((x["knob"], x["value"]) for x in r_led.screen)
    assert [x["knob"] for x in r.screen] != [x["knob"] for x in r_led.screen]  # same space, different order
    # every survivor earned it by its own screen effect, none by a ledger lead
    survivors = [e for e in s.orch.events.read() if e["type"] == "survivor" and e["round"] == "screen"]
    assert survivors and all(e["units"] >= s.cfg.effect_threshold for e in survivors)
    note = next(e for e in s.orch.events.read() if e["type"] == "note" and e.get("rank"))
    assert note["rank"] == "random" and note["seed"] == 3


def test_search_config_rejects_an_unknown_rank():
    with pytest.raises(ValueError):
        SearchConfig(rank="alphabetical")


async def test_equally_good_values_are_reported_as_a_set(tmp_path):
    """gamma only matters with CACHE=on in the toy, so with alpha fixed by the paper several measured
    alpha values can't all fit; the set must contain the answer's value and only near-equal fits."""
    s, [r] = await search(tmp_path, {"alpha": "2.0"})
    assert r.changes == {"alpha": "2.0"}
    assert r.value_sets["alpha"][0] == "2.0" or "2.0" in r.value_sets["alpha"]
    for v in r.value_sets["alpha"]:  # every member fits within one band of the answer
        assert abs(s.gap(s.targets[0], {"alpha": v})) <= abs(r.gap_after) + s.band(s.targets[0])


def test_scorer_credits_a_set_that_contains_the_truth():
    import sys
    sys.path.insert(0, "eval/gapbench")
    from score import score_claim

    key = {"id": "t", "type": "single_unstated", "category": "known_cause", "hidden": {"max_steps": "500"}}
    pred = {"label": "Fits but unsupported", "knobs": {"max_steps": "400"}, "value_sets": {"max_steps": ["400", "500", "1000"]}}
    sc = score_claim(key, pred)
    assert sc["outcome"] == "missed" and sc["correct_set"]  # exact score unchanged; set credit separate
    assert not score_claim(key, {**pred, "value_sets": {"max_steps": ["400", "1000"]}})["correct_set"]


async def test_a_confident_label_needs_a_complete_search(tmp_path):
    """blind-2: "Explained" came from a partial run, with a knob never tested and only a code default as
    evidence. Each of those now caps the label at Fits but unsupported, with the reason."""
    m = await paper(tmp_path, {"alpha": "2.0"})
    code_only = [Assumption(id="A1", knob="alpha", layer="config", paper_value="unstated", candidate_values=["2.0"],
                            prior_score=0.9, status="unstated",
                            evidence=[Evidence(kind="code", ref="bench.py:5", quote="alpha default 2.0 in an older script")])]
    s = GapSearch(orch(tmp_path), targets(m), code_only, SearchConfig())
    [r] = await s.run()
    assert r.changes == {"alpha": "2.0"} and r.attribution.confidence_label == "Fits but unsupported"
    assert any("capped" in n and "code evidence" in n for n in r.notes)
    # documentation (README) is the authors' own account: it supports a confident label
    s2, [r2] = await search(tmp_path, {"alpha": "2.0"})
    assert r2.attribution.confidence_label == "Explained"
    # and with the cap off, the code default would have been enough, as before
    s3 = GapSearch(orch(tmp_path, "off"), targets(m), code_only, SearchConfig(complete_for_confidence=False))
    [r3] = await s3.run()
    assert r3.attribution.confidence_label == "Explained"


async def test_relation_claims_check_candidates(tmp_path):
    """Part 3: a relation the paper states over a setting is checked under the candidate. One that holds
    changes nothing; one that reverses beyond noise fails the candidate like a broken held-out claim."""
    m = await paper(tmp_path, {"alpha": "2.0"})

    def rel(cid, knob, a, b, direction):
        return Target(cid, "score", relation={"knob": knob, "from": a, "to": b, "direction": direction})

    holds = targets(m) + [rel("R1", "beta", "0.5", "2.0", "down")]  # more beta, lower score: true
    s = GapSearch(orch(tmp_path, "holds"), holds, ALL, SearchConfig())
    [r] = await s.run()
    assert r.changes == {"alpha": "2.0"} and r.attribution.confidence_label == "Explained"
    assert r.relations["R1"]["checked"] and r.relations["R1"]["holds"]
    md = GapReport.from_search(s, [r], paper="toy").to_markdown()
    assert "Paper's stated relation: R1" in md and "(holds)" in md

    reversed_ = targets(m) + [rel("R2", "alpha", "1.0", "2.0", "down")]  # false under any alpha: the score rises
    s2 = GapSearch(orch(tmp_path, "rev"), reversed_, ALL, SearchConfig())
    [r2] = await s2.run()
    assert r2.attribution.confidence_label not in ("Explained", "Paper-artifact inconsistency", "Partially explained")
    assert all(v["broken"] for v in r2.relations.values() if v.get("checked")) or not r2.relations

    unknown = targets(m) + [rel("R3", "no_such_knob", "1", "2", "up")]
    s3 = GapSearch(orch(tmp_path, "unk"), unknown, ALL, SearchConfig())
    [r3] = await s3.run()
    assert r3.attribution.confidence_label == "Explained" and not r3.relations["R3"]["checked"]
    assert len(s3.targets) == 2 and len(s3.relations) == 1  # a relation is never a target to explain
