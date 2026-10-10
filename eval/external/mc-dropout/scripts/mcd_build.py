import asyncio, json, os, sys, time
from gapfinder.config import settings
from gapfinder.sandbox.backend import ContreeBackend
from gapfinder.models import budget

ENV = {"KERAS_BACKEND": "theano", "THEANO_FLAGS": "device=cpu,floatX=float32"}
BUILD = ("apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq g++ >/dev/null 2>&1 && echo gxx-ok; "
         "pip install -q 'numpy==1.13.3' 'scipy==1.1.0' 'theano==0.8.2' 'keras==2.2.0' 'h5py==2.8.0' pyyaml 2>&1 | grep -v WARNING | tail -3; "
         "python -c 'import numpy, scipy, theano, keras; from scipy.misc import logsumexp; print(\"versions\", numpy.__version__, scipy.__version__, theano.__version__, keras.__version__)' 2>&1 | tail -2; pip freeze")
RUN = ("cd /work && echo 2 > UCI_Datasets/yacht/data/n_splits.txt && s=$(date +%s) && "
       "python experiment.py --dir yacht --epochx 1 --hidden 1 2>&1 | grep -v Warning | tail -5; "
       "e=$(date +%s); echo WALL=$((e-s)); cat UCI_Datasets/yacht/results/log_1_xepochs_1_hidden_layers.txt")

async def main():
    os.environ["GF_CONTREE_LOCAL_IMAGE"] = "python:3.6-slim"
    b = ContreeBackend()
    src = await b.base("local:" + sys.argv[1])
    t = time.time()
    built = await b.run(src, BUILD, env=ENV, timeout=900, disposable=False)
    print("BUILD", built.exit_code, round(time.time() - t), "s, cost", built.resources.cost_usd, "checkpoint", built.checkpoint)
    print(built.stdout[-2500:], built.stderr[-800:])
    if built.exit_code != 0 or "versions" not in built.stdout:
        return
    t = time.time()
    r = await b.run(built.checkpoint, RUN, env=ENV, timeout=1800, disposable=True)
    print("RUN", r.exit_code, round(time.time() - t), "s, cost", r.resources.cost_usd, "cpu", r.resources.user_cpu_s)
    print(r.stdout[-2500:], r.stderr[-1500:])

settings()
asyncio.run(main())
print("reported sandbox total", round(budget.sandbox_reported_usd(), 3))
