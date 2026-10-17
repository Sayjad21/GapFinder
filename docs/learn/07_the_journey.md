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

What is still unproven: all the successes since blind-2 are on papers whose answers we knew. The next step
is a frozen batch of papers, run in Sandboxes without changes in between, to measure a rate.

## Before and after, in one table

| | v1.0 | v1.3 |
|---|---|---|
| Where candidate values come from | AI suggestions only | AI + code (choices, ladder, multipliers, edges) |
| When several answers fit | picks one, silently | picks the simplest and lists the others |
| "Unexplained" | the end of the story | "out of space suspected", with code leads and tested code patches |
| Small gaps | could be blamed on something | "Inconclusive" when under the detectable size |
| Budget | first come, first served | escrow for confirmation, a reserve for patch tests, racing |
| Cloud hiccups | could lose the right answer | retried with the same value |
| MC Dropout verdict | Unexplained | documented settings named + out of space |
| Confident mistakes (blind) | 0 | 0 |

## What this journey teaches

1. **Read the logs before changing anything.** Most real causes were different from our first guess.
2. **Measure every change against noise.** Several "obvious" improvements made things worse.
3. **Say less when the data say less.** Sets, Inconclusive and out of space are honest answers, not
   failures.
4. **Keep the tests sealed.** Otherwise you only measure how well you tuned to them.

Next: [Limits and what's next →](08_limits_and_next.md)
