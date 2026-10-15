# 3. The big picture

GapFinder has three big stages: **read**, **experiment** and **report**. This page shows how they fit
together. [The next page](04_components_deep_dive.md) opens each box.

```
   PAPER (PDF)                  CODE (repo)
       │                            │
       ▼                            ▼
 ┌─────────────┐             ┌─────────────┐
 │ Claim ledger │             │  Repo map   │   ← READ: what does the paper claim?
 │ (Nemotron)   │             │ (no AI)     │     what settings exist in the code?
 └──────┬──────┘             └──────┬──────┘
        └──────────┬────────────────┘
                   ▼
          ┌─────────────────┐
          │ Assumption space │  ← which settings might explain the gap, and what values to try
          └────────┬────────┘
                   ▼
   ┌────────────────────────────────────────┐
   │  SEARCH  (in cloud sandboxes, forked)    │  ← EXPERIMENT
   │  screen → confirm → combine → bisect     │
   │  → verify → history matching → patches   │
   └────────────────┬───────────────────────┘
                    ▼
            ┌───────────────┐
            │  Gap Report    │  ← REPORT: verdict per claim, with proof and replay
            │  + web replay  │
            └───────────────┘
```

## Stage 1: read

- **Claim ledger.** An AI model (Nemotron 3 Ultra) reads the paper and lists every result it claims,
  each with an exact quote. A second model (Nemotron 3 Super) removes things that aren't results. Every
  quote must match the PDF word for word, or it's thrown away.
- **Repo map.** A plain program (no AI) reads the code and lists every command-line setting, its default
  value and where it is defined (file and line).
- **Assumption space.** The AI combines the two: "the paper never says how many epochs; the code uses
  500; the result probably depends on it". Each assumption has candidate values to try and the evidence
  for it.

## Stage 2: experiment

This is where most of the work happens.

**The harness spec** (a small YAML file a person approves) says how to build and run the code, and which
settings may be changed.

**Sandboxes and forks.** The code runs in cloud machines (Token Factory Sandboxes). GapFinder builds and
loads the experiment **once** and saves a checkpoint, like a save point. Every test then starts from
that save point. This is called **forking**, and it's much faster and cheaper than starting from
scratch each time.

**The search** goes through steps, like a detective narrowing down suspects:

1. **Screen:** try each setting change once.
2. **Confirm:** repeat the promising ones, to make sure the effect isn't luck.
3. **Combine:** try pairs, because sometimes two settings only matter together.
4. **Bisect:** if a combination works, remove the parts that aren't needed.
5. **Verify:** three checks, explained on the next page.
6. **History matching:** look at all the claims together. Can any setting explain all of them?
7. **Patch round:** if the answer is "no, look in the code", test hard-coded numbers in the code, in
   memory, without editing any file.

## Stage 3: report

- The **Gap Report** is written as Markdown (for people) and JSON (for programs).
- The **web UI** reads the JSON and shows the cards, the replay and the scoreboard.
- Every claim in the report points to the exact experiment, so anyone can replay it.

## Where things live in the repository

| Folder | What's inside |
|---|---|
| `gapfinder/ingest/` | reading: PDF text, repo map, config flow, static code checks |
| `gapfinder/ledger/` | the claim ledger and the assumption space |
| `gapfinder/models/` | the connection to the AI models, the cache and the spending guard |
| `gapfinder/sandbox/` | running code: backends (local, Docker, cloud), checkpoints, forks, noise, patch knobs |
| `gapfinder/search/` | the search engine, candidate values, verification, history matching |
| `gapfinder/report/` | the Gap Report |
| `gapfinder/api/`, `web/` | the web server and the browser app |
| `eval/` | how we test GapFinder: the GapBench benchmark, results, the MC Dropout case |
| `docs/` | documentation, including these pages |

Next: [Inside each part →](04_components_deep_dive.md)
