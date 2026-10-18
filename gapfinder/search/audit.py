"""Audit of the reproduction: what a reproduced number doesn't tell you. No runs, no model calls.

devbatch-2's three papers (NCF, PyG GAT vs GCN, Anomaly Transformer) all reproduced their target within noise,
and each report said nothing more, though each had something to say:
- NCF picks its reported epoch by the test-set score (`if hr > best_hr` over test evaluations);
- PyG's held-out CiteSeer numbers reverse the paper's ranking (GCN 71.1 beats GAT 70.8, against the paper's
  72.5 vs 70.3);
- Anomaly Transformer's paper states an evaluation convention (point adjustment), which the ledger extracted
  and the harness can't vary.

A reproduction that matches the paper reproduces its protocol too, flaws included. So every report now carries
four checks, whatever the target's label:
1. held-out claims outside noise in the naive runs;
2. comparisons the paper makes that the naive runs reverse beyond noise: two claims on metrics whose names
   differ in one word (`gat_cora_acc` and `gcn_cora_acc`);
3. static findings that the code selects a result by its test score (`code_checks`, selection_in_code on test
   data), shown even when nothing is out of space;
4. settings the paper states, with a verbatim quote, that this harness can't vary: they are part of what the
   number means.

These are findings to read, not attributions: nothing here was tested.
"""

from __future__ import annotations

import math


def _tokens(metric: str) -> list[str]:
    return metric.lower().split("_")


def comparable(a: str, b: str) -> bool:
    """Two metrics that differ in exactly one name word: the same measure of two methods (or two datasets)."""
    ta, tb = _tokens(a), _tokens(b)
    return a != b and len(ta) == len(tb) and sum(x != y for x, y in zip(ta, tb)) == 1


def audit(search, results) -> dict:
    out: dict = {"held_out": [], "comparisons": [], "leakage": [], "stated_untestable": []}
    targets = [t for t in search.targets if not getattr(t, "relation", None) and not math.isnan(t.paper_value)]
    naive = search.naive
    bands = search.bands

    # 1. held-out claims outside noise
    for t in targets:
        if not t.held_out or t.metric not in naive or t.metric not in bands:
            continue
        g = search.gap(t, {})
        b = search.band(t)
        if g is not None and abs(g) > b:
            out["held_out"].append({"claim": t.claim_id, "metric": t.metric, "paper": t.paper_value,
                                    "measured": naive[t.metric], "gap": g, "band": b,
                                    "tuned_separately": bool(getattr(t, "tuned_separately", False))})

    # 2. comparisons the naive runs reverse
    seen = set()
    for a in targets:
        for b in targets:
            key = tuple(sorted((a.claim_id, b.claim_id)))
            if key in seen or not comparable(a.metric, b.metric) or a.paper_value <= b.paper_value:
                continue
            seen.add(key)
            if a.metric not in naive or b.metric not in naive or a.metric not in bands or b.metric not in bands:
                continue
            diff = naive[a.metric] - naive[b.metric]
            noise = math.hypot(bands[a.metric].band, bands[b.metric].band)
            if diff < -noise:  # the paper says a > b; the runs say b > a, beyond noise
                out["comparisons"].append({
                    "paper_says": f"{a.metric} {a.paper_value:g} > {b.metric} {b.paper_value:g}",
                    "measured": f"{a.metric} {naive[a.metric]:.4g} < {b.metric} {naive[b.metric]:.4g}",
                    "margin": diff, "noise": noise, "claims": [a.claim_id, b.claim_id]})

    # 3. selection on test data, from the static checks
    root = search.spec.code_root()
    if root is not None:
        from gapfinder.ingest.code_checks import code_checks

        try:
            leads = code_checks(root, set(search.spec.knobs), limit=60)
        except Exception:  # an aid: unreadable code leaves the audit without this part
            leads = []
        for x in leads:
            if x.family == "selection_in_code" and "TEST data" in x.detail:
                out["leakage"].append({"file": x.file, "line": x.line, "code": x.code, "detail": x.detail})

    # 4. paper-stated settings this harness can't vary
    for a in sorted(getattr(search, "_unmapped_assumptions", []), key=lambda a: -a.prior_score):
        if a.knob not in search.unmapped or str(a.paper_value).strip().lower().startswith("unstated"):
            continue
        quote = next((e.quote for e in a.evidence if e.kind == "paper" and e.quote), None)
        if quote and a.prior_score >= 0.5:
            out["stated_untestable"].append({"setting": a.knob, "paper_value": a.paper_value, "quote": quote,
                                             "ref": next((e.ref for e in a.evidence if e.kind == "paper"), "")})
        if len(out["stated_untestable"]) >= 6:
            break
    return out


def audit_markdown(a: dict | None) -> list[str]:
    if not a or not any(a.values()):
        return []
    out = ["", "## Audit of the reproduction",
           "What a matching number doesn't show. Static and descriptive: nothing below was tested."]
    if a["leakage"]:
        out.append("- **The code selects its result by the test score** (the reported number is then optimistic):")
        out += [f"  - `{x['file']}:{x['line']}`: {x['detail']}" for x in a["leakage"][:6]]
    if a["comparisons"]:
        out.append("- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):")
        out += [f"  - paper: {x['paper_says']}; measured: {x['measured']} (margin {x['margin']:.3g}, noise "
                f"{x['noise']:.3g})" for x in a["comparisons"][:6]]
    if a["held_out"]:
        out.append("- **Held-out claims outside noise:**")
        out += [f"  - {x['claim']} (`{x['metric']}`): paper {x['paper']:g}, measured {x['measured']:.4g} "
                f"({x['gap']:+.1%}, band ±{x['band']:.1%})" + (" (tuned separately in the paper)"
                                                                  if x["tuned_separately"] else "")
                for x in a["held_out"][:8]]
    if a["stated_untestable"]:
        out.append("- **The paper states these, and this harness can't vary them** (they are part of what the "
                   "number means):")
        out += [f"  - `{x['setting']}`: \"{x['quote'][:200]}\" ({x['ref']})" for x in a["stated_untestable"]]
    return out
