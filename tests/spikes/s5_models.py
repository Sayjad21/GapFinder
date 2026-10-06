"""S5 - Models: each Nemotron tier returns valid JSON for a schema task; Ultra handles a ~100K-token prompt.

Also lists the models the key can see, to confirm the IDs in config.py.

    python tests/spikes/s5_models.py [--long-tokens 100000]
"""

import argparse
import asyncio
import time
from pathlib import Path

from _common import ROOT, Check, need, save
from pydantic import BaseModel

from gapfinder.config import settings, tiers
from gapfinder.models.router import Router


class Extract(BaseModel):
    benchmark: str
    ops_per_sec: float
    micros_per_op: float


LOG = "fillrandom   :       2.345 micros/op 426439 ops/sec 23.450 seconds 10000000 operations;   47.2 MB/s"


async def main(long_tokens: int) -> None:
    need("TOKEN_FACTORY_API_KEY")
    from openai import AsyncOpenAI

    s = settings()
    client = AsyncOpenAI(base_url=s.token_factory_base_url, api_key=s.token_factory_api_key)
    check = Check()
    listed = sorted(m.id for m in (await client.models.list()).data)
    nemotron = [m for m in listed if "emotron" in m]
    configured = {name: t.model_id for name, t in tiers().items()}
    check("configured IDs exist", all(mid in listed for mid in configured.values()),
          configured=configured, nemotron_listed=nemotron)

    router = Router(use_cache=False)
    per_tier = {}
    for name in ("nano", "super", "ultra", "omni"):
        t0 = time.monotonic()
        try:
            out = await router.structured(name, [{"role": "user", "content": f"Parse this db_bench line:\n{LOG}"}], Extract)
            ok = out.ops_per_sec == 426439 and out.micros_per_op == 2.345
            per_tier[name] = {"ok": ok, "s": round(time.monotonic() - t0, 2), "parsed": out.model_dump()}
        except Exception as exc:  # record, keep going
            per_tier[name] = {"ok": False, "error": repr(exc)[:500]}
        detail = {k: v for k, v in per_tier[name].items() if k != "ok"}
        check(f"{name}: valid JSON for schema task", per_tier[name]["ok"], **detail)

    # Long-context probe: repeat the paper text up to ~long_tokens (4 chars/token) and plant a needle.
    paper_path = ROOT / "papers" / "ruskey" / "ruskey_paper.txt"  # git-ignored; filler is fine for a context probe
    paper = (paper_path.read_text(encoding="utf-8", errors="replace") if paper_path.exists()
             else "RocksDB compaction policy tuning under mixed read/write workloads. " * 200)
    filler = (paper * (long_tokens * 4 // len(paper) + 1))[: long_tokens * 4]
    mid = len(filler) // 2
    prompt = filler[:mid] + "\nNEEDLE: the secret build flag is GF_NEEDLE_7731.\n" + filler[mid:]

    class Needle(BaseModel):
        flag: str

    t0 = time.monotonic()
    try:
        n = await router.structured("ultra", [{"role": "user", "content": prompt + "\n\nWhat is the secret build flag?"}],
                                    Needle)
        long_ok, detail = "GF_NEEDLE_7731" in n.flag, {"answer": n.flag}
    except Exception as exc:
        long_ok, detail = False, {"error": repr(exc)[:800]}
    check(f"ultra ~{long_tokens // 1000}K-token prompt", long_ok, s=round(time.monotonic() - t0, 1), **detail)

    save("S5", {"pass": check.all_ok, "base_url": s.token_factory_base_url, "models_listed": listed,
                "usage": router.meter.summary(), "checks": check.items})


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--long-tokens", type=int, default=100_000)
    asyncio.run(main(p.parse_args().long_tokens))
