"""The four core data objects. Frozen after M1: change only with a migration note.

Claim, Assumption, Branch and Attribution are what every stage passes around.
The LLM stages emit Claim/Assumption JSON that is validated against these
models; the sandbox stages produce Branch; search produces Attribution.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SCHEMA_VERSION = "1.0"


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid", use_enum_values=True)


# --------------------------------------------------------------------- Claim


class ClaimType(str, Enum):
    absolute = "absolute"  # "throughput is 120 kops/s"
    ratio = "ratio"  # "RusKey is 4x faster than RocksDB"
    trend = "trend"  # "latency falls as K rises"


class Claim(_Model):
    id: str = Field(description="Stable id, e.g. C1")
    figure_or_table: str | None = Field(description="e.g. 'Figure 6', 'Table 3', or null for prose")
    metric: str = Field(description="What is measured, e.g. 'mean latency per operation'")
    unit: str | None = None
    reported_value: float | None = Field(default=None, description="Null for pure trend claims")
    conditions: dict[str, str] = Field(default_factory=dict, description="workload, system, baseline...")
    type: ClaimType
    page: int | None = Field(default=None, description="1-based PDF page")
    quote: str = Field(description="Exact sentence or table cell the claim came from")
    headline: bool = False


# ---------------------------------------------------------------- Assumption


class Layer(str, Enum):
    build = "build"
    dataset = "dataset"  # needs a reload, but not a rebuild
    config = "config"
    workload = "workload"
    environment = "environment"


class AssumptionStatus(str, Enum):
    unstated = "unstated"
    stated_matches = "stated_matches"
    stated_code_differs = "stated_code_differs"  # paper-artifact inconsistency


class Evidence(_Model):
    kind: Literal["paper", "code", "web", "measurement"]
    ref: str = Field(description="'p.7' for paper, 'path/file.cc:123' for code, URL for web")
    quote: str = Field(description="Verbatim text at ref; the grounding checker string-matches it")


class Assumption(_Model):
    id: str
    knob: str = Field(description="Flag, option or env var name")
    layer: Layer
    paper_value: str = Field(description="Value stated in the paper, or 'unstated'")
    code_default: str | None = None
    candidate_values: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    prior_score: float = Field(ge=0.0, le=1.0, description="Prior that this knob explains a gap")
    status: AssumptionStatus = AssumptionStatus.unstated
    affects_claims: list[str] = Field(default_factory=list)


# -------------------------------------------------------------------- Branch


class BranchStatus(str, Enum):
    queued = "queued"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"  # experiment failed (non-zero exit, unparsable output)
    timed_out = "timed_out"
    infra_error = "infra_error"  # sandbox/API trouble, eligible for retry
    rejected = "rejected"  # diff guard refused it
    pruned = "pruned"
    survivor = "survivor"
    explained = "explained"


class ResourceStats(_Model):
    elapsed_s: float = 0.0
    user_cpu_s: float = 0.0
    system_cpu_s: float = 0.0
    max_rss_kb: int = 0
    block_in: int = 0
    block_out: int = 0
    involuntary_switches: int = 0
    cost_usd: float = 0.0


class Branch(_Model):
    id: str
    parent_checkpoint: str
    knob_changes: dict[str, str] = Field(default_factory=dict)
    command: str
    run_tag: str
    result_checkpoint: str | None = None
    exit_code: int | None = None
    parsed_metrics: dict[str, float] = Field(default_factory=dict)
    resources: ResourceStats = Field(default_factory=ResourceStats)
    status: BranchStatus = BranchStatus.queued
    note: str | None = None


# --------------------------------------------------------------- Attribution


class ConfidenceLabel(str, Enum):
    explained = "Explained"
    partially_explained = "Partially explained"
    fits_but_unsupported = "Fits but unsupported"
    unexplained = "Unexplained"
    inconsistency = "Paper-artifact inconsistency"


class Attribution(_Model):
    claim_id: str
    assumption_set: list[str]
    gap_before: float
    gap_after: float
    noise_band: float
    held_out_result: str | None = None
    counterfactual_ok: bool | None = None
    hypotheses_tested: int = 0
    checkpoint_ids: list[str] = Field(default_factory=list)
    confidence_label: ConfidenceLabel


class ClaimLedger(_Model):
    schema_version: str = SCHEMA_VERSION
    paper: str
    claims: list[Claim]


class AssumptionSpace(_Model):
    schema_version: str = SCHEMA_VERSION
    paper: str
    repo: str
    assumptions: list[Assumption]
