# 8. Limits and what's next

No tool is perfect. Knowing the limits helps you use GapFinder well.

## What GapFinder can't do (yet)

- **It can only change what the harness exposes.** If a cause is a setting nobody listed, it stays
  hidden. Patch knobs help, but only for hard-coded *numbers* in Python files.
- **Loops, pipelines and algorithm changes can't be tested.** MC Dropout's per-split hyperparameter
  tuning is an example: GapFinder can point to it as a lead, but can't change it.
- **CPU only.** The cloud machines have 4 CPUs and about 4 GB of memory. Big GPU papers must be scaled
  down, and some causes only show at full scale.
- **A person must approve the harness spec.** `spec-draft` writes a draft, but a human decides how the
  code is run.
- **When the paper's numbers can't tell answers apart, GapFinder can't either.** It then reports a set of
  equally good answers. More information from the paper, such as more numbers, figures or datasets, is
  the only real fix.
- **The evidence is still thin:**
  - each blind test has 15 runs with a cause, so accuracy differences between versions are within noise;
  - there is **no blind real paper yet**, because MC Dropout's answer was known while we improved the
    system.

## What's next (in priority order)

1. **A blind real paper.** Someone who hasn't worked on GapFinder picks a paper with a documented
   reproduction gap and seals the answer; GapFinder is frozen first. Protocol:
   `eval/external/BLIND_CASE.md`.
2. **Use more of each paper's numbers.** Every extra independent claim makes wrong answers easier to rule
   out.
3. **Fairer interaction tasks in the benchmark.** The generator should reject a task whenever another pair
   of settings fits as well, checked the way GapFinder itself searches.
4. **Bigger test sets.** Then accuracy differences between versions become measurable, not just the
   safety result.
5. **More kinds of patch knobs.** Settings read from data files; maybe small loop changes, with careful
   rules.

## How to contribute

- **Run it on a paper you know.** The more real cases, the better we understand where it works.
- **Read `docs/CONTEXT_v11.md`.** It has the full technical history, every measured result, and the
  current list of problems.
- **Check every change on the dev suite before keeping it:**
  ```bash
  python eval/dev_suite.py --base 3000
  python eval/compare_suites.py --a <old results> --b <new results>
  ```
- **Never look at sealed answers before a test is scored.** It's the one rule that keeps the results
  meaningful.

Next: [Glossary →](09_glossary.md)
