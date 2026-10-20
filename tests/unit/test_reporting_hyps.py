"""Reporting rules (gapfinder/diagnose/reporting.py): a rule the runs can't read on every claim isn't proposed."""

from types import SimpleNamespace

from gapfinder.diagnose.reporting import reporting_hypotheses


def _runs(**stats):
    return [SimpleNamespace(parsed_metrics={k: v + 0.01 * i for k, v in stats.items()}) for i in range(3)]


def test_a_rule_without_a_statistic_for_a_held_out_is_not_proposed():
    runs = _runs(acc=70.0, acc__x_len=20, acc__x_best=75.0, f1__x_best=66.0, acc__x_attarget=75.0)
    hyps = reporting_hypotheses(runs, [("C1", "acc", True), ("C2", "f1", False)], {"C1": 0.5, "C2": 0.5})
    rules = {h.detail["rule"] for h in hyps}
    assert "best" in rules  # both claims have a best-epoch statistic
    assert "best+attarget" not in rules  # f1 at the target's best epoch was never recorded
