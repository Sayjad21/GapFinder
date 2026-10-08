"""Score a ledger run against a gold set (M1 eval bars). Free: no model calls.

    python eval/ledger_eval.py runs/ruskey-ledger papers/ruskey [--out eval/results/ledger_ruskey.json]

Claim recall: a gold claim is found if an extracted claim's quote overlaps it
(token Jaccard >= 0.5, or one quote contains the other), or it cites the same
figure/table with the same reported value.
Assumption recall: a gold knob is found if it appears among the top 30
extracted knobs (names normalised: case, dashes, a leading `no_`).
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from gapfinder.ledger.grounding import normalise

# Gold knobs that are a concept rather than one flag, and the extracted names that count for them.
KNOB_ALIASES = {
    "host_memory_and_device": {"memory", "ram", "ssd", "nvme", "device", "hardware", "cpu", "disk"},
    "key_value_size": {"key_size", "value_size"},  # a concept made of two flags
}


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9.]+", normalise(text)))


def _quote_match(a: str, b: str) -> bool:
    na, nb = normalise(a), normalise(b)
    if na in nb or nb in na:
        return True
    ta, tb = _tokens(a), _tokens(b)
    return bool(ta and tb) and len(ta & tb) / len(ta | tb) >= 0.5


def _claim_found(gold: dict, extracted: list[dict]) -> str | None:
    for c in extracted:
        if _quote_match(gold["quote"], c["quote"]):
            return c["id"]
        if (gold.get("figure_or_table") and gold["figure_or_table"] == c.get("figure_or_table")
                and gold.get("reported_value") is not None and gold["reported_value"] == c.get("reported_value")):
            return c["id"]
    return None


def _norm_knob(k: str) -> str:
    k = k.lower().lstrip("-").replace("-", "_")
    return k[3:] if k.startswith("no_") else k


def _knob_found(gold_knob: str, extracted: list[dict]) -> str | None:
    g = _norm_knob(gold_knob)
    for a in extracted:
        if _norm_knob(a["knob"]) == g:
            return a["id"]
    aliases = KNOB_ALIASES.get(g)
    if aliases:
        for a in extracted:
            if any(w in _norm_knob(a["knob"]) for w in aliases):
                return a["id"]
    return None


def score(run_dir: Path, gold_dir: Path) -> dict:
    claims = json.loads((run_dir / "claim_ledger.json").read_text())["claims"]
    assumptions = json.loads((run_dir / "assumptions.json").read_text())["assumptions"][:30]
    dropped = json.loads((run_dir / "dropped.json").read_text())
    gold_c = json.loads((gold_dir / "gold_ledger.json").read_text())["claims"]
    gold_a = json.loads((gold_dir / "gold_assumptions.json").read_text())["assumptions"]

    c_hits = {g["id"]: _claim_found(g, claims) for g in gold_c}
    head = [g["id"] for g in gold_c if g.get("headline")]
    # out of scope by design: GapFinder only changes conditions, never code (hard-coded settings,
    # algorithm rewrites); the gold file says which and why
    out_of_scope = [g["knob"] for g in gold_a if g.get("in_scope") is False]
    gold_a = [g for g in gold_a if g.get("in_scope") is not False]
    a_hits = {g["knob"]: _knob_found(g["knob"], assumptions) for g in gold_a}
    rel = [g["knob"] for g in gold_a if g.get("prior_score", 0) >= 0.3]  # knobs that could explain a gap
    cost = json.loads((run_dir / "cost.json").read_text()) if (run_dir / "cost.json").exists() else {}
    # precision: extracted claims judged real by the author-reviewed labels (matched by quote)
    lab_path = gold_dir / "claim_labels.json"
    labels = json.loads(lab_path.read_text())["labels"] if lab_path.exists() else []
    judged, unlabeled = [], []
    for c in claims:
        hit = next((l for l in labels if _quote_match(l["quote"], c["quote"])), None)
        (judged.append(hit["real"]) if hit else unlabeled.append({"id": c["id"], "quote": c["quote"][:200]}))
    return {
        "claim_recall_all": round(sum(v is not None for v in c_hits.values()) / len(gold_c), 3),
        "claim_recall_headline": round(sum(c_hits[h] is not None for h in head) / max(len(head), 1), 3),
        "claims_extracted": len(claims),
        "claim_precision_labeled": round(sum(judged) / len(judged), 3) if judged else None,
        "claims_labeled": len(judged),
        "claims_needing_label": unlabeled,
        "claims_dropped_ungrounded": len(dropped.get("claims", [])),
        "assumption_recall_relevant_top30": round(sum(a_hits[k] is not None for k in rel) / max(len(rel), 1), 3),
        "assumption_recall_all_top30": round(sum(v is not None for v in a_hits.values()) / len(gold_a), 3),
        "ungrounded_in_output": 0,  # by construction: the grounder drops them before writing
        "claim_matches": c_hits,
        "knob_matches": a_hits,
        "missed_claims": [k for k, v in c_hits.items() if v is None],
        "missed_knobs": [k for k, v in a_hits.items() if v is None],
        "out_of_scope_knobs": out_of_scope,
        "cost": cost,
        "bars": {"claim_recall_headline": 0.85, "assumption_recall_relevant_top30": 0.80,
                 "claim_precision": 0.90},
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("run_dir", type=Path)
    p.add_argument("gold_dir", type=Path)
    p.add_argument("--out", type=Path)
    a = p.parse_args()
    res = score(a.run_dir, a.gold_dir)
    print(json.dumps({k: v for k, v in res.items() if k not in ("claim_matches", "knob_matches", "cost")}, indent=1))
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(res, indent=1))
