"""Claims against the paper's own tables (plans D3.1, D3.5): $0, no model call.

    python eval/claims_recall.py regound [--scratch DIR]       # every cached ledger, old grounding against new
    python eval/claims_recall.py recall --claims FILE --arxiv ID [--method NAME ...]

`regound`: each ledger's raw (pre-grounding) claims, grounded by the quote alone (before plan D3.1) and by the new
grounder (numbers in any spelling, fuzzy quotes that keep every number, table cells). Every claim the new grounder
recovers is checked against the LaTeX tables when the paper's source is on arXiv: its number must be a cell of the
table it names. Every claim it newly drops is listed with the reason. The acceptance (D3.1): recovered claims are
true (in their table), and no claim the old grounder kept is dropped unless its number is nowhere in the paper.

`recall`: the method's rows of every LaTeX table are the ground truth (gapfinder/ingest/tables.py); a cell is recalled
when a claim holds its number (any spelling) and names its table. Any extractor's claims can be scored.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _arxiv_of(case_dir: Path) -> str | None:
    for name in ("case.json", "case.md"):
        p = case_dir / name
        if p.exists():
            m = re.search(r"(\d{4}\.\d{4,5})", p.read_text(encoding="utf-8", errors="replace"))
            if m:
                return m.group(1)
    return None


def _grids(arxiv_id: str | None):
    if not arxiv_id:
        return []
    from gapfinder.config import settings
    from gapfinder.ingest import arxiv_source
    from gapfinder.ingest.tables import latex_grids

    src = arxiv_source.fetch_source(arxiv_id, settings().cache_dir / "arxiv")
    return latex_grids(arxiv_source.document(src)) if src else []


def regound(scratch: Path) -> list[dict]:
    from gapfinder.ingest.pdf import load_paper
    from gapfinder.ledger.grounding import Grounder, _print_close, _table_no
    from gapfinder.ledger.schemas import Claim

    rows = []
    for raw in sorted((ROOT / "eval" / "external").glob("**/ledger/raw/claims.json")):
        led = raw.parent.parent
        meta = json.loads((led / "claim_ledger.json").read_text(encoding="utf-8")) if (led / "claim_ledger.json").exists() else {}
        pdf = Path(str(meta.get("paper", "")).replace("<scratch>", str(scratch)))
        if not pdf.exists():
            rows.append({"ledger": str(led.relative_to(ROOT)), "skipped": f"paper not found: {pdf}"})
            continue
        claims = [Claim(**c) for c in json.loads(raw.read_text(encoding="utf-8"))]
        paper = load_paper(pdf)
        pages = {p.number: p.text for p in paper.pages}
        case = led.parent if led.parent.name != "posthoc-fixed" else led.parent.parent
        grids = _grids(_arxiv_of(case) or _arxiv_of(case.parent))
        old = Grounder(paper.full_text, pages=pages)
        old_kept = {c.id for c in claims if old.quote_in_paper(c.quote)}
        rep = Grounder(paper.full_text, pages=pages, grids=grids).check_claims(claims)
        new_kept = {c.id for c in rep.kept}
        by_id = {c.id: c for c in claims}
        checked = []
        for cid, how in rep.recovered:
            c = by_id[cid]
            if not grids or c.reported_value is None:
                checked.append({"id": cid, "how": how, "in_table": None})
                continue
            want = _table_no(c.figure_or_table)
            ok = any(_print_close(c.reported_value, x.value) for g in grids
                     if want is None or _table_no(g.label) == want for _, _, x in g.body())
            checked.append({"id": cid, "how": how, "in_table": ok})
        rows.append({"ledger": str(led.relative_to(ROOT)), "claims": len(claims), "old_kept": len(old_kept),
                     "new_kept": len(new_kept), "recovered": checked,
                     "newly_dropped": [(cid, why) for cid, why in rep.dropped if cid in old_kept],
                     "latex_tables": len(grids)})
    return rows


def recall(claims: list[dict], grids, method_names: list[str]) -> dict:
    from gapfinder.ingest.tables import cell_claims, label
    from gapfinder.ledger.grounding import _print_close, _table_no

    truth = [x for g in grids for x in cell_claims(g, label(g, method_names))]
    hit = [t for t in truth if any(c.get("reported_value") is not None and _print_close(t["reported_value"], c["reported_value"])
                                   and (_table_no(c.get("figure_or_table")) in (None, _table_no(t["figure_or_table"])))
                                   for c in claims)]
    per = {}
    for t in truth:
        k = t["figure_or_table"]
        per.setdefault(k, [0, 0])
        per[k][1] += 1
        per[k][0] += t in hit
    return {"cells": len(truth), "recalled": len(hit), "recall": round(len(hit) / len(truth), 3) if truth else None,
            "per_table": {k: f"{a}/{b}" for k, (a, b) in per.items()},
            "missed": [{"table": t["figure_or_table"], "value": t["reported_value"], "conditions": t["conditions"]}
                       for t in truth if t not in hit][:40]}


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("regound")
    pr.add_argument("--scratch", type=Path, required=True, help="the folder the ledgers' <scratch> paths point to")
    pr.add_argument("--out", type=Path, default=ROOT / "eval" / "results" / "regound.json")
    pc = sub.add_parser("recall")
    pc.add_argument("--claims", type=Path, required=True, help="a claim_ledger.json or a list of claims")
    pc.add_argument("--arxiv", default=None, help="default: the id in the case folder above the claims file")
    pc.add_argument("--method", nargs="*", default=[])
    a = p.parse_args()
    if a.cmd == "regound":
        rows = regound(a.scratch)
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(rows, indent=1), encoding="utf-8")
        for r in rows:
            if "skipped" in r:
                print(f"{r['ledger']:48s} skipped ({r['skipped'][:60]})")
                continue
            rec = r["recovered"]
            true = sum(x["in_table"] is True for x in rec)
            false = sum(x["in_table"] is False for x in rec)
            print(f"{r['ledger']:48s} {r['claims']:3d} claims: kept {r['old_kept']:3d} -> {r['new_kept']:3d}; "
                  f"recovered {len(rec)} (in their table {true}, not {false}, unchecked {len(rec) - true - false}); "
                  f"newly dropped {len(r['newly_dropped'])}; {r['latex_tables']} LaTeX tables")
    else:
        d = json.loads(a.claims.read_text(encoding="utf-8"))
        claims = d["claims"] if isinstance(d, dict) else d
        aid = a.arxiv or next((x for p in a.claims.resolve().parents[:4] if (x := _arxiv_of(p))), None)
        if not aid:
            sys.exit("no arXiv id: pass --arxiv")
        print(json.dumps({"arxiv": aid, **recall(claims, _grids(aid), a.method)}, indent=1))


if __name__ == "__main__":
    sys.exit(main())
