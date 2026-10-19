# Answer key, blind case b4a (PRIVATE until the reveal)

## Paper
RippleNet: Propagating User Preferences on the Knowledge Graph for Recommender Systems.
Hongwei Wang, Fuzheng Zhang, Jialin Wang, Miao Zhao, Wenjie Li, Xing Xie, Minyi Guo. CIKM 2018.
arXiv 1803.03467v4 (https://arxiv.org/abs/1803.03467v4).
Repo: https://github.com/hwwang55/RippleNet, commit 05459f1e6a47080375a0556aa70b6a286fa5b636 (2018-09-12),
the last commit before "update default settings" (ba7ce72f12b1, 2018-10-29).

## Claims (Table 3, CTR prediction, RippleNet row)
- TARGET: Book-Crossing AUC 0.729.
- Held-out (same run): Book-Crossing ACC 0.662.
- (MovieLens-1M 0.921 / 0.844 and Bing-News 0.678 / 0.632 are other datasets with their own
  per-dataset hyperparameters in Table 2; not part of the scored experiment.)

## Documented cause
The README run command for this experiment (`python preprocess.py --dataset book`, then
`python main.py --dataset book`) trains Book-Crossing with the argparse defaults of src/main.py, which are
the MovieLens-1M settings. The Book-Crossing settings exist only inside a commented-out string block in
src/main.py ("# default settings for Book-Crossing") and in the paper's Table 2.

Settings, default (as run) -> needed for Book-Crossing:
- `--lr` 0.02 -> 1e-3   (paper Table 2: eta = 0.001)
- `--l2_weight` 1e-7 -> 1e-5   (paper Table 2: lambda1 = 1e-5)
- `--n_hop` 2 -> 3 (commented block and Table 2 say H = 3; the paper's Sec. 4.3 text says H = 2 for
  Book-Crossing, and Table 5 shows H = 2 vs 3 differ by under 0.01 AUC). This one is NOT required.
- Unchanged at this commit: dim 4, kge_weight 0.01, batch_size 1024, n_epoch 10, n_memory 32.

## Sources
1. Issue https://github.com/hwwang55/RippleNet/issues/4 ("Can't get the paper results for
   Book-crossing dataset"). Repository owner hwwang55, 2018-10-11: "did you use the default setting for
   book-crossing (see main.py)? You cannot just run "python main.py --dataset book". The default setting
   is for movielens." Owner's own run with book settings: best test AUC 0.7223, ACC 0.6618. Owner (same
   thread): the earlier arXiv table (0.840 / 0.775) was superseded; the correct result is in the latest
   arXiv version (v4: 0.729 / 0.662).
2. src/main.py at the commit: the active defaults (dim 4, n_hop 2, kge 0.01, l2 1e-7, lr 0.02) and the
   commented "default settings for Book-Crossing" block (dim 4, n_hop 3, kge 1e-2, l2 1e-5, lr 1e-3).
3. Paper v4 Table 2: "Book-Crossing d = 4, H = 3, lambda1 = 10^-5, lambda2 = 0.01, eta = 0.001";
   "MovieLens-1M d = 16, H = 2, lambda1 = 10^-7, lambda2 = 0.01, eta = 0.02".

## Sealer's verification run (CPU, TF 2.15 tf.compat.v1, xavier -> glorot_uniform, one run each,
final epoch 9 / best-eval epoch)
- Defaults (`--dataset book`): test AUC 0.659, ACC 0.626 at the final epoch (peak AUC 0.712 at epoch 0,
  then overfits: train AUC 0.998).
- `--lr 1e-3 --l2_weight 1e-5 --n_hop 2`: final test AUC 0.703, ACC 0.654; at the best eval epoch (4)
  test AUC 0.721, ACC 0.649.
- `--lr 1e-3 --l2_weight 1e-5 --n_hop 3`: this run stayed near AUC 0.5 for 7 epochs, then reached 0.688 /
  0.625 at epoch 9 (the "stuck" behaviour the thread reports; seed dependent).
Each run takes about 1-2 minutes on a laptop CPU.

## Equivalence set (max 3 settings)
{ lr in [5e-4, 2e-3],  l2_weight in [1e-6, 1e-4],  n_hop in {2, 3} (free) }.
Also accepted as the same label: "use the commented Book-Crossing settings in src/main.py" or "use
Table 2's Book-Crossing hyperparameters" when the named values include lr and l2_weight as above.

## Pre-registered scoring rule
- correct: the named setting(s) include BOTH lr (in [5e-4, 2e-3]) AND l2_weight (in [1e-6, 1e-4]);
  n_hop may be 2 or 3 or unnamed; no other changed knob is required for the claim.
- partial: a strict subset, i.e. only lr in range, or only l2_weight in range (with or without n_hop).
- diagnosed out of space: not applicable (the cause is in exposed flags); a "the README command uses
  the wrong dataset's hyperparameters" diagnosis with no values counts as partial.
- confidently wrong: a confident label whose named settings include neither lr nor l2_weight in range
  (e.g. only dim, n_epoch, batch_size, kge_weight, n_memory, n_hop, item_update_mode or a seed), or a
  confident "no gap / noise" verdict.

Sealed 2026-10-19 by the independent sealer.
