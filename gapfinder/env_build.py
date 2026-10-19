"""Build a runnable environment for a repo in Sandboxes, one command at a time (Repo2Run-style).

    gapfinder env-build <github url> --commit <sha> --local <checkout> --out env.json

The harness's hardest part on real papers was the image: an old Python, pinned libraries, a package that no
longer installs (devbatch-1: every case needed hand-picked pins). Repo2Run (2025) builds such environments with
an agent that runs one command at a time in a container and rolls back on failure. Sandboxes make the rollback
free: every successful command leaves a checkpoint, and a failed one is simply not built on.

Loop:
  1. pick a base image (the model, from a fixed list, given the commit date and the build files);
  2. fetch the repo at the commit into /work (no upload, no file of the repo changed);
  3. check: import every third-party module the entry scripts import (plain code finds them, no model);
  4. if a module is missing, ask the model for ONE next shell command, given the history and the check's
     output; run it from the last good checkpoint; keep the new checkpoint only if it exits 0;
  5. stop when the check passes or after `max_steps` commands.

The result is the checkpoint (the spec's `base`) and the recipe: the commands that succeeded, in order, which a
person can read like a Dockerfile. Nothing here decides what a paper means; it only makes the code importable.
"""

from __future__ import annotations

import ast
import json
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from pydantic import BaseModel

IMAGES = ("python:2.7-slim", "python:3.6-slim", "python:3.7-slim", "python:3.8-slim", "python:3.9-slim",
          "python:3.10-slim", "python:3.11-slim", "python:3.12-slim")
MAX_TAIL = 2500
STEP_TIMEOUT_S = 1800

IMAGE_PROMPT = """Pick the base image for running a research repository, from this list only:
{images}

The repository's commit date is {date}. Prefer the Python version that was current then, unless the build
files require another (a pinned library that only exists for an older or newer Python decides it).

BUILD FILES:
{build}

README (install part):
{readme}
"""

STEP_PROMPT = """You are making a research repository runnable inside a fresh Linux VM ({image}, no GPU, 4 CPUs,
3.9 GB memory). The repository is checked out at /work, at a commit dated {date}. Commands run with `bash -c`
in /work; the network is available for package installs.

Goal: every module below imports. The check runs `python -c "import <module>"` for each, from the directories
the entry scripts run in.{goal}
Third-party modules the entry scripts import: {modules}

BUILD FILES:
{build}

README (install part):
{readme}

What has been run so far (successful commands are kept; a failed one was rolled back):
{history}

The last check said:
{check}

Give ONE next shell command (it may chain a few steps with &&). Pin versions that existed at the commit date
when the build files don't (e.g. tensorflow==1.15.5 for a 2018 TensorFlow 1 repo); prefer pip wheels over
compiling; use `pip install --no-cache-dir`. You are root: system packages and tools come from
`apt-get update && apt-get install -y --no-install-recommends <packages>` (a missing command such as `free`,
`wget` or `unzip`, or a library a wheel needs). Do not edit the repository's source files. If the goal can't be
reached in this VM (e.g. it needs a GPU-only package), set "give_up" with the reason. If the base image itself is
the problem (its Python version can't install what the code needs), set "switch_image" to another image from
this list instead: {images}. The VM then restarts from a fresh checkout on that image; this history is kept."""


class ImageChoice(BaseModel):
    image: str
    why: str = ""


class NextStep(BaseModel):
    command: str = ""
    why: str = ""
    give_up: str = ""
    switch_image: str = ""


@dataclass
class StepRecord:
    command: str
    exit_code: int
    ok: bool
    tail: str
    elapsed_s: float
    why: str = ""
    image: str = ""


@dataclass
class EnvResult:
    ok: bool
    image: str
    checkpoint: str | None
    modules: list[str]
    steps: list[StepRecord] = field(default_factory=list)
    reason: str = ""
    cost_usd: float = 0.0

    @property
    def recipe(self) -> list[str]:
        # the commands that worked on the final image (an image switch is recorded as a "# switch" step)
        return [s.command for s in self.steps if s.ok and s.image in ("", self.image) and not s.command.startswith("#")]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["recipe"] = self.recipe
        return d


# ------------------------------------------------------------------ plain-code inputs

_STDLIB = set(getattr(sys, "stdlib_module_names", ())) | {
    "__future__", "distutils", "imp", "asynchat", "asyncore", "smtpd"}


def local_modules(root: Path) -> set[str]:
    """Names the repo itself provides: top-level packages and modules, anywhere a script might run from."""
    out = set()
    for p in root.rglob("*.py"):
        if any(part.startswith(".") for part in p.relative_to(root).parts):
            continue
        out.add(p.stem)
        for parent in p.relative_to(root).parents:
            if parent.name:
                out.add(parent.name)
    return out


def entry_scripts(root: Path, limit: int = 8) -> list[Path]:
    """Files that look like entry points: a __main__ block or argument parsing, shallowest first."""
    hits = []
    for p in sorted(root.rglob("*.py"), key=lambda p: (len(p.relative_to(root).parts), str(p))):
        if any(part.startswith(".") or part in ("tests", "test", "docs") for part in p.relative_to(root).parts):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "__main__" in text or "argparse" in text or "tf.app.flags" in text or "absl" in text:
            hits.append(p)
        if len(hits) >= limit:
            break
    return hits


def third_party_imports(root: Path, scripts: list[Path] | None = None) -> list[str]:
    """Top-level modules the entry scripts (and the repo modules they import) need from outside the repo."""
    root = Path(root)
    local = local_modules(root)
    seen_files: set[Path] = set()
    todo = list(scripts if scripts is not None else entry_scripts(root))
    mods: set[str] = set()
    by_stem = {p.stem: p for p in root.rglob("*.py")}
    while todo:
        p = todo.pop()
        if p in seen_files:
            continue
        seen_files.add(p)
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except (OSError, SyntaxError, ValueError):
            continue
        for n in ast.walk(tree):
            names = []
            if isinstance(n, ast.Import):
                names = [a.name for a in n.names]
            elif isinstance(n, ast.ImportFrom) and n.module and not n.level:
                names = [n.module]
            for name in names:
                top = name.split(".")[0]
                if top in local:
                    leaf = name.split(".")[-1]
                    if leaf in by_stem:
                        todo.append(by_stem[leaf])
                    elif top in by_stem:
                        todo.append(by_stem[top])
                elif top not in _STDLIB:
                    mods.add(top)
    return sorted(mods)


def readme_install(root: Path, limit: int = 2500) -> str:
    for name in ("README.md", "README.rst", "README.txt", "README"):
        p = Path(root) / name
        if p.is_file():
            text = p.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"(?im)^#*\s*.*(install|requirement|dependenc|setup|environment).*$", text)
            return text[m.start(): m.start() + limit] if m else text[:limit]
    return ""


_README_CMD = re.compile(
    r"(?m)^[ \t>$]*((?:cd [\w./-]+ *(?:&&|;) *)?"
    r"(?:python[23]?(?:\.\d+)?(?: +-[A-Za-z]+)* +(?!setup\.py\b)[\w./-]+\.py\b|(?:bash|sh) +[\w./-]+\.sh\b)[^\n`]*)")


def readme_command(root: Path) -> str | None:
    """The first experiment command in the README: `python [-u] <script>.py ...` (not setup.py) or
    `bash <script>.sh ...`, an optional `cd dir &&` kept; None when there is none."""
    for name in ("README.md", "README.rst", "README.txt", "README"):
        p = Path(root) / name
        if p.is_file():
            text = p.read_text(encoding="utf-8", errors="replace")
            m = _README_CMD.search(text)
            if m:
                cmd = _plain_command(m.group(1))
                # `$ cd src` on the line just before (RippleNet's README): the command runs from there
                before = text[: m.start()].rstrip("\n").rsplit("\n", 1)[-1]
                cd = re.match(r"^[ \t>$]*cd ([\w./-]+)\s*$", before)
                if cd and not cmd.startswith("cd "):
                    cmd = f"cd {cd.group(1)} && {cmd}"
                return cmd
    return None


def _plain_command(cmd: str) -> str:
    """Drop prose after the command: `python main.py --dataset movie (or --dataset book)`, `... # note`."""
    cmd = re.split(r"\s+\((?:or|e\.g\.|note|optional|see)\b|\s+#\s", cmd, maxsplit=1)[0]
    return cmd.strip().rstrip(";")


def short_run_goal(command: str, seconds: int = 300) -> str:
    """Run `command` for up to `seconds`: it passes if it exits 0 or is still running at the deadline (an import
    can succeed and the code still fail at its first step: devbatch-2's NCF was Python 2 code on Python 3.7,
    and Anomaly Transformer called `.cuda()` with no GPU; both images "loaded every import")."""
    return f"cd /work && timeout {seconds} bash -c {_shq(command)}; rc=$?; [ $rc -eq 0 ] || [ $rc -eq 124 ]"


def _shq(s: str) -> str:
    return "'" + s.replace("'", "'\"'\"'") + "'"


def build_text(root: Path, limit: int = 2500) -> str:
    out = []
    for pat in ("requirements*.txt", "setup.py", "pyproject.toml", "environment*.yml", "setup.cfg", "Pipfile"):
        for p in sorted(Path(root).rglob(pat))[:3]:
            if any(part.startswith(".") for part in p.relative_to(root).parts):
                continue
            out.append(f"=== {p.relative_to(root).as_posix()} ===\n"
                       + p.read_text(encoding="utf-8", errors="replace")[:limit])
    return "\n".join(out) or "(none)"


def fetch(repo: str, commit: str) -> str:
    """A shell command that downloads the repo at `commit` from GitHub into /work (inside the VM)."""
    owner_repo = repo.rstrip("/").removeprefix("https://github.com/").removesuffix(".git")
    name = owner_repo.split("/")[-1]
    # Python 2 and 3 alike (a 2016 repo runs on python:2.7-slim, which has no python3 and no curl)
    return ("python -c \"import io, tarfile\n"
            "try:\n    from urllib.request import urlopen\nexcept ImportError:\n    from urllib2 import urlopen\n"
            f"d = urlopen('https://codeload.github.com/{owner_repo}/tar.gz/{commit}', timeout=300).read()\n"
            "tarfile.open(fileobj=io.BytesIO(d)).extractall('/tmp/src'); print('fetched %d' % len(d))\" "
            f"&& cp -r /tmp/src/{name}-{commit}/. /work/ && rm -rf /tmp/src && ls /work")


def commit_date(root: Path) -> str:
    """The checkout's commit date, when it is a git clone ('unknown' otherwise)."""
    import subprocess

    try:
        out = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%cs"], capture_output=True, text=True,
                             timeout=20)
        return out.stdout.strip() or "unknown"
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def check_command(modules: list[str], dirs: list[str]) -> str:
    """Import each module from each script directory; print the ones that fail, exit 1 if any do."""
    code = ("import importlib, os, sys, traceback\n"
            f"mods = {modules!r}\n"
            f"dirs = {dirs!r}\n"
            "bad = {}\n"
            "for m in mods:\n"
            "    err = None\n"
            "    for d in dirs:\n"
            "        sys.path.insert(0, os.path.join('/work' if os.path.isdir('/work') else os.getcwd(), d))\n"
            "        try:\n"
            "            importlib.import_module(m); err = None; break\n"
            "        except BaseException as e:\n"
            "            err = (type(e).__name__ + ': ' + str(e))[:300]\n"
            "        finally:\n"
            "            sys.path.pop(0)\n"
            "    if err: bad[m] = err\n"
            "print('GF_IMPORT_CHECK', 'ok' if not bad else 'missing')\n"
            "for m, e in bad.items(): print('  ', m, '->', e)\n"
            "sys.exit(1 if bad else 0)\n")
    return "python - <<'GF_EOF'\n" + code + "GF_EOF"


# ------------------------------------------------------------------------ the loop


def _tail(s: str, n: int = MAX_TAIL) -> str:
    s = s or ""
    return s if len(s) <= n else "..." + s[-n:]


def _history(steps: list[StepRecord]) -> str:
    if not steps:
        return "(nothing yet)"
    return "\n".join(f"{'OK  ' if s.ok else 'FAIL'} $ {s.command}" + ("" if s.ok else f"\n     {_tail(s.tail, 600)}")
                     for s in steps[-12:])


MAX_IMAGE_SWITCHES = 2
INFRA_RETRIES = 3


async def _run(backend, *args, **kw):
    """backend.run with retries on sandbox or network trouble (env bench: DNS and connect timeouts)."""
    import asyncio

    from gapfinder.sandbox.backend import InfraError

    for i in range(INFRA_RETRIES):
        try:
            return await backend.run(*args, **kw)
        except InfraError:
            if i == INFRA_RETRIES - 1:
                raise
            await asyncio.sleep(20 * (i + 1))


async def _start(backend, root: Path, image: str, fetch: str | None) -> tuple[str | None, str]:
    """A fresh checkpoint with the repo at /work on `image`: (checkpoint, error)."""
    import asyncio
    import os
    import tempfile

    from gapfinder.sandbox.backend import InfraError

    if fetch is None:
        return await backend.base("local:" + str(root)), ""
    for i in range(INFRA_RETRIES):
        try:
            os.environ["GF_CONTREE_LOCAL_IMAGE"] = image
            ckpt = await backend.base("local:" + tempfile.mkdtemp(prefix="gf-env-"))
            break
        except InfraError:
            if i == INFRA_RETRIES - 1:
                raise
            await asyncio.sleep(20 * (i + 1))
    r = await _run(backend, ckpt, fetch, timeout=STEP_TIMEOUT_S, disposable=False)
    if r.exit_code != 0 or not r.checkpoint:
        return None, f"fetch failed: {_tail((r.stdout or '') + (r.stderr or ''), 600)}"
    return r.checkpoint, ""


async def build_env(router, backend, root: str | Path, *, fetch: str | None = None, image: str | None = None,
                    date: str | None = None, max_steps: int = 12, goal: str | None = None,
                    goal_timeout: float = 1800) -> EnvResult:
    """`root`: a local checkout (read for imports and build files). `fetch`: a shell command that puts the repo
    at /work in the VM (None: the backend's base is the checkout itself, as on the local backend). `goal`: a
    command that must also exit 0 once the imports load (e.g. a short run of the experiment), so system tools
    and data steps it needs are installed in the same rollback loop.

    The model may ask for another base image when the first can't work (VGAE and GAT in the first env bench:
    TensorFlow 1 has no wheels for the Python it picked, and the loop could only give up). The VM restarts from a
    fresh checkout on that image, at most MAX_IMAGE_SWITCHES times; the history goes along."""
    root = Path(root)
    date = date or commit_date(root)
    scripts = entry_scripts(root)
    modules = third_party_imports(root, scripts)
    dirs = sorted({p.parent.relative_to(root).as_posix() for p in scripts} | {"."})
    build, readme = build_text(root), readme_install(root)
    before = router.meter.total_cost() if router is not None else 0.0
    if image is None:
        choice = await router.structured("super", [{"role": "user", "content": IMAGE_PROMPT.format(
            images="\n".join(IMAGES), date=date, build=build, readme=readme)}], ImageChoice)
        image = choice.image if choice.image in IMAGES else "python:3.10-slim"
    ckpt, err = await _start(backend, root, image, fetch)
    if ckpt is None:
        return EnvResult(False, image, None, modules, reason=err)
    res = EnvResult(False, image, ckpt, modules)
    tried = [image]
    check = check_command(modules, dirs)
    for _ in range(max_steps + MAX_IMAGE_SWITCHES + 1):
        c = await _run(backend, ckpt, check, timeout=600, disposable=True)
        out = _tail((c.stdout or "") + (c.stderr or ""))
        if c.exit_code == 0 and goal:
            # imports load; the run's own command must work too (PatchTST's smoke needed `free`, a system tool)
            g = await _run(backend, ckpt, goal, timeout=goal_timeout, disposable=True)
            if g.exit_code != 0:
                c = g
                out = "the imports load, but the goal command failed (exit %d):\n%s" % (
                    g.exit_code, _tail((g.stdout or "") + (g.stderr or "")))
        if c.exit_code == 0:
            res.ok, res.checkpoint = True, ckpt
            break
        if sum(s.image == image for s in res.steps) >= max_steps:
            res.reason = f"{max_steps} commands on {image} and the check still fails: {out[-400:]}"
            break
        step = await router.structured("super", [{"role": "user", "content": STEP_PROMPT.format(
            image=image, date=date, modules=", ".join(modules) or "(none)", build=build, readme=readme,
            goal=(f"\nThen this command must also exit 0 (it uses the programs and files the run needs):\n  {goal}"
                  if goal else ""),
            history=_history(res.steps), check=out, images=", ".join(i for i in IMAGES if i not in tried))}], NextStep)
        new = step.switch_image.strip()
        if new and new in IMAGES and new not in tried and len(tried) <= MAX_IMAGE_SWITCHES:
            fresh, err = await _start(backend, root, new, fetch)
            res.steps.append(StepRecord(f"# switch base image {image} -> {new}", 0, fresh is not None, err, 0.0,
                                        step.why or step.give_up, image=new))
            tried.append(new)
            if fresh is None:
                res.reason = err
                break
            image, ckpt = new, fresh
            res.image, res.checkpoint = image, ckpt
            continue
        if step.give_up or not step.command.strip():
            res.reason = f"the model gave up: {step.give_up or 'no command'}"
            break
        t = time.monotonic()
        r = await _run(backend, ckpt, step.command, timeout=STEP_TIMEOUT_S, disposable=False)
        ok = r.exit_code == 0 and bool(r.checkpoint)
        res.steps.append(StepRecord(step.command, r.exit_code, ok, _tail((r.stdout or "") + (r.stderr or ""), 1500),
                                    round(time.monotonic() - t, 1), step.why, image=image))
        if ok:
            ckpt = r.checkpoint
    res.cost_usd = (router.meter.total_cost() - before) if router is not None else 0.0
    return res


def write_result(res: EnvResult, out: str | Path) -> Path:
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res.to_dict(), indent=1), encoding="utf-8")
    return out
