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

## The real paper: MC Dropout

The synthetic tasks prove the method works in a controlled world. A real paper is harder. We used MC
Dropout because its cause is documented:
- an answer key was written and sealed (hashed) before the first run;
- GapFinder ran on the real code in cloud Sandboxes (scaled down so it fits the machines).

**Important:** this case is **not blind any more**. Its answer was revealed after v1.0, and later versions
were improved with it in view. A truly blind real paper is the main missing evidence; the protocol for one
is in `eval/external/BLIND_CASE.md`.

Next: [The journey →](07_the_journey.md)
