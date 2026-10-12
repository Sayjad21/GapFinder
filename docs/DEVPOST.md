# GapFinder: Devpost description

<!--
FOR WHOEVER PASTES THIS INTO DEVPOST (delete this block first)
- Everything below the "---" line is the text. Paste it into the project story field.
- Search for "[[V1.0:" before you submit. Each one is a number or link that is not final until the
  second GapBench test run (on the v1.0 tag) is scored. Replace it with the real value from the file
  named inside the brackets, or delete the sentence if the file does not exist. Do not paste a
  placeholder, and do not invent a number.
- Links use the repository's main branch. They only work once the repo is public.
- The text uses lists, not tables, because Devpost's editor may not render tables.
- Upload docs/img/report.png, docs/img/scoreboard.png and docs/img/replay.png as the gallery images.
- Track: Coding and Agentic Engineering.
-->

---

**Everyone asks whether a paper reproduces. GapFinder asks why it doesn't.**

Judges: open https://sayjad21.github.io/GapFinder/ and press 16x. It replays a recorded RusKey run
with no login and no cost. Then open Gap Report for the verdicts and Scoreboard for GapFinder against
a standard coding agent. Code: https://github.com/Sayjad21/GapFinder (MIT license).

## Inspiration

Sayjad Rahman spent weeks reproducing RusKey, a SIGMOD 2024 paper about a key-value store built on
RocksDB. His numbers for Figure 6 did not match the paper's, and the paper does not say why. The
cause could be a setting it never states, the scale of the data, or something else, and finding out
means running one controlled experiment after another, each starting from the same loaded database.
The tools we know of check whether a paper reproduces. We did not find one that searches for why it
doesn't, so we built it, and we made it say "unexplained" when the evidence does not support a cause.

## What it does

You give GapFinder a paper PDF and the artifact's repo. It reads the paper into a claim ledger (every
result the paper claims, each with a quote that must match the PDF) and a ranked list of settings the
results could depend on. It builds and loads the artifact once in Token Factory Sandboxes, then forks
one branch per hypothesis from that exact state. The output is a Gap Report with one card per claim:
a label, the setting that explains the gap (if any), the evidence for the value, a noise band, the
held-out checks, and the checkpoint and command to replay the branch.

The labels are Explained, Paper-artifact inconsistency, Partially explained, Fits but unsupported,
Inconclusive, Reproduced and Unexplained. A value that closes the gap but has no evidence behind it is "Fits but
unsupported", never "Explained". GapFinder changes experimental conditions only (configs, flags,
workload, build options, environment). It never edits the paper's algorithm code, and a diff guard
enforces that.

![Gap Report card](https://raw.githubusercontent.com/Sayjad21/GapFinder/main/docs/img/report.png)

To run it yourself without keys: `python scripts/try_it.py` runs a full investigation on a GapBench
dev task from recorded model answers, with the experiments running on your machine
([README](https://github.com/Sayjad21/GapFinder#quick-start-no-keys-free)). Running a new paper needs
a Token Factory key.

## How we built it

The pipeline has five stages: claim ledger, assumption space, checkpoint tree, search, Gap Report.
The search screens one change per branch, confirms survivors with repeats, combines the best, bisects
combinations to a minimal set, then verifies. Verification reverts each setting (the gap must come
back), checks the held-out claims (they must not get worse beyond noise), and looks for evidence that
the authors used the value (paper, then code, then web search). When the budget runs out, nothing is
labelled from runs that were not confirmed.

**How we use Nemotron on Token Factory.** Every call goes through one router
([router.py](https://github.com/Sayjad21/GapFinder/blob/main/gapfinder/models/router.py)) that splits
the reasoning trace from the answer, recovers once from an empty answer, repairs malformed JSON,
checks a hard spend cap before each call, and caches every response.
- **Nemotron 3 Ultra** (`nvidia/Nemotron-3-Ultra-550b-a55b`): the two long-context reasoning calls
  per paper. It extracts the claim ledger from the paper and builds the assumption space from the
  paper and the repo map.
- **Nemotron 3 Super** (`nvidia/nemotron-3-super-120b-a12b`): filters the extracted claims down to
  results, and triages failed branches (it reads the error and proposes a valid value). It is also the
  model behind the baseline agent we compare against (mini-swe-agent).
- **Nemotron 3 Nano** (`nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`): a fallback metric parser for log
  formats the deterministic parsers do not know, with every value grounded in the log. We exercised
  it in a spike only, because every artifact in this project prints a format the deterministic
  parsers already handle.
- **Not used:** Nemotron 3 Nano Omni is not served on Token Factory, so GapFinder has no model that
  reads figures. The RusKey Figure 6 values were digitized outside the pipeline.
- Usage and billed cost per tier are in the
  [README table](https://github.com/Sayjad21/GapFinder#how-we-use-nemotron-on-token-factory), taken
  from the spend ledger. [[V1.0: refresh the calls, tokens and billed dollars per tier, and the
  billed total, from eval/results/spend_ledger.jsonl after the final runs]]

**How we use Token Factory Sandboxes.**
- **One loaded database, many forks.** The checkpoint tree builds once and loads once. Each
  hypothesis forks from the deepest checkpoint still valid for it: a config change forks the loaded
  database, a dataset change reloads from the build, a build flag rebuilds. Sandbox VMs have 4 vCPUs
  and 3.9 GB, so we run CPU-only artifacts.
- **Checkpoint IDs as a measurement.** Identical filesystems get identical IDs. With `--noise-setups N`
  GapFinder loads the database N times with the same command before trusting a noise band. For RusKey,
  5 loads with the identical command gave 5 different checkpoints. A noise band from forked repeats
  alone would have hidden that.
- **Replayable answers.** Every attribution names its checkpoint and exact command. The replay site
  plays recorded runs and costs nothing.
- **Guards on our side.** Each command runs under a CPU-time limit, and a guard on the reported
  sandbox cost refuses new runs past a set total. Two MC Dropout arms, its confirmation runs and its post-hoc
  diagnostic ran in Sandboxes (up to 48 simultaneous operations), and RusKey ran its 127-branch
  search there. GapBench's
  toy artifacts run on the local backend.

## Evaluation

All numbers below link to the file they come from. The test protocol was committed before any test
run ([PROTOCOL.md](https://github.com/Sayjad21/GapFinder/blob/main/eval/gapbench/PROTOCOL.md)). With
8 tasks, nothing here is a conclusive win, and we do not claim one.

### GapBench blind test, run 1

Eight tasks drawn at random by a sealed generator, from a seed created after GapFinder was frozen
(git tag `pre-tasks-1`). Three runs of each arm per task, 24 runs per arm. The tasks use our two toy
artifacts, and we designed the generator's categories and value pools, so these are blind tasks, not
outside papers. Source:
[gapbench_test_v1_summary.json](https://github.com/Sayjad21/GapFinder/blob/main/eval/results/gapbench_test_v1_summary.json).
- **GapFinder:** 0 of 24 runs confidently wrong (95% interval 0 to 14%). It abstained correctly in 9
  of 9 runs on tasks with no findable cause. On tasks with a cause it named the right cause in 5 of
  15 runs and part of it in 2; in the other 8 it abstained (6) or gave no answer (2). Median run:
  4 of 8 tasks solved (interval 22 to 79%). Median cost per run $0.05, median wall time 52 s.
- **Baseline** (mini-swe-agent with Nemotron 3 Super, same inputs and dollar cap): 14 of 24 runs
  confidently wrong (58%, interval 39 to 76%), correct abstention in 1 of 9, right cause in 4 of 15
  runs. Median run: 1 of 8 tasks solved (interval 2 to 47%). Median cost per run $0.06, median wall
  time 129 s.
- **Ablation without verification:** 7 of 24 runs confidently wrong (29%, interval 15 to 49%).
  Verification is what keeps wrong answers out.
- **Honest limitation, from the ablations:** the arm with random hypothesis order and the arm with the
  evidence step off both found more causes than the full pipeline (6 of 8 tasks in the median run
  each, against 4 of 8), still with no confident wrong answer. On these tasks, the ledger ranking and
  the evidence gate cost recall. The intervals overlap, so the data do not separate these arms, but
  we are not claiming the ranking or the evidence step helps here.
- **Caveats:** the intervals treat the 3 runs of a task as independent, which they are not, so they
  are optimistic. The interval on tasks solved overlaps between GapFinder and the baseline. The
  separation we do see is in confident wrong answers (0 of 24 against 14 of 24), and it comes from 8
  tasks on toy artifacts.
- **Run 2 (frozen v1.0, run exactly once more, per the protocol):** [[V1.0: GapFinder confidently
  wrong k of 24, correct abstention k of 9, tasks solved in the median run k of 8; baseline-super
  the same three numbers; the three ablation arms; from eval/results/gapbench_test_v2.json after
  scoring with --runs 4,5,6]]
- **Independent AI-authored tasks:** [[V1.0: if tasks written by an independent AI model were run,
  their result reported separately from the generator tasks, from the by_source entry
  "ai_author" in the scored file; otherwise delete this bullet]]

The 4 dev tasks (the ones GapFinder was tuned on) are kept apart: GapFinder 4 of 4 with no false
attribution, the baseline 2 of 4 with 50% false attribution
([gapbench_dev_v7.json](https://github.com/Sayjad21/GapFinder/blob/main/eval/results/gapbench_dev_v7.json)).

### External case: MC Dropout (Gal and Ghahramani, ICML 2016)

A real paper whose reproduction gap was documented by its authors, with an answer key sealed before
any run and revealed after. Semi-blind: our TODO file named the documented cause. We ran a scaled
reproduction (100 Monte Carlo passes, 3 splits). Full write-up:
[RESULT.md](https://github.com/Sayjad21/GapFinder/blob/main/eval/external/mc-dropout/RESULT.md).
- **All four arms ended Unexplained** (normal, evidence step off, no README, all flags in random
  order). None made a false attribution, and none found the documented cause, so by the pre-registered
  key none earns credit.
- **The documented cause is real for the target.** When we ran it ourselves (`epochx=10 hidden=1`,
  both needed), Energy RMSE moved from 0.364 to a median of 1.716 against the paper's 1.66. Neither
  setting alone does it (0.533 and 0.427).
- **It breaks the held-out claim.** The same setting gives Yacht RMSE 2.996 against the paper's 1.11,
  where the defaults give 0.831. GapFinder's held-out check rejects a change that makes another claim
  worse.
- **So the miss was coverage, not verification.** In a post-hoc run (not blind, scores unchanged) we
  wrote the documented values into the hypothesis set by hand. GapFinder tested them, confirmed the
  Energy effect (1.723 against 1.66), saw Yacht at 1.987 against 1.11, and rejected the pair. The
  label was Unexplained, with the pair reported as the closest configuration. In the real runs
  the search never tried a value near `epochx=10`, because the ledger read the paper's "10x more
  iterations" as unstated and the generic grid started at 250.
- **Why Yacht probably cannot be matched:** the authors' own 2018 README says the paper-era code tuned
  hyperparameters with Bayesian optimization shared across all splits, which contaminated the test
  sets, and was replaced by a per-split grid search. That is a code change, not a setting, so
  GapFinder cannot test it. We did not test it either; this is the probable reason, not a result.
- **Caveats:** semi-blind, a 3-split scaled reproduction, and the arms ran across local Docker and
  Sandboxes because a Sandboxes operation is capped at 3,600 s (deviations are in
  [FROZEN.md](https://github.com/Sayjad21/GapFinder/blob/main/eval/external/mc-dropout/FROZEN.md)).

### RusKey, the founder case

Figure 6 of RusKey, run end to end in Sandboxes at 2M keys (the paper used 100M, which we could not
test). Source:
[FINDINGS.md](https://github.com/Sayjad21/GapFinder/blob/main/papers/ruskey/FINDINGS.md).
- **Verdict: Unexplained.** 127 branches from 13 database loads. Nothing explains the balanced-workload
  claims. The paper's 8 bits per key brings both balanced ratios to the paper but breaks the held-out
  write-heavy ratio, so verification rejects it.
- **The setup is not reproducible.** Loading the database with the identical command gave a different
  checkpoint every time: 12 loads, 12 checkpoints, and the naive K1/K5 ratio ranged from 0.52 to 1.38
  ([ruskey_load_variance.json](https://github.com/Sayjad21/GapFinder/blob/main/eval/results/ruskey_load_variance.json)).
  The 127-branch run had drawn an outlier load, so two of its observations were corrected.
- **With the load-to-load spread in the noise band** (5 independent loads), K1/K5 is within noise of
  the paper, with a wide band, and K10/K5 is 31% short and Unexplained
  ([search_setups](https://github.com/Sayjad21/GapFinder/blob/main/papers/ruskey/search_setups/gap_report.md)).
- **Forking vs not forking, same search, 22 branches each:** 8 database loads instead of 22, setup cost
  $1.88 instead of $5.21 (64% less), total $4.48 instead of $8.07 (45% less). These are the cost figures
  Sandboxes report, which are not billed in the Beta
  ([ablation_ruskey.json](https://github.com/Sayjad21/GapFinder/blob/main/eval/results/ablation_ruskey.json)).
- **Claim ledger against a gold set signed off by the paper's reproducer:** claim precision 1.00 (40 of
  40, measured on the paper the prompts were tuned on), headline-claim recall 1.00, all-claim recall
  0.93. Setting recall was 0.67, below our 0.80 bar: the tuner's mode flags are missed
  ([ledger_ruskey_v5.json](https://github.com/Sayjad21/GapFinder/blob/main/eval/results/ledger_ruskey_v5.json)).

## Challenges and what we learned

- **Noise is the hard part.** Our 127-branch RusKey run forked everything from one database load, and two of
  its observations had to be corrected once we measured 12 loads. Now the noise band includes load-to-load spread,
  every confirmed effect must pass a bootstrap test, and a result inside a wide band is "Inconclusive",
  not "Reproduced". Forked repeats from one load are too narrow to stand in for fresh loads on two of
  three RusKey ratios
  ([ruskey_fork_comparability.json](https://github.com/Sayjad21/GapFinder/blob/main/eval/results/ruskey_fork_comparability.json)).
- **Quotes must match.** Claims and assumptions are dropped, not repaired, when their quote is not in
  the PDF or the repo. On RusKey 17 extracted claims were dropped as ungrounded.
- **Reasoning traces.** The models return their trace in different places, and sometimes an empty
  answer. The router handles both.
- **Two bugs the ablation exposed.** A single screen run could produce a label after the budget ran
  out, and 8 branches still in flight when the budget stopped were never recorded. Both are fixed.
- **Sandboxes limits, learned the hard way.** An operation is capped at 3,600 s. The reported
  `elapsed_time` is CPU time summed over processes, which made us read a 4-core VM as one core until
  we measured it. The reported `cost` is diagnostic and reached thousands of dollars on the MC Dropout
  runs while the console showed no Sandboxes charge. The details are in our
  [feedback](https://github.com/Sayjad21/GapFinder/blob/main/docs/FEEDBACK_SUBMISSION.md).
- **Honesty cost us a headline.** The strongest-looking result would have been "found the cause". On
  the real paper, RusKey, and on the external case, the honest answer was Unexplained, and we kept it.

## What's next

- Derive candidate values from the paper's own numbers. The MC Dropout miss came from reading "10x
  more iterations" as unstated; it should become `epochx=10`.
- Wider generic grids, so a random-order search can reach values far from the defaults.
- A new label for "explains the target but conflicts with a held-out claim", so a result like MC
  Dropout's `epochx=10 hidden=1` is reported as what it is, not folded into Unexplained.
- Sharding one experiment across several Sandboxes operations, for cells that exceed the 3,600 s cap.
- A second external case where the cause is hidden from us (Paragraph Vector on IMDB), and a RusKey
  positive control with a planted setting.
- Longer term: artifact-evaluation committees as users, GPU papers, and more paper types. Today's
  limits are CPU-only VMs, a harness spec that a human confirms, and toy artifacts in the benchmark.

## Provenance

GapFinder was built during the submission period; the git history shows when each part was written.
The RusKey reproduction it is tested on is Sayjad Rahman's earlier research, used here as a test case.
Its source code is private and is not in the repository; only the built program was uploaded to a
Sandboxes snapshot. The MC Dropout case uses the public code and paper of Gal and Ghahramani, unmodified
except for one documented patch (100 Monte Carlo passes instead of 10,000).

## Links

- Code, MIT license: https://github.com/Sayjad21/GapFinder
- Replay site: https://sayjad21.github.io/GapFinder/
- Video: [[V1.0: YouTube URL, public, under 3 minutes]]
- Feedback on Token Factory, Sandboxes and Nemotron: [FEEDBACK_SUBMISSION.md](https://github.com/Sayjad21/GapFinder/blob/main/docs/FEEDBACK_SUBMISSION.md)

**Built with:** Nemotron 3 Ultra, Nemotron 3 Super, Nemotron 3 Nano, Nebius Token Factory, Token
Factory Sandboxes, Python, React, mini-swe-agent, Tavily.
