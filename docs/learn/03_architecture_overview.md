# 3. The big picture

GapFinder has three big stages: **read**, **experiment** and **report**. This page shows how they fit together
in the current version (c5). [The next page](04_components_deep_dive.md) opens each box, and
[page 10](10_where_the_ideas_came_from.md) says where each idea came from.

```
   PAPER (PDF + LaTeX source)          CODE (repo)
          │                                 │
          ▼                                 ▼
 ┌──────────────────┐            ┌────────────────────────┐
 │ Claim ledger      │            │ Repo map + links + trace│   ← READ: what does the paper claim?
 │ (Nemotron, quotes │            │ (no AI; one dry run)    │     which settings exist, what do they do?
 │  grounded)        │            └───────────┬────────────┘
 └────────┬─────────┘                         │
          └──────────────┬────────────────────┘
                         ▼
               ┌───────────────────┐
               │ Assumption space   │  ← candidate causes and values to try
               └─────────┬─────────┘
                         ▼
   ┌─────────────────────────────────────────────────────────┐
   │  SEARCH (cloud Sandboxes, forked from checkpoints)        │  ← EXPERIMENT
   │  zero-run probes: reporting rules, library and era        │
   │  screen → early code screen → confirm → combine → bisect  │
   │  → verify → history matching → discrimination             │
   │  → scale probe → patch round → mutation round             │
   │  → value intervals → identifiability                      │
   └──────────────────────────┬───────────────────────────────┘
                              ▼
                  ┌────────────────────────┐
                  │ Differential + labels   │  ← which cause class, how sure
                  └───────────┬────────────┘
                              ▼
                  ┌────────────────────────┐
                  │ Gap Report + web replay │  ← REPORT: verdict per claim, with proof and replay
                  └────────────────────────┘
```

## Stage 1: read

- **Claim ledger.** Nemotron 3 Ultra reads the paper and lists every result it claims, each with an exact
  quote. Super removes non-results. A claim is kept only if its number really is in its quote, page or table.
  The tables come from the LaTeX source and the PDF, checked against each other, and the appendix gets its
  own reading.
- **Repo map.** A plain program (no AI) lists every setting, its default, its help text and where it is
  defined. A commented-out block of settings is kept as an alternative to try whole.
- **Links.** Paper words are matched to code settings ("learning rate" to `--lr`) by text search, then
  checked by what the value does when the program runs.
- **Trace.** One short run watches where every value lands (the optimizer, a dropout layer, a loop length)
  and which lines execute.
- **Assumption space.** The AI combines all this: "the paper never says how many epochs; the code uses 500".
  The AI may change the order of tests, never which settings are skipped.

## Stage 2: experiment

The **harness spec** (a YAML file, drafted automatically by `gapfinder harness` and approved by a person)
says how to build and run the code and which settings may change.

**Sandboxes and forks.** The experiment is built and loaded once and saved as a checkpoint. Every test starts
from that save point.

**The search, in order:**
1. **Zero-run probes:**
   - **reporting rules:** read from runs already made (did the paper report the best epoch? the best of N
     seeds?);
   - **library and era:** the package releases and the code as of the paper's date.
2. **Screen:** each candidate value once, coarse values first; the repo's alternative settings blocks too.
3. **Early code screen:** the cheapest code tests (top hard-coded numbers, the first code edits) run before
   the settings use up the budget. A class scheduler decides how much budget to keep for code.
4. **Confirm:** repeat the promising candidates, as a race.
5. **Combine:** pairs of settings, and whole alternative blocks.
6. **Bisect and verify:** drop what isn't needed. Then the three checks: undo it, other numbers, evidence.
7. **History matching:** is any configuration consistent with every claim? If not, "out of space".
8. **Discrimination:** runs at the paper's other conditions to separate tied answers.
9. **Scale probe:** is the paper's value a fixed multiple of the code's?
10. **Patch round:** hard-coded numbers changed in memory.
11. **Mutation round:** small code edits, in memory, scored on every claim.
12. **Value intervals and identifiability:** the range of values that fit, and whether the claims can name
    the cause at all.

## Stage 3: report

- **The differential** scores every candidate from every cause class against all the claims, including
  "outside every class".
- **The label** follows strict rules. A confident label needs:
  - a finished search;
  - every setting tried;
  - evidence beyond the code.
  A code edit is never "Explained".
- **The Gap Report** is written as Markdown (for people) and JSON (for programs). The web app replays it.
  Every claim points to the exact experiments behind it.

## Where things live in the repository

| Folder | What's inside |
|---|---|
| `gapfinder/ingest/` | reading: PDF text, arXiv source, table grids, repo map, links, static code checks |
| `gapfinder/ledger/` | the claim ledger, grounding, the assumption space |
| `gapfinder/models/` | the AI connection, the cache and the spending guard |
| `gapfinder/sandbox/` | running code: backends, checkpoints, forks, noise, the in-memory patch hook, the trace hook, the runtime shim |
| `gapfinder/search/` | the search engine, candidate values, verification, history matching, mutation, the code proposer |
| `gapfinder/diagnose/` | the differential, reporting rules, library drift, discrimination |
| `gapfinder/report/`, `gapfinder/api/`, `web/` | the Gap Report, the web server and the browser app |
| `gapfinder/harness_build.py`, `env_build.py`, `env_year.py` | building the harness and the environment, the paper-year packages |
| `eval/` | how we test GapFinder: GapBench, the dev suite, real papers (`external/`), the planted curriculum (`planted/`), results |
| `docs/` | documentation; `docs/CONTEXT_v11.md` is the current technical context |

Next: [Inside each part →](04_components_deep_dive.md)
