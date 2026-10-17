# Answer key (SEALED) - blind case 2 (blind-2)

Sealed: 2026-10-16 by the sealer (independent model). Do not open before the reveal.

## Case
- Paper: "GraphMAE: Self-Supervised Masked Graph Autoencoders", Zhenyu Hou, Xiao Liu, Yukuo Cen, Yuxiao Dong, Hongxia Yang, Chunjie Wang, Jie Tang. KDD 2022.
- Version URL given to the runner: https://arxiv.org/abs/2205.10803v1 (PDF: https://arxiv.org/pdf/2205.10803v1)
- Repo: https://github.com/THUDM/GraphMAE
- Commit (state BEFORE the authors' fix): 1be594160bb7c1fde0d16ced6af1e88b53612e49 ("fix bug in GIN", 2022-10-21)
- Fix commit (do not show runner): fdea388026e00d84a706e06e3c1e772aae0e6fd7 ("update hyper-parameters", 2022-10-25)

## Targets
Table 2 (unsupervised graph classification, accuracy %, mean 10-fold CV accuracy +- std after 5 runs), GraphMAE row:
- MAIN target: COLLAB 80.32 +- 0.46
- Held-out claims (same experiment/row): IMDB-B 75.52 +- 0.66; IMDB-M 51.63 +- 0.52; PROTEINS 75.30 +- 0.39; MUTAG 88.19 +- 1.26; REDDIT-B 88.01 +- 0.19; NCI1 80.40 +- 0.30.
- Only COLLAB is affected by the documented cause (the config entries of the other datasets already had the documented values at this commit).

## Documented cause
Dataset COLLAB, graph classification (main_graph.py, configs.yml, run with --use_cfg):
1. `alpha_l` (power coefficient of the scaled-cosine-error "sce" loss, the paper's "scaling factor"): paper Table 8 (appendix) = 1 for COLLAB. The code default (graphmae/utils.py `--alpha_l`, default 2) was applied because configs.yml had no `alpha_l` entry for COLLAB. Documented value: alpha_l = 1 (code used 2).
2. (Secondary, documented only by the fix commit diff) configs.yml COLLAB entry had a mistyped key `pool: max` instead of `pooling: max`, so pooling silently fell back to the default `mean` instead of `max` (paper Table 8: pooling = max). Fix: `pooling: max`.
Decoy: paper Table 8 says hidden_size 512 for COLLAB but configs.yml has 256. The issue reporter tried 512 and saw no improvement (78.70), and the fix commit did not change it. Not part of the cause.

## Sources
- GitHub issue https://github.com/THUDM/GraphMAE/issues/16 "The inconsistent performance on COLLAB dataset" (opened 2022-10-25, closed 2022-11-01). Reporter: `sh scripts/run_graph.sh COLLAB 0`, 78.78+-0.46 vs paper 80.32+-0.46; hidden 512 gave 78.70+-0.32. Author THINK2TRY (2022-10-25): "The scaling coefficient `alpha_l` should be set to 1 in COLLAB, while it is 2 by default now." and "Sorry to miss this hyper-parameter in configs.yml. We have updated `configs.yml`." and "The appendix shows only several key hyper-parameters due to space limits."
- Fix commit https://github.com/THUDM/GraphMAE/commit/fdea388026e00d84a706e06e3c1e772aae0e6fd7 : in configs.yml, COLLAB: `-  pool: max` -> `+  pooling: max` and `+  alpha_l: 1` (the commit also adds alpha_l lines to other datasets that duplicate existing values).
- Paper Table 8 (arXiv v1): COLLAB scaling factor 1, pooling max, hidden size 512, 20 epochs, mask rate 0.75, batch 32.
Note: the paper itself lists the scaling factor in its appendix table (a normal hyperparameter table, no explanation of any gap).

## Sealer's private check (not for the runner)
Single seed 0, CPU, commit 1be5941, `python main_graph.py --device -1 --dataset COLLAB --encoder gin --decoder gin --seeds 0 --use_cfg [...]`, DGL 0.9.1, torch 1.13.1 CPU, numpy<2:
- defaults: 78.68 ; `--alpha_l 1`: 80.50 ; `--alpha_l 1 --pooling max`: 80.46. Paper 80.32. So alpha_l=1 alone closes the gap; pooling is not needed. About 20 min per COLLAB seed (about 55 s/epoch x 20 epochs plus the SVM evaluation) on a laptop CPU.
- IMDB-BINARY with its config, seed 0: 76.20 (no gap). About 4 min per seed.

## Equivalence set (counted as correct) - written before the runner starts
- E1: alpha_l = 1 (alone; this is the author-stated cause).
- E2: alpha_l = 1 together with pooling = max (the full content of the fix commit).
- E3: a description of the COLLAB configs.yml entry as incomplete: missing `alpha_l: 1` (default 2 used), optionally also noting the `pool`/`pooling` key typo.
Everything else is not in the set. In particular: naming only pooling=max is partial; naming hidden_size / num_hidden, mask_rate, lr, max_epoch, batch size, norm, or seeds as the cause is confidently wrong if the label is Explained / Paper-artifact inconsistency / Partially explained.
Note on the scoring rule: although alpha_l=1 alone is a strict subset of {alpha_l=1, pooling=max}, it is counted as correct because it is the cause stated by the authors in the issue (E1).

## Pre-registered scoring rule (verbatim)
- correct: GapFinder's named settings match the documented ones, exactly or inside the equivalence set of at most 3 configurations;
- partial: a strict subset of the documented settings;
- diagnosed out of space: when the documented cause is in code or data, GapFinder says out of space (suspected or likely), ideally with a code lead at the right place;
- confidently wrong: a confident label (Explained / Paper-artifact inconsistency / Partially explained) on a setting that is not part of the documented cause;
- otherwise: missed (Unexplained / Inconclusive / Fits but unsupported on the wrong setting).
