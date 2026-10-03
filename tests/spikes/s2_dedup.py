"""S2 - Dedup: does the same command from the same image re-execute or return a cached result?

The branching guide shows identical UUIDs for identical commands. If results
are cached, noise calibration would see zero variance, so every repeat gets a
RUN_TAG env var. This spike tells us which world we are in.
"""

import asyncio

from _common import Check, need, save

from gapfinder.sandbox.backend import ContreeBackend

CMD = "head -c 16 /dev/urandom | od -An -tx1 | tr -d ' \\n'; echo; date +%s%N"


async def main() -> None:
    need("NEBIUS_API_KEY", "NEBIUS_PROJECT_ID")
    be = ContreeBackend()
    check = Check()
    base = await be.base("ubuntu:24.04")

    r1 = await be.run(base, CMD)
    r2 = await be.run(base, CMD)
    cached = r1.stdout == r2.stdout
    check("identical command, no tag", True, same_stdout=cached, same_uuid=r1.checkpoint == r2.checkpoint,
          note="cached result returned" if cached else "re-executed")

    t1 = await be.run(base, CMD, env={"RUN_TAG": "s2-a"})
    t2 = await be.run(base, CMD, env={"RUN_TAG": "s2-b"})
    check("distinct RUN_TAG re-executes", t1.stdout != t2.stdout, same_uuid=t1.checkpoint == t2.checkpoint)

    d1 = await be.run(base, CMD, disposable=True)
    d2 = await be.run(base, CMD, disposable=True)
    check("disposable identical runs", True, same_stdout=d1.stdout == d2.stdout)

    save("S2", {"pass": check.all_ok, "identical_commands_cached": cached,
                "decision": "RUN_TAG required on every repeat" if cached else "RUN_TAG kept anyway (cheap, defensive)",
                "checks": check.items})


if __name__ == "__main__":
    asyncio.run(main())
