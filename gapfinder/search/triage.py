"""Failure triage (Nemotron 3 Super): when a hypothesis's branches fail, read the log tail and say why.

The common case is an invalid value for the artifact (e.g. the ledger proposed `threshold=auto`
for a float flag): Super proposes a valid value, which is tried once. Crashes, timeouts and
infrastructure errors are recorded, not retried here. Super never edits code: it can only suggest
another value for the same knob, which still passes through the spec (shell-safe rendering, cost
limits) like any other hypothesis.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

from gapfinder.ledger.schemas import Branch

TRIAGE_PROMPT = """A benchmark run failed. Classify the failure and, if the cause is an invalid value
for the setting that was changed, propose ONE valid value that keeps the same intent.

Setting changed: {knob} = {value!r} (the artifact's default is {default!r})
Command:
{command}

Last lines of the error output:
{log}

kind: "invalid_value" (the program rejected the value), "crash" (it ran and crashed),
"timeout", "infra" (sandbox or environment problem), or "other".
suggestion: a valid value for {knob} (only for invalid_value; otherwise null). The default
{default!r} has already been measured, so suggest a different valid value that is closest to what
{value!r} meant; null if there is none.
"""


class Triage(BaseModel):
    kind: Literal["invalid_value", "crash", "timeout", "infra", "other"]
    suggestion: str | None = None
    why: str


async def triage(router, knob: str, value: str, default: str, branch: Branch) -> Triage:
    log = (branch.note or "")[-2500:]
    msg = TRIAGE_PROMPT.format(knob=knob, value=value, default=default, command=branch.command[:1500], log=log)
    return await router.structured("super", [{"role": "user", "content": msg}], Triage)
