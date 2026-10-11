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

## Deviation 1 (execution fix)

Everything above is the frozen record and is unchanged. This section was added afterwards, before any search had produced a result, under the rule above ("if something blocks a run, fix only that, and describe the fix").

**What failed.** All four arms stopped in calibration. In each arm the five naive cells (`bash run_cell.sh dir=energy,yacht epochx=500 hidden=2 n_splits=3 ...`) hit the 14,400 s run timeout (exit 124), so calibration raised "naive configuration failed: only 0 successful runs". That is 20 cells (4 arms x 5), each cut off at 14,400 s, with no result from any of them. No search ran, no hypothesis was tested, and no model call was billed ($0 spent on searches). It happened with `GF_MAX_CONCURRENCY=6` and also when the machine was otherwise idle (arms 2 to 4).

**Measured cause: BLAS thread oversubscription, not Docker I/O.** The image's numpy (1.13.3, OpenBLAS wheel) starts one OpenBLAS thread per core the container can see, and Docker Desktop shows every container all 12 cores. The networks here are tiny (50 units, batches of 128), so those threads do almost no useful work but spin and fight for cores. A full cell runs two `experiment.py` processes (energy, yacht), and the search runs 6 cells at once, so 12 processes, each with up to 12 spinning threads, shared 12 cores. Measurements on this machine (12 CPUs), same settings within each row, otherwise idle unless stated:

| Run | Default threads | `OPENBLAS_NUM_THREADS=1` |
|---|---|---|
| plain `docker run`, yacht, epochx=2, n_splits=1 | 41 s wall, 158.8 CPU-s | 32 s wall, 31.4 CPU-s |
| plain `docker run`, energy, epochx=20, n_splits=1 | 105 s wall, 932 CPU-s | 50 s wall, 49.8 CPU-s |
| same, checkpoint bind-mounted from a Windows path as LocalBackend does | 41 s (yacht, epochx=2) | 51 s (energy, epochx=20) |
| through LocalBackend (`fanout`), energy+yacht, epochx=20, n_splits=1, one cell | 88 s | not run separately |
| through LocalBackend, 6 such cells at once | 656-670 s each | 91-99 s each |

- The bind mount is not the cause: the cell writes a few KB of result files under `/work` (one line per grid step, no per-epoch logging), and bind-mounted and plain runs took the same time (41 s vs 41 s at default threads; 51 s vs 50 s at one thread).
- Theano's compile cache lives in the container's own `/root/.theano`, so every `--rm` container compiles from cold (about 20 s once per cell), which is a fixed cost, not the cause.
- Contention is the cause: 6 cells at once (12 processes on 12 cores) were each 7.5 times slower than one cell alone at default threads (660 s vs 88 s), although 12 single-threaded processes fit on 12 cores. With one thread per container the same 6 cells ran about as fast as one cell alone (91-99 s vs 88 s).

**The fix (infrastructure only).** `gapfinder/sandbox/backend.py`: `LocalBackend` now passes `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1` and `MKL_NUM_THREADS=1` to every Docker container it starts, unless the run sets its own value (`DOCKER_THREAD_ENV`, merged under the run's env). The non-Docker LocalBackend path is unchanged. A test (`tests/integration/test_local_docker.py`) checks that the container sees `1 1 1` by default and that a run's own env value wins. The full test suite passes (237 tests).

**Files and hashes.** `mcd.yaml`, `harness/run_cell.sh` and `docker/Dockerfile` are unchanged, with the same sha256 as in the table above (re-checked: `148c480a...`, `28cdc6c8...`, `9d7612f9...`). The Docker image is not rebuilt: it is still `sha256:7206df29c1c85795d6b003548e1191f21371097bbe44740c274e5eff8deb9ee0`. The only changed code is the LocalBackend change above, which is outside the frozen file list.

**Proof at full size.** The exact default cell (`bash run_cell.sh dir=energy,yacht epochx=500 hidden=2 n_splits=3 ...`, the real `mcd.yaml`), 6 of them concurrently through LocalBackend (`gapfinder fanout --spec mcd.yaml --knobs <6 empty change sets> --noise 0 --backend local --concurrency 6`, `GF_CACHE_ONLY=1`), all finished with exit 0 in **3,127 to 3,171 s (52 to 53 min)** each, 3,176 s for the whole fan-out, against the 14,400 s timeout (4.5x headroom). Before the fix the same cell did not finish in 14,400 s.

**Recommended settings.** Keep `GF_MAX_CONCURRENCY=6` (6 cells x 2 datasets = 12 processes on 12 cores; more concurrency adds no throughput, it only lengthens each cell proportionally). Keep the 14,400 s timeout: it is enough with 4.5x headroom at that concurrency (it would still be enough at concurrency 12, about 105 min a cell by linear scaling, but nothing is gained). A search of 40 runs at default size is then at most about 7 waves of about 53 min, roughly 6 hours of wall time per arm (less where a knob shrinks the cell, e.g. a smaller `epochx`).

**One side effect, stated plainly.** Thread count changes the order of floating-point sums, so a run at one thread does not bit-match a run at 12 threads (energy, epochx=20, n_splits=1: RMSE 0.4546 at one thread vs 0.4535 at default threads, a 0.2% difference). Runs at one thread are bit-identical to each other. The gap check in `gapcheck/` was run at default threads; its numbers are unaffected in substance, but a repeat of it would differ in the third digit.

**What is unchanged.** The hypothesis space, the knobs and their defaults, the candidate values, the targets (`targets_mcd.json`), the scoring rule, the search logic (screen, confirm, combine, bisect, verify), the prompts (hashes above) and the models are all unchanged. The experiments themselves are the same commands in the same image; only the number of BLAS threads each container uses changed.
