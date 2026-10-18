"""devset informer: run Informer2020's main_informer.py unchanged, with every RNG seeded from GF_SEED.

main_informer.py has no seed flag and sets no seed, so the harness seeds python, numpy and torch (weight
init, ProbSparse key sampling, the shuffled train loader) from GF_SEED (derived from RUN_TAG by the run
command), then runs the script as __main__ with the given argv. The working directory is /work/out, so the
hard-coded ./results/ folder lands under out/.
"""
import os
import random
import runpy
import sys

import numpy as np
import torch

seed = int(os.environ.get("GF_SEED", "0"))
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)
print("gf_seed", seed, "torch", torch.__version__, "threads", torch.get_num_threads(), flush=True)
os.makedirs("/work/out", exist_ok=True)
os.chdir("/work/out")
sys.path.insert(0, "/work")
sys.argv = ["/work/main_informer.py"] + sys.argv[1:]
runpy.run_path("/work/main_informer.py", run_name="__main__")
