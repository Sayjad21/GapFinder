"""Check that every credential GapFinder needs is present and actually works.

    .venv/Scripts/python scripts/check_env.py

Spends nothing: lists models (free) and asks Sandboxes who you are (free).
Prints keys only as their last 4 characters.
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gapfinder.config import settings, tiers  # noqa: E402  (also loads .env)


def mask(v: str | None) -> str:
    return "MISSING" if not v else f"set (...{v[-4:]})"


async def check_inference() -> bool:
    s = settings()
    print(f"\n[1] LLM provider {s.llm_provider!r}  key: {mask(s.token_factory_api_key)}  url: {s.token_factory_base_url}")
    if s.llm_provider != "tokenfactory":
        print("    NOTE: development provider. Submission and demo runs must use Token Factory.")
    if not s.token_factory_api_key:
        hint = ("create a key at https://tokenfactory.nebius.com/project/api-keys" if s.llm_provider == "tokenfactory"
                else "get a free key at https://build.nvidia.com (no card needed)")
        print(f"    -> {hint} and put it in .env")
        return False
    from openai import AsyncOpenAI

    try:
        models = sorted(m.id for m in (await AsyncOpenAI(base_url=s.token_factory_base_url,
                                                          api_key=s.token_factory_api_key).models.list()).data)
    except Exception as exc:
        print(f"    FAIL: {type(exc).__name__}: {str(exc)[:300]}")
        print("    -> wrong key, or try TOKEN_FACTORY_BASE_URL=https://api.tokenfactory.us-central1.nebius.com/v1/")
        return False
    print(f"    OK: {len(models)} models visible")
    ok = True
    for name, t in tiers().items():
        found = t.model_id in models
        ok &= found
        near = [m for m in models if t.model_id.split("/")[-1].lower()[:14] in m.lower()]
        print(f"    {'ok ' if found else 'MISSING'} {name:6s} {t.model_id}" + ("" if found else f"   similar: {near[:3]}"))
    if not ok:
        print("    -> set GF_MODEL_<TIER>=<exact id> in .env for any missing tier")
    return ok


async def check_sandboxes() -> bool:
    key, proj = os.environ.get("NEBIUS_API_KEY"), os.environ.get("NEBIUS_PROJECT_ID")
    print(f"\n[2] Sandboxes  NEBIUS_API_KEY: {mask(key)}  NEBIUS_PROJECT_ID: {mask(proj)}")
    if not key or not proj:
        print("    -> needs Sandboxes Beta access first; then key + project ID in .env")
        return False
    from contree_sdk import Contree

    try:
        info = await Contree()._get_token_info()
    except Exception as exc:
        print(f"    FAIL: {type(exc).__name__}: {str(exc)[:300]}")
        print("    -> 401/403 usually means Beta access not granted yet, or wrong project ID")
        return False
    print(f"    OK: authenticated. limits: {getattr(info, 'limits', {})}")
    return True


async def main() -> int:
    a = await check_inference()
    b = await check_sandboxes()
    tav = os.environ.get("TAVILY_API_KEY")
    print(f"\n[3] Tavily (optional, M3)  key: {mask(tav)}")
    print(f"\nSummary: inference {'OK' if a else 'NOT READY'}, sandboxes {'OK' if b else 'NOT READY'}")
    print("Next: " + ("python tests/spikes/s5_models.py" if a else "fix [1]") +
          ("; python tests/spikes/s1_lifecycle.py" if b else ""))
    return 0 if a and b else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
