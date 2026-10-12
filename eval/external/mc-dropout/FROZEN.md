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

## Deviation 2 (backend: local Docker to Token Factory Sandboxes)

Everything above, including Deviation 1, is unchanged. This section was added after attempt 2 (local Docker), before any scored result, under the same rule ("if something blocks a run, fix only that, and describe the fix"). Attempt-2 local outputs are kept in `eval/external/mc-dropout/attempt2-local/` (see its README) and attempt-1 in `attempt1-timeout/`; the search runs of attempt 3 write to `eval/external/mc-dropout/run-<arm>/`.

**Why.** Local runs are too slow: attempt 2's normal arm took about 14 hours on the lead's laptop (26 branch runs, 12 cores, 6 cells at a time), and a teammate's laptop is far slower. Sandboxes give one VM per cell, so a whole wave of cells runs at once.

**Billing evidence.** Sandboxes usage is not billed during the Beta. The Nebius billing console showed no Sandboxes service and no Sandboxes charge for 6-12 October, although the spend ledger had by then recorded about $56 of reported sandbox `cost`. The Sandboxes docs describe the operation `cost` field as diagnostic only. GapFinder's own guard counts that diagnostic number, so for these runs it is raised through the environment (below); no GapFinder code changed.

**Base image on Sandboxes.** Checkpoint **`75aeac20-b2f1-4fed-83df-1554a229d51f`**, tagged **`gf/mcd/base-v1`**, built on 2026-10-12 through `ContreeBackend` (base `python:3.6-slim` by OCI name, then three build operations, then an upload of `harness/run_cell.sh`), following `docker/Dockerfile` step by step:
1. the Debian 11 apt sources pointed at `archive.debian.org` (same `sed` and `Check-Valid-Until` line as the Dockerfile), then `apt-get install -y --no-install-recommends g++ git ca-certificates` (g++ 10.2.1, git 2.30.2);
2. `pip install numpy==1.13.3 scipy==1.1.0 h5py==2.8.0 Theano==0.8.2 Keras==2.2.0`. `pip freeze` is identical to the Docker image's (h5py 2.8.0, Keras 2.2.0, Keras-Applications 1.0.2, Keras-Preprocessing 1.0.1, numpy 1.13.3, PyYAML 6.0.1, scipy 1.1.0, six 1.17.0, Theano 0.8.2);
3. `git clone https://github.com/yaringal/DropoutUncertaintyExps`, `git checkout 6eb4497628d12b0f300f4b4f6bdc386bebad565c`, copied into `/work` (with its `.git`), then the one documented patch `sed -i 's/T = 10000/T = 100/' net/net.py` (`git status` shows only `net/net.py` modified);
4. `harness/run_cell.sh` uploaded to `/work/run_cell.sh` (sha256 `28cdc6c8...`, the frozen hash).
Not part of a Sandboxes image: the Dockerfile's `ENV` lines (see below). The build script was a throwaway in the scratchpad and is not committed; the steps above are the whole recipe. Reported sandbox cost of the build: $0.22.

**Spec.** `eval/external/mc-dropout/mcd_sandbox.yaml` is `mcd.yaml` with three changes and nothing else (diff `mcd.yaml mcd_sandbox.yaml`, comments aside):
1. `base: docker:gf-mcdropout` became `base: ${GF_MCD_SANDBOX_BASE}` (set it to the checkpoint id above; the launcher does);
2. the run command is prefixed with `export THEANO_FLAGS=device=cpu,floatX=float32 KERAS_BACKEND=theano OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1;`. A Sandboxes run does not apply the image's `ENV`, and a spec has no environment section, so the Dockerfile's two variables and Deviation 1's thread caps have to come from the command. This is the same environment the Docker runs had;
3. `run.timeout: 14400` became `3600`. This one is forced: the Sandboxes API rejects any operation timeout above 3600 s (HTTP 400, "Timeout 14400 exceeds the maximum allowed value of 3600"; seen on the first smoke attempt).
Knobs, defaults, candidates, the run command's arguments, build command, metrics and `allowed_paths` are identical. (`--cap 0.5` is unchanged; the search's cost meter does not enforce it on sandbox cost, and the Nemotron cap in `budget.py` counts billed kinds only.)

**Environment for these runs.** `GF_SANDBOX_GUARD_USD=20000` (the reported-cost guard; the default $60 would stop the first arm within two cells), `GF_SANDBOX_CPU_LIMIT_S=60000` (the per-process `ulimit -t`; the default 300 would kill every cell), `GF_SPEND_TAG=ext-mcd-sandbox`, `GF_MAX_CONCURRENCY=10` per arm (40 in all, under the Beta limit of 50 simultaneous operations). `scripts/run_mcd_sandbox_arms.sh` starts the four arms of the "Arms" section in parallel with exactly those commands plus `--spec eval/external/mc-dropout/mcd_sandbox.yaml --backend contree`. Same `--max-runs 40 --candidates-per-knob 2 --cap 0.5`, same ledgers, same seed 0.

**Smoke and timing (Sandboxes, `GF_CACHE_ONLY=1`, no Nemotron calls).**
- Smoke: one naive cell through `gapfinder fanout --backend contree` with `dir=energy,yacht epochx=1 n_splits=1`: succeeded in 44 s of run time, parsed `energy_rmse`, `energy_ll`, `yacht_rmse`, `yacht_ll`. (With a single dataset `run_cell.sh` prints unprefixed names, so `yacht_rmse` only exists when two or more datasets run.) The same cell re-run in the Docker image with the same `RUN_TAG` gives energy RMSE 2.676988 vs 2.676989 and yacht RMSE 8.859091 vs 8.859091 (Sandboxes), i.e. the two backends agree to the last printed digit.
- One full-size default cell (`dir=energy,yacht epochx=500 hidden=2 n_splits=3`, alone, `--noise 0`): exit 0 in **2,673 s (44.6 min)**: energy 1,907 s, yacht 803 s; energy RMSE 0.3658, yacht RMSE 1.0880. User CPU 2,669 s equals the elapsed time, so a Sandboxes VM behaves like one effective core and the two datasets do not run faster in parallel. That is under the 3,600 s limit with 26% headroom (attempt 2 locally: 2,792-2,819 s for the same cell at 6 at a time). Reported cost of that cell: $26.73 (about $0.010 per CPU-second), diagnostic only.
- Expected wall time per arm: calibration (5 naive cells, one wave) plus about 35 branch runs in waves of 10, each wave 45-60 min: roughly 4-6 hours per arm, all four arms at once. The reported (unbilled) cost is about $27 per default cell, up to $36 per cell that hits the limit, so roughly $5,000-7,000 for the four arms against the $20,000 guard.

**Known consequence of the 3,600 s limit (information lost, stated plainly).** In attempt 2 the normal arm's non-default cells took, locally, 5,072-7,501 s for `hidden=4`, `hidden=5` and `epochx=1000`, and 8,674-12,472 s for `epochx=2000` (21 of 26 cells took over 3,600 s). On Sandboxes, any cell whose run is slower than about 1.35 times the default cell (roughly `hidden>=3` and `epochx>=700`, estimated from those local timings) will end as a timeout (exit 124, status `timed_out`) instead of a result. Cells with fewer epochs or hidden layers (including the paper's `epochx=10 hidden=1`) are cheaper than the default and unaffected. No timeout was changed beyond what the API forces, no knob or candidate was removed, and the search logic is unchanged; but a cause that only shows at a large `epochx` or `hidden` value can no longer be observed in these runs.

**What is unchanged.** The hypothesis space, the knobs and their defaults, the candidate values, the targets (`targets_mcd.json`), the scoring rule, the search logic (screen, confirm, combine, bisect, verify), the prompts (hashes above), the models, `harness/run_cell.sh` and `docker/Dockerfile` (hashes above) are all unchanged. The experiments are the same commands on the same pinned stack and repo commit; only where they run, the run-stage environment export and the per-operation timeout changed. Thread count is one per library, as in Deviation 1.

- Decision (2026-10-12): the team chose to run all four arms in Sandboxes (rather than keeping the
  completed local normal and evidence-off arms), knowing that cells longer
  than the 3,600 s Sandboxes limit end as timeouts. The completed local attempt-2 normal and
  evidence-off arms (both Unexplained) are kept in attempt2-local/ and reported alongside. This
  decision is under review (see the note below if it changes).

## Deviation 3 (sharded execution for the Sandboxes 3,600 s limit)

Everything above, including Deviations 1 and 2, is unchanged. This section was added before any scored Sandboxes result, under the same rule ("if something blocks a run, fix only that, and describe the fix"). Arms 1 and 2 (normal, evidence-off) were completed locally in attempt 2 (`attempt2-local/`, both Unexplained); this deviation is for arms 3 and 4 (no-README, all-flags-random) and any later Sandboxes run.

**The problem.** The Sandboxes API caps every operation at 3,600 s of wall time. Deviation 2 estimated that cells slower than about 1.35 times the default cell (roughly `epochx>=700`, `hidden>=3`) would time out, because it believed a Sandboxes VM was one effective core. In attempt 2 (local) 21 of 26 normal-arm cells took longer than 3,600 s, so a plain Sandboxes run would have lost the very hypotheses the case is about (`epochx` 1000 and 2000, `hidden` 4 and 5, larger `n_splits`).

**Measured: a VM has 4 effective cores, and Deviation 2's one-core reading was wrong.** On the base checkpoint (2026-10-12, Sandboxes, `GF_CACHE_ONLY=1`):
- `nproc` = 4, `/proc/cpuinfo` shows 4 processors, scheduler affinity 4, no cgroup CPU quota file;
- a CPU-burning Python loop, 30 s wall: 1 process got 30.0 CPU-s; 4 processes at once got 30.0 CPU-s each (no slowdown); 8 processes at once for 20 s got 10.0 CPU-s each, i.e. a total of 80 CPU-s in 20 s = 4 cores;
- the operation's reported `elapsed_s` is not wall time: it equals user plus system CPU summed over all processes (a test that took 63.9 s of real wall reported 180.4 s, and the 4-process test reported 150 s for a 60 s wall). That is why Deviation 2's "user CPU equals elapsed, so one core" was a misreading: the default cell's 2,673 s was 2,667 CPU-s over two parallel processes (energy 1,907 s, yacht 803 s, as the cell itself timed them), real wall about 1,910 s;
- the 3,600 s timeout is real wall: an operation with `timeout=30` ran 4 processes of 20 s each (80 CPU-s) and finished normally.

**The design (a): shard inside the VM. Harness only; no GapFinder code, no search, no artifact code change.** `harness/run_cell.sh` gets one new argument, `procs=<N|auto>`. With it, each (dataset, split) is its own `experiment.py` process with `n_splits=1`, run in its own copy of the dataset and `net/` folders (each shard is `run_cell.sh` run unsharded with `split_offset=<its split>`, so the split draw from `RUN_TAG`, the swapping of split files and every setting are the existing code), at most N at a time (`auto` is the VM's cores, 4; the spec's `OMP_NUM_THREADS=1` is ignored for this count), the datasets with more rows first. When all shards are done, their per-split result lines are put back in split order and aggregated by the same `stats` and `emit_metrics` code as an unsharded run, so the printed `rmse`, `rmse_sd`, `rmse_single`, `ll`, `mean_tau`, `splits_done`, `splits_used` and the per-dataset prefixes are the same. Differences in the printout: `wall_s` is the longest shard, `cpu_s` the sum, and `shards=`, `procs=` and `shards_wall_s=` are added. Without `procs`, the script behaves as before (the local Docker runs are unaffected). If any shard fails the cell fails and prints no metrics for that dataset.
- `mcd_sandbox.yaml`: the run command ends with `procs=auto` (`diff` against Deviation 2's spec: nothing else). Knobs, defaults, candidates, `max`, targets, build, metrics, `allowed_paths` and timeout 3600 are identical; `mcd.yaml` is unchanged.
- New base checkpoint **`76b71887-d3e7-48ff-96d5-f16cefcf6779`**, tag **`gf/mcd/base-v2`**: the Deviation 2 checkpoint `75aeac20-...` (tag `gf/mcd/base-v1`) plus the new `run_cell.sh` uploaded (one operation). The script is not uploaded per run: the spec's `base` is this checkpoint, so `GF_MCD_SANDBOX_BASE` must be it (the launcher's default). Hashes: `harness/run_cell.sh` sha256 `16e4aec193769a2c67c5410b86adff8585eb624788077613bc2b0862679b5294` (was `28cdc6c8...`; the file is in the arms' inputs, so this change is stated here rather than hidden), `mcd_sandbox.yaml` `f68d5d29f0422e1ac0800c7137af72b5bcd24b9c5cbda08bb5f2829e2e1637f2`, `mcd.yaml` unchanged `148c480a...`.
- Why not sharding across several operations: a VM has 4 cores, so in-VM sharding is enough for nearly every cell and needs no change to the orchestrator or the search.

**Seeding note (a real difference from the sequential run).** `experiment.py` calls `np.random.seed(1)` once per process, and Keras and Theano draw their initial weights and dropout masks from it. Unsharded, split k continues the random stream where split k-1 stopped; sharded, every split starts the stream afresh. So the first split of each dataset is bit-identical to the unsharded run, and the other splits get different (equally valid) random numbers. This is noise of the same kind as the noise between repeats, which the search already measures with five naive repeats on different splits. It is not a change of any knob. Runs within one design are reproducible; sharded and unsharded runs of one configuration do not bit-match beyond the first split.

**Equivalence check (Sandboxes, same `RUN_TAG`, `dir=energy,yacht hidden=2 n_splits=3`, unsharded vs `procs=auto`).**
- epochx=2: the draw is the same (splits 3,1,6) and the first-split values are bit-identical in both datasets and all four per-split metrics (energy MC RMSE 2.0721809779080855, yacht 6.2904211149393374, the same for single-pass RMSE, ll and tau). Other splits differ (energy MC RMSE, second and third split: 1.7538 and 1.8278 sharded, 1.8787 and 1.9405 unsharded).
- epochx=50 (splits 7,12,15): first split again bit-identical in both datasets (energy MC RMSE 0.47595331717358513, yacht 2.1015872021586524). Remaining splits, energy MC RMSE sharded 0.5259, 0.4317 vs unsharded 0.4535, 0.4097; yacht 1.8339, 1.0109 vs 1.7611, 1.1923. Aggregates (sharded vs unsharded): energy RMSE 0.4779 vs 0.4464, yacht RMSE 1.6488 vs 1.6850; energy ll -1.1750 vs -1.1621, yacht ll -1.6297 vs -1.5206. The aggregate difference (energy 0.032, yacht 0.036) is within one standard deviation of the three per-split values (0.03 to 0.04 energy, 0.3 to 0.5 yacht), and smaller than the energy noise band of the naive repeats (0.057 at the default size).
- At the default size: the energy shard of split 4 run alone (`n_splits=1`) gave MC RMSE 0.44140804931327016, and the same split inside the full sharded cell gave exactly that value again, so concurrent shards do not interfere with one another.

**Timings on Sandboxes** (one VM each, `RUN_TAG` fixed, `GF_CACHE_ONLY=1`; all times real wall; the reported `cost`, about $0.01 per CPU-second, is diagnostic only):
- default cell, sharded (`dir=energy,yacht epochx=500 hidden=2 n_splits=3`, 6 shards, 4 at a time): **805 s** operation wall (13.4 min), against about 1,910 s unsharded; exit 0, all metrics parsed (energy RMSE 0.3645, yacht RMSE 1.0121). Longest shard (energy split) 666 s, yacht shards about 270 s each; total CPU 2,672 s, the same as unsharded (2,673 s), so sharding adds no work. The cell's wall is set by the three yacht shards queueing on the fourth core (3 x about 268 s = 804 s) while the three energy shards (654 to 666 s) run on the other three.
- longest shard of the default cell, run alone (energy, one split): **654 s** (reported cost $6.48).
- epochx=2000, longest shard run alone (energy, one split): **2,505 s** (41.8 min; 3.8 times the default shard; reported cost $24.99); with 26% headroom under 3,600 s for this shard.
- hidden=5, longest shard run alone (energy, one split, epochx=500): **1,438 s** (2.2 times).
- Total reported cost of all development tests in this deviation: about $90 (diagnostic).

**Estimates per hypothesis** (full cell, 2 datasets x 3 splits unless stated; cell wall is about 805 s times the cost factor f, because the cell is set by the yacht chain, and f is the shard-time ratio measured above or the local attempt-2 ratio where not measured; estimates are marked "est."):

| Cell | f | Longest shard | Cell wall | Under 3,600 s? |
|---|---|---|---|---|
| default (epochx 500, hidden 2, n_splits 3) | 1 | 654 s (measured) | 805 s (measured) | yes |
| epochx=1000 | about 2 (est.) | about 1,300 s | about 1,600 s (est.) | yes |
| hidden=4 | about 1.8 to 2 (est.; local ratio 1.8 to 2.2) | about 1,200 to 1,300 s | about 1,500 to 1,600 s (est.) | yes |
| hidden=5 | 2.2 (shard measured) | 1,438 s (measured) | about 1,800 s (est.) | yes |
| epochx=2000 | 3.8 (shard measured) | 2,505 s (measured) | about 3,050 to 3,150 s (est.: 3 yacht shards of about 1,010 s on one core) | yes, margin about 12% to 15% (not run as a full cell) |
| n_splits=6 | 1 | 654 s | about 1,400 s (est.: 6 x 891 CPU-s / 4 cores + tail) | yes |
| n_splits=10 | 1 | 654 s | about 2,300 to 2,600 s (est.) | yes |
| n_splits=14 | 1 | 654 s | about 3,300 s (est.) | marginal; the largest that fits |
| n_splits=20 | 1 | 654 s | about 4,500 s (est.: 17,800 CPU-s / 4 cores) | **no, will time out** |
| epochx=2000 with hidden=5, or epochx=2000 with n_splits above 3, or hidden=5 with n_splits above 6 | above 6 | 5,500 s and more | above 4,000 s | **no, will time out** |

The rule of thumb: a cell fits when (n_splits / 3) times f is at most about 4. Cells that still end as a timeout (exit 124, status `timed_out`) are `n_splits=20` and combined cells such as the search's combine round putting `epochx=2000` and `hidden=5` together. The information lost is now the narrow set above, instead of every cell above about 1.35 times the default. The only remedy would be sharding across several operations (not built; a VM's four cores are already used).

**Concurrency settings.** The Beta allows 50 simultaneous operations in the project. A branch run is one operation (its shards run inside that VM), and the orchestrator's `GF_MAX_CONCURRENCY` is per search process, so the arms' limits add. `scripts/run_mcd_sandbox_arms.sh` now takes the arms to run (default: no-README and all-flags-random; `all`, or any list of `normal`, `evidence-off`, `no-README`, `all-flags-random`) and gives each `floor(48 / arms)`: **24 each for two arms (48 operations at most), 12 each for four**; it refuses a total above 50. Its other environment is Deviation 2's: `GF_SANDBOX_GUARD_USD=20000`, `GF_SANDBOX_CPU_LIMIT_S=60000`, `GF_SPEND_TAG=ext-mcd-sandbox`, and `GF_MCD_SANDBOX_BASE=76b71887-d3e7-48ff-96d5-f16cefcf6779`. Same `--max-runs 40 --candidates-per-knob 2 --cap 0.5`, same ledgers, same seed 0.

**Expected wall time for arms 3 and 4 (two arms at once).** Calibration is five default cells in one wave, about 14 min. Each later round waits for its slowest cell: a round containing an `epochx=2000` cell takes about 52 min, a round of default-size or smaller cells 14 to 30 min. With about 35 branch runs in five rounds (screen, confirm, combine, bisect, verify), about 3 to 5 hours per arm, both arms in parallel (a local `normal` arm took about 14 hours). Cells that time out cost 60 min of wall.

**What is unchanged.** The hypothesis space, the knobs and their defaults, the candidate values, the targets (`targets_mcd.json`), the scoring rule, the search logic (screen, confirm, combine, bisect, verify), the prompts (hashes above), the models, `net/` and `experiment.py` (the artifact's algorithm code is untouched, still at commit `6eb4497` with `T = 100`), and the experiments' commands and settings are unchanged. What changed: `run_cell.sh` runs (dataset, split) pairs as parallel processes when `procs` is given, a new base checkpoint holds that script, `mcd_sandbox.yaml` passes `procs=auto`, and the launcher chooses arms. Per-split seeding differs as stated above. Tests: `tests/unit/test_mcd_shards.py` (the shard mode against a stub `python`, the spec diff, the launcher plan) and `tests/unit/test_mcd_harness.py` (unchanged, still passing).
