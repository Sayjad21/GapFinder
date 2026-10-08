"""Orchestrator: depth planner + async runner over the checkpoint tree.

* Each branch forks from the deepest checkpoint still valid for it: build
  knobs start from source (branches needing the same build flags share one
  build), dataset knobs from the built image, everything else from loaded.
* A semaphore caps concurrency (Beta allows 50 operations; we use 40).
* Every run gets a unique RUN_TAG env var, so identical commands re-execute
  instead of returning a cached snapshot (spike S2).
* Retries happen only on InfraError, never on experiment failures.
* `no_fork=True` is the ablation: every branch rebuilds and reloads.
"""

from __future__ import annotations

import asyncio
import itertools
import uuid as uuidlib

from gapfinder.ledger.schemas import Branch, BranchStatus, Layer
from gapfinder.models import budget
from gapfinder.sandbox.backend import InfraError, RunResult, SandboxBackend
from gapfinder.sandbox.cost import CostMeter
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.noise import NoiseBand, noise_band, starved
from gapfinder.sandbox.parse import UngroundedValueError, ground_values, parse_metrics
from gapfinder.sandbox.spec import HarnessSpec, diff_guard
from gapfinder.sandbox.tree import CheckpointTree, Node

BUILD_LAYERS = {Layer.build.value}
DATASET_LAYERS = {Layer.build.value, Layer.dataset.value}


class Orchestrator:
    def __init__(
        self,
        backend: SandboxBackend,
        spec: HarnessSpec,
        events: EventLog,
        *,
        cost: CostMeter | None = None,
        concurrency: int = 40,
        no_fork: bool = False,
        infra_retries: int = 3,
        tag_prefix: str | None = None,
    ):
        self.backend = backend
        self.spec = spec
        self.events = events
        self.cost = cost or CostMeter()
        self.tree = CheckpointTree()
        self.sem = asyncio.Semaphore(concurrency)
        self.no_fork = no_fork
        self.infra_retries = infra_retries
        self.tag_prefix = tag_prefix or f"gf/{spec.name}"
        self._stage_locks: dict[tuple, asyncio.Lock] = {}
        self._ids = itertools.count(1)
        self.running = 0
        self.max_running_seen = 0

    # ------------------------------------------------------------- stages
    async def _exec(self, parent: str, shell: str, env: dict, timeout: float, disposable: bool = False,
                    files: dict[str, bytes] | None = None) -> RunResult:
        last: Exception | None = None
        for attempt in range(self.infra_retries + 1):
            budget.check(0.0, "sandbox run", kind="sandbox")  # cost unknown up front: stop at the guard
            try:
                async with self.sem:
                    self.running += 1
                    self.max_running_seen = max(self.max_running_seen, self.running)
                    try:
                        return await self.backend.run(parent, shell, env=env, timeout=timeout,
                                                      disposable=disposable, files=files)
                    finally:
                        self.running -= 1
            except InfraError as exc:
                last = exc
                self.events.emit("note", level="warn", msg=f"infra error (attempt {attempt + 1}): {exc}")
                await asyncio.sleep(min(2**attempt, 15) * 0.1)
        raise last  # type: ignore[misc]

    async def source(self) -> str:
        key = ("source", ())
        async with self._lock(key):
            if (cid := self.tree.find_stage("source")) is None:
                cid = await self.backend.base(self.spec.base)
                self._add(Node(cid, None, "source"), tag="source")
            return cid

    async def stage(self, stage: str, changes: dict[str, str]) -> str:
        """Checkpoint for `stage` (source|built|loaded) under the build/dataset part of `changes`."""
        if stage == "source":
            return await self.source()
        layers = BUILD_LAYERS if stage == "built" else DATASET_LAYERS
        relevant = self.spec.changes_for_layers(changes, layers)
        key = (stage, tuple(sorted(relevant.items())))
        async with self._lock(key):
            if not self.no_fork and (cid := self.tree.find_stage(stage, relevant)):
                return cid
            prev = "source" if stage == "built" else "built"
            parent = await self.stage(prev, changes)  # in no_fork mode this rebuilds too
            spec_stage = self.spec.build if stage == "built" else self.spec.load
            if spec_stage is None:  # stage not used by this artifact: alias the parent
                return parent
            cmd, env = self.spec.render(spec_stage, relevant)
            res = await self._exec(parent, cmd, {**env, "RUN_TAG": _tag()}, spec_stage.timeout)
            self.cost.add_run(res.resources.cost_usd, setup=True)
            if res.exit_code != 0 or res.checkpoint is None:
                raise RuntimeError(f"{stage} failed (exit {res.exit_code}): {res.stderr[-2000:]}")
            new_changes = {k: v for k, v in relevant.items() if self.spec.knobs[k].layer in (
                {Layer.build.value} if stage == "built" else {Layer.dataset.value})}
            node = Node(res.checkpoint, parent, stage, new_changes, command=cmd,
                        cost_usd=res.resources.cost_usd, elapsed_s=res.resources.elapsed_s)
            self._add(node, tag=None if relevant or self.no_fork else stage)
            return res.checkpoint

    # ------------------------------------------------------------ branches
    async def run_branch(self, changes: dict[str, str], *, label: str | None = None,
                         files: dict[str, bytes] | None = None) -> Branch:
        """Run one branch. `files` (e.g. a config fix proposed by a model) pass the diff guard first:
        anything outside the spec's allowed_paths is algorithm code and the branch is rejected unrun."""
        bid = f"B{next(self._ids):04d}"
        self.spec.values(changes)  # validates knob names
        run_tag = _tag()
        if files and (bad := diff_guard(list(files), self.spec.allowed_paths)):
            branch = Branch(id=bid, parent_checkpoint="-", knob_changes=changes, command="-", run_tag=run_tag,
                            status=BranchStatus.rejected, note=f"diff guard: edits outside allowed paths: {bad}")
            self.events.emit("branch_finished", branch=branch.model_dump())
            return branch
        # build/dataset changes are handled by stage(): it keys checkpoints on them
        parent = await self.stage("loaded", changes)
        cmd, env = self.spec.render(self.spec.run, changes)
        branch = Branch(id=bid, parent_checkpoint=parent, knob_changes=changes, command=cmd, run_tag=run_tag,
                        status=BranchStatus.running, note=label)
        self.events.emit("branch_created", branch=branch.model_dump())
        self.events.emit("branch_started", id=bid)
        try:
            res = await self._exec(parent, cmd, {**env, "RUN_TAG": run_tag}, self.spec.run.timeout, files=files)
        except InfraError as exc:
            branch.status, branch.note = BranchStatus.infra_error, _note(label, str(exc))
            self.events.emit("branch_finished", branch=branch.model_dump())
            return branch
        self.cost.add_run(res.resources.cost_usd)
        branch.exit_code, branch.resources, branch.result_checkpoint = res.exit_code, res.resources, res.checkpoint
        if res.timed_out:
            branch.status = BranchStatus.timed_out
        elif res.exit_code != 0:
            branch.status, branch.note = BranchStatus.failed, _note(label, (res.stderr or res.stdout)[-1500:])
        else:
            raw = res.stdout
            if self.spec.run.output != "stdout" and res.checkpoint:
                try:
                    raw = (await self.backend.read_file(res.checkpoint, self.spec.run.output)).decode(errors="replace")
                except FileNotFoundError:
                    raw = ""
            try:
                metrics = ground_values(parse_metrics(raw, self.spec.run.format), raw)
            except UngroundedValueError as exc:
                metrics, branch.note = {}, _note(label, str(exc))
            if self.spec.metrics:
                metrics = {k: v for k, v in metrics.items() if k in self.spec.metrics}
            if not metrics:
                branch.status = BranchStatus.failed
                if branch.note == label:
                    branch.note = _note(label, f"no metrics parsed from output: {raw[-500:]!r}")
            else:
                branch.parsed_metrics, branch.status = metrics, BranchStatus.succeeded
        if res.checkpoint:
            self._add(Node(res.checkpoint, parent, "branch", changes, command=cmd,
                           cost_usd=res.resources.cost_usd, elapsed_s=res.resources.elapsed_s))
        self.events.emit("branch_finished", branch=branch.model_dump())
        self.events.emit("cost", **self.cost.summary())
        return branch

    async def fanout(self, change_sets: list[dict[str, str]], labels: list[str] | None = None) -> list[Branch]:
        labels = labels or [None] * len(change_sets)
        return list(await asyncio.gather(*(self.run_branch(c, label=l) for c, l in zip(change_sets, labels))))

    async def calibrate_noise(self, n: int = 5, changes: dict[str, str] | None = None,
                              floor_frac: float = 0.0) -> tuple[dict[str, NoiseBand], list[Branch]]:
        """n identical forks of `changes` (default: the naive config). Starved runs are re-run once."""
        changes = changes or {}
        branches = await self.fanout([changes] * n, [f"noise-{i}" for i in range(n)])
        flags = starved([b.resources.involuntary_switches for b in branches])
        for i, flag in enumerate(flags):
            if flag:
                self.events.emit("note", level="warn", msg=f"{branches[i].id} CPU-starved; re-running")
                branches[i] = await self.run_branch(changes, label=f"noise-{i}-rerun")
        ok = [b for b in branches if b.status == BranchStatus.succeeded]
        bands: dict[str, NoiseBand] = {}
        if len(ok) >= 3:
            for metric in ok[0].parsed_metrics:
                vals = [b.parsed_metrics[metric] for b in ok if metric in b.parsed_metrics]
                if len(vals) >= 3:
                    bands[metric] = noise_band(metric, vals, floor_frac=floor_frac)
                    self.events.emit("noise_band", **bands[metric].to_dict())
        return bands, branches

    def adopt(self, stage: str, checkpoint: str, parent: str | None = None) -> None:
        """Register an existing default-config checkpoint (e.g. from spike S3) so this process
        forks from it instead of rebuilding. Only for the no-changes chain: source/built/loaded."""
        if stage not in ("source", "built", "loaded"):
            raise ValueError(f"can only adopt source/built/loaded, not {stage}")
        self._add(Node(checkpoint, parent, stage), tag=None)

    async def tag_key_nodes(self) -> None:
        for node in self.tree.nodes.values():
            if node.tag:
                await self.backend.tag(node.id, node.tag)

    # -------------------------------------------------------------- helpers
    def _lock(self, key) -> asyncio.Lock:
        if self.no_fork:
            return asyncio.Lock()  # no sharing in the ablation
        return self._stage_locks.setdefault(key, asyncio.Lock())

    def _add(self, node: Node, tag: str | None = None) -> None:
        if tag and not self.no_fork:
            node.tag = f"{self.tag_prefix}/{tag}"
        self.tree.add(node)
        self.events.emit("checkpoint", node=node.__dict__)


def _note(label: str | None, detail: str) -> str:
    """Failure detail without losing the branch's label (the UI groups branches by it)."""
    return f"{label} | {detail}" if label else detail


def _tag() -> str:
    return uuidlib.uuid4().hex[:12]
