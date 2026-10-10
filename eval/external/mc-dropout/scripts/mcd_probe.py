import asyncio, json
from gapfinder.config import settings
from gapfinder.sandbox.backend import ContreeBackend
from gapfinder.models import budget

PROBE = ("python --version 2>&1; nproc; "
         "timeout 60 pip download -q --no-deps -d /tmp/x theano==0.8.2 2>&1 | tail -2; ls /tmp/x 2>&1; "
         "timeout 20 python -c \"import urllib.request as u; print('pypi', u.urlopen('https://pypi.org/simple/').status)\" 2>&1 | tail -1")

async def main():
    b = ContreeBackend()
    cid = await b.base("python:3.6-slim")
    r = await b.run(cid, PROBE, timeout=180, disposable=True)
    print(json.dumps({"base": cid, "exit": r.exit_code, "stdout": r.stdout[-1500:], "stderr": r.stderr[-600:],
                      "cost": r.resources.cost_usd}, indent=1))

settings()
asyncio.run(main())
print("reported sandbox total", round(budget.sandbox_reported_usd(), 3))
