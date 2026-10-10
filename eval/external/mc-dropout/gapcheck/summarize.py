"""Summarise the gap check: defaults (epochx 500, hidden 2) vs ICML Table 1, from the per-split
result files that experiment.py writes. Usage: python summarize.py [dataset ...]

Each <dataset>_defaults_offset<k>/ folder is one repeat: the same code run on a disjoint set of
the repo's train/test splits (the code seeds everything, so repeating the same splits is
bit-identical). Files hold one number per split. Paper numbers: ICML 2016 Table 1, dropout RMSE
(mean, "std. error" column, which the arXiv version later corrects to a standard deviation).
"""
import math
import statistics as st
import sys
from pathlib import Path

PAPER = {"yacht": (1.11, 0.38), "energy": (1.66, 0.19), "concrete": (5.23, 0.53)}
HERE = Path(__file__).resolve().parent


def load(path):
    return [float(x) for x in path.read_text().split()]


for ds in sys.argv[1:] or PAPER:
    repeats = sorted(p for p in HERE.glob(f"{ds}_defaults_offset*") if p.is_dir())
    if not repeats:
        continue
    per_repeat, every = [], []
    for r in repeats:
        v = load(r / "test_MC_rmse.txt")
        per_repeat.append(st.mean(v))
        every += v
    mean = st.mean(every)
    sd = st.stdev(every) if len(every) > 1 else float("nan")
    se = sd / math.sqrt(len(every))
    rep_sd = st.stdev(per_repeat) if len(per_repeat) > 1 else float("nan")
    paper, paper_sd = PAPER[ds]
    print(f"{ds}: {len(repeats)} repeats x {len(load(repeats[0] / 'test_MC_rmse.txt'))} splits")
    print(f"  repeat means          {['%.3f' % m for m in per_repeat]}  sd between repeats {rep_sd:.3f}")
    print(f"  all {len(every)} splits       mean {mean:.3f}  sd {sd:.3f}  se {se:.3f}")
    print(f"  paper (Table 1)       {paper:.2f}  (listed +- {paper_sd})")
    print(f"  defaults - paper      {mean - paper:+.3f}  ({(mean - paper) / paper:+.1%}),"
          f" {abs(mean - paper) / rep_sd:.1f} x repeat sd, {abs(mean - paper) / se:.1f} x split se")
