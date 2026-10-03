"""S1 - Sandbox lifecycle.

Base image, chained runs, 3 branches from one checkpoint, isolation (file
written in branch A absent in B), 40 concurrent runs, timeout, log download.
Records nproc, memory and disk speed inside a sandbox.

    python tests/spikes/s1_lifecycle.py [--image ubuntu:24.04] [--concurrency 40]
"""

import argparse
import asyncio
import time

from _common import Check, need, save

from gapfinder.sandbox.backend import ContreeBackend


async def main(image: str, concurrency: int) -> None:
    need("NEBIUS_API_KEY", "NEBIUS_PROJECT_ID")
    be = ContreeBackend()
    check = Check()
    t0 = time.monotonic()
    base = await be.base(image)
    check("base image", bool(base), uuid=base, seconds=round(time.monotonic() - t0, 1))

    a = await be.run(base, "echo one > chain.txt")
    b = await be.run(a.checkpoint, "echo two >> chain.txt && cat chain.txt")
    check("chained runs keep filesystem", b.stdout.split() == ["one", "two"], stdout=b.stdout)

    branches = await asyncio.gather(*(be.run(b.checkpoint, f"echo branch{i} > mine.txt; ls") for i in range(3)))
    check("3 branches from one checkpoint", all(r.exit_code == 0 for r in branches),
          uuids=[r.checkpoint for r in branches])
    probe = await be.run(branches[1].checkpoint, "cat mine.txt; test -f other.txt && echo leak || echo clean")
    check("isolation: sibling write absent", "branch1" in probe.stdout and "clean" in probe.stdout, stdout=probe.stdout)

    env = await be.run(base, "nproc; free -m | awk '/Mem:/{print $2}'; df -m /work | tail -1 | awk '{print $4}'; "
                            "dd if=/dev/zero of=/work/dd.bin bs=1M count=512 oflag=direct 2>&1 | tail -1; "
                            "dd if=/work/dd.bin of=/dev/null bs=1M iflag=direct 2>&1 | tail -1; rm -f /work/dd.bin",
                       disposable=True, timeout=300)
    lines = env.stdout.strip().splitlines()
    check("machine shape recorded", env.exit_code == 0, nproc=lines[0] if lines else None,
          mem_mb=lines[1] if len(lines) > 1 else None, free_disk_mb=lines[2] if len(lines) > 2 else None,
          dd_write=lines[3] if len(lines) > 3 else None, dd_read=lines[4] if len(lines) > 4 else None,
          cost_usd=env.resources.cost_usd)

    t1 = time.monotonic()
    sem = asyncio.Semaphore(concurrency)

    async def one(i):
        async with sem:
            return await be.run(base, f"sleep 5; echo {i} $RUN_TAG", env={"RUN_TAG": f"s1-{i}-{time.time()}"},
                                disposable=True, timeout=120)

    results = await asyncio.gather(*(one(i) for i in range(concurrency)), return_exceptions=True)
    errors = [repr(r) for r in results if isinstance(r, Exception)]
    wall = time.monotonic() - t1
    check(f"{concurrency} concurrent runs", not errors, wall_s=round(wall, 1), errors=errors[:5],
          parallel_speedup=round(5 * concurrency / wall, 1) if wall else None)

    to = await be.run(base, "sleep 60", timeout=5, disposable=True)
    check("timeout enforced", to.timed_out or to.exit_code != 0, exit_code=to.exit_code, timed_out=to.timed_out)

    big = await be.run(base, "mkdir -p logs; seq 1 400000 > logs/bench.log; echo done", timeout=120)
    data = await be.read_file(big.checkpoint, "logs/bench.log")
    check("log download via inspect API (bypasses 1 MiB stdout cap)", data.count(b"\n") == 400000, bytes=len(data))

    await be.tag(base, "gf/spike/s1-base")
    save("S1", {"pass": check.all_ok, "image": image, "checks": check.items})


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--image", default="ubuntu:24.04")
    p.add_argument("--concurrency", type=int, default=40)
    a = p.parse_args()
    asyncio.run(main(a.image, a.concurrency))
