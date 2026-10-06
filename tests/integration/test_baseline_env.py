import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "eval" / "baseline"))
pytest.importorskip("minisweagent")

from minisweagent.exceptions import Submitted  # noqa: E402
from mini_swe_env import SandboxEnvironment  # noqa: E402

from gapfinder.sandbox.backend import LocalBackend  # noqa: E402


async def _root(be):
    return await be.base("empty")


def test_adapter_chains_linearly_and_submits(tmp_path):
    import asyncio

    be = LocalBackend(tmp_path / "sbx")
    root = asyncio.run(_root(be))
    env = SandboxEnvironment(be, root, timeout=20)
    assert env.execute({"command": "echo hi > note.txt"})["returncode"] == 0
    out = env.execute({"command": "cat note.txt"})
    assert out["output"].strip() == "hi"  # state carried from the previous command
    assert env.execute({"command": "exit 3"})["returncode"] == 3
    with pytest.raises(Submitted) as exc:
        env.execute({"command": "echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT; echo '{\"attributions\": []}'"})
    assert "attributions" in exc.value.messages[0]["content"]
    assert len(env.history) == 4 and env.cost.sandbox_runs == 4


def test_budgeted_model_records_spend_and_respects_cap(monkeypatch):
    from budgeted_model import BudgetedLitellmModel

    from gapfinder.models import budget

    # litellm's mock_response: no network, but a real response object with usage
    m = BudgetedLitellmModel(tier="super", model_kwargs={"mock_response": "ok", "api_key": "test"})
    msgs = [{"role": "user", "content": "hello"}]
    m._query(msgs)
    assert budget.spent_usd() > 0 and m._calculate_cost(None)["cost"] == budget.spent_usd()
    assert budget.entries()[-1]["source"] == "baseline"

    monkeypatch.setenv("GF_SPEND_CAP_USD", "0.000001")
    with pytest.raises(budget.BudgetExceeded):
        m._query(msgs)  # refused before sending
    assert budget.BudgetExceeded in m.abort_exceptions  # the agent's retry loop won't retry it
