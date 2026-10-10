# Freeze record: MC Dropout external case (ext-eval-1)

Written 2026-10-10 14:54:01 UTC by `scripts/freeze_record.py`, before any GapFinder search on this case. Nothing below may change until the case is scored.

No GapFinder code, prompt, spec or target changes for this case after this record. If something blocks a run (a crash, a missing parser), fix only that, and describe the fix in RESULT.md.

## Code

- GapFinder commit: `95edcd8591cc77bfd61889e4b45c4a6627cb87fa`
- Tag to create on that commit: `git tag ext-eval-1 95edcd8591cc && git push origin ext-eval-1`

## Models (from the config; environment overrides are applied)

| Tier | Model ID |
|---|---|
| ultra | `nvidia/Nemotron-3-Ultra-550b-a55b` |
| super | `nvidia/nemotron-3-super-120b-a12b` |
| nano | `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B` |
| omni | `nvidia/Nemotron-3-Nano-Omni` |

## Prompts (sha256)

| Prompt | sha256 |
|---|---|
| ASSUMPTION_PROMPT | `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b` |
| CLAIM_PROMPT | `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34` |
| FILTER_PROMPT | `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32` |
| MISSING_SENTENCE_PROMPT | `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0` |
| TRIAGE_PROMPT | `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e` |

## Inputs (sha256)

| File | sha256 |
|---|---|
| `eval/external/mc-dropout/mcd.yaml` | `148c480aa9e841e2456fb10e9686bee79d3ef04d7ab183d50caede9c92e68da3` |
| `eval/external/mc-dropout/targets_mcd.json` | `a06fd720f3ce6164fb363e0b4b9dfa57618db4139ec78600438cb5620d9b104d` |
| `eval/external/mc-dropout/harness/run_cell.sh` | `28cdc6c8508d1dcf74bc1296b16f9d28eefff033c75fe39471aee91a85947627` |
| `eval/external/mc-dropout/docker/Dockerfile` | `9d7612f917bbcc997f6b8cc1eb4a80bd2b76cd191efbfc85b203fb652c6d8943` |
| `eval/external/mc-dropout/answer_key.sha256` | `cc969f61b1aa95d290f8793709bd10f85e1a4c43af2e5d4abcb5a2280726e0f5` |

- Docker image `gf-mcdropout`: `sha256:7206df29c1c85795d6b003548e1191f21371097bbe44740c274e5eff8deb9ee0`
- Artifact: Gal & Ghahramani's DropoutUncertaintyExps at the commit pinned in the Dockerfile, with the one documented patch `T = 10000` to `T = 100`.

## Budget

- Branch runs per search: `--max-runs 40` (each arm gets the same).
- Dollar cap per search (Nemotron, billed): `--cap 0.5`. The runs are local Docker cells, so there is no sandbox cost; ledger extraction is separate, about $0.10-0.30 of Ultra per run (one for the normal and evidence-off arms, one on the stripped clone).
- Values tried per knob in the screen: `--candidates-per-knob 2` (every arm).
- Seed for the random arm: `0`.

## Arms (pre-registered)

All arms use the same spec, targets, budget and build. Energy RMSE is the target claim; Yacht RMSE is held out. Concrete is not searched.

| Arm | What changes | What it shows |
|---|---|---|
| normal | nothing | the product as is |
| evidence off | the evidence check is skipped; a closing value is at most 'Fits but unsupported' | the experiments alone carry the verdict |
| no README | the ledger runs on a clone with README*, readme* and docs/ removed (scripts/strip_docs.py), and the evidence check is off | the cause was found without the documentation |
| all flags, random | hypotheses are every knob of the harness spec with generated candidate values, uniform priors, no paper values, no ledger; random order | the ranking is not what found it |

Commands (after the ledgers exist; see TODO P0-1 Step 4):

```bash
GF_SPEND_TAG=ext-mcd GF_MAX_CONCURRENCY=6 gapfinder search --spec eval/external/mc-dropout/mcd.yaml --targets eval/external/mc-dropout/targets_mcd.json --assumptions runs/mcd-ledger/assumptions.json --claims runs/mcd-ledger/claim_ledger.json --backend local --max-runs 40 --candidates-per-knob 2 --cap 0.5 --out eval/external/mc-dropout/run-normal
GF_SPEND_TAG=ext-mcd GF_MAX_CONCURRENCY=6 gapfinder search --spec eval/external/mc-dropout/mcd.yaml --targets eval/external/mc-dropout/targets_mcd.json --assumptions runs/mcd-ledger/assumptions.json --claims runs/mcd-ledger/claim_ledger.json --no-evidence-gate --backend local --max-runs 40 --candidates-per-knob 2 --cap 0.5 --out eval/external/mc-dropout/run-evidence-off
GF_SPEND_TAG=ext-mcd GF_MAX_CONCURRENCY=6 gapfinder search --spec eval/external/mc-dropout/mcd.yaml --targets eval/external/mc-dropout/targets_mcd.json --assumptions runs/mcd-ledger-nodocs/assumptions.json --claims runs/mcd-ledger-nodocs/claim_ledger.json --no-evidence-gate --backend local --max-runs 40 --candidates-per-knob 2 --cap 0.5 --out eval/external/mc-dropout/run-no-README
GF_SPEND_TAG=ext-mcd GF_MAX_CONCURRENCY=6 gapfinder search --spec eval/external/mc-dropout/mcd.yaml --targets eval/external/mc-dropout/targets_mcd.json --hypotheses repomap --rank random --seed 0 --backend local --max-runs 40 --candidates-per-knob 2 --cap 0.5 --out eval/external/mc-dropout/run-all-flags-random
```

Ledger inputs:

```bash
gapfinder ledger <paper.pdf> --repo <clone> --out runs/mcd-ledger
python scripts/strip_docs.py <clone> <clone>-nodocs
gapfinder ledger <paper.pdf> --repo <clone>-nodocs --out runs/mcd-ledger-nodocs
```
