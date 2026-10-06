"""S3 - Build the RusKey RocksDB fork in release mode, checkpoint it, load the dataset, checkpoint again.

First pack the sources inside WSL (paths are WSL paths):
    bash scripts/pack_ruskey.sh /root/ruskey /mnt/c/.../gapfinder-repo/.gf_cache/ruskey_src.tar.gz
Then:
    python tests/spikes/s3_build_ruskey.py --tarball .gf_cache/ruskey_src.tar.gz [--num-keys 2000000]

It prepares the *source* checkpoint (dependencies + RusKey sources + papers/ruskey/harness in
/work) and then builds and loads it through papers/ruskey/ruskey_fig6.yaml with the same
Orchestrator the search uses, so the built/loaded checkpoints are exactly the ones branches
fork from. Prints GF_RUSKEY_SOURCE=<uuid> for .env.

Pass: build and load succeed; the loaded image fits in the 12 GiB layer; time and cost recorded.
"""

import argparse
import asyncio
import json
import os
import time
from pathlib import Path

from _common import ROOT, Check, need, save

from gapfinder.sandbox.backend import ContreeBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator

DEPS = ("apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq "
        "build-essential libgflags-dev libsnappy-dev zlib1g-dev libbz2-dev liblz4-dev libzstd-dev "
        "python3 > /dev/null && mkdir -p /work && echo deps-ok")
UNPACK = "cd /work && tar -xzf src.tar.gz && rm src.tar.gz && chmod +x harness/*.sh && ls"


async def main(tarball: Path, num_keys: int) -> None:
    need("NEBIUS_API_KEY", "NEBIUS_PROJECT_ID")
    be = ContreeBackend()
    check = Check()
    t0 = time.monotonic()
    base = await be.base("ubuntu:24.04")
    deps = await be.run(base, DEPS, timeout=1800)
    check("dependencies", "deps-ok" in deps.stdout, s=deps.resources.elapsed_s, usd=deps.resources.cost_usd)

    files = {"src.tar.gz": tarball.read_bytes()}
    for f in (ROOT / "papers" / "ruskey" / "harness").glob("*.sh"):
        files[f"harness/{f.name}"] = f.read_bytes().replace(b"\r\n", b"\n")
    src = await be.run(deps.checkpoint, UNPACK, files=files, timeout=900)
    ok = check("sources + harness in /work", src.exit_code == 0 and "harness" in src.stdout, ls=src.stdout[-300:])
    if not ok:
        save("S3", {"pass": False, "checks": check.items, "stderr": src.stderr[-2000:]})
        return
    await be.tag(src.checkpoint, "gf/ruskey/source")
    print(f"\nGF_RUSKEY_SOURCE={src.checkpoint}   <- add this line to .env\n")

    os.environ["GF_RUSKEY_SOURCE"] = src.checkpoint
    from gapfinder.sandbox.spec import HarnessSpec

    spec = HarnessSpec.load_yaml(ROOT / "papers" / "ruskey" / "ruskey_fig6.yaml")
    spec.knobs["num_keys"].default = str(num_keys)
    events = EventLog(ROOT / "eval" / "results" / "spikes" / "S3_events.jsonl")
    orch = Orchestrator(be, spec, events, tag_prefix="gf/ruskey")
    try:
        loaded = await orch.stage("loaded", {})
        built = orch.tree.find_stage("built")
        check("build (release) + load via the harness spec", True, built=built, loaded=loaded)
    except RuntimeError as exc:
        check("build (release) + load via the harness spec", False, error=str(exc)[-1500:])
        save("S3", {"pass": False, "source": src.checkpoint, "checks": check.items})
        return
    stages = {n.stage: {"id": n.id, "s": n.elapsed_s, "usd": n.cost_usd} for n in orch.tree.nodes.values()}
    size = await be.run(loaded, "du -sm /work/db | cut -f1; df -m /work | tail -1", disposable=True, timeout=300)
    lines = size.stdout.split()
    db_mb = int(lines[0]) if lines and lines[0].isdigit() else None
    check("fits 12 GiB layer", db_mb is not None and db_mb < 11 * 1024, db_mb=db_mb, df=size.stdout[-200:])
    await orch.tag_key_nodes()
    print("\nAdd to .env:")
    print(f"GF_RUSKEY_SOURCE={src.checkpoint}\nGF_RUSKEY_BUILT={built}\nGF_RUSKEY_LOADED={loaded}\n")
    meta = tarball.with_suffix("").with_suffix(".json")
    save("S3", {"pass": check.all_ok, "num_keys": num_keys, "wall_s": round(time.monotonic() - t0, 1),
                "GF_RUSKEY_SOURCE": src.checkpoint, "GF_RUSKEY_BUILT": built, "GF_RUSKEY_LOADED": loaded,
                "stages": stages,
                "source_commit": json.loads(meta.read_text()) if meta.exists() else None, "checks": check.items})


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--tarball", type=Path, required=True)
    p.add_argument("--num-keys", type=int, default=2_000_000, help="2M x 1 KB ~ 2 GB; scale toward 10M if it fits")
    a = p.parse_args()
    asyncio.run(main(a.tarball, a.num_keys))
