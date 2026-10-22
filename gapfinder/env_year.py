"""The paper-year environment (plan item 19; D1.3 and D7.2, docs/CONTEXT_v11.md section 7.2).

Library defaults and APIs drift: a reproduction on today's packages can differ from the paper's because a default
changed, a keyword was renamed (an old keyword then vanishes into **kwargs), or the repository is itself a library
whose benchmark scripts now run its newest release (batch-5 b5c: PyGOD 1.0 against the paper's 0.3.1).

- For each package the code imports, and for the repository's own package when it is on PyPI: the newest final
  release uploaded before the paper's date that supports the environment's Python (PyPI's JSON API), when it is
  older than what is installed. Wheels too large for the VM are not pinned; torch, torchvision and torchaudio come
  from PyTorch's CPU index.
- Each old release goes into its own directory, `/opt/gf_py/<dist>`, without dependencies, so any subset can be
  switched on: the knob `gf_paper_year_env` takes `0`, `all`, a comma list of directories, or `dist==version` (a
  release installed on demand into the run's VM, for the binary search over releases).
- The switch is an import redirect in the runtime shim (GF_LIB_DIRS): the old directories' top-level modules are
  imported from there whatever sys.path says, so an old release wins even over a package beside the script.
- The paper-era code: the repository's last commit before the paper's date (history before the given commit only)
  is fetched into `/opt/gf_paper_era`; the knob `gf_paper_era_code=1` copies its code files over the checkout.

What doesn't install or import is dropped with the reason: nothing is guessed. gapfinder/diagnose/library.py turns
a library effect into the package, the release and the call site.
"""

from __future__ import annotations

import json
import re
import urllib.request
from datetime import date, datetime
from pathlib import Path

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


def installable(f: dict, python: str) -> bool:
    """A release file pip could install on Linux x86_64 under `python`: its requires_python allows it, and a wheel's
    tags match (cpXY, py3, abi3; any or manylinux x86_64), or it is a source archive. Old wheels often declare no
    requires_python (tensorflow 1.7 has cp27-cp36 wheels and none for 3.7, yet no metadata says so)."""
    if not _python_ok(f.get("requires_python"), python):
        return False
    name = f.get("filename")
    if not name:
        return True  # no file name recorded: nothing to judge by
    if not name.endswith(".whl"):
        return name.endswith((".tar.gz", ".zip", ".tar.bz2"))
    tag = "cp" + "".join(python.split(".")[:2])
    parts = name[:-4].split("-")
    if len(parts) < 5:
        return True
    py_tags, abi_tags, plat = parts[-3].split("."), parts[-2].split("."), parts[-1]
    py_ok = tag in py_tags or "py3" in py_tags or (any(t.startswith("cp3") and t <= tag for t in py_tags)
                                                    and "abi3" in abi_tags)
    plat_ok = plat == "any" or ("linux" in plat and "x86_64" in plat)
    return py_ok and plat_ok


def compiled(releases: dict) -> bool:
    """The distribution has C extensions: some release, of any date, ships a platform wheel (a tag other than `any`).
    Pre-wheel installers (.exe, .egg) don't tell: pure packages shipped them too (networkx 1.0)."""
    return any(str(f.get("filename", "")).endswith(".whl") and not str(f["filename"])[:-4].endswith("-any")
               for files in releases.values() for f in files)


def release_installable(files: list[dict], python: str, is_compiled: bool = False) -> bool:
    """A release pip could install under `python` without building a C extension: a matching file, where a compiled
    distribution (compiled()) needs a matching wheel; its source archive would be compiled against this Python,
    which an old extension's source rarely survives (numpy 1.11.1 on Python 3.10 and numpy 1.14.2 on 3.7 both failed
    to build). A pure package's source archive counts."""
    return any(installable(f, python) and not (is_compiled and f.get("filename") and not f["filename"].endswith(".whl"))
               for f in files)


def _finals(releases: dict, spec=None):
    """(version, first upload date, files) for each final release (inside `spec`, when given)."""
    for v, files in releases.items():
        if not files or re.search(r"[a-zA-Z]", v.replace("post", "")):  # pre-releases, dev builds
            continue
        if spec is not None and not spec.contains(v, prereleases=False):
            continue
        yield v, min(datetime.fromisoformat(f["upload_time"][:19]).date() for f in files), files


def version_at(releases: dict, when: date, python: str, spec=None) -> str | None:
    """The newest final release first uploaded before `when` that installs under `python` (release_installable),
    inside the specifier `spec` (a packaging SpecifierSet) when given."""
    best, c = None, compiled(releases)
    for v, first, files in _finals(releases, spec):
        if first >= when or not release_installable(files, python, c):
            continue
        if best is None or _ver_key(v) > _ver_key(best):
            best = v
    return best


# A compiled package ships wheels for a new Python some months after that Python's release, so a paper written just
# before then has no installable release from its date: the first one after it, within this window, is that era's
# package for this Python (RippleNet, 2018-04-01, on Python 3.7: numpy 1.14.5 of 2018-06-12). Beyond it, not pinned.
NEAREST_DAYS = 183


def first_after(releases: dict, when: date, python: str, spec=None, days: int = NEAREST_DAYS) -> tuple[str, date] | None:
    """(version, upload date) of the oldest final release uploaded on or after `when`, within `days`, that installs
    under `python`; None when there is none."""
    best, c = None, compiled(releases)
    for v, first, files in _finals(releases, spec):
        if not (when <= first and (first - when).days <= days) or not release_installable(files, python, c):
            continue
        if best is None or _ver_key(v) < _ver_key(best[0]):
            best = (v, first)
    return best


TORCH_CPU = {"torch", "torchvision", "torchaudio"}  # from download.pytorch.org/whl/cpu (PyPI's are CUDA builds)
CPU_INDEX = "https://download.pytorch.org/whl/cpu"
MAX_WHEEL_MB = 400  # a larger old wheel doesn't fit the VM's disk and memory budget beside the installed one


def wheel_mb(files: list[dict], python: str) -> float | None:
    """The smallest file pip could install on Linux x86_64 under `python` (MB): a matching wheel, else the sdist."""
    tag = "cp" + "".join(python.split(".")[:2])
    sizes = []
    for f in files:
        name, size = f.get("filename", ""), f.get("size")
        if size is None:
            continue
        if name.endswith(".whl"):
            plat_ok = "none-any" in name or ("linux" in name and "x86_64" in name)
            py_ok = "py3" in name or "py2.py3" in name or f"-{tag}-" in name or "abi3" in name
            if plat_ok and py_ok:
                sizes.append(size)
        elif name.endswith((".tar.gz", ".zip")):
            sizes.append(size)
    return min(sizes) / 2 ** 20 if sizes else None


def releases_between(releases: dict, lo: str, hi: str, python: str) -> list[str]:
    """Final releases from `lo` to `hi` (both included) with a file for `python`, oldest first: the binary search's
    range."""
    out = []
    for v, files in releases.items():
        if not files or re.search(r"[a-zA-Z]", v.replace("post", "")):
            continue
        if not (_ver_key(lo) <= _ver_key(v) <= _ver_key(hi)):
            continue
        if any(_python_ok(f.get("requires_python"), python) for f in files):
            out.append(v)
    out.sort(key=_ver_key)
    if hi not in out:
        out.append(hi)  # the installed version may be a local or a pre-release build
    return out


def own_package(root: str | Path) -> dict | None:
    """The package the repository itself is ({"dist", "version", "module", "path"}), from setup.py, setup.cfg or
    pyproject.toml, with its import name and directory (PyGOD's benchmark repo is the PyGOD library); None when the
    repository is not a package or its package directory isn't found."""
    root = Path(root)
    texts = {n: (root / n).read_text(encoding="utf-8", errors="replace") for n in ("setup.py", "setup.cfg", "pyproject.toml")
             if (root / n).is_file()}
    name = version = None
    for n, t in texts.items():
        m = re.search(r"""(?m)^\s*name\s*[=:]\s*["']?([A-Za-z0-9_.-]+)["']?""", t) if n != "setup.py" else \
            re.search(r"""\bname\s*=\s*["']([A-Za-z0-9_.-]+)["']""", t)
        if m and not name:
            name = m.group(1)
        v = re.search(r"""\bversion\s*[=:]\s*["']([0-9][A-Za-z0-9_.+-]*)["']""", t)
        if v and not version:
            version = v.group(1)
    if not name:
        return None
    module = name.replace("-", "_").lower()
    path = next((d for d in (module, f"src/{module}") if (root / d / "__init__.py").is_file()), None)
    if path is None:
        return None
    if not version:  # a version file: pkg/version.py, pkg/__init__.py
        for f in (root / path / "version.py", root / path / "__init__.py"):
            v = re.search(r"""__version__\s*=\s*["']([0-9][A-Za-z0-9_.+-]*)["']""",
                          f.read_text(encoding="utf-8", errors="replace")) if f.is_file() else None
            if v:
                version = v.group(1)
                break
    return {"dist": name, "version": version, "module": module, "path": path}


def paper_year_pins(modules: list[str], installed: dict[str, str], when: date, python: str,
                    cache: Path | None = None, own: dict | None = None,
                    releases: dict[str, list[str]] | None = None) -> tuple[dict[str, str], dict[str, str]]:
    """(dist -> version to install, dist -> why not pinned, or why a pin is from after the date: first_after) for
    the imported modules, and for the repository's own
    package (`own`, from own_package) when it is on PyPI: a library-benchmark repo (PyGOD, PyG, RecBole) runs the
    library as it is now, while the paper ran a release from its time (batch-5 b5c: PyGOD 1.0 against 0.3.1).
    `releases`, when given, receives each pinned package's releases from the pin to the installed one."""
    pins, skipped = {}, {}
    inst = {k.lower().replace("_", "-"): v for k, v in installed.items()}
    todo = [(DIST.get(m, m), False) for m in modules]
    if own:
        k0 = own["dist"].lower().replace("_", "-")
        todo = [(own["dist"], True)] + [x for x in todo if x[0].lower().replace("_", "-") != k0]
    for dist, is_own in todo:
        key = dist.lower().replace("_", "-")
        if dist in SKIP or key in SKIP:
            skipped[dist] = "compiled against other packages"
            continue
        have = (own["version"] or "local") if is_own else inst.get(key)
        if have is None:
            skipped[dist] = "not installed (part of another package, or not needed)"
            continue
        d = _fetch(dist, cache)
        if d is None:
            skipped[dist] = "not on PyPI"
            continue
        v = version_at(d.get("releases", {}), when, python)
        near = first_after(d.get("releases", {}), when, python) if v is None else None
        if near:
            v = near[0]
            skipped[dist] = (f"{v} ({near[1]}, {(near[1] - when).days} days after the date): no release before it "
                             f"installs on Python {python}")
        if v is None:
            skipped[dist] = f"no release before {when} for Python {python}"
        elif have != "local" and _ver_key(v) >= _ver_key(have):
            skipped[dist] = f"installed {have} is already from then"
        elif key not in TORCH_CPU and (mb := wheel_mb(d["releases"].get(v, []), python)) and mb > MAX_WHEEL_MB:
            skipped[dist] = f"{dist}=={v} is {mb:.0f} MB, too large for the VM"
        else:
            pins[dist] = v
            if releases is not None:
                releases[dist] = releases_between(d.get("releases", {}), v, have, python) if have != "local" else [v]
    return pins, skipped


def _key(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _fetch_version(dist: str, version: str, cache: Path | None) -> dict | None:
    """PyPI's metadata of one release ({"requires_dist": [...]})."""
    p = cache / f"{dist.lower()}-{version}.json" if cache else None
    if p and p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    try:
        raw = urllib.request.urlopen(urllib.request.Request(
            f"https://pypi.org/pypi/{dist}/{version}/json", headers={"User-Agent": "gapfinder"}), timeout=30).read()
    except Exception:  # noqa: BLE001
        return None
    d = {"requires_dist": (json.loads(raw).get("info") or {}).get("requires_dist") or []}
    if p:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(d), encoding="utf-8")
    return d


_LINUX = {"sys_platform": "linux", "platform_system": "Linux", "os_name": "posix", "platform_machine": "x86_64",
          "implementation_name": "cpython", "platform_python_implementation": "CPython"}


def dependency_pins(pins: dict[str, str], installed: dict[str, str], when: date, python: str,
                    cache: Path | None = None, depth: int = 3) -> tuple[dict[str, str], dict[str, str], dict[str, list[str]]]:
    """The dependencies the old releases need at other versions than the installed ones: (extra pins, why each,
    pinned dist -> the dependencies it brought in). For each old release's own requirements (PyPI's requires_dist for
    that version; extras and markers that don't hold on the VM's Linux and Python are skipped), an installed version
    outside the requirement, or a requirement that isn't installed, gets the newest release before the paper's date
    that satisfies it, and its requirements are checked in turn (`depth` levels). A date-bounded resolution of only
    the conflicting part: the compiled stack stays as installed unless an old release excludes it, and never more
    than the VM holds."""
    from packaging.requirements import Requirement
    from packaging.specifiers import SpecifierSet

    inst = {_key(k): v for k, v in installed.items()}
    pinned = {_key(d) for d in pins}
    extra: dict[str, str] = {}
    why: dict[str, str] = {}
    brought: dict[str, list[str]] = {}
    env = {**_LINUX, "python_version": ".".join(python.split(".")[:2]), "python_full_version": python, "extra": ""}
    todo = [(d, v, d, 0) for d, v in pins.items()]
    while todo:
        dist, ver, root, level = todo.pop(0)
        meta = _fetch_version(dist, ver, cache)
        for line in (meta or {}).get("requires_dist") or []:
            try:
                req = Requirement(line)
                if req.marker is not None and not req.marker.evaluate(env):
                    continue
            except Exception:  # noqa: BLE001 (an unparsable requirement: not ours to guess)
                continue
            key = _key(req.name)
            if key in pinned or key in {_key(x) for x in extra} or key in {_key(x) for x in SKIP}:
                continue
            have = inst.get(key)
            spec = req.specifier or SpecifierSet()
            if have is not None and (not str(spec) or spec.contains(have, prereleases=True)):
                continue
            d = _fetch(req.name, cache)
            v = version_at(d.get("releases", {}), when, python, spec) if d else None
            near = first_after(d.get("releases", {}), when, python, spec) if d and v is None else None
            v = near[0] if near else v
            if v is None:
                why[req.name] = f"needed by {dist}=={ver} as {req.name}{spec}; no release before {when} fits"
                continue
            mb = wheel_mb(d["releases"].get(v, []), python)
            if key not in TORCH_CPU and mb and mb > MAX_WHEEL_MB:
                why[req.name] = f"needed by {dist}=={ver} as {req.name}{spec}; {v} is {mb:.0f} MB, too large"
                continue
            extra[req.name] = v
            why[req.name] = (f"needed by {dist}=={ver} as {req.name}{spec or ''} (installed: {have or 'none'})"
                             + (f"; {near[1]}, the first release after the date that installs" if near else ""))
            brought.setdefault(root, []).append(req.name)
            if level + 1 < depth:
                todo.append((req.name, v, root, level + 1))
    return extra, why, brought


ROOT_DIR = "/opt/gf_py"  # one directory per old package, so any subset can be switched on
REL_DIR = "/tmp/gf_py"  # releases installed on demand by a run (the binary search)


def dirname(dist: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.]", "_", dist.lower())


# the installer: the environment's pip, or GF_PIP (a command such as `uv pip`, for a local backend without pip)
PIP_FN = ('gf_pip() { if [ -n "$GF_PIP" ]; then $GF_PIP "$@"; else "${PYTHON:-python}" -m pip "$@"; fi; }; ')


def _pip(dist: str, version: str, target: str) -> str:
    ix = f" --index-url {CPU_INDEX}" if dist.lower() in TORCH_CPU else ""
    return f'PIP_NO_CACHE_DIR=1 gf_pip install -q --no-deps{ix} --target "{target}" "{dist}=={version}"'


ROOT = f"${{GF_PY_ROOT:-{ROOT_DIR}}}"  # in the VM's shell


def install_command(pins: dict[str, str]) -> str:
    """One pip call per pin into its own directory (no dependencies); a pin that fails is reported, not fatal."""
    steps = [f"({_pip(d, v, f'{ROOT}/{dirname(d)}')} >/dev/null 2>&1 && echo GF_PIN_OK {d} {v} || "
             f'(rm -rf "{ROOT}/{dirname(d)}"; echo GF_PIN_FAIL {d} {v}))' for d, v in sorted(pins.items())]
    return f'{PIP_FN}mkdir -p "{ROOT}"; ' + "; ".join(steps)


def bundle(dist: str, brought: dict[str, list[str]]) -> list[str]:
    """A pinned package's directory and those of the dependencies it brought in (they go on together)."""
    return sorted({dirname(dist)} | {dirname(x) for x in brought.get(dist, [])})


def import_check(pins: dict[str, str], modules: list[str], brought: dict[str, list[str]] | None = None) -> str:
    """The code's imports under every old package together (GF_YEAR_IMPORT_all) and under each pinned package with
    the dependencies it brought (GF_YEAR_IMPORT_<dir>): 0 when they load. Run with the runtime shim on PYTHONPATH
    (the import redirect)."""
    brought = brought or {}
    deps = {x for v in brought.values() for x in v}
    direct = [d for d in sorted(pins) if d not in deps]
    mods = ", ".join(m for m in modules if m not in SKIP and "." not in m) or "sys"
    check = f'"${{PYTHON:-python}}" -c "import {mods}" >/dev/null 2>&1'
    alone = "; ".join(f'GF_LIB_DIRS="' + "|".join(f"{ROOT}/{x}" for x in bundle(d, brought)) + f'" {check}; '
                      f"echo GF_YEAR_IMPORT_{dirname(d)}=$?" for d in direct if len(direct) > 1)
    every = "|".join(f"{ROOT}/{dirname(d)}" for d in sorted(pins))
    return f'GF_LIB_DIRS="{every}" {check}; echo GF_YEAR_IMPORT_all=$?' + (f"; {alone}" if alone else "")


def parse_import_check(stdout: str) -> dict[str, bool]:
    return {k: v == "0" for k, v in re.findall(r"GF_YEAR_IMPORT_([A-Za-z0-9_.]+)=(\d+)", stdout or "")}


def run_prefix() -> str:
    """The knob's value: 0 (as installed), all (every old package), a comma list of directories, or `dist==version`
    (a release installed on demand into the run's VM: the binary search over releases, plan D1.4). The directories
    reach the runtime shim's import redirect through GF_LIB_DIRS (first listed wins); `1` is `all` (older specs)."""
    return (f'v="{{{KNOB}}}"; if [ "$v" != 0 ]; then {PIP_FN}[ "$v" = 1 ] && v=all; r="${{GF_PY_ROOT:-{ROOT_DIR}}}"; '
            f'[ "$v" = all ] && v="$(ls "$r" 2>/dev/null | tr "\\n" ",")"; GF_LIB_DIRS=""; '
            f'for p in $(echo "$v" | tr "," " "); do case "$p" in *==*) d="${{GF_PY_REL:-{REL_DIR}}}/$p"; '
            f'case "$p" in torch==*|torchvision==*|torchaudio==*) ix="--index-url {CPU_INDEX}";; *) ix="";; esac; '
            f'[ -d "$d" ] || PIP_NO_CACHE_DIR=1 gf_pip install -q --no-deps $ix --target "$d" "$p" '
            f'>/dev/null 2>&1 || echo "GF_LIB_INSTALL_FAIL $p" >&2;; *) d="$r/$p";; esac; '
            f'GF_LIB_DIRS="${{GF_LIB_DIRS:+$GF_LIB_DIRS|}}$d"; done; export GF_LIB_DIRS; fi; ')


def knob_choices(bundles: list[list[str]], all_ok: bool) -> list[str]:
    """0, every old package together (when they import together), and each pinned package with its dependencies (a
    single culprit is then found by the screen itself; an interaction by delta debugging in the library probe)."""
    out = ["0"] + (["all"] if all_ok else [])
    return out + ([",".join(b) for b in bundles] if len(bundles) > 1 or not all_ok else [])


# ------------------------------------------------------------------ the paper-era code (plan D7.2)

ERA_DIR = "/opt/gf_paper_era"
ERA_KNOB = "gf_paper_era_code"
ERA_REL = "/tmp/gf_era"  # commits fetched on demand by a run (the binary search over commits)
ERA_SCRIPT = "gf_harness/era_fetch.py"
CODE_EXT = (".py", ".yaml", ".yml", ".json", ".cfg", ".ini", ".toml", ".sh")


def _owner_repo(repo: str) -> str:
    return repo.rstrip("/").removeprefix("https://github.com/").removeprefix("http://github.com/").removesuffix(".git")


def _github(url: str, timeout: float = 30):
    import os

    headers = {"User-Agent": "gapfinder", "Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout).read())


def commit_before(repo: str, commit: str, when: date, timeout: float = 30) -> dict | None:
    """The last commit at or before `commit` dated before `when` ({"sha", "date", "message"}; GitHub's API, the
    history before the given commit only), or None when it is the given commit itself or can't be read."""
    url = (f"https://api.github.com/repos/{_owner_repo(repo)}/commits?sha={commit}&until={when.isoformat()}T00:00:00Z"
           "&per_page=1")
    try:
        data = _github(url, timeout)
    except Exception:  # noqa: BLE001 (rate limit, no network): no paper-era knob
        return None
    if not (isinstance(data, list) and data) or data[0]["sha"] == commit or commit.startswith(data[0]["sha"][:12]):
        return None
    return _brief(data[0])


def _brief(c: dict) -> dict:
    return {"sha": c["sha"], "date": c["commit"]["committer"]["date"][:10],
            "message": (c["commit"]["message"] or "").splitlines()[0][:120] if c["commit"].get("message") else ""}


def commits_between(repo: str, commit: str, since: str, pages: int = 5, timeout: float = 30) -> list[dict]:
    """The commits reachable from `commit` dated after `since` (ISO date), oldest first (at most 100 x pages)."""
    out = []
    for page in range(1, pages + 1):
        url = (f"https://api.github.com/repos/{_owner_repo(repo)}/commits?sha={commit}&since={since}T00:00:00Z"
               f"&per_page=100&page={page}")
        try:
            data = _github(url, timeout)
        except Exception:  # noqa: BLE001
            break
        if not isinstance(data, list) or not data:
            break
        out += [_brief(c) for c in data]
        if len(data) < 100:
            break
    out.reverse()
    return out


def commit_diff(repo: str, sha: str, max_lines: int = 60, timeout: float = 30) -> dict | None:
    """The files a commit changed and their patches (code files first, each patch cut to `max_lines`)."""
    try:
        data = _github(f"https://api.github.com/repos/{_owner_repo(repo)}/commits/{sha}", timeout)
    except Exception:  # noqa: BLE001
        return None
    files = []
    for f in data.get("files") or []:
        files.append({"file": f.get("filename"), "status": f.get("status"), "additions": f.get("additions"),
                      "deletions": f.get("deletions"), "code": str(f.get("filename", "")).endswith(CODE_EXT),
                      "patch": (f.get("patch") or "").splitlines()[:max_lines]})
    files.sort(key=lambda f: (not f["code"], -(f["additions"] or 0) - (f["deletions"] or 0)))
    return {"sha": sha, "message": (data.get("commit") or {}).get("message", "")[:500], "files": files}


def era_fetch_script(repo: str) -> str:
    """`python era_fetch.py SHA DEST`: the code files (under 1 MB) of the repo at SHA into DEST (Python 2.7 and 3)."""
    name = _owner_repo(repo)
    return ("import io, os, shutil, sys, tarfile\n"
            "try:\n    from urllib.request import urlopen\nexcept ImportError:\n    from urllib2 import urlopen\n"
            "sha, dest = sys.argv[1], sys.argv[2]\n"
            f"data = urlopen('https://codeload.github.com/{name}/tar.gz/' + sha, timeout=600).read()\n"
            "t = tarfile.open(fileobj=io.BytesIO(data))\n"
            f"exts = {CODE_EXT!r}\n"
            "ms = [m for m in t.getmembers() if m.isfile() and m.size < 2 ** 20 and m.name.endswith(exts)]\n"
            "tmp = dest + '.part'\n"
            "t.extractall(tmp, members=ms)\n"
            "top = [d for d in os.listdir(tmp)][0]\n"
            "if os.path.isdir(dest):\n    shutil.rmtree(dest)\n"
            "shutil.move(os.path.join(tmp, top), dest)\n"
            "shutil.rmtree(tmp, ignore_errors=True)\n"
            "print('GF_ERA_FILES %d' % len(ms))\n")


def era_fetch_command(sha: str) -> str:
    """Inside the VM, in the harness's last step: the paper-era commit into ERA_DIR."""
    return f'"${{PYTHON:-python}}" {ERA_SCRIPT} {sha} {ERA_DIR} || echo GF_ERA_FILES 0'


def era_prefix() -> str:
    """`gf_paper_era_code`: 0 (the given commit), 1 (the paper-era commit, fetched by the harness) or a commit sha
    (fetched on demand: the binary search over commits). The commit's code files go over the checkout (files added
    since stay)."""
    return (f'e="{{{ERA_KNOB}}}"; if [ "$e" = 1 ]; then cp -rf "${{GF_ERA_DIR:-{ERA_DIR}}}/." ./; '
            f'elif [ "$e" != 0 ]; then d="${{GF_ERA_REL:-{ERA_REL}}}/$e"; [ -d "$d" ] || "${{PYTHON:-python}}" '
            f'{ERA_SCRIPT} "$e" "$d" >/dev/null 2>&1 || echo "GF_ERA_FETCH_FAIL $e" >&2; cp -rf "$d/." ./; fi; ')


FREEZE = ('"${PYTHON:-python}" -c "import sys; print(\'GF_PY\', \'%d.%d.%d\' % sys.version_info[:3])"; '
          '"${PYTHON:-python}" -m pip freeze 2>/dev/null | sed "s/^/GF_FREEZE /"')


def parse_freeze(stdout: str) -> tuple[str | None, dict[str, str]]:
    py = re.search(r"GF_PY (\S+)", stdout or "")
    pkgs = dict(re.findall(r"(?m)^GF_FREEZE ([A-Za-z0-9_.-]+)==([^\s;]+)", stdout or ""))
    return (py.group(1) if py else None), pkgs
