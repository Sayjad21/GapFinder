"""Export the replay site's data as static files, for hosting without a server (GitHub Pages).

    python scripts/export_static.py web/public/data [--showcase]   # --showcase: only demo/runs, not every dev run

Writes exactly what the API serves, by calling the server's own handlers:
    runs.json, scoreboard.json, showcase.json (when built), runs/<id>.json, runs/<id>/events.json, runs/<id>/report.md
The web app built with VITE_STATIC=1 reads these and replays events in the browser with the
same timing rule as the server's SSE replay. Nothing here needs credentials or costs anything.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from gapfinder.api import server


def main(out: Path, showcase: bool = False) -> None:
    """`showcase`: only the runs under the demo root (demo/runs: the showcase and the featured demos), not every
    development run under eval/gapbench/runs."""
    if out.exists():
        shutil.rmtree(out)
    (out / "runs").mkdir(parents=True)
    runs = server.list_runs()
    if showcase:
        demo = server.run_roots()[0].resolve()
        keep = {rid for rid, d in server.discover().items() if demo in d.resolve().parents}
        runs = [r for r in runs if r["id"] in keep]
    _write(out / "runs.json", runs)
    _write(out / "scoreboard.json", server.scoreboard())
    if (server.run_roots()[0] / "showcase.json").exists():
        _write(out / "showcase.json", server.showcase())
    for r in runs:
        rid = r["id"]
        _write(out / "runs" / f"{rid}.json", server.get_run(rid))
        (out / "runs" / rid).mkdir()
        _write(out / "runs" / rid / "events.json", server.get_events(rid))
        md = server._run_dir(rid) / "gap_report.md"
        if md.exists():
            shutil.copyfile(md, out / "runs" / rid / "report.md")
        issue = server._run_dir(rid) / "issue_draft.md"
        if issue.exists():
            shutil.copyfile(issue, out / "runs" / rid / "issue_draft.md")
    _write(out / "config.json", {"max_idle_s": server.MAX_IDLE_S, "static": True})
    size = sum(p.stat().st_size for p in out.rglob("*") if p.is_file())
    print(f"exported {len(runs)} runs to {out} ({size / 1e6:.1f} MB)")


def _write(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, separators=(",", ":"), allow_nan=False), encoding="utf-8")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(Path(args[0] if args else "web/public/data"), showcase="--showcase" in sys.argv)
