"""S3 - Build the RusKey RocksDB fork in release mode, checkpoint, load the dataset, checkpoint again.

First pack the sources inside WSL:
    wsl -d Ubuntu-24.04 -u root -- bash scripts/pack_ruskey.sh /root/ruskey /mnt/c/.../ruskey_src.tar.gz
Then:
    python tests/spikes/s3_build_ruskey.py --tarball ruskey_src.tar.gz --num-keys 2000000

Pass: build and load both succeed, the loaded image fits the 12 GiB layer, time and cost recorded.
"""

import argparse
import asyncio
import json
import time
from pathlib import Path

from _common import Check, need, save

from gapfinder.sandbox.backend import ContreeBackend

DEPS = ("apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq "
        "build-essential libgflags-dev libsnappy-dev zlib1g-dev libbz2-dev liblz4-dev libzstd-dev "
        "python3 python3-pip python3-venv > /dev/null && echo deps-ok")
BUILD = ("tar -xzf src.tar.gz && rm src.tar.gz && cd rocksdb && "
         "make -j$(nproc) AUTO_CLEAN=1 DISABLE_WARNING_AS_ERROR=1 DEBUG_LEVEL=0 static_lib > /work/build.log 2>&1 && "
         "cd ../driver && make >> /work/build.log 2>&1 && ./ruskey_bench --help | head -5 && "
         "find /work/rocksdb -name '*.o' -delete && du -sh /work")
LOAD = ("mkdir -p /work/db && cd /work/driver && "
        "./ruskey_bench --db /work/db --num_keys {n} --load_only --direct_io --target_file_size_mb 2 "
        "> /work/load.log 2>&1; echo exit=$?; du -sm /work/db | cut -f1; df -m /work | tail -1")


async def main(tarball: Path, num_keys: int) -> None:
    need("NEBIUS_API_KEY", "NEBIUS_PROJECT_ID")
    be = ContreeBackend()
    check = Check()
    t = time.monotonic()
    base = await be.base("ubuntu:24.04")
    deps = await be.run(base, DEPS, timeout=1200)
    check("dependencies", "deps-ok" in deps.stdout, s=deps.resources.elapsed_s, usd=deps.resources.cost_usd)

    src = await be.run(deps.checkpoint, "ls -la src.tar.gz", files={"src.tar.gz": tarball.read_bytes()}, timeout=600)
    built = await be.run(src.checkpoint, BUILD, timeout=3600)
    ok = check("build (release, DEBUG_LEVEL=0)", built.exit_code == 0, s=built.resources.elapsed_s,
               usd=built.resources.cost_usd, cpu_s=built.resources.user_cpu_s, tail=built.stdout[-400:])
    if not ok:
        log = await be.read_file(built.checkpoint, "build.log") if built.checkpoint else b""
        save("S3", {"pass": False, "checks": check.items, "build_log_tail": log[-4000:].decode(errors="replace")})
        return
    await be.tag(built.checkpoint, "gf/ruskey/built")

    loaded = await be.run(built.checkpoint, LOAD.format(n=num_keys), timeout=7200)
    lines = loaded.stdout.strip().splitlines()
    db_mb = int(lines[1]) if len(lines) > 1 and lines[1].isdigit() else None
    check("load", "exit=0" in loaded.stdout, s=loaded.resources.elapsed_s, usd=loaded.resources.cost_usd,
          db_mb=db_mb, df=lines[2] if len(lines) > 2 else None)
    check("fits 12 GiB layer", db_mb is not None and db_mb < 11 * 1024, db_mb=db_mb)
    if loaded.checkpoint:
        await be.tag(loaded.checkpoint, "gf/ruskey/loaded")
    meta = tarball.with_suffix("").with_suffix(".json")
    save("S3", {"pass": check.all_ok, "num_keys": num_keys, "wall_s": round(time.monotonic() - t, 1),
                "source": json.loads(meta.read_text()) if meta.exists() else None,
                "built": built.checkpoint, "loaded": loaded.checkpoint, "checks": check.items})


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--tarball", type=Path, required=True)
    p.add_argument("--num-keys", type=int, default=2_000_000, help="2M x 1 KB ~ 2 GB; scale toward 10M if it fits")
    a = p.parse_args()
    asyncio.run(main(a.tarball, a.num_keys))
