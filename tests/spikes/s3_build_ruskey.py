"""S3 - Put the RusKey driver in a sandbox, load the dataset, checkpoint both.

The driver is prebuilt locally: compiling RocksDB in a sandbox costs thousands of CPU-seconds
(~$20-40 at the price measured in eval/results/spikes/S0_pricing_probe.json). So:

    # inside WSL: stripped binary + its non-system libs + provenance
    bash scripts/prep_ruskey_bin.sh /root/ruskey /tmp/ruskey_bin && cp -r /tmp/ruskey_bin <repo>/.gf_cache/
    # then, with the RusKey budget tag so the project cap applies:
    GF_SPEND_TAG=ruskey GF_TAG_CAP_USD=8 python tests/spikes/s3_build_ruskey.py --num-keys 500000

It uploads the bundle and papers/ruskey/harness into /work of ubuntu:24.04 (the *source*
checkpoint), then runs the spec's build check and load stage through the same Orchestrator
the search uses, so the loaded checkpoint is exactly what branches fork from.
Prints GF_RUSKEY_SOURCE / GF_RUSKEY_BUILT / GF_RUSKEY_LOADED for .env.

Pass: the binary runs, the load succeeds, the loaded image fits in 12 GiB; time and cost recorded.
"""

import argparse
import asyncio
import json
import os
import time
from pathlib import Path

from _common import ROOT, Check, need, save

from gapfinder.models import budget
from gapfinder.sandbox.backend import ContreeBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator


def bundle_files(bundle: Path) -> dict[str, bytes]:
    files = {}
    for sub in ("driver", "lib"):
        for f in (bundle / sub).iterdir():
            files[f"{sub}/{f.name}"] = f.read_bytes()
    files["provenance.json"] = (bundle / "provenance.json").read_bytes()
    for f in (ROOT / "papers" / "ruskey" / "harness").glob("*.sh"):
        files[f"harness/{f.name}"] = f.read_bytes().replace(b"\r\n", b"\n")
    return files


async def main(bundle: Path, num_keys: int) -> None:
    need("NEBIUS_API_KEY", "NEBIUS_PROJECT_ID")
    be = ContreeBackend()
    check = Check()
    t0, s0 = time.monotonic(), budget.spent_usd()
    base = await be.base("ubuntu:24.04")
    files = bundle_files(bundle)
    setup = ("chmod +x driver/ruskey_bench harness/*.sh && "
             "LD_LIBRARY_PATH=/work/lib ./driver/ruskey_bench --help 2>&1 | head -1")
    src = await be.run(base, setup, files=files, timeout=600)
    ok = check("prebuilt driver runs in ubuntu:24.04", src.exit_code == 0 and "RusKey" in src.stdout,
               out=src.stdout.strip()[:120], err=src.stderr[-300:], usd=src.resources.cost_usd)
    if not ok:
        save("S3", {"pass": False, "checks": check.items})
        return
    await be.tag(src.checkpoint, "gf/ruskey/source")

    os.environ["GF_RUSKEY_SOURCE"] = src.checkpoint
    from gapfinder.sandbox.spec import HarnessSpec

    spec = HarnessSpec.load_yaml(ROOT / "papers" / "ruskey" / "ruskey_fig6.yaml")
    spec.knobs["num_keys"].default = str(num_keys)
    events = EventLog(ROOT / "eval" / "results" / "spikes" / "S3_events.jsonl")
    orch = Orchestrator(be, spec, events, tag_prefix="gf/ruskey")
    orch.adopt("source", src.checkpoint)
    try:
        loaded = await orch.stage("loaded", {})
        built = orch.tree.find_stage("built")
        check("build check + load via the harness spec", True, built=built, loaded=loaded)
    except RuntimeError as exc:
        check("build check + load via the harness spec", False, error=str(exc)[-1500:])
        save("S3", {"pass": False, "source": src.checkpoint, "checks": check.items})
        return
    stages = {n.stage: {"id": n.id, "cpu_s": n.elapsed_s, "usd": n.cost_usd}
              for n in orch.tree.nodes.values() if n.stage in ("built", "loaded")}
    size = await be.run(loaded, "du -sm /work/db | cut -f1; cat /work/load.log | tail -2", disposable=True, timeout=300)
    lines = size.stdout.split()
    db_mb = int(lines[0]) if lines and lines[0].isdigit() else None
    check("fits 12 GiB layer", db_mb is not None and db_mb < 11 * 1024, db_mb=db_mb)
    await orch.tag_key_nodes()
    print("\nAdd to .env:")
    print(f"GF_RUSKEY_SOURCE={src.checkpoint}\nGF_RUSKEY_BUILT={built}\nGF_RUSKEY_LOADED={loaded}\n")
    save("S3", {"pass": check.all_ok, "num_keys": num_keys, "wall_s": round(time.monotonic() - t0, 1),
                "cost_usd": round(budget.spent_usd() - s0, 4), "stages": stages,
                "GF_RUSKEY_SOURCE": src.checkpoint, "GF_RUSKEY_BUILT": built, "GF_RUSKEY_LOADED": loaded,
                "provenance": json.loads(files["provenance.json"]), "checks": check.items})


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--bundle", type=Path, default=ROOT / ".gf_cache" / "ruskey_bin")
    p.add_argument("--num-keys", type=int, default=500_000)
    a = p.parse_args()
    asyncio.run(main(a.bundle, a.num_keys))
