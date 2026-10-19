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
    assert "## Audit of the reproduction" in md and "How the code computes the reported number" in md
    assert "Comparisons the runs reverse" in md and "We adopt the adjustment" in md


def test_a_clean_reproduction_has_no_audit_section(tmp_path):
    targets = [Target("T", "a_acc", 80.0), Target("H", "a_f1", 70.0, held_out=True)]
    naive = {"a_acc": 80.0, "a_f1": 70.1}
    a = audit(_search(tmp_path, naive, {m: 0.5 for m in naive}, targets), [])
    assert not any(a.values()) and audit_markdown(a) == []


def test_a_paper_setting_a_prefixed_knob_covers_is_not_listed_as_untestable(tmp_path):
    from gapfinder.search.audit import _settable

    assert _settable("lr", {"gat_lr": 1, "gcn_lr": 1}) and _settable("dropout", {"gcn_dropout": 1})
    assert not _settable("adjustment_strategy", {"gat_lr": 1, "anormly_ratio": 1})


def test_one_flag_split_into_several_knobs_is_a_family():
    from gapfinder.search.engine import knob_family

    knobs = {"kmeans_synthetic_lmbda": 1, "kmeans_unequal_lmbda": 1, "kmedian_synthetic_lmbda": 1, "lmbda_tune": 1}
    assert knob_family("lmbda", knobs) == ["kmeans_synthetic_lmbda", "kmeans_unequal_lmbda", "kmedian_synthetic_lmbda"]
    assert knob_family("--lmbda (fairness weight)", knobs) == ["kmeans_synthetic_lmbda", "kmeans_unequal_lmbda",
                                                               "kmedian_synthetic_lmbda"]
    assert knob_family("lr", {"gat_lr": 1, "gcn_lr": 1}) == ["gat_lr", "gcn_lr"]
    assert knob_family("lr", {"lr": 1, "gat_lr": 1, "gcn_lr": 1}) == []  # the flag itself is a knob
    assert knob_family("tune", knobs) == []  # one match only is not a family


def test_the_papers_comparison_claims_are_checked_against_the_runs(tmp_path):
    from gapfinder.ledger.schemas import Claim
    from gapfinder.search.audit import paper_comparisons

    targets = [Target("T", "newnet_d1_acc", 83.0), Target("H1", "oldnet_d1_acc", 81.5, held_out=True),
               Target("H2", "newnet_d2_acc", 72.5, held_out=True), Target("H3", "oldnet_d2_acc", 70.3, held_out=True)]
    naive = {"newnet_d1_acc": 83.0, "oldnet_d1_acc": 81.3, "newnet_d2_acc": 70.8, "oldnet_d2_acc": 71.1}
    s = _search(tmp_path, naive, {m: 0.15 for m in naive}, targets)
    q = "NewNet improves upon OldNet (Smith et al.) by 1.5% and 1.6% on D1 and D2"
    s.claims = {"C1": Claim(id="C1", figure_or_table=None, metric="accuracy gain", reported_value=1.5, type="ratio",
                            conditions={"dataset": "D1", "baseline": "OldNet (Smith et al.)", "our_method": "NewNet"},
                            quote=q, page=8),
                "C2": Claim(id="C2", figure_or_table=None, metric="accuracy gain", reported_value=1.6, type="ratio",
                            conditions={"dataset": "D2", "baseline": "OldNet (Smith et al.)", "our_method": "NewNet"},
                            quote=q, page=8)}
    got = {x["claim"]: (x["a"], x["b"], x["holds"], x["reversed"]) for x in paper_comparisons(s)}
    assert got == {"C1": ("newnet_d1_acc", "oldnet_d1_acc", True, False),
                   "C2": ("newnet_d2_acc", "oldnet_d2_acc", False, True)}
