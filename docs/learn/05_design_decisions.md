# 5. Why it's built this way

Every big design choice answers one question: **how do we find real causes without fooling ourselves?** Each
choice below says what we chose, why, where the idea came from (**published**, **from another field**, or
**ours**), and what evidence we have. [Page 10](10_where_the_ideas_came_from.md) lists every technique with
its source.

---

## Part 1. Choices about answers

### "I don't know" beats a confident wrong answer
- **Choice:** many careful labels ("Fits but unsupported", "Inconclusive", "Unexplained"). Only an answer that
  passes every check is "Explained".
- **Why:** a researcher who reads "Explained: learning rate" believes it and moves on. A careful "here are the
  leads" still helps; a confident mistake does harm.
- **From:** ours.
- **Evidence:** 0 confidently wrong in 90 sealed GapBench runs, against 49 of 90 for a coding agent. One
  blind real paper was confidently wrong (GraphMAE, before the next rule existed).

### A confident label must be earned
- **Choice:** "Explained" or "Paper-artifact inconsistency" needs all of: the search finished, every setting
  got a run, and the evidence comes from the paper, its docs or the web. Source code alone shows what the code
  does, not what the authors ran.
- **Why:** GraphMAE's mistake was a chain: the appendix was never read, so the code's value was taken as the
  paper's, and a wrong answer passed on weak evidence.
- **From:** ours.
- **Evidence:** nothing confidently wrong on real papers since. On planted tasks, one confident mistake in 132
  gap-task searches until c6.

### A code change is never "Explained"
- **Choice:** a code edit that makes the numbers fit is a "code lead", labelled at most "Fits but
  unsupported".
- **Why:** code can be edited until any number fits. A fitting edit shows where to look, not what the authors
  did.
- **From:** ours.

### Three independent checks before "Explained"
- **Choice:** the counterfactual (undo it, the gap must return), held-out claims (other numbers must not get
  worse), and evidence (the authors plausibly used this value).
- **Why:** each catches a different mistake: a setting that came along for the ride, a "fix" that breaks
  something else, a lucky fit.
- **From:** the counterfactual is causal reasoning; held-out checks are cross-validation; the evidence rule is
  ours.
- **Evidence:** without verification, 7 of 24 GapBench runs were confidently wrong; with it, 0.

### When the numbers can't decide, say so
- **Choice:** list every answer that fits equally well, pick the simplest, and say "not identifiable from the
  paper's numbers" when nothing the paper reports could separate them.
- **Why:** one number can be matched by many settings. Pretending to know would be dishonest.
- **From:** "equifinality" in hydrology (GLUE) and practical identifiability (profile likelihood).
- **Evidence:** honest, but it does not raise the score. Ties are the main reason settings are missed.

### Not reproduced? Say why it can't be the settings
- **Choice:** history matching scores every configuration against all the claims. When none fits all of them,
  the report says "out of space": look in the code, the data or the evaluation.
- **Why:** "Unexplained" alone tells the user nothing.
- **From:** climate and oil-reservoir model calibration.
- **Evidence:** MC Dropout's diagnosis. One hidden setting, a 5% discrepancy allowance, had blocked every real
  paper from reaching "out of space" until it was set to 1%.

### Small gaps under 1% count as reproduced
- **Choice:** a gap under 1% of the value is "Reproduced", even when it is many times the run-to-run noise.
- **Why:** a paper's machine, libraries and hardware differ from ours by small amounts we can't see. Chasing
  sub-1% gaps on real papers would find causes that aren't there.
- **From:** ours, a safety margin.
- **Evidence:** an outside review proposed lowering it, and we kept it. The planted curriculum now plants only
  gaps of at least 1%.

## Part 2. Choices about the search

### Run real experiments, don't just read
- **Choice:** every answer comes from runs that actually happened, each replayable from its checkpoint.
- **Why:** an AI that only reads can sound convincing and be wrong.
- **From:** ours.
- **Evidence:** the coding agent that read and reasoned was confidently wrong in about half its runs.

### Change conditions, never the algorithm
- **Choice:** only settings, data choices and environment change on disk. A diff guard blocks edits to the
  code. Code hypotheses are tested **in memory**, through an import hook, and reported separately.
- **Why:** if a tool may edit the algorithm, it can "fix" any gap.
- **From:** ours. The in-memory hook resembles how mutation-testing tools work.

### Fork from save points
- **Choice:** build and load once, save checkpoints, start every test from the right one.
- **Why:** loading can take a long time, and checkpoints make every result replayable.
- **From:** a feature of the Sandboxes platform.
- **Evidence:** RusKey: 8 loads instead of 22, about 45% cheaper.

### Measure the noise before believing anything
- **Choice:** run the defaults several times first; anything smaller than the spread is luck; Inconclusive
  when the gap is below the minimum detectable effect.
- **Why:** ML results wobble from run to run.
- **From:** standard experimental practice and power analysis.

### Values from the code, not only from the AI
- **Choice:** every allowed choice, a ladder of sizes, roles from the trace, edge values, and the secant step
  when two tried values bracket the paper's number.
- **Why:** the first version tried only the AI's suggestions, which often missed the answer entirely.
- **From:** ours, plus the secant method from numerical analysis.
- **Evidence:** the true value was tried in 12 of 15 runs after this, against rarely before.

### AI may reorder what is tested, never exclude it
- **Choice:** AI reading decides the order of tests, never which settings are skipped.
- **Why:** GraphMAE's true setting was skipped as "already matching the paper" because the reading was wrong.
- **From:** ours.

### A differential over six cause classes, including "none of these"
- **Choice:** settings, reporting rules, library releases and paper-era code, code defects, the data pipeline,
  and "outside every class" are all scored against every claim.
- **Why:** batch-5's sealed papers had causes in code, evaluation and libraries; a settings-only search
  could only be wrong about them.
- **From:** medical differential diagnosis, plus Bayesian model comparison.
- **Evidence:** toys for every class. On planted tasks the scale, reporting and data classes find causes; the
  library and era classes never could be planted.

### Look in the code by small edits, ranked by where the reported number is computed
- **Choice:** the mutation round makes small edits near the code that computes the printed metric, groups
  them to cover many sites cheaply, and needs a fit on every claim.
- **From:** mutation-based fault localisation (MUSE, Metallaxis), program slicing, group testing.
- **Evidence:** the first planted code defect found (c3). Code is still the weakest class (2 of 6 planted).

### Use AI for reading, plain code for counting
- **Choice:** AI reads the paper, suggests assumptions, reads error messages, and (optionally) proposes code
  edits. Plain code does everything that must be exact: the repo map, candidate values, statistics,
  verification.
- **Why:** AI is good at text and unreliable at exactness. Every AI output that matters is checked: quotes must
  match, file and line references must exist, a proposed edit must parse and must not write a reported number
  into the code.
- **From:** ours.

## Part 3. Choices about money

### Spend only on purpose
- **Choice:** a hard spending cap checked before every AI call; every answer cached; a separate guard on cloud
  costs; a free practice mode that can't spend.
- **Why:** the budget is about $50 in total.
- **Evidence:** $32.73 billed so far. Model calls for a whole planted round cost under $0.10.

## Part 4. Choices about testing (the most important ones)

### Sealed tests, frozen code, and no patching
- **Choice:**
  - the code is frozen first (a git tag);
  - the tasks are made afterwards;
  - the answers stay sealed until the run is committed;
  - success criteria are written first.
- **The owner's lifetime rule:** no change to make a specific paper pass. A change must fix a class of failure
  seen on two papers, or follow a published method. It is never judged on the case that revealed it.
- **Why:** if you tune while looking at the answers, the test measures nothing.
- **From:** pre-registration in clinical trials and psychology.

### Judge a change on a fresh batch, against the frozen old version
- **Choice:** a new version is adopted only if, on a batch made after it was frozen, it is at least as good as
  the old version task by task, holds the dev suite, and is never confidently wrong.
- **Evidence:** this rule rejected c2, c4 and c6. Each looked like progress on its own target and failed on a
  fresh batch.

### Keep the test generator separate from the engine
- **Choice:** the planted curriculum draws its code and data faults from operators frozen at an old version,
  and its training-data cuts use a different expression from the engine's own.
- **Why:** on seed 5 the generator drew faults from the engine's newest operator, so the engine "found" faults
  it had generated itself. That fake gain was caught only afterwards.
- **From:** ours, after the mistake.

### State what a test can detect before running it
- **Choice:** before a batch, say how many differing tasks a sign test needs (at least 6 all one way for
  p < 0.05).
- **Why:** every batch from seed 3 to seed 6 had only 2-5 differing tasks, so none could show a significant
  difference. That was not said in advance, and it cost the owner time.
- **Evidence:** seed 7 aimed at 45 gap tasks and reached 27.

---

## Things we chose *not* to do, and why

| Idea | Why not |
|---|---|
| Let the AI edit the code to match the paper | it would "explain" everything and prove nothing |
| Trust the AI's suggested values alone | early versions never tried the right value |
| Penalise values the paper doesn't mention | 45% of true causes were values only the code suggested |
| Penalise configurations that make results noisier | the true cause often makes results noisier too |
| A fixed run budget held for the code rounds (`code_hold`, c2) | its gains were picks among tied settings, and the dev suite fell |
| Pairing random seeds across runs, and adding repeats as you go | measured on their toy: fewer correct, one confident mistake |
| Lowering the 1% reproduce floor to 2.5 run-to-run standard deviations | on real papers it would chase environment noise |
| Five confirmation runs instead of three | costs budget; the review's arithmetic assumed the wrong formula |
| Letting the model break ties between candidates | can't be measured on the planted tasks, and tie-break tuning is forbidden |
| Judging a new version on the batches that revealed its problems | that is tuning to the answers |
| Crediting a cause at another line as the planted one | a near miss is not a hit |
| Test loss as an extra pygcn claim | the paper reports only accuracy; it would make the test easier than reality |
| A split-sum "conservation" check on the data | in the planted tasks the cut is on the paper's side, and the standard Cora split leaves most nodes unused, so it would fire on every run |
| A lookup table of library default changes | a planted change can't be found by installing old releases |
| Cutting the paper to save model cost | output is two thirds of the cost; it would save about 3% |
| Generic preprocessing knobs (normalisation, clipping) | untargeted changes manufacture fits that look like answers |
| One merged reading of the paper | brings back the appendix miss |

Next: [How we test it →](06_how_we_test_it.md)
