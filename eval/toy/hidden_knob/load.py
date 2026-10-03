"""'Load the dataset': N rows of deterministic pseudo-random values."""
import random, sys, os
n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
os.makedirs("data", exist_ok=True)
rng = random.Random(42)
with open("data/rows.txt", "w") as f:
    for _ in range(n):
        f.write(f"{rng.random():.6f}\n")
