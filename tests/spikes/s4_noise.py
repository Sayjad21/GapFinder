"""S4 - Noise: 5 identical forks of the loaded checkpoint run the same benchmark.

Pass: CV <= 10% on throughput, or stable ratios between configurations
(K=1 vs K=10 measured in the same fork). Write amplification and compaction
bytes are expected to be far less noisy than latency.

    python tests/spikes/s4_noise.py --loaded <uuid from S3> [--n 5]
"""

import argparse
import asyncio
import json
import statistics

from _common import Check, need, save

from gapfinder.sandbox.backend import ContreeBackend
from gapfinder.sandbox.noise import noise_band, starved
from gapfinder.sandbox.parse import ground_values

# The driver prints one JSON object per mission on stdout (ruskey_bench.cc:1177).
RUN = ("cd /work/driver && ./ruskey_bench --db /work/db --skip_load --direct_io --target_file_size_mb 2 "
       "--missions {m} --ops_per_mission 20000 --lookup_ratio 0.5 --policy {k} --seed {seed} "
       "> /work/out/missions.jsonl 2> /work/out/run.log; echo exit=$?")
ENTRY_BYTES = 128 + 896


async def one(be, loaded, k, seed, missions, tag):
    cmd = "mkdir -p /work/out && " + RUN.format(m=missions, k=k, seed=seed)
    r = await be.run(loaded, cmd, env={"RUN_TAG": tag}, timeout=3600)
    raw = (await be.read_file(r.checkpoint, "out/missions.jsonl")).decode(errors="replace") if r.checkpoint else ""
    lines = [l for l in raw.splitlines() if l.strip().startswith("{")]
    second_half = lines[len(lines) // 2:]  # as in the reproduction's protocol
    per_mission = [ground_values(_numeric(json.loads(l)), l) for l in second_half]
    metrics = {}
    if per_mission:
        metrics["us_per_op"] = statistics.fmean(m["us_per_op"] for m in per_mission)
        metrics["stall_us"] = statistics.fmean(m["stall_us"] for m in per_mission)
        upd = sum(m["updates"] for m in per_mission)
        if upd:  # hardware-independent: bytes compacted+flushed per user byte written
            metrics["write_amp"] = sum(m["c_write_b"] + m["flush_b"] for m in per_mission) / (upd * ENTRY_BYTES)
    return r, metrics


def _numeric(obj: dict) -> dict[str, float]:
    return {k: float(v) for k, v in obj.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}


async def main(loaded: str, n: int, missions: int) -> None:
    need("NEBIUS_API_KEY", "NEBIUS_PROJECT_ID")
    be = ContreeBackend()
    check = Check()
    runs = await asyncio.gather(*(one(be, loaded, "1,1,1,1,1,1", 42, missions, f"s4-k1-{i}") for i in range(n)))
    ratio_runs = await asyncio.gather(*(one(be, loaded, "10,10,10,10,10,10", 42, missions, f"s4-k10-{i}")
                                        for i in range(n)))
    flags = starved([r.resources.involuntary_switches for r, _ in runs])
    bands = {}
    for metric in runs[0][1]:
        vals = [m[metric] for _, m in runs if metric in m]
        if len(vals) >= 3:
            bands[metric] = noise_band(metric, vals).to_dict()
    cv_ok = any(b["cv"] <= 0.10 for k, b in bands.items() if k == "us_per_op")
    ratios = [m1.get("us_per_op", 0) / m10["us_per_op"] for (_, m1), (_, m10) in zip(runs, ratio_runs)
              if m10.get("us_per_op")]
    ratio_cv = statistics.stdev(ratios) / statistics.fmean(ratios) if len(ratios) >= 2 else None
    check("throughput CV <= 10%", cv_ok, bands=bands)
    check("or stable K=1/K=10 ratio", ratio_cv is not None and ratio_cv <= 0.10, ratios=ratios, ratio_cv=ratio_cv)
    save("S4", {"pass": cv_ok or (ratio_cv is not None and ratio_cv <= 0.10), "n": n, "missions": missions,
                "bands": bands, "ratio_cv": ratio_cv, "starved_flags": flags,
                "cost_usd": sum(r.resources.cost_usd for r, _ in runs + ratio_runs), "checks": check.items})


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--loaded", required=True)
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--missions", type=int, default=40)
    a = p.parse_args()
    asyncio.run(main(a.loaded, a.n, a.missions))
