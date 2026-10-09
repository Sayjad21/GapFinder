"""Sandbox backends: the one interface the checkpoint tree talks to.

`ContreeBackend` is the real thing (Token Factory Sandboxes). `LocalBackend` is
a stand-in that models the same semantics with directory snapshots, so the
orchestrator, search and tests can run before Beta access arrives and in CI.

Semantics both backends share (from the Sandboxes docs):
* every run starts from a checkpoint and, unless disposable, yields a new one
  holding the full filesystem afterwards;
* processes do not survive between runs -- state lives on disk only;
* commands run with the working directory WORK_DIR; paths in harness specs
  are relative to it.
"""

from __future__ import annotations

import abc
import asyncio
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import sys
import time
import uuid as uuidlib
from dataclasses import dataclass, field
from pathlib import Path

from gapfinder.ledger.schemas import ResourceStats
from gapfinder.models import budget

WORK_DIR = "/work"


class InfraError(RuntimeError):
    """Sandbox or API trouble -- the runner may retry these, never experiment failures."""


@dataclass
class RunResult:
    parent: str
    checkpoint: str | None  # None when disposable
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False
    truncated: bool = False
    resources: ResourceStats = field(default_factory=ResourceStats)


class SandboxBackend(abc.ABC):
    name: str

    @abc.abstractmethod
    async def base(self, ref: str) -> str:
        """Resolve/import a base image and return its checkpoint id."""

    @abc.abstractmethod
    async def run(
        self,
        parent: str,
        shell: str,
        *,
        env: dict[str, str] | None = None,
        timeout: float = 600,
        disposable: bool = False,
        files: dict[str, bytes] | None = None,
    ) -> RunResult:
        """Run `shell` in a fresh VM from `parent`; files are written (relative to WORK_DIR) first."""

    @abc.abstractmethod
    async def read_file(self, checkpoint: str, path: str) -> bytes:
        """Read a file from a checkpoint; relative paths are under WORK_DIR."""

    @abc.abstractmethod
    async def tag(self, checkpoint: str, tag: str) -> None: ...


# ======================================================================= local


class LocalBackend(SandboxBackend):
    """Directory-snapshot stand-in. A checkpoint is a directory: .gf_local/images/<id>/.

    `emulate_dedup=True` reproduces the documented Contree behaviour where the
    same command from the same image returns the cached result, so the
    RUN_TAG logic can be tested without network access.
    `content_ids=True` names each checkpoint after its content, as Sandboxes do: two runs that
    leave identical files get the same ID (the setup-reproducibility check relies on it).
    """

    content_addressed = False
    name = "local"

    def __init__(self, root: str | Path, *, emulate_dedup: bool = False, shell: str | None = None,
                 content_ids: bool = False):
        self.content_addressed = content_ids
        self.root = Path(root)
        self.images = self.root / "images"
        self.images.mkdir(parents=True, exist_ok=True)
        self.tags_file = self.root / "tags.json"
        self.emulate_dedup = emulate_dedup
        self._dedup: dict[str, RunResult] = {}
        self.shell = shell or _find_bash()

    def _dir(self, checkpoint: str) -> Path:
        tags = self._tags()
        checkpoint = tags.get(checkpoint, checkpoint)
        d = self.images / checkpoint
        if not d.is_dir():
            raise InfraError(f"unknown checkpoint {checkpoint}")
        return d

    def _tags(self) -> dict[str, str]:
        return json.loads(self.tags_file.read_text()) if self.tags_file.exists() else {}

    async def base(self, ref: str) -> str:
        """`ref` is a local directory to seed from, or 'empty'."""
        cid = str(uuidlib.uuid4())
        dest = self.images / cid
        if ref == "empty":
            dest.mkdir()
        else:
            src = Path(ref.removeprefix("local:"))
            if not src.is_dir():
                raise InfraError(f"base ref {ref} is not a directory")
            await asyncio.to_thread(shutil.copytree, src, dest, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        return cid

    async def run(self, parent, shell, *, env=None, timeout=600, disposable=False, files=None) -> RunResult:
        src = self._dir(parent)
        env = dict(env or {})
        if self.emulate_dedup:
            key = hashlib.sha256(json.dumps([parent, shell, sorted(env.items())]).encode()).hexdigest()
            if key in self._dedup and not files:
                return self._dedup[key]
        cid = str(uuidlib.uuid4())
        dest = self.images / cid
        await asyncio.to_thread(shutil.copytree, src, dest)
        for rel, data in (files or {}).items():
            p = dest / rel.removeprefix(WORK_DIR + "/").lstrip("/")
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        full_env = {**os.environ, **env, "WORK": str(dest), "PYTHON": Path(sys.executable).as_posix()}
        start = time.monotonic()
        timed_out = False

        def _go():
            # Output goes to files, not pipes: a grandchild that outlives a killed
            # shell would otherwise hold the pipe open and hang the read.
            with tempfile.TemporaryFile() as fo, tempfile.TemporaryFile() as fe:
                proc = subprocess.Popen(
                    [self.shell, "-c", shell], cwd=dest, env=full_env, stdout=fo, stderr=fe,
                    **_new_group_kwargs(),
                )
                try:
                    code, hit_timeout = proc.wait(timeout=timeout), False
                except subprocess.TimeoutExpired:
                    _kill_tree(proc)
                    code, hit_timeout = 124, True
                fo.seek(0), fe.seek(0)
                return code, fo.read(), fe.read(), hit_timeout

        code, out, err, timed_out = await asyncio.to_thread(_go)
        elapsed = time.monotonic() - start
        if disposable:
            await asyncio.to_thread(shutil.rmtree, dest, True)
        elif self.content_addressed:
            cid = await asyncio.to_thread(self._by_content, dest)
        result = RunResult(
            parent=parent,
            checkpoint=None if disposable else cid,
            exit_code=code,
            stdout=out.decode(errors="replace"),
            stderr=err.decode(errors="replace"),
            timed_out=timed_out,
            resources=ResourceStats(elapsed_s=round(elapsed, 4)),
        )
        if self.emulate_dedup:
            self._dedup[key] = result
        return result

    def _by_content(self, d: Path) -> str:
        h = hashlib.sha256()
        for p in sorted(d.rglob("*")):
            if p.is_file():
                h.update(p.relative_to(d).as_posix().encode() + b"\0" + p.read_bytes() + b"\0")
        cid = str(uuidlib.UUID(bytes=h.digest()[:16]))
        try:
            d.rename(self.images / cid)
        except OSError:  # that content exists already (perhaps from a concurrent run): keep one copy
            if not (self.images / cid).is_dir():
                raise
            shutil.rmtree(d, True)
        return cid

    async def read_file(self, checkpoint, path) -> bytes:
        p = self._dir(checkpoint) / path.removeprefix(WORK_DIR + "/").lstrip("/")
        if not p.is_file():
            raise FileNotFoundError(path)
        return p.read_bytes()

    async def tag(self, checkpoint, tag) -> None:
        tags = self._tags()
        tags[tag] = self._dir(checkpoint).name
        self.tags_file.write_text(json.dumps(tags, indent=1))


def _new_group_kwargs() -> dict:
    if os.name == "nt":
        return {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    return {"start_new_session": True}


def _kill_tree(proc: subprocess.Popen) -> None:
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
    else:
        import signal

        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()


def _find_bash() -> str:
    """A POSIX bash. On Windows avoid System32\\bash.exe, which is WSL."""
    if os.name != "nt":
        return shutil.which("bash") or "/bin/bash"
    for cand in (
        r"C:\Program Files\Git\usr\bin\bash.exe",
        r"C:\Program Files\Git\bin\bash.exe",
    ):
        if Path(cand).exists():
            return cand
    found = shutil.which("bash")
    if found and "system32" not in found.lower():
        return found
    raise RuntimeError("No POSIX bash found; install Git for Windows or set a shell explicitly")


# ===================================================================== contree


class ContreeBackend(SandboxBackend):
    """Token Factory Sandboxes via contree-sdk (auth: NEBIUS_API_KEY + NEBIUS_PROJECT_ID)."""

    content_addressed = True  # checkpoint IDs name the filesystem's content
    name = "contree"

    def __init__(self, client=None, *, truncate_output_at: int = 1024 * 1024):
        from contree_sdk import Contree

        self.sdk = client or Contree()
        self.truncate_output_at = truncate_output_at

    async def base(self, ref: str) -> str:
        from contree_sdk.sdk.exceptions import ContreeError

        try:
            files = None
            if ref.startswith("local:"):
                # a local artifact folder: upload it into /work of a Python image, so the same
                # harness spec runs on the local backend and in Sandboxes
                files = _folder_files(Path(ref[6:]))
                ref = os.environ.get("GF_CONTREE_LOCAL_IMAGE", "python:3.12-slim")
            if _looks_like_uuid(ref):
                img = await self.sdk.images.use(ref)
            else:
                img = await self.sdk.images.oci(ref)
            # make sure the work dir exists in every descendant
            upload = {f"{WORK_DIR}/{k}": v for k, v in (files or {}).items()} or None
            img = await img.run(shell=f"mkdir -p {WORK_DIR}", disposable=False, files=upload)
            if img.result.cost:
                budget.record("sandbox", img.result.cost, note="base image setup")
            return str(img.uuid)
        except ContreeError as exc:
            raise InfraError(str(exc)) from exc

    async def run(self, parent, shell, *, env=None, timeout=600, disposable=False, files=None) -> RunResult:
        """Every sandbox run, from any caller, is checked against the spend cap and recorded."""
        budget.check(0.0, "sandbox run", kind="sandbox")  # cost isn't known up front: refuse at the guard
        # The cap can't stop a run already executing, and billing is per CPU-second, so every
        # process in the run gets a CPU-time limit: a runaway gets killed instead of draining credits.
        cpu_limit = int(os.environ.get("GF_SANDBOX_CPU_LIMIT_S", "300"))
        shell = f"ulimit -t {cpu_limit}; {shell}"
        res = await self._run(parent, shell, env=env, timeout=timeout, disposable=disposable, files=files)
        if res.resources.cost_usd:
            budget.record("sandbox", res.resources.cost_usd, elapsed_s=res.resources.elapsed_s,
                          cpu_s=res.resources.user_cpu_s + res.resources.system_cpu_s)
        return res

    async def _run(self, parent, shell, *, env=None, timeout=600, disposable=False, files=None) -> RunResult:
        from contree_sdk.sdk.exceptions import (
            ApiTimeoutError,
            ContreeApiError,
            ContreeTransportError,
            FailedOperationError,
            OperationTimedOutError,
        )
        from contree_sdk.sdk.exceptions.api import TooManyRequestsError  # not re-exported by the package

        img = await self.sdk.images.use(parent)
        upload = {f"{WORK_DIR}/{k.removeprefix(WORK_DIR + '/').lstrip('/')}": v for k, v in (files or {}).items()}
        try:
            done = await img.run(
                shell=shell,
                env=env or {},
                cwd=WORK_DIR,
                timeout=timeout,
                disposable=disposable,
                files=upload or None,
                truncate_output_at=self.truncate_output_at,
            )
        except OperationTimedOutError:
            return RunResult(parent=parent, checkpoint=None, exit_code=124, stdout="", stderr="", timed_out=True)
        except (TooManyRequestsError, ApiTimeoutError, ContreeTransportError) as exc:
            raise InfraError(f"{type(exc).__name__}: {exc}") from exc
        except ContreeApiError as exc:
            raise InfraError(str(exc)) from exc
        res = done.result
        raw = res._raw.result if res._raw is not None else None
        stats = ResourceStats(elapsed_s=res.elapsed_time.total_seconds(), cost_usd=res.cost)
        timed_out = False
        if raw is not None:
            r = raw.resources
            stats = ResourceStats(
                elapsed_s=r.elapsed_time,
                user_cpu_s=r.user_cpu_time,
                system_cpu_s=r.system_cpu_time,
                max_rss_kb=r.max_rss,
                block_in=r.block_input,
                block_out=r.block_output,
                involuntary_switches=r.involuntary_switches,
                cost_usd=r.cost,
            )
            timed_out = raw.state.timed_out
        return RunResult(
            parent=parent,
            checkpoint=None if disposable or done.uuid is None else str(done.uuid),
            exit_code=res.exit_code,
            stdout=res.stdout if isinstance(res.stdout, str) else (res.stdout or b"").decode(errors="replace"),
            stderr=res.stderr if isinstance(res.stderr, str) else (res.stderr or b"").decode(errors="replace"),
            timed_out=timed_out,
            truncated=res.truncated,
            resources=stats,
        )

    async def read_file(self, checkpoint, path) -> bytes:
        img = await self.sdk.images.use(checkpoint)
        full = path if path.startswith("/") else f"{WORK_DIR}/{path}"
        return await img.read(full)

    async def tag(self, checkpoint, tag) -> None:
        img = await self.sdk.images.use(checkpoint)
        await img.tag_as(tag)


def _folder_files(root: Path, max_bytes: int = 50_000_000) -> dict[str, bytes]:
    """All files under `root` (relative posix paths), skipping VCS/cache dirs; CRLF -> LF for scripts."""
    if not root.is_dir():
        raise InfraError(f"local artifact folder {root} does not exist")
    out, total = {}, 0
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).as_posix()
        if p.is_dir() or any(part in {".git", "__pycache__", ".venv", "node_modules", "out"} for part in rel.split("/")):
            continue
        data = p.read_bytes()
        if p.suffix in {".sh", ".py", ".yaml", ".yml"}:
            data = data.replace(b"\r\n", b"\n")
        total += len(data)
        if total > max_bytes:
            raise InfraError(f"{root} is over {max_bytes} bytes; build an image instead of uploading")
        out[rel] = data
    return out


def _looks_like_uuid(s: str) -> bool:
    try:
        uuidlib.UUID(s)
        return True
    except ValueError:
        return False


def make_backend(kind: str | None = None, **kw) -> SandboxBackend:
    from gapfinder.config import settings

    s = settings()
    kind = kind or s.sandbox_backend
    if kind == "local":
        return LocalBackend(kw.pop("root", s.local_sandbox_dir), **kw)
    if kind == "contree":
        return ContreeBackend(**kw)
    raise ValueError(f"unknown sandbox backend {kind!r}")
