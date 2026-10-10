"""Run a full GapFinder investigation on a GapBench dev task: free, offline, no keys.

    python scripts/try_it.py                          # dev-ml-threshold, about 20 s
    python scripts/try_it.py --task dev-rl-schedule
    python scripts/try_it.py --list

The model answers (claim ledger and assumption space) come from demo/cache/, which holds the
recorded responses for the four dev tasks. The experiments themselves run for real on this
machine, in the local sandbox backend. The model cache is read-only here (GF_CACHE_ONLY=1): a
cache miss stops the run instead of calling an API, so nothing can be spent and no network call
is made. No .env or API key is needed.

The Gap Report is written to runs/try_it/<task>/gap_report.md (git-ignored).
"""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO_CACHE = ROOT / "demo" / "cache"
TASKS = ROOT / "eval" / "gapbench" / "tasks"
DEFAULT_TASK = "dev-ml-threshold"
# Credentials a stray .env or shell could supply. Setting them to "" keeps the .env loader from
# filling them in, so this script has nothing to authenticate with even by accident.
_CREDENTIALS = ("TOKEN_FACTORY_API_KEY", "NVIDIA_API_KEY", "TAVILY_API_KEY", "NEBIUS_PROJECT_ID",
                "NEBIUS_AI_PROJECT", "NEBIUS_IAM_TOKEN", "GF_RUSKEY_SOURCE")


def dev_tasks() -> list[str]:
    return sorted(p.name for p in TASKS.glob("dev-*") if (p / "task.yaml").exists())


def _load_harness():
    spec = importlib.util.spec_from_file_location("gapbench_harness", ROOT / "eval" / "gapbench" / "harness.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--task", default=DEFAULT_TASK, help=f"a GapBench dev task (default {DEFAULT_TASK})")
    p.add_argument("--list", action="store_true", help="list the available tasks and exit")
    p.add_argument("--out", type=Path, help="where to write the Gap Report (default runs/try_it/<task>)")
    a = p.parse_args(argv)

    if a.list:
        print("\n".join(dev_tasks()))
        return 0
    if a.task not in dev_tasks():
        print(f"unknown task {a.task!r}; choose one of: {', '.join(dev_tasks())}", file=sys.stderr)
        return 2
    if not (DEMO_CACHE / "llm").is_dir():
        print(f"{DEMO_CACHE / 'llm'} is missing, so there are no recorded model answers to replay.", file=sys.stderr)
        return 2
    for stream in (sys.stdout, sys.stderr):  # reports contain non-ASCII; a Windows console may not
        stream.reconfigure(encoding="utf-8", errors="replace")

    work = Path(tempfile.mkdtemp(prefix="gapfinder_try_"))
    try:
        shutil.copytree(DEMO_CACHE, work / "cache")  # a copy: the router writes a spend ledger beside it
        os.environ.update({"GF_CACHE_DIR": str(work / "cache"), "GF_CACHE_ONLY": "1",
                           "GF_LOCAL_SANDBOX_DIR": str(work / "sandbox"), "GF_SANDBOX_BACKEND": "local",
                           "GF_SPEND_CAP_USD": "0"})
        for name in _CREDENTIALS:
            os.environ[name] = ""
        sys.path.insert(0, str(ROOT))
        harness = _load_harness()

        out = a.out or ROOT / "runs" / "try_it" / a.task
        out.mkdir(parents=True, exist_ok=True)
        print(f"{a.task}: replaying recorded model answers, running the experiments locally ...")
        t0 = time.monotonic()
        try:
            res = asyncio.run(harness.run_gapfinder(TASKS / a.task, out, harness.ARM_CONFIG["gapfinder"], backend="local", use_cache=True))
        except Exception as exc:
            if type(exc).__name__ == "CacheMiss":
                print(f"cache miss: {exc}\nNothing was spent. This task needs model answers that are not in "
                      f"demo/cache.", file=sys.stderr)
                return 1
            raise
        elapsed = time.monotonic() - t0
    finally:
        shutil.rmtree(work, ignore_errors=True)

    report = out / "gap_report.md"
    print(report.read_text(encoding="utf-8"))
    print(f"Done in {elapsed:.0f} s: {res['runs']} experiment runs, "
          f"{res['llm_usd_paid']:.2f} USD spent on models ({res['llm_usd']:.2f} USD if they had been called fresh).")
    print(f"Gap Report: {report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
