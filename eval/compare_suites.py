"""Paired per-task comparison of two code versions on the dev suite (TODO B4/§0.7 step 5).

    python eval/compare_suites.py --a eval/results/dev_suite_v13tag_a.json eval/results/dev_suite_v13tag_b.json \
                                  --b eval/results/dev_suite_run2400.json eval/results/dev_suite_run2500.json

Totals over 69 cause runs swing by about ±5 between replicates of identical code, so comparing two totals
can hide or fake an effect. This pairs by task instead:
- per task, the correct cause runs summed over each side's replicates;
- a task counts as better or worse when its sums differ;
- an exact two-sided sign test over the tasks that changed, with ties dropped.

It also reports confidently-wrong and abstention counts, which must not get worse. Free: it reads existing
results.
"""

from __future__ import annotations

import argparse
import collections
import json
from math import comb
from pathlib import Path


def per_task(files: list[Path]) -> tuple[dict[str, int], dict[str, int], collections.Counter]:
    correct: dict[str, int] = collections.Counter()
    runs: dict[str, int] = collections.Counter()
    outcomes: collections.Counter = collections.Counter()
    for f in files:
        for r in json.loads(f.read_text(encoding="utf-8"))["rows"]:
            outcomes[r["outcome"]] += 1
            if r["truth"] == "cause":
                runs[r["task"]] += 1
                correct[r["task"]] += r["outcome"] == "correct"
    return dict(correct), dict(runs), outcomes


def sign_test(wins: int, losses: int) -> float:
    """Exact two-sided sign test p-value for wins vs losses (ties dropped)."""
    n = wins + losses
    if n == 0:
        return 1.0
    k = min(wins, losses)
    p = sum(comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", nargs="+", type=Path, required=True, help="dev-suite results of version A (replicates)")
    ap.add_argument("--b", nargs="+", type=Path, required=True, help="dev-suite results of version B (replicates)")
    a = ap.parse_args()
    ca, ra, oa = per_task(a.a)
    cb, rb, ob = per_task(a.b)
    tasks = sorted(set(ra) & set(rb))
    better = [t for t in tasks if cb.get(t, 0) / rb[t] > ca.get(t, 0) / ra[t]]
    worse = [t for t in tasks if cb.get(t, 0) / rb[t] < ca.get(t, 0) / ra[t]]
    print(f"{'task':20} {'A':>7} {'B':>7}")
    for t in tasks:
        mark = " +" if t in better else " -" if t in worse else ""
        print(f"{t:20} {ca.get(t, 0):>3}/{ra[t]:<3} {cb.get(t, 0):>3}/{rb[t]:<3}{mark}")
    print(f"\ncause runs correct: A {sum(ca.values())}/{sum(ra.values())}, B {sum(cb.values())}/{sum(rb.values())}")
    print(f"tasks better {len(better)}, worse {len(worse)}, same {len(tasks) - len(better) - len(worse)}; "
          f"sign test p = {sign_test(len(better), len(worse)):.3f}")
    print(f"confidently wrong: A {oa['confidently_wrong']}, B {ob['confidently_wrong']}; "
          f"correct abstentions: A {oa['correct_abstention']}, B {ob['correct_abstention']}")


if __name__ == "__main__":
    main()
