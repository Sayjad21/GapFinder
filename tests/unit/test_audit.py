"""Audit of the reproduction (gapfinder/search/audit.py): what a matching number doesn't show."""

from types import SimpleNamespace

from gapfinder.ledger.schemas import Assumption, Evidence
from gapfinder.search.audit import audit, audit_markdown, comparable
from gapfinder.search.engine import Target


class _Band:
    def __init__(self, band):
        self.band = band


def _search(tmp_path, naive, bands, targets, unmapped=()):
    s = SimpleNamespace(targets=targets, naive=naive, bands={m: _Band(b) for m, b in bands.items()},
                        spec=SimpleNamespace(code_root=lambda: tmp_path, knobs={}),
                        _unmapped_assumptions=list(unmapped), unmapped=[a.knob for a in unmapped])
    s.gap = lambda t, c: (naive[t.metric] - t.paper_value) / abs(t.paper_value)
    s.band = lambda t: s.bands[t.metric].band / abs(t.paper_value)
    return s


def test_comparable_metrics_differ_in_one_word():
    assert comparable("alpha_x_acc", "beta_x_acc") and comparable("m_d1_f1", "m_d2_f1")
    assert not comparable("alpha_x_acc", "alpha_x_acc") and not comparable("a_acc", "b_c_acc")
    assert not comparable("alpha_x_acc", "beta_y_acc")


def test_held_out_misses_reversed_comparisons_leakage_and_stated_settings(tmp_path):
    (tmp_path / "train.py").write_text(
        "best_score, best_epoch = 0, 0\n"
        "for epoch in range(10):\n"
        "    score = evaluate(model, test_data)\n"
        "    if score > best_score:\n"
        "        best_score, best_epoch = score, epoch\n", encoding="utf-8")
    targets = [Target("T", "alpha_x_acc", 80.0), Target("H1", "alpha_y_acc", 70.0, held_out=True),
               Target("H2", "beta_y_acc", 68.0, held_out=True), Target("H3", "beta_x_acc", 78.0, held_out=True)]
    naive = {"alpha_x_acc": 80.1, "alpha_y_acc": 67.0, "beta_y_acc": 68.2, "beta_x_acc": 78.1}
    bands = {m: 0.5 for m in naive}
    stated = Assumption(id="A1", knob="evaluation convention", layer="config", paper_value="segment adjustment",
                        prior_score=0.8, evidence=[Evidence(kind="paper", ref="p.6", quote="We adopt the adjustment")])
    unstated = Assumption(id="A2", knob="cudnn", layer="environment", paper_value="unstated", prior_score=0.9)
    a = audit(_search(tmp_path, naive, bands, targets, [stated, unstated]), [])
    assert [x["claim"] for x in a["held_out"]] == ["H1"]  # 67 vs 70 is outside ±0.5; the others are inside
    # the paper says alpha_y 70 > beta_y 68; measured 67.0 < 68.2, beyond the combined noise (0.71)
    assert [x["claims"] for x in a["comparisons"]] == [["H1", "H2"]]
    assert a["leakage"] and a["leakage"][0]["file"] == "train.py"
    assert [x["setting"] for x in a["stated_untestable"]] == ["evaluation convention"]
    md = "\n".join(audit_markdown(a))
    assert "## Audit of the reproduction" in md and "selects its result by the test score" in md
    assert "Comparisons the runs reverse" in md and "We adopt the adjustment" in md


def test_a_clean_reproduction_has_no_audit_section(tmp_path):
    targets = [Target("T", "a_acc", 80.0), Target("H", "a_f1", 70.0, held_out=True)]
    naive = {"a_acc": 80.0, "a_f1": 70.1}
    a = audit(_search(tmp_path, naive, {m: 0.5 for m in naive}, targets), [])
    assert not any(a.values()) and audit_markdown(a) == []
