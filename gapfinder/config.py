"""Runtime settings, read from the environment (and an optional .env file)."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_dotenv(path: Path = REPO_ROOT / ".env") -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if value and key not in os.environ:
            os.environ[key] = value


_load_dotenv()

# The Sandboxes CLI reads NEBIUS_AI_PROJECT; contree-sdk's IAMAuth reads NEBIUS_PROJECT_ID.
# Accept either so one .env works for both.
if not os.environ.get("NEBIUS_PROJECT_ID") and os.environ.get("NEBIUS_AI_PROJECT"):
    os.environ["NEBIUS_PROJECT_ID"] = os.environ["NEBIUS_AI_PROJECT"]


@dataclass(frozen=True)
class ModelTier:
    name: str
    model_id: str
    price_in: float  # USD per 1M input tokens
    price_out: float  # USD per 1M output tokens
    max_tokens: int  # generous: reasoning traces count against this


# IDs and prices from the plan's routing table; spike S5 confirms them against
# the list-models API. Override any ID with GF_MODEL_<TIER>.
DEFAULT_TIERS = {
    "ultra": ModelTier("ultra", "nvidia/Nemotron-3-Ultra-550b-a55b", 1.00, 3.00, 32768),
    "super": ModelTier("super", "nvidia/nemotron-3-super-120b-a12b", 0.30, 0.90, 16384),
    "nano": ModelTier("nano", "nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B", 0.06, 0.24, 8192),
    "omni": ModelTier("omni", "nvidia/Nemotron-3-Nano-Omni", 0.06, 0.24, 8192),
}


def _live_prices() -> dict[str, tuple[float, float]]:
    """Per-1M-token prices saved from the provider's /models?verbose=true (scripts/check_env.py writes it)."""
    import json

    path = Path(os.environ.get("GF_CACHE_DIR", REPO_ROOT / ".gf_cache")) / "pricing.json"
    if not path.exists():
        return {}
    return {k: (v[0], v[1]) for k, v in json.loads(path.read_text()).items()}


def tiers() -> dict[str, ModelTier]:
    out, live = {}, _live_prices()
    for name, tier in DEFAULT_TIERS.items():
        model_id = os.environ.get(f"GF_MODEL_{name.upper()}") or tier.model_id
        price_in, price_out = live.get(model_id, (tier.price_in, tier.price_out))
        out[name] = ModelTier(name, model_id, price_in, price_out, tier.max_tokens)
    return out


# GF_LLM_PROVIDER picks where model calls go:
#   tokenfactory (default) -- Nebius Token Factory; required for anything submitted or demoed.
#   nvidia-dev -- NVIDIA's free build.nvidia.com endpoint (no card needed), for development
#                 only while Token Factory billing isn't set up. Same OpenAI-compatible API.
PROVIDERS = {
    "tokenfactory": ("TOKEN_FACTORY_API_KEY", "TOKEN_FACTORY_BASE_URL", "https://api.tokenfactory.nebius.com/v1/"),
    "nvidia-dev": ("NVIDIA_API_KEY", "NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1"),
}


def _provider() -> tuple[str, str, str]:
    name = os.environ.get("GF_LLM_PROVIDER", "tokenfactory")
    if name not in PROVIDERS:
        raise ValueError(f"GF_LLM_PROVIDER must be one of {sorted(PROVIDERS)}, got {name!r}")
    key_var, url_var, _ = PROVIDERS[name]
    return name, key_var, url_var


@dataclass(frozen=True)
class Settings:
    llm_provider: str = field(default_factory=lambda: _provider()[0])
    token_factory_api_key: str | None = field(default_factory=lambda: os.environ.get(_provider()[1]))
    token_factory_base_url: str = field(
        default_factory=lambda: os.environ.get(_provider()[2], PROVIDERS[_provider()[0]][2])
    )
    sandbox_backend: str = field(default_factory=lambda: os.environ.get("GF_SANDBOX_BACKEND", "local"))
    max_concurrency: int = field(default_factory=lambda: int(os.environ.get("GF_MAX_CONCURRENCY", "40")))
    cache_dir: Path = field(default_factory=lambda: Path(os.environ.get("GF_CACHE_DIR", REPO_ROOT / ".gf_cache")))
    local_sandbox_dir: Path = field(
        default_factory=lambda: Path(os.environ.get("GF_LOCAL_SANDBOX_DIR", REPO_ROOT / ".gf_local"))
    )
    runs_dir: Path = field(default_factory=lambda: Path(os.environ.get("GF_RUNS_DIR", REPO_ROOT / "runs")))


def settings() -> Settings:
    return Settings()
