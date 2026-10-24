# 7. The journey: how GapFinder grew

This is the story of the project, version by version. For each step:
- **What was the problem?**
- **How did we find it?**
- **What did we change?**
- **Did it help?**

The pattern you'll see: every improvement started with looking closely at *why* a run failed, in the
run logs, before changing anything.

---

## Stage 0: the first working system

**Goal:** prove the basic idea works end to end on a real system paper.

**Built:**
- the claim ledger and the assumption space (with Nemotron);
- the checkpoint tree and forking in Sandboxes;
- the search (screen, confirm, combine, bisect, verify);
- the Gap Report and the web replay.

**First real case: RusKey**, a database-tuning paper. GapFinder ran 127 experiments from 13 database
loads.
- **Verdict:** "Unexplained" for the main claims.
- **A surprise discovery:** loading the same database with the same command gave a *different* result
  each time. So one load can't be trusted, and GapFinder learned to measure "setup noise" too.

## v1.0: the first blind test

**Test:** 8 generated tasks, 3 runs each, and the whole test done twice.

**Result:**
- **0 confident mistakes** out of 24 runs, both times, and all 9 "nothing to blame" runs right;
- but only **5 and 7 of 15** correct causes;
- the coding-agent baseline was confidently wrong in 14 and 12 of 24 runs;
- **MC Dropout: "Unexplained"** in all four variants we tried.

**Why it missed so much** (found by reading the logs with `eval/reachability.py`): the true value was
often **never even tried**. Not one of the 6 interaction runs ever tested both true values. The AI
suggested candidate values, and its suggestions simply didn't include the answer. On MC Dropout it
suggested `epochx` = 500, 1000, 2000, all *higher* than the default, while the answer was 10.

**Lesson:** the bottleneck wasn't checking answers; it was *coverage*, meaning trying the right values at
all.

## v1.1: fixing coverage

**Changed:**
- **Values from the code, not just the AI:**
  - every allowed choice of a setting;
  - a "ladder" of sizes around the default (×10, ÷10, ×2, …);
  - fraction-aware values;
  - edge values (1 and 0.0);
  - simple factors for multipliers.
- **Config flow:** reading the code to learn that `--epochx` *multiplies* the epochs, so 10 is a natural
  value.
- **Sets:** when several values fit equally well, report all of them.
- **History matching:** look at all the claims together, and say "out of space" when no setting can fit
  them all.
- **Static code checks:** list suspicious lines in the code when the answer is "out of space".
- **Inconclusive:** when a gap is smaller than the noise can detect, say so.
- **A new benchmark category, "out of space":** bugs in an older copy of the code.

**Result:**
- The sealed v1.1 test: **the true value was tested in 12 of 15 runs**. Coverage was largely fixed.
- 7 + 1 partial of 15 correct, 0 confident mistakes.

**New problem:** the right answer was now *tested* but not always *chosen*. Several answers fit the numbers
about equally well, and the tie-breaking rules picked the wrong one.

## Phase 3 (v1.2): fixing selection

We studied every miss in the logs. The real causes were often different from what we expected:

| Miss | What we expected | What the logs actually showed | Fix |
|---|---|---|---|
| `lr=0.91` was chosen | bad luck in a noisy run | a bug: learning rates were treated like fractions (0.91 = 1 − 0.9/10) | only fraction-like settings get fraction values |
| `epochs=75` never tried | | a limit of 6 values per setting cut it | the ×5 step comes earlier; the limit grows with the budget |
| an extra, useless setting kept | the simplification step failed | a ranking bug: an unsupported guess outranked a well-supported partial answer | fixed the ranking; remove a setting that doesn't beat the noise |
| a very noisy setting won | | "close enough" used the candidate's own spread, so noisy candidates passed easily | judge closeness with a fair likelihood rule |

We also built:
- the **dev suite**, which re-runs the search on all public tasks for free, to measure every change
  before keeping it;
- **racing:** spend repeats on the best candidates, not all of them;
- **the forward step**, which pairs the best setting with every value of the others, for interactions.

**Things we tried that didn't work, and removed:** pairing values by "how much they move the result" (it
made things worse), an unconditional forward step (also worse), and pairing random seeds (no noise
reduction).

**Result:**
- The sealed v1.2 test: **12 of 15 correct, 0 confident mistakes, balanced accuracy 0.90.**
- The task generator was also improved, so tasks with no single right answer are rejected.

**MC Dropout on v1.2:** the search was better, but the label still named a wrong (equally good) pair,
because the budget ran out before the documented pair got a second run.

## Phase 4 (v1.3): budget and code-level causes

**Changed:**
- **Escrow:** keep 25% of the budget for confirming the best candidates.
- **Early stop:** don't try fine values for settings whose coarse values did nothing.
- **Patch knobs:** test hard-coded numbers in the code, in memory, without editing files. Built because on
  MC Dropout the clues pointed at `batch_size = 128`, and nothing could test it.
- **The web report** shows history matching, leads and equally good answers.

**Result on MC Dropout:**
- **For the first time, GapFinder names the documented settings (`epochx=10, hidden=1`)**, and says the
  rest is out of space.
- The patch round showed the batch size is the one constant that strongly moves the second claim
  (Yacht). But no single code change fixed both claims, which matches the authors' explanation: part of
  the cause is how hyperparameters were tuned, and that is a loop, not a number.

**Result on the sealed v1.3 test:**
- 0 confident mistakes;
- 9 of 15 correct (+1 partial), with every miss on two hard interaction tasks;
- out-of-space diagnosis 6 of 9, the best yet;
- two of the four pre-registered goals missed, and reported as missed.

## The first blind real papers (v1.3 → v1.4)

Every real-paper result so far had been on MC Dropout, whose answer we already knew. So the next step was
**blind real papers**: a separate AI model picked a paper with a documented reproduction gap and sealed the
answer before GapFinder saw anything.

**blind-1, FastGCN: missed, not confidently wrong.**
- GapFinder named the right setting (learning rate) but the wrong value.
- Reason 1: it couldn't read TensorFlow-style flags, so most settings were never tried.
- Reason 2: the true value fixed the main number but made another row worse. That row had been tuned
  separately in the paper.
- Fixed: absl flags, testing every setting, checking guessed defaults, and "tuned separately" rows.

**blind-2, GraphMAE: confidently wrong**, the first confident mistake on any blind test. It said
"Explained: `mask_rate=0.5`"; the real cause was `alpha_l=1`. It was one chain of failures:
1. the AI never saw the appendix table with the answer, because its excerpt was cut at 25,000 characters;
2. so it wrote the code's value as "the paper's value";
3. a rule then skipped the true setting as "already matching the paper";
4. an equally good wrong answer passed on weak evidence.

The lesson that changed the plan: **fixing one paper at a time never ends.** Each new paper fails in a new
way. So instead of more patches, the next stage changed two patterns behind both failures:
- AI reading may only *reorder* what is tested, never *exclude* it;
- a confident label must be *earned*.

## The white-box rebuild (after v1.4)

GapFinder stopped treating the program as a black box:
- **runtime tracing** (watch where values go);
- the **secant step**;
- **relation claims**;
- **paper-versus-trace comparison**;
- patch knobs for **function defaults**;
- the **confidence rules**.

Two lessons from testing these:
1. **The practice suite caught two regressions.** Both times we found the cause and fixed it:
   - the secant step manufacturing decoys: 102 → 92 of 138 correct;
   - screening "already matching" settings first, which wasted budget: 102 → 76.
   After the fixes it is back to 99 of 138 (the same within noise), with 0 confident mistakes.
2. **One hidden setting had been blocking every real paper.** History matching allowed a 5% "model
   discrepancy", meant for scaled-down reproductions. With the 3-sigma rule, gaps up to about 15% looked like
   noise, so no real paper ever reached "look in the code". With 1% at full scale, the VGAE development case
   was found end to end: a changed function default, matched to the paper's own sentence, tested in memory
   and verified on all 8 numbers.

What was still unproven: all the successes since blind-2 were on papers whose answers we knew.

## Frozen and sealed batches of real papers (2026-10-18/19)

**Frozen batches with known causes:**
- **devbatch-1** (5 papers): 1 correct.
- **devbatch-2** (3 papers): 0 causes found, 3 correct abstentions.

**Sealed batches 3-5 (6 papers):**
- **Fair Clustering correct:** the paper's λ=10 is wrong; the authors' real value is 100, and all four claims
  matched.
- **RippleNet partial:** the learning rate found; the second needed setting (l2) missed for budget.
- **Missed:** SparseTSF, the GCN attack, SDCN and BOND.

**What the misses had in common:** across batch-5, settings causes were found 1 time in 4, and causes in code,
evaluation and libraries 0 times in 4. GapFinder could only answer "a setting", and the real causes were
often elsewhere:
- an edge counted twice;
- the best epoch chosen on the test labels;
- an API that changed between library releases.

**The rule that changed everything after this.** The owner was tired of fixes that made one paper pass. From
then on, for the life of the project:
- a change must fix a class of failure seen on at least two papers, or follow a published method;
- it is never judged on the paper that revealed it;
- progress is a rate on fresh, frozen batches.

## Plan D1-D7: six cause classes (2026-10-20/21)

Seven pieces of work, each with its own small acceptance test:
- **D1:** a differential over six cause classes:
  - settings;
  - reporting rules (best epoch, best by validation, best of N seeds, read from runs already made);
  - library releases and the paper-era code;
  - code defects;
  - the data pipeline;
  - "outside every class".
- **D2:** breaking ties with runs at the paper's other conditions (Bayesian experimental design); the scale
  probe for unit and counting conventions; paper priors.
- **D3:** better paper reading:
  - numbers grounded in any spelling;
  - table grids from the LaTeX source and the PDF, checked against each other;
  - a recall harness.
- **D4:** paper words linked to code flags by meaning (BM25, then checked at runtime).
- **D5:** the mutation round: small edits to the code, tested in memory, scored on every claim.
- **D6:** the harness built automatically, step by step (`gapfinder harness`).
- **D7:** the calibration gate, multi-fidelity screening, the planted archetypes.

Everything passed its toys, and the dev suite stayed the same within noise (52 of 69). But no fresh real
paper was run, so there was no way to know whether it helped.

## The planted-gap curriculum (2026-10-21 onwards)

The owner asked: plant gaps into papers that already reproduce, from easy to hard, and see which kinds
GapFinder finds. Page 6 explains how it works. What happened, version by version:

### c1: the baseline (seeds 2 and 3, 30 gap tasks)
- **Results by family:**
  - scale conventions 6 of 7;
  - settings 2 of 18;
  - code defects 0 of 5;
  - data, reporting, era and library never moved a number enough to plant.
- **0 confidently wrong.**
- **The misses were sorted into seven classes:**
  - **E1:** code rounds starved by the run budget;
  - **E2:** mutation sites ranked out of reach;
  - **E3:** the right knob at a value off the grid;
  - **E4:** ties on a single number;
  - **E5:** a wrong knob with no tie (watched only);
  - **E6:** gaps below the detection limit;
  - **E7:** families that couldn't be planted.

### c2: a fixed run budget for the code rounds (seed 3), not adopted
7 of 16 against c1's 4. But every gain was a setting, one of them a lucky pick among ties, and code stayed at
0 of 3. The dev suite fell from 52 to 48. Lesson: **gains can come from somewhere other than the target**, so
look at which tasks moved, not just the total.

### c3: plan F1-F10 (seed 4), adopted
- **What changed:**
  - mutation sites ranked by the code that computes the printed number;
  - code tests run early;
  - value intervals;
  - group screening of mutation sites;
  - a class scheduler;
  - the "not identifiable" note;
  - DeepCrime fault operators in the curriculum.
- **The full test suite caught four regressions first**, each fixed at its class. Two examples: the early code
  screen ran before the repo's own alternative settings block; a guard judged "off as run" with the noise
  floor.
- **Result:** 6 of 13 against c1's 4: better on 2, worse on 0.
  - **The first planted code defect found:** RippleNet's `np.mean` that should be `np.sum`.
  - **c1's one confident mistake gone.**

### c4: plan G1-G8 from an outside review (seed 5), not adopted
- **What changed:**
  - a log-scale scale probe;
  - a training-data-cut operator;
  - mutation operator classes taking turns;
  - a cheap AI code proposer.
- **Result:** 5 of 14 against c3's 4, but its three gains were all training-data cuts, two of them made by
  its own new operator: the generator drew faults from the engine it was testing. On the other 10 tasks it
  got 2 against 4.
- **Its two losses were its own changes:**
  - the turn-taking pushed a planted constant out of the first tries;
  - the log scale picked a factor that makes the epochs 3.33.
- **The proposer's edits mostly didn't parse** (7 of 8).

### c5: plan H1-H5 (seed 6), adopted and current
- **What changed:**
  - scale factors must give whole numbers for whole-number settings, and the second-best factor is tried when
    the best fails;
  - the first 6 mutants stay in priority order;
  - the proposer's edits are text replacements, re-parsed;
  - the scale probe's verification runs are reserved.
- **The curriculum generator was fixed:** it now draws its faults from operators frozen at an old version.
- **Result:** 7 of 16 against c3's 5: better on 2, worse on 0.
  - a 60% training-data cut found at its site;
  - a FastGCN epochs convention found;
  - confident labels back on a scale convention.
- **The dev suite was unchanged** (99 against c1's 100 of 138).

### The test-design mistake
Asked "what kinds of gaps does it find, compared with previous versions", the honest answer was: no
comparison so far was statistically significant. Each batch had only 2-5 tasks where two versions differed,
and a sign test needs at least 6. That should have been said before the first round. The owner's frustration
was fair. From then on, every round states in advance what it can detect.

### c6: plan I, from a second outside review (seed 7), not adopted
- **What changed:**
  - split sizes (`test_ratio`) became leads, with their in-between values screened;
  - the proposer runs on unsupported fits;
  - the training-data fraction is estimated on a log scale;
  - a switch-flip operator for layer `bias` and `affine`;
  - planted gaps of at least 1%.
- **Several of the review's claims were wrong when checked against the code:**
  - its statistics formula didn't match ours;
  - a factor it wanted added was already there;
  - its straight-line formula would have put a 40% cut at 30%.
  These were corrected before building.
- **Result** (27 gap tasks, the largest batch yet): 7 against c5's 10, better on 1, worse on 4, **two confident
  mistakes**, two crashes.
- **The confident mistakes exposed a defect that c5 also has.** The scale probe tries several factors, and on
  noisy or flat data a wrong one can fit by chance. Its confident label doesn't account for how many were
  tried.

## Before and after, in one table

| | v1.0 | v1.3 | c5 (now) |
|---|---|---|---|
| Where candidate values come from | AI suggestions only | AI + code (choices, ladder, multipliers, edges) | + roles from the trace, the secant step, value intervals |
| Kinds of cause it can test | settings | settings + hard-coded numbers | six classes: settings, reporting rules, libraries and paper-era code, code edits, data pipeline, "none of these" |
| When several answers fit | picks one, silently | picks the simplest and lists the others | + "not identifiable from the paper's numbers" |
| "Unexplained" | the end of the story | "out of space suspected", with code leads | + the mutation round, tested in memory |
| Unit and counting conventions | not tested | not tested | the scale probe |
| Budget | first come, first served | escrow, a patch reserve, racing | + a class scheduler and an early code screen |
| Confident label | after three checks | after three checks | after three checks + a finished search, every setting tried, evidence beyond the code |
| Confident mistakes | 0 (GapBench) | 0 (GapBench), 1 (blind GraphMAE) | 0 on real papers since the rules; 1 in 132 planted searches (c1), but 2 on seed 7 for c6 |

## What this journey teaches

1. **Read the logs before changing anything.** Most real causes were different from our first guess.
2. **Measure every change against noise, on a fresh batch, against the old version.** c2, c4 and c6 all
   looked like progress until they were.
3. **Say less when the data say less.** Sets, Inconclusive and "out of space" are honest answers.
4. **Keep the tests sealed, and keep the test generator separate from the engine.** Otherwise you measure
   how well you tuned to them, or how well the engine finds its own faults.
5. **Size the test before running it.** A test that can't show a difference wastes everyone's time.
6. **Check outside advice against the code.** Both reviews had good ideas and several wrong claims.

Next: [Limits and what's next →](08_limits_and_next.md)
