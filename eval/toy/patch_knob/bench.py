"""Entry script: one flag; the model's lengthscale is fixed in model.py (no flag reaches it)."""
import argparse
import os

import model

p = argparse.ArgumentParser()
p.add_argument("--alpha", type=float, default=1.0)
a = p.parse_args()
m = model.model(a.alpha)
os.makedirs("out", exist_ok=True)
with open("out/run.log", "w") as fh:
    fh.write("".join(f"{k}={v}\n" for k, v in m.items()))
