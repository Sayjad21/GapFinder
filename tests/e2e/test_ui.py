"""Browser test of the judge path (plan M5). Needs `npm --prefix web run build` and
`python -m playwright install chromium`. Run with: pytest -m e2e tests/e2e"""

import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

pytestmark = pytest.mark.e2e
ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def server():
    if not (ROOT / "web" / "dist" / "index.html").exists():
        pytest.skip("web/dist not built")
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "gapfinder.api.server:app", "--port", str(port),
                             "--log-level", "warning"], cwd=ROOT)
    for _ in range(50):
        try:
            socket.create_connection(("127.0.0.1", port), timeout=0.2).close()
            break
        except OSError:
            time.sleep(0.2)
    yield f"http://127.0.0.1:{port}"
    proc.terminate()


async def test_judge_path_replay_report_scoreboard_and_phone(server):
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 1400, "height": 900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.goto(server)  # lands on replay of the first featured run
        await page.wait_for_selector("text=REPLAY", timeout=15000)
        await page.click("text=16×")
        await page.wait_for_selector("text=finished", timeout=90000)
        assert await page.locator(".verdict").count() >= 1  # replay ends on the run's verdict
        await page.click("text=Gap Report")
        await page.wait_for_selector(".card", timeout=15000)
        await page.click("text=Scoreboard")
        await page.wait_for_selector("table", timeout=15000)
        phone = await b.new_page(viewport={"width": 390, "height": 844})
        await phone.goto(f"{server}/#/report/")
        await phone.wait_for_selector(".card", timeout=15000)
        assert await phone.evaluate("document.documentElement.scrollWidth") <= 390  # readable on a phone
        assert errors == []
        await b.close()
