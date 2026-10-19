"""The paper-year environment as one knob (plan item 19, docs/CONTEXT_v11.md section 7).

Library defaults drift: a reproduction run on today's packages can differ from the paper's because a default
changed between versions (dependency drift: scikit-learn's LogisticRegression solver in 0.22, PyTorch's and
TensorFlow's initialisers and reductions, pandas' groupby). One knob tests that whole class at once:

- for each package the code imports, the newest release published on PyPI before the paper's date that
  supports the environment's Python (PyPI's JSON API: upload dates and requires_python);
- those versions are installed with `pip --target` into a separate directory of the same base checkpoint,
  without dependencies (only the packages the code imports change), and only where they differ from what the
  environment has;
- the knob `gf_paper_year_env` (0/1) puts that directory first on PYTHONPATH.

If the old set doesn't import, the knob is dropped with the reason: nothing is guessed.
"""

from __future__ import annotations

import json
import re
import urllib.request
from datetime import date, datetime
from pathlib import Path

TARGET_DIR = "/opt/gf_paper_year"
KNOB = "gf_paper_year_env"

# import name -> distribution name, where they differ
DIST = {"sklearn": "scikit-learn", "cv2": "opencv-python", "PIL": "Pillow", "yaml": "PyYAML", "skimage": "scikit-image",
        "torch_geometric": "torch-geometric", "dgl": "dgl", "bs4": "beautifulsoup4", "Crypto": "pycryptodome",
        "dateutil": "python-dateutil", "google.protobuf": "protobuf", "tensorflow_probability": "tensorflow-probability",
        "torch_scatter": "torch-scatter", "torch_sparse": "torch-sparse", "lightgbm": "lightgbm", "attr": "attrs"}
# compiled against each other or the interpreter: changing one alone breaks the others (never pinned here)
SKIP = {"pip", "setuptools", "wheel", "numpy_financial", "torch_scatter", "torch-scatter", "torch_sparse",
        "torch-sparse", "torch-cluster", "torch-spline-conv"}


def paper_date(arxiv_id: str | None = None, fallback: str | None = None) -> date | None:
    """The first day after the month of the arXiv id (YYMM.NNNNN), else the fallback ISO date."""
    if arxiv_id and (m := re.match(r"(\d{2})(\d{2})\.\d{4,5}", arxiv_id)):
        y, mo = 2000 + int(m.group(1)), int(m.group(2))
        return date(y + (mo == 12), mo % 12 + 1, 1)
    if fallback:
        try:
            return date.fromisoformat(fallback[:10])
        except ValueError:
            return None
    return None


def _fetch(dist: str, cache: Path | None) -> dict | None:
    p = cache / f"{dist.lower()}.json" if cache else None
    if p and p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    try:
        raw = urllib.request.urlopen(urllib.request.Request(
            f"https://pypi.org/pypi/{dist}/json", headers={"User-Agent": "gapfinder"}), timeout=30).read()
    except Exception:  # noqa: BLE001 (no network, unknown package: no pin)
        return None
    d = json.loads(raw)
    if p:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"releases": d.get("releases", {})}), encoding="utf-8")
    return d


def _ver_key(v: str) -> tuple:
    return tuple(int(x) if x.isdigit() else -1 for x in re.split(r"[.]", re.sub(r"[^0-9.].*$", "", v)) if x != "")


def _python_ok(spec: str | None, python: str) -> bool:
    if not spec:
        return True
    try:
        from packaging.specifiers import SpecifierSet

        return SpecifierSet(spec).contains(python, prereleases=True)
    except Exception:  # noqa: BLE001 (an unparsable spec: don't exclude on it)
        return True


def version_at(releases: dict, when: date, python: str) -> str | None:
    """The newest final release first uploaded before `when` with a file that supports `python`."""
    best = None
    for v, files in releases.items():
        if not files or re.search(r"[a-zA-Z]", v.replace("post", "")):  # pre-releases, dev builds
            continue
        first = min(datetime.fromisoformat(f["upload_time"][:19]).date() for f in files)
        if first >= when or not any(_python_ok(f.get("requires_python"), python) for f in files):
            continue
        if best is None or _ver_key(v) > _ver_key(best):
            best = v
    return best


def paper_year_pins(modules: list[str], installed: dict[str, str], when: date, python: str,
                    cache: Path | None = None) -> tuple[dict[str, str], dict[str, str]]:
    """(dist -> version to install, dist -> why not pinned) for the imported modules."""
    pins, skipped = {}, {}
    inst = {k.lower().replace("_", "-"): v for k, v in installed.items()}
    for m in modules:
        dist = DIST.get(m, m)
        key = dist.lower().replace("_", "-")
        if dist in SKIP or key in SKIP:
            skipped[dist] = "compiled against other packages"
            continue
        if key not in inst:
            skipped[dist] = "not installed (part of another package, or not needed)"
            continue
        d = _fetch(dist, cache)
        if d is None:
            skipped[dist] = "not on PyPI"
            continue
        v = version_at(d.get("releases", {}), when, python)
        if v is None:
            skipped[dist] = f"no release before {when} for Python {python}"
        elif _ver_key(v) >= _ver_key(inst[key]):
            skipped[dist] = f"installed {inst[key]} is already from then"
        else:
            pins[dist] = v
    return pins, skipped


def install_command(pins: dict[str, str]) -> str:
    """One pip call per pin into TARGET_DIR (no dependencies); a pin that fails is reported, not fatal."""
    steps = [f'(pip install --no-cache-dir --no-deps --target {TARGET_DIR} "{d}=={v}" >/dev/null 2>&1 '
             f'&& echo GF_PIN_OK {d} {v} || echo GF_PIN_FAIL {d} {v})' for d, v in sorted(pins.items())]
    return f"mkdir -p {TARGET_DIR}; " + "; ".join(steps)


def run_prefix() -> str:
    return f'if [ "{{{KNOB}}}" = 1 ]; then export PYTHONPATH="{TARGET_DIR}${{PYTHONPATH:+:$PYTHONPATH}}"; fi; '


FREEZE = ('"${PYTHON:-python}" -c "import sys; print(\'GF_PY\', \'%d.%d.%d\' % sys.version_info[:3])"; '
          '"${PYTHON:-python}" -m pip freeze 2>/dev/null | sed "s/^/GF_FREEZE /"')


def parse_freeze(stdout: str) -> tuple[str | None, dict[str, str]]:
    py = re.search(r"GF_PY (\S+)", stdout or "")
    pkgs = dict(re.findall(r"(?m)^GF_FREEZE ([A-Za-z0-9_.-]+)==([^\s;]+)", stdout or ""))
    return (py.group(1) if py else None), pkgs
