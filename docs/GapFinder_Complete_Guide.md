# GapFinder: the complete guide, in plain words

**Written for:** someone new to the project who wants to understand the whole flow, the research behind each step, what is new, and what the words mean.

**Sources:** `docs/learn/` pages 1 to 11, `docs/CONTEXT_v11.md`, `README.md`, `docs/ARCHITECTURE.md`, `PROGRESS_REPORT.md`, and the design notes. Facts are as of 24 October 2026, with the current adopted version called **c5**. Some later work (c6, c7) is mentioned where it matters. Where something was not measured, this guide says so.

---

## How to read this guide

1. Sections 1 to 3 give the problem, what you give and get, and the full flow.
2. Section 4 walks through every step: what goes in and out, the research it uses, how we used it, whether it helped, and what is new.
3. Sections 5 to 7 summarise the cause classes, what is new, and where every idea came from.
4. Sections 8 to 11 cover the testing, the comparison with other work, the history, and the limits.
5. Section 12 is the glossary. Look up any unfamiliar word there.

---

## 1. The problem, as a story

Imagine a recipe book says: "this cake comes out 10 cm tall". You follow the recipe exactly, and your cake is 6 cm. Maybe the book forgot to say "preheat the oven", or used different flour. The recipe is not lying. Something was **left out or changed**, and you have to find what.

Research papers have the same problem:
- A paper reports a number: "our method gets 1.66 error" (smaller is better).
- The authors publish their code.
- You run the code and get 0.36.

This is called a **reproduction gap**. The usual question is "does this paper reproduce?", and the answer is usually just yes or no.

**GapFinder asks a more useful question: *why* doesn't it reproduce?**

### The running example: MC Dropout

The MC Dropout paper (Gal and Ghahramani, 2016) reports Energy RMSE **1.66**. The published code, with its default settings, gives about **0.36**.

The authors later explained the difference: the paper used about 10 times fewer training rounds (`epochx=10` instead of 500), one hidden layer instead of two (`hidden=1`), and some differences inside the code that no setting can change (how hyperparameters were tuned, the batch size).

So the right answer is: "two settings explain part of it, and the rest is in the code". GapFinder v1.3 reached nearly that answer. It named the two settings, said a second number got worse, and pointed at the code lines involved. Version 1.0 had just said "Unexplained".

---

## 2. What you give GapFinder, and what you get back

| You give it | You get back |
|---|---|
| The paper (PDF or arXiv link) | A **claim ledger**: each reported result with an exact quote and page |
| The paper's code (GitHub URL or folder) | A list of **settings** the results may depend on, with evidence |
| A **harness spec**: a small YAML file saying how to build, load and run the code, and which settings may change (drafted automatically, approved by a person) | Experiments run in cloud sandboxes, one branch per hypothesis |
| Optional: the number you want explained | A **Gap Report**: one card per claim with a label, the setting that explains the gap (if any), the evidence, a noise band and held-out checks |
| | A replay command for every branch, plus a web replay |

**The labels a card can carry**, from most to least sure:

| Label | Plain meaning |
|---|---|
| **Explained** | this setting causes the gap; every check passed, and the authors plausibly used it |
| **Paper-artifact inconsistency** | the paper says one value, the code uses another, and that difference causes the gap |
| **Explained by the reporting rule** | the paper chose its number in a special way (for example the best epoch) |
| **Partially explained** | a setting closes much of the gap, with evidence, but not all of it |
| **Fits but unsupported** | a setting fits the numbers, but nothing shows the authors used it. A strong guess |
| **Explains target, conflicts with held-out** | it fixes the main number but breaks another one |
| **Inconclusive** | the measurements are too noisy to decide |
| **Reproduced** | the code already matches the paper |
| **Unexplained** | nothing GapFinder can change explains the gap. This is a valid, honest answer |

**Hard limits:** GapFinder changes *conditions* only (settings, data choices, build options, environment, and constants patched in memory). A **diff guard** blocks any edit to the algorithm's code. Sandboxes machines have 4 CPU cores and 3.9 GB of memory, so it works on CPU-only papers.

---

## 3. The full flow, from input to output

```
 INPUT                                                          OUTPUT
 ┌──────────────┐
 │ Paper (PDF)  │──► Step 1  Claim ledger ───────────────┐
 └──────────────┘        (what results are claimed?)     │
 ┌──────────────┐                                        ▼
 │ Code (repo)  │──► Step 2  Repo map ──► Step 3  Links and trace
 └──────────────┘       (what knobs exist?)  (which words mean which knob,
                                              what does each knob do?)
 ┌──────────────┐                                        │
 │ Harness spec │──► Step 0  (how to build, load, run)   ▼
 │ (YAML)       │                              Step 4  Assumption space
 └──────────────┘                              (what might matter?)
                                                         │
                                                         ▼
                                              Step 5  Hypotheses, six cause classes
                                                         │
                                                         ▼
                                              Step 6  Checkpoint tree (sandboxes)
                                              build once, load once, fork many
                                                         │
                                                         ▼
                                              Step 7  Search, in rounds:
                                              screen → confirm → combine → bisect
                                              → discriminate → scale probe
                                              → patch round → mutation round
                                                         │
                                                         ▼
                                              Step 8  Patch round (code constants,
                                              changed in memory only)
                                                         │
                                                         ▼
                                              Step 9  Verify: revert, held-out,
                                              history matching, evidence,
                                              identifiability
                                                         │
                                                         ▼
                                              Step 10 Gap Report + replay  ──► Verdict per claim
```

The search (step 7) is the only branching stage. Everything else runs in a straight line.

---

## 4. Step by step

Each step covers: **In/Out**, **What it does**, **Research it uses (SOTA)**, **How we used it**, **Did it help?**, **Cross-domain idea**, and **What is new**. Where a part does not apply, it is left out.

### Step 0. Harness spec (once per repo)

- **In:** the code repo. **Out:** a YAML file with build, load and run commands, the knobs, and the folders a run may write to.
- **What it does:** turns a messy research repo into something a program can run.
- **Research used:** Repo2Run (Hu et al., 2025). An AI proposes one install or run command at a time. A command is kept only if it worked, and a failed command rolls back to the last good save point.
- **How we used it:** `gapfinder harness` and `env-build` draft the spec. `spec-draft` runs the experiment twice to check that numbers vary (otherwise there is no noise to measure) and checks memory and time against a Sandboxes machine. A person approves the spec. This is the one human checkpoint.
- **Did it help?** On two small test artifacts the drafted spec ran unedited and found 13 of 13 and 14 of 14 knobs. It rebuilt 5 of 6 reproduced papers' harnesses without a person. On an unseen repository it ran unaided about 2 times in the last 6. It has **not** yet run end to end on a new repository.
- **Is it new?** The layers (build, dataset, config, workload, environment) are ours. They decide where each branch forks from, which saves setup time.

### Step 1. Claim ledger (what does the paper claim?)

- **In:** the paper's text and tables. **Out:** each claim with its number, unit, conditions, page, and an exact quote.
- **What it does:** lists every result the paper reports, so each one can be checked.
- **Research used:**
  - Large language models (Nemotron 3 Ultra) do the reading. A second, smaller model (Nemotron 3 Super) removes text that is not a result.
  - **HyperPIE** (Saier et al., ECIR 2024) showed that LLMs are weak at linking a value to what it applies to. So we do not trust the reading. We check it.
  - **SciTab** (2023) showed that LLMs make mistakes on quantitative claims in scientific tables.
- **How we used it:** a quote that does not match the PDF text is **dropped, never repaired**. Numbers are matched in any spelling ("0.91", "91%"). Tables are read from both the LaTeX source and the PDF, and only cells the two agree on are trusted.
- **Did it help?**
  - On RusKey, 17 extracted claims were dropped as ungrounded, so the model cannot invent evidence.
  - Re-grounding saved ledgers recovered about 350 claims that had been dropped, and dropped none new.
  - RusKey ledger: claim precision 1.00 (40 of 40, on the paper the prompts were tuned on), headline-claim recall 1.00, all-claim recall 0.93.
  - Setting recall was 0.67 on RusKey, below our 0.80 bar. The tuner's mode flags were missed.
  - The LaTeX source exists for about 93% of the papers checked.
- **Cross-domain idea:** the table check is "double entry" from accounting. Two independent records must agree before one is trusted.
- **Is it new?** The "drop, never repair" rule and numeric grounding in any spelling are ours.

### Step 2. Repo map (what knobs does the code have?)

- **In:** the repo. **Out:** every command-line flag, config key and environment variable, with its default and its file and line.
- **What it does:** reads the code without any AI. It finds `argparse`, `gflags`, `absl` flags, YAML keys and environment variables.
- **Research used:** ordinary static program analysis.
- **How we used it:** it also keeps commented-out blocks of settings as alternatives to try whole. A helper called **config flow** follows the code a little further. For example, it notices that `--epochx` *multiplies* the base number of epochs, so 10 is a natural value to try.
- **Did it help?** Missed knobs show up here. On FastGCN the repo map did not read `tf.app.flags`, so only one learning-rate knob was screened. The RippleNet alternative block turned out to be its real answer (learning rate and L2 together).
- **Is it new?** Using the repo's own commented-out alternatives as candidate values.

### Step 3. Links and trace (which words mean which knob, and what does each knob do?)

- **In:** paper terms and the repo map. **Out:** a mapping from paper terms to code knobs, and a record of what each knob changes when the program runs.
- **What it does:**
  - **Links:** matches paper words to flags. "Learning rate" is matched to `--lr`, then checked by what the value does at runtime.
  - **Trace:** runs the program once with a small hook, and records where each value lands (the optimizer's step size, a dropout layer, a loop length). Each knob gets a role: rate, fraction, size, count, multiplier, or seed.
- **Research used:**
  - **BM25**, a classic search-ranking formula, with a small lexicon of machine-learning words.
  - The idea of following configuration values through a running program comes from systems research on misconfiguration (**ConfAid**, **X-ray**).
  - A **lesion** check (switch a knob off and see what changes) is an old idea from neuroscience.
- **How we used it:** the trace gives each knob a sensible range of values. A rate gets steps of ×10 and ÷10, a fraction stays between 0 and 1, and a random seed is never tried, because seeds are noise, not causes. If two knobs share a value so nobody can tell which reached the call, GapFinder says "ambiguous" and does not guess.
- **Did it help?**
  - 86% of the first guesses were right on a 47-term test set. The decisive links were 9 of 9.
  - The trace found FastGCN's learning rate and epochs by watching them.
  - Before the trace, learning rates were sometimes treated as fractions (0.91 instead of 0.009). Roles fixed that.
- **Is it new?** The dry-run trace that records where values land in the program. Standard tools do not do this.

### Step 4. Assumption space (what might the result depend on?)

- **In:** the paper's setup section, the appendix (read in its own call), the repo map and 10 to 30 relevant files. **Out:** a list of assumptions. Each has a knob, a layer, the paper's stated value or "unstated", the code's default, candidate values, evidence (a quote or file:line), and a prior score.
- **What it does:** lists the settings that could explain a gap, with evidence for each.
- **Research used:** the reproduction-study literature. Raff (2019), Gundersen et al. (2022) and Fostiropoulos et al. (2023) found that missing hyperparameter details are a main cause of failed reproductions. That is why this step exists.
- **How we used it:**
  - The status of each setting (stated and matches, stated but code differs, unstated) is computed by code, not by the model.
  - "Stated but code differs" is kept as its own finding: a paper–code inconsistency.
  - The appendix gets its own reading. Long text loses its end (SA-Bench found the same). GraphMAE's first run never saw the appendix table that stated the true cause.
  - The AI may **reorder** what gets tested, but never **exclude** a setting. GraphMAE's true setting was skipped as "already matching the paper" because the reading was wrong. That is why exclusion is now forbidden.
- **Did it help?** The appendix reading is a direct fix from a real miss. Its effect on new papers is not yet measured.
- **Is it new?** The "stated but code differs" status as a finding, and the rule that AI reading may never exclude a setting.

### Step 5. Hypotheses in six cause classes (what should we test?)

- **In:** assumptions, spec knobs and trace roles. **Out:** a ranked list of hypotheses. Each one is a single change to test.
- **What it does:** turns the assumptions into tests, covering six classes of cause (see section 5 for the full table):
  1. **Settings:** flags and config values.
  2. **Reporting rules:** how the paper picked its number (the final epoch, the best epoch, the best on validation data, the best of N seeds).
  3. **Library and paper-era code:** package releases and the code commit from the paper's date.
  4. **Code defects:** small edits, such as a changed constant or a flipped operator.
  5. **Data pipeline:** how training data is cut or prepared.
  6. **Outside every class:** an honest default when nothing fits.
- **Research used:**
  - **Mutation testing** (for code defects). Tools such as mutmut and the fault-localisation methods MUSE and Metallaxis.
  - **Delta debugging** (Zeller and Hildebrandt, 2002), for finding the smallest set of packages or changes that matters.
  - **DeepCrime** (Humbatova, Jahangirova and Tonella, 2021), a set of fault types taken from real deep-learning bugs, such as removing training data or a bias.
  - Medical **differential diagnosis**: a ranked list of possible causes, with "none of these" as a real answer.
- **How we used it:**
  - Reporting rules are read from runs already made, at zero cost.
  - Library and era candidates are switched on as knobs, then searched with delta debugging and a binary search over releases.
  - Mutations are small: ×2, ÷2, mean to sum, a loop bound ±1, a flipped comparison, a data-loading switch, or cutting the training data to a half or three quarters.
  - Each candidate is scored by how likely the paper's numbers are under it, including a small allowance for model discrepancy.
- **Did it help?**
  - Code defects: 0 of 7 found by version c1, 2 of 6 by c3.
  - Data-pipeline cuts: 0 of 13 by c1, 1 of 4 by c5.
  - Reporting rules: 1 of 1.
  - Paper-era code and library releases: never plantable on our papers, so never tested.
- **Is it new?** Framing the search as six cause classes. Most tools search settings only.

### Step 6. Checkpoint tree (Token Factory Sandboxes)

- **In:** the harness spec. **Out:** saved states: source, built, loaded, then one fork per hypothesis.
- **What it does:** build the code once, load the data once, save the state. Every test then starts from the right save point. This is called **forking**.
- **Research used:** snapshot trees in Token Factory Sandboxes, where each saved state has a **content-addressed ID** (the ID is computed from the contents, so identical states get identical IDs).
- **How we used it:**
  - A config change forks from the loaded database. A dataset change reloads from the build. A build flag rebuilds.
  - **Noise setups:** with `--noise-setups N`, the database is loaded N times with the same command. If the IDs differ, the noise band must widen.
- **Did it help?**
  - Fork vs no fork, same search of 22 branches: 8 loads instead of 22. Reported cost $4.48 instead of $8.07, about 45% less. Sandboxes costs are reported, not billed, during the beta.
  - RusKey: 5 identical loads gave 5 different checkpoints. Across 12 loads the naive K1/K5 ratio ranged from 0.52 to 1.38.
- **Cross-domain idea:** database benchmarking pitfalls. Didona et al. (VLDB 2021) and Luo and Carey (VLDB 2020) show that LSM-tree results vary a lot from load to load. Forks from one load share one hidden random draw, which is **pseudo-replication** (fake independent repeats). That is why the noise band must include load-to-load variation.
- **Is it new?** Using the content ID as a test of whether a setup is reproducible at all.

### Step 7. Search (which change closes the gap?)

- **In:** the hypothesis list and a fixed run budget (`--max-runs`). **Out:** survivors, a combination, and a minimal set of changes.
- **What it does, in rounds:**
  1. **Noise calibration.** Repeat the default setup. An effect counts only if a bootstrap interval (a resampling test) excludes zero.
  2. **Screen.** One change per run, coarse values first. Finer values are tried only for settings whose coarse values moved the result at all. A **25% escrow** of the budget is kept for later confirmation.
  3. **Confirm.** Everyone gets 2 runs, then only the best half gets the full repeats. This is a **race**, where losing candidates are dropped early.
  4. **Group screening.** When nothing fits, several unmentioned flags go into one pooled run. A flat pool is pruned whole.
  5. **Combine.** The best knobs are tried in pairs. Once a combination fits every claim, only candidates inside the tie margin get confirmation runs.
  6. **Bisect.** Remove knobs one at a time to find the smallest set that still closes the gap. This is delta debugging. The name comes from `git bisect`.
  7. **Discriminate.** When two settings tie, run them at the paper's *other* reported conditions (another dataset, another sweep value), where they predict different numbers. Keep the most informative runs.
  8. **Scale probe.** Tests whether the paper's value is a fixed multiple of the code's, such as "10 times more iterations" or "the code's 2 times v".
  9. **Patch round.** Hard-coded numbers are changed in memory (step 8).
  10. **Class scheduler.** When no setting looks likely, up to 30% of the runs go to code tests.
  11. **Triage.** When every run of a value fails, a model reads the error. If the program rejected the value, one valid value is tried. The model's suggestion is trusted only when the error really shows a rejection.
- **Research used:**
  - **Racing** (Maron and Moore, 1994, "Hoeffding races"; Birattari's F-race).
  - **Successive halving and Hyperband** (Jamieson and Talwalkar, 2016; Li et al., 2017), for cheap screening runs first.
  - **Group testing** (Dorfman, 1943) and **sequential bifurcation** (Bettonvil and Kleijnen, 1997), for pooled screening.
  - **Delta debugging** (Zeller and Hildebrandt, 2002), for bisection.
  - **Optimal experimental design for model discrimination** (Box and Hill, 1967; Lindley, 1956), for tie-breaking runs.
  - **Value intervals:** level-set estimation (Gotovos et al., 2013) and probabilistic bisection (Frazier et al., 2019).
  - **Class scheduling** comes from Bayesian search theory, used to find lost ships and planes (Koopman; Stone, 1975).
  - **Early code screen** comes from the value of information in sequential diagnosis (de Kleer and Williams, 1987).
- **How we used it:** the search is built for an expensive oracle, where each run costs minutes of sandbox time. The rounds are ordered so the cheapest, most likely answers come first. Ties are broken by **paper priors**: a value the paper states gets 0.9, a mentioned setting 0.6, an unmentioned one 0.4.
- **Did it help?**
  - Racing kept budget for combining. Repeats were given to the leaders, not everyone.
  - The forward step (pairing the best setting with every value of the others) was added for interactions. Interactions are still unsolved: 0 of 12 full-pipeline runs.
  - Group screening, inside a bundle of version-c3 changes: 6 of 13 tasks solved against 4 of 13, better on 2 and worse on 0. The sign test gives p = 0.5, so it is not significant.
  - Ties remain the main reason settings are missed. About 3 in 10 planted settings were found.
- **Is it new?** The scale probe, the class scheduler, and how the rounds are arranged for an expensive oracle.

### Step 8. Patch round (test a code constant without editing a file)

- **In:** constants found in the code, such as `batch_size = 128`. **Out:** a test run with the constant changed, in memory only.
- **What it does:** a small AST transformer runs inside the child process. The program imports its module, the transformer reads the source, swaps one literal (for example 128 becomes 32), compiles the changed version in memory, and runs that. The file on disk never changes.
- **Research used:** mutation testing tools (mutmut) and Python's import hooks (PEP 451). Durable-execution systems (ModShim, AutoKitteh) use the same trick.
- **How we used it:**
  - A small helper file (`sitecustomize.py`) is loaded automatically when Python starts.
  - If the line does not contain the expected number, the run fails loudly, so a wrong patch can never look like a result.
  - A patch is reported only if it makes **every** claim fit after repeats, and it is always reported as a **code change**, never as a setting.
  - The patch round has its own share of the budget.
- **Did it help?**
  - MC Dropout (not blind): the batch-size patch was the only constant that moved the held-out Yacht claim. With batch 64 and the pair, Yacht gave 1.18 against the paper's 1.11.
  - VGAE (development case): the paper's 5% and 10% splits were matched to the code's 30 and 20, and the gap went from -5.8% to +0.4%. All eight paper numbers still held.
  - RippleNet: the planted `np.mean` to `np.sum` edit was found.
- **Cross-domain idea:** mutation testing checks test suites by changing code in memory. We use it to check a paper's numbers.
- **Is it new?** Using in-memory mutation as a diagnostic for reproduction gaps. Mutation testing normally checks test suites, not papers.

### Step 9. Verify (is the answer real?)

- **In:** the best candidate and its run. **Out:** a label and the checks behind it.
- **What it checks:**
  1. **Revert (counterfactual).** Undo the change. The gap must come back. If it does not, the change was not needed.
  2. **Held-out claims.** Other numbers from the paper must not get worse beyond noise.
  3. **History matching.** Test every configuration against every claim at once. Each claim gets an *implausibility* score: how far the paper's number is from what that configuration gives, counting all the noise. Over 3 means ruled out. If every claim fits some configuration but none fits all, the claims contradict each other under every setting, so the cause is "out of space suspected". If some claim fits nothing at all, it is "out of space likely".
  4. **Identifiability.** If other knobs fit every claim just as well, the report says "not identifiable from the paper's numbers". The chosen answer and settings that change nothing do not count as rivals.
  5. **Evidence.** Is there a quote from the paper, its docs or the web showing the authors used this value? A line of source code only shows what the code does, not what the authors ran. Without evidence the best label is "Fits but unsupported".
  6. **Confidence cap.** A finished search can earn a confident label only with evidence beyond the code.
- **Research used:**
  - **Equifinality** (Beven and Binley, 1992, GLUE; Beven, 2006): many different settings can fit one number equally well.
  - **Practical identifiability** (profile likelihood; Raue et al., 2009).
  - **History matching** (Craig et al., 1996 and 1997; Vernon et al., 2010): rule out implausible settings, with the 3-sigma cutoff from Pukelsheim's rule. The goal is to rule out regions, not to find one best setting.
  - **Model discrepancy** (Kennedy and O'Hagan, 2001): when no setting can reach the data, the model itself is wrong.
- **Did it help?**
  - Without verification, 7 of 24 GapBench runs were confidently wrong. With verification, 0 of 24.
  - MC Dropout (not blind): history matching labelled the cause "out of space", which matches the authors' explanation.
  - A discrepancy allowance of 5%, meant for scaled-down reproductions, had silently blocked every real paper from reaching "out of space". Setting it to 1% fixed that.
- **Is it new?**
  - Applying history matching to ML papers to say "no setting can explain these claims, look in the code". The method is decades old; this use is new here.
  - The **label rules**: "Fits but unsupported" kept apart from "Explained", and a confident label must be earned.

### Step 10. Gap Report and replay (what do you get?)

- **In:** everything above. **Out:**
  - One card per claim, with a verdict label, the paper's number with its quote, what we measured, the noise band, and the checks.
  - A **provenance** block: code hash, model and prompt hashes, spec hash, cost.
  - A replay command for each winning run.
  - A web replay, which plays a recorded run at 1×, 4× or 16× at no cost.
- **Rule:** when the budget runs out, nothing unconfirmed is labelled.
- **Is it new?** The replay is the default landing page, so a judge sees the result without running anything.

---

## 5. The six cause classes at a glance

| Class | What it means | Example | How it is tested | How well it has worked so far |
|---|---|---|---|---|
| **Settings** | a flag or config value differs | `epochx=10` | screen, confirm, combine, bisect | about 3 in 10 planted settings found; most misses are ties |
| **Reporting rule** | the paper picked its number specially | best epoch on the test labels | read from runs already made, zero cost | 1 of 1 planted |
| **Library and paper-era code** | a package release or old commit changes the result | an API that changed between releases | delta debugging over packages, binary search over releases | never planted, so untested |
| **Code defect** | the code computes something slightly different | `np.mean` where `np.sum` belongs | patch round and mutation round, in memory | rare; first found in c3 (2 of 6) |
| **Data pipeline** | the training data is cut or prepared differently | a 60% training cut; an edge counted twice | training-data cut and data-loading mutants | 1 of 4 cuts (c5) |
| **Outside every class** | none of the above | a bug the tool cannot model | the honest default | works: correct "Unexplained" on tasks with no cause |

A **scale convention** ("the paper's v is the code's 2 times v") is not its own class. It is a setting-level effect found by the scale probe, and it has been the most reliable family (mostly found).

---

## 6. What is new in GapFinder

These are our own choices. No published work we found does exactly this.

1. **The whole loop.** Claims read with exact quotes, then forked sandbox runs, then a differential over six cause classes, then a report that can say "outside every class".
2. **Six cause classes**, not settings only.
3. **Drop, never repair.** A claim or assumption whose quote is not in the source is removed.
4. **The scale probe:** finding that a paper's value is a fixed multiple of the code's, from a sweep the paper reports.
5. **A reporting-rule probe** read at zero cost from per-epoch values.
6. **Content IDs as a measurement:** identical load IDs show the setup is reproducible; a difference widens the noise band.
7. **History matching applied to ML papers**, to say "look in the code".
8. **In-memory code tests** through an import hook, so no file is edited.
9. **Confidence rules:** a confident label needs a finished search, every setting tried, and evidence beyond the code. A code fix is never "Explained".
10. **Labels** that separate "Fits but unsupported" from "Explained", and "Explains target, conflicts with held-out" from "Unexplained".
11. **A planted-gap curriculum** on papers that already reproduce, with controls, sealed answers, and a generator kept separate from the engine it tests.
12. **A class scheduler** that keeps part of the budget for code tests.
13. **A training-data cut measured from one run** on a log scale, instead of a fixed half or three quarters.

---

## 7. Where every idea came from

The table below lists each technique, its origin, whether it is on in c5, and whether it helped. "Toy only" means it passes its own small test and nothing more is known. "Not measured" means we have no separate result.

| Technique | Where it comes from | Used for | On in c5? | Did it help? |
|---|---|---|---|---|
| Claim ledger with exact quotes | ours | reading claims | yes | it is the input to everything |
| Numeric grounding in any spelling | ours | keeping claims | yes | recovered about 350 dropped claims |
| Table double-check (LaTeX and PDF) | double-entry accounting | reading tables | yes | source exists for about 93% of papers |
| Appendix read separately | a known long-text failure | reading | yes | fixes GraphMAE's miss |
| BM25 word matching | Robertson and Zaragoza | paper words to flags | yes | 86% right first guess |
| Runtime trace of values | ConfAid, X-ray (misconfiguration research) | knob roles, value ranges | yes | found FastGCN's learning rate and epochs |
| Static code checks | hidden choices in ML code (Kapoor and Narayanan, 2023) | code leads | yes | found MC Dropout's batch size |
| Repo map | ordinary program analysis | knob list | yes | RippleNet's real answer |
| Value ladder | ours (a coarse-to-fine grid) | candidate values | yes | true value tried in 12 of 15 runs after it |
| Secant step | the secant method | values between two tried points | yes, guarded | first version made wrong exact fits: 102 down to 92 of 138 on the dev suite; the guard fixed it |
| Paper priors | ours | tie-breaks | yes | not measured |
| Minimum description length | Rissanen, 1978 | tie-breaks | **no** (built, off) | not measured |
| Forking from checkpoints | Token Factory Sandboxes feature | running | yes | 8 loads instead of 22 (RusKey) |
| Noise calibration | standard experimental practice | noise band | yes | found RusKey's loads differ |
| 1% noise floor | ours | "Reproduced" | yes | kept after an outside review |
| Diff guard | ours | no algorithm edits | yes | keeps answers meaningful |
| In-memory patches | ours, like mutation testing tools | constants, defaults | yes | VGAE found end to end |
| Shards and segments | checkpoint and restart | long jobs | yes | long papers fit |
| Memory-mapped arrays | an operating-system technique | big datasets | yes | not measured on a paper |
| Environment builder | Repo2Run (Hu et al., 2025) | install commands | yes | about 2 of the last 6 unseen repos |
| Screen, confirm, combine, bisect, verify | factor screening in experiment design | the search | yes | the backbone |
| Racing | Maron and Moore, 1994; Birattari's F-race | repeats for leaders | yes | kept budget for combining |
| Short screening runs | successive halving; Hyperband | cheap first screens | yes | not measured alone |
| Bisecting combinations | delta debugging (Zeller and Hildebrandt, 2002) | removing extra settings | yes | standard |
| Escrow (25% kept) | ours | confirmation | yes | MC Dropout's pair was lost to budget before it |
| History matching | Craig et al., 1997; Vernon et al., 2010; Pukelsheim's 3-sigma rule | in space vs out of space | yes | turned MC Dropout's "Unexplained" into "look in the code" |
| Model discrepancy | Kennedy and O'Hagan, 2001 | exact-hit guard | yes | the exact-hit guard |
| Six-class differential | medical differential diagnosis; Bayesian model comparison | scoring causes | yes | lets the report say "probably the code" |
| Discriminating runs | Box and Hill, 1967; Lindley, 1956 | breaking ties | yes | helps only when the paper reports such conditions |
| Equally good configurations | Occam's razor; equifinality (Beven and Binley, 1992) | listing ties | yes | honest, does not raise the score |
| "Not identifiable" note | practical identifiability (Raue et al., 2009) | saying ties cannot be broken | yes | honest, does not raise the score |
| Value intervals | Gotovos et al., 2013; Frazier et al., 2019 | range that fits | yes | scorer counts values inside the range |
| Minimum detectable effect | statistical power analysis (Cohen) | Inconclusive | yes | correct abstentions on small gaps |
| Common random numbers | variance reduction in simulation | paired seeds | **no** (built, off) | on its toy: 11 found vs 13 without it; one confident mistake |
| Sequential testing (SPRT) | Wald, 1945 | adding repeats | **no** (built, off) | on its toy: 12 vs 13, no gain |
| Scale probe | ours | "the paper's v is the code's c times v" | yes | most reliable family; open defect: a wrong factor can fit noisy data by chance |
| Reporting-rule probe | Dodge et al., 2019 ("Show your work") | best epoch, best seed | yes | 1 of 1 planted |
| Paper-year packages, paper-era commit | software-history mining; git bisect | library and era | yes | toy only; never plantable |
| Patch round | program repair | constants in memory | yes | VGAE; RippleNet |
| Grounded operation swaps | ours | paper says ELU, code uses ReLU | yes | toy |
| Paper against trace | ours | literal differences, checked | yes, when a paper is given | VGAE |
| Mutation round | MUSE (Moon et al., 2014); Metallaxis (Papadakis and Le Traon, 2015) | code defects | yes | first planted code defect (c3) |
| Output slice first | thin slicing (Sridharan et al., 2007); program slicing (Weiser, 1981) | ranking edits | yes | part of c3 |
| Group screening of mutants | Dorfman, 1943; Bettonvil and Kleijnen, 1997; Wang et al., 2021 | many edits at once | yes | toy only |
| Interference control | interference in mutation-based fault localisation | a fix must move two claims that were off | yes | removed a confident wrong path on a toy |
| Data-pipeline mutants | ours, from common ML evaluation mistakes | drop_last, shuffle, splits | yes | PatchTST's real cause was drop_last |
| Training data cut | DeepCrime (Humbatova et al., 2021) | data pipeline | yes | 1 of 4 planted cuts (c5) |
| Operator classes take turns | Zhang et al., 2013 | fair mutant order | yes | fixed a lost planted constant (seed 5) |
| Class scheduler | Bayesian search (Stone, 1975) | budget across classes | yes | toy; part of c3 |
| Early code screen | value of information (de Kleer and Williams, 1987) | early code tests | yes | toy; part of c3 |
| Code proposer (AI edits) | Agentless (Xia et al., 2024); AutoFL | edits when nothing fits | **no** (built, off) | no gain in three batches |
| Three checks before "Explained" | counterfactual reasoning; held-out checks; evidence (ours) | confident labels | yes | 7 of 24 vs 0 of 24 confidently wrong |
| Confident label must be earned | ours, after GraphMAE | label rules | yes | nothing confidently wrong on real papers since |
| Sealed tests and pre-registration | clinical trials; hash commitments | fair testing | yes | the only way the numbers mean anything |
| GapBench | ours | fake papers with a planted cause | yes | main comparison with a coding agent |
| Dev suite | regression testing | free check on public tasks | yes | caught two regressions |
| Planted-gap curriculum | fault injection; DeepCrime; curriculum learning | development measurement | yes | showed which gaps are found, and its own flaws |
| Controls | placebo controls | tasks with nothing planted | yes | 0 wrong answers on 69 control searches |
| Frozen operators in the generator | ours, after a mistake | no circular tasks | yes | fixed seed 5's circular result |
| Credible set and MRR | fault-localisation metrics | scoring ties | yes | cause in a small set more often in c5 |
| Sign test | standard statistics (McNemar's test) | comparing versions | yes | no version comparison was significant |

---

## 8. Compared with the state of the art

**Short answer:** nobody has published a system that diagnoses *why* a paper's code misses its numbers. So there is no state of the art to beat head to head. The closest work solves neighbouring problems.

### 8.1 Closest work on the same task (reproduction)

| Work | What it does | Best result reported |
|---|---|---|
| PaperBench (Starace et al., ICML 2025) | agents rebuild 20 ICML papers from scratch | best agent: 21% of the grading rubric |
| RECLAIM (2026) | agents reproduce papers' claims from released code | best agent: 41% when code, data and weights are released, 27% when the model must be trained, 12% with no code |
| REPRO-Bench (2025) | agents judge whether social-science results reproduce | best agent about 21% accuracy, below the 25% of guessing |
| CORE-Bench (2024) | agents run a study's code and report results | not collected here |

None of these answers *why* a gap exists, so their numbers cannot be compared with ours. They show that reproducing a paper is already hard for today's agents, and diagnosing a gap is a step further.

### 8.2 Neighbouring fields, and what we borrowed

| Field | Best-known methods | What GapFinder borrows | Compared? |
|---|---|---|---|
| Fixing bugs in code (SWE-bench) | Agentless solves 32% of SWE-bench Lite | the loop of localise, propose, check; our "test" is the paper's numbers | no. We have no test suite, only noisy numbers |
| Finding the buggy line (fault localisation) | AutoFL is about 20% better than Ochiai at top-1 on Defects4J; AgentFL finds 157 of 395 bugs at top-1 | mutation-based localisation (MUSE, Metallaxis), program slicing | no. Our code-defect results are weak (2 of 6), so we are probably worse on their benchmarks |
| Misconfiguration in computer systems | PeerPressure (right in 12 of 20 real cases), ConfAid, EnCore | tracing where values go | no |
| Calibrating simulators to data | history matching; Bayesian calibration with model discrepancy; ensemble methods | history matching and the discrepancy term, used directly | no. Used as published |
| Data checks in production ML | TensorFlow Data Validation (Google) | not used. Our planted changes sit on the paper's side, so checks of our own runs find nothing | no |
| Mutation testing for deep learning | DeepCrime's operators from real faults | its operators, to plant faults and to search | no |

### 8.3 What was measured head to head

Only one comparison exists: **GapBench**, our generator of small fake papers. The comparison was a general coding agent (mini-swe-agent, Nemotron 3 Super), with the same inputs and the same dollar cap.

| Test | GapFinder | Coding agent |
|---|---|---|
| Confidently wrong, three sealed tests (90 runs) | **0 of 90** | 49 of 90 |
| Blind test, confidently wrong (8 tasks, run twice, 24 runs each) | **0 and 0** | 14 and 12 |
| Tasks solved in the median run (of 8, run twice) | **4 and 6** | 1 and 2 |
| GapBench dev (4 tasks) | 4 of 4, no false attribution, $0.04 a task | 2 of 4, 50% false attribution, $0.07 a task |

**How strong is this?**
- **Strong on safety.** 0 against 49 confident mistakes is a large difference, on sealed tasks.
- **Weaker on finding causes.** The sets are small (15 runs with a cause per test) and the intervals overlap. Random hypothesis order (9 of 15) and no evidence check (8 of 15) found as many causes as the full pipeline (5 to 7 of 15). So the ranking and the evidence rule cost recall on these tasks. What they buy is safety.
- **Limited scope.** The baseline used a mid-sized model. A coding agent on a frontier model was never tried. The tasks are toys.

### 8.4 What has not been measured

- Real papers against any other system. Our blind record is 1 correct, 1 partial, 5 missed and 1 confidently wrong, out of 8 sealed papers. All 8 predate the work since 20 October.
- Our parts against the best tools in their own fields. The mutation round was never run on a standard fault-localisation benchmark, and the environment builder was never compared with Repo2Run.
- Whether the planted curriculum reflects real papers. It plants random causes into papers that already reproduce. Real causes are not random.

### 8.5 The verdict in plain words

- **Better than a general coding agent at not being confidently wrong**, clearly, on synthetic tasks.
- **Not shown to be better than anything at finding causes on real papers.** Nothing to compare against yet, and our own rate is low.
- **Works today on:** scale and unit conventions; settings when the paper reports enough numbers to tell them apart; honest abstention.
- **Weak on:** code defects; ties on few numbers; and, as seed 7 showed, the scale probe can be confidently wrong when it tries many factors on noisy data.

---

## 9. How we test it

### 9.1 The practice bench: GapBench

GapBench is a set of small artificial papers, each with a secret cause:
1. Take a small program: a CartPole reinforcement-learning agent (`rlbench`) or a logistic-regression classifier (`mlbench`).
2. Secretly change a setting (say `normalize=minmax`) and run it. Those numbers become "the paper's numbers".
3. Write a short fake paper that reports those numbers but does not say which setting was used.
4. GapFinder gets the fake paper and the program with default settings, and must find the hidden setting.

| Category | What is planted | Right answer |
|---|---|---|
| known cause | one setting | name it |
| decoy | one setting, plus a tempting wrong one | name the right one, avoid the decoy |
| interaction | two settings that only matter together | name both |
| no cause | nothing; the numbers are shifted or just noisy | "Unexplained" or "Inconclusive" |
| incomplete | a setting GapFinder may not change | do not blame something else |
| out of space | a bug in an older copy of the code | say it is outside the settings |

A generator makes the tasks and **rejects** any task where the gap is smaller than three noise bands, or where another setting fits the claims just as well (the answer would not be findable).

### 9.2 Sealed tests: how we avoid fooling ourselves

1. **Freeze** the code with a git tag.
2. **Write the success criteria first** (`eval/gapbench/PROTOCOL.md`).
3. **Make a random seed after the freeze.** The seed decides the tasks, so nobody could tune toward them.
4. **Generate** the tasks. Answers go into a sealed folder; only a fingerprint (hash) is published.
5. **Run** GapFinder and the comparison arms three times on every task.
6. **Reveal**, check the fingerprint, and score.

The arms: **gapfinder** (full system); **gapfinder-noverify** (no three checks); **gapfinder-noevidence** (no evidence check); **gapfinder-random** (random order instead of the AI's ranking); **baseline-super** (a general coding agent).

### 9.3 Sealed results on GapBench

| Test | Confidently wrong (of 30) | Correct causes (of 15) | Correct "nothing to blame" (of 15) | Balanced accuracy |
|---|---|---|---|---|
| v1.1 | 0 | 7 (+1 partial) | 15 | 0.73 |
| v1.2 | 0 | 12 | 15 | 0.90 |
| v1.3 | 0 | 9 (+1 partial) | 15 | 0.80 |

The coding-agent baseline was confidently wrong in 19, 8 and 22 of 30 runs.

**How to read these honestly:**
- "Confidently wrong" comes first. It is the error that hurts users. 0 in 90 runs is the strongest result.
- Balanced accuracy averages "found the cause when there was one" and "blamed nothing when there was none". Always saying "Unexplained" scores 0.50, so 0.50 is the floor.
- The sets are small: 15 runs with a cause, over 5 tasks. Different tests draw different difficulty, so 12 then 9 does not mean v1.3 got worse.
- The dev suite compares versions on the same public tasks. Most engine changes after v1.1 were within noise. Only the safety result is clear.

### 9.4 Real papers: three kinds of test

| Kind | What it means | Results |
|---|---|---|
| **Known answer** (MC Dropout, the development set) | the cause is documented and known; useful for building, but every success may come from tuning to it | MC Dropout names the documented settings; VGAE found end to end; pygcn honestly "Unexplained" |
| **Frozen batch** | papers with known causes; the code is frozen first and the harness writers do not see the causes | devbatch-1 (5 papers): 1 correct, 0 confidently wrong. devbatch-2 (3 papers): 0 found, 3 correct abstentions |
| **Sealed blind** | another model picks the paper and seals the answer; GapFinder is frozen; the key opens only after the run is committed | 8 papers: **1 correct** (Fair Clustering: the paper's λ=10 is wrong, the authors used 100), **1 partial** (RippleNet, the learning rate), 5 missed, **1 confidently wrong** (GraphMAE) |

Only the sealed blind cases count as proof. All 8 were run before 20 October 2026, so none of the work since (six cause classes, the planted curriculum, versions c1 to c6) has blind evidence yet.

### 9.5 The dev suite: a free regression check

`eval/dev_suite.py` re-runs the search on every public GapBench task (69 runs with a cause, 57 without) for free. `eval/compare_suites.py` compares two versions task by task with a sign test.

| Version | Cause runs correct (of 138) | Confidently wrong |
|---|---|---|
| c1 | 100 (two replicates) | 0 |
| c4 | 96 | 0 |
| c5 | 99 | 0 |
| c6 | 97 | 0 |

Identical code swings by about ±5 per run, so these are the same within noise. Every run got all 57 abstentions right. It guards against regressions; it is too easy to show progress.

### 9.6 The planted-gap curriculum

Documented reproduction gaps are rare, so measuring on them is slow. Since 21 October 2026 the main development measurement plants hidden changes into papers whose code already reproduces.

**How a task is made:**
1. **Papers:** six that already reproduce: pygcn, FastGCN, Fair Clustering, SparseTSF, RippleNet, VGAE.
2. **Planting:** a seeded generator hides **one** change from a family: a setting at another value; a scale convention; a code defect (an arithmetic or reduction edit, or DeepCrime's "bias added or removed"); a data-pipeline change (a training cut); or a reporting rule.
3. **The paper's numbers:** the changed program runs 3 times, and the average becomes "the paper's number".
4. **Keeping it:** only if the change moves the number by at least 5 run-to-run standard deviations (level 1) or 3 to 5 (level 2), and by at least 1% of the value. About one task in five is a **control**: nothing planted, so the right answer is to say nothing.
5. **Sealing:** the answer is sealed. The search runs without the paper and without a ledger.

**Each round:** the new version is frozen first; a fresh seed makes the tasks; the old and new frozen versions search every task; a scorer compares them task by task.

| Round | Versions | Gap tasks | Old correct | New correct | New better / worse | Confidently wrong (old / new) | Adopted? |
|---|---|---|---|---|---|---|---|
| seed 2 | c1 alone | 14 | 4 | - | - | 0 | baseline |
| seed 3 | c1 vs c2 | 16 | 4 | 7 | 4 / 1 | 0 / 0 | no: gains were picks among ties |
| seed 4 | c1 vs c3 | 13 | 4 | 6 | 2 / 0 | 1 / 0 | **yes** |
| seed 5 | c3 vs c4 | 14 | 4 | 5 | 3 / 2 | 0 / 0 | no: its gains were faults its own operator generated |
| seed 6 | c3 vs c5 | 16 | 5 | 7 | 2 / 0 | 0 / 0 | **yes** |
| seed 7 | c5 vs c6 | 27 | 10 | 7 | 1 / 4 | 0 / 2 | no: worse, two confident mistakes, two crashes |

Every control in every round was answered correctly (69 control searches).

**What kinds of gap are found (c1 to c5):**
- Scale conventions: mostly found.
- Settings: about 3 in 10. Most misses are ties on few numbers.
- Code defects: rare (the first in c3).
- Data cuts: sometimes, since c5.
- Reporting rules: 1 of 1.
- Paper-era code and library releases: never plantable on these papers.

**Lessons the curriculum taught about testing itself:**
- **Too small to decide.** Each comparison had only 2 to 5 tasks where the versions differed. A sign test needs at least 6 all one way for p < 0.05, so no comparison has been significant.
- **Circular tasks.** On seed 5 the generator drew faults from the engine's newest operator. Now the generator uses operators frozen at an old version.
- **Scoring mistakes.** A tied reading of the reporting rule was first scored as confidently wrong. A tie now counts as correct when the planted value is inside the set of equal values.
- **Gaps the engine treats as reproduced.** Gaps between 0.5% and 1% were planted before the 1% rule matched the engine's floor.

These are development measurements: the builder knows every family. They are never blind evidence.

---

## 10. The journey: how GapFinder grew

The pattern throughout: every improvement started by reading *why* a run failed, in the logs, before changing anything.

### Stage 0: the first working system
Built the claim ledger, the assumption space, the checkpoint tree with forking, the search, the Gap Report and the web replay. First real case: **RusKey**. 127 experiments from 13 database loads. Verdict: "Unexplained". A surprise: the same database load gave a different result each time, so GapFinder learned to measure setup noise.

### v1.0: the first blind test
8 generated tasks, 3 runs each, done twice. 0 confident mistakes in 24 runs each time, but only 5 and 7 of 15 correct causes. The logs showed why: **the true value was often never tried**. The AI's suggested values did not include the answer. On MC Dropout it suggested `epochx` of 500, 1000 and 2000, while the answer was 10.

**Lesson:** the bottleneck was *coverage* (trying the right values at all), not checking answers.

### v1.1: fixing coverage
Values come from the code, not only from the AI: every allowed choice, a ladder of sizes, fraction-aware values, edge values, simple multiplier factors. The config flow notices that `--epochx` multiplies the epochs. Several equally good answers are reported. History matching says "out of space" when no setting fits everything. The sealed v1.1 test tried the true value in 12 of 15 runs.

**New problem:** the right answer was now tested but not always chosen. Tie-breaking picked the wrong one.

### v1.2: fixing selection
Each miss was studied in the logs, and the real causes were often not what we expected:

| Miss | What we expected | What the logs showed | Fix |
|---|---|---|---|
| a learning rate of 0.91 chosen | bad luck | learning rates treated like fractions (0.91 = 1 − 0.9/10) | only fraction-like settings get fraction values |
| epochs of 75 never tried | | a limit of 6 values per setting cut it | the ×5 step comes earlier |
| a useless extra setting kept | the simplification step failed | an unsupported guess outranked a well-supported partial answer | fixed the ranking |
| a very noisy setting won | | "close enough" used the candidate's own spread | a fair likelihood rule |

Also built: the dev suite, racing, and the forward step. Removed: pairing values by how much they move the result (worse), an unconditional forward step (worse), and pairing random seeds (no noise reduction). Sealed v1.2: 12 of 15, 0 confident mistakes, balanced accuracy 0.90.

### v1.3: budget and code-level causes
Added: escrow (25% of the budget kept for confirmation), early stop for fine values, and **patch knobs** (hard-coded numbers tested in memory). On MC Dropout, GapFinder named the documented settings for the first time and said the rest was out of space. Sealed v1.3: 0 confident mistakes, 9 of 15 correct, with every miss on two hard interaction tasks.

### The first blind real papers (v1.3 to v1.4)
Every real-paper result so far had been on MC Dropout, whose answer was known. So a separate model picked papers with documented gaps and sealed the answers.

- **FastGCN: missed, not confidently wrong.** It named the right setting (learning rate) with the wrong value. Reasons: it could not read TensorFlow-style flags, and the true value fixed the main number but broke a row that the paper had tuned separately. Fixed: absl flags, testing every setting, checking guessed defaults, and "tuned separately" rows.
- **GraphMAE: confidently wrong.** It said "Explained: `mask_rate=0.5`". The real cause was `alpha_l=1`. One chain of failures: the appendix table was cut off at 25,000 characters; the code's value was taken as the paper's; a rule skipped the true setting as "already matching"; an equally good wrong answer passed on weak evidence.

**The lesson that changed the plan:** fixing one paper at a time never ends. Two patterns were changed behind both failures: AI reading may only *reorder* what is tested, never *exclude* it; and a confident label must be *earned*.

### The white-box rebuild (after v1.4)
GapFinder stopped treating the program as a black box: runtime tracing, the secant step, relation claims, paper-versus-trace comparison, patch knobs for function defaults, and the confidence rules.

Two lessons:
1. The dev suite caught two regressions (the secant step manufacturing wrong exact fits: 102 down to 92; screening "already matching" settings first: 102 down to 76). Both were fixed, and the suite returned to 99 of 138.
2. **One hidden setting had blocked every real paper.** History matching allowed a 5% "model discrepancy", meant for scaled-down reproductions. With that allowance, gaps up to about 15% looked like noise, so no real paper reached "look in the code". At 1% the VGAE case was found end to end.

### Frozen and sealed batches (18 and 19 October)
- devbatch-1: 1 correct. devbatch-2: 0 found, 3 correct abstentions.
- Sealed batch 3 to 5 (6 papers): Fair Clustering correct; RippleNet partial; SparseTSF, the GCN attack, SDCN and BOND missed.
- Across batch 5, settings causes were found 1 time in 4, and code, evaluation and library causes 0 times in 4. The real causes were often elsewhere: an edge counted twice, the best epoch chosen on test labels, an API that changed between library releases.

**The rule from then on, for the life of the project** (set by the owner): a change must fix a class of failure seen on at least two papers, or follow a published method. It is never judged on the paper that revealed it. Progress is a rate on fresh, frozen batches.

### Plan D1 to D7: six cause classes (20 and 21 October)
Added the six-class differential, reporting-rule reading, library and era knobs, the mutation round, the automatic harness, multi-fidelity screening, and better paper reading. The dev suite stayed the same (52 of 69). No fresh real paper was run, so the effect was unknown.

### The planted-gap curriculum (21 October onwards)

- **c1 (baseline):** scale conventions 6 of 7, settings 2 of 18, code defects 0 of 5. Misses were sorted into seven classes: code rounds starved by budget (E1), mutation sites ranked out of reach (E2), the right knob at an off-grid value (E3), ties on a single number (E4), a wrong knob with no tie (E5), gaps below the detection limit (E6), and families that could not be planted (E7).
- **c2 (not adopted):** 7 of 16 against c1's 4, but every gain was a setting, one a lucky pick among ties, and code stayed at 0 of 3. Lesson: gains can come from somewhere other than the target, so look at which tasks moved.
- **c3 (adopted):** group screening, early code tests, value intervals, a class scheduler, the "not identifiable" note, and DeepCrime operators. 6 of 13 against 4, better on 2, worse on 0. **First planted code defect found** (RippleNet's `np.mean` that should be `np.sum`). c1's one confident mistake was gone.
- **c4 (not adopted):** 5 of 14 against 4, but its three gains were training cuts its own new operator generated (circular). On the other 10 tasks it got 2 against 4.
- **c5 (adopted, current):** scale factors must give whole numbers for whole-number settings; the second-best factor is tried; the first 6 mutants keep priority order; the curriculum generator uses frozen operators. 7 of 16 against c3's 5, better on 2, worse on 0. A 60% training cut found; a FastGCN epochs convention found. The dev suite was unchanged (99 against c1's 100 of 138).
- **c6 (not adopted):** 7 of 27 against c5's 10, better on 1, worse on 4, **two confident mistakes**, two crashes. The mistakes exposed a defect c5 also has: the scale probe tries several factors, and a wrong one can fit noisy data by chance without the confidence label counting how many were tried.

**The test-design mistake:** asked whether any version was better, the honest answer was that no comparison was statistically significant. Each batch had only 2 to 5 differing tasks, and a sign test needs at least 6. That should have been said before the first round. From then on, every round states in advance what it can detect.

### What the journey teaches
1. Read the logs before changing anything. Most real causes differed from the first guess.
2. Measure every change against noise, on a fresh batch, against the old version. c2, c4 and c6 all looked like progress until they were tested this way.
3. Say less when the data say less. Sets, Inconclusive and "out of space" are honest answers.
4. Keep tests sealed, and keep the generator separate from the engine.
5. Size the test before running it.
6. Check outside advice against the code. Both outside reviews had good ideas and several wrong claims.

---

## 11. Results in plain numbers

These are our own runs, self-reported, with small samples. They are not conclusive.

**Blind test on practice tasks (8 tasks, run twice):**

| | GapFinder | Coding agent (mini-swe-agent, Nemotron 3 Super) |
|---|---|---|
| Confidently wrong, runs 1 and 2 | 0 of 24, 0 of 24 | 14 of 24, 12 of 24 |
| Correct cause found | 5 of 15, 7 of 15 | 4 of 15, 4 of 15 |
| Correct "unexplained" on no-cause tasks | 9 of 9, 9 of 9 | 1 of 9, 2 of 9 |
| Tasks solved in median run | 4 of 8, then 6 of 8 | 1 of 8, then 2 of 8 |
| Answer stability across 3 runs | 0.83, 0.88 | 0.46, 0.58 |

- The safety result (no confident mistakes) is the strongest.
- Interaction tasks were never fully solved: 0 of 12 runs.
- Random hypothesis order (9 of 15) and no evidence check (8 of 15) matched or beat the full pipeline. None of the three made a confident error.

**Real papers, blind (8 papers, keys sealed before each run):** 1 correct, 1 partial, 5 missed, 1 confidently wrong (GraphMAE). The earlier README reports only the first two of these.

**Real paper, not blind (MC Dropout):** the v1.3 run names the documented cause (`epochx=10, hidden=1`) and says the rest is outside the settings. Energy goes from 0.364 by default to a median of 1.716, against the paper's 1.66; neither setting alone does it (0.533 and 0.427). But the same pair breaks the held-out Yacht claim (2.996, against the paper's 1.11, where the defaults give 0.831).

**RusKey (the founder case):** verdict "Unexplained" at 2 million keys. The paper used 100 million, so settings that only matter at full scale cannot be tested here.

**Cost:** about $33 of billed model calls by 24 October (the sources give $17 in mid-October, so the figure has grown). Sandboxes costs are reported but not billed during the beta.

---

## 12. Limits and what is next

### What GapFinder cannot do yet

- **Real papers are unproven.** The 8 sealed blind papers gave 1 correct, 1 partial, 5 missed and 1 confidently wrong. Nothing since 20 October has blind evidence.
- **Most kinds of cause are found only partly.** The current line (c1 to c5):

| Kind of gap | Found | Why the misses happen |
|---|---|---|
| Scale or unit convention | mostly | noisy data can let a wrong factor fit |
| Setting | about 3 in 10 | several settings move the few reported numbers alike (a tie); values off the tried grid |
| Code defect | rarely | the right edit is outside the operators, ranked too low, or the budget ran out first |
| Training-data cut | sometimes | the engine's cuts (1/2, 3/4) do not match other fractions closely enough |
| Reporting rule | 1 of 1 | only one was planted |
| Paper-era code, old library release | never tested | these never moved a planted number enough |

- **One number cannot decide between causes.** When the paper reports one or two numbers, many settings fit equally well. GapFinder says so, but cannot do better.
- **The scale probe has an open defect.** It tries several factors, and on noisy data a wrong one can fit by chance. It caused two confident mistakes in c6 on seed 7; c5 has the same logic.
- **It changes settings, constants, defaults and small edits, never code structure.** A different loop, pipeline order or algorithm can be pointed at, but never tested. That is on purpose: rewriting code until a number fits would explain nothing.
- **Sandboxes only:** 4 cores, 3.9 GB of memory, up to an hour per run. Papers that need more are out of scope.
- **The harness still needs a person to approve it.** It has not yet run end to end on an unseen repository.
- **The tests so far cannot show progress.** Every comparison between versions had too few differing tasks to be significant.

### What is next, in order

1. **Make the scale probe's confident label account for the factors tried.** Either a multiple-comparison correction, or confidence only for the best factor verified on the first try. It must be judged on a fresh batch (seed 8), not seed 7.
2. **Fix c6's two crashes:** split leads only for numbers, and bound the exponent in the fraction formula. Then decide which of c6's ideas are worth a fresh test.
3. **A test big enough to decide:** about 50 gap tasks, more tasks per paper and more papers. Say beforehand what difference it can detect. Run c1 on seed 6 for a direct comparison with c5.
4. **A sealed blind batch of real papers on the current version.** This is the only proof that counts.
5. **The harness end to end on an unseen repository.**
6. **Parts not run for budget:** a claim labeller, two-pass prose reading, and link adjudication.

### How to contribute

- Run it on a paper you know. More real cases show where it works.
- Read `docs/CONTEXT_v11.md` for the current architecture, every result and the open list.
- Check every change on the dev suite and on a fresh planted batch, against the old frozen version.
- Never look at sealed answers before a test is scored. That one rule keeps the results meaningful.

---

## 13. Glossary

Alphabetical. Words in *italics* are defined elsewhere in this list.

**Ablation.** A test where one part of the system is turned off to see what that part is worth.

**Artifact.** The code published with a paper.

**Arm.** One version of the system in a test, compared side by side with others (for example, GapFinder without verification).

**Assumption.** A setting the paper's result might depend on, with values to try and evidence.

**Assumption space.** The full list of assumptions for one paper.

**Backend.** Where code runs: your computer (local), Docker, or cloud Sandboxes.

**Balanced accuracy.** The average of "found the cause when there was one" and "blamed nothing when there was none". Always saying "Unexplained" scores 0.50.

**Baseline.** The comparison system: a general coding agent with the same model and budget.

**Bisect.** Remove the parts of a combination that are not needed, to find the smallest set that matters. From `git bisect`.

**Blind test.** A test whose answers were hidden from the people building the tool until results were frozen.

**Bootstrap interval.** A statistical range for an effect, built by resampling the data many times. If it excludes zero, the effect is probably real.

**Branch.** One experiment run, started from a checkpoint.

**Calibration.** Running the default settings several times to measure the noise.

**Checkpoint.** A saved state of an experiment (built or loaded) that other runs start from.

**Claim.** One result the paper reports, such as "Energy RMSE 1.66".

**Claim ledger.** The list of all claims from a paper, each with an exact quote.

**Class scheduler.** The rule that keeps part of the budget for code tests when no setting looks likely.

**Code defect.** A small error or difference in the code that changes the result.

**Code lead.** A place in the code where a hidden cause could live (for example `batch_size = 128`). Never labelled "Explained".

**Code proposer.** One cheap AI call that proposes at most three code edits when nothing fits. Off by default.

**Coarse rungs.** The first, big steps of the value ladder (×10, ÷10).

**Coverage.** Whether the right value is tried at all.

**Confidently wrong.** A confident label on the wrong cause. The worst kind of error.

**Confirm.** Repeating a promising change to check it is not luck.

**Config flow.** Following a setting through the code to see what it controls (for example, `epochx` multiplies the epochs).

**Content-addressed ID.** An ID computed from the contents of a saved state. Identical states get identical IDs.

**Control.** A planted task with nothing planted. The right answer is to blame nothing.

**Counterfactual.** Undo a change and check that the gap comes back.

**Credible set.** The answer plus the configurations the claims cannot tell apart from it. "In a credible set of at most 3" means the cause is among at most three.

**DeepCrime.** A published set of fault types taken from real deep-learning bugs (removing training data, removing a bias, removing weight decay).

**Delta debugging (ddmin).** A method for finding the smallest set of changes that still causes a failure (Zeller and Hildebrandt, 2002).

**Dev suite.** Re-running the search on all public tasks, to measure a change for free.

**Diff guard.** The rule that blocks any edit to the algorithm's code.

**Differential.** Every candidate cause from every class, scored against all claims together, like a doctor's list of possible diagnoses.

**Discrepancy (model discrepancy).** When no setting of a model can match the data, the model itself is wrong in a way settings cannot fix.

**Discrimination.** Choosing runs so that tied candidate answers predict different numbers.

**Early code screen.** Cheap code tests (top constants, first mutants) run right after the settings screen.

**Equally good configurations.** Answers the paper's numbers cannot tell apart.

**Equifinality.** When several different settings (or causes) produce the same result. The term comes from hydrology.

**Escrow.** Budget kept aside for confirming the best candidates.

**Evidence check.** Is there a quote in the paper, its docs or the web showing that the authors used this value?

**Explained.** The top label. Every check passed, and there is evidence the authors used the value.

**Family.** The kind of change the curriculum plants (setting, scale, code, data, reporting).

**Fits but unsupported.** A setting closes the gap, but nothing shows the authors used it.

**Fork.** Starting a new experiment from a saved checkpoint instead of from scratch.

**Forward step.** Pairing the best setting with every value of the other top settings, to find interactions.

**Fresh batch.** Planted tasks made after the version being tested was frozen. The only fair test of it.

**Gap.** The difference between what the code gives and what the paper reports.

**GapBench.** Our benchmark of small artificial papers with planted causes.

**Gap Report.** GapFinder's output: one card per claim, with a label, proof and replay.

**Group screening.** Many edits or settings tested together in one pooled run. A pool that moves the numbers is split in half.

**Harness spec.** A YAML file, approved by a person, saying how to build and run the code and which settings may change.

**Held-out claim.** A paper number GapFinder must not make worse while fixing the main one.

**History matching.** Scoring every tested configuration against all claims at once. Finds "out of space" causes.

**Hypothesis.** One setting and one value to test.

**Identifiable.** The claims can tell the cause apart from every other candidate. "Not identifiable" means they cannot.

**Implausibility.** How unlikely the paper's number is under a configuration, counting noise. Over 3 means ruled out.

**In space / out of space.** Whether some setting GapFinder can change could explain all the claims ("in space") or none could ("out of space").

**Inconclusive.** The measurements are too noisy to decide.

**Interaction.** Two settings that only matter together.

**Interference control.** The rule that a code edit must move at least two claims that were off, so an edit next to the output cannot "fix" one number by force.

**Knob.** A setting GapFinder may change (a flag, an environment variable, a data choice).

**Ladder.** The coarse-to-fine sequence of values tried around a default.

**Lesion.** A test that removes one knob to see whether it matters.

**Level (curriculum).** How hard a planted task is. Level 1 is a clear effect (at least 5 run-to-run standard deviations); level 2 is subtler (3 to 5).

**Likelihood.** How well a configuration's measured spread explains the paper's number. Used to rank fits fairly.

**Load-to-load variance.** The difference between identical loads of the same database. It can be large.

**Minimum detectable effect (MDE).** The smallest gap the runs can reliably detect.

**MRR (mean reciprocal rank).** A score that is 1 if the cause is the top answer, 1/2 if it is second in the tied set, and so on, averaged.

**Mutation round.** Small edits to the code (×2, ÷2, mean to sum, a loop bound, a data switch), each tested in memory on every claim.

**Mutation testing.** Making small deliberate edits to code to see whether a test suite notices.

**Nemotron.** The family of NVIDIA AI models GapFinder uses. Ultra reads the hardest text, Super filters and diagnoses, Nano is a fallback parser. Nano Omni is not served on Token Factory, so figures are not read.

**NROY (not ruled out yet).** A configuration still consistent with a claim in history matching.

**Null (no cause) task.** A task where nothing is planted. The right answer is "Unexplained" or "Inconclusive".

**Occam's margin.** An extra setting must improve the fit by more than the noise, or it is dropped.

**Operator.** One kind of mutation edit (for example "swap mean and sum").

**Out of space.** See *in space*.

**Output slice.** The part of the code that computes the number the program prints. Edits there are tried first.

**Passenger knob.** A setting that only fits the noise and does not cause the gap.

**Patch knob.** A hard-coded number in the code, changed in memory for a test, without editing any file.

**Paper priors.** Weights that break ties: a value the paper states 0.9, a mentioned setting 0.6, an unmentioned one 0.4.

**Planted-gap curriculum.** The test bench of hidden changes in papers that already reproduce.

**Pre-registration.** Writing down the test plan and success criteria before running the test.

**Pseudo-replication.** Treating repeats that share one hidden random draw as if they were independent samples. Forks from one database load are an example.

**Racing.** Giving repeats only to the best candidates, step by step.

**Reporting rule.** How the paper chose which number to report (the final epoch, the best epoch, the best seed).

**Repo map.** The list of settings, defaults and file locations, read from the code without AI.

**Replay.** A recorded run that plays back in the web app.

**Reasoning trace.** The step-by-step thinking a reasoning model writes before its answer. The router separates it from the answer.

**Reproduction gap.** When running a paper's code does not give the paper's numbers.

**Router.** The one place every AI call goes through: cache, JSON repair, spending cap.

**Sandbox.** A cloud machine where code runs safely (Token Factory Sandboxes).

**Scale convention.** A unit or counting difference between paper and code, such as "the paper's v is the code's 2 times v".

**Scale probe.** The test for scale conventions.

**Screen.** Trying each candidate value once.

**Seed (curriculum).** The number that decides which tasks a batch contains. A new seed makes a fresh batch.

**Sealed test.** A test whose tasks are made after the code is frozen and whose answers stay hidden until scoring.

**Secant step.** Estimating where a curve crosses a level from two tried values. Used only when no tried value fits every claim.

**Sign test.** A simple test that counts tasks where one version won against tasks where it lost. It needs enough differing tasks to mean anything.

**Sigma (3 sigma).** One standard deviation of noise. "Within 3 sigma" means within three standard deviations.

**Static code checks.** Reading the code, without running it, for hidden causes.

**Structural switch.** A layer's on/off setting, such as `bias=True` or `affine=True`.

**Successive halving / multi-fidelity.** Screen many candidates with cheap runs, and keep only the best for expensive runs.

**Token Factory.** The service that runs the Nemotron models and the Sandboxes.

**Trace (runtime trace).** A short run that records where each setting's value lands in the program.

**Training-data cut.** The paper trained on part of the data (a half, 40%, and so on).

**Triage.** Reading why a run failed and, if a value was rejected, trying a valid one.

**Value interval.** The range of a setting's values that fit every claim, not just one point.

**Verification.** The checks before a confident label: counterfactual, held-out claims, evidence.

**Versions c1 to c6.** Frozen versions of GapFinder (git tags `planted-c1` to `planted-c6`). c5 is the current adopted version.

**Wilson interval.** A confidence range for a proportion that behaves well with small samples.

**Sealed key.** The answer key for a test, written down and committed before the test runs and revealed afterwards.
