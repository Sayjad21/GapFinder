"""Plans D1.3-D1.5 and D7.2 end to end, on new toy instances of the class (not batch-5's PyGOD case).

(a) A detector library renamed a keyword in a middle release (alpha -> weight); the newer release takes the old
    keyword through **kwargs and ignores it. A decoy package is old too and changes nothing. The probe finds the
    package (not the decoy), the release (0.5.0, with 0.4.0 still old-like) and the call site, and verifies the
    rename on the newer release.
(b) The same library with no behavioural change between releases: no effect, and the probe stops at once.
(c) The paper-era code: a later commit changed a constant; the binary search over commits finds it."""

import textwrap

import yaml

from gapfinder import env_year
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec

BENCH = textwrap.dedent('''\
    import argparse, hashlib, os
    from toylib import Detector
    import decoylib
    p = argparse.ArgumentParser()
    p.add_argument("--lr", type=float, default=0.01)
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 50000.0
    m = Detector(alpha=0.8, lr=a.lr)
    auc, ap = m.score()
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write(decoylib.fmt("auc", 100 * (auc + noise)) + decoylib.fmt("ap", 100 * (ap + noise)))
    ''')
OLD = textwrap.dedent('''\
    __version__ = "{v}"
    class Detector:
        def __init__(self, alpha=0.8, lr=0.004, **kwargs):
            self.alpha, self.lr = alpha, lr
        def score(self):
            return 0.70 + 0.2 * self.alpha - (0.01 if self.lr > 0.05 else 0.0), 0.50 + 0.25 * self.alpha
    ''')
NEW = textwrap.dedent('''\
    __version__ = "{v}"
    class Detector:
        def __init__(self, weight=0.5, lr=0.004, **kwargs):
            self.weight, self.lr = weight, lr
        def score(self):
            return 0.70 + 0.2 * self.weight - (0.01 if self.lr > 0.05 else 0.0), 0.50 + 0.25 * self.weight
    ''')
DECOY = 'VERSION = "{v}"\ndef fmt(name, v):\n    return "%s=%.5f\\n" % (name, v)\n'


def _pkg(root, name, src):
    (root / name).mkdir(parents=True)
    (root / name / "__init__.py").write_text(src, encoding="utf-8")


def _setup(tmp_path, monkeypatch, drift=True):
    art, py, rel = tmp_path / "art", tmp_path / "gf_py", tmp_path / "gf_rel"
    art.mkdir()
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    newer = NEW if drift else OLD
    _pkg(art, "toylib", newer.format(v="1.0.0"))  # what is installed now (beside the script)
    _pkg(art, "decoylib", DECOY.format(v="2.0"))
    _pkg(py / "toylib", "toylib", OLD.format(v="0.3.1"))  # the paper-year directories
    _pkg(py / "decoylib", "decoylib", DECOY.format(v="0.9"))
    _pkg(rel / "toylib==0.4.0", "toylib", OLD.format(v="0.4.0"))  # releases a run would install on demand
    _pkg(rel / "toylib==0.5.0", "toylib", newer.format(v="0.5.0"))
    monkeypatch.setenv("GF_PY_ROOT", py.as_posix())
    monkeypatch.setenv("GF_PY_REL", rel.as_posix())
    spec = {
        "name": "lib", "base": f"local:{art.as_posix()}",
        "run": {"command": env_year.run_prefix() + '"${PYTHON:-python3}" bench.py --lr {lr}', "output": "out/run.log",
                "format": "kv", "timeout": 60},
        "knobs": {"lr": {"layer": "config", "default": "0.01"},
                  env_year.KNOB: {"layer": "environment", "default": "0", "choices": ["0", "all", "decoylib", "toylib"]}},
        "allowed_paths": ["out/"], "metrics": ["auc", "ap"],
        "library": {"pins": {
            "toylib": {"old": "0.3.1", "installed": "1.0.0", "dir": "toylib", "releases": ["0.3.1", "0.4.0", "0.5.0", "1.0.0"],
                       "own": False, "modules": ["toylib"], "path": None},
            "decoylib": {"old": "0.9", "installed": "2.0", "dir": "decoylib", "releases": ["0.9", "2.0"], "own": False,
                         "modules": ["decoylib"], "path": None}}}}
    (tmp_path / "s.yaml").write_text(yaml.safe_dump(spec, sort_keys=False, width=400), encoding="utf-8")
    return HarnessSpec.load_yaml(tmp_path / "s.yaml")


def _search(tmp_path, spec, targets):
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=220, trace=False, hm_disc=0.005, patch_knobs=False,
                                                      mutations=False))


async def test_a_renamed_keyword_is_found_to_the_release_and_the_call_site(tmp_path, monkeypatch):
    spec = _setup(tmp_path, monkeypatch)
    s = _search(tmp_path, spec, [Target("C1", "auc", 86.0), Target("C2", "ap", 70.0, held_out=True)])
    [r] = await s.run()
    lib = r.library
    assert lib and lib["effect"] and lib["culprits"] == ["toylib"], (lib, r.notes)  # not the decoy
    [cp] = lib["change_points"]
    assert (cp["package"], cp["before"], cp["after"]) == ("toylib", "0.4.0", "0.5.0")
    assert cp["loaded"]["before"][0] == "0.4.0" and cp["loaded"]["after"][0] == "0.5.0"
    top = cp["leads"][0]
    assert top["kind"] == "swallowed" and top["op"] == "kw.alpha.weight" and top["verified"] is True, cp["leads"]
    assert top["site"] == "bench.py:8"
    assert any("verified at the call site bench.py:8" in n for n in r.notes), r.notes
    ranked = r.differential["ranked"]
    assert any(h["class"] == "library" for h in ranked[:3]), ranked[:3]
    # the date-localised effect is evidence: the paper predates the release that changed the numbers
    assert r.attribution.confidence_label == "Explained" and r.changes in ({env_year.KNOB: "toylib"},
                                                                         {env_year.KNOB: "all"}), (r.changes, r.notes)
    from gapfinder.report.gap_report import GapReport

    rep = GapReport.from_search(s, [r], paper="toy")
    md = rep.to_markdown()
    assert "Library drift: the packages as of the paper's date give the paper's numbers (toylib)" in md
    assert "### Library drift and the paper-era code" in md and "**verified**" in md
    assert GapReport.from_dict(rep.to_dict()).results[0].library["culprits"] == ["toylib"]


async def test_b_no_drift_no_probe(tmp_path, monkeypatch):
    spec = _setup(tmp_path, monkeypatch, drift=False)
    s = _search(tmp_path, spec, [Target("C1", "auc", 90.0), Target("C2", "ap", 75.0, held_out=True)])
    [r] = await s.run()
    assert r.library and r.library["effect"] is False and not r.library["change_points"]
    assert any("no effect beyond noise" in n for n in r.notes)


ERA_BENCH = textwrap.dedent('''\
    import hashlib, os
    import model
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 5000.0
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.4f\\nf1=%.4f\\n" % (90 * model.SCALE + noise, 80 * model.SCALE + noise))
    ''')


async def test_c_the_commit_that_changed_the_numbers(tmp_path, monkeypatch):
    art, era, rel = tmp_path / "art", tmp_path / "era", tmp_path / "era_rel"
    for d, scale in ((art, "0.9"), (era, "1.0"), (rel / "c2", "1.0"), (rel / "c3", "0.9")):
        d.mkdir(parents=True)
        (d / "bench.py").write_text(ERA_BENCH, encoding="utf-8")
        (d / "model.py").write_text(f"SCALE = {scale}\n", encoding="utf-8")
    monkeypatch.setenv("GF_ERA_DIR", era.as_posix())
    monkeypatch.setenv("GF_ERA_REL", rel.as_posix())
    spec = {"name": "era", "base": f"local:{art.as_posix()}",
            "run": {"command": env_year.era_prefix() + '"${PYTHON:-python3}" bench.py', "output": "out/run.log",
                    "format": "kv", "timeout": 60},
            "knobs": {env_year.ERA_KNOB: {"layer": "environment", "default": "0", "choices": ["0", "1"]}},
            "allowed_paths": ["out/"], "metrics": ["acc", "f1"],
            "library": {"era": {"repo": None, "commit": "c4", "sha": "c1", "date": "2020-01-01",
                                "commits": [{"sha": f"c{i}", "message": m} for i, m in
                                            ((1, "first"), (2, "docs"), (3, "tune the scale"), (4, "head"))]}}}
    (tmp_path / "s.yaml").write_text(yaml.safe_dump(spec, sort_keys=False, width=400), encoding="utf-8")
    s = _search(tmp_path, HarnessSpec.load_yaml(tmp_path / "s.yaml"), [Target("C1", "acc", 90.0),
                                                                       Target("C2", "f1", 80.0, held_out=True)])
    [r] = await s.run()
    era_out = r.library["era"]
    assert era_out["effect"] and [(c["before"], c["after"]) for c in era_out["change_points"]] == [("c2", "c3")], r.notes
    assert any("commit c3 (tune the scale) changed the numbers" in n for n in r.notes)
    assert r.changes == {env_year.ERA_KNOB: "1"} and r.attribution.confidence_label == "Explained", (r.changes, r.notes)


async def test_d_a_drift_that_is_not_the_cause(tmp_path, monkeypatch):
    """The library drifts, but the paper's numbers come from a setting (lr) on today's release: the probe reports
    the drift; the answer is the setting, not the library."""
    spec = _setup(tmp_path, monkeypatch)
    s = _search(tmp_path, spec, [Target("C1", "auc", 79.0), Target("C2", "ap", 62.5, held_out=True)])
    [r] = await s.run()
    assert r.library["effect"] and r.library["culprits"] == ["toylib"]
    assert env_year.KNOB not in r.changes and float(r.changes.get("lr", 0)) > 0.05, (r.changes, r.notes)  # any lr > 0.05
