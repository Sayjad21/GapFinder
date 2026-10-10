"""Provenance block for a Gap Report: which code, models, prompts and harness produced it, and its cost.

It records identifiers and hashes only. It never reads the environment for values: model IDs come from
the tier table (which may be overridden by an environment variable, but only the resulting ID is kept),
and nothing about keys, endpoints or the Nebius project is touched, so nothing of that kind can leak
into a report that gets published.
"""

from __future__ import annotations

import hashlib
import json
import subprocess

from gapfinder.config import REPO_ROOT, tiers


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _git(*args: str) -> str | None:
    try:
        out = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None  # no git, or not a checkout
    return out.stdout.strip() if out.returncode == 0 else None


def git_state() -> dict:
    """The commit GapFinder ran from, and whether the working tree had uncommitted changes."""
    commit = _git("rev-parse", "HEAD")
    status = _git("status", "--porcelain") if commit else None
    return {"commit": commit, "dirty": None if status is None else bool(status)}


def prompt_hashes() -> dict[str, str]:
    """sha256 of each prompt template the pipeline sends to a model, by name."""
    found = {}
    for module, names in (("gapfinder.ledger.claims", ("CLAIM_PROMPT", "FILTER_PROMPT")),
                          ("gapfinder.ledger.assumptions", ("ASSUMPTION_PROMPT",)),
                          ("gapfinder.search.triage", ("TRIAGE_PROMPT",))):
        try:
            mod = __import__(module, fromlist=list(names))
        except ImportError:
            continue
        for n in names:
            if hasattr(mod, n):
                found[n] = sha256_text(getattr(mod, n))
    return found


def spec_hash(spec) -> str:
    """sha256 of the harness spec in a canonical form, so formatting and key order don't change it."""
    return sha256_text(json.dumps(spec.model_dump(mode="json"), sort_keys=True, separators=(",", ":")))


def search_cost(search) -> dict:
    """Cost of this search: Nemotron inference (billed) and sandbox runs (reported, not billed in the Beta)."""
    meters = {id(search.orch.cost.tokens): search.orch.cost.tokens}
    if search.router is not None:
        meters[id(search.router.meter)] = search.router.meter
    nemotron = sum(m.total_cost() for m in meters.values())
    sandbox = search.orch.cost.sandbox_usd
    return {"nemotron_billed_usd": round(nemotron, 6), "sandbox_reported_usd": round(sandbox, 6),
            "total_usd": round(nemotron + sandbox, 6),
            "scope": "this search; ledger extraction is included only if it shared the search's router"}


def collect(search) -> dict:
    return {"gapfinder": git_state(),
            "models": {name: t.model_id for name, t in tiers().items()},
            "prompt_sha256": prompt_hashes(),
            "harness_spec_sha256": spec_hash(search.spec),
            "cost": search_cost(search)}
