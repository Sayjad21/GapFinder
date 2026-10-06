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
    import json

    import httpx

    try:
        r = httpx.get(s.token_factory_base_url.rstrip("/") + "/models", params={"verbose": "true"},
                      headers={"Authorization": f"Bearer {s.token_factory_api_key}"}, timeout=30)
        r.raise_for_status()
        data = r.json()["data"]
        models = sorted(m["id"] for m in data)
    except Exception as exc:
        print(f"    FAIL: {type(exc).__name__}: {str(exc)[:300]}")
        print("    -> wrong key, or try TOKEN_FACTORY_BASE_URL=https://api.tokenfactory.us-central1.nebius.com/v1/")
        return False
    prices = {m["id"]: (float(m["pricing"]["prompt"]) * 1e6, float(m["pricing"]["completion"]) * 1e6)
              for m in data if m.get("pricing", {}).get("prompt") is not None}
    s.cache_dir.mkdir(parents=True, exist_ok=True)
    (s.cache_dir / "pricing.json").write_text(json.dumps(prices, indent=1))
    print(f"    OK: {len(models)} models visible; live prices saved for {len(prices)} (used by the spend ledger)")
    ok = True
    for name, t in tiers().items():
        found = t.model_id in models
        if name != "omni":  # image tier is optional: only figure reading needs it
            ok &= found
        near = [m for m in models if t.model_id.split("/")[-1].lower()[:14] in m.lower()]
        price = f"${prices[t.model_id][0]:.2f}/${prices[t.model_id][1]:.2f} per 1M" if t.model_id in prices else ""
        print(f"    {'ok ' if found else 'MISSING'} {name:6s} {t.model_id}  {price}" + ("" if found else f"   similar: {near[:3]}"))
    if not ok:
        print("    -> set GF_MODEL_<TIER>=<exact id> in .env for any missing tier")
    return ok


async def check_sandboxes() -> bool:
    key, proj = os.environ.get("NEBIUS_API_KEY"), os.environ.get("NEBIUS_PROJECT_ID")
    print(f"\n[2] Sandboxes  NEBIUS_API_KEY: {mask(key)}  NEBIUS_PROJECT_ID: {mask(proj)}")
    if not key or not proj:
        print("    -> add NEBIUS_PROJECT_ID to .env (key is set; the server rejects requests without a project)")
        return False
    from contree_sdk import Contree

    try:
        info = await Contree()._get_token_info()
    except Exception as exc:
        print(f"    FAIL: {type(exc).__name__}: {str(exc)[:300]}")
        print("    -> 401/403 usually means Beta access not granted yet, or wrong project ID")
        return False
    perms = getattr(info, "permissions", {}) or {}
    print(f"    authenticated. permissions: {perms}")
    print(f"    limits: {getattr(info, 'limits', {})}")
    if not perms.get("spawn"):
        print("    NOT READY: 'spawn' is false -> wrong project ID, or Sandboxes Beta access not granted yet")
        return False
    print("    OK: can spawn sandboxes")
    return True


async def main() -> int:
    a = await check_inference()
    b = await check_sandboxes()
    tav = os.environ.get("TAVILY_API_KEY")
    print(f"\n[3] Tavily (optional, M3)  key: {mask(tav)}")
    if tav:
        import httpx

        r = httpx.get("https://api.tavily.com/usage", headers={"Authorization": f"Bearer {tav}"}, timeout=30)
        if r.status_code == 200:
            acct = r.json().get("account", {})
            print(f"    OK: plan {acct.get('current_plan')}, used {acct.get('plan_usage')} of {acct.get('plan_limit')} credits")
        else:
            print(f"    FAIL: {r.status_code} {r.text[:200]}")
    print(f"\nSummary: inference {'OK' if a else 'NOT READY'}, sandboxes {'OK' if b else 'NOT READY'}")
    print("Next: " + ("python tests/spikes/s5_models.py" if a else "fix [1]") +
          ("; python tests/spikes/s1_lifecycle.py" if b else ""))
    return 0 if a and b else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
