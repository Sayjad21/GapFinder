import json

import pytest

from gapfinder.ledger.schemas import (
    Assumption,
    Attribution,
    Branch,
    Claim,
    ConfidenceLabel,
    Evidence,
)
from gapfinder.models.router import (
    BadJSONError,
    EmptyAnswerError,
    ResponseCache,
    Router,
    extract_json,
    split_reasoning,
)

# ------------------------------------------------------------ schema round-trip

SAMPLES = [
    Claim(id="C1", figure_or_table="Figure 6", metric="mean latency", unit="us/op", reported_value=126.5,
          conditions={"workload": "write-heavy"}, type="absolute", page=12, quote="RusKey reduces latency"),
    Assumption(id="A1", knob="write_buffer_size", layer="config", paper_value="2 MB", code_default="64 MB",
               candidate_values=["2097152"], prior_score=0.7, status="stated_code_differs",
               evidence=[Evidence(kind="code", ref="include/rocksdb/options.h:12", quote="write_buffer_size")]),
    Branch(id="B0001", parent_checkpoint="abc", knob_changes={"alpha": "2.0"}, command="x", run_tag="t1"),
    Attribution(claim_id="C1", assumption_set=["A1"], gap_before=0.3, gap_after=0.02, noise_band=0.01,
                confidence_label=ConfidenceLabel.explained),
]


@pytest.mark.parametrize("obj", SAMPLES, ids=lambda o: type(o).__name__)
def test_schema_round_trip(obj):
    again = type(obj).model_validate_json(obj.model_dump_json())
    assert again == obj
    assert type(obj).model_validate(json.loads(json.dumps(obj.model_dump()))) == obj


def test_schema_rejects_extra_fields():
    with pytest.raises(Exception):
        Claim.model_validate({**SAMPLES[0].model_dump(), "surprise": 1})


# --------------------------------------------------------- reasoning handling


def test_split_reasoning_think_wrapped():
    r, a = split_reasoning('<think>let me see</think>{"x": 1}')
    assert r == "let me see" and a == '{"x": 1}'


def test_split_reasoning_separate_field():
    r, a = split_reasoning('{"x": 1}', "trace")
    assert r == "trace" and a == '{"x": 1}'


def test_split_reasoning_unterminated_is_empty_answer():
    r, a = split_reasoning("<think>I ran out of tokens while thin")
    assert a == "" and "ran out" in r


def test_split_reasoning_closing_tag_only():
    r, a = split_reasoning('reasoning text</think>\n{"x": 2}')
    assert a == '{"x": 2}' and "reasoning text" in r


def test_extract_json_variants():
    assert extract_json('```json\n{"a": 1}\n```') == {"a": 1}
    assert extract_json('Sure! here: {"a": [1,2]} done') == {"a": [1, 2]}
    with pytest.raises(EmptyAnswerError):
        extract_json("   ")
    with pytest.raises(BadJSONError):
        extract_json("no json here")


def _fake(responses):
    calls = []

    async def transport(model, messages, max_tokens, response_format):
        calls.append({"model": model, "max_tokens": max_tokens, "rf": response_format})
        content = responses[min(len(calls) - 1, len(responses) - 1)]
        return {"choices": [{"message": {"content": content}}],
                "usage": {"prompt_tokens": 100, "completion_tokens": 50}}

    return transport, calls


async def test_router_doubles_budget_on_empty_answer(tmp_path):
    transport, calls = _fake(["<think>long reasoning, no answer", '<think>ok</think>{"metric": "x", "value": 1}'])
    r = Router(transport=transport, cache=ResponseCache(tmp_path))
    _, answer, _ = await r.complete("nano", [{"role": "user", "content": "hi"}])
    assert json.loads(answer)["value"] == 1
    assert calls[1]["max_tokens"] == 2 * calls[0]["max_tokens"]


async def test_router_never_returns_silent_empty(tmp_path):
    transport, _ = _fake(["<think>never finishes"])
    r = Router(transport=transport, cache=ResponseCache(tmp_path))
    with pytest.raises(EmptyAnswerError):
        await r.complete("nano", [{"role": "user", "content": "hi"}])


async def test_router_cache_hit_is_free_and_identical(tmp_path):
    transport, calls = _fake(['{"id": "C1"}'])
    r = Router(transport=transport, cache=ResponseCache(tmp_path))
    msgs = [{"role": "user", "content": "same"}]
    a1 = await r.complete("super", msgs)
    a2 = await r.complete("super", msgs)
    assert a1[1] == a2[1] and len(calls) == 1
    s = r.meter.summary()["super"]
    assert s["calls"] == 2 and s["cached_calls"] == 1
    assert r.meter.total_fresh_cost() == pytest.approx(2 * r.meter.total_cost())  # the hit counts at full price
    assert s["cost_usd"] == pytest.approx((100 * 0.30 + 50 * 0.90) / 1e6)


async def test_structured_repairs_once(tmp_path):
    from pydantic import BaseModel

    class Out(BaseModel):
        n: int

    transport, calls = _fake(['{"n": "not a number"}', '{"n": 3}'])
    r = Router(transport=transport, cache=ResponseCache(tmp_path))
    out = await r.structured("nano", [{"role": "user", "content": "q"}], Out)
    assert out.n == 3 and len(calls) == 2


async def test_budget_refuses_call_that_could_cross_cap(tmp_path, monkeypatch):
    from gapfinder.models import budget

    monkeypatch.setenv("GF_SPEND_CAP_USD", "0.01")
    transport, calls = _fake(['{"x": 1}'])
    r = Router(transport=transport, cache=ResponseCache(tmp_path))
    # ultra worst case: 32768 output tokens x $3/M = ~$0.098 > $0.01 cap
    with pytest.raises(budget.BudgetExceeded):
        await r.complete("ultra", [{"role": "user", "content": "hi"}])
    assert calls == []  # refused before any request was sent


async def test_spend_is_recorded_and_doubling_happens_once(tmp_path):
    from gapfinder.models import budget

    transport, calls = _fake(["<think>no answer"])
    r = Router(transport=transport, cache=ResponseCache(tmp_path))
    with pytest.raises(EmptyAnswerError):
        await r.complete("nano", [{"role": "user", "content": "hi"}])
    assert len(calls) == 2 and calls[1]["max_tokens"] == 2 * calls[0]["max_tokens"]
    assert budget.spent_usd() == pytest.approx(2 * (100 * 0.06 + 50 * 0.24) / 1e6)


async def test_fatal_errors_not_retried(tmp_path):
    class Unauthorized(Exception):
        status_code = 401

    n = {"calls": 0}

    async def transport(*a):
        n["calls"] += 1
        raise Unauthorized("invalid api key")

    r = Router(transport=transport, cache=ResponseCache(tmp_path))
    with pytest.raises(Unauthorized):
        await r.complete("nano", [{"role": "user", "content": "hi"}])
    assert n["calls"] == 1


async def test_cache_only_mode_never_calls_api(tmp_path, monkeypatch):
    from gapfinder.models.router import CacheMiss

    monkeypatch.setenv("GF_CACHE_ONLY", "1")
    transport, calls = _fake(['{"x": 1}'])
    r = Router(transport=transport, cache=ResponseCache(tmp_path))
    with pytest.raises(CacheMiss):
        await r.complete("nano", [{"role": "user", "content": "hi"}])
    assert calls == []


def test_tagged_project_cap(monkeypatch):
    from gapfinder.models import budget

    monkeypatch.setenv("GF_SPEND_CAP_USD", "100")
    budget.record("sandbox", 3.0)  # untagged spend doesn't count against the project
    monkeypatch.setenv("GF_SPEND_TAG", "ruskey")
    monkeypatch.setenv("GF_TAG_CAP_USD", "8")
    budget.record("sandbox", 7.5)
    assert budget.tag_spent_usd("ruskey") == 7.5
    budget.check(0.4, "ok")
    with pytest.raises(budget.BudgetExceeded):
        budget.check(0.6, "over the project cap")


def test_sandbox_cost_has_its_own_guard_not_the_billing_cap(monkeypatch):
    from gapfinder.models import budget

    monkeypatch.setenv("GF_SPEND_CAP_USD", "1.0")
    monkeypatch.setenv("GF_SANDBOX_GUARD_USD", "10")
    budget.record("sandbox", 5.0)  # reported, not billed
    budget.check(0.5, "llm call")  # the billing cap ignores sandbox-reported cost
    budget.check(0.0, "sandbox run", kind="sandbox")
    budget.record("sandbox", 6.0)
    with pytest.raises(budget.BudgetExceeded):
        budget.check(0.0, "sandbox run", kind="sandbox")


async def test_failed_call_is_recorded_as_unconfirmed(tmp_path):
    from gapfinder.models import budget

    async def boom(*a):
        raise TimeoutError("read timeout")

    r = Router(transport=boom, cache=ResponseCache(tmp_path))
    with pytest.raises(TimeoutError):
        await r.complete("nano", [{"role": "user", "content": "x" * 3000}])
    unconfirmed = [e for e in budget.entries() if e["kind"] == "llm_unconfirmed"]
    assert len(unconfirmed) == 4 and budget.spent_usd() > 0


async def test_filter_claims_drops_non_results_and_keeps_unjudged(tmp_path):
    from gapfinder.ingest.pdf import FigureCrop, Page, PaperText
    from gapfinder.ledger.claims import filter_claims

    verdicts = '{"verdicts": [{"id": "C1", "result": true, "why": "measured"}, {"id": "C2", "result": false, "why": "setup"}]}'
    transport, calls = _fake([verdicts])
    r = Router(transport=transport, cache=ResponseCache(tmp_path))
    paper = PaperText(path=tmp_path / "p.pdf", pages=[Page(1, "x")],
                      figures=[FigureCrop(label="Figure 2", page=1, caption="Figure 2: a simplified example")])
    claims = [Claim(id=i, figure_or_table=None, metric="m", type="trend", quote=f"q{i}") for i in ("C1", "C2", "C3")]
    kept, dropped = await filter_claims(r, paper, claims)
    assert [c.id for c in kept] == ["C1", "C3"]  # C3 wasn't judged: kept, never silently dropped
    assert dropped == [("C2", "not a result: setup")]
