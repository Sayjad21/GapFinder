"""Export the replay site's data as static files, for hosting without a server (GitHub Pages).

    python scripts/export_static.py web/public/data

Writes exactly what the API serves, by calling the server's own handlers:
    runs.json, scoreboard.json, runs/<id>.json, runs/<id>/events.json, runs/<id>/report.md
The web app built with VITE_STATIC=1 reads these and replays events in the browser with the
same timing rule as the server's SSE replay. Nothing here needs credentials or costs anything.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from gapfinder.api import server


def main(out: Path) -> None:
    if out.exists():
        shutil.rmtree(out)
    (out / "runs").mkdir(parents=True)
    runs = server.list_runs()
    _write(out / "runs.json", runs)
    _write(out / "scoreboard.json", server.scoreboard())
    for r in runs:
        rid = r["id"]
        _write(out / "runs" / f"{rid}.json", server.get_run(rid))
        (out / "runs" / rid).mkdir()
        _write(out / "runs" / rid / "events.json", server.get_events(rid))
        md = server._run_dir(rid) / "gap_report.md"
        if md.exists():
            shutil.copyfile(md, out / "runs" / rid / "report.md")
    _write(out / "config.json", {"max_idle_s": server.MAX_IDLE_S, "static": True})
    size = sum(p.stat().st_size for p in out.rglob("*") if p.is_file())
    print(f"exported {len(runs)} runs to {out} ({size / 1e6:.1f} MB)")


def _write(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, separators=(",", ":"), allow_nan=False), encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "web/public/data"))
