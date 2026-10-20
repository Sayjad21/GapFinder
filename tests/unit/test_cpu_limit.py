"""Plan D6.3: unset, the per-process CPU-time limit follows the run's timeout (a fixed 300 s killed long runs)."""

import asyncio

from gapfinder.sandbox import backend as B


class _Res:
    resources = type("R", (), {"cost_usd": 0.0, "elapsed_s": 0.0, "user_cpu_s": 0.0, "system_cpu_s": 0.0})()


def _shell_for(monkeypatch, timeout, env_value=None):
    seen = {}

    async def fake_run(self, parent, shell, **kw):
        seen["shell"] = shell
        return _Res()

    monkeypatch.setattr(B.ContreeBackend, "_run", fake_run)
    monkeypatch.setattr(B.budget, "check", lambda *a, **k: None)
    if env_value is None:
        monkeypatch.delenv("GF_SANDBOX_CPU_LIMIT_S", raising=False)
    else:
        monkeypatch.setenv("GF_SANDBOX_CPU_LIMIT_S", env_value)
    b = B.ContreeBackend.__new__(B.ContreeBackend)
    asyncio.run(b.run("p", "echo hi", timeout=timeout))
    return seen["shell"]


def test_the_cpu_limit_follows_the_timeout(monkeypatch):
    assert _shell_for(monkeypatch, 3300).startswith(f"ulimit -t {int(3300 * 4 * 1.2)};")
    assert _shell_for(monkeypatch, 10).startswith("ulimit -t 300;")  # never below the old floor
    assert _shell_for(monkeypatch, 3300, "999").startswith("ulimit -t 999;")  # an explicit setting wins
