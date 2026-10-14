# GapBench sealed test on GapFinder v1.1 (2026-10-14)

**Protocol** (pre-registered in `eval/gapbench/PROTOCOL.md`, "Pre-registered run plan for the v1.1
sealed test"):
- GapFinder was frozen at tag `v1.1`, and the seed was made after the tag;
- 10 generated tasks, `test-v11-01` to `-10`;
- 5 arms × 3 runs, through `run_arms.py`, with one shared ledger per task and run;
- answers sealed until scoring. The hash `da16e75c…` was checked at the reveal and matches.

**Cost:** $3.86 billed (Nemotron), $0 sandbox (local backend). Raw rows are in
`gapbench_test_v11.json`.

**Scoring:** `score.py`'s own functions, restricted to the `test-v11-*` tasks; `score.py` itself was not
changed after the freeze.

## Results (30 runs per arm: 15 on tasks with a cause, 15 on tasks without one)

| Arm | Confidently wrong (exact 95% CI) | Correct causes / partial (of 15) | Correct abstentions (of 15) | Balanced accuracy |
|---|---|---|---|---|
| **GapFinder** | **0/30** (0-11.6%) | **7 / 1** | **15** | **0.73** |
| GapFinder, evidence step off | 0/30 | 6 / 1 | 15 | 0.70 |
| GapFinder, random ranking | 0/30 | 6 / 0 | 15 | 0.70 |
| GapFinder, verification off | 16/30 (34-72%) | 5 / 2 | 6 | 0.37 |
| Super baseline agent | 19/30 (44-80%) | 3 / 0 | 4 | 0.23 |
| Always "Unexplained" (trivial) | 0/30 | 0 / 0 | 15 | 0.50 |

**For reference, the v1.0 blind tests** (a different 8-task set with no out-of-space tasks; 15 cause
runs each). GapFinder got 5/15 and 7/15 correct causes, with 0 confidently wrong.

## Per task (GapFinder arm, 3 runs each)

| Task | Category | Truth | Outcomes |
|---|---|---|---|
| 01 | interaction | `max_steps=500`, `gamma=0.999` | missed, missed, partial |
| 02 | no cause | none | 3 correct abstentions |
| 03 | out of space | data bug (`clip5`) | 3 correct abstentions (hedged "Fits but unsupported") |
| 04 | decoy | `max_steps=100` | correct, missed, correct |
| 05 | interaction | `normalize=minmax`, `epochs=75` | 3 missed |
| 06 | incomplete | `positive_rate=0.5` (not exposed) | 3 correct abstentions |
| 07 | noise only | none | 3 correct abstentions ("Inconclusive") |
| 08 | known cause | `normalize=minmax` | 3 correct |
| 09 | out of space | data bug (`drop_scaled`) | 3 correct abstentions (hedged) |
| 10 | known cause | `max_steps=100` | correct, missed, correct |

## What this says about hypothesis coverage

**Was the true configuration tested?** In 12 of the 15 GapFinder runs on tasks with a cause, the exact
true configuration was measured.

- **Coverage miss (3 runs, task 05):** `epochs=75` (5× the default) was never tried. The 6-value cap per
  knob cut it, after the ledger's own candidates and the larger ladder rungs.
- **Selection misses (5 runs):** the truth was measured, but a different, equally good configuration was
  chosen. This was task 01 in all three runs (e.g. `max_steps=2000` alone), and one run each of tasks 04
  and 10.

So coverage is no longer the main failure mode. Choosing among equally good fits is.

## Problems this test exposed (for the next version, not fixed here)

1. **The out-of-space tasks are only out of space for single settings.** The generator's rival check
   tries single settings only. On both out-of-space tasks, a *pair* of settings fits the claims
   (e.g. `normalize=zscore` + `positive_rate=0.5`), so history matching found an in-space fit and
   `out_of_space_diagnosed` is 0/9 for every arm. GapFinder's hedge ("Fits but unsupported") was the
   honest answer, but the category doesn't measure what it was meant to. The fix is to extend the
   generator's rival check to the pairs the combine round can test.
2. **Selection among equally good fits** is the main loss: task 01, and the MC Dropout v1.1 case.
3. **The value cap** dropped a ×5 rung (task 05). The ladder order, or a per-knob cap that depends on
   how many knobs are open, would decide this.

These tasks are now public, so they are dev data from here on. Any claim about a fix needs a new
sealed set.
