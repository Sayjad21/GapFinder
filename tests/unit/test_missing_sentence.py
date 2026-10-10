"""Missing-sentence drafting: eligibility, shape, issue file, spend cap, off by default. No network."""

import asyncio
import json
from pathlib import Path

import pytest

from gapfinder import cli
from gapfinder.ingest.pdf import Page, PaperText
from gapfinder.models.router import ResponseCache, Router
from gapfinder.report import missing_sentence as ms

PARA = ("We evaluate on a single machine with 64 GB of memory and an NVMe SSD. "
        "All systems use the default configuration unless stated otherwise in this section. "
        "Each experiment loads the database and then runs the workload to completion. "
        "Results are averaged over several runs of the benchmark workload.")


def _card(cid, label, changes=None):
    return {"target": {"claim_id": cid, "metric": "latency", "paper_value": 2.0},
            "attribution": {"confidence_label": label} if label else None, "status": "searched",
            "gap_before": 0.4, "gap_after": 0.02, "band": 0.03, "changes": changes if changes is not None else {"threads": "8"},
            "plausibility": {"threads": {"supported": True, "reason": "code uses 8 threads"}},
            "counterfactual": {"threads": {"gap_without": 0.4, "ok": True}},
            "replay": [{"env": {"THREADS": "8", "API_KEY": "sk-abcdefghijklmnopqrstuvwxyz"}, "command": "./run"}]}


def _report(*labels):
    return {"paper": "Toy Paper", "claims": [_card(f"C{i}", l) for i, l in enumerate(labels)]}


def _paper():
    return PaperText(path=Path("p.txt"), pages=[Page(1, "Intro.\n\nshort."), Page(2, PARA)])


def _router(tmp_path):
    calls = []

    async def transport(model, messages, max_tokens, response_format):
        calls.append(messages)
        body = json.dumps({"sentence": "All runs use 8 worker threads.", "insert_after": 2})
        return {"choices": [{"message": {"content": body}}], "usage": {"prompt_tokens": 100, "completion_tokens": 20}}

    return Router(transport=transport, cache=ResponseCache(tmp_path / "c")), calls


def test_only_eligible_labels_trigger_calls(tmp_path):
    r, calls = _router(tmp_path)
    rep = _report("Explained", "Paper-artifact inconsistency", "Fits but unsupported", "Partially explained",
                  "Unexplained", "Inconclusive", None)
    meta = asyncio.run(ms.draft_missing_sentences(rep, _paper(), r))
    assert len(calls) == 2 and meta["drafted"] == 2
    drafted = [c["target"]["claim_id"] for c in rep["claims"] if "missing_sentence" in c]
    assert drafted == ["C0", "C1"]


def test_ineligible_report_makes_zero_calls(tmp_path):
    r, calls = _router(tmp_path)
    rep = _report("Fits but unsupported", "Unexplained", "Partially explained", "Inconclusive", None)
    meta = asyncio.run(ms.draft_missing_sentences(rep, _paper(), r))
    assert calls == [] and meta["drafted"] == 0
    assert not any("missing_sentence" in c for c in rep["claims"])


def test_output_shape(tmp_path):
    r, _ = _router(tmp_path)
    rep = _report("Explained")
    asyncio.run(ms.draft_missing_sentences(rep, _paper(), r))
    out = rep["claims"][0]["missing_sentence"]
    assert out["sentence"] == "All runs use 8 worker threads."
    assert out["paragraph"] == PARA and out["page"] == 2 and out["insert_after"] == 2
    assert out["model_drafted"] is True and out["prompt_sha256"] == ms.PROMPT_SHA256
    assert rep["missing_sentence_meta"]["prompt_sha256"] == ms.PROMPT_SHA256
    parts = ms.paragraph_with_insertion(out)
    assert [k for k, _ in parts] == ["paper", "drafted", "paper"]
    assert "threads" in ms._evidence_text(rep["claims"][0], [])


def test_insert_after_is_clamped(tmp_path):
    r, _ = _router(tmp_path)

    async def wild(model, messages, max_tokens, response_format):
        body = json.dumps({"sentence": "X.", "insert_after": 99})
        return {"choices": [{"message": {"content": body}}], "usage": {}}

    r2 = Router(transport=wild, cache=ResponseCache(tmp_path / "c2"))
    rep = _report("Explained")
    asyncio.run(ms.draft_missing_sentences(rep, _paper(), r2))
    assert rep["claims"][0]["missing_sentence"]["insert_after"] == 4


def test_issue_file_written_without_secrets(tmp_path):
    r, _ = _router(tmp_path)
    run = tmp_path / "run"
    run.mkdir()
    rep = _report("Explained", "Unexplained")
    (run / "gap_report.json").write_text(json.dumps(rep), encoding="utf-8")
    (run / "gap_report.md").write_text("# Gap Report\n", encoding="utf-8")
    meta = asyncio.run(ms.add_to_run_dir(run, _paper(), r, repo="https://github.com/o/r"))
    assert meta["drafted"] == 1
    issue = (run / "issue_draft.md").read_text(encoding="utf-8")
    assert "Thank you" in issue and "All runs use 8 worker threads." in issue and "github.com/o/r" in issue
    assert "sk-abcdef" not in issue and "API_KEY" not in issue
    assert "never posted" in issue
    saved = json.loads((run / "gap_report.json").read_text(encoding="utf-8"))
    assert saved["claims"][0]["missing_sentence"]["page"] == 2 and "missing_sentence" not in saved["claims"][1]
    md = (run / "gap_report.md").read_text(encoding="utf-8")
    assert "The sentence the paper was missing" in md and "drafted by GapFinder" in md
    # running again replaces rather than duplicates the section
    asyncio.run(ms.add_to_run_dir(run, _paper(), r))
    assert (run / "gap_report.md").read_text(encoding="utf-8").count("The sentence the paper was missing") == 1


def test_no_issue_file_when_nothing_drafted(tmp_path):
    r, calls = _router(tmp_path)
    run = tmp_path / "run"
    run.mkdir()
    (run / "gap_report.json").write_text(json.dumps(_report("Unexplained")), encoding="utf-8")
    asyncio.run(ms.add_to_run_dir(run, _paper(), r))
    assert not (run / "issue_draft.md").exists() and calls == []


def test_spend_cap_honoured(tmp_path, monkeypatch):
    monkeypatch.setenv("GF_SPEND_CAP_USD", "0.0000001")
    r, calls = _router(tmp_path)
    rep = _report("Explained", "Explained")
    meta = asyncio.run(ms.draft_missing_sentences(rep, _paper(), r))
    assert calls == [] and meta["drafted"] == 0
    assert [s["reason"] for s in meta["skipped"]] == ["spend cap", "spend cap"]


def test_no_setup_paragraph_means_no_call(tmp_path):
    r, calls = _router(tmp_path)
    rep = _report("Explained")
    paper = PaperText(path=Path("p.txt"), pages=[Page(1, "Too short.")])
    meta = asyncio.run(ms.draft_missing_sentences(rep, paper, r))
    assert calls == [] and meta["skipped"][0]["claim_id"] == "C0"


def test_off_by_default():
    # search has the flag, defaulting to False; no other path calls the module
    import sys
    from unittest import mock

    parsed = {}
    with mock.patch.object(cli.asyncio, "run", lambda coro: (coro.close(), 0)[1]):
        orig = cli.cmd_search

        def grab(args):
            parsed["a"] = args
            return orig(args)

        with mock.patch.object(cli, "cmd_search", grab):
            cli.main(["search", "--spec", "s.yaml", "--targets", "t.json", "--assumptions", "a.json"])
    assert parsed["a"].missing_sentence is False
    src = Path(cli.__file__).read_text(encoding="utf-8")
    assert src.count("args.missing_sentence") == 1  # only gate
