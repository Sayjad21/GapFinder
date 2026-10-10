"""Gap Report cards: the five questions, effect sizes, provenance, and reports saved in the old format."""

import json
from pathlib import Path

import pytest

from gapfinder.ledger.schemas import Assumption, BranchStatus, Claim, Evidence
from gapfinder.report.gap_report import GapReport, upgrade_report
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target

ROOT = Path(__file__).resolve().parents[2]
TOY = ROOT / "eval" / "toy" / "hidden_knob.yaml"
QUESTIONS = ["Which experiment changed it?", "What did the paper report?", "What did we measure?",
             "Why do we believe it?", "What remains unknown?"]
OLD_REPORTS = sorted((ROOT / "demo" / "runs").glob("*/gap_report.json"))


def _orch(tmp_path, name):
    return Orchestrator(LocalBackend(tmp_path / f"sbx-{name}"), HarnessSpec.load_yaml(TOY),
                        EventLog(tmp_path / f"{name}.jsonl"))


async def _toy_report(tmp_path) -> GapReport:
    b = await _orch(tmp_path, "paper").run_branch({"alpha": "2.0"})
    assert b.status == BranchStatus.succeeded
    m = b.parsed_metrics
    ev = [Evidence(kind="code", ref="eval/toy/README", quote="alpha is sometimes set to 2.0")]
    assumptions = [Assumption(id="A1", knob="alpha", layer="config", paper_value="unstated",
                              candidate_values=["2.0", "50.0"], evidence=ev, prior_score=0.9)]
    claims = [Claim(id="C1", figure_or_table="Table 1", metric="score", reported_value=m["score"], type="absolute",
                    page=7, quote="The model reaches a score of 12.3 on the benchmark.", headline=True)]
    targets = [Target("C1", "score", m["score"]), Target("C2", "write_amp", m["write_amp"], held_out=True)]
    s = GapSearch(_orch(tmp_path, "search"), targets, assumptions, SearchConfig(), claims=claims)
    return GapReport.from_search(s, await s.run(), paper="toy")


async def test_card_answers_five_questions_in_markdown(tmp_path):
    md = (await _toy_report(tmp_path)).to_markdown()
    card = md.split("## C1:")[1].split("\n## ")[0]
    positions = [card.index(f"### {q}") for q in QUESTIONS]
    # the experiment comes first after the label, then the other four in the order asked
    assert positions == sorted(positions)
    assert "The model reaches a score of 12.3" in card and "p. 7" in card  # the ledger quote and page
    assert "PASS · Counterfactual" in card and "PASS · Evidence" in card and "Held-out claim" in card
    assert "Confirmed cause" in card
    assert "Effect: candidate" in card and "bootstrap interval [" in card


async def test_json_card_has_effect_with_interval_and_run_counts(tmp_path):
    d = (await _toy_report(tmp_path)).to_dict()
    c = d["claims"][0]
    for key in ("paper_claim", "measured", "experiment", "belief", "unknown", "cause", "effect"):
        assert key in c
    e = c["effect"]
    assert e["diff"] == pytest.approx(e["candidate"] - e["naive"])
    assert e["ci"][0] > 0 and e["excludes_zero"]  # the effect on a planted cause is clearly nonzero
    assert e["n_naive"] >= 5 and e["n_candidate"] >= 3
    assert c["cause"]["kind"] == "confirmed_cause"
    assert c["experiment"]["branches"] and c["experiment"]["config"][0]["naive"] == "1.0"
    assert c["measured"]["repeats"] and c["paper_claim"]["recorded"]
    json.dumps(d, default=str)


async def test_provenance_present_and_leaks_nothing(tmp_path, monkeypatch):
    monkeypatch.setenv("NEBIUS_PROJECT_ID", "project-secret-123")
    monkeypatch.setenv("TOKEN_FACTORY_API_KEY", "sk-secret-456")
    monkeypatch.setenv("TAVILY_API_KEY", "tvly-secret-789")
    rep = await _toy_report(tmp_path)
    p = rep.to_dict()["provenance"]
    assert len(p["harness_spec_sha256"]) == 64 and set(p["prompt_sha256"]) >= {"CLAIM_PROMPT", "TRIAGE_PROMPT"}
    assert p["models"]["ultra"] and set(p["cost"]) >= {"nemotron_billed_usd", "sandbox_reported_usd"}
    assert "commit" in p["gapfinder"]  # None when there is no git, never an error
    text = rep.to_markdown() + json.dumps(rep.to_dict(), default=str)
    assert "## Provenance" in text and "Harness spec sha256" in text
    for secret in ("project-secret-123", "sk-secret-456", "tvly-secret-789"):
        assert secret not in text


def test_provenance_survives_missing_git(monkeypatch):
    from gapfinder.report import provenance

    monkeypatch.setattr(provenance.subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(FileNotFoundError()))
    assert provenance.git_state() == {"commit": None, "dirty": None}


@pytest.mark.parametrize("path", OLD_REPORTS, ids=lambda p: p.parent.name)
def test_old_format_reports_still_render(path):
    old = json.loads(path.read_text(encoding="utf-8"))
    assert all("belief" not in c for c in old["claims"])  # recorded before the card fields existed
    md = GapReport.from_dict(old).to_markdown()
    for q in QUESTIONS:
        assert md.count(f"### {q}") == len(old["claims"])
    assert "Not recorded: this report was written before provenance was kept." in md
    up = upgrade_report(old)
    for a, b in zip(old["claims"], up["claims"]):  # nothing recorded is changed, only added to
        for k in ("gap_before", "gap_after", "changes", "replay", "counterfactual", "held_out", "notes"):
            assert a.get(k) == b.get(k)
        assert b["paper_claim"]["quote"] is None and b["belief"] is not None
    assert up["provenance"] is None


def test_minimal_report_is_returned_unchanged():
    minimal = {"paper": "toy", "claims": [{"target": {"claim_id": "C1"}, "attribution": {"confidence_label": "Explained"}}]}
    assert upgrade_report(minimal) == minimal
    assert upgrade_report(None) is None
