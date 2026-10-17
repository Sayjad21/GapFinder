"""Build a dev-set case's base image in Token Factory Sandboxes, then run one smoke cell.

    python eval/external/devset/build_case.py <case.json>

case.json: {"name", "repo" (GitHub URL), "commit", "image" (OCI, e.g. python:3.7-slim), "pip" (list of
requirement strings), "setup" (optional shell run in /work after the install), "smoke" (shell run in
/work from the built checkpoint, with RUN_TAG set)}. The repo is fetched inside the sandbox at the commit
(an upload of the local clone timed out on blind-1), so no repository file is changed. Prints the
checkpoint id for the case's spec (its `base`).
"""
import asyncio
import json
import sys
import time

from gapfinder.config import settings
from gapfinder.models import budget
from gapfinder.sandbox.backend import ContreeBackend


def fetch(repo: str, commit: str) -> str:
    owner_repo = repo.rstrip("/").removeprefix("https://github.com/").removesuffix(".git")
    name = owner_repo.split("/")[-1]
    return ("python -c \"import io, tarfile, urllib.request; "
            f"d = urllib.request.urlopen('https://codeload.github.com/{owner_repo}/tar.gz/{commit}', timeout=300).read(); "
            "tarfile.open(fileobj=io.BytesIO(d)).extractall('/tmp/src'); print('fetched', len(d))\" "
            f"&& cp -r /tmp/src/{name}-{commit}/. /work/ && rm -rf /tmp/src && ls /work")


async def main(case: dict) -> None:
    import os

    os.environ["GF_CONTREE_LOCAL_IMAGE"] = case["image"]
    b = ContreeBackend()
    import shutil
    import tempfile

    case_dir = os.path.dirname(os.path.abspath(sys.argv[1]))
    stage = tempfile.mkdtemp(prefix="gf-case-")  # only the case's harness/ is uploaded, as /work/gf_harness/
    if os.path.isdir(os.path.join(case_dir, "harness")):
        shutil.copytree(os.path.join(case_dir, "harness"), os.path.join(stage, "gf_harness"))
    src = await b.base("local:" + stage)
    pip = " ".join(f"'{p}'" for p in case.get("pip", []))
    build = (fetch(case["repo"], case["commit"]) + "; "
             + (f"pip install -q {pip} 2>&1 | grep -v -i warning | tail -3; " if pip else "")
             + (case.get("setup", "") + "; " if case.get("setup") else "")
             + "python --version; pip freeze | head -40")
    t = time.time()
    built = await b.run(src, "cd /work && " + build, timeout=3000, disposable=False)
    print("BUILD", built.exit_code, round(time.time() - t), "s, checkpoint", built.checkpoint, flush=True)
    print(built.stdout[-3500:], built.stderr[-1500:], flush=True)
    if built.exit_code != 0 or not built.checkpoint:
        return
    if case.get("smoke"):
        for tag in ("smoke-a", "smoke-b"):
            t = time.time()
            r = await b.run(built.checkpoint, "cd /work && " + case["smoke"], env={"RUN_TAG": tag}, timeout=3600,
                            disposable=True)
            print("SMOKE", tag, r.exit_code, round(time.time() - t), "s, max_rss_kb", r.resources.max_rss_kb, flush=True)
            print(r.stdout[-2500:], r.stderr[-1500:], flush=True)
    print("CHECKPOINT", built.checkpoint)


settings()
asyncio.run(main(json.loads(open(sys.argv[1], encoding="utf-8").read())))
print("reported sandbox total", round(budget.sandbox_reported_usd(), 3))
