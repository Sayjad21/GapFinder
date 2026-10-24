# 8. Limits and what's next

No tool is perfect. Knowing the limits helps you use GapFinder well. This is the state on 2026-10-24, with
c5 as the current version.

## What GapFinder can't do (yet)

**On real papers it is unproven.**
- The 8 sealed blind papers gave 1 correct, 1 partial, 5 missed and 1 confidently wrong.
- All 8 were run before the work since 2026-10-20. Nothing since has blind evidence.

**Some kinds of cause are found, most are not.** On planted gaps, the current line (c1 → c3 → c5):

| Kind of gap | Found | Why the misses happen |
|---|---|---|
| Scale or unit convention | mostly | noisy data can let a wrong factor fit |
| Setting | about 3 in 10 | several settings move the few reported numbers alike (a tie); values off the tried grid |
| Code defect | rarely | the right edit is outside the operators, or ranked too low, or the budget runs out first |
| Training-data cut | sometimes | the engine's cuts (1/2, 3/4) don't match other fractions closely enough |
| Reporting rule | 1 of 1 | (only one planted) |
| Paper-era code, old library release | never tested | these never moved a planted number enough |

**One number can't decide between causes.**
- When the paper reports one or two numbers, many settings fit them equally well.
- GapFinder says so ("not identifiable from the paper's numbers") but can't do better.
- Only more reported numbers break such ties.

**The scale probe has an open defect.**
- It tries several factors.
- On noisy or flat data a wrong factor can fit by chance, and the confident label doesn't account for how many
  were tried.
- It caused two confident mistakes in c6 on seed 7; c5 has the same logic.

**It changes settings, constants, defaults and small code edits, never code structure.**
- A different loop, pipeline order or algorithm can be pointed at, never tested.
- That is on purpose: rewriting code until the number fits would explain nothing.

**Sandboxes only:**
- CPU, 4 cores, about 4 GB of memory, up to an hour per run;
- papers that need more are out of scope.

**The harness still needs a person to approve it.**
- `gapfinder harness` builds it automatically (5 of 6 reproduced papers rebuilt), but it has not yet run end
  to end on an unseen repository.

**The tests so far can't show progress.**
- Every comparison of two versions had too few differing tasks to be significant.
- The adopted steps (c1 → c3 → c5) each went +2 with 0 losses: a direction, not proof.

## What's next, in order

1. **Make the scale probe's confident label account for the factors tried.** Either a multiple-comparison
   correction, or confidence only for the curve's own best factor verified on the first try. It must be judged
   on a fresh batch (seed 8), not on seed 7, which revealed it.
2. **Fix c6's two crashes:**
   - split leads only for numbers;
   - a bounded exponent in the fraction formula.
   Then decide which of c6's ideas are worth a fresh test.
3. **A test big enough to decide:**
   - about 50 gap tasks, with more tasks per paper and more papers;
   - before it runs, say what difference it can detect;
   - and run c1 on seed 6, for a direct c1-against-c5 comparison.
4. **A sealed blind batch of real papers on the current version:** the only proof that counts.
5. **The harness end to end on an unseen repository.**
6. **Model-dependent parts not run for budget:**
   - a claim labeller;
   - two-pass prose reading;
   - link adjudication.

## How to contribute

- **Run it on a paper you know.** The more real cases, the better we understand where it works.
- **Read `docs/CONTEXT_v11.md`.** It has the current architecture, every result and the open list.
- **Check every change on the dev suite and on a fresh planted batch, against the old frozen version:**
  ```bash
  python eval/dev_suite.py --base 12000 --code ../gf-new
  python eval/compare_suites.py --a <old results> --b <new results>
  python eval/planted/curriculum.py make --level 1 --seed <new seed> ...   # only after the new version is frozen
  ```
- **Never look at sealed answers before a test is scored.** It's the one rule that keeps the results
  meaningful.

Next: [Glossary →](09_glossary.md)
