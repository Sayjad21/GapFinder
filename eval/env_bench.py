"""How often does the environment builder (gapfinder/env_build.py) make a dev-set repo runnable on its own?

    python eval/env_bench.py --case vgae=<local checkout> --case pygcn=<local checkout> ... --out eval/results/env_bench.json

For each case: build the environment from the repo alone (its README and build files; NOT the case's
hand-picked pins in case.json), then run the case's own data step (`setup`, hand-written, not measured here)
and its smoke command with its harness, exactly as the hand-built image ran them. A case counts as built when
the smoke run exits 0 and prints every metric the case's spec declares.

This measures one part of the harness, the environment. The data step, the run command and the metric
parser are still the hand-written ones; they are later parts of item 4 (docs/CONTEXT_v11.md section 7.2).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEVSET = ROOT / "eval" / "external" / "devset"


async def one(case: str, local: Path, max_steps: int) -> dict:
    import yaml

    from gapfinder.env_build import build_env, fetch
    from gapfinder.models.router import Router
    from gapfinder.sandbox.backend import ContreeBackend

    c = json.loads((DEVSET / case / "case.json").read_text(encoding="utf-8"))
    metrics = yaml.safe_load((DEVSET / case / f"{case}.yaml").read_text(encoding="utf-8")).get("metrics") or []
    b = ContreeBackend()
    res = await build_env(Router(), b, local, fetch=fetch(c["repo"], c["commit"], local), max_steps=max_steps)
    row = {"case": case, "env_ok": res.ok, "image": res.image, "hand_image": c["image"], "steps": len(res.steps),
           "kept": len(res.recipe), "recipe": res.recipe, "reason": res.reason, "llm_usd": round(res.cost_usd, 4),
           "smoke_ok": False}
    if not res.ok:
        return row
    harness = DEVSET / case / "harness"
    files = {f"gf_harness/{p.relative_to(harness).as_posix()}": p.read_bytes()
             for p in harness.rglob("*") if p.is_file()} if harness.is_dir() else {}
    ckpt = res.checkpoint
    if c.get("setup"):
        r = await b.run(ckpt, "cd /work && " + c["setup"], timeout=3000, disposable=False, files=files or None)
        row["setup_exit"] = r.exit_code
        if r.exit_code != 0 or not r.checkpoint:
            row["smoke_tail"] = (r.stdout + r.stderr)[-1200:]
            return row
        ckpt, files = r.checkpoint, {}
    r = await b.run(ckpt, "cd /work && " + c["smoke"], env={"RUN_TAG": "env-bench"}, timeout=3600, disposable=True,
                    files=files or None)
    found = {m for m in metrics if re.search(rf"(?m)^\s*{re.escape(m)}\s*[:=]\s*[-+0-9.eE]+", r.stdout or "")}
    row.update({"smoke_exit": r.exit_code, "metrics_found": sorted(found), "metrics_declared": metrics,
                "smoke_ok": r.exit_code == 0 and set(metrics) <= found,
                "smoke_tail": "" if r.exit_code == 0 else ((r.stdout or "") + (r.stderr or ""))[-1200:]})
    return row


async def main(cases: dict[str, Path], out: Path, max_steps: int) -> None:
    rows = await asyncio.gather(*(one(c, p, max_steps) for c, p in cases.items()), return_exceptions=True)
    rows = [r if isinstance(r, dict) else {"case": c, "error": f"{type(r).__name__}: {r}"} for c, r in zip(cases, rows)]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    for r in rows:
        print(f"{r['case']:10s} env {'ok' if r.get('env_ok') else 'FAIL':4s} smoke {'ok' if r.get('smoke_ok') else 'FAIL':4s} "
              f"{r.get('image', '')} ({r.get('kept', 0)}/{r.get('steps', 0)} cmds) {r.get('reason') or r.get('error') or ''}"[:220])
    print(f"\n{sum(bool(r.get('smoke_ok')) for r in rows)}/{len(rows)} runnable from the repo alone -> {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", action="append", required=True, metavar="NAME=LOCAL_CHECKOUT")
    ap.add_argument("--out", type=Path, default=ROOT / "eval" / "results" / "env_bench.json")
    ap.add_argument("--max-steps", type=int, default=12)
    a = ap.parse_args()
    asyncio.run(main({x.split("=", 1)[0]: Path(x.split("=", 1)[1]) for x in a.case}, a.out, a.max_steps))
