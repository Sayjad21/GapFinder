"""Dev regression suite: re-run only the search on every dev GapBench task from its recorded ledger, and score.

    python eval/dev_suite.py --base 100            # runs 101-103 on all 22 dev tasks
    python eval/dev_suite.py --base 100 --score-only
    python eval/dev_suite.py --base 100 --code <worktree at tag v1.1>   # the same suite on older code

Every task whose answers are public is dev data. That's the 4 dev tasks, the v1.0 set (test-gen-*) and
the v1.1 set (test-v11-*). Each search re-uses a recorded ledger (`harness.py --ledger-from`): no
model call, $0, local backend. So a change to the search can be checked on all 22 tasks before any new
sealed test, instead of on the one or two tasks that motivated it.

Ledger sources: dev tasks run 1 (one ledger, searched 3 times), test-gen runs 4-6 (the v1.0 freeze's
runs), test-v11 runs 1-3. The output run numbers are base+1 to base+3. Already finished runs are
skipped, so an interrupted suite resumes.

These results are post-hoc by construction: the tasks shaped the changes being checked. They decide
whether a change goes into the next frozen version; they are never reported as blind evidence.
"""

from __future__ import annotations

import argparse
import asyncio
import collections
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GB = ROOT / "eval" / "gapbench"
sys.path.insert(0, str(GB))


def plan() -> list[tuple[Path, Path, int]]:
    """(task dir, ledger run dir, k) for k = 1..3."""
    out = []
    for task in sorted((GB / "tasks").iterdir()):
        if not (task / "task.yaml").exists():
            continue
        name = task.name
        if name.startswith("dev-"):
            src = [1, 1, 1]
        elif name.startswith("test-gen-"):
            src = [4, 5, 6]
        elif name.startswith("test-v11-"):
            src = [1, 2, 3]
        else:
            continue
        for k, r in enumerate(src, 1):
            ledger = GB / "runs" / name / "gapfinder" / f"run{r}"
            if (ledger / "assumptions.json").exists():
                out.append((task, ledger, k))
    return out


def answers_dir(task: Path) -> Path | None:
    if task.name.startswith("test-gen-"):
        return GB / "sealed"
    if task.name.startswith("test-v11-"):
        return GB / "sealed-v11"
    return None  # dev tasks keep answer.json in the task folder


CODE = ROOT  # whose harness (and so whose gapfinder package) runs the searches; --code changes it


def runs_root() -> Path:
    return CODE / "eval" / "gapbench" / "runs"


def run_one(task: Path, ledger: Path, run: int) -> str:
    pred = runs_root() / task.name / "gapfinder" / f"run{run}" / "prediction.json"
    if pred.exists() and "error" not in json.loads(pred.read_text(encoding="utf-8")):
        return f"skip {task.name} run{run}"
    env = {**os.environ, "GF_CACHE_ONLY": "1", "GF_SANDBOX_GUARD_USD": "1000000", "PYTHONIOENCODING": "utf-8",
           "GF_CACHE_DIR": str(ROOT / ".gf_cache")}
    cmd = [sys.executable, str(CODE / "eval" / "gapbench" / "harness.py"), str(task), "--arm", "gapfinder", "--run", str(run),
           "--cap", "0.5", "--ledger-from", str(ledger)]
    p = subprocess.run(cmd, env=env, capture_output=True, text=True)
    return f"{'ok' if p.returncode == 0 else 'FAIL'} {task.name} run{run}"


async def score(base: int) -> list[dict]:
    import score as S

    rows = []
    for task, _, k in plan():
        run_dir = runs_root() / task.name / "gapfinder" / f"run{base + k}"
        if (run_dir / "prediction.json").exists():
            rows.append(await S.score_run(task, run_dir, 3, answers_dir(task)))
    return rows


def summary(rows: list[dict]) -> dict:
    by_cat = collections.defaultdict(collections.Counter)
    for r in rows:
        by_cat[r["category"]][r["outcome"]] += 1
    total = collections.Counter(r["outcome"] for r in rows)
    return {"runs": len(rows), "outcomes": dict(total), "by_category": {c: dict(v) for c, v in sorted(by_cat.items())},
            "per_task": {f"{r['task']} run{r['run']}": (r["outcome"], {c: (v["label"], v["knobs"])
                                                                        for c, v in r["claims"].items()})
                         for r in rows}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=int, required=True, help="output runs are base+1..base+3")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--score-only", action="store_true")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--code", type=Path, help="repo checkout whose code runs the searches (default: this one)")
    a = ap.parse_args()
    global CODE
    CODE = (a.code or ROOT).resolve()
    if not a.score_only:
        jobs = [(t, led, a.base + k) for t, led, k in plan()]
        with ThreadPoolExecutor(a.jobs) as ex:
            for msg in ex.map(lambda j: run_one(*j), jobs):
                print(msg, flush=True)
    os.environ.setdefault("GF_SANDBOX_GUARD_USD", "1000000")
    rows = asyncio.run(score(a.base))
    s = summary(rows)
    print(json.dumps({k: s[k] for k in ("runs", "outcomes", "by_category")}, indent=1))
    out = a.out or ROOT / "eval" / "results" / f"dev_suite_run{a.base}.json"
    out.write_text(json.dumps({"base": a.base, "code": str(CODE), **s, "rows": rows}, indent=1), encoding="utf-8")
    print("->", out)


if __name__ == "__main__":
    main()
