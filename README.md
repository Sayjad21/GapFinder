[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

# GapFinder

**Everyone asks whether a paper reproduces. GapFinder asks why it doesn't.**
Give it a paper PDF and the artifact's repo. It builds a claim ledger and a
ranked list of unstated experimental assumptions with Nemotron on Token
Factory. It builds and loads the artifact once in Token Factory Sandboxes,
then forks one branch per hypothesis from that exact checkpoint. The output
is a Gap Report: per-claim attributions with evidence, noise bands, and
replayable checkpoint IDs. It says "unexplained" when it should.

> Status: M0 spikes S5 and S7 pass; M1 ledger meets its bars on RusKey; M3
> search passes all nine planted toy behaviours; GapBench-mini dev set: 4/4
> solved with 0 false attributions. Waiting on Sandboxes Beta access for the
> sandbox spikes (S1-S4) and the RusKey end-to-end run.
> Plan: [docs/PLAN.md](docs/PLAN.md) · spikes: [tests/spikes/](tests/spikes/README.md).

## What works today

| Piece | Where | State |
|---|---|---|
| Frozen data objects (Claim, Assumption, Branch, Attribution) | `gapfinder/ledger/schemas.py` | done, tested |
| Nemotron tier router: reasoning-trace split, empty-answer recovery, JSON repair, response cache, token/cost meter | `gapfinder/models/router.py` | done, tested offline |
| PDF ingest (page text + figure crops), repo map (gflags/argparse/CMake/Make/option defaults with `file:line`) | `gapfinder/ingest/` | done |
| Grounding checker (quotes must string-match the PDF; `file:line` must exist and contain the flag) | `gapfinder/ledger/grounding.py` | done, tested |
| Claim extraction and assumption space (Ultra), figure reading (Nano Omni) | `gapfinder/ledger/`, `gapfinder/ingest/figures.py` | written, needs S5 |
| Sandbox backends: Contree (real) and local directory snapshots (stand-in) | `gapfinder/sandbox/backend.py` | local tested; Contree needs S1 |
| Checkpoint tree, depth planner, async runner (40-way cap, `RUN_TAG`, infra-only retries), no-fork ablation | `gapfinder/sandbox/` | tested on local |
| Grounded metric parser (db_bench, RocksDB stats, kv, JSONL), noise band (2×MAD), cost meter, JSONL event log + replay | `gapfinder/sandbox/` | tested |
| mini-swe-agent baseline adapter (same sandbox, linear history) | `eval/baseline/` | tested on local |
| RusKey gold ledger / assumptions (draft), S6 gap check | `papers/ruskey/` | draft, needs author review |
| Search loop: screen, confirm, combine, bisect, verify (counterfactual, held-out, evidence) | `gapfinder/search/` | 9/9 toy behaviours |
| Gap Report (Markdown + JSON, replay recipes) | `gapfinder/report/` | done |
| Spend cap + ledger for every paid call, including the baseline agent | `gapfinder/models/budget.py` | done |
| GapBench-mini: RL + tabular artifacts, task generator, leakage check, harness, scorer | `eval/gapbench/` | 4 dev tasks; test tasks pending |
| Web enrichment: web evidence search (Tavily) for the plausibility gate | `gapfinder/search/evidence.py` | done, cached |
| Web UI: replay, Gap Report, scoreboard; FastAPI + SSE | `web/`, `gapfinder/api/` | done, browser-tested |
| RusKey Figure 6 harness (spec, cell script, S3/S4 on it) | `papers/ruskey/` | ready; waiting on Sandboxes |

## Quick start (no credentials needed)

Teammates: see [SETUP.md](SETUP.md) for the full setup, keys and budget rules.

```bash
uv venv --python 3.11 .venv && uv pip install --python .venv -e ".[dev,baseline]"
.venv/bin/pytest                                  # unit + local-backend integration tests
.venv/bin/gapfinder fanout --spec eval/toy/hidden_knob.yaml --knobs eval/toy/knobs.json --backend local
.venv/bin/gapfinder repomap path/to/any/repo
```

With credentials in `.env` (see `.env.example`):

```bash
gapfinder ledger papers/ruskey/ruskey_paper.pdf --repo <path-or-url>
gapfinder fanout --spec <paper>.yaml --knobs knobs.json --backend contree
```

## Web UI (replay mode)

```bash
npm --prefix web ci && npm --prefix web run build      # once
.venv/bin/uvicorn gapfinder.api.server:app --port 8000  # then open http://localhost:8000
```

It lands on **Replay**, which plays a recorded run (from `demo/runs/`) at 1x, 4x or 16x and costs
nothing. The other tabs are the **Gap Report** cards (with replay commands) and the **Scoreboard**
(GapBench arms, per-task answers). Live mode stays off and refuses politely until Sandboxes
access and an access code are configured. Browser test: `pytest -m e2e tests/e2e`.

## Scope rule

GapFinder changes only experimental conditions: configs, flags, workload,
build options and environment. It never edits the paper's algorithm code. A
diff guard enforces this.

## Provenance

GapFinder is being built during the hackathon submission period. The RusKey
reproduction it's tested on is Sayjad Rahman's earlier research, used here as
a test case.
