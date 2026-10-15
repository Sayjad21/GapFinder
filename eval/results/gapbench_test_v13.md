# GapBench sealed test on GapFinder v1.3 (2026-10-16)

**Protocol** (pre-registered in `eval/gapbench/PROTOCOL.md`, "Amendment for the v1.3 sealed test"):
- frozen at tag `v1.3`, seed made after the tag;
- 10 tasks `test-v13-01` to `-10` (7 mlbench, 3 rlbench);
- 5 arms × 3 runs;
- the sealed hash `a4a56482…` was checked at the reveal and matches.

**Cost:** $3.58 billed. **Scoring:** `score.py`'s functions on `test-v13-*`, with the same display fix as
v1.2. Raw rows are in `gapbench_test_v13.json`.

## Results (30 runs per arm: 15 with a cause, 15 without)

| Arm | Confidently wrong (exact 95% CI) | Correct causes (of 15) | Correct abstentions (of 15) | Balanced acc. | Out-of-space diagnosed |
|---|---|---|---|---|---|
| **GapFinder v1.3** | **0/30** (0-11.6%) | 9 (+1 partial) | **15** | 0.80 | **6/9** |
| GapFinder, evidence off | 0/30 | 9 | 15 | 0.80 | 6/9 |
| GapFinder, random order | 0/30 | 9 | 15 | 0.80 | 6/9 |
| GapFinder, verification off | 11/30 | 9 | 10 | 0.63 | 6/9 |
| Super baseline agent | 22/30 (54-88%) | 2 (+1 partial) | 1 | 0.10 | 0/9 |
| Always "Unexplained" | 0/30 | 0 | 15 | 0.50 | 0 |

**Pre-registered criteria: two of four missed.**

| Criterion | Target | Result | Met? |
|---|---|---|---|
| Confidently wrong | 0/30 | 0/30 | met |
| Exact correct causes | ≥ 12/15 | 9/15 | **missed** |
| Balanced accuracy | ≥ 0.85 | 0.80 | **missed** |
| Out-of-space diagnosed | > 0 | 6/9 | met (v1.2: 4/9) |

## Per task (GapFinder arm)

| Task | Category | Truth | Outcomes |
|---|---|---|---|
| 01 | interaction (mlbench) | `threshold=0.4`, `normalize=minmax` | 3 missed (`normalize=zscore`, `threshold=0.3`) |
| 02 | incomplete | `normalize=zscore`, not exposed | 3 correct abstentions |
| 03 | decoy (rlbench) | `max_steps=100` | 3 correct |
| 04 | known cause | `normalize=zscore` | 3 correct |
| 05 | out of space | `clip5` | 3 correct abstentions |
| 06 | interaction (mlbench) | `n=12000`, `normalize=zscore` | missed (`n=6000`), partial (`zscore` alone), missed (`n=5000`) |
| 07 | no cause | none | 3 correct abstentions |
| 08 | noise only | none | 3 correct abstentions |
| 09 | known cause (rlbench) | `max_steps=100` | 3 correct |
| 10 | incomplete | `normalize=zscore`, not exposed | 3 correct abstentions |

**Every miss is on the two interaction tasks; everything else is 24/24.** The two misses have two
different causes.

- **test-v13-01: a coverage gap.**
  - The true `threshold=0.4` was never tested. For a default of 0.5, the fraction ladder gives
    0.05, 0.95, 0.25, 0.75, 0.1, 0.9, … but no small step either side (0.4, 0.6), and the ledger didn't
    propose 0.4.
  - The truth wasn't in the equivalence set either; the set held `zscore + 0.3` and
    `minmax + class_weight`.
  - **Fix:** add ±0.1 steps (and similar small additive steps) to the fraction ladder.
- **test-v13-06: value-level equifinality.**
  - The true pair `zscore + n=12000` was measured, and it was inside GapFinder's set of equally good
    configurations in runs 1 and 2. But `n` = 5000, 6000, 10000 and 12000 all fit, so the sets had 5
    and 10 members, over the pre-registered K = 3, and earned no `correct_in_set`.
  - The per-knob value set contains 12000 in run 1 (`correct_set` 10/15).
  - **The generator should have rejected this task.** Its pair-rival check pairs only the 8 single
    settings closest to the paper, and `n` alone barely moves the metric without normalisation, so
    `zscore + n=6000` was never checked as a rival. That is the same lesson as GapFinder's own combine
    round.

## Reading against v1.2 (12/15, balanced 0.90)

**Not a paired comparison: the two sets differ.** v1.2 had one easy and one moderate interaction
task (5/6); v1.3 had two hard ones (0/6). Like for like on the 32 public tasks, the post-v1.2 changes
were accuracy-neutral. So this is a different draw of task difficulty, not a regression the dev suite
missed.

The pre-registered criteria were missed all the same, and that is the reported result.

**What held up:**
- safety: 0/30 confidently wrong;
- every non-interaction task correct;
- out-of-space diagnosis up to 6/9;
- a baseline that is confidently wrong in 22/30 runs on the same tasks.

These tasks are now public, so they are dev data.
