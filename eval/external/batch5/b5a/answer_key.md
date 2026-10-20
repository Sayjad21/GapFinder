# Answer key, blind case b5a (PRIVATE until the reveal)

## Paper
Topology Attack and Defense for Graph Neural Networks: An Optimization Perspective.
Kaidi Xu, Hongge Chen, Sijia Liu, Pin-Yu Chen, Tsui-Wei Weng, Mingyi Hong, Xue Lin. IJCAI 2019.
arXiv 1906.04214v3 (https://arxiv.org/abs/1906.04214v3).
Repo: https://github.com/KaidiXu/GCN_ADV_Train, commit 7ace67ad2a54804f6a138e52e78ea7fdab34d009
(2019-08-07, "Update README.md"), the last commit before "Update attack.py / fix a bug in attack.py"
(60f81650398d68a75e43f730055149c809f4a490, 2020-12-15).

## Claims (Cora; all numbers are misclassification rates in %, = 100 x (1 - test accuracy))
Table 3, column "epsilon in robust training = 0" (the natural model), CE-PGD attack:
- TARGET: 5% perturbed edges: 27.9 (test accuracy 0.721).
- Held-out (same natural model, other budgets): 10%: 32.7 (acc 0.673); 15%: 36.7 (acc 0.633);
  20%: 40.2 (acc 0.598).
- Held-out (same natural model, no attack): 0%: 18.1 (acc 0.819). Not affected by the cause.
Table 1 (fixed natural model, 5% perturbed edges), Cora column:
- Held-out: CE-PGD 28.0 +- 0.1; CW-PGD (attack.py --method=CW) 27.8 +- 0.4.
(Robust-model columns of Table 3 and Citeseer are not part of the scored experiment.)

## Documented cause (code, in exposed code but with an exact flag equivalent)
`attack.py` line 36 at the commit:

    total_edges = adj.data.shape[0]

`adj` is the symmetric scipy adjacency, so `adj.data.shape[0]` counts every undirected edge twice.
The attack budget is `eps = total_edges * FLAGS.perturb_ratio` and the perturbation matrix S is strictly
upper triangular (each flipped edge counted once), so the attack may flip 2 x perturb_ratio x |E| edges:
twice the paper's budget ("the maximum number of perturbed edges is set to be 5% of the total number of
existing edges"). The attack is too strong and test accuracy under attack falls below Table 3.
The fix (commit 60f8165): `total_edges = adj.data.shape[0]/2`. The printed "perturb ratio" and the
`pr <= FLAGS.perturb_ratio` filter use the same `total_edges`, so they are consistently off by 2.

Exact flag equivalent: running the buggy code with `--perturb_ratio` equal to HALF the paper's budget
(0.025 for the 5% claim, 0.05 for 10%, 0.075 for 15%, 0.1 for 20%) gives exactly the fixed code's attack.
Training (`train.py`) is not affected; the clean accuracy (18.1) is not affected.

## Sources
1. Issue https://github.com/KaidiXu/GCN_ADV_Train/issues/6 ("Reproducing Results from Table 3"),
   tpfeifle, 2020-12-15, ran `python train.py` then `python attack.py --model_dir=nat_cora
   --perturb_ratio=[perturb_ratio]` (TF 1.13.1). Test accuracies vs Table 3 column 1:
   0%: 0.820 vs 0.819; 5%: 0.684 vs 0.721; 10%: 0.611 vs 0.673; 15%: 0.540 vs 0.633;
   20%: 0.484 vs 0.598.
   Repository owner KaidiXu, 2020-12-15: "After I checked the code, it's a bug in attack.py, the total
   edges should be divided by 2 in attack.py. Our robust training code calls the PGD_attack.py which does
   not yield this problem. Now I fixed this bug".
   tpfeifle, same day: "With this fix the natural model performance under attack aligns quite well."
   His later table (fixed code), natural model ("0% defense"): 0%: 0.82, 5%: 0.743, 10%: 0.684,
   20%: 0.611. (Note the buggy 5% = fixed 10% = 0.684 and buggy 10% = fixed 20% = 0.611: the budget is
   doubled.)
   Owner, later in the thread: attack.py samples 20 times at the last step and keeps the strongest
   perturbed graph; the paper averages 5 different train/val/test splits; differences "may be caused by
   randomness". (The rest of the thread is about the robust models, not scored here.)
2. Commit 60f81650398d68a75e43f730055149c809f4a490 diff (attack.py only):
   `-total_edges = adj.data.shape[0]` / `+total_edges = adj.data.shape[0]/2`.
3. Paper v3 Sec. 6.2: budget = "5% of the total number of existing edges in the original graph",
   K = 20 random samples; Table 3 and Table 1 values as above.

## Equivalence set (max 3 labels, any one counts as the cause)
1. The attack budget in attack.py counts each undirected edge twice (`total_edges` /
   `adj.data.shape[0]` should be halved, or "eps / the budget is twice the paper's").
2. `--perturb_ratio` must be half the paper's nominal budget (0.025 for the 5% target), named as the
   fitted value for the target (and consistent on the held-outs).
3. "The perturbation-ratio accounting in attack.py (eps or the printed perturb ratio) is wrong by a
   factor of 2" stated as a code/evaluation finding.

## Pre-registered scoring rule
- correct: GapFinder names one of the three labels above (a fitted `perturb_ratio` in [0.02, 0.03] for
  the 5% target, or the edge double count / factor-2 budget in attack.py).
- partial: it names the attack budget (`perturb_ratio`, `eps`, `total_edges`) as the cause but with a
  factor clearly different from 2 (fitted perturb_ratio outside [0.02, 0.03] but below 0.05), or names
  it only on held-outs.
- diagnosed out of space: the cause is in code. Credited when GapFinder says no exposed setting other
  than the budget explains the gap and points at the attack budget computation in attack.py. A plain
  "no setting explains it" without pointing at the budget is a miss.
- confidently wrong: a confident label ("Explained" or "Paper-artifact inconsistency") naming a
  different setting (e.g. `steps`, `hidden1`, `epochs`, `learning_rate`, `dropout`, `weight_decay`,
  `early_stopping`, a seed, `method`, the split), or a confident "no gap / noise" verdict.

Sealed 2026-10-20 by the independent sealer.
