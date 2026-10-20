"""`gapfinder harness` with a paper date on a repository that is itself a library (plans D1.3, D7.2; a new toy, not
batch-5's PyGOD): its own package is pinned to the release from the paper's time, installed into its own directory
(here from a local wheel instead of PyPI), and the knob switches the benchmark script onto it, although the
package's newer code sits beside the script."""

import json
import textwrap
import zipfile
from datetime import date

import yaml

from gapfinder import env_year
from gapfinder.harness_build import build_harness
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec

README = "# toydet\n## Benchmark\n    python bench.py --dataset beta\n"
BENCH = textwrap.dedent('''\
    import argparse
    import toydet
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", default="alpha")
    p.add_argument("--lr", type=float, default=0.01)
    a = p.parse_args()
    auc = toydet.Detector(alpha=0.8).score()
    print("test auc: %.4f test ap: %.4f" % (auc, auc - 0.1))
    ''')
NEW = textwrap.dedent('''\
    __version__ = "1.0.0"
    class Detector:
        def __init__(self, weight=0.5, **kwargs):
            self.weight = weight
        def score(self):
            return 0.6 + 0.3 * self.weight
    ''')
OLD = NEW.replace("1.0.0", "0.3.0").replace("weight", "alpha").replace("alpha=0.5", "alpha=0.8")


def _wheel(where, name, version, init):
    where.mkdir(parents=True, exist_ok=True)
    whl = where / f"{name}-{version}-py3-none-any.whl"
    di = f"{name}-{version}.dist-info"
    with zipfile.ZipFile(whl, "w") as z:
        z.writestr(f"{name}/__init__.py", init)
        z.writestr(f"{di}/METADATA", f"Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n")
        z.writestr(f"{di}/WHEEL", "Wheel-Version: 1.0\nGenerator: gf-test\nRoot-Is-Purelib: true\nTag: py3-none-any\n")
        z.writestr(f"{di}/top_level.txt", f"{name}\n")
        z.writestr(f"{di}/RECORD", f"{name}/__init__.py,,\n{di}/METADATA,,\n{di}/WHEEL,,\n{di}/top_level.txt,,\n{di}/RECORD,,\n")
    return whl


LEDGER = {"claims": [
    {"id": "C1", "metric": "AUC", "reported_value": 84.0, "unit": "%", "type": "absolute", "figure_or_table": "Table 2",
     "conditions": {"dataset": "Beta", "model": "toydet"}},
    {"id": "C2", "metric": "AP", "reported_value": 74.0, "unit": "%", "type": "absolute", "figure_or_table": "Table 2",
     "conditions": {"dataset": "Beta", "model": "toydet"}}]}


async def test_the_repositorys_own_package_from_the_papers_time(tmp_path, monkeypatch):
    repo = tmp_path / "toydet_repo"
    (repo / "toydet").mkdir(parents=True)
    (repo / "toydet" / "__init__.py").write_text(NEW, encoding="utf-8")
    (repo / "setup.py").write_text('from setuptools import setup\nsetup(name="toydet", version="1.0.0")\n')
    (repo / "README.md").write_text(README, encoding="utf-8")
    (repo / "bench.py").write_text(BENCH, encoding="utf-8")
    cache = tmp_path / "pypi"
    cache.mkdir()
    rel = lambda day: [{"upload_time": f"{day}T00:00:00", "requires_python": None, "size": 2000,  # noqa: E731
                        "filename": "toydet-x-py3-none-any.whl"}]
    (cache / "toydet.json").write_text(json.dumps({"releases": {"0.3.0": rel("2018-05-01"), "1.0.0": rel("2020-02-01")}}))
    wheels = tmp_path / "wheels"
    _wheel(wheels, "toydet", "0.3.0", OLD)
    monkeypatch.setenv("GF_PYPI_CACHE", str(cache))
    monkeypatch.setenv("GF_PY_ROOT", (tmp_path / "gf_py").as_posix())
    for k, v in (("NO_INDEX", "1"), ("FIND_LINKS", wheels.as_posix())):  # offline: the local wheel only
        monkeypatch.setenv("PIP_" + k, v)
        monkeypatch.setenv("UV_" + k, v)
    import importlib.util
    import shutil

    if importlib.util.find_spec("pip") is None:  # a uv-made environment has no pip; the VMs do
        monkeypatch.setenv("GF_PIP", "uv pip")
        assert shutil.which("uv"), "this test needs pip or uv"
    backend = LocalBackend(tmp_path / "sbx")
    env = await backend.base("local:" + str(repo))
    out = tmp_path / "h"
    r = await build_harness(None, backend, repo=None, commit=None, local=repo, ledger=LEDGER, target="C1", out=out,
                            repeats=1, smoke_timeout=120, env_checkpoint=env, paper_date=date(2019, 6, 1))
    md = (out / "HARNESS.md").read_text(encoding="utf-8")
    assert r.ok, md
    y = r.paper_year
    assert y["own"]["dist"] == "toydet" and y["pins"] == {"toydet": "0.3.0"} and y["used"], {k: v for k, v in y.items() if k != "releases"}
    assert "the repository's own package" in md
    spec_d = yaml.safe_load((out / "spec.yaml").read_text(encoding="utf-8"))
    assert spec_d["knobs"][env_year.KNOB]["choices"] == ["0", "all"]
    pin = spec_d["library"]["pins"]["toydet"]
    assert pin["own"] and pin["releases"] == ["0.3.0", "1.0.0"] and pin["modules"] == ["toydet"] and pin["path"] == "toydet"

    spec = HarnessSpec.load_yaml(out / "spec.yaml")
    spec.base = "local:" + str(backend.images / spec.base)
    orch = Orchestrator(backend, spec, EventLog(tmp_path / "ev.jsonl"))
    now = await orch.run_branch({})
    then = await orch.run_branch({env_year.KNOB: "all"})
    name = r.claims[0]["name"]
    assert abs(now.parsed_metrics[name] - 75.0) < 1e-6, now.note  # weight 0.5 (alpha=0.8 swallowed)
    assert abs(then.parsed_metrics[name] - 84.0) < 1e-6, then.note  # the paper-era release: alpha=0.8 is used
