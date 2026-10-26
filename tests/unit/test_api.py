import json

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    run = tmp_path / "demo" / "toy-alpha"
    run.mkdir(parents=True)
    events = [{"seq": 1, "t": 100.0, "type": "noise_band", "metric": "score", "median": 34.0, "band": 0.3},
              {"seq": 2, "t": 101.0, "type": "survivor", "claim": "C1", "knob": "alpha", "value": "2.0", "units": 9},
              {"seq": 3, "t": 160.0, "type": "attribution", "claim": "C1", "label": "Explained"}]
    (run / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events))
    report = {"paper": "toy", "artifact": "toy", "generated": "2026-10-06", "runs": 26, "partial": False,
              "claims": [{"target": {"claim_id": "C1"}, "attribution": {"confidence_label": "Explained"}}]}
    (run / "gap_report.json").write_text(json.dumps(report))
    (run / "meta.json").write_text(json.dumps({"title": "Toy: planted alpha", "featured": True}))
    monkeypatch.setenv("GF_DEMO_DIR", str(tmp_path / "demo"))
    from gapfinder.api.server import app

    return TestClient(app)


def test_runs_listing_and_detail(client):
    runs = client.get("/api/runs").json()
    toy = next(r for r in runs if r["id"] == "toy-alpha")
    assert toy["title"] == "Toy: planted alpha" and toy["labels"] == {"C1": "Explained"} and toy["featured"]
    d = client.get("/api/runs/toy-alpha").json()
    assert d["events"] == 3 and d["duration_s"] == 60.0 and d["report"]["runs"] == 26
    assert client.get("/api/runs/nope").status_code == 404


def test_runs_filter_by_group_and_showcase_manifest(client, tmp_path):
    assert client.get("/api/showcase").status_code == 404
    run = tmp_path / "demo" / "real" / "toy-beta"
    run.mkdir(parents=True)
    (run / "events.jsonl").write_text(json.dumps({"seq": 1, "t": 1.0, "type": "noise_band"}))
    (run / "gap_report.json").write_text(json.dumps({"paper": "beta", "claims": []}))
    (run / "meta.json").write_text(json.dumps({"title": "Beta", "group": "real", "version": "c5"}))
    (tmp_path / "demo" / "showcase.json").write_text(json.dumps({"real": [{"id": "real~toy-beta"}]}))
    runs = client.get("/api/runs?group=real").json()
    assert [r["id"] for r in runs] == ["real~toy-beta"] and runs[0]["version"] == "c5"
    assert client.get("/api/showcase").json()["real"][0]["id"] == "real~toy-beta"


def test_replay_streams_all_events_and_compresses_idle(client):
    import time

    t0 = time.monotonic()
    with client.stream("GET", "/api/runs/toy-alpha/replay?speed=256") as r:
        body = "".join(r.iter_text())
    assert body.count("event: gf") == 3 and "event: done" in body
    assert time.monotonic() - t0 < 5  # the 59 s idle gap is capped, not replayed


def test_live_mode_refuses_and_spends_nothing(client):
    r = client.post("/api/live")
    assert r.status_code == 503 and not r.json()["ok"]
