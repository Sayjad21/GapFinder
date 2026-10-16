# blind-2 harness: how GraphMAE is run, and every deviation

Written by the runner after GapFinder was frozen at `v1.4` = `blind-2` (`e0568b6`), and after the sealer
committed `case.md` and the answer-key hash (`66a5056`). Written before the search and before the reveal.
The runner has not seen the answer key and has read no reproduction report about GraphMAE.

## Roles

- **Sealer:** a separate model (Claude Sonnet, a subagent with its own context).
  - It was told to send back only the paper, repo and commit, targets, the hash and neutral setup facts:
    versions, how to get the data, the run command and the run time.
  - It was not to send measurements or remarks about the code (the caveat of blind-1). Its hand-back
    followed that.
- **Runner:** the GapFinder builder (Claude Opus, this session).
- **Caveat:** both are AI models directed by the same user.

## Disclosure: something the runner noticed before the run

While reading `configs.yml` to write this harness, the runner saw that the `COLLAB` (and `NCI1`) entries
use the key `pool:`, while the code reads `args.pooling`. So that entry has no effect, and COLLAB runs with
`pooling=mean`.
- The runner doesn't know whether this matters.
- It did not shape the harness: knobs are every argparse flag, chosen mechanically (`pooling` is one of
  31), with defaults printed by the code itself.
- It is recorded here so the reveal can be judged with that knowledge in view.

## Where the runs happen: local Docker, not Sandboxes

COLLAB, the target, can't load on a Sandboxes VM:
- loading the dataset (dense graphs, 401-dimensional degree features) reached 3.9 GB RSS and was killed by
  the kernel's OOM killer;
- the VM has 3.9 GB of RAM and refuses `swapon`;
- the SDK has no memory setting.

So the search runs in local Docker on the runner's machine (16 logical CPUs; Docker has 16.7 GB). The image
is `docker/Dockerfile`, with the same pins as the Sandboxes image built first (`build.py`, checkpoint
`712565da-...`):
- python 3.10;
- torch 1.13.1+cpu, dgl 0.9.1 (the code uses `dgl.function.copy_src`, removed in dgl 1.x), numpy < 2,
  scipy < 1.12, scikit-learn < 1.4, pyyaml 6.0.1, tqdm, tensorboardX, ogb;
- the repo at `1be5941`, fetched from GitHub;
- the Table 2 datasets fetched at build time (DGL `TUDataset`).

**No repository file is changed by the build.**

## The naive run and the cell

**Naive run:** the README's command, `scripts/run_graph.sh <dataset>`. That is its flags plus `--use_cfg`,
which applies `configs.yml[<dataset>]` over them.
- One seed per run: `--seeds <crc32(RUN_TAG) % 100000>`. The script's five seeds become five repeats.
- Each run is one 10-fold SVM evaluation, as in `main_graph.py`.

**One cell runs, in parallel:**
- COLLAB (6 threads), the target;
- IMDB-BINARY, IMDB-MULTI and MUTAG (1 thread each), as held-out claims.

`gf_harness/emit.sh` prints each `final_acc` in percent.

**Scope, decided on run time only before the search** (timings from `build.py` in Sandboxes, one run per
dataset, and one local Docker cell):
- **REDDIT-B and NCI1 are left out:** each ran past 3600 s alone.
- **PROTEINS is left out:** it was the slowest part of the local cell (1945 s with 1 thread, against
  1554 s for COLLAB with 4).
- A cell takes about 26-32 minutes and 5.5 GB, so two run at a time.

## Knobs

**Knobs** are every argparse flag in `graphmae/utils.py:build_args`, except the ones that say how to run:
`seeds`, `dataset`, `device`, `use_cfg`, `logging`, `load_model`, `save_model`. That leaves 31 knobs.
- **Defaults** are COLLAB's effective values under the README command, printed by
  `gf_harness/apply_knobs.py --print-defaults` (the repo's own `build_args()` and `load_best_configs()`).
- `pool` is set by `configs.yml` but is not a flag, so it is not a knob.

**How a knob is applied:**
- `--use_cfg` overwrites any flag the dataset's config names, so a changed knob is written into the
  branch's own `configs.yml` for every dataset of the cell.
- A knob at the default is left alone, so each held-out dataset keeps its own configuration.
- `configs.yml` is a configuration file (`allowed_paths`), not algorithm code.

**Cost caps, fixed before any search run:** `max_epoch` ≤ 60, `num_hidden` ≤ 1024, `num_layers` ≤ 5.
COLLAB pre-training time grows with each.

## Targets and held-out claims

- **Main target:** COLLAB 80.32 (Table 2).
- **Held-out:** IMDB-B 75.52, IMDB-M 51.63 and MUTAG 88.19, all `"tuned_separately": true`.
- **Why `tuned_separately`, from the paper's text only:**
  - "The hyper-parameters and statistics of datasets are in Table 8".
  - "The scaling factor γ is a hyper-parameter adjustable over different datasets".
  - So each dataset was tuned on its own (the repo's per-dataset `configs.yml` agrees). A shared setting
    isn't expected to fit them: they are reported, not vetoes.

## Search

`gapfinder search` at `v1.4`, local Docker backend:
- `--max-runs 60` and `--concurrency 2`, stated here before the run (about 13 hours);
- defaults otherwise.

The run is committed unchanged before the reveal.
