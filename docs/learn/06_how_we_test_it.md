# 6. How we test it

How do you know whether a "why doesn't it reproduce?" tool works? You need cases where **you already know
the answer**, but the tool doesn't. This page explains our test bench and how to read its numbers
honestly.

---

## GapBench: practice papers with a planted cause

**GapBench** (`eval/gapbench/`) is a set of small artificial "papers":
1. We take a small program: a CartPole reinforcement-learning agent (`rlbench`), or a logistic
   regression classifier (`mlbench`).
2. We secretly change a setting (say, `normalize=minmax`) and run it. Those numbers become "the paper's
   numbers".
3. We write a short fake paper that reports those numbers but *doesn't* say which setting was used.
4. GapFinder gets the fake paper and the program with its default settings, and must find the hidden
   setting.

There are several kinds of task:

| Category | What's planted | Right answer |
|---|---|---|
| known cause | one setting | name it |
| decoy | one setting, plus a tempting wrong one | name the right one, avoid the decoy |
| interaction | two settings that only matter together | name both |
| no cause / noise only | nothing; the numbers are shifted or just noisy | "Unexplained" or "Inconclusive" |
| incomplete | a setting GapFinder isn't allowed to change | don't blame something else |
| out of space | a bug in an older copy of the code | say it's outside the settings |

## The task generator, and why it rejects tasks

The tasks are made by a program (`gen_tasks.py`), not by hand. A person writing tasks would know what
GapFinder is good at. The generator checks every task before keeping it:
- the gap must be bigger than the noise (at least 3 noise bands);
- **no other setting may fit the claims just as well.** Otherwise the "right answer" isn't really
  findable. The check covers single settings and pairs, and uses the same "fits equally well" rule as
  GapFinder;
- the fake paper must not leak the answer.

## Sealed tests: how we avoid fooling ourselves

1. **Freeze** GapFinder's code with a git tag (e.g. `v1.3`).
2. **Write down the success criteria first**, in `eval/gapbench/PROTOCOL.md`.
3. **Make a random seed** *after* the freeze. The seed decides the tasks, so nobody could tune toward
   them.
4. **Generate** 10 tasks. Their answers go into a sealed folder; only a fingerprint (hash) is published.
5. **Run** GapFinder and several comparison "arms" 3 times on every task.
6. **Reveal** the answers, check the fingerprint, and score.

The arms:

| Arm | What it is |
|---|---|
| gapfinder | the full system |
| gapfinder-noverify | the same, without the three checks: shows what verification is worth |
| gapfinder-noevidence | without the evidence check |
| gapfinder-random | trying settings in random order instead of the AI's ranking |
| baseline-super | a general coding agent with the same AI model and budget |

## How to read the results

Use the latest three sealed tests:

| Test | Confidently wrong (of 30) | Correct causes (of 15) | Correct "nothing to blame" (of 15) | Balanced accuracy |
|---|---|---|---|---|
| v1.1 | 0 | 7 + 1 partial | 15 | 0.73 |
| v1.2 | 0 | 12 | 15 | 0.90 |
| v1.3 | 0 | 9 + 1 partial | 15 | 0.80 |

The coding-agent baseline was confidently wrong in 19, 8 and 22 of 30 runs.

**How to read this honestly:**
- **"Confidently wrong" comes first.** It's the error that hurts users. 0 in 90 runs is the strongest
  result.
- **Balanced accuracy** is the average of "found the cause when there was one" and "didn't blame anything
  when there wasn't". A tool that always says "Unexplained" scores 0.50, so 0.50 is the floor to beat.
- **The sets are small.** Each test has only 15 runs with a cause, over 5 tasks. Different tests draw
  tasks of different difficulty, so 12 then 9 doesn't mean v1.3 got worse.
- **We compare versions properly, too.** The **dev suite** (below) re-runs old and new versions on the same
  public tasks and compares them task by task. It showed that most engine changes after v1.1 were within
  noise. Only the safety result is clear.

## Real papers

The synthetic tasks prove the method works in a controlled world. Real papers are harder. There are three
kinds of real-paper test, from weakest to strongest evidence:

| Kind | What it means | Results so far |
|---|---|---|
| **Known answer** (MC Dropout, the development set) | the cause is documented and we know it; useful for building, but every success can be the result of tuning to it | MC Dropout names the documented settings; VGAE found end to end; pygcn honestly "Unexplained" |
| **Frozen batch** | papers with known causes; the code is frozen first, and the harness writers don't see the causes | devbatch-1 (5 papers): 1 correct, 0 confidently wrong. devbatch-2 (3 papers): 0 causes found, 3 correct abstentions (all three reproduced: their causes were noise and protocol inside the paper's own number) |
| **Sealed blind** | another model picks the paper and seals the answer; GapFinder is frozen; the key is opened only after the run is committed | 8 papers: **1 correct** (Fair Clustering, λ=100), **1 partial** (RippleNet, the learning rate), 5 missed, **1 confidently wrong** (GraphMAE, before the confidence rules) |

The sealed blind cases are the only ones that count as proof. **All 8 were run before 2026-10-20**, so none of
the work since (the six cause classes, the planted curriculum, versions c1-c6) has blind evidence yet.

## The dev suite: a free regression check

`eval/dev_suite.py` re-runs the search on every public GapBench task (69 runs with a cause, 57 without),
locally and for free. `eval/compare_suites.py` compares two versions task by task with a sign test.

| Version | Runs with a cause correct | Confidently wrong |
|---|---|---|
| c1 (two replicates) | 100 of 138 | 0 |
| c4 (two replicates) | 96 of 138 | 0 |
| c5 (two replicates) | 99 of 138 | 0 |
| c6 (two replicates) | 97 of 138 | 0 |

Identical code swings by about ±5 per run, so all of these are the same within noise. Every run had all 57
abstentions correct. It guards against regressions; it is too easy and too synthetic to show progress.

## The planted-gap curriculum (`eval/planted/curriculum.py`)

Documented reproduction gaps are rare, so measuring on them is slow. Since 2026-10-21 the main development
measurement plants hidden changes into papers whose code already reproduces.

**How a task is made:**
1. **Papers:** six that already reproduce: pygcn, FastGCN, Fair Clustering, SparseTSF, RippleNet, VGAE. Also
   their harnesses rebuilt automatically (named `-h`), which add per-epoch values and paper-year packages.
2. **Planting:** a seeded generator picks a family and hides **one** change:
   - a setting at another value;
   - a scale convention ("the paper's v is the code's 2 × v"), with a two-point sweep reported as extra claims;
   - a code defect (an arithmetic or reduction edit, or DeepCrime's "bias added/removed");
   - a data-pipeline change (DeepCrime's "training data cut");
   - a reporting rule (each metric's best epoch).
3. **The paper's numbers:** the change runs 3 times, and the average becomes "the paper's number".
4. **Keeping it:** only if the change moves the number by at least 5 run-to-run standard deviations (level 1)
   or 3-5 (level 2), and by at least 1% of the value. About one task in five is a **control**: nothing
   planted, so saying nothing is right.
5. **Sealing:** the answer is sealed. The search runs without the paper and without a ledger.

**How a round works:**
- the new version is frozen first;
- then a fresh seed makes the tasks;
- both the old and the new frozen versions search every task;
- the scorer compares them task by task.

**Every round so far:**

| Round | Versions | Gap tasks | Old correct | New correct | New better / worse | Confidently wrong (old / new) | Adopted? |
|---|---|---|---|---|---|---|---|
| seed 2 | c1 alone | 14 | 4 | - | - | 0 | baseline |
| seed 3 | c1 vs c2 | 16 | 4 | 7 | 4 / 1 | 0 / 0 | no: gains were picks among ties |
| seed 4 | c1 vs c3 | 13 | 4 | 6 | 2 / 0 | 1 / 0 | **yes** |
| seed 5 | c3 vs c4 | 14 | 4 | 5 | 3 / 2 | 0 / 0 | no: its gains were faults its own operator generated |
| seed 6 | c3 vs c5 | 16 | 5 | 7 | 2 / 0 | 0 / 0 | **yes** |
| seed 7 | c5 vs c6 | 27 | 10 | 7 | 1 / 4 | 0 / 2 | no: worse, two confident mistakes, two crashes |

Every control in every round was answered correctly (69 control searches).

**What kinds of gap are found (the adopted line, c1 → c3 → c5):**
- **Scale conventions:** mostly found.
- **Settings:** about 3 in 10. Most misses are ties on few numbers.
- **Code defects:** rare (the first in c3).
- **Data cuts:** sometimes since c5.
- **Reporting rule:** 1 of 1.
- **Paper-era code and package releases:** never plantable on these papers.

**Lessons the curriculum taught about testing itself:**
- **Too small to decide.** Each comparison had only 2-5 tasks where the versions differed. A sign test needs at
  least 6 all one way for p < 0.05, so **no comparison has been significant**. Two adopted steps each went
  +2 with 0 losses: a consistent direction, not proof.
- **Circular tasks.** On seed 5 the generator drew faults from the engine's newest operator. Now it uses
  operators frozen at an old version, and its data cuts differ from the engine's.
- **Scoring mistakes.** A tied reading of the reporting rule was first scored "confidently wrong". A tie
  now counts like a planted value inside the set of equal values. Ties are also scored apart ("in a credible
  set of at most 3").
- **Planted gaps the engine treats as reproduced.** Gaps between 0.5% and 1% were planted before the 1% rule
  matched the engine's floor.

These are development measurements: the builder knows every family. They are never blind evidence.

Next: [The journey →](07_the_journey.md)
