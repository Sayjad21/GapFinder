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
- **We compare versions properly, too.** The **dev suite** (`eval/dev_suite.py`) re-runs old and new
  versions on the same public tasks, and `eval/compare_suites.py` compares them task by task with a
  statistical test. It showed that most engine changes after v1.1 were within noise. Only the safety
  result and the real-paper results are clear.

## Real papers

The synthetic tasks prove the method works in a controlled world. Real papers are harder. There are three
kinds of real-paper test, from weakest to strongest evidence:

| Kind | What it means | Results so far |
|---|---|---|
| **Known answer** (MC Dropout, the development set) | the cause is documented and we know it; useful for building, but every success can be the result of tuning to it | MC Dropout names the documented settings (v1.3); VGAE found end to end; pygcn honestly "Unexplained" |
| **Frozen batch** | papers with known causes, but the code is frozen first and not changed between them, and the harness writers don't see the causes | devbatch-1 (5 papers, all in Sandboxes): 1 correct, 0 confidently wrong |
| **Sealed blind** | another model picks the paper and seals the answer; GapFinder is frozen; the key is opened only after the run is committed | blind-1 FastGCN: missed. blind-2 GraphMAE: confidently wrong |

The sealed blind cases are the only ones that count as proof. Both were on older versions, and both led to
the rebuild described in [the journey](07_the_journey.md).

## Planted causes in real repositories (`eval/planted/plant.py`)

Documented reproduction gaps are rare, so the measuring itself is slow. A planted-cause task skips the wait:
1. take a real repository that already runs in Sandboxes;
2. a random generator with a fixed seed hides **one** change: a setting given another value, or a constant
   in the code changed in memory;
3. the change runs a few times, and the average becomes the "paper" number;
4. the change is kept only if it moves the number by more than 3 times the noise;
5. the answer is sealed, and GapFinder searches without seeing it.

The answers are read only by the scoring step, and no change to GapFinder is ever judged on these tasks.
They measure; they don't train. Scoring splits each miss into two kinds: "the planted change was among the
configurations that fit" means the claims can't tell the options apart; "not found" means the search missed
it.

First result (pygcn, 3 tasks): 2 correct, 0 confidently wrong. The miss was a case where two different
changes give the same single number.

Next: [The journey →](07_the_journey.md)
