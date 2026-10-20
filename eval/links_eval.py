"""Paper-term to flag links on the dev set (plan D4.1-D4.4): $0, no model call.

    python eval/links_eval.py --scratch DIR

The link set: every ledger assumption on the dev cases whose name is not a spec knob, labelled by hand with the knob
(or knobs, for a flag split per model) it refers to, or None when no knob does. Development data: the builder chose
the labels, so this measures the retrieval, it is not blind evidence. Reported: recall at 1 and at 5 over the
linkable terms; the decisive links (taken without a model): how many, how many right, and how many made for a term
that no knob matches (the costly error).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = {  # case -> (spec, repo under --scratch)
    "gat": ("devset/gat/gat.yaml", "devbatch/gat/repo"),
    "gin": ("devset/gin/gin.yaml", "devbatch/gin/powerful-gnns"),
    "gmixup": ("devset/gmixup/gmixup.yaml", "devbatch/gmixup/repo"),
    "patchtst": ("devset/patchtst/patchtst.yaml", "devbatch/patchtst/src"),
    "pyg": ("devbatch2/pyg/pyg.yaml", "db2/pyg/repo"),
    "at": ("devbatch2/at/at.yaml", None),
    "ncf": ("devbatch2/ncf/ncf.yaml", None),
    "pygcn": ("devset/pygcn/pygcn.yaml", None),
    "vgae": ("devset/vgae/vgae.yaml", None),
}
LINKS = {
    "gat": {"num_attention_heads": {"n_heads"}, "l2_reg_lambda": {"l2_coef"}, "learning_rate": {"lr"},
            "early_stopping_patience": {"patience"}, "features_per_head": {"hid_units"},
            "activation_function": {"nonlinearity"}, "skip_connections": {"residual"},
            "use_sparse_implementation": {"sparse"}, "dropout_rate": None, "num_runs": None, "optimizer_type": None},
    "pyg": {"lr": {"gcn_lr", "gat_lr"}, "weight_decay": {"gcn_weight_decay", "gat_weight_decay"},
            "output_heads": {"gat_output_heads"}, "dropout": {"gcn_dropout", "gat_dropout"},
            "hidden": {"gcn_hidden", "gat_hidden"}, "heads": {"gat_heads"},
            "early_stopping": {"gcn_early_stopping", "gat_early_stopping"}, "epochs": {"gcn_epochs", "gat_epochs"},
            "dataset_splits": {"random_splits"}, "activation": None, "num_layers": None},
    "gin": {"readout function (sum vs mean)": {"graph_pooling_type"}, "Adam optimizer": {"lr"},
            "batch normalization": None, "--neighbor_pooling_type": None},
    "gmixup": {"lam_range": {"lam_lo", "lam_hi"}, "ge": None, "weight_decay": None},
    "patchtst": {"context_points": {"seq_len"}, "n_layers": {"e_layers"}, "n_epochs_finetune": {"train_epochs"},
                 "target_points": None, "mask_ratio": None, "n_epochs_pretrain": None},
    "at": {"loss weight lambda": {"k"}, "lambda_hyperparameter": {"k"},
           "threshold selection method (δ vs r)": {"anormly_ratio"}, "validation_set_for_threshold": {"anormly_ratio"},
           "early_stopping_criterion": None},
    "ncf": {"num_layers_mlp": {"layers"}, "negative_sampling_strategy": None, "topK": None},
    "pygcn": {"early_stopping_window": None, "num_layers": None},
    "vgae": {"sc_embedding_dim": None, "mask_test_edges_split": None},
}


def evaluate(scratch: Path) -> dict:
    import yaml

    from gapfinder.ingest.links import decisive, entities, link
    from gapfinder.sandbox.spec import Knob

    rows = []
    for case, (spec_rel, repo_rel) in CASES.items():
        spec_p = ROOT / "eval" / "external" / spec_rel
        d = yaml.safe_load(spec_p.read_text(encoding="utf-8"))
        knobs = {k: Knob(**v) for k, v in (d.get("knobs") or {}).items()}
        spec = type("S", (), {"knobs": knobs})()
        repo = scratch / repo_rel if repo_rel and (scratch / repo_rel).exists() else None
        ents = entities(spec, repo)
        led = json.loads((spec_p.parent / "ledger" / "assumptions.json").read_text(encoding="utf-8"))["assumptions"]
        by = {a["knob"]: a for a in led}
        for term, truth in LINKS[case].items():
            a = by.get(term)
            if a is None:
                continue
            ctx = " ".join([a.get("paper_value", "")] + [e["quote"] for e in a["evidence"] if e["kind"] == "paper"][:2])
            cands = link(term, ctx, ents)
            top = [c.knob for c in cands]
            dec = decisive(cands, ents)
            rows.append({"case": case, "term": term, "truth": sorted(truth) if truth else None, "top5": top,
                         "at1": bool(truth) and bool(top) and top[0] in truth,
                         "at5": bool(truth) and any(t in truth for t in top),
                         "decisive": dec.knob if dec else None,
                         "decisive_ok": None if dec is None else bool(truth) and dec.knob in truth,
                         "repo": bool(repo)})
    pos = [r for r in rows if r["truth"]]
    neg = [r for r in rows if not r["truth"]]
    dec = [r for r in rows if r["decisive"]]
    return {"terms": len(rows), "linkable": len(pos),
            "recall@1": round(sum(r["at1"] for r in pos) / len(pos), 3) if pos else None,
            "recall@5": round(sum(r["at5"] for r in pos) / len(pos), 3) if pos else None,
            "decisive": len(dec), "decisive_right": sum(bool(r["decisive_ok"]) for r in dec),
            "decisive_for_unlinkable": sum(1 for r in neg if r["decisive"]), "rows": rows}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--scratch", type=Path, required=True)
    p.add_argument("--out", type=Path, default=ROOT / "eval" / "results" / "links_eval.json")
    a = p.parse_args()
    res = evaluate(a.scratch)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    for r in res["rows"]:
        mark = "ok" if r["at1"] else "@5" if r["at5"] else "--" if r["truth"] else "  "
        print(f"{mark} {r['case']:9s} {r['term'][:38]:38s} truth={r['truth']} top={r['top5'][:3]} decisive={r['decisive']}")
    print({k: v for k, v in res.items() if k != "rows"})


if __name__ == "__main__":
    sys.exit(main())
