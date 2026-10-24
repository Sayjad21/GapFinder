# 4. Inside each part

This page opens every box from [the big picture](03_architecture_overview.md). Each section says what
the part does, how it does it in simple terms, and where the code lives.

---

## 4.1 The AI models and the router (`gapfinder/models/`)

GapFinder uses a family of AI models called **Nemotron**, through a service called **Token Factory**.

| Model | Its job |
|---|---|
| Nemotron 3 Ultra (big) | reads the whole paper, lists claims and assumptions |
| Nemotron 3 Super (medium) | filters claims; reads error messages when a run fails |
| Nemotron 3 Nano (small) | backup reader for unusual output formats |

Every call goes through one **router** (`router.py`). The router:
- **caches** every answer, so re-running costs nothing;
- **repairs** broken JSON;
- **checks a spending cap** before each call (`budget.py`). If the cap is reached, the call is refused,
  not made. Money safety is built in.

## 4.2 Reading the paper: the claim ledger (`gapfinder/ledger/claims.py`)

- The paper is turned into text (`ingest/pdf.py`).
- Ultra lists every claimed result: a number, a comparison or a trend.
- Each claim comes with an exact quote. If the quote isn't found in the PDF, the claim is dropped. This
  stops the AI from inventing claims.
- Super then removes non-results (like "we used Python").

## 4.3 Reading the code: the repo map (`gapfinder/ingest/repo_map.py`)

A plain program, with no AI, scans the code for command-line settings:
- their names (`--epochx`), their defaults (`500`), and allowed choices (`zscore`, `minmax`);
- where each is defined (file and line).

A helper called **config flow** (`config_flow.py`) follows the code a little further. For example, it
notices that `--epochx` is *multiplied* by the base number of epochs. That tells GapFinder it's a
"multiplier", and that values like 10 or 100 make sense for it.

## 4.4 Possible causes: the assumption space (`gapfinder/ledger/assumptions.py`)

Ultra combines the claims and the repo map into **assumptions**:

> "Setting: epochx. The paper says '10x more iterations'. The code default is 500. It probably affects
> the Energy result. Values to try: 10, 500, 1000."

Each assumption is tied to evidence: a quote from the paper, or a `file:line` in the code (checked).

## 4.5 What values to try: candidate values (`gapfinder/search/hypotheses.py`)

The AI's suggestions aren't enough on their own: early versions often never tried the right value. So
GapFinder adds values computed from the code itself:

- **Choices:** every allowed option of a setting (e.g. all normalisation methods).
- **A "ladder" of sizes** around the default, coarse first: ×10, ÷10, then ×2, ÷2, ×5, ÷5, and further.
  For a default of 15 epochs: 2, 150, 1, 8, 30, 3, 75, …
- **Fractions stay fractions.** A probability of 0.5 gets 0.05 and 0.95, never 5.
- **Multipliers** get simple factors: 1, 2, 5, 10, 100.
- **Edge values:** 1 for counts (one layer, one thread), 0.0 for amounts (no noise).
- **How many per setting:** 6 to 10, depending on the budget.

## 4.6 Running code: backends, checkpoints and forks (`gapfinder/sandbox/`)

- **Backends** are where the code runs: your computer (`local`), Docker, or cloud Sandboxes (`contree`).
- **The checkpoint tree.** The code goes through stages: `source → built → loaded`. Each stage is saved.
  A setting that only affects running forks from `loaded`. A setting that changes the data reloads from
  `built`. A build flag rebuilds.
- **The runner** (`runner.py`) starts each experiment (a *branch*) from the right checkpoint, and gives
  every run its own random seed tag, so repeats are real repeats.
- **The diff guard.** A branch may only change files the spec allows (like `out/`). It can never edit
  the algorithm's code.
- **Retries.** If a run fails because the cloud machine had a hiccup (a timeout, a cache race), it's run
  again once with the same values.

## 4.7 How noisy is a number? The noise band (`gapfinder/sandbox/noise.py`)

If you run the same experiment five times, you get five slightly different numbers. GapFinder measures
that first:
- **Calibration:** run the default settings about 5 times.
- **Noise band:** how far the repeats spread. A change smaller than this is treated as luck.
- **Minimum detectable effect:** if the gap itself is smaller than what the runs can detect, the label is
  "Inconclusive", not "Unexplained".

## 4.8 The search engine (`gapfinder/search/engine.py`)

The heart of GapFinder. It works like a detective with a fixed budget of experiments (`--max-runs`).

1. **Screen:** each candidate value once.
   - First the coarse values; finer values only for settings whose coarse values moved the result at
     all (the "early stop").
   - It also keeps a **25% reserve** of the budget for confirming the best candidates later (the
     "escrow").
2. **Confirm:** repeat the promising ones, as a race. Everyone gets 2 runs, then only the best half gets
   the full repeats. The effect must also pass a statistical test against the default runs (a bootstrap
   interval that excludes zero).
3. **Combine:** try pairs of the best settings. If no single setting explains the result, it also pairs
   the best ones with *every* value of the other top settings (the "forward step"), because some
   settings only matter together.
4. **Rank the candidates:**
   - Closest to the paper counts first, with "closeness" judged fairly: a very noisy candidate can't win
     just because its own spread is wide (a likelihood rule).
   - Among answers that fit equally well, the simplest wins: fewest changes, then the smallest change.
5. **Bisect:** in a combination, drop any setting that doesn't improve the fit by more than the noise
   ("Occam's margin").
6. **Verify** (`verify.py`), with three checks:
   - **Counterfactual:** undo each change. The gap must come back. If it doesn't, the change wasn't
     needed.
   - **Held-out claims:** other numbers from the paper must not get worse.
   - **Evidence:** is there a quote in the paper or code (or, last, the web) showing the authors used
     this value? Without evidence the best possible label is "Fits but unsupported".
7. **Equally good configurations:** every answer the numbers can't tell apart from the chosen one is
   listed in the report.

## 4.9 Looking at all claims together: history matching (`gapfinder/search/history.py`)

The idea comes from climate and oil-field modelling. For every tested configuration and every claim, it
computes how *implausible* the paper's number is under that configuration, counting all the sources of
noise. Anything over 3 means "ruled out". Then:
- **reproduced:** the default already fits everything;
- **in space:** some tested configuration fits every claim;
- **out of space suspected:** each claim fits *some* configuration, but none fits all. The claims
  contradict each other under every setting, so the cause is probably outside the settings;
- **out of space likely:** some claim fits nothing at all.

## 4.10 Clues in the code: static code checks (`gapfinder/ingest/code_checks.py`)

When the answer is "out of space", GapFinder reads the code, without running it, for places a hidden
cause could live:
- numbers fixed in the code that look like settings (`batch_size = 128`);
- settings read from data files;
- loops that pick the best of several settings (grid searches), and whether they peek at test data;
- fixed random seeds and fixed data-split fractions.

Each is listed as a **lead** with its file and line.

## 4.11 Testing code clues: patch knobs (`gapfinder/sandbox/ast_patch.py`)

A lead like `batch_size = 128` can't be changed with a setting. So GapFinder changes it **in memory**:
- It uploads a tiny helper (`sitecustomize.py`) next to the code. Python loads it automatically when it
  starts.
- When the program imports `net/net.py`, the helper reads the file, swaps `128` for (say) `32` in memory,
  and runs that version.
- **No file is edited.** The diff guard is still satisfied, and nothing in the repo changes.
- If the line doesn't contain the expected number, the run fails loudly, so a wrong patch can never look
  like a result.
- For the script the command runs directly, a small runner (`gf_patch_run`) does the same.

It runs when the claims look out of space, or when the answer is only an unsupported fit (and its cheapest
tests also run early, section 4.27). It has its own share of the budget, and a patch is reported only if it
makes **every** claim fit after repeats. It's always reported as a *code change*, never as a setting.

## 4.12 When runs fail: triage (`gapfinder/search/triage.py`)

If every run of a value fails, Super reads the error and says why. If the program rejected the value
(like the text "two" for a number), it suggests a valid one, which is tried once. Super's guess is only
trusted when the error message really shows a rejection. That rule exists because once it mistook a
cloud hiccup for a rejected value and lost the right answer.

## 4.13 The report and the app (`gapfinder/report/`, `gapfinder/api/`, `web/`)

- `gap_report.py` writes the Markdown and JSON report: the cards, history matching, leads, and
  provenance (which code version, which models, what it cost).
- `missing_sentence.py` can draft the sentence the paper's methods section is missing, and an issue
  text for the authors (never posted automatically).
- The **web app** (React) shows replay, reports and the scoreboard. A static copy is built for GitHub
  Pages.

---

## Added after the blind real-paper tests (v1.4 and later)

These parts came from studying why real papers failed. Each one makes GapFinder look *inside* the
program instead of guessing from names and text.

### 4.14 Watching what values do: the runtime trace (`gapfinder/sandbox/trace_hook.py`, `gapfinder/search/trace.py`)

Before the search, GapFinder runs the program once, briefly, with a small hook that watches where each
setting's value ends up:

| The value lands in… | So the setting is a… | Values worth trying |
|---|---|---|
| the optimizer's step size | **rate** | ×10, ÷10, … never 0, never "fraction" steps |
| a dropout layer | **fraction** | between 0 and 1 |
| a data loader's batch size, a layer width | **size** | powers of two |
| the length of a training loop | **count** | ×10, ÷10, 1 |
| a loop length that is this setting × another | **multiplier** | 1, 2, 5, 10, 100 |
| a random-seed call | **seed** | not tried at all: seeds are noise, not causes |

This works whatever the setting is called (`--lr`, `--eta`, a YAML key). If two settings share a value, so
nobody can tell which one reached the call, GapFinder says "ambiguous" rather than guessing. A number written
straight into the code that reaches one of these calls becomes a **lead** for a patch knob. Real result: on
FastGCN it found `learning_rate` (the optimizer) and `epochs` (the loop) by watching them.

### 4.15 Filling the gaps between ladder values: the secant step

If the paper's number falls *between* two values GapFinder tried (say ×2 gives too little and ×5 too much),
it estimates where the crossing is, rounds it to a value a person would write (3, 25, 0.002), and tries
that. **It only does this when no tested value already fits every claim.** The first version did it always,
and made up exact-fit values for the *wrong* settings that sometimes beat the true cause. The practice
suite caught that.

### 4.16 The paper's own statements as checks: relation claims

Papers say things like "the leave-unchanged strategy harms accuracy". GapFinder can take such a statement as
a claim: under a candidate answer, changing that setting must still move the result in the stated
direction. A candidate that reverses it is rejected, like one that breaks a held-out number. It is a way to
tell apart answers that the plain numbers can't.

### 4.17 Comparing the paper with what the code actually did (`gapfinder/search/contrast.py`)

When no setting explains the gap, or only settings nothing supports, one AI call compares two things: the
paper's training details and hyperparameter tables, and what the trace saw the code actually do. It returns
differences, each tied to a file and line, and each is checked:
- the line must exist;
- a "literal" difference must name a number really on that line;
- the paper sentence it quotes must really be in the paper and contain the stated number.

Checked literal differences are tested as patch knobs, with the paper's value first. Differences in how the
code is structured are listed for a person, never tested: rewriting code until the number fits would
explain nothing.

### 4.18 Earning a confident label

"Explained" or "Paper-artifact inconsistency" now requires all of:
1. the search finished (the run budget didn't cut it short);
2. every setting with candidate values got at least one run;
3. the evidence comes from the paper, its documentation or the web. A line of source code only shows what the
   code does, not what the authors ran for this experiment.

Anything less is reported as "Fits but unsupported", with the reason. This rule came straight from blind-2.

**A worked example (VGAE, from the development set):**
1. The static check noticed that `mask_test_edges(adj, test_percent=30., val_percent=20.)` is always called
   without those two arguments.
2. The contrast step matched them to the paper's sentence: "The validation and test sets contain 5% and 10%
   of citation links, respectively."
3. The patch round set both to the paper's values, in memory, and the gap went from -5.8% to +0.4%.
4. All 8 numbers from the paper's table still held.

Label: Paper-artifact inconsistency, with the paper's sentence as evidence.

## Added under the no-patching rule (2026-10-18)

Each of these targets a kind of failure seen on two or more papers, or follows a published method. None was
tuned to make one paper pass.

### 4.19 Reading the paper in pieces, and names by meaning

- **The appendix gets its own reading.** One long excerpt loses its end (the SA-Bench study found the same).
  The two readings are merged, and a value the paper states beats "unstated".
- **Names by meaning.** The paper may write "number of attention heads" where the code has `n_heads`. One
  cheap AI call matches such names to the code's real settings. It may only answer with a name that exists.

### 4.20 Paper numbers against code constants (`gapfinder/search/matcher.py`)

A plain-code check, with no AI and no runs, for a paper value with no matching setting:
1. the number must appear in a sentence quoted word for word from the paper;
2. the matcher looks for a constant in the code whose name has the same core words (`num_epochs` and
   `epochs`);
3. if that constant holds a different number, it becomes a patch knob, tried with the paper's number first.

### 4.21 Building the environment (`gapfinder/env_build.py`, `gapfinder env-build`)

The hardest part of a real paper is often making its old code run at all. The builder works the way
Repo2Run does:
- pick a base image from the commit date and the build files;
- download the repository at that commit;
- ask the AI for **one** install command at a time;
- keep each command's save point only if it worked.

A failed command costs nothing, because the next one starts from the last good save point. It stops when
every library the entry scripts import loads. The kept commands are a readable recipe. `spec-draft` now also
runs the experiment twice, to check the numbers vary between runs (otherwise there is no noise to measure),
and checks memory and time against a Sandboxes VM.

### 4.22 Your reproduction against the authors' code (`gapfinder/search/difftrace.py`, `gapfinder diff`)

If you have your own reproduction and the authors' code:
1. both programs run once, with the trace on;
2. GapFinder lists every value that reached the same place differently, for example "optimizer learning
   rate: reference 0.01, yours 0.05", or "dropout: reference 0.5, yours 0.2";
3. each difference becomes a hypothesis: your setting, or your constant, set to the reference's value;
4. the authors' measured numbers are the target;
5. the usual search keeps only the differences that close the gap.

This is the setting-level version of TTrace (which compares a training implementation with a reference) and
of delta debugging (which shrinks a set of differences to the ones that matter).

## Added with plan D1-D7: six cause classes (2026-10-20/21)

### 4.23 The differential over cause classes (`gapfinder/diagnose/core.py`)

Every candidate from every class becomes a hypothesis with a predicted number for every claim. The classes:
- settings;
- reporting rules;
- library releases and the paper-era code;
- code edits;
- the data pipeline;
- **"outside every class"**: a wide, flat prediction that wins when nothing else fits.

Each hypothesis is scored by how likely the paper's numbers are under it. The likelihood includes:
- the run noise;
- the paper's own noise;
- a small **model-discrepancy** term, so an exact hit on one number by chance can't beat a close fit on all of
  them.

The report shows the top three with their evidence and how to check them. It works like a doctor's
differential diagnosis, with "none of these" as a real answer.

### 4.24 Reporting rules, read for free (`gapfinder/diagnose/reporting.py`)

Did the paper report the final epoch, the best epoch, the epoch best on validation, or the best of N seeds?
The answer is read from the per-epoch values of runs already made, without new runs. A reading that makes
every claim fit is a candidate answer: "Explained by the reporting rule". Choosing the best epoch on the test
labels is also flagged as a flaw in the paper's protocol.

### 4.25 Library releases and the paper-era code (`gapfinder/env_year.py`, `gapfinder/diagnose/library.py`)

- The packages as released on the paper's date are installed in their own directories and can be switched on
  as a knob.
- So can the repository's code as of the paper's date: the last commit before it, or the first commit when
  the repository starts after the paper.
- If switching to the old releases closes the gap, a **delta-debugging** search finds the smallest set of
  packages that matters. A binary search over releases then finds the release that changed it, and the
  signature diff shows the function.

### 4.26 Breaking ties and finding conventions

- **Discrimination** (`diagnose/discriminate.py`): when several answers tie, GapFinder picks runs at the
  paper's other reported conditions (another dataset, another sweep value) where the tied answers predict
  different numbers, by expected information gain. Ties are first broken by **paper priors**: a value the
  paper states 0.9, a mentioned setting 0.6, an unmentioned one 0.4.
- **The scale probe** (in `engine.py`): when the paper reports a sweep of a setting, it asks whether the
  paper's value is a fixed multiple of the code's (×2, ÷2, ×10, ×0.01, or +1 for counting from zero):
  - the measured curve is read on a log scale for rates and weights;
  - only factors that give whole numbers are tried for a whole-number setting;
  - the best factor, then the runner-up, are verified by running the code at the converted values.
  - A confident "Paper-artifact inconsistency" needs at least two swept claims that were off as run.
  - **Open defect:** trying several factors lets a wrong one fit by chance on noisy data.
- **Value intervals:** after the answer is chosen, its setting is bisected on both sides to the range of
  values that fit every claim.
- **Identifiability:** when other settings fit every claim just as well and no reported condition separates
  them, the report says "not identifiable from the paper's numbers". The answer plus settings that change
  nothing is not counted as a rival.

### 4.27 Looking inside the code: the mutation round (`gapfinder/search/mutation.py`)

When no setting explains everything, GapFinder makes small edits to the code, in memory, with the same hook
as the patch knobs.

**The edits:**
- ×2 and ÷2;
- swapping a mean for a sum;
- a loop bound ±1;
- flipping a comparison;
- data-loading switches (`drop_last`, `shuffle`);
- split fractions, and what a scaler is fit on;
- the training data cut to a half or three quarters.

**Where:** the edits are made at sites on the data flow of the settings the claims depend on, and above all
on the **output slice**: the statements that compute the number the program prints.

**The order:**
- the first 6 edits are the highest-priority ones;
- after that, each kind of edit takes a turn, so no kind crowds out the others;
- when none of the first edits fits, the rest are applied **in groups**, and a group that moves the numbers
  is split until the site is found.

**When an edit counts:** a fitting edit must move at least two claims that were off. Otherwise an edit right
next to the output could "fix" one number by force. A fit is always a **code lead**, never "Explained".

**The budget:** the **early code screen** runs the cheapest code tests right after the settings screen. The
**class scheduler** keeps up to 30% of the runs for code when the settings don't look likely to explain the
claims.

### 4.28 The automatic harness (`gapfinder/harness_build.py`, `gapfinder harness`)

Steps 2 to 8 of the harness are automatic:
1. data download;
2. the command that prints each claim's metric;
3. a metric parser that refuses ambiguous bindings;
4. the knobs, confirmed by the trace;
5. fitting the 3.9 GB Sandbox (shards, segments, a scaled run with an allowance);
6. self-checks (do the seeds vary? is every claim printed?);
7. the claims.

`HARNESS.md` records every choice and its reason. A person still approves it.

### 4.29 The runtime shim (`gapfinder/sandbox/runtime_shim.py`)

Loaded into every run:
- it forces CPU code paths;
- it memory-maps arrays over 50 MB (copy-on-write), so large datasets fit in the small machines.

## Built but switched off, or in versions that were not adopted

- **The code proposer** (`gapfinder/search/proposer.py`, `--code-proposer`): one Super call reads the executed
  code and the ratios between the paper's and the code's numbers, and proposes at most 3 line edits. Each edit
  is re-parsed into an in-memory patch, refused if it writes a reported number into the code, and run like any
  patch. No gain in three batches.
- **Paired seeds and adaptive repeats** (common random numbers, sequential testing): measured worse on their
  toy.
- **MDL priors:** unmeasured.
- **In c6 only** (not adopted), still in the main branch's code:
  - split sizes (`test_ratio`) as leads, with their in-between values screened;
  - the training-data fraction estimated on a log scale;
  - a switch-flip operator for layer `bias` and `affine`;
  - the proposer on unsupported fits.

Next: [Why it's built this way →](05_design_decisions.md)
