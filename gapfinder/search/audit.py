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
    out: dict = {"held_out": [], "comparisons": [], "leakage": [], "stated_untestable": [],
                 "paper_comparisons": paper_comparisons(search),
                 "protocol_tests": list(getattr(search, "protocol_results", []) or [])}
    tested = {(x["file"], x["line"]) for x in out["protocol_tests"]}
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
            if ((x.family == "selection_in_code" and "TEST data" in x.detail)
                    or x.family in ("label_in_prediction", "eval_switch")) \
                    and (x.file, x.line) not in tested:
                out["leakage"].append({"file": x.file, "line": x.line, "code": x.code, "detail": x.detail})

    # 4. paper-stated settings this harness can't vary
    for a in sorted(getattr(search, "_unmapped_assumptions", []), key=lambda a: -a.prior_score):
        if a.knob not in search.unmapped or str(a.paper_value).strip().lower().startswith("unstated"):
            continue
        if _settable(a.knob, search.spec.knobs):
            continue  # a knob covers it under a longer name (`lr` -> `gat_lr`): it is variable, just not named so
        quote = next((e.quote for e in a.evidence if e.kind == "paper" and e.quote), None)
        if quote and a.prior_score >= 0.5:
            out["stated_untestable"].append({"setting": a.knob, "paper_value": a.paper_value, "quote": quote,
                                             "ref": next((e.ref for e in a.evidence if e.kind == "paper"), "")})
        if len(out["stated_untestable"]) >= 6:
            break
    return out


_STOP = {"ours", "our", "the", "a", "an", "of", "and", "et", "al", "model", "method", "best", "baseline", "proposed",
         "variant", "with", "without", "on", "for", "in", "by"}


def _words(text: str) -> set[str]:
    import re

    return {w for w in re.findall(r"[a-z][a-z0-9]*", str(text).lower()) if w not in _STOP and len(w) >= 2}


def paper_comparisons(search) -> list[dict]:
    """The paper's comparison claims ("we improve upon GCN by 1.5% on Cora": a ledger ratio claim with the method,
    the baseline and the dataset in its conditions), each matched to the two measured claims it compares (the
    metrics that name the method and the baseline and agree on everything else), and checked: does the measured
    margin have the paper's sign, and is it within noise of the paper's margin? (devbatch-2 PyG: the paper's GAT
    over GCN on Citeseer, +1.6, measured -0.3.)"""
    claims = getattr(search, "claims", None) or {}
    targets = [t for t in search.targets if not getattr(t, "relation", None) and t.metric in search.naive]
    out = []
    for c in claims.values():
        if str(getattr(c.type, "value", c.type)) != "ratio" or c.reported_value is None:
            continue
        cond = {k.lower(): v for k, v in (c.conditions or {}).items()}
        base = next((v for k, v in cond.items() if "baseline" in k or k in ("compared_to", "versus", "vs")), None)
        ours = next((v for k, v in cond.items() if k in ("our_method", "method", "model", "ours", "proposed")), None)
        if not base or not ours:
            continue
        rest = set().union(*(_words(v) for k, v in cond.items() if v not in (base, ours))) if cond else set()
        bw, ow = _words(base) - _words(ours), _words(ours) - _words(base)
        pairs = []
        for a in targets:
            for b in targets:
                ta, tb = set(a.metric.lower().split("_")), set(b.metric.lower().split("_"))
                if a is b or not comparable(a.metric, b.metric) or not (ta & ow) or not (tb & bw):
                    continue
                if rest and not (ta & tb & rest):
                    continue  # the dataset (or another condition) must be the same one the claim names
                pairs.append((a, b))
        if len(pairs) != 1:
            continue  # none, or ambiguous: not reported
        a, b = pairs[0]
        m = search.naive[a.metric] - search.naive[b.metric]
        noise = math.hypot(search.bands[a.metric].band, search.bands[b.metric].band) if (
            a.metric in search.bands and b.metric in search.bands) else 0.0
        r = float(c.reported_value)
        sign_ok = (m > 0) == (r > 0) or abs(m) <= noise
        out.append({"claim": c.id, "quote": (c.quote or "")[:200], "page": c.page, "a": a.metric, "b": b.metric,
                    "paper_margin": r, "measured_margin": m, "noise": noise,
                    "holds": sign_ok and abs(m - r) <= max(noise, 0.25 * abs(r)),
                    "reversed": not sign_ok})
    return out


def _settable(name: str, knobs) -> bool:
    """Some knob's name holds every core word of `name` plus at most one more (`lr` ~ `gat_lr`, `dropout` ~
    `gcn_dropout`): the setting is variable in this harness under another name."""
    import re

    from gapfinder.search.engine import _core

    core = _core(re.sub(r"\s*\(.*$", "", name.strip()).replace(" ", "_"))
    return bool(core) and any(core <= _core(k) and len(_core(k) - core) <= 1 for k in knobs)


def audit_markdown(a: dict | None) -> list[str]:
    if not a or not any(a.values()):
        return []
    out = ["", "## Audit of the reproduction",
           "What a matching number doesn't show. The protocol tests below were run; the rest is static."]
    for x in a.get("protocol_tests") or []:
        moved = [c for c in x["claims"] if c["depends"]]
        if not x["runs"]:
            out.append(f"- **Found, but the test failed**: `{x['file']}:{x['line']}` {x['detail']}; with it switched "
                       f"off the program didn't finish ({x.get('failure', '')[:160]}). The code may assume it.")
            continue
        what = ("**Measured: the reported numbers depend on this code**" if moved else
                "Tested: switching this code off moved no claim beyond noise")
        out.append(f"- {what}: `{x['file']}:{x['line']}` {x['detail']}; switched off ({x['runs']} runs):")
        out += [f"  - {c['claim']} (`{c['metric']}`): paper {c['paper']:g}, as run {c['naive']:.4g}, without it "
                f"{c['without']:.4g}" + (f" (difference 95% CI [{c['ci'][0]:+.3g}, {c['ci'][1]:+.3g}])" if c["ci"] else "")
                for c in (moved or x["claims"])[:6]]
    if a["leakage"]:
        out.append("- **How the code computes the reported number** (test-score selection, label-based edits, "
                   "switches fixed for evaluation):")
        out += [f"  - `{x['file']}:{x['line']}`: {x['detail']}" for x in a["leakage"][:6]]
    if a["comparisons"]:
        out.append("- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):")
        out += [f"  - paper: {x['paper_says']}; measured: {x['measured']} (margin {x['margin']:.3g}, noise "
                f"{x['noise']:.3g})" for x in a["comparisons"][:6]]
    pc = a.get("paper_comparisons") or []
    if pc:
        out.append("- **The paper's own comparisons, as measured:**")
        out += [f"  - {x['claim']} (p.{x['page']}): \"{x['quote'][:140]}\"; {x['a']} minus {x['b']}: paper "
                f"{x['paper_margin']:+.3g}, measured {x['measured_margin']:+.3g} (noise {x['noise']:.2g}): "
                + ("**reversed**" if x["reversed"] else "holds" if x["holds"] else "**smaller than claimed**")
                for x in pc[:8]]
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
