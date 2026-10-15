"""Entry script with a hard-coded constant (patch knobs: a literal in the script the command runs)."""
import argparse
import os
tau = 1.5

p = argparse.ArgumentParser()
p.add_argument("--alpha", type=float, default=1.0)
a = p.parse_args()
os.makedirs("out", exist_ok=True)
with open("out/run.log", "w") as fh:
    fh.write(f"score={100.0 * a.alpha * tau}\naux={50.0 * tau * tau}\n")
