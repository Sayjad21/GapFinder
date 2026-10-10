import importlib.util
import json
from pathlib import Path

_spec = importlib.util.spec_from_file_location("load_variance", Path(__file__).parents[2] / "eval" / "load_variance.py")
lv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lv)


def _event(parent, k10_k5, k1_k5, k1_k10, knobs=None):
    m = {"balanced_ratio_k10_k5": k10_k5, "balanced_ratio_k1_k5": k1_k5, "writeheavy_ratio_k1_k10": k1_k10}
    return {"type": "branch_finished",
            "branch": {"parent_checkpoint": parent, "knob_changes": knobs or {}, "status": "succeeded", "parsed_metrics": m}}


def _write(d: Path, events):
    d.mkdir(parents=True)
    (d / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events), encoding="utf-8")
    return d


def test_forked_outside_fresh_band(tmp_path):
    # one load with 4 forked naive runs, all near 2.0; five fresh loads near 1.0; a non-naive run is ignored
    forked = _write(tmp_path / "fork", [_event("L0", 2.0, 2.0, 2.0) for _ in range(4)] + [_event("L0", 9, 9, 9, {"x": 1})])
    fresh = _write(tmp_path / "fresh", [_event(f"F{i}", v, v, v) for i, v in enumerate([0.9, 1.0, 1.0, 1.1, 1.0])])
    res = lv.comparability([forked, fresh])
    assert res["forked_loads"] == 1 and res["forked_runs"] == 4 and res["fresh_loads"] == 5
    m = res["metrics"]["C5"]
    assert m["forked"]["median"] == 2.0 and m["fresh"]["median"] == 1.0
    assert m["fresh"]["mad"] == 0.0 and m["fresh"]["min"] == 0.9 and m["fresh"]["max"] == 1.1
    assert m["forked_median_inside_band"] is False
    assert m["forked_load_medians_inside_band"] == 0
    assert "OUTSIDE" in lv.comparability_text(res)


def test_forked_inside_fresh_band(tmp_path):
    forked = _write(tmp_path / "fork", [_event("L0", 1.0, 1.0, 1.0) for _ in range(3)])
    fresh = _write(tmp_path / "fresh", [_event(f"F{i}", v, v, v) for i, v in enumerate([0.8, 0.9, 1.0, 1.1, 1.2])])
    m = lv.comparability([forked, fresh])["metrics"]["C3"]
    assert m["forked_median_inside_band"] is True and m["forked_runs_inside_band"] == 3
