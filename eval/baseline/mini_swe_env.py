"""mini-swe-agent environment over GapFinder's SandboxBackend (~50 lines of logic).

Why not the upstream `ContreeEnvironment`: it builds its own `ContreeSync`
client from config and cannot take an explicit one, so it can't share the
backend, cost meter and sandbox type GapFinder uses. Fairness rule: same
sandbox machine type for both arms. This adapter gives the baseline exactly
that, plus a linear history: each command runs from the previous command's
checkpoint, with no forking. That is how a normal shell agent works.
"""

from __future__ import annotations

import asyncio
import platform
import threading
from typing import Any

from minisweagent.exceptions import Submitted

from gapfinder.sandbox.backend import InfraError, SandboxBackend
from gapfinder.sandbox.cost import CostMeter

SUBMIT = "COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"


class SandboxEnvironment:
    def __init__(self, backend: SandboxBackend, start_checkpoint: str, *, timeout: int = 1800,
                 env: dict[str, str] | None = None, cost: CostMeter | None = None, max_output: int = 20000):
        self.backend, self.checkpoint = backend, start_checkpoint
        self.timeout, self.env, self.max_output = timeout, env or {}, max_output
        self.cost = cost or CostMeter()
        self.history: list[dict] = []  # (command, checkpoint, exit, cost) for the audit log
        self._loop = asyncio.new_event_loop()
        threading.Thread(target=self._loop.run_forever, daemon=True).start()

    def _sync(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result()

    def execute(self, action: dict, cwd: str = "", *, timeout: int | None = None) -> dict[str, Any]:
        command = action.get("command", "")
        if cwd:
            command = f"cd {cwd} && {command}"
        try:
            res = self._sync(self.backend.run(self.checkpoint, command, env=self.env, timeout=timeout or self.timeout))
        except InfraError as exc:
            return {"output": "", "returncode": -1, "exception_info": f"sandbox error: {exc}"}
        self.cost.add_run(res.resources.cost_usd)
        if res.checkpoint:  # linear chain: next command starts where this one ended
            self.checkpoint = res.checkpoint
        out = (res.stdout + res.stderr)
        if len(out) > self.max_output:
            out = out[: self.max_output // 2] + "\n...[output truncated]...\n" + out[-self.max_output // 2:]
        if res.timed_out:
            out += f"\n[command timed out after {timeout or self.timeout}s]"
        self.history.append({"command": command, "checkpoint": self.checkpoint, "exit": res.exit_code,
                             "cost_usd": res.resources.cost_usd, "elapsed_s": res.resources.elapsed_s})
        output = {"output": out, "returncode": res.exit_code, "exception_info": ""}
        lines = out.lstrip().splitlines(keepends=True)
        if lines and lines[0].strip() == SUBMIT and res.exit_code == 0:
            submission = "".join(lines[1:])
            raise Submitted({"role": "exit", "content": submission,
                             "extra": {"exit_status": "Submitted", "submission": submission}})
        return output

    def get_template_vars(self, **kwargs) -> dict[str, Any]:
        return {**platform.uname()._asdict(), "cwd": "/work", **kwargs}

    def serialize(self) -> dict:
        return {"info": {"config": {"environment": {"backend": self.backend.name, "timeout": self.timeout},
                                    "environment_type": f"{__name__}.SandboxEnvironment"},
                         "sandbox_history": self.history, "sandbox_cost": self.cost.summary()}}
