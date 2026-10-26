# The showcase: recorded runs for the web app

`python scripts/build_showcase.py` assembles this from runs already recorded and scored. It runs nothing and costs
nothing. The runs sit under `demo/runs/`, and the manifest is `demo/runs/showcase.json`.

## The three groups, and what each one is

| Group | Folder | What it is | How to label it on a page |
|---|---|---|---|
| `real` | `demo/runs/real/<paper>/` | earlier real papers re-run on the adopted engine (c5, frozen 2026-10-23) | **post-hoc demonstration.** Each cause is documented, and the engine was developed with several of these papers in view |
| `planted` | `demo/runs/synthetic/planted/<task>-<version>/` | planted-gap tasks that a frozen version solved: one hidden change planted into a paper whose code reproduces | **synthetic, development measurement**, scored by the curriculum's sealed scorer |
| `gapbench` | `demo/runs/synthetic/gapbench/<task>/` | GapBench dev-suite runs of c5 scored correct, one per task | **synthetic, development suite**, seen while tuning |

The only clean evidence is the sealed blind record of real papers: 1 correct, 1 partial, 5 missed and
1 confidently wrong, out of 8 (`docs/CONTEXT_v11.md` 5.1). A page that shows the wins should also show the rates.
The manifest includes them, misses included:
- `planted_totals`: every scored round, by version and seed, with counts by family;
- `gapbench_totals`: c5's full dev-suite outcome.

## The API

| Endpoint | Returns |
|---|---|
| `GET /api/showcase` | the manifest: `real`, `planted`, `gapbench` (one entry per case, with its id), `planted_totals`, `gapbench_totals` |
| `GET /api/runs?group=real` (or `planted`, `gapbench`) | the run list for one group: id, title, labels per claim, group, version, note |
| `GET /api/runs/<id>` | `meta` (the whole `meta.json`), the report, the event count |
| `GET /api/runs/<id>/replay?speed=16` | the recorded events over SSE |
| `GET /api/runs/<id>/report.md` | the Markdown Gap Report |

An id is the path below `demo/runs`, with `~` in place of `/`, for example `real~ripplenet` or
`synthetic~planted~L1-b3a-s6-1-c5`. The static export (`scripts/export_static.py`) writes the same data, including
`showcase.json`.

## `meta.json` fields

| Field | Groups | Meaning |
|---|---|---|
| `title`, `group`, `version`, `note` | all | the note says what the case is and how it was scored |
| `documented_cause`, `before`, `found`, `reading` | real | the documented cause; the result recorded before c5; c5's label and changes per claim; our one-line reading of c5 against the cause |
| `planted`, `family`, `found`, `label`, `verdict`, `seed`, `level`, `frozen`, `tied`, `rank` | planted | the planted change, in the scorer's words, and what the version found |
| `category`, `type`, `outcome`, `found`, `hidden`, `gap_closed` | gapbench | the task category and the outcome. `hidden` is the planted setting, for the dev-* tasks only; the test-* tasks' answers stay sealed |
