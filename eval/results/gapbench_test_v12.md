# GapBench sealed test on GapFinder v1.2 (2026-10-15)

**Protocol** (pre-registered in `eval/gapbench/PROTOCOL.md`, "Amendment for the v1.2 sealed test"):
- GapFinder was frozen at tag `v1.2`, and the seed was made after the tag;
- 10 generated tasks, `test-v12-01` to `-10` (6 mlbench, 4 rlbench);
- 5 arms × 3 runs, through `run_arms.py`;
- answers sealed until scoring. The hash `cf836e88…` was checked at the reveal and matches.

**Cost:** $4.21 billed in total, including the MC Dropout run's $0.002; $0 sandbox. Raw rows are in
`gapbench_test_v12.json`.

**Scoring:** `score.py`'s own functions on the `test-v12-*` tasks, from a scratch script. One display
fix was needed: the baseline produced no answer on 9 no-cause runs, which the scorer counts as
"missed". That made the missed count exceed its denominator, the cause runs, and crashed the Wilson
interval. The script caps that one input at its denominator. No outcome is changed, and `score.py`
itself was not edited.

## Results (30 runs per arm: 15 on tasks with a cause, 15 without)

| Arm | Confidently wrong (exact 95% CI) | Correct causes (of 15) | Correct abstentions (of 15) | Balanced acc. | Out-of-space diagnosed |
|---|---|---|---|---|---|
| **GapFinder** | **0/30** (0-11.6%) | **12** | **15** | **0.90** | 4/9 |
| GapFinder, evidence off | 0/30 | 12 | 15 | 0.90 | 4/9 |
| GapFinder, random order | 0/30 | 12 | 15 | 0.90 | 5/9 |
| GapFinder, verification off | 12/30 (23-59%) | 10 | 8 | 0.60 | 5/9 |
| Super baseline agent | 8/30 (12-46%) | 5 (+1 partial) | 0 | 0.17 | 0/9 |
| Always "Unexplained" | 0/30 | 0 | 15 | 0.50 | 0 |

**Pre-registered success criteria:**

| Criterion | Target | Result |
|---|---|---|
| Confidently wrong | 0/30 | 0/30 |
| Exact correct causes | > 7/15 | 12/15 |
| Balanced accuracy | > 0.73 | 0.90 |
| Out-of-space diagnosed | > 0 | 4/9 |

All four are met.

## Per task (GapFinder arm)

| Task | Category | Truth | Outcomes |
|---|---|---|---|
| 01 | interaction | `normalize=minmax`, `n=6000` | correct, missed (`normalize=zscore`, `n=2400`), correct |
| 02 | no cause | none | 3 correct abstentions |
| 03 | interaction | `positive_rate=0.15`, `normalize=minmax` | 3 correct |
| 04 | known cause | `normalize=zscore` | 3 correct |
| 05 | incomplete | `max_steps=100`, not exposed | 3 correct abstentions |
| 06 | out of space | data bug (`clip5`) | 3 correct abstentions |
| 07 | incomplete | `max_steps=100`, not exposed | 3 correct abstentions |
| 08 | decoy (rlbench) | `max_steps=100` | correct, missed (`max_steps=100` + `lr=0.5`), missed (`lr=1`) |
| 09 | noise only | none | 3 correct abstentions |
| 10 | known cause | `normalize=zscore` | 3 correct |

## How to read the jump from v1.1 (7/15, balanced 0.73)

**The sets differ, so this is not a paired comparison.** Two things changed at once:
- **GapFinder**, through the phase 3 selection changes. Like for like on the 22 public tasks
  (`eval/dev_suite.py`, post-hoc), correct causes went from 24 to about 27-28 of 39.
- **The benchmark.** The v1.2 generator rejects tasks where another configuration explains the claims
  as well as the planted one. It now checks with standard errors and likelihoods, and checks pairs too.
  So every task here has an identifiable answer, which makes the set fairer, and so easier, for every
  arm. The baseline also rose, from 3/15 to 5/15.

The honest claim:
- on identifiable tasks, GapFinder v1.2 found the planted cause in 12 of 15 runs, with no confident
  mistakes;
- interactions, its weakest category in v1.1 (0/6), were 5/6 here.

## Remaining misses

- **The rlbench decoy (task 08).** One run proposed `lr=1`, a ×10 ladder value added in v1.2. Another
  kept a passenger, `lr=0.5`, next to the true `max_steps=100`. Both are noisy-RL equifinality, the
  same pattern as v1.1's task 04.
- **One interaction run (task 01)** chose the equally plausible `normalize=zscore, n=2400`.

These tasks are now public, so they are dev data.
