"""LocalBackend with a Docker image as the base: runs happen in containers of that image.

Needs Docker and the MC Dropout image (docker build -t gf-mcdropout -f docker/Dockerfile .,
from eval/external/mc-dropout); skipped otherwise.
"""

import shutil
import subprocess

import pytest

from gapfinder.sandbox.backend import LocalBackend

IMAGE = "gf-mcdropout"


def _have_image() -> bool:
    if not shutil.which("docker"):
        return False
    try:
        return subprocess.run(["docker", "image", "inspect", IMAGE], capture_output=True, timeout=30).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


pytestmark = pytest.mark.skipif(not _have_image(), reason=f"Docker image {IMAGE} not available")


async def test_runs_in_the_image_and_keeps_files_between_runs(tmp_path):
    be = LocalBackend(tmp_path / "sbx")
    src = await be.base(f"docker:{IMAGE}")
    first = await be.run(src, "python --version; echo $WORK; echo kept > out_marker.txt; ls experiment.py", env={"X": "1"})
    assert first.exit_code == 0, first.stderr
    assert "Python 3.6" in first.stdout + first.stderr  # the image's python, not the host's
    assert "/work" in first.stdout
    second = await be.run(first.checkpoint, "cat out_marker.txt; echo $X", disposable=True)
    assert second.stdout.split() == ["kept"]  # env is per run; files persist in the checkpoint


async def test_timeout_kills_the_container(tmp_path):
    be = LocalBackend(tmp_path / "sbx")
    src = await be.base(f"docker:{IMAGE}")
    res = await be.run(src, "sleep 600", timeout=5, disposable=True)
    assert res.timed_out
    running = subprocess.run(["docker", "ps", "-q", "--filter", "name=gf-"], capture_output=True, text=True).stdout
    assert running.strip() == ""
