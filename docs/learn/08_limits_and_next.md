# 8. Limits and what's next

No tool is perfect. Knowing the limits helps you use GapFinder well.

## What GapFinder can't do (yet)

- **It can change settings, hard-coded numbers and function defaults, but not code structure.** A loop, a
  pipeline order or an algorithm change (MC Dropout's per-split tuning, pygcn's normalisation) can be
  *pointed at* as a lead, never tested. That is on purpose: rewriting code until the number fits would
  explain nothing.
- **Sandboxes only: CPU, 4 cores, about 4 GB of memory, up to an hour per run.** Papers that don't fit
  (GraphMAE's COLLAB needed more memory just to load) are out of scope, and some causes only show at full
  scale.
- **A person writes and approves the harness spec.** `spec-draft` writes a draft, but a human decides how the
  code is run, and that takes some work per paper.
- **When the paper's numbers can't tell answers apart, GapFinder can't either.** It then reports a set of
  equally good answers. More numbers, statements of relations, and the paper's own tables are what break
  ties.
- **The evidence on real papers is thin:**
  - blind real papers so far: 0 of 2 correct (one miss, one confident mistake), both before the latest
    rebuild;
  - development papers, with answers known: VGAE found end to end; pygcn honestly "Unexplained";
  - practice tasks: accuracy flat across versions (within noise), safety held.

## What's next (in priority order)

1. **A frozen batch of real papers, all in Sandboxes**, run without changes in between and reported as a
   rate: found, missed, confidently wrong. The first one (GIN, Informer, PatchTST, GAT, G-Mixup) is running.
2. **A sealed blind batch** of 3-5 new papers after that, frozen first. Only this can show the method works
   on papers it hasn't seen. Protocol: `eval/external/BLIND_CASE.md`.
3. **Use more of each paper's information:** more numbers, relation claims, how many runs a paper's number
   averages.
4. **Bigger test sets,** so accuracy differences between versions become measurable.

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
