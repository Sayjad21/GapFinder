"""FastAPI server: recorded runs, Gap Reports, the GapBench scoreboard, and replay over SSE.

    uvicorn gapfinder.api.server:app --port 8000      (then open http://localhost:8000)

Replay mode is the default for judges: it plays a recorded event log at 1x, 4x or 16x and
costs nothing. A run is any directory holding events.jsonl and gap_report.json, under
GF_DEMO_DIR (default: demo/runs, committed) or eval/gapbench/runs.
Live mode is off unless GF_LIVE_CODE is set (and even then capped by the spend ledger).
"""

from __future__ import annotations

import asyncio
import json
import math
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse

from gapfinder.config import REPO_ROOT
from gapfinder.report.gap_report import upgrade_report

WEB_DIST = REPO_ROOT / "web" / "dist"
MAX_IDLE_S = 2.0  # replay compresses idle gaps longer than this (in replay time)

app = FastAPI(title="GapFinder", docs_url="/api/docs")


def run_roots() -> list[Path]:
    demo = Path(os.environ.get("GF_DEMO_DIR", REPO_ROOT / "demo" / "runs"))
    return [demo, REPO_ROOT / "eval" / "gapbench" / "runs"]


def discover() -> dict[str, Path]:
    """run id -> directory. Ids are the path below the root, with '/' replaced by '~'."""
    runs = {}
    for root in run_roots():
        if not root.exists():
            continue
        for ev in sorted(root.rglob("events.jsonl")):
            d = ev.parent
            if (d / "gap_report.json").exists():
                runs[str(d.relative_to(root)).replace("\\", "/").replace("/", "~")] = d
    return runs


def _run_dir(run_id: str) -> Path:
    d = discover().get(run_id)
    if d is None:
        raise HTTPException(404, f"no recorded run {run_id!r}")
    return d


def _finite(x):
    """Browsers reject Infinity/NaN in JSON; Python's json writes them. Send null instead."""
    if isinstance(x, float) and not math.isfinite(x):
        return None
    if isinstance(x, dict):
        return {k: _finite(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_finite(v) for v in x]
    return x


def _read_events(d: Path) -> list[dict]:
    lines = (d / "events.jsonl").read_text(encoding="utf-8").splitlines()
    return [_finite(json.loads(line)) for line in lines if line.strip()]


def _json(path: Path):
    return _finite(json.loads(path.read_text(encoding="utf-8"))) if path.exists() else None


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "runs": len(discover()), "live_mode": bool(os.environ.get("GF_LIVE_CODE"))}


@app.get("/api/runs")
def list_runs() -> list[dict]:
    out = []
    for run_id, d in discover().items():
        rep = _json(d / "gap_report.json") or {}
        meta = _json(d / "meta.json") or {}
        out.append({
            "id": run_id,
            "title": meta.get("title") or rep.get("paper") or run_id,
            "kind": meta.get("kind", "gapbench" if "eval" in str(d) else "demo"),
            "artifact": rep.get("artifact"),
            "generated": rep.get("generated"),
            "runs": rep.get("runs"),
            "partial": rep.get("partial", False),
            "labels": {c["target"]["claim_id"]: (c["attribution"] or {}).get("confidence_label", "Reproduced")
                       for c in rep.get("claims", [])},
            "featured": meta.get("featured", False),
        })
    return sorted(out, key=lambda r: (not r["featured"], r["kind"] != "demo", r["id"]))


@app.get("/api/runs/{run_id}")
def get_run(run_id: str) -> dict:
    d = _run_dir(run_id)
    events = _read_events(d)
    ts = [e["t"] for e in events if "t" in e]
    return {
        "id": run_id,
        "meta": _json(d / "meta.json") or {},
        "report": _finite(upgrade_report(_json(d / "gap_report.json"))),  # old reports get the card fields
        "claims": _json(d / "claims.json"),
        "assumptions": _json(d / "assumptions.json"),
        "prediction": _json(d / "prediction.json"),
        "events": len(events),
        "recorded_at": min(ts) if ts else None,
        "duration_s": round(max(ts) - min(ts), 1) if ts else 0,
    }


@app.get("/api/runs/{run_id}/report.md")
def get_report_md(run_id: str):
    path = _run_dir(run_id) / "gap_report.md"
    if not path.exists():
        raise HTTPException(404, "no Markdown report for this run")
    return FileResponse(path, media_type="text/markdown", filename=f"gap_report_{run_id}.md")


@app.get("/api/runs/{run_id}/issue_draft.md")
def get_issue_draft(run_id: str):
    path = _run_dir(run_id) / "issue_draft.md"
    if not path.exists():
        raise HTTPException(404, "no issue draft for this run")
    return FileResponse(path, media_type="text/markdown", filename=f"issue_draft_{run_id}.md")


@app.get("/api/runs/{run_id}/events")
def get_events(run_id: str) -> list[dict]:
    return _read_events(_run_dir(run_id))


@app.get("/api/runs/{run_id}/replay")
async def replay(run_id: str, speed: float = Query(4.0, ge=0.25, le=256)):
    """Stream the recorded events with their original spacing divided by `speed`."""
    events = _read_events(_run_dir(run_id))

    async def gen():
        prev = None
        for ev in events:
            t = ev.get("t")
            if prev is not None and t is not None:
                await asyncio.sleep(min((t - prev) / speed, MAX_IDLE_S))
            prev = t if t is not None else prev
            yield {"event": "gf", "data": json.dumps(ev)}
        yield {"event": "done", "data": "{}"}

    return EventSourceResponse(gen())


@app.get("/api/scoreboard")
def scoreboard() -> dict:
    """Latest GapBench results per split (highest version number wins)."""
    res_dir = REPO_ROOT / "eval" / "results"
    out = {}
    for split in ("dev", "test"):
        files = sorted(res_dir.glob(f"gapbench_{split}*.json"),
                       key=lambda p: int("".join(c for c in p.stem.split("_v")[-1] if c.isdigit()) or 0)
                       if "_v" in p.stem else 0)
        if files:
            out[split] = {"file": files[-1].name, **_json(files[-1])}
    return out


@app.post("/api/live")
def live() -> JSONResponse:
    """Live mode needs Sandboxes access and an access code; until then it refuses politely and spends nothing."""
    return JSONResponse({"ok": False, "reason": "Live mode is not enabled on this deployment. "
                         "Replay mode shows recorded runs at no cost."}, status_code=503)


if WEB_DIST.exists():
    app.mount("/assets", StaticFiles(directory=WEB_DIST / "assets"), name="assets")

    @app.get("/{path:path}")
    def spa(path: str):
        target = WEB_DIST / path
        return FileResponse(target if path and target.is_file() else WEB_DIST / "index.html")
