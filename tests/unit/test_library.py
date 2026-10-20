"""Library drift (gapfinder/diagnose/library.py, env_year.py, the runtime shim's import redirect): new toy instances."""

import asyncio
import os
import subprocess
import sys
import textwrap

from gapfinder import env_year
from gapfinder.diagnose import library as L
from gapfinder.sandbox import runtime_shim


def run(c):
    return asyncio.run(c)


def test_ddmin_finds_an_interaction_of_two_among_six():
    calls = []

    async def test(sub):
        calls.append(sorted(sub))
        return {"numpy", "scipy"} <= set(sub)

    items = ["a", "b", "numpy", "c", "scipy", "d"]
    sub, n, minimal = run(L.ddmin(items, test))
    assert sorted(sub) == ["numpy", "scipy"] and minimal
    assert n == len({tuple(c) for c in calls})  # cached: no subset tested twice


def test_ddmin_uses_what_is_known_and_stops_at_its_cap():
    async def test(sub):
        return "x" in sub

    sub, n, _ = run(L.ddmin(["x", "y"], test, known={frozenset(["x"]): True}))
    assert sub == ["x"] and n == 0
    sub, n, minimal = run(L.ddmin(list("abcdefgh"), lambda s: asyncio.sleep(0, result=False), max_tests=2))
    assert not minimal and n <= 4


def test_change_points_one_and_two_changes():
    seq = ["0.3", "0.4", "0.5", "0.6", "0.7", "1.0"]
    value = {"0.3": 1, "0.4": 1, "0.5": 2, "0.6": 2, "0.7": 3, "1.0": 3}
    seen = []

    async def same(a, b):
        seen.append((a, b))
        return value[a] == value[b]

    assert run(L.change_points(seq, same)) == [("0.4", "0.5"), ("0.6", "0.7")]
    value.update({"0.7": 2, "1.0": 2})
    assert run(L.change_points(seq, same)) == [("0.4", "0.5")]
    value.update({k: 1 for k in value})
    assert run(L.change_points(seq, same)) == []


TOY = textwrap.dedent('''\
    import numpy as np
    import toylib.models as tm
    from toylib.models import Detector as D
    from toylib import utils
    m = D(alpha=0.8, lr=0.01)
    m.fit(np.zeros(3))
    tm.Other(3, k=2)
    utils.helper(*args)
    class Runner:
        def __init__(self):
            self.det = D(epoch=3)
        def go(self):
            return self.det.decision_function(1)
    ''')


def test_call_sites_through_imports_and_instances(tmp_path):
    (tmp_path / "main.py").write_text(TOY, encoding="utf-8")
    (tmp_path / "toylib").mkdir()
    (tmp_path / "toylib" / "inner.py").write_text("from toylib.models import Detector\nDetector(alpha=1)\n")
    sites = L.call_sites(tmp_path, ["toylib"], exclude=["toylib"])
    got = {(s.qual, tuple(s.keywords), s.n_args, s.star, s.bound) for s in sites}
    assert ("toylib.models.Detector", ("alpha", "lr"), 0, False, False) in got
    assert ("toylib.models.Detector.fit", (), 1, False, True) in got
    assert ("toylib.models.Other", ("k",), 1, False, False) in got
    assert ("toylib.utils.helper", (), 0, True, False) in got
    assert ("toylib.models.Detector.decision_function", (), 1, False, True) in got
    assert all(s.file == "main.py" for s in sites)  # the package's own code is left out
    assert not any(s.qual.startswith("numpy") for s in sites)


OLD = textwrap.dedent('''\
    __version__ = "0.3.1"
    class Base:
        def __init__(self, contamination=0.1, **kwargs):
            self.contamination = contamination
    class Detector(Base):
        def __init__(self, alpha=0.8, epoch=5, lr=0.004, hidden=64, **kwargs):
            super().__init__(**kwargs)
            self.alpha, self.epoch, self.lr = alpha, epoch, lr
            self.dropout = kwargs.get("dropout", 0.3)
        def fit(self, x, y=None):
            return _loss(x, self.alpha)
    def _loss(x, a):
        return a * x
    def split(data, ratio=0.2, seed=0):
        return data
    ''')
NEW = textwrap.dedent('''\
    __version__ = "1.0.0"
    class Base:
        def __init__(self, contamination=0.1, **kwargs):
            self.contamination = contamination
    class Detector(Base):
        def __init__(self, weight=0.5, epoch=100, lr=0.004, hidden=64, **kwargs):
            super().__init__(**kwargs)
            self.weight, self.epoch, self.lr = weight, epoch, lr
        def fit(self, x, y=None):
            return _loss(x, self.weight)
    def _loss(x, a):
        return a * x + 0.0
    def split(seed, data, ratio=0.2):
        return data
    ''')
CALLER = textwrap.dedent('''\
    from toylib import Detector, split
    m = Detector(alpha=0.8, lr=0.01, contamination=0.05, dropout=0.5)
    print(m.fit(2.0))
    split([1, 2], 0.3)
    ''')


def _probe(tmp_path, side_dirs):
    work = tmp_path / "work"
    work.mkdir()
    (work / "main.py").write_text(CALLER, encoding="utf-8")
    sites = L.call_sites(work, ["toylib"])
    for k, v in L.probe_files([s.qual for s in sites]).items():
        (work / k).parent.mkdir(exist_ok=True)
        (work / k).write_bytes(v)
    hook = tmp_path / "hook"
    hook.mkdir()
    (hook / "sitecustomize.py").write_text(runtime_shim.HOOK_SOURCE, encoding="utf-8")
    out = {}
    for side, d in side_dirs.items():
        env = {**os.environ, "PYTHONPATH": str(hook), "GF_LIB_DIRS": str(d)}
        r = subprocess.run([sys.executable, ".gf_lib/probe.py", side, ".gf_lib/names.json"], cwd=work, env=env,
                           capture_output=True, text=True, timeout=120)
        out[side] = L.parse_probe(r.stdout, side)
    return sites, out


def test_api_diff_under_two_releases(tmp_path):
    for name, src in (("old", OLD), ("new", NEW)):
        (tmp_path / name / "toylib").mkdir(parents=True)
        (tmp_path / name / "toylib" / "__init__.py").write_text(src, encoding="utf-8")
    sites, out = _probe(tmp_path, {"A": tmp_path / "old", "B": tmp_path / "new"})
    assert out["A"]["versions"]["toylib"][0] == "0.3.1" and out["B"]["versions"]["toylib"][0] == "1.0.0"
    leads = L.compare(sites, out["A"], out["B"], "0.3.1", "1.0.0")
    kinds = {(x.kind, x.op) for x in leads}
    assert ("swallowed", "kw.alpha.weight") in kinds  # renamed, the old keyword vanishes into **kwargs
    assert leads[0].kind == "swallowed" and leads[0].op == "kw.alpha.weight"
    assert any(x.kind == "swallowed" and "dropout" in x.detail for x in leads)  # read from **kwargs, then not
    assert any(x.kind == "default" and "epoch" in x.detail and x.op.startswith("kwset.epoch.") for x in leads)
    assert not any("contamination" in x.detail for x in leads)  # forwarded to the base class in both
    assert not any(x.kind == "default" and "hidden" in x.detail for x in leads)  # unchanged default
    assert any(x.kind == "positional" and "seed" in x.detail for x in leads)
    assert any(x.kind == "source" and "_loss" in x.qual and any("+ 0.0" in ln for ln in x.diff) for x in leads)


def test_the_redirect_beats_a_package_beside_the_script(tmp_path):
    (tmp_path / "old" / "toylib").mkdir(parents=True)
    (tmp_path / "old" / "toylib" / "__init__.py").write_text('V = "old"\n')
    (tmp_path / "old" / "toylib-0.3.1.dist-info").mkdir()
    (tmp_path / "old" / "toylib-0.3.1.dist-info" / "top_level.txt").write_text("toylib\n")
    work = tmp_path / "work"
    (work / "toylib").mkdir(parents=True)
    (work / "toylib" / "__init__.py").write_text('V = "new"\n')
    (work / "main.py").write_text("import toylib, json\nprint(toylib.V)\n")
    hook = tmp_path / "hook"
    hook.mkdir()
    (hook / "sitecustomize.py").write_text(runtime_shim.HOOK_SOURCE, encoding="utf-8")

    def go(dirs):
        env = {**os.environ, "PYTHONPATH": str(hook), "GF_LIB_DIRS": dirs}
        return subprocess.run([sys.executable, "main.py"], cwd=work, env=env, capture_output=True, text=True).stdout.strip()

    assert go("") == "new"
    assert go(str(tmp_path / "old")) == "old"
    assert go(str(tmp_path / "missing") + "|" + str(tmp_path / "old")) == "old"


def _bash():
    from gapfinder.sandbox.backend import _find_bash

    return _find_bash()


def test_run_prefix_values(tmp_path):
    root, rel = tmp_path / "py", tmp_path / "rel"
    for d in ("scikit_learn", "torch_geometric"):
        (root / d).mkdir(parents=True)
    (rel / "torch-geometric==2.1.0").mkdir(parents=True)

    def dirs(value):
        cmd = env_year.run_prefix().replace("{%s}" % env_year.KNOB, value) + 'echo "DIRS=$GF_LIB_DIRS"'
        env = {**os.environ, "GF_PY_ROOT": root.as_posix(), "GF_PY_REL": rel.as_posix()}
        out = subprocess.run([_bash(), "-c", cmd], env=env, capture_output=True, text=True).stdout
        return [x.rsplit("/", 1)[-1] for x in out.split("DIRS=")[1].strip().split("|") if x]

    assert dirs("0") == []
    assert dirs("all") == dirs("1") == ["scikit_learn", "torch_geometric"]
    assert dirs("scikit_learn") == ["scikit_learn"]
    assert dirs("scikit_learn,torch-geometric==2.1.0") == ["scikit_learn", "torch-geometric==2.1.0"]


def test_own_package_releases_and_choices(tmp_path):
    (tmp_path / "setup.py").write_text('from setuptools import setup\nsetup(name="pygod", packages=["pygod"])\n')
    (tmp_path / "pygod").mkdir()
    (tmp_path / "pygod" / "version.py").write_text('__version__ = "1.0.0"\n')
    (tmp_path / "pygod" / "__init__.py").write_text("")
    assert env_year.own_package(tmp_path) == {"dist": "pygod", "version": "1.0.0", "module": "pygod", "path": "pygod"}

    def rel(day, size=10):
        return [{"upload_time": f"{day}T10:00:00", "requires_python": ">=3.7", "filename": "x-py3-none-any.whl",
                 "size": size * 2 ** 20}]

    releases = {"0.2.0": rel("2021-01-01"), "0.3.0": rel("2022-03-01"), "0.3.1": rel("2022-06-01"),
                "0.4.0": rel("2023-01-01"), "1.0.0rc1": rel("2023-05-01"), "1.0.0": rel("2023-06-01")}
    import json
    from datetime import date

    cache = tmp_path / "cache"
    cache.mkdir()
    (cache / "pygod.json").write_text(json.dumps({"releases": releases}))
    got: dict = {}
    pins, why = env_year.paper_year_pins([], {}, date(2022, 9, 1), "3.10.4", cache=cache,
                                         own=env_year.own_package(tmp_path), releases=got)
    assert pins == {"pygod": "0.3.1"} and got["pygod"] == ["0.3.1", "0.4.0", "1.0.0"]
    assert env_year.wheel_mb(rel("2022-01-01", 900), "3.10.4") == 900
    assert env_year.knob_choices([["a"], ["b", "n"]], True) == ["0", "all", "a", "b,n"]
    assert env_year.knob_choices([["a"]], True) == ["0", "all"]
    assert env_year.knob_choices([["a"], ["b"]], False) == ["0", "a", "b"]
    cmd = env_year.install_command({"torch": "1.8.0", "pygod": "0.3.1"})
    assert "--index-url https://download.pytorch.org/whl/cpu --target \"${GF_PY_ROOT:-/opt/gf_py}/torch\" \"torch==1.8.0\"" in cmd
    assert "--target \"${GF_PY_ROOT:-/opt/gf_py}/pygod\" \"pygod==0.3.1\"" in cmd and "GF_PIN_FAIL pygod" in cmd


def test_big_old_wheels_are_not_pinned(tmp_path):
    import json
    from datetime import date

    files = [{"upload_time": "2020-01-01T00:00:00", "requires_python": None, "size": 700 * 2 ** 20,
              "filename": "tensorflow-2.1.0-cp37-cp37m-manylinux2010_x86_64.whl"}]
    (tmp_path / "tensorflow.json").write_text(json.dumps({"releases": {"2.1.0": files}}))
    pins, why = env_year.paper_year_pins(["tensorflow"], {"tensorflow": "2.15.0"}, date(2020, 6, 1), "3.7.3", cache=tmp_path)
    assert pins == {} and "too large" in why["tensorflow"]


def test_dependency_pins_resolve_only_the_conflicting_part(tmp_path):
    """An old release's own requirements: an installed dependency it excludes, and one not installed, get the newest
    release before the paper's date inside the requirement; satisfied ones, extras and other platforms don't."""
    import json
    from datetime import date

    def rel(*vs):
        return {v: [{"upload_time": f"{d}T00:00:00", "requires_python": None, "size": 1000,
                     "filename": "x-py3-none-any.whl"}] for v, d in vs}

    (tmp_path / "geolib-0.4.json").write_text(json.dumps({"requires_dist": [
        "numpy (<1.24,>=1.16)", "scipy", "sparsekit>=0.6; python_version >= '3.6'", "pywin32; sys_platform == 'win32'",
        "pytest; extra == 'test'"]}))
    (tmp_path / "numpy.json").write_text(json.dumps({"releases": rel(("1.21.0", "2021-06-22"), ("1.23.5", "2022-11-20"),
                                                                     ("1.26.0", "2023-09-16"))}))
    (tmp_path / "sparsekit.json").write_text(json.dumps({"releases": rel(("0.6.1", "2021-01-01"), ("0.9.0", "2023-01-01"))}))
    (tmp_path / "sparsekit-0.6.1.json").write_text(json.dumps({"requires_dist": []}))
    (tmp_path / "numpy-1.23.5.json").write_text(json.dumps({"requires_dist": []}))
    extra, why, brought = env_year.dependency_pins({"geolib": "0.4"}, {"numpy": "1.26.4", "scipy": "1.11.0"},
                                                   date(2022, 12, 1), "3.10.4", cache=tmp_path)
    assert extra == {"numpy": "1.23.5", "sparsekit": "0.6.1"}, (extra, why)
    assert "installed: 1.26.4" in why["numpy"] and "installed: none" in why["sparsekit"]
    assert brought == {"geolib": ["numpy", "sparsekit"]}
    assert env_year.bundle("geolib", brought) == ["geolib", "numpy", "sparsekit"]
