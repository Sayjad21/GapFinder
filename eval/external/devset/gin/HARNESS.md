# GIN (Xu, Hu, Leskovec, Jegelka, ICLR 2019): harness

Devset batch devbatch-1. Paper: arXiv 1810.00826v3. Code: weihua916/powerful-gnns at `9a2ce8a`.

## Target and held-out claims

- **Target:** Table 1, SUM-MLP (GIN-0) on IMDB-BINARY, **75.1** ± 5.1 (ledger claim C69).
- **Held-out** (same GIN-0 row, checked against the rendered Table 1): IMDB-MULTI 52.3 (C70), PTC 64.6 (C76),
  MUTAG 89.4 (C74).
- **All three held-out claims are `tuned_separately: true`.** The paper tunes every dataset on its own (p. 9):
  > "The hyper-parameters we tune for each dataset are: (1) the number of hidden units ∈ {16, 32} for
  > bioinformatics graphs and 64 for social graphs; (2) the batch size ∈ {32, 128}; (3) the dropout ratio
  > ∈ {0, 0.5} after the dense layer (Srivastava et al., 2014); (4) the number of epochs, i.e., a single epoch
  > with the best cross-validation accuracy averaged over the 10 folds was selected."

  The readout differs by dataset family as well: "specifically, sum readout on bioinformatics datasets and
  mean readout on social datasets due to better test performance." So no single shared setting is
  expected to fit IMDB-B and the others, IMDB-MULTI included.
- **Left out:**
  - COLLAB and REDDIT-BINARY (and REDDIT-MULTI5K): too large for a Sandboxes VM (instruction);
  - PROTEINS (76.2) and NCI1 (82.7): cost (see "Scope").

## Image (`case.json`, `../build_case.py`)

- `python:3.10-slim`, with torch 2.1.2+cpu, numpy 1.26.4, scipy 1.11.4, scikit-learn 1.3.2, networkx 3.2.1
  and tqdm 4.66.1.
- The repo is fetched at the commit. Setup: `python -m zipfile -e dataset.zip .`, as the README's
  `unzip dataset.zip`, because the slim image has no `unzip`. Then the unused `__MACOSX`, COLLAB and REDDIT
  folders are removed. No repository file is changed.
- `requirements.txt` lists only tqdm, numpy and networkx. torch and scikit-learn (`util.py` imports
  `StratifiedKFold`) are added.

## What one run is

- A paper number is a 10-fold cross-validation mean. **One run = the full 10-fold cross-validation on each
  dataset.**
  - That is 40 `python main.py --dataset D --fold_idx k` processes (4 datasets x 10 folds), 4 at a time
    (`harness/run.sh`, one thread each, 4 vCPUs).
  - Each process trains for `--epochs` epochs and prints "accuracy train: x test: y" after every epoch.
- **Scoring** (`harness/emit.sh`) follows the README's own description of the paper's protocol: "after
  obtaining 10 validation curves corresponding to 10 folds, we first took average of validation curves across
  the 10 folds (thus, we obtain an averaged validation curve), and then selected a single epoch that achieved
  the maximum averaged validation accuracy."
  - The metric is the maximum over epochs of the fold-averaged test-fold accuracy, in percent: `imdbb_acc`,
    `imdbm_acc`, `ptc_acc`, `mutag_acc`.
  - A dataset with a missing or short fold prints no metric.
- **Naive run:** what the README says.
  - `python main.py` with the default flags.
  - `--degree_as_tag` on the IMDB datasets ("for the COLLAB and IMDB datasets, you need to add
    `--degree_as_tag`").
  - All 10 folds, 350 epochs: full scale, so `discrepancy` is left unset.
- **Cost:** a default run takes about 17 min and peaks at about 0.34 GB (see "Smoke"; 0.44 GB in the batch-128 timing test). The timing tests in
  Sandboxes (10 folds, 4 at a time) took the following per 20 epochs:

  | Dataset | Batch 32 | Batch 128 |
  |---|---|---|
  | NCI1 | 35 s | 138 s (with PROTEINS) |
  | PROTEINS | 29 s | (with NCI1) |
  | IMDB-B | 20 s | 146 s (all four small) |
  | IMDB-M | 17 s | |
  | PTC | 18 s | |
  | MUTAG | 13 s | |

## Scope: why PROTEINS and NCI1 are left out

- With all six datasets, a default run takes about 40 min.
- A run at `batch_size=128` (a value in the paper's own grid) takes about 85 min, over the 3600 s limit.
- With the four smaller datasets, a default run takes about 17 min, and a batch-128 run about 45 min.

## Knobs (`gin.yaml`)

Every argparse flag of `main.py`, with the code's default:

| Knob | Default |
|---|---|
| `batch_size` | 32 |
| `iters_per_epoch` | 50 |
| `epochs` | 350 |
| `lr` | 0.01 |
| `num_layers` | 5 |
| `num_mlp_layers` | 2 |
| `hidden_dim` | 64 |
| `final_dropout` | 0.5 |
| `graph_pooling_type` | sum (choices: sum, average) |

The `max` values only bound the cost, so that a run finishes in under 3600 s: `batch_size` 128,
`iters_per_epoch` 100, `epochs` 700, `num_layers` 8, `num_mlp_layers` 4, `hidden_dim` 256.

Left out, and why:

- **How-to-run flags:**
  - `--device`: the VM has no GPU, so the code uses the CPU.
  - `--filename`: an output file.
  - `--seed`: the seed of the 10-fold split (`StratifiedKFold(random_state=seed)`). Each run derives it from
    RUN_TAG: `S=$(( $(printf %s "$RUN_TAG" | cksum | cut -d" " -f1) % 100000 ))`, so repeats differ. The
    code fixes `torch.manual_seed(0)` and `np.random.seed(0)` itself, so the fold split is the only source of
    run-to-run noise. The paper doesn't give its split seed.
- **Flags that say which claim a metric belongs to:**
  - `--dataset`.
  - `--fold_idx`: the harness runs all 10 folds; that is the cross-validation.
  - `--neighbor_pooling_type sum` and no `--learn_eps`: these make the row SUM-MLP (GIN-0), with ε fixed at 0.
    Other values are other rows of Table 1 (MEAN-MLP, MAX-MLP, GIN-ε), as `vgae`'s spec fixes the model.
  - `--degree_as_tag`: on for IMDB-B and IMDB-M, as the README says, and off for PTC and MUTAG. It decides
    the input features per dataset family, as in the paper: "in the bioinformatic graphs, the nodes have
    categorical input features ... for the other social graphs, we use one-hot encodings of node degrees."
    One shared value can't hold both families.
- `num_mlp_layers=1` would also be another row (SUM-1-LAYER). It stays a knob because every other value is
  still SUM-MLP and it is an ordinary training flag.

## Deviations, and why

1. **torch 2.1.2 (CPU) instead of 0.4.1/1.0.0.** The old wheels don't install on a current Python. The code
   runs unchanged:
   - `torch.sparse.FloatTensor` and `torch.spmm` still work;
   - `scheduler.step()` before training only warns, and StepLR halves the learning rate at the same epochs
     (50, 100, ...) as in torch 0.4.
2. **CPU instead of GPU.** Sandboxes VMs have no GPU. Results should not depend on the device beyond float
   noise.
3. **scikit-learn 1.3.2.** `StratifiedKFold(shuffle=True)` has drawn different splits since 0.22. The fold
   assignment for a given seed differs from 2019, but every run draws its own split seed anyway. The
   `dataset/*/10fold_idx` files in the zip are not read by the code, so they are not used.
4. **Logs:** tqdm's progress bar is turned off (`TQDM_DISABLE=1`) and Python warnings are silenced, to keep
   the logs small. Nothing else changes.
5. **Scope:** PROTEINS and NCI1 are left out for cost, as above. Nothing is scaled down.

## Smoke (two default runs, `build_case.py`)

- Checkpoint: `456ea388-a435-4471-9340-90806fdc261f`.
- **smoke-a:** 1034 s, max_rss 339 MB (0.34 GB of 3.9 GB). Folds took 80-120 s each.

  | Metric | Measured | Paper | Best epoch |
  |---|---|---|---|
  | imdbb_acc | 73.50 | 75.1 | 15 |
  | imdbm_acc | 50.60 | 52.3 | 85 |
  | mutag_acc | 89.36 | 89.4 | 80 |
  | ptc_acc | 62.50 | 64.6 | 274 |

- **smoke-b:** 1047 s, max_rss 338 MB. imdbb_acc 74.50 (best epoch 145), imdbm_acc 50.33 (170), mutag_acc
  86.67 (40), ptc_acc 60.75 (44).

- Search budget: a default run takes about 17 min; a batch-128 or 700-epoch run takes 35-45 min. At
  `--concurrency 8`, 4 h is about 1900 run-minutes, so `--max-runs 80`.
