"""mini-swe-agent's litellm model, wired into GapFinder's spend ledger and cap.

Without this, the baseline would bypass the cap entirely: litellm doesn't know
Token Factory prices, so the agent's own cost_limit would see $0 per call and
never trigger. Here every call is checked against GF_SPEND_CAP_USD before it
is sent, recorded at Token Factory list prices after, and reported to the
agent as its real cost, so `cost_limit` gives both arms the same dollar cap.
"""

from __future__ import annotations

from minisweagent.models.litellm_model import LitellmModel

from gapfinder.config import settings, tiers
from gapfinder.models import budget


class BudgetedLitellmModel(LitellmModel):
    abort_exceptions = [*LitellmModel.abort_exceptions, budget.BudgetExceeded]

    def __init__(self, *, tier: str = "super", **kwargs):
        self.tier = tiers()[tier]
        s = settings()
        kwargs.setdefault("model_name", f"openai/{self.tier.model_id}")
        model_kwargs = dict(kwargs.pop("model_kwargs", {}))
        model_kwargs.setdefault("api_base", s.token_factory_base_url)
        model_kwargs.setdefault("api_key", s.token_factory_api_key)
        model_kwargs.setdefault("max_tokens", self.tier.max_tokens)
        kwargs["model_kwargs"] = model_kwargs
        kwargs.setdefault("cost_tracking", "ignore_errors")
        super().__init__(**kwargs)
        self._last_cost = 0.0

    def _query(self, messages, **kwargs):
        max_out = {**self.config.model_kwargs, **kwargs}.get("max_tokens", self.tier.max_tokens)
        worst = (budget.estimate_prompt_tokens(messages) * self.tier.price_in + max_out * self.tier.price_out) / 1e6
        budget.check(worst, f"baseline {self.tier.name} call")
        try:
            response = super()._query(messages, **kwargs)
        except Exception as exc:  # may have been billed without a response: record the input cost
            est = budget.estimate_prompt_tokens(messages) * self.tier.price_in / 1e6
            budget.record("llm_unconfirmed", est, tier=self.tier.name, model=self.tier.model_id,
                          source="baseline", error=type(exc).__name__)
            raise
        usage = getattr(response, "usage", None)
        p_tok = getattr(usage, "prompt_tokens", 0) or 0
        c_tok = getattr(usage, "completion_tokens", 0) or 0
        self._last_cost = (p_tok * self.tier.price_in + c_tok * self.tier.price_out) / 1e6
        budget.record("llm", self._last_cost, tier=self.tier.name, model=self.tier.model_id,
                      prompt_tokens=p_tok, completion_tokens=c_tok, source="baseline")
        return response

    def _calculate_cost(self, response) -> dict[str, float]:
        return {"cost": self._last_cost}
