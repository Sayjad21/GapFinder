"""Plan item 16: does Super extract the claims Ultra extracts? (Ultra stays for assumptions either way.)

    python eval/claims_tier.py --case b4a=<dir with paper.pdf>:eval/external/batch4/b4a/ledger ... --out eval/results/claims_tier.json

For each paper with an Ultra ledger, Super extracts claims from the same text (the PDF; those ledgers were made
without the arXiv supplement), and each numeric Ultra claim counts as found when a Super claim has the same
number in the same table or figure (or the same number and metric family when either side names no table).
Recall is over Ultra's numeric claims; Super's extra claims are counted, not judged.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
from pathlib import Path


def _table(x: str | None) -> str:
    return re.sub(r"\s+", " ", (x or "").lower()).strip()


def _same(u: dict, s: dict) -> bool:
    from gapfinder.harness_auto import _family

    a, b = u.get("reported_value"), s.get("reported_value")
    if a is None or b is None or abs(a - b) > 1e-9 * max(1.0, abs(a)):
        return False
    tu, ts = _table(u.get("figure_or_table")), _table(s.get("figure_or_table"))
    if tu and ts:
        return tu == ts
    return _family(u.get("metric", "")) == _family(s.get("metric", "")) or not (_family(u.get("metric", ""))
                                                                              and _family(s.get("metric", "")))


async def one(name: str, pdf: Path, ledger: Path) -> dict:
    from gapfinder.ingest.pdf import load_paper
    from gapfinder.ledger.claims import extract_claims
    from gapfinder.models.router import Router

    ultra = json.loads((ledger / "raw" / "claims.json").read_text(encoding="utf-8"))
    paper = load_paper(pdf)
    router = Router()
    before = router.meter.total_cost()
    sup = [c.model_dump() for c in await extract_claims(router, paper, tier="super")]
    un = [u for u in ultra if u.get("reported_value") is not None]
    found = [u for u in un if any(_same(u, s) for s in sup)]
    missed = [{"id": u["id"], "table": u.get("figure_or_table"), "metric": u.get("metric"), "value": u["reported_value"]}
              for u in un if u not in found]
    extra = [s for s in sup if s.get("reported_value") is not None and not any(_same(u, s) for u in un)]
    return {"case": name, "ultra_numeric": len(un), "super_numeric": sum(s.get("reported_value") is not None for s in sup),
            "found": len(found), "recall": round(len(found) / max(1, len(un)), 3), "super_extra": len(extra),
            "missed": missed[:40], "super_usd": round(router.meter.total_cost() - before, 4)}


async def main(cases: dict[str, tuple[Path, Path]], out: Path) -> None:
    rows = []
    for n, (p, l) in cases.items():
        try:
            rows.append(await one(n, p, l))
        except Exception as e:  # noqa: BLE001 (Super out of output tokens, a connection error): a result too
            rows.append({"case": n, "error": f"{type(e).__name__}: {str(e)[:200]}", "ultra_numeric": 0, "found": 0})
    for r in rows:
        if "error" in r:
            print(f"{r['case']:6s} FAILED: {r['error']}")
    rows_ok = [r for r in rows if "error" not in r]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    for r in rows_ok:
        print(f"{r['case']:6s} Ultra {r['ultra_numeric']:3d} numeric claims, Super found {r['found']:3d} "
              f"(recall {r['recall']:.0%}), Super extra {r['super_extra']:3d}, ${r['super_usd']:.4f}")
    tot_u, tot_f = sum(r["ultra_numeric"] for r in rows_ok), sum(r["found"] for r in rows_ok)
    print(f"\npooled recall {tot_f}/{tot_u} = {tot_f / max(1, tot_u):.0%} -> {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", action="append", required=True, metavar="NAME=PDF:LEDGER_DIR")
    ap.add_argument("--out", type=Path, default=Path("eval/results/claims_tier.json"))
    a = ap.parse_args()
    cases = {}
    for x in a.case:
        n, rest = x.split("=", 1)
        pdf, led = rest.rsplit(":", 1) if rest.count(":") > 1 else rest.split(":", 1)
        cases[n] = (Path(pdf), Path(led))
    asyncio.run(main(cases, a.out))
