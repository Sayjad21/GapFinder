"""Reporting-rule hypotheses from the runs already made (plan D1.2): zero extra runs.

The program printed its metric at every epoch and the harness's emitter summarised each run's trajectory
(`<metric>__x_best`, `__x_bestval`, `__x_attarget`, `__x_atbestval`, `__x_last5`, `__x_maxrun`, `__x_medrun`). A
paper's number can be any of these rather than the value at the end of training averaged over seeds:

| rule | what the paper did | a flaw? |
|---|---|---|
| `best` | each metric's best epoch, chosen with the test labels | yes: selection on the test set |
| `best+attarget` | one epoch chosen by the headline metric on the test labels, every metric read there | yes |
| `bestval` | every metric at the epoch where the validation score is best (early stopping, model selection) | no: a protocol the code doesn't implement |
| `last5` | the mean of the last epochs | no |
| `maxrun` | the best run (seed) of several, not their mean | yes: best-of-N (Dodge et al. 2019, "Show your work") |
| `medrun` | the median run | no |

Each rule is one hypothesis, scored on every claim at once (diagnose.core): a rule must explain the target and the
held-outs together, with the same choice, to rank high. Rules whose statistics the runs don't have (one value per
run, one run per cell) are not proposed.
"""

from __future__ import annotations

from gapfinder.diagnose.core import Hypothesis, Prediction

# rule -> (what it says, flaw?, prior)
RULES = {
    "best": ("the paper reports each metric's best epoch, chosen with the test labels", True, 0.10),
    "best+attarget": ("the paper picks one epoch by the headline metric on the test labels and reports every metric "
                      "there", True, 0.08),
    "bestval": ("the paper reports the epoch with the best validation score (early stopping or model selection)",
                False, 0.12),
    "last5": ("the paper reports the mean of the last epochs", False, 0.03),
    "maxrun": ("the paper reports the best run (seed) of several, not their mean", True, 0.06),
    "medrun": ("the paper reports the median run", False, 0.02),
}
CHECKS = {
    "best": "print the test metric per epoch: is the paper's number the maximum over epochs rather than the last value?",
    "best+attarget": "read every metric at the epoch where the headline test metric peaks",
    "bestval": "add early stopping on the validation score (or read the test metric at the best validation epoch)",
    "last5": "average the last epochs",
    "maxrun": "compare the paper's number with the best of the seeds rather than their mean",
    "medrun": "compare with the median over the seeds",
}


def _vals(branches, key: str) -> list[float]:
    return [b.parsed_metrics[key] for b in branches if key in (b.parsed_metrics or {})]


def _stat_for(rule: str, metric: str, is_target: bool) -> list[str]:
    """The emitter statistics a rule reads for one claim, in order of preference (the first present is used)."""
    if rule == "best":
        return [f"{metric}__x_best"]
    if rule == "best+attarget":
        return [f"{metric}__x_best"] if is_target else [f"{metric}__x_attarget"]
    if rule == "bestval":
        return [f"{metric}__x_bestval"] if is_target else [f"{metric}__x_atbestval", f"{metric}__x_bestval"]
    return [f"{metric}__x_{rule}"]


def applicable(rule: str, branches, target_metric: str) -> bool:
    lens = _vals(branches, f"{target_metric}__x_len")
    if rule in ("best", "best+attarget", "bestval", "last5"):
        if not lens or max(lens) <= 1:  # one value per run: no trajectory to choose from
            return False
    if rule in ("maxrun", "medrun"):
        hi, lo = _vals(branches, f"{target_metric}__x_maxrun"), _vals(branches, f"{target_metric}__x_minrun")
        if not hi or all(abs(a - b) < 1e-12 for a, b in zip(hi, lo)):  # one run per cell, or identical runs
            return False
    keys = _stat_for(rule, target_metric, True)
    return len(_vals(branches, keys[0])) >= 2


def reporting_hypotheses(branches, claims: list[tuple[str, str, bool]], sd_floor: dict[str, float]) -> list[Hypothesis]:
    """`claims`: (claim id, metric, is_target), the target first. `branches`: the naive runs. `sd_floor`: claim id ->
    the smallest spread to assume (the naive band's)."""
    target_metric = next(m for _, m, t in claims if t)
    out = []
    for rule, (title, flaw, prior) in RULES.items():
        if not applicable(rule, branches, target_metric):
            continue
        preds, used = {}, {}
        for cid, metric, is_target in claims:
            for key in _stat_for(rule, metric, is_target):
                vals = _vals(branches, key)
                if len(vals) >= 2:
                    preds[cid] = Prediction.from_values(vals, sd_floor.get(cid, 0.0))
                    used[cid] = key
                    break
        if len(preds) < len(claims):
            # a rule the runs can't read on every claim isn't proposed: scored on fewer claims it would look likelier
            # than the rules that can (and take their share of the posterior)
            continue
        h = Hypothesis(f"reporting:{rule}", "reporting", title, prior, preds,
                       detail={"rule": rule, "flaw": flaw, "statistics": used},
                       evidence=[f"computed from the {len(branches)} naive runs' printed trajectories (no extra run)"],
                       check=CHECKS[rule])
        out.append(h)
    return out
