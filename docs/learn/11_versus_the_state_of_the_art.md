# 11. Compared with the state of the art

The short answer: **nobody has published a system that does what GapFinder does, so there is no state of the
art to beat head to head.** The closest work solves neighbouring problems. GapFinder has been compared
directly with one thing only: a general coding agent on our own synthetic benchmark. There it is much safer.
Against everything else, the honest answer is "not measured".

---

## 1. Is there a state of the art for this exact task?

The task: given a paper and its code, find *why* the code doesn't give the paper's numbers, by running it.

A search of the literature (2026-10-23) found no system that diagnoses the cause of a reproduction gap. The
nearest work reproduces papers, and reports whether it managed to, not why it failed:

| Work | What it does | Best result reported |
|---|---|---|
| PaperBench (Starace et al., ICML 2025) | agents rebuild 20 ICML papers from scratch | best agent: 21% of the grading rubric |
| RECLAIM (2026) | agents reproduce papers' claims from the released code | best agent: 41% when code, data and weights are all released, 27% when the model must be trained, 12% with no code |
| REPRO-Bench (2025) | agents judge whether social-science results reproduce | best existing agent about 21% accuracy (below the 25% of guessing among four options) |
| CORE-Bench (2024) | agents run a study's code and report its results | (scores not collected here) |
| "Automated Reproducibility Has a Problem Statement Problem" (2025) | argues the field has no agreed problem definition yet | (a position paper) |

None of these answers our question, so their numbers can't be compared with ours. What they do show is that
even reproducing a paper is hard for today's agents, and diagnosing a gap is a step beyond that.

## 2. The neighbouring problems, and how GapFinder relates to each

| Field | Its best-known methods | What GapFinder borrows | Compared? |
|---|---|---|---|
| Fixing bugs in code (SWE-bench) | agents that localise, propose fixes and check them with tests: Agentless solves 32% of SWE-bench Lite | the same loop, with the paper's numbers as the test (the mutation round, the patch round, the code proposer) | no. Our setting has no test suite, only a few noisy numbers |
| Finding the buggy line (fault localisation) | statistical methods; large-model methods (AutoFL is about 20% better than the classic Ochiai method at top-1 on Defects4J; AgentFL finds 157 of 395 bugs at top-1) | mutation-based localisation (MUSE, Metallaxis), program slicing | no. GapFinder's code-defect results are weak (2 of 6 planted in c3), so it is very likely worse than these on their benchmarks |
| Diagnosing misconfiguration in computer systems | PeerPressure (statistics from many machines: right in 12 of 20 real cases), ConfAid (tracing values through the program), EnCore | tracing where values go (the runtime trace) | no |
| Calibrating expensive simulators to data | history matching (climate, oil reservoirs), Bayesian calibration with model discrepancy, ensemble methods with about 100 runs | history matching and the discrepancy term, directly | no; GapFinder uses these as published |
| Checking data in production ML | TFDV at Google: statistics against a schema | not used: the planted tasks put the change on the paper's side, so a check of our own runs finds nothing | no |
| Mutation testing for deep learning | DeepCrime's operators from real faults | its operators, to plant faults in the curriculum and to search for them | no |

## 3. What was measured head to head

Only one comparison exists, on **GapBench**, our generator of small fake papers. The comparison system was a
general coding agent (mini-swe-agent) using Nemotron 3 Super, the same inputs and the same dollar cap.

| Test | GapFinder | Coding agent |
|---|---|---|
| Confidently wrong, three sealed tests (90 runs) | **0 of 90** | 49 of 90 |
| GapBench-mini blind test, confidently wrong (24 runs, done twice) | **0 and 0** | 14 and 12 |
| Tasks solved in the median run (of 8, done twice) | **4 and 6** | 1 and 2 |
| GapBench dev (4 tasks) | 4 of 4, no false attribution, $0.04 a task | 2 of 4, 50% false attribution, $0.07 a task |

**How strong is this?**
- **Strong on safety.** 0 against 49 confident mistakes is a large difference, measured on sealed tasks.
- **Weaker on finding causes.** The sets are small (15 runs with a cause per test) and the intervals overlap.
  Our own ablation was humbling: on GapBench, trying settings in random order, or switching off the evidence
  check, found as many causes or more. So GapFinder's ranking and its evidence rule cost recall there; what
  they buy is safety.
- **Limited in scope.** The baseline used the same mid-sized model. A coding agent on a frontier model was
  never tried. The tasks are toys, not real papers.

## 4. What has not been measured

- **Real papers against any other system.** GapFinder's own blind record is 1 correct, 1 partial, 5 missed
  and 1 confidently wrong out of 8 sealed papers, and all 8 predate the work since 2026-10-20.
- **Its parts against the best tools in their own fields.** The mutation round was never run on a standard
  fault-localisation benchmark, and the environment builder was never compared with Repo2Run.
- **Whether the planted curriculum reflects real papers.** It plants random causes into papers that already
  reproduce. Real causes are not random: some kinds are far more common than others.

## 5. What is genuinely new, as far as we found

These have no close published counterpart that we know of:
- **The whole loop:** claims read with exact quotes, then forked sandbox runs, a differential over six cause
  classes, then a report that says when the answer is outside every class it can test.
- **The scale probe:** finding that a paper's value is a fixed multiple of the code's (a unit or counting
  convention), from a sweep the paper reports.
- **History matching applied to ML papers:** the method itself is decades old; applying it to say "no setting
  can explain these claims, look in the code" is new here.
- **The confidence rules:** a confident label needs a finished search, every setting tried, and evidence beyond
  the code itself; a code fix is never "Explained".
- **Testing code changes in memory** through an import hook, so no file is ever edited.
- **The planted-gap curriculum** on papers that already reproduce, with controls, sealed answers, and a
  generator kept separate from the engine it tests.

Everything else is borrowed, usually directly (page 10).

## 6. The verdict, in plain words

- **Better than a general coding agent at not being confidently wrong**, clearly, on synthetic tasks.
- **Not shown to be better than anything at finding causes on real papers.** There is nothing to compare
  against yet, and its own rate is low.
- **Where it works today:**
  - scale and unit conventions;
  - settings when the paper reports enough numbers to tell them apart;
  - abstaining honestly.
- **Where it is weak:**
  - code defects;
  - ties on few numbers;
  - and, as seed 7 showed, the scale probe can be confidently wrong when it tries many factors on noisy data.

## Sources

- [PaperBench](https://proceedings.mlr.press/v267/starace25a.html)
- [RECLAIM](https://arxiv.org/html/2609.28850v1)
- [REPRO-Bench](https://arxiv.org/pdf/2507.18901)
- [CORE-Bench](https://arxiv.org/pdf/2409.11363)
- [Automated Reproducibility Has a Problem Statement Problem](https://arxiv.org/abs/2601.04226)
- [Agentless](https://arxiv.org/html/2407.01489v2)
- [AutoFL evaluation](https://arxiv.org/html/2308.05487v3)
- [AgentFL](https://arxiv.org/html/2409.13642v2)
- [PeerPressure](https://www.usenix.org/legacy/events/osdi04/tech/full_papers/wang/wang_html/)
- [EnCore](https://www.research.ibm.com/publications/encore-exploiting-system-environment-and-correlation-information-for-misconfiguration-detection)
- [TensorFlow Data Validation](https://research.google/pubs/pub48974/)
- [ES-MDA, ensemble size and iterations](https://link.springer.com/article/10.1007/s10596-018-9731-y)
- [Practical identifiability and experiment design (Liu, Maini & Baker)](https://arxiv.org/html/2506.11311v1)
- GapFinder's own numbers: `README.md` (GapBench), `docs/CONTEXT_v11.md` section 5 (real papers, dev suite,
  planted curriculum)

← Back to [the start](README.md)
