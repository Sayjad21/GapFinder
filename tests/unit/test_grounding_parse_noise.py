import random
import statistics

import pytest

from gapfinder.ledger.grounding import Grounder
from gapfinder.ledger.schemas import Assumption, Claim, Evidence
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.noise import effect_in_noise_units, noise_band, starved
from gapfinder.sandbox.parse import UngroundedValueError, ground_values, parse_db_bench, parse_kv
from gapfinder.sandbox.spec import diff_guard
from gapfinder.sandbox.tree import CheckpointTree, Node

PAPER = """We set the memtable size to 2 MB and the size ra-
tio T to 10. RusKey achieves up to 4x lower latency on write-heavy workloads."""


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "opts.h").write_text("int x;\nsize_t write_buffer_size = 64 << 20;\n")
    return tmp_path


def _claim(quote, cid="C1"):
    return Claim(id=cid, figure_or_table=None, metric="m", type="ratio", quote=quote)


def test_grounding_accepts_real_quote_across_hyphenation(repo):
    g = Grounder(PAPER, repo)
    rep = g.check_claims([_claim("the size ratio T to 10")])
    assert len(rep.kept) == 1


def test_grounding_rejects_planted_fake_quote(repo):
    g = Grounder(PAPER, repo)
    rep = g.check_claims([_claim("RusKey achieves up to 10x lower latency")])
    assert rep.kept == [] and rep.dropped[0][0] == "C1"


def test_grounding_rejects_fake_file_line(repo):
    g = Grounder(PAPER, repo)
    assert g.code_ref_ok("opts.h:2", "write_buffer_size")
    assert not g.code_ref_ok("opts.h:1", "write_buffer_size")  # wrong line
    assert not g.code_ref_ok("missing.h:2", "write_buffer_size")  # no file
    assert not g.code_ref_ok("opts.h:99", "write_buffer_size")  # past EOF
    assert not g.code_ref_ok("../outside.h:1", None)  # escapes repo


def test_grounding_drops_assumption_with_only_fake_evidence(repo):
    g = Grounder(PAPER, repo)
    good = Assumption(id="A1", knob="write_buffer_size", layer="config", paper_value="2 MB", prior_score=0.5,
                      evidence=[Evidence(kind="code", ref="opts.h:2", quote="write_buffer_size"),
                                Evidence(kind="paper", ref="p.1", quote="memtable size to 2 MB")])
    fake = Assumption(id="A2", knob="bloom_bits", layer="config", paper_value="unstated", prior_score=0.5,
                      evidence=[Evidence(kind="code", ref="opts.h:2", quote="bloom_bits")])
    rep = g.check_assumptions([good, fake])
    assert [a.id for a in rep.kept] == ["A1"] and rep.dropped == [("A2", "no grounded evidence")]


# ---------------------------------------------------------------------- parser

DB_BENCH = """fillrandom   :       2.345 micros/op 426439 ops/sec 23.450 seconds 10000000 operations;   47.2 MB/s
readrandom   :       5.100 micros/op 196078 ops/sec;
rocksdb.compact.write.bytes COUNT : 123456789
"""


def test_parse_db_bench():
    m = parse_db_bench(DB_BENCH)
    assert m["fillrandom.micros_per_op"] == 2.345
    assert m["fillrandom.ops_per_sec"] == 426439
    assert m["fillrandom.mb_per_s"] == 47.2
    assert m["readrandom.ops_per_sec"] == 196078
    assert m["rocksdb.compact.write.bytes"] == 123456789
    assert ground_values(m, DB_BENCH) == m


def test_parser_rejects_hallucinated_value():
    log = "score: 12.5\nwrite_amp: 3.0\n"
    parsed = parse_kv(log)
    assert ground_values(parsed, log)
    with pytest.raises(UngroundedValueError):
        ground_values({**parsed, "score": 13.7}, log)  # what an LLM might invent


# ----------------------------------------------------------------------- noise


def test_noise_band_within_30pct_of_true_spread():
    """With known injected noise, 2xMAD over 5 runs should track 2x(0.6745 sigma) to +-30% on median."""
    sigma, true_band = 2.0, 2 * 0.6745 * 2.0
    rng = random.Random(7)
    estimates = [noise_band("m", [100 + rng.gauss(0, sigma) for _ in range(5)]).band for _ in range(400)]
    est = statistics.median(estimates)
    assert abs(est - true_band) / true_band < 0.30


def test_noise_band_floor_and_effect_units():
    nb = noise_band("wamp", [5.0, 5.0, 5.0, 5.0, 5.0], floor_frac=0.01)
    assert nb.band == pytest.approx(0.05)
    assert effect_in_noise_units(naive_gap=1.0, branch_gap=0.1, band=0.3) == pytest.approx(3.0)
    assert effect_in_noise_units(naive_gap=1.0, branch_gap=1.5, band=0.5) < 0  # decoy moves it the wrong way


def test_starved_flags_outliers():
    assert starved([10, 12, 11, 200, 9]) == [False, False, False, True, False]


# ------------------------------------------------------------ diff guard, replay


def test_diff_guard_rejects_source_edits():
    assert diff_guard(["configs/a.yaml", "out/x.log"], ["configs/", "out/"]) == []
    assert diff_guard(["db/compaction/compaction_picker_flex.cc"], ["configs/"]) == [
        "db/compaction/compaction_picker_flex.cc"
    ]
    assert diff_guard(["opts/a.ini"], ["opts/*.ini"]) == []


def test_replay_rebuilds_identical_tree(tmp_path):
    log = EventLog(tmp_path / "ev.jsonl")
    live = CheckpointTree()
    for n in [Node("s", None, "source", tag="gf/x/source"), Node("b", "s", "built"), Node("l", "b", "loaded"),
              Node("x1", "l", "branch", {"alpha": "2"}), Node("x2", "l", "branch", {"beta": "1"})]:
        live.add(n)
        log.emit("checkpoint", node=n.__dict__)
    log.emit("note", msg="noise")
    replayed = CheckpointTree.replay(log.read())
    assert replayed.to_dict() == live.to_dict()


def test_grounding_tolerates_pdf_hyphen_and_math_spacing():
    g = Grounder("in the read-\nheavy workload Lerp selects 𝐾= 4 on the balanced workload")
    assert g.quote_in_paper("in the read-heavy workload Lerp selects K = 4 on the balanced")
    assert not g.quote_in_paper("in the read-heavy workload Lerp selects K = 5 on the balanced")


@pytest.mark.parametrize("paper,code,expected", [
    ("unstated", "64", "unstated"),
    ("100000000", "100000000", "stated_matches"),
    ("100 million", "100000000", "stated_matches"),
    ("2MB", "2097152", "stated_matches"),
    ("true", "false", "stated_code_differs"),
    ("8", "8.0", "stated_matches"),
    ("4", "8", "stated_code_differs"),
    ("DDPG actor", "greedy critic", "stated_code_differs"),  # unparseable: model's label kept
])
def test_derive_status(paper, code, expected):
    from gapfinder.ledger.assumptions import derive_status

    assert derive_status(paper, code, "stated_code_differs") == expected


def test_stated_paper_value_needs_paper_quote(repo):
    g = Grounder(PAPER, repo)
    a = Assumption(id="A9", knob="write_buffer_size", layer="config", paper_value="64", prior_score=0.5,
                   status="stated_matches",
                   evidence=[Evidence(kind="code", ref="opts.h:2", quote="write_buffer_size")])
    rep = g.check_assumptions([a])
    assert rep.kept[0].paper_value == "unstated" and rep.kept[0].status == "unstated"


def test_wrong_page_ref_is_corrected_not_rejected(repo):
    pages = {1: "intro text here", 2: "We set the memory buffer size to 2MB for all runs."}
    g = Grounder(" ".join(pages.values()), repo, pages=pages)
    a = Assumption(id="A1", knob="write_buffer_size", layer="config", paper_value="2 MB", prior_score=0.5,
                   evidence=[Evidence(kind="paper", ref="p.7", quote="set the memory buffer size to 2MB")])
    kept = g.check_assumptions([a]).kept[0]
    assert kept.paper_value == "2 MB" and kept.evidence[0].ref == "p.2"
    c = g.check_claims([_claim("set the memory buffer size to 2MB")]).kept[0]
    assert c.page == 2


def test_tree_handles_content_addressed_noop_stage():
    """A build check that changes no files returns its parent's ID (spike S2). Regression: infinite loop."""
    t = CheckpointTree()
    t.add(Node("img-1", None, "source"))
    t.add(Node("img-1", "img-1", "built"))  # no-op stage: same ID as its parent
    t.add(Node("img-2", "img-1", "loaded"))
    assert t.find_stage("source") == "img-1" and t.find_stage("built") == "img-1"
    assert t.find_stage("loaded") == "img-2"
    assert t.lineage_changes("img-2") == {}  # terminates
    t.nodes["img-3"] = Node("img-3", "img-3", "branch")  # even a self-parent can't loop forever
    assert t.lineage_changes("img-3") == {}


def test_a_stated_number_must_appear_in_a_paper_quote(repo):
    """blind-2: the ledger wrote alpha_l's code default (2) as the paper's value, backed by a paper quote that
    held no number; the search then dropped the true cause as "stated and matching". Now it's unstated."""
    paper = "with a scaled cosine error as the reconstruction criterion. We set the size ratio T to 10."
    g = Grounder(paper, repo)

    def asm(value, quote):
        return Assumption(id="A1", knob="alpha_l", layer="config", paper_value=value, code_default="2",
                          candidate_values=[], prior_score=0.5, status="stated_matches",
                          evidence=[Evidence(kind="paper", ref="p.4", quote=quote)])

    rep = g.check_assumptions([asm("2.0 (pow coefficient for sce loss)", "with a scaled cosine error")])
    assert rep.kept[0].paper_value == "unstated" and rep.kept[0].status == "unstated"
    assert "no paper quote contains that number" in rep.dropped[0][1]
    ok = g.check_assumptions([asm("10", "We set the size ratio T to 10")])
    assert ok.kept[0].paper_value == "10" and not ok.dropped
    words = g.check_assumptions([asm("scaled cosine error", "with a scaled cosine error")])
    assert words.kept[0].paper_value == "scaled cosine error"  # no number: the quote rule as before


def test_hyperparameter_tables_are_found_anywhere_in_the_paper():
    from gapfinder.ledger.assumptions import hyperparameter_tables

    text = ("1 Introduction\nWe study masking.\nTable 1: Dataset statistics\nDataset\nCora\n2708\n"
            "A Appendix\nTable 8: Statistics and hyper-parameters for graph classification datasets.\n"
            "Dataset\nCOLLAB\nScaling factor\n1\nmasking rate\n0.75\nTable 9: Molecular datasets\nZINC\n")
    tabs = hyperparameter_tables(text)
    assert len(tabs) == 1 and tabs[0].startswith("Table 8:") and "Scaling factor\n1" in tabs[0]
    assert "Table 9" not in tabs[0]  # stops at the next caption
