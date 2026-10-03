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
