"""Measure each mined candidate's gap: does the fix change any printed number beyond noise? (plan item 1, step 2)

    python eval/pool/verify.py --ids pf12d42c9 pf2f5437a ... [--repeats 3] [--max-steps 8]

A candidate becomes a case only when the numbers its README command prints differ between the parent commit
and the fix commit by more than noise (most "match the paper" commits change nothing measurable). Blind by
construction, like the miner:
- this script alone reads the sealed answer (eval/pool/sealed/<id>/: the fix commit and the files it touched);
- the fixed files go into the VM from GitHub's tarball of the fix commit, and are never printed;
- the output is a verdict per candidate (kept / no measurable gap / why it couldn't be run) and how many printed
  numbers were compared, nothing about what the fix changed. Verdicts go to eval/pool/verified.json.

The environment is built for the parent (env-build: Super, about $0.02-0.05 a repo); runs are Sandboxes.
"""

from __future__ import annotations

import argparse
import asyncio
import io
import json
import statistics
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
SEALED = ROOT / "eval" / "pool" / "sealed"
PUBLIC = ROOT / "eval" / "pool" / "candidates.json"
OUT = ROOT / "eval" / "pool" / "verified.json"  # --out to write elsewhere


_TEXT = (".py", ".sh", ".md", ".rst", ".txt", ".yaml", ".yml", ".json", ".cfg", ".ini", ".toml", ".cu", ".cuh", ".gitmodules")
BIG_MB = 500


def _tree(repo: str, sha: str, dest: Path) -> tuple[Path | None, list[str]]:
    """The repo at `sha`, code and text files only (the VM fetches the full tree itself), and the files larger
    than BIG_MB (a static blocker). Members that can't be written here (Windows path limits) are skipped."""
    owner_repo = repo.removeprefix("https://github.com/")
    try:
        data = urllib.request.urlopen(f"https://codeload.github.com/{owner_repo}/tar.gz/{sha}", timeout=300).read()
    except Exception:  # noqa: BLE001
        return None, []
    big = []
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as t:
        for m in t.getmembers():
            if m.isfile() and m.size > BIG_MB * 2**20:
                big.append(f"{m.name.split('/', 1)[-1]} is {m.size / 2**20:.0f} MB")
                continue
            if m.isfile() and (not m.name.endswith(_TEXT) or m.size > 5 * 2**20):
                continue
            try:
                t.extract(m, dest, filter="data")
            except (OSError, tarfile.TarError):
                continue
    subs = [p for p in dest.iterdir() if p.is_dir()]
    return (subs[0] if len(subs) == 1 else None), big


def differs(a: list[dict[str, float]], b: list[dict[str, float]], z: float = 3.0, rel: float = 0.01) -> tuple[int, int]:
    """(labels compared, labels whose means differ beyond z pooled standard errors and by more than rel)."""
    labels = set.intersection(*(set(x) for x in a + b)) if a and b else set()
    moved = 0
    for k in labels:
        xa, xb = [x[k] for x in a], [x[k] for x in b]
        ma, mb = statistics.fmean(xa), statistics.fmean(xb)
        se = ((statistics.pvariance(xa) / len(xa) + statistics.pvariance(xb) / len(xb)) ** 0.5) or 1e-12
        if abs(ma - mb) > z * se and abs(ma - mb) > rel * max(abs(ma), abs(mb), 1e-12):
            moved += 1
    return len(labels), moved


async def one(cid: str, repeats: int, max_steps: int, timeout: float, dry: bool = False) -> dict:
    from gapfinder.env_build import build_env, fetch, readme_command, short_run_goal
    from gapfinder.harness_auto import compute_blockers, labelled_numbers, pick_commands
    from gapfinder.models.router import Router
    from gapfinder.sandbox import runtime_shim
    from gapfinder.sandbox.backend import ContreeBackend

    pub = next(c for c in json.loads(PUBLIC.read_text(encoding="utf-8")) if c["id"] == cid)
    meta = json.loads((SEALED / cid / "meta.json").read_text(encoding="utf-8"))  # read here, never printed
    tmp = Path(tempfile.mkdtemp(prefix="gfp"))  # short: Windows path limits
    parent, big = _tree(pub["repo"], pub["commit"], tmp / "a")
    fixed, _ = _tree(pub["repo"], meta["fix_commit"], tmp / "b")
    if parent is None or fixed is None:
        return {"id": cid, "verdict": "unrunnable", "why": "could not fetch the trees"}
    blockers = compute_blockers(parent) + big
    if blockers:
        return {"id": cid, "verdict": "unrunnable", "why": "static blockers: " + "; ".join(blockers[:3])}
    cmd = readme_command(parent) or next((c.cmd for c in pick_commands(parent, [])), None)
    if not cmd:
        return {"id": cid, "verdict": "unrunnable", "why": "no experiment command in the README or scripts"}
    if dry:  # the free checks only: trees, static blockers, a command
        return {"id": cid, "verdict": "ready", "why": "", "command_script": next((w for w in cmd.split() if w.endswith((".py", ".sh"))), "")}
    router, backend = Router(), ContreeBackend()
    before = router.meter.total_cost()
    env = await build_env(router, backend, parent, fetch=fetch(pub["repo"], pub["commit"], parent), max_steps=max_steps,
                          goal=short_run_goal(cmd))
    row = {"id": cid, "env_ok": env.ok, "llm_usd": round(router.meter.total_cost() - before, 4)}
    if not env.ok:
        return {**row, "verdict": "unrunnable", "why": "environment: " + env.reason[:200]}
    senv, sfiles, sprefix = runtime_shim.run_parts()
    fix_files = {rel: (fixed / rel).read_bytes() for rel in meta["files"] if (fixed / rel).is_file()}
    run = f"cd /work && {sprefix}timeout {int(timeout)} bash -c {json.dumps(cmd)} 2>&1 | tail -n 60"

    async def go(files):
        outs = await asyncio.gather(*(backend.run(env.checkpoint, run, env={**senv, "RUN_TAG": f"pool-{i}"},
                                                  timeout=timeout + 120, disposable=True, files={**sfiles, **files})
                                      for i in range(repeats)))
        return [labelled_numbers(o.stdout or "") for o in outs if (o.stdout or "").strip()]

    a = await go({})
    b = await go(fix_files)
    n, moved = differs([x for x in a if x], [x for x in b if x])
    verdict = "kept" if moved else ("no measurable gap" if n else "unrunnable")
    return {**row, "verdict": verdict, "labels_compared": n, "labels_moved": moved,
            "why": "" if n else "no printed numbers in common"}


async def main(ids: list[str], repeats: int, max_steps: int, timeout: float, dry: bool = False) -> None:
    done = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    for cid in ids:
        try:
            r = await one(cid, repeats, max_steps, timeout, dry)
        except Exception as e:  # noqa: BLE001
            r = {"id": cid, "verdict": "unrunnable", "why": f"{type(e).__name__}: {str(e)[:200]}"}
        if dry:
            print(f"{cid}: {r['verdict']} {r.get('why', '')[:120]}", flush=True)
            done.setdefault("_dry", {})[cid] = r
            OUT.write_text(json.dumps(done, indent=1), encoding="utf-8")
            continue
        done[cid] = r
        OUT.write_text(json.dumps(done, indent=1), encoding="utf-8")
        print(f"{cid}: {r['verdict']}" + (f" ({r.get('labels_moved')}/{r.get('labels_compared')} numbers moved)"
                                          if r["verdict"] != "unrunnable" else f" ({r.get('why', '')[:120]})"), flush=True)
    kept = sum(v.get("verdict") == "kept" for k, v in done.items() if k != "_dry")
    print(f"\n{kept} kept of {len(done)} verified -> {OUT}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", nargs="+", required=True, help="candidate ids, or `all`")
    ap.add_argument("--dry", action="store_true", help="free checks only: trees, static blockers, a command")
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--max-steps", type=int, default=8)
    ap.add_argument("--timeout", type=float, default=1500, help="seconds per run of the README command")
    a = ap.parse_args()
    ids = [c["id"] for c in json.loads(PUBLIC.read_text(encoding="utf-8"))] if a.ids == ["all"] else a.ids
    OUT = a.out
    asyncio.run(main(ids, a.repeats, a.max_steps, a.timeout, a.dry))
