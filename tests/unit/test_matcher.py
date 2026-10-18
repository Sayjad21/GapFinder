"""Paper-versus-code constant matcher (search/matcher.py): deterministic leads where a stated value differs."""

from gapfinder.ledger.schemas import Assumption, Evidence
from gapfinder.search.matcher import match_constants


def _a(knob, value, quote):
    return Assumption(id="A1", knob=knob, layer="config", paper_value=value, prior_score=0.5,
                      evidence=[Evidence(kind="paper", ref="p.5", quote=quote)] if quote else [])


def test_stated_values_that_differ_from_named_literals_become_leads(tmp_path):
    (tmp_path / "prep.py").write_text(
        "def mask_edges(adj, test_percent=30., val_percent=20.):\n    return adj\n", encoding="utf-8")
    (tmp_path / "train.py").write_text(
        "from prep import mask_edges\nepochs = 200\nhidden = 32\nmask_edges(None)\n", encoding="utf-8")
    leads = match_constants([
        _a("test_split", "10%", "we hold out 10% of the edges for testing"),           # other words: no lead
        _a("test_percent", "10%", "we hold out 10% of the edges for testing"),         # differs: lead, value 10
        _a("num_epochs", "200", "trained for 200 epochs"),                             # already as stated
        _a("hidden_units", "64", "a hidden layer of 64 units"),                        # one word more: lead
        _a("val_percent", "5%", ""),                                                   # no quote: not evidence
        _a("dropout", "unstated", "dropout"),
    ], tmp_path)
    got = {(x["name"], x["value"], x["paper_value"]) for x in leads}
    assert got == {("test_percent", "30.0", "10.0"), ("hidden", "32", "64")}
    lead = next(x for x in leads if x["name"] == "test_percent")
    assert lead["file"] == "prep.py" and lead["line"] == 1 and lead["source"] == "matcher"
    assert lead["quote"] == "we hold out 10% of the edges for testing"


def test_a_percentage_matches_a_fraction_in_the_code(tmp_path):
    (tmp_path / "run.py").write_text("test_frac = 0.1\nval_frac = 0.2\n", encoding="utf-8")
    leads = match_constants([_a("test_frac", "10%", "10% of the nodes for test"),
                             _a("val_frac", "5%", "5% for validation")], tmp_path)
    assert [(x["name"], x["paper_value"]) for x in leads] == [("val_frac", "0.05")]
