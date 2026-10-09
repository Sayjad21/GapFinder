"""Browser test of the judge path (plan M5), on both sites: the FastAPI server and the static
build for GitHub Pages. Needs `npm --prefix web run build`, the static build (see
.github/workflows/pages.yml) and `python -m playwright install chromium`.
Run with: pytest -m e2e tests/e2e"""

import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

pytestmark = pytest.mark.e2e
ROOT = Path(__file__).resolve().parents[2]


def _port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait(port: int) -> None:
    for _ in range(50):
        try:
            socket.create_connection(("127.0.0.1", port), timeout=0.2).close()
            return
        except OSError:
            time.sleep(0.2)


@pytest.fixture(scope="module", params=["api", "static"])
def server(request, tmp_path_factory):
    port = _port()
    if request.param == "api":
        if not (ROOT / "web" / "dist" / "index.html").exists():
            pytest.skip("web/dist not built")
        cmd, url = [sys.executable, "-m", "uvicorn", "gapfinder.api.server:app", "--port", str(port),
                    "--log-level", "warning"], f"http://127.0.0.1:{port}"
    else:  # served under a sub-path, as GitHub Pages serves the repo's site
        site = ROOT / "web" / "dist-static"
        if not (site / "data" / "runs.json").exists():
            pytest.skip("static site not built")
        root = tmp_path_factory.mktemp("pages")
        shutil.copytree(site, root / "GapFinder")
        cmd, url = [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1",
                    "--directory", str(root)], f"http://127.0.0.1:{port}/GapFinder/"
    proc = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    _wait(port)
    yield url
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
        await phone.goto(f"{server.rstrip('/')}/#/report/")
        await phone.wait_for_selector(".card", timeout=15000)
        assert await phone.evaluate("document.documentElement.scrollWidth") <= 390  # readable on a phone
        assert errors == []
        await b.close()
