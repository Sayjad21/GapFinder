"""blind-1: build the FastGCN base image in Token Factory Sandboxes and run one smoke cell."""
import asyncio, os, shutil, sys, time
from pathlib import Path

from gapfinder.config import settings
from gapfinder.sandbox.backend import ContreeBackend
from gapfinder.models import budget

HERE = Path(__file__).parent
REPO = Path(sys.argv[1])          # gapfinder repo
STAGE = HERE / "stage"

SHA = "b8e6e6412d8cb696e0adb7910832ed1ae7243ac9"
FETCH = ("python -c \"import io, tarfile, urllib.request; "
         "d = urllib.request.urlopen('https://codeload.github.com/matenure/FastGCN/tar.gz/" + SHA + "', timeout=300).read(); "
         "t = tarfile.open(fileobj=io.BytesIO(d)); t.extractall('/tmp/src'); print('fetched', len(d))\" "
         "&& cp -r /tmp/src/FastGCN-" + SHA + "/. /work/ && rm -rf /tmp/src && ls /work | head -40 && ls /work/data | wc -l; ")
BUILD = FETCH + (
    "pip install -q 'tensorflow==1.15.5' 'numpy==1.18.5' 'scipy==1.4.1' 'networkx==2.4' 'protobuf==3.20.3' 2>&1 "
    "| grep -v -i warning | tail -3; "
    "SP=$(python -c 'import site; print(site.getsitepackages()[0])') && cp gf_harness/gf_seed_hook.py gf_harness/gf_seed.pth \"$SP\"/ "
    "&& echo hook-installed \"$SP\"; "
    "python -c 'import tensorflow as tf, numpy, scipy, networkx; from scipy.sparse.linalg.eigen.arpack import eigsh; "
    "print(\"versions\", tf.__version__, numpy.__version__, scipy.__version__, networkx.__version__)' 2>&1 | tail -1; "
    "python --version; pip freeze"
)


def cell(**kw):
    a = " ".join(f"--{k} {v}" for k, v in kw.items())
    runs = " ".join(
        f"python pubmed-original_{s}_FastGCN.py --dataset {d} {a} > out/{t}_{d}.log 2>&1 &"
        for s, t in (("transductive", "trans"), ("inductive", "ind")) for d in ("cora", "pubmed"))
    return ("export GF_SEED_FROM_RUN_TAG=1 OMP_NUM_THREADS=1 TF_CPP_MIN_LOG_LEVEL=2; mkdir -p out; "
            f"{runs} wait; bash gf_harness/emit.sh")


async def main():
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir()
    shutil.copytree(REPO / "eval/external/blind-1/harness", STAGE / "gf_harness")
    os.environ["GF_CONTREE_LOCAL_IMAGE"] = "python:3.7-slim"
    b = ContreeBackend()
    t = time.time()
    src = await b.base("local:" + str(STAGE))
    print("BASE", src, round(time.time() - t), "s")
    t = time.time()
    built = await b.run(src, "cd /work && " + BUILD, timeout=1800, disposable=False)
    print("BUILD", built.exit_code, round(time.time() - t), "s, cost", built.resources.cost_usd, "checkpoint", built.checkpoint)
    print(built.stdout[-3000:], built.stderr[-1500:])
    if built.exit_code != 0 or "versions 1.15" not in built.stdout:
        return
    defaults = dict(model="gcn_mix", learning_rate=0.01, epochs=100, hidden1=16, dropout=0.0,
                    weight_decay=5e-4, early_stopping=10, max_degree=3)
    for tag in ("smoke-a", "smoke-b"):
        t = time.time()
        r = await b.run(built.checkpoint, "cd /work && " + cell(**defaults), env={"RUN_TAG": tag},
                        timeout=1800, disposable=True)
        print("RUN", tag, r.exit_code, round(time.time() - t), "s, cost", r.resources.cost_usd)
        print(r.stdout[-2000:], r.stderr[-2500:])


settings()
asyncio.run(main())
print("reported sandbox total", round(budget.sandbox_reported_usd(), 3))
