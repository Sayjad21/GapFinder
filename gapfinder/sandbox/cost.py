"""Cost meter: sandbox dollars from each result plus tokens per Nemotron tier."""

from __future__ import annotations

from dataclasses import dataclass, field

from gapfinder.models import budget
from gapfinder.models.router import TokenMeter


class BudgetExceeded(RuntimeError):
    pass


@dataclass
class CostMeter:
    cap_usd: float | None = None
    sandbox_usd: float = 0.0
    sandbox_runs: int = 0
    setup_runs: int = 0  # builds and loads -- the expensive ones forking avoids
    tokens: TokenMeter = field(default_factory=TokenMeter)

    def add_run(self, cost_usd: float, *, setup: bool = False) -> None:
        if cost_usd:
            budget.record("sandbox", cost_usd, setup=setup)
        self.sandbox_usd += cost_usd
        self.sandbox_runs += 1
        self.setup_runs += int(setup)

    @property
    def total_usd(self) -> float:
        return self.sandbox_usd + self.tokens.total_cost()

    def remaining(self) -> float:
        return float("inf") if self.cap_usd is None else self.cap_usd - self.total_usd

    def check(self) -> None:
        if self.cap_usd is not None and self.total_usd >= self.cap_usd:
            raise BudgetExceeded(f"spent ${self.total_usd:.4f} of ${self.cap_usd:.2f} cap")

    def summary(self) -> dict:
        return {
            "sandbox_usd": round(self.sandbox_usd, 6),
            "sandbox_runs": self.sandbox_runs,
            "setup_runs": self.setup_runs,
            "tokens": self.tokens.summary(),
            "total_usd": round(self.total_usd, 6),
            "cap_usd": self.cap_usd,
        }
