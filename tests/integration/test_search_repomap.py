"""`gapfinder search --hypotheses repomap`: every spec knob is a hypothesis, with no ledger ranking or evidence."""

import json
from pathlib import Path

import pytest

from gapfinder import cli
from gapfinder.ledger.schemas import BranchStatus
from gapfinder.report.gap_report import GapReport
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec, generate_values

TOY = Path(__file__).resolve().parents[2] / "eval" / "toy" / "hidden_knob.yaml"


def test_generated_values_are_factors_around_the_default():
    assert generate_values("500") == ["250", "1000", "100", "2500", "50", "5000"]
    assert generate_values("2") == ["1", "4", "10", "20"]  # never below 1 for an integer knob
    assert generate_values("3") == ["2", "6", "1", "15", "30"]
    assert generate_values("0.5") == ["0.25", "1", "0.1", "2.5", "0.05", "5"]
    assert generate_values("true") == ["false"] and generate_values("on") == ["off"]
    assert generate_values("yacht,energy,concrete") == [] and generate_values("default") == []
    assert generate_values("0") == [] and generate_values("") == []


def test_every_knob_with_values_becomes_an_unranked_assumption():
    spec = HarnessSpec.load_yaml(TOY)
    asm, skipped = assumptions_from_spec(spec)
    assert {a.knob for a in asm} | set(skipped) == set(spec.knobs)
    assert set(skipped) == {"fault", "noise"}  # "" and 0.0: nothing to scale and the spec lists no values
    for a in asm:
        assert a.prior_score == 0.5 and a.paper_value == "unstated" and a.status == "unstated"
        assert a.evidence == [] and a.affects_claims == [] and a.layer == spec.knobs[a.knob].layer
    alpha = next(a for a in asm if a.knob == "alpha")
    assert alpha.candidate_values[:2] == ["2.0", "50.0"]  # the spec's own candidates come first
    assert alpha.candidate_values[2:] == ["0.5", "0.2", "5", "0.1", "10"]  # then generated ones; "2" is "2.0" again
    log_level = next(a for a in asm if a.knob == "LOG_LEVEL")
    assert log_level.candidate_values == ["debug"]  # text default: only what the spec lists


def orch(tmp_path, name="s"):
    return Orchestrator(LocalBackend(tmp_path / f"sbx-{name}"), HarnessSpec.load_yaml(TOY),
                        EventLog(tmp_path / f"{name}.jsonl"))


async def toy_metrics(tmp_path, hidden):
    b = await orch(tmp_path, "paper").run_branch(hidden)
    assert b.status == BranchStatus.succeeded
    return b.parsed_metrics


async def test_random_arm_over_all_flags_finds_a_planted_cause_without_the_ledger(tmp_path):
    m = await toy_metrics(tmp_path, {"alpha": "2.0"})
    asm, _ = assumptions_from_spec(HarnessSpec.load_yaml(TOY))
    targets = [Target("C1", "score", m["score"]), Target("C2", "write_amp", m["write_amp"], held_out=True)]
    s = GapSearch(orch(tmp_path), targets, asm, SearchConfig(rank="random", seed=3))
    [r] = await s.run()
    assert r.changes == {"alpha": "2.0"}
    assert r.attribution.confidence_label == "Fits but unsupported"  # no evidence exists, so none can support it
    assert not r.plausibility["alpha"].supported
    assert not s.unmapped
    GapReport.from_search(s, [r], paper="toy").to_markdown()


def write_inputs(tmp_path, hidden_metrics):
    t = tmp_path / "targets.json"
    t.write_text(json.dumps([{"claim_id": "C1", "metric": "score", "paper_value": hidden_metrics["score"]},
                             {"claim_id": "C2", "metric": "write_amp", "paper_value": hidden_metrics["write_amp"],
                              "held_out": True}]))
    return t


async def test_cli_repomap_needs_no_assumptions_file_and_ledger_still_needs_one(tmp_path, capsys, monkeypatch):
    monkeypatch.setenv("GF_CACHE_ONLY", "1")
    m = await toy_metrics(tmp_path, {"alpha": "2.0"})
    targets = write_inputs(tmp_path, m)
    base = ["search", "--spec", str(TOY), "--targets", str(targets), "--backend", "local"]
    assert await cli.cmd_search(_args(base + ["--hypotheses", "repomap", "--rank", "random", "--seed", "1",
                                              "--out", str(tmp_path / "run")])) == 0
    out = capsys.readouterr().out
    assert "hypotheses from the repo map" in out and "C1:" in out
    events = [json.loads(x) for x in (tmp_path / "run" / "events.jsonl").read_text().splitlines()]
    started = next(e for e in events if e["type"] == "run_started")
    assert started["hypotheses"] == "repomap" and started["rank"] == "random"
    assert await cli.cmd_search(_args(base + ["--out", str(tmp_path / "run2")])) == 2  # default: ledger file required


def _args(argv):
    """Parse a `search` command line the way main() does, without running it."""
    import argparse
    import sys
    from unittest import mock

    captured = {}

    def fake_run(coro):
        captured["coro"] = coro
        coro.close()
        return 0

    with mock.patch.object(sys, "argv", ["gapfinder"] + argv), mock.patch.object(cli.asyncio, "run", fake_run):
        orig = argparse.ArgumentParser.parse_args
        got = {}

        def spy(self, a=None, ns=None):
            got["args"] = orig(self, a, ns)
            return got["args"]

        with mock.patch.object(argparse.ArgumentParser, "parse_args", spy):
            cli.main(argv)
    return got["args"]


def test_default_hypotheses_source_is_the_ledger():
    args = _args(["search", "--spec", "s.yaml", "--targets", "t.json", "--assumptions", "a.json"])
    assert args.hypotheses == "ledger" and args.candidates_per_knob == 2 and args.assumptions == "a.json"
