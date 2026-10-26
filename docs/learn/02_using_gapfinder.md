# 2. Using GapFinder

## The fastest way to see it work (free, no account)

```bash
uv venv --python 3.11 .venv && uv pip install --python .venv -e ".[dev,baseline]"   # once
python scripts/try_it.py                 # runs a full investigation on a small practice task (~20 s)
python scripts/try_it.py --list          # shows the four practice tasks
```

This runs everything on your own computer. It uses recorded answers from the AI models, so it costs
nothing and needs no internet. At the end it prints a Gap Report and saves it to
`runs/try_it/<task>/gap_report.md`.

## Looking at recorded runs in the browser

```bash
.venv/bin/uvicorn gapfinder.api.server:app --port 8000      # then open http://localhost:8000
```

The site has five parts (design notes in `web/DESIGN.md`):
- **Home:** a live "gap gauge" on four solved cases. It is a measuring rule showing the paper's number, the
  code's number as released, and the code's number after GapFinder's change, with the gap highlighted between
  them. Below it is the record of all 16 real papers, version by version, misses included.
- **Cases:** one row per real paper: the documented cause, what GapFinder found, and its verdict on each version.
  Each case page shows the gauge, the versions, a replay of the investigation (press play) and the full Gap Report.
- **Synthetic:** the planted-gap and GapBench cases it solved, filterable by kind.
- **Evidence:** every measurement, with what it can and can't show: the sealed blind papers, the planted rates per
  version, the dev suite, and the comparison with a general coding agent.
- **How it works:** the pipeline, step by step, and what it can't do yet.

The data comes from `python scripts/build_showcase.py`, which writes `demo/runs/showcase.json`. For the static
site, run `python scripts/export_static.py web/public/data --showcase`.

The public version is at <https://sayjad21.github.io/GapFinder/>. It replays recorded runs; nothing is
spent.

## Running it on a real paper

You need two kinds of accounts:
- a Token Factory account, for the AI models (Nemotron);
- Sandboxes access, for running the code in cloud machines.

The keys go in a `.env` file (see `SETUP.md`). The steps:

**Step 1. Read the paper (the "ledger").**
```bash
gapfinder ledger --paper paper.pdf --repo path/to/code --out runs/my-paper
```
This produces a list of the paper's claims and a list of settings that might matter. It costs a few cents.

**Step 2. Describe how to run the code (the "harness spec").**
```bash
gapfinder harness <github url> --commit <sha> --local <checkout> --ledger runs/my-paper --target C7 --out runs/my-paper/harness
gapfinder spec-draft path/to/code   # or: just draft the YAML file
```
This produces a small YAML file: how to build the code, how to run it, which settings (knobs) can be changed,
and how to read the result. `gapfinder harness` also writes `HARNESS.md`, with every choice and its reason.
**A person must read and approve it**, because only a human should decide how the code is run.

**Step 3. Pick the target numbers.** These go in a small JSON file:
- the main paper number to explain (the *target*);
- other numbers from the same experiment, which GapFinder must not make worse (*held-out* claims).

**Step 4. Search for the cause.**
```bash
gapfinder search --spec my-spec.yaml --targets targets.json \
    --assumptions runs/my-paper/assumptions.json --claims runs/my-paper/claim_ledger.json \
    --backend contree --max-runs 200 --out runs/my-paper/search
```
`--max-runs` is your budget: the most experiments GapFinder may run.

## How to read a Gap Report

Each result gets a **card** that answers five questions:

| Question | What it tells you |
|---|---|
| Which experiment changed it? | the exact setting change, the command, the saved checkpoint you can replay |
| What did the paper report? | the paper's number, with the exact quote and page |
| What did we measure? | our numbers, how much they vary between repeats (the "noise band") |
| Why do we believe it? | the three checks, each PASS or FAIL (see below) |
| What remains unknown? | settings it couldn't test, and other close candidates |

Each card also has a **label**. These are the labels, from most to least sure:

| Label | Meaning in plain words |
|---|---|
| **Explained** | this setting causes the gap; all checks passed, and there's evidence the authors used it |
| **Paper-artifact inconsistency** | the paper says one value, the code uses another, and that difference causes the gap |
| **Partially explained** | this setting closes much of the gap, with evidence, but not all of it |
| **Fits but unsupported** | this setting fits the numbers, but nothing says the authors used it. Treat it as a strong guess |
| **Explains target, conflicts with held-out** | it fixes the main number but breaks another one. Part of the cause is probably elsewhere |
| **Inconclusive** | the measurements are too noisy to tell |
| **Reproduced** | the code already matches the paper |
| **Unexplained** | nothing it could change explains the gap |

Newer reports add a **History matching** section, which looks at all the claims together. It can say:
- **in space:** some setting could explain everything;
- **out of space suspected / likely:** no setting can, so look in the code, the data or the evaluation.

It may also list **leads**, lines in the code worth checking, and **equally good configurations** when
several answers fit the numbers just as well.

## The MC Dropout report, read with these rules

- **Label: "Explains target, conflicts with held-out: `epochx=10, hidden=1`".** These two settings fix
  Energy, but Yacht gets worse.
- **History matching: "out of space suspected".** No setting fixes both.
- **Leads:** `batch_size = 128` (net/net.py:70), the per-split grid search (experiment.py:163), and
  others.
- **Patch round:** it tried changing those hard-coded numbers in memory. A smaller batch size helped
  Yacht a lot, but no change fixed both numbers, so it didn't claim a code fix.

Next: [The big picture →](03_architecture_overview.md)
