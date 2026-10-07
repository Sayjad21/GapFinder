"""S4 - Noise: 5 identical forks of the loaded RusKey checkpoint run the same Figure 6 cells.

Uses papers/ruskey/ruskey_fig6.yaml and the checkpoints from spike S3 (GF_RUSKEY_SOURCE,
GF_RUSKEY_BUILT, GF_RUSKEY_LOADED in .env), through the same Orchestrator the search uses.
Pass: the within-VM latency ratios (the search's targets) have CV <= 10%. Write amplification
should be steadier still. Fallback if not: claims move to hardware-independent metrics.

    python tests/spikes/s4_noise.py [--n 5] [--missions 40]
"""

import argparse
import asyncio
import os

from _common import ROOT, Check, need, save

from gapfinder.sandbox.backend import ContreeBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec

RATIOS = ("balanced_ratio_k1_k5", "balanced_ratio_k10_k5", "writeheavy_ratio_k1_k10")


async def main(n: int, missions: int) -> None:
    need("NEBIUS_API_KEY", "NEBIUS_PROJECT_ID", "GF_RUSKEY_SOURCE", "GF_RUSKEY_BUILT", "GF_RUSKEY_LOADED")
    spec = HarnessSpec.load_yaml(ROOT / "papers" / "ruskey" / "ruskey_fig6.yaml")
    if missions is not None:
        spec.knobs["missions"].default = str(missions)
    orch = Orchestrator(ContreeBackend(), spec, EventLog(ROOT / "eval" / "results" / "spikes" / "S4_events.jsonl"))
    orch.adopt("source", os.environ["GF_RUSKEY_SOURCE"])
    orch.adopt("built", os.environ["GF_RUSKEY_BUILT"], os.environ["GF_RUSKEY_SOURCE"])
    orch.adopt("loaded", os.environ["GF_RUSKEY_LOADED"], os.environ["GF_RUSKEY_BUILT"])
    check = Check()
    bands, branches = await orch.calibrate_noise(n=n)
    ok_runs = [b for b in branches if b.status == "succeeded"]
    check("identical forks ran", len(ok_runs) >= 3, succeeded=len(ok_runs), of=n,
          notes=[b.note for b in branches if b.status != "succeeded"][:3])
    summary = {m: b.to_dict() for m, b in bands.items()}
    ratio_ok = all(m in bands and bands[m].cv <= 0.10 for m in RATIOS)
    check("latency ratios CV <= 10%", ratio_ok, cv={m: round(bands[m].cv, 3) for m in RATIOS if m in bands})
    save("S4", {"pass": check.all_ok, "n": n, "missions": missions, "bands": summary,
                "elapsed_s": [b.resources.elapsed_s for b in ok_runs],
                "cost_usd": sum(b.resources.cost_usd for b in branches), "checks": check.items})


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--missions", type=int, default=None, help="override the spec default")
    a = p.parse_args()
    asyncio.run(main(a.n, a.missions))
