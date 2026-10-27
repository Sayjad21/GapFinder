# GapFinder, explained simply

Written for: someone new to the project who wants the full flow, the research behind each step, what is new, and what the words mean.

Facts come from the project docs as of 24 October 2026 (`docs/CONTEXT_v11.md`, `README.md`, `docs/ARCHITECTURE.md`, `PROGRESS_REPORT.md`). Later versions may differ. Where a result is not measured, this file says so.

---

## 1. The problem in one paragraph

A research paper reports a number, such as "our method gets 1.66 error". When you run the paper's released code, you often get a different number, such as 0.36. Most tools only ask **"does this paper reproduce?"**. GapFinder asks **"why doesn't it?"**. It tries to find the setting, or the piece of code, that explains the difference. If it cannot find a convincing reason, it says **"Unexplained"**. It does not guess.

---

## 2. The big picture: input to output

```
 INPUT                                                          OUTPUT
 ┌──────────────┐
 │ Paper (PDF)  │──► 1. Claim ledger ──────────────┐
 └──────────────┘        (what results are claimed)│
 ┌──────────────┐                                  ▼
 │ Code (repo)  │──► 2. Repo map ──► 3. Assumption space ──► 4. Hypotheses
 └──────────────┘       (what knobs exist)  (what might matter)  (what to test)
 ┌──────────────┐                                  │
 │ Harness spec │──► (how to build, load, run) ◄───┤
 │ (YAML file)  │                                  ▼
 └──────────────┘                     5. Checkpoint tree (Sandboxes)
                                         build once, load once, fork many
                                                    │
                                                    ▼
                                     6. Search: screen → confirm → combine
                                        → bisect → discriminate
                                                    │
                                                    ▼
                                     7. Verify: revert, held-out, history
                                        matching, evidence, identifiability
                                                    │
                                                    ▼
                                     8. Gap Report + replay  ──► Verdict per claim
```

**Input:** a paper, its code, and a harness spec. The harness spec is a small YAML file that says how to build the code, how to load its data, and how to run it. It is drafted automatically and approved by a person.

**Output:** a **Gap Report**. It has one card per claim. Each card shows a verdict label, the setting that explains the gap (if any), the evidence, a noise band, the held-out checks, and a command to replay the winning experiment.

---

## 3. Step by step

Each step has the same parts: what goes in and out, what it does, the state-of-the-art (SOTA) work it uses, how we used it, how it helped, and what is new.

### Step 0. Harness spec (set-up, once per code repo)

- **In:** the code repo. **Out:** a YAML file with build, load and run commands, the list of knobs, and the folders a branch may write to.
- **What it does:** turns a messy research repo into something a program can run.
- **SOTA used:** Repo2Run-style environment building. An LLM reads the README and scripts, drafts the setup, and tries it.
- **How we used it:** Nemotron drafts the spec, a smoke test runs it, and a person approves it. This is the one human checkpoint.
- **How it helped:** the drafted spec ran unedited on two small test artifacts, finding 13 of 13 and 14 of 14 knobs. On real research repos this still needs more work.
- **New:** the spec has a "layer" for each knob (build, dataset, config, workload or environment). The layer decides where a branch forks from, which saves setup time.

### Step 1. Claim ledger (what does the paper claim?)

- **In:** the paper's text and tables. **Out:** a list of claims. Each claim has a number, a unit, the conditions it holds under, a page, and an exact quote.
- **What it does:** lists every result the paper reports, so each one can be checked.
- **SOTA used:**
  - Large language models (Nemotron 3 Ultra) do the reading. A second, smaller model (Nemotron 3 Super) removes text that is not a result.
  - HyperPIE (Saier et al., 2024) showed that LLMs are weak at linking a value to what it applies to. So GapFinder does not trust the model's reading. It checks it.
  - SciTab (2023) showed that LLMs make mistakes in scientific table claims, including wrong calculations.
- **How we used it:** every quote must match the PDF text. A claim whose quote is not in the PDF is **dropped, never repaired**. Tables are read from LaTeX or PDF grids.
- **How it helped:** on RusKey, 17 extracted claims were dropped this way, so the model cannot invent evidence. On RusKey the ledger got headline-claim recall 1.00 and precision 1.00 on the paper the prompts were tuned on. Setting recall was only 0.67, below our 0.80 bar.
- **New:** the "drop, never repair" rule. Many tools fix a bad quote. We throw it away.

### Step 2. Repo map (what knobs does the code have?)

- **In:** the repo. **Out:** every command-line flag, config key and environment variable, with its default value and its file and line number.
- **What it does:** reads the code without using a language model. It finds `argparse` flags, `gflags`, YAML keys and the like.
- **SOTA used:** classic static analysis. No LLM.
- **How we used it:** it also records commented-out alternative blocks in the repo, such as `# lr = 0.01`. Those become candidate values.
- **How it helped:** the repo map is cheap and exact, so the language model does not need to read the whole repo. Gaps in it show up as missed knobs. For example, the FastGCN repo map did not read `tf.app.flags`, so one learning-rate knob was missed.
- **New:** using the repo's own commented-out alternatives as candidate values.

### Step 3. Links and trace (which paper word means which flag?)

- **In:** the words in the paper and the repo map. **Out:** a mapping from paper terms to flags, and a record of which knobs actually change what runs.
- **What it does:** matches paper words to flags, then runs the code once and records where each value goes.
- **SOTA used:** BM25, a classic search-ranking formula, with a small lexicon of machine-learning terms.
- **How we used it:** a "trace hook" runs one dry pass and records which lines execute and where each value lands. A "lesion" run then checks that each knob really does something.
- **How it helped:** knobs that never change anything are removed before the expensive search. Knob roles also decide which candidate values are sensible.
- **New:** the dry-run trace. Standard tools do not record the path of values through the code.

### Step 4. Assumption space (what might the result depend on?)

- **In:** the paper's setup section, the appendix (read in its own call), the repo map and 10 to 30 relevant files. **Out:** a list of assumptions. Each has a knob, a layer, the paper's stated value or "unstated", the code's default, candidate values, evidence, and a prior score.
- **What it does:** lists the settings that could explain a gap.
- **SOTA used:** an LLM reads the paper and code together. The method follows the reproduction-study literature: Raff (2019), Gundersen et al. (2022) and Fostiropoulos et al. (2023) found that missing hyperparameter details are a main cause of failed reproductions.
- **How we used it:**
  - The status of each setting (stated and matches, stated but code differs, unstated) is computed by code, not by the model.
  - "Stated but code differs" is kept as its own finding. It is a paper–code inconsistency.
  - The appendix gets its own call. GraphMAE's first run missed the appendix table that stated the true cause.
- **How it helped:** the appendix call is a direct fix from a real miss. Whether it helps on new papers is not yet measured.
- **New:** the "stated but code differs" status is treated as a finding in its own right.

### Step 5. Hypotheses in six cause classes (what should we test?)

- **In:** assumptions, spec knobs and trace roles. **Out:** a ranked list of hypotheses. Each hypothesis is one change to test.
- **What it does:** turns the assumptions into runnable tests, across six classes of cause:
  1. **Settings**: flags and config values.
  2. **Reporting rules**: how the paper picked its number, such as the best epoch, or the best on validation data. Checked with zero extra runs, from per-epoch values.
  3. **Library and paper-era code**: package versions and the code commit from the paper's date. Searched with delta debugging.
  4. **Code defects**: small edits to the code, such as a changed constant or a flipped operator.
  5. **Data pipeline**: changes to how training data is cut or prepared.
  6. **Outside every class**: an honest default when nothing fits.
- **SOTA used:** mutation testing (for code defects) and delta debugging (Zeller and Hildebrandt, 2002) for library and era searches.
- **How we used it:** the mutation round uses small edits, such as ×2, ÷2, mean to sum, or a changed bound. Data-pipeline edits are measured as a fraction of the training data.
- **How it helped:** code defects went from 0 of 7 found (earlier version) to 2 of 6 found (version c3). Data-pipeline cuts went from 0 of 13 to 1 of 4 (version c5). Both are small numbers.
- **New:** framing the search as six cause classes. Most tools search only settings.

### Step 6. Checkpoint tree (Token Factory Sandboxes)

- **In:** the harness spec. **Out:** a tree of saved states: source, built, loaded, then one branch per hypothesis.
- **What it does:** build the code once, load the data once, save the state, then start every test from that saved state. This is called **forking**.
- **SOTA used:** snapshot trees in Token Factory Sandboxes. Each saved state has a content ID, so identical states get the same ID.
- **How we used it:**
  - A config change forks from the loaded database. A dataset change reloads from the build. A build flag rebuilds.
  - **Noise setups:** with `--noise-setups N`, the database is loaded N times with the same command. If the IDs differ, the noise band must widen.
- **How it helped:**
  - Fork against no fork, same search of 22 branches: 8 loads instead of 22. Reported cost $4.48 instead of $8.07. The Sandboxes cost is reported, not billed during the beta.
  - Five identical loads gave five different checkpoints on RusKey. Across 12 loads the naive ratio ranged from 0.52 to 1.38. Forked repeats from one load are too narrow.
- **Cross-domain link:** database benchmarking warnings (Didona et al., VLDB 2021; Luo and Carey, VLDB 2020) say that results vary a lot from one load to another. The idea of "pseudo-replication" (repeats that share one hidden random draw) comes from there.
- **New:** using the content ID as a test of whether a setup is reproducible at all.

### Step 7. Search (which change closes the gap?)

- **In:** the hypothesis list and a fixed run budget. **Out:** survivors, a combination, and a minimal set of changes.
- **What it does, in rounds:**
  1. **Noise calibration.** Repeat the default setup to measure the noise. An effect counts only if a bootstrap interval (a resampling test) excludes zero.
  2. **Screen.** One change per run. Cheap runs come first (multi-fidelity, as in successive halving).
  3. **Confirm.** Survivors get repeats. Losing candidates are dropped early (racing, Maron and Moore, 1994).
  4. **Group screening.** When nothing fits, several unmentioned flags are tested together in one pooled run. A flat pool is pruned whole. This comes from group testing (Dorfman, 1943) and sequential bifurcation (Shi and Kleijnen).
  5. **Combine.** The best knobs are tried in pairs. Once a combination fits every claim, only candidates inside the tie margin are confirmed.
  6. **Bisect.** Remove knobs one at a time to find the smallest set that still closes the gap. This is delta debugging. The name "bisect" comes from `git bisect`.
  7. **Discriminate.** When two settings tie, run them at the paper's other conditions. Keep the runs that best separate them (optimal design for model discrimination, Box and Hill, 1967).
  8. **Scale probe (ours).** Tests whether the paper's value equals the code's value times a factor, such as "10 times more iterations".
  9. **Patch round.** Changes literal constants in memory, without touching files on disk (see the next step).
  10. **Class scheduler (ours).** When no setting looks likely, up to 30% of the runs go to code tests.
  11. **Triage.** When a run fails, a model reads the error and proposes one valid value.
- **SOTA used:** racing, successive halving, delta debugging, group testing, sequential bifurcation, and optimal experimental design. Each is an existing method. We combined them for this job.
- **How it helped:**
  - Group screening, in a bundle of version-c3 changes: 6 of 13 tasks solved against 4 of 13. Better on 2 tasks, worse on 0. The sign test gives p = 0.5, so this is not significant.
  - The scale probe found "mostly found" scale conventions in the planted tests (9 of 13 in version c1).
  - On the planted-task curriculum, settings are the weak point: about 3 in 10 found.
- **New:** the scale probe, the class scheduler, and the way the rounds are arranged for an expensive oracle (each run costs minutes of sandbox time).

### Step 8. Patch round (test a constant without editing a file)

- **In:** literal constants found in the code (such as `batch_size = 128`). **Out:** a test run with that constant changed, in memory only.
- **What it does:** a small AST transformer runs inside the child process. It parses the source file, replaces one literal, compiles the result in RAM, and runs it. The file on disk never changes.
- **SOTA used:** mutation testing tools (mutmut) and Python's import hooks (PEP 451). Durable-execution systems such as ModShim and AutoKitteh use the same trick.
- **How we used it:** this respects the project's main rule, which is that GapFinder may change conditions but never the algorithm. The diff guard still passes.
- **How it helped:** on MC Dropout (not a blind test), the batch-size patch was the only one that moved the held-out Yacht claim (with batch 64, Yacht gave 1.18 against the paper's 1.11).
- **Novelty:** using in-memory mutation as a diagnostic for reproduction gaps. Mutation testing normally checks test suites, not papers.

### Step 9. Verify (is the answer real?)

- **In:** the best candidate and its run. **Out:** a label and the checks behind it.
- **What it checks:**
  1. **Revert.** Undo the change. The gap must come back.
  2. **Held-out claims.** Other numbers in the paper must not get worse beyond noise.
  3. **History matching.** Test every configuration against every claim. If no configuration fits all claims within 3 sigma (3 standard deviations of noise), the cause is probably outside the knobs ("out of space").
  4. **Identifiability.** If other knobs fit as well, the answer is "not identifiable from the paper's numbers".
  5. **Evidence.** Is there a source that says the authors used this value? Paper text first, then code, then the web (Tavily). With no evidence the label is "Fits but unsupported".
  6. **Confidence cap.** A finished search can only be "Explained" with evidence beyond the code.
- **SOTA used:**
  - Equifinality (Beven and Binley, 1992; Beven, 2006): many different settings can fit one number equally well.
  - History matching (Craig et al., 1996; Vernon et al., 2010): rule out settings that fail a test, and treat "no setting fits" as a sign of model error.
  - Discrepancy reading (Kennedy and O'Hagan, 2001): when no setting can reach the data, the simulator itself is wrong.
- **How it helped:**
  - Without the verify step, 7 of 24 blind runs were confidently wrong. With it, 0 of 24 were.
  - On MC Dropout (not blind), history matching labelled the cause "out of space", which matches the documented cause (test-set contamination and a code difference).
- **New:** the labels. "Fits but unsupported" is kept apart from "Explained". "Explains target, conflicts with held-out" is planned as a new label.

### Step 10. Gap Report and replay (what do you get?)

- **In:** everything above. **Out:**
  - One card per claim, with a verdict label.
  - A provenance block: code hash, model and prompt hashes, spec hash, cost.
  - A replay command for each winning run.
  - A web replay, which plays a recorded run at 1×, 4× or 16× at no cost.
- **Rule:** when the budget runs out, nothing that was not confirmed is labelled.
- **New:** the replay is the default landing page, so a judge can see the result without running anything.

---

## 4. What is new in GapFinder

Our own design choices, not taken from one paper:

1. **Six cause classes**, not only settings.
2. **The drop-don't-repair grounding rule.** Quotes that do not match the source are removed.
3. **Scale probe**: "the paper's value equals the code's value times a factor".
4. **Reporting-rule probe** with zero extra runs.
5. **Content IDs as a measurement**: identical load IDs show the setup is reproducible. A difference widens the noise band.
6. **In-memory patch round** as a diagnostic, not only as a test-suite tool.
7. **Labels that separate "fits but unsupported" from "explained"**.
8. **Planted-task evaluation with frozen operators**. The engine under test cannot create its own test cases. Seed 4 showed why: some gains came from operators the engine had written itself, so they were thrown out.
9. **Class scheduler** that keeps part of the budget for code tests.
10. **Data cut measured on a log scale** from one run, instead of a fixed half or three quarters.

---

## 5. Results, in plain numbers

Our own runs, self-reported. Small samples: these are not conclusive.

**Blind test on toy tasks (8 tasks, run twice, 3 runs per task):**

| | GapFinder | Standard coding agent (mini-swe-agent with Nemotron 3 Super) |
|---|---|---|
| Confidently wrong, runs 1 and 2 | 0 of 24, 0 of 24 | 14 of 24, 12 of 24 |
| Correct cause found | 5 of 15, 7 of 15 | 4 of 15, 4 of 15 |
| Correct "unexplained" on no-cause tasks | 9 of 9, 9 of 9 | 1 of 9, 2 of 9 |
| Tasks solved in median run | 4 of 8, then 6 of 8 | 1 of 8, then 2 of 8 |

- The safety result (no confident mistakes) is the strongest.
- Interaction tasks (two settings that matter only together) were never fully solved: 0 of 12 runs.
- Random hypothesis order (9 of 15 causes) and no evidence step (8 of 15) found as many causes as the full pipeline, with no confident mistakes. So the ranking and evidence step have not yet been shown to find more causes.

**Real papers, blind (8 papers, answer keys sealed before each run; the first two were sealed by a separate AI model):**

- 1 correct, 1 partial, 5 missed, 1 confidently wrong (GraphMAE).
- The earlier README reports only the first 2 papers.

**Real paper, not blind (MC Dropout):** GapFinder names the documented cause (`epochx=10, hidden=1`) in the v1.3 run. It also says the rest is outside the settings, and points to the code lines involved. The 0.36 to 1.72 move on the Energy claim matches the paper's 1.66, but the same setting breaks the held-out Yacht claim.

**RusKey (the founder case):** verdict "Unexplained" at 2M keys. The paper used 100M, so some settings may only matter at full scale.

**Cost:** about $17 to $33 of billed Nemotron calls, depending on the snapshot. Sandboxes runs are reported but not billed during the beta.

---

## 6. Limits, stated plainly

- Small samples. One real case is not blind and two are blind but not solved.
- CPU only. Sandboxes VMs have 4 vCPUs and 3.9 GB, so GPU papers and full-size data are out of reach.
- The harness spec still needs a person to approve it.
- Patch knobs only change literal constants in Python. Loops and data pipelines cannot be patched this way.
- Timing numbers are noisy, so the project compares ratios measured inside one VM.
- The model's reading of relative wording ("10 times more iterations") is weak. That is the MC Dropout miss.

---

## 7. Terminology

**Ablation**: a test where one part of the system is turned off, to see what that part is worth.

**Artifact**: the code released with a paper.

**Balanced accuracy**: the average of accuracy on tasks with a cause and accuracy on tasks without one. Always answering "unexplained" scores 0.50.

**Baseline**: the comparison system. Here, a standard coding agent (mini-swe-agent) run on the same model, sandbox and budget.

**Blind test**: a test whose answers were hidden from the people building the tool until the results were frozen.

**Bisect**: a search that halves a set of changes again and again, to find the smallest set that still matters. The name comes from `git bisect`.

**Bootstrap**: a resampling test. It repeats the measurement many times with random subsets of the data, to see how stable a result is.

**Checkpoint**: a saved state of the sandbox (the built or loaded program and its data).

**Claim**: one result the paper reports, such as a number with its conditions.

**Confidently wrong**: a label such as "Explained" that names the wrong cause. The most serious kind of error.

**Content-addressed ID**: an ID computed from the contents of a saved state. Identical states get identical IDs.

**Counterfactual (revert)**: undo the suspected change and check that the gap comes back.

**Delta debugging**: a method for finding the smallest set of changes that still causes a failure (Zeller and Hildebrandt, 2002).

**Diff guard**: a check that rejects any run which edits files outside the allowed folders.

**Discrepancy (model discrepancy)**: when no setting of a model can match the data, the model is wrong in a way that settings cannot fix.

**Equifinality**: many different settings can give the same result. The term comes from hydrology (Beven).

**Explained**: the top label. Every check passed, and there is evidence the authors used the value.

**Fits but unsupported**: a setting closes the gap, but there is no evidence the authors used it.

**Fork**: start a new run from a saved checkpoint, so earlier work is not repeated.

**Gap**: the difference between the paper's number and the number from running the code.

**Gap Report**: the output document. One card per claim.

**Group testing**: test several items in one pooled run. If the pool is clean, all of them are cleared at once (Dorfman, 1943).

**Harness spec**: a YAML file that says how to build, load and run an artifact, and which knobs exist.

**Held-out claim**: a claim that was not used to choose the setting. It checks that the setting is not overfitted.

**History matching**: a method that rules out settings that fail to match the data, within a set number of standard deviations (here 3 sigma). If none survive, the cause is likely outside the settings.

**Hypothesis**: one specific change to test, such as "set epochs to 10".

**Identifiability**: whether the data can tell which of several settings is the true one.

**In space / out of space**: "in space" means the cause is a setting GapFinder can change. "Out of space" means it is not, such as a bug in the code.

**Knob**: a setting that can be changed, such as a flag, a config value or a constant.

**Layer**: where a knob takes effect: build, dataset, config, workload or environment.

**Lesion**: a test that removes one knob to see whether it matters.

**Load-to-load variance**: the difference between two identical loads of the same database. It can be large.

**Mutation testing**: making small deliberate edits to code, to see whether a test suite notices.

**Noise band**: the range of values that could come from random noise alone. An effect inside the band is not real.

**Nemotron 3 Ultra / Super / Nano**: three sizes of the NVIDIA language model, used for different jobs. Ultra does the hardest reading, Super filters and diagnoses, and Nano is a fallback parser. Nano Omni is not served on Token Factory, so no figure reading is done.

**Out of space**: see "in space".

**Passenger knob**: a setting that only fits the noise and does not cause the gap.

**Pseudo-replication**: treating repeats that share one hidden random draw as if they were independent samples. Forks from one database load are an example.

**Racing**: test candidates together and drop the losers early.

**Repo map**: a list of every knob in the code, built without a language model.

**Replay**: a recorded run that plays back in the web app.

**Reasoning trace**: the step-by-step thinking a reasoning model writes before its answer. The router separates it from the answer.

**Router**: the code that calls the models. It splits reasoning from answers, repairs broken JSON, caches answers and checks the spend limit.

**Sandbox (Token Factory Sandboxes)**: an isolated virtual machine where the code runs.

**Scale convention**: the paper's value equals the code's value times a factor. For example, "10 times more iterations".

**Successive halving / multi-fidelity**: screen many candidates with cheap runs, and keep only the best for expensive runs.

**Triage**: when a run fails, a model reads the error and proposes a fix.

**Verify**: the checks a candidate must pass before it is called explained.

**Ledger**: the table of claims. In GapFinder, the claim ledger.

**Sigma (3 sigma)**: one standard deviation of noise. "Within 3 sigma" means within three standard deviations.

**Sign test**: a simple test that counts how many tasks improved and how many got worse. It needs enough differing tasks to show significance.

**Wilson interval**: a confidence range for a proportion that behaves well with small samples.

**Sealed key**: the answer key for a test, written down and committed before the test runs and revealed afterwards.
