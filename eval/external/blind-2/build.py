"""blind-2: build the GraphMAE base image in Token Factory Sandboxes, then time one default run per dataset.

    python eval/external/blind-2/build.py <gapfinder repo> [timing]

The timing pass runs the README configuration (one seed) of every Table 2 dataset, one at a time, so the
cell can be scoped by run time before the search (HARNESS.md). Its accuracies are printed but not used to
choose anything.
"""
import asyncio
import os
import shutil
import sys
import time
from pathlib import Path

from gapfinder.config import settings
from gapfinder.models import budget
from gapfinder.sandbox.backend import ContreeBackend

REPO = Path(sys.argv[1])
HERE = Path(__file__).parent
STAGE = Path(os.environ.get("GF_B2_STAGE", HERE / "stage"))
SHA = "1be594160bb7c1fde0d16ced6af1e88b53612e49"
DATASETS = ["COLLAB", "IMDB-BINARY", "IMDB-MULTI", "PROTEINS", "MUTAG", "REDDIT-BINARY", "NCI1"]

FETCH = ("python -c \"import io, tarfile, urllib.request; "
         "d = urllib.request.urlopen('https://codeload.github.com/THUDM/GraphMAE/tar.gz/" + SHA + "', timeout=300).read(); "
         "t = tarfile.open(fileobj=io.BytesIO(d)); t.extractall('/tmp/src'); print('fetched', len(d))\" "
         "&& cp -r /tmp/src/GraphMAE-" + SHA + "/. /work/ && rm -rf /tmp/src && ls /work; ")
BUILD = FETCH + (
    "pip install -q 'torch==1.13.1+cpu' --extra-index-url https://download.pytorch.org/whl/cpu 2>&1 | tail -2; "
    "pip install -q 'dgl==0.9.1' 'numpy<2' 'scipy<1.12' 'scikit-learn<1.4' 'pyyaml==6.0.1' tqdm tensorboardX ogb 2>&1 | tail -2; "
    "python -c 'import torch, dgl, numpy, sklearn, yaml; print(\"versions\", torch.__version__, dgl.__version__, "
    "numpy.__version__, sklearn.__version__, yaml.__version__)' 2>&1 | tail -1; "
    "python -c \"from dgl.data import TUDataset; [print(n, len(TUDataset(n))) for n in " + repr(DATASETS) + "]\" 2>&1 | tail -8; "
    "python --version; pip freeze | head -60"
)


def run_one(ds, seed=0):
    return ("cd /work && export OMP_NUM_THREADS=4; mkdir -p out; F=\"$(cat gf_harness/run_graph_flags)\"; s=$(date +%s); "
            f"python main_graph.py --device -1 --dataset {ds} $F --seeds {seed} > out/{ds}.log 2>&1; "
            f"echo gf_wall_s=$(( $(date +%s) - s )) >> out/{ds}.log; bash gf_harness/emit.sh; tail -3 out/{ds}.log")


async def main():
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    shutil.copytree(REPO / "eval/external/blind-2/harness", STAGE / "gf_harness")
    os.environ["GF_CONTREE_LOCAL_IMAGE"] = "python:3.10-slim"
    b = ContreeBackend()
    src = await b.base("local:" + str(STAGE))
    t = time.time()
    built = await b.run(src, "cd /work && " + BUILD, timeout=3600, disposable=False)
    print("BUILD", built.exit_code, round(time.time() - t), "s, checkpoint", built.checkpoint, flush=True)
    print(built.stdout[-4000:], built.stderr[-2000:], flush=True)
    if built.exit_code != 0 or "versions 1.13.1" not in built.stdout:
        return
    if "timing" not in sys.argv:
        return
    rs = await asyncio.gather(*(b.run(built.checkpoint, run_one(ds), env={"RUN_TAG": "timing"}, timeout=3600,
                                      disposable=True) for ds in DATASETS), return_exceptions=True)
    for ds, r in zip(DATASETS, rs):
        if isinstance(r, Exception):
            print("TIMING", ds, "error", r, flush=True)
            continue
        print("TIMING", ds, "exit", r.exit_code, "elapsed_s", r.resources.elapsed_s, flush=True)
        print(r.stdout[-600:], r.stderr[-800:], flush=True)


settings()
asyncio.run(main())
print("reported sandbox total", round(budget.sandbox_reported_usd(), 3))
