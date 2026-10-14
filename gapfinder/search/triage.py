"""Failure triage (Nemotron 3 Super): when a hypothesis's branches fail, read the log tail and say why.

The common case is an invalid value for the artifact (e.g. the ledger proposed `threshold=auto`
for a float flag): Super proposes a valid value, which is tried once. Crashes, timeouts and
infrastructure errors are recorded, not retried here. Super never edits code: it can only suggest
another value for the same knob, which still passes through the spec (shell-safe rendering, cost
limits) like any other hypothesis.
"""

from __future__ import annotations

import re
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


# A program that rejects a value says so: argparse errors, type conversions, explicit checks. Without one of
# these in the log, "invalid_value" is a guess, and swapping the value would lose the hypothesis (MC Dropout
# v1.1: a Theano compile-cache race was read as "the program rejected epochx=10", which was then replaced).
REJECTION = re.compile(r"error: argument|invalid choice|invalid (?:int|float|literal)|unrecognized arguments|"
                       r"ValueError|TypeError|must be|not supported|out of range|expected one of|"
                       r"could not convert", re.I)
# Signs that the environment failed, not the value: retry the same value once.
INFRA = re.compile(r"No module named 'tmp|compiledir|Removing key file|lock(?:ed| file)|Resource temporarily "
                   r"unavailable|No space left|Connection (?:reset|refused|aborted)|Broken pipe|"
                   r"Temporary failure|sandbox (?:error|unavailable)|OSError: \[Errno (?:11|28|104|111)\]", re.I)


def looks_like_infra(branch: Branch) -> bool:
    return bool(INFRA.search(branch.note or ""))


def shows_rejection(branch: Branch) -> bool:
    return bool(REJECTION.search(branch.note or ""))


class Triage(BaseModel):
    kind: Literal["invalid_value", "crash", "timeout", "infra", "other"]
    suggestion: str | None = None
    why: str


async def triage(router, knob: str, value: str, default: str, branch: Branch) -> Triage:
    log = (branch.note or "")[-2500:]
    msg = TRIAGE_PROMPT.format(knob=knob, value=value, default=default, command=branch.command[:1500], log=log)
    return await router.structured("super", [{"role": "user", "content": msg}], Triage)
