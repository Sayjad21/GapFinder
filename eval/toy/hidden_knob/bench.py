"""Hidden-knob toy benchmark. Output depends on flags, env vars, build and data.

Planted gap: the 'paper' ran with --alpha 2.0; the code default is 1.0.
"""
import argparse, hashlib, os, random

p = argparse.ArgumentParser()
p.add_argument("--alpha", type=float, default=1.0)   # the planted default
p.add_argument("--beta", type=float, default=0.5)    # decoy: moves score the wrong way
p.add_argument("--gamma", type=float, default=1.0)   # only matters together with CACHE=on
p.add_argument("--noise", type=float, default=0.0)   # injected noise sigma (fraction)
p.add_argument("--threads", type=int, default=1)     # no effect on any metric (bisect must drop it)
p.add_argument("--crash", action="store_true")
p.add_argument("--hang", action="store_true")
p.add_argument("--garbage", action="store_true")
a = p.parse_args()
if a.crash:
    raise SystemExit("segfault (simulated)")
if a.hang:
    import time; time.sleep(3600)
rows = [float(x) for x in open("data/rows.txt")]
mode = open("build/mode.txt").read().strip()
speed = 3.0 if mode == "release" else 1.0
cache = os.environ.get("CACHE", "off") == "on"
score = 100 * a.alpha * speed * (sum(rows) / len(rows)) / (1 + a.beta)
if cache:
    score *= a.gamma
write_amp = 10.0 / a.alpha + (2.0 if not cache else 0.5)
seed = int(hashlib.sha256(os.environ.get("RUN_TAG", "x").encode()).hexdigest()[:8], 16)
rng = random.Random(seed)
score *= 1 + rng.gauss(0, a.noise)
os.makedirs("out", exist_ok=True)
with open("out/run.log", "w") as f:
    if a.garbage:
        f.write("Segmentation fault (core dumped)\n")
    else:
        f.write(f"rows: {len(rows)}\nscore: {score:.4f}\nwrite_amp: {write_amp:.4f}\n")
print(open("out/run.log").read())
