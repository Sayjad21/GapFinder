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


def test_ledger_names_map_to_spec_knobs_by_their_core_words():
    """blind-1 (FastGCN): the ledger said num_epochs / dropout_rate / hidden_dim for epochs / dropout / hidden1."""
    from gapfinder.search.engine import map_knob_name

    knobs = ["model", "learning_rate", "epochs", "hidden1", "dropout", "weight_decay", "early_stopping", "max_degree"]
    assert map_knob_name("--Learning-Rate", knobs) == "learning_rate"  # exact, as before
    assert map_knob_name("num_epochs", knobs) == "epochs"
    assert map_knob_name("dropout_rate", knobs) == "dropout"
    assert map_knob_name("hidden_dim", knobs) == "hidden1"
    assert map_knob_name("early_stopping_patience", knobs) == "early_stopping"
    assert map_knob_name("lr", knobs) == "learning_rate"
    assert map_knob_name("FLAGS.hidden1", knobs) == "hidden1"  # a fresh blind-1 ledger wrote these
    assert map_knob_name("args.learning_rate (Adam step size)", knobs) == "learning_rate"
    assert map_knob_name("rank1 (sample size top layer)", knobs) is None
    assert map_knob_name("Number of GCN layers (1 vs 2)", knobs) is None
    for other in ("graphsage_hidden_dim", "cpu_model", "sample_size_layer1", "num_layers", "random_seed"):
        assert map_knob_name(other, knobs) is None, other
    assert map_knob_name("hidden_size", ["hidden1", "hidden2"]) is None  # ambiguous: no guess


async def test_spec_knobs_the_ledger_never_names_are_still_screened(tmp_path):
    """blind-1: knobs no assumption named were never tested. Now they are, after the ledger's own."""
    from gapfinder.ledger.schemas import Assumption

    m = await toy_metrics(tmp_path, {"alpha": "2.0"})
    targets = [Target("C1", "score", m["score"]), Target("C2", "write_amp", m["write_amp"], held_out=True)]
    # the ledger names only knobs that aren't the cause, one of them by another name
    asm = [Assumption(id="A1", knob="num_threads", layer="config", paper_value="unstated", code_default="1",
                      candidate_values=["4"], evidence=[], prior_score=0.8, status="unstated", affects_claims=[]),
           Assumption(id="A2", knob="cpu_model", layer="config", paper_value="i7", code_default="?",
                      candidate_values=[], evidence=[], prior_score=0.6, status="unstated", affects_claims=[])]
    s = GapSearch(orch(tmp_path), targets, asm, SearchConfig())
    assert s.renamed == {"num_threads": "threads"} and s.unmapped == ["cpu_model"]
    assert "alpha" in s.spec_only and "threads" not in s.spec_only
    assert "alpha" not in s.assumptions and s._fallback["alpha"].prior_score < 0.6  # a fallback, after the ledger
    [r] = await s.run()
    assert r.changes == {"alpha": "2.0"}
    md = GapReport.from_search(s, [r], paper="toy").to_markdown()
    assert "`num_threads` → `threads`" in md and "`alpha`" in md.split("## Knob names")[1]

    off = GapSearch(orch(tmp_path, "off"), targets, asm, SearchConfig(screen_spec_knobs=False))
    assert off.spec_only == [] and "alpha" not in off.all_for


async def test_code_defaults_are_read_from_the_code_not_the_ledger(tmp_path):
    """blind-1: the ledger guessed FastGCN's dropout default as 0.5 (it is 0.0), which made a paper value
    of 0 look like a paper-artifact inconsistency. With the code here, defaults come from the code; a
    "code differs" the code can't confirm never yields that label."""
    from gapfinder.ledger.schemas import Assumption

    m = await toy_metrics(tmp_path, {"alpha": "2.0"})
    targets = [Target("C1", "score", m["score"]), Target("C2", "write_amp", m["write_amp"], held_out=True)]

    def asm(knob, paper, guessed, status):
        return Assumption(id=knob, knob=knob, layer="config", paper_value=paper, code_default=guessed,
                          candidate_values=["2.0"], evidence=[], prior_score=0.8, status=status, affects_claims=[])

    s = GapSearch(orch(tmp_path), targets, [
        asm("beta", "0.5", "0.9", "stated_code_differs"),     # wrong guess: the code says 0.5, as the paper
        asm("gamma", "1.0", "1.0", "stated_matches"),        # right
        asm("LOG_LEVEL", "debug", "info", "stated_code_differs"),  # no flag in the code: unverified
    ], SearchConfig())
    assert s.all_for["beta"][0].code_default == "0.5" and s.all_for["beta"][0].status == "stated_matches"
    assert [c["knob"] for c in s.corrected_defaults] == ["beta"]
    assert s.corrected_defaults[0]["at"] == "bench.py:6"
    assert s.all_for["gamma"][0].status == "stated_matches"
    assert s.unverified_defaults == {"LOG_LEVEL"}
    [r] = await s.run()
    assert r.changes == {"alpha": "2.0"}
    md = GapReport.from_search(s, [r], paper="toy").to_markdown()
    assert "`beta` 0.5 at bench.py:6 (ledger said 0.9)" in md and "`LOG_LEVEL`" in md.split("## Knob names")[1]


async def test_a_separately_tuned_held_out_row_is_reported_not_a_constraint(tmp_path):
    """blind-1: the documented lr=0.001 fixed FastGCN's transductive Cora row but hurt the inductive rows,
    which the paper tuned on their own; the shared-setting held-out check rejected the true answer."""
    m = await toy_metrics(tmp_path, {"alpha": "2.0"})
    asm, _ = assumptions_from_spec(HarnessSpec.load_yaml(TOY))
    # a held-out claim alpha=2.0 breaks: the paper's write_amp as if measured under another setting
    wrong = m["write_amp"] * 3
    strict = [Target("C1", "score", m["score"]), Target("C2", "write_amp", wrong, held_out=True)]
    s = GapSearch(orch(tmp_path, "strict"), strict, asm, SearchConfig())
    [r] = await s.run()
    assert r.attribution.confidence_label != "Explained"  # the shared-setting check blocks it, as before

    loose = [Target("C1", "score", m["score"]), Target("C2", "write_amp", wrong, held_out=True, tuned_separately=True)]
    s2 = GapSearch(orch(tmp_path, "loose"), loose, asm, SearchConfig())
    [r2] = await s2.run()
    assert r2.changes == {"alpha": "2.0"}
    assert r2.held_out["C2"]["tuned_separately"] and r2.held_out["C2"]["ok"]
    md = GapReport.from_search(s2, [r2], paper="toy").to_markdown()
    assert "NOTE · Held-out claim, tuned separately: C2" in md
    back = GapReport.from_dict(GapReport.from_search(s2, [r2], paper="toy").to_dict())
    assert back.results[0].held_out["C2"]["tuned_separately"]


def test_paper_sentences_naming_a_knob_are_evidence_for_fallback_knobs():
    """blind-1, post-hoc: a fresh ledger didn't name learning_rate, so the paper's sweep sentence never
    counted as evidence for 0.001. The sentence is found by the knob's whole name, not a word of it."""
    from gapfinder.search.engine import paper_mentions
    from gapfinder.search.verify import plausible
    from gapfinder.ledger.schemas import Assumption, Evidence

    text = ("FASTGCN: FAST LEARNING WITH GRAPH CONVOLUTIONAL NETWORKS (2018). We performed hyperparameter "
            "selection for the learning rate and model dimension. We swept learning rate in the set "
            "{0.01, 0.001, 0.0001}. The hidden dimension is 16. Dropout rate is set as 0. We train for 200 epochs.")
    assert paper_mentions(text, "learning_rate") == ["We swept learning rate in the set {0.01, 0.001, 0.0001}."]
    assert paper_mentions(text, "hidden1") == ["The hidden dimension is 16."]
    assert paper_mentions(text, "epochs") == ["We train for 200 epochs."]
    assert paper_mentions(text, "weight_decay") == []
    a = Assumption(id="R1", knob="learning_rate", layer="config", paper_value="unstated", code_default="0.01",
                   candidate_values=["0.001"], prior_score=0.1, status="unstated", affects_claims=[],
                   evidence=[Evidence(kind="paper", ref="paper text", quote=q) for q in paper_mentions(text, "learning_rate")])
    assert plausible(a, "0.001").supported and not plausible(a, "0.002").supported
    assert not plausible(a, "0.0001".replace("1", "2")).supported


def test_secant_values_interpolate_the_crossing_and_snap_to_round_numbers():
    from gapfinder.search.engine import secant_values as sv

    assert sv([("1", 10.0), ("10", 50.0), ("100", 60.0)], 30.0, "multiplier", "1") == ["3"]  # a x3 the ladder skips
    assert sv([("15", 60.0), ("150", 90.0), ("2", 30.0)], 80.0, "count", "15") == ["80"]
    assert sv([("0.01", 70.0), ("0.1", 40.0), ("0.001", 85.0)], 80.0, "rate", "0.01") == ["0.002"]
    assert sv([("0.5", 0.6), ("0.05", 0.9), ("0.95", 0.2)], 0.8, "fraction", "0.5") == ["0.12"]
    assert sv([("0.01", 70.0), ("0.001", 72.0)], 80.0, "rate", "0.01") == []  # not bracketed: no guess
    assert sv([("1", 10.0)], 30.0, None, "1") == []


async def test_secant_step_finds_a_value_between_ladder_rungs(tmp_path):
    """Planted alpha=3.0: the ladder (2, 5, 10, ...) never tries 3; the secant iteration gets there."""
    m = await toy_metrics(tmp_path, {"alpha": "3.0"})
    asm, _ = assumptions_from_spec(HarnessSpec.load_yaml(TOY))
    targets = [Target("C1", "score", m["score"]), Target("C2", "write_amp", m["write_amp"], held_out=True)]
    s = GapSearch(orch(tmp_path), targets, asm, SearchConfig(trace=False))
    [r] = await s.run()
    assert r.changes == {"alpha": "3"}, (r.changes, [x for x in r.screen if x["knob"] == "alpha"])
    notes = [e["msg"] for e in s.orch.events.read() if e["type"] == "note" and "secant" in e.get("msg", "")]
    assert notes and "alpha=2.5" in notes[0]
    off = GapSearch(orch(tmp_path, "off"), targets, asm, SearchConfig(trace=False, secant_per_knob=0))
    [r0] = await off.run()
    assert r0.changes != {"alpha": "3"}


async def test_secant_step_stays_out_when_a_screened_value_already_fits(tmp_path):
    """Dev suite: interpolated values of other knobs (lr=0.04, eps_start=0.3) fit as exactly as the true
    ladder value and sometimes won. With a ladder value that fits, the secant step adds nothing."""
    m = await toy_metrics(tmp_path, {"alpha": "2.0"})  # 2.0 is on the ladder
    asm, _ = assumptions_from_spec(HarnessSpec.load_yaml(TOY))
    targets = [Target("C1", "score", m["score"]), Target("C2", "write_amp", m["write_amp"], held_out=True)]
    s = GapSearch(orch(tmp_path), targets, asm, SearchConfig(trace=False))
    [r] = await s.run()
    assert r.changes == {"alpha": "2.0"}
    assert not [e for e in s.orch.events.read() if e["type"] == "note" and "secant" in e.get("msg", "")]
