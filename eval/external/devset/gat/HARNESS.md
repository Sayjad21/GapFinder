# Devset case: GAT (Velickovic et al., ICLR 2018), harness

- **Paper:** "Graph Attention Networks", ICLR 2018, arXiv 1710.10903v3.
- **Repo:** https://github.com/PetarV-/GAT at `5af87e7fce2b90ae1cbd621cd58059036a3c7436`.
- **Target:** Table 2 (transductive), GAT on PubMed, **79.0** (paper: 79.0 ± 0.3%, mean of 100 runs).
- **Held-out:** GAT on Cora (**83.0**) and Citeseer (**72.5**), same table. Both are marked
  `tuned_separately` (see below).

## Image (`case.json`, `../build_case.py`)

- `python:3.7-slim`, with `tensorflow==1.15.5`, `numpy==1.18.5`, `scipy==1.4.1`, `networkx==2.4` and
  `protobuf==3.20.3`.
- The repo is fetched inside the sandbox at the commit. No repository file is changed.
- **Data:** the repo ships only Cora. At build time, the `ind.citeseer.*` and `ind.pubmed.*` files (x, y, tx,
  ty, allx, ally, graph, test.index) are downloaded into `data/` from tkipf/gcn at
  `39a4089fe72ad9f055ed6fdb9746abdcfebc4d81` (`gcn/data/`).
- The harness (`harness/`) is uploaded as `/work/gf_harness/`.

## Script and scope

- The harness uses the **sparse** script, `execute_cora_sparse.py` (model `SpGAT`).
  - The dense `execute_cora.py` would need a 19717 x 19717 adjacency for PubMed (3.1 GB in float64, built
    by a Python double loop), which doesn't fit a 3.9 GB VM.
- **One cell** runs that script, as shipped, once on each of cora, citeseer and pubmed. The three run in
  parallel, each from its own copy of the script (`harness/run_cell.sh`).
- **Measured in the two smoke runs** (naive configuration, run in parallel; checkpoint
  `3f93d0a9-644f-4d74-9d14-a62d484d4f10`):

  | Dataset | Epochs | Wall time | Peak RSS | Test acc. | Paper |
  |---|---|---|---|---|---|
  | cora | 889 / 751 | 436 / 385 s | 0.86 / 0.82 GB | 82.5 / 82.7 | 83.0 |
  | citeseer | 659 / 684 | 671 / 756 s | 1.31 / 1.35 GB | 73.6 / 72.9 | 72.5 |
  | pubmed | 489 / 663 | 587 / 758 s | 1.28 / 1.23 GB | 78.1 / 76.6 | 79.0 |

  - A cell takes 675 to 765 s.
  - PubMed is fast enough per run, so the scope is the full Table 2 GAT row. Nothing is scaled down, and
    `discrepancy` is left unset.
  - The three processes peak at about 3.4 GB together, which is close to the VM's 3.9 GB. A setting that
    makes the model much bigger could run out of memory.
- **Metrics:** `gat_<dataset>_acc`, the script's final "Test accuracy" (after it restores the
  early-stopping checkpoint), in percent.

## Knobs, and how the constants are set

- The script has no command-line flags. Its settings are module-level constants.
- **Knobs:** every module-level constant assignment of the script, with the script's own value:

  | Knob | Default |
  |---|---|
  | `batch_size` | 1 |
  | `nb_epochs` | 100000 |
  | `patience` | 100 |
  | `lr` | 0.005 |
  | `l2_coef` | 0.0005 |
  | `hid_units` | 8 |
  | `n_heads` | 8,1 |
  | `residual` | False |
  | `nonlinearity` | tf.nn.elu |
  | `model` | SpGAT |
  | `sparse` | True |

  Two constants are not knobs:
  - `dataset` is set per metric.
  - `checkpt_file` is an output path (see Deviations).
- **How a run sets them:** `harness/set_constants.py` reads the shipped script with `ast`. For each
  `NAME=VALUE`, it checks that `NAME` is a single module-level assignment, and replaces that statement with
  `NAME = VALUE`. Nothing else in the file changes. The result is written to `out/<dataset>/execute.py` and
  run from `/work` (`PYTHONPATH=/work`).
  - A list constant takes comma-separated items: `n_heads=8,8` becomes `[8, 8]`. Knob values may not contain
    brackets or spaces.
  - Any other value is used as a Python expression, for example `tf.nn.relu`, `GAT` or `True`.
- **Settings that are not knobs:** the dropout rates are not module-level constants. They are literals in
  the `feed_dict` (`attn_drop: 0.6, ffd_drop: 0.6`), so they stay as shipped.
- **Settings that don't run:**
  - `model=GAT` with `sparse=True`, or `model=SpGAT` with `sparse=False`, does not run: the model and the
    input format must agree.
  - `batch_size` other than 1 does not run either. The README says: "working only when the batch size is
    equal to 1".
  - These knobs are kept anyway, because every constant is exposed mechanically.
- **Limit:** `patience` max is 1000, to keep a cell under the 3300 s run timeout.

## Seeds and noise

- The code sets no seed: no `tf.set_random_seed`, and NumPy draws no random numbers. Glorot initialisation
  and dropout differ on every run, so repeats differ naturally, as the paper's 100 runs do.
- The harness sets no seed either. Each run's `RUN_TAG` is a different sandbox run, so its draws are
  independent.
- The smoke runs smoke-a and smoke-b gave different numbers (the table above; `build.log`).

## Held-out claims: tuned separately (from the paper's text)

Section 3.3, "Experimental setup", Transductive learning:

> "Its architectural hyperparameters have been optimized on the Cora dataset and are then reused for
> Citeseer. [...] Similarly as observed by Monti et al. (2016), we found that Pubmed's training set size
> (60 examples) required slight changes to the GAT architecture: we have applied K = 8 output attention
> heads (instead of one), and strengthened the L2 regularization to λ = 0.001. Otherwise, the architecture
> matches the one used for Cora and Citeseer."

> "[...] using the Adam SGD optimizer [...] with an initial learning rate of 0.01 for Pubmed, and 0.005 for
> all other datasets."

- Cora and Citeseer share one setting, and PubMed (the target) has its own.
- So one shared setting is not expected to fit the target and the held-out rows at once. Both held-out
  claims are `"tuned_separately": true`.

## Deviations from the script as shipped

- **`checkpt_file`:** set to `out/<dataset>/mod.ckpt` instead of `pre_trained/cora/mod_cora.ckpt`.
  - The script saves its early-stopping checkpoint there, and restores it before testing.
  - With the shipped path, the three parallel runs would overwrite one file, and the shipped pre-trained
    model would be overwritten too.
- **`dataset`:** set per run (the shipped value is `'cora'`).
- **Inline comments:** the inline comments on rewritten lines are dropped.
- Nothing else changes.

## Budget

- `--max-runs 150` at `--concurrency 8`: about 19 waves of about 12 min, so roughly 4 hours with slower
  settings included.
- `GF_SPEND_CAP_USD=33` is set on the ledger and search processes. Sandboxes are unbilled.
