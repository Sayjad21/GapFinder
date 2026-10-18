# Answer key (SEALED) - blind case b3a

Sealed: 2026-10-18 by the sealer (independent model). Do not open before the reveal.

## Case
- Paper: "Variational Fair Clustering", Imtiaz Masud Ziko, Eric Granger, Jing Yuan, Ismail Ben Ayed. AAAI 2021.
- Version given to the runner: https://arxiv.org/abs/1906.08207v5 (PDF https://arxiv.org/pdf/1906.08207v5, the AAAI 2021 version).
- Repo: https://github.com/imtiazziko/Variational-Fair-Clustering
- Commit given to the runner: eb1bb2cf91bb0c54ed0104c807b6ed988203f241 (2021-03-01, "Variational Fair Clustering update"), the last commit before the reproducers contacted the authors. Later commits dc50c384 (2022-01-19, "update lambda") and 9cc6f5a2 (2022-01-22, "Fix issue with lipchitz L") came during the reproduction study; they do not touch the Synthetic K-means setting.

## Claims
Table 3 (Fair K-means, "Ours" column), arXiv v5:
- MAIN target: Synthetic, clustering objective 207.80.
- Held-out, same row and run: Synthetic fairness error 0.00, balance 1.00.
- Held-out, same table: Synthetic-unequal objective 159.75, fairness error 0.00, balance 0.33. Not affected by the documented cause (the code reproduces it at the paper's lambda=10 and at lambda=100; see the sealer's check).
- Further held-out (Table 2, Fair K-median, a different clustering objective): Synthetic 292.4, 0.00/1.00; Synthetic-unequal 174.81, 0.00/0.33. The reproducers say the K-median Synthetic row is only partly closed even after tuning (lambda 600: 314.98, 0.0/0.93), so it should not veto an answer.
The paper states lambda = 10 for both synthetic datasets (in the row labels of Tables 2 and 3) and "In all the experiments, we fixed L = 2".

## Documented cause (setting: a hyperparameter value stated wrongly in the paper)
The trade-off multiplier lambda (`--lmbda` in test_fair_clustering.py) that the paper states for the Synthetic dataset (lambda = 10) is not the value behind the reported Fair K-means Synthetic numbers. The original authors told the reproducers that some reported lambda values are incorrect. With lambda = 100 the code gives exactly the paper's numbers (207.80, fairness error 0.00, balance 1.00), with zero variance over seeds. With the stated lambda = 10 it gives objective 203.66 +- 2.55, fairness error 2.43 +- 1.47, balance 0.27 +- 0.44 (30 seeds): a partly unfair clustering in most seeds.

Not part of the cause: the Lipschitz constant L (hard-coded 2.0 in src/bound_update.py at this commit, the paper's value; the reproducers discuss L for Ncut and Census II, not for Synthetic K-means), bound_iterations (5000), K, data generation, seeds.

## Sources
- Eijkelboom, Fokkema, Lau, Verheijen, "[Re] Reproduction Study of Variational Fair Clustering", ReScience C 8(2) #14, 2022 (ML Reproducibility Challenge 2021). https://doi.org/10.5281/zenodo.6574653 ; review https://openreview.net/forum?id=rq8fRhMm20F
  - Sec. 3.4: "After failing to reproduce some reported results, it was established in communication with the OA that some reported lambda values are incorrect and therefore unknown. A manual search is executed to test 10 lambda values ranging from 100 to 1500 for the K-medians and K-means algorithms on the SB dataset."
  - Table 7 (Fair K-means, original vs reproduction): Synthetic 207.80 vs 203.66 (+-2.55); 0.00/1.00 vs 2.43(+-1.47)/0.27(+-0.44). Synthetic-unequal 159.75 vs 159.75 (+-0.00); 0.00/0.33 vs 0.00/0.33.
  - Table 2 (SB dataset, tuned lambda): K-means 207.8 (+-0.00), 0.0 (+-0.00) / 1.0 (+-0.00). Table 5: K-means Synthetic lambda "10 (100)", the value in parentheses being the tuned lambda.
  - Sec. 4.1: "The fairness error and balance for the SB dataset could only be reproduced after tuning lambda (Table 2)."
  - Sec. 5: "Another problem was that the OA used a different Lipschitz constant than was used in the code." (relevant to Ncut / Census II, not to this target).

## Sealer's private check (not for the runner)
Commit eb1bb2c, Python 3.8, scikit-learn 0.22.2.post1, numpy 1.24, numba; Windows laptop, `multiprocessing.Pool` replaced by an in-process serial map (Windows spawn breaks the shared-variable pool; numerics unchanged), pyflann stubbed (only used for Ncut on N > 50000).
`python test_fair_clustering.py -d Synthetic --cluster_option kmeans --lmbda-tune False --lmbda <lam> --seed <s>`, seeds 0-7, about 5 s per run:
- lambda 0: 207.80/1.00 balance in 2 of 8 seeds, else 195.86/0.00.
- lambda 10 (paper): 207.80/1.00 in 3 of 8 seeds (0, 1, 7); other seeds 201.86 or 203.50 with balance 0.01. Mean objective about 204.1.
- lambda 20: 4/8 match; 30: 6/8; 50: 6/8; 70: 8/8; 100: 8/8; 200: 8/8; 1000: 6/8 (two seeds collapse to 604.13, balance 0).
- Synthetic-unequal K-means: 159.75, fairness 0.0000, balance 0.33 in 6/6 seeds at both lambda 10 and 100.
- Synthetic K-median: lambda 10 -> about 288.1, fairness 0.123, balance 0.48; lambda 100 -> about 291.3, 0.009, 0.83 (paper 292.4, 0.00, 1.00).
So the gap shows only when several seeds are averaged (the reproducers used 30); a single lucky seed at lambda 10 matches the paper.

## Equivalence set (counted as correct), written before the runner starts
- E1: lambda (`--lmbda`) for Synthetic Fair K-means set to a value in [60, 1500] (the authors' tuned 100; the reproducers' searched range 100-1500; the sealer's sweep shows 70-200 matches on every seed).
- E2: the finding that the paper's stated lambda = 10 for Synthetic is wrong / inconsistent with the reported Synthetic numbers, with a much larger lambda (any value >= 60) fitting them (a Paper-artifact-inconsistency label on lambda counts).
- E3: lambda as the single named setting with direction "increase" and a fitted value in [60, 1500], even if other knobs are listed as having no effect.

## Pre-registered scoring rule
- correct: GapFinder's named setting matches the documented one, exactly or inside the equivalence set above (E1-E3);
- partial: lambda named as the cause but with a fitted value in (10, 60), which closes the gap only on some seeds; or lambda named together with other settings that are not part of the cause (a superset), with lambda's value inside [60, 1500];
- diagnosed out of space: not applicable as the main outcome (the cause is an exposed flag); if GapFinder says out of space and its code lead points at lambda / the paper's lambda table, score as partial;
- confidently wrong: a confident label (Explained / Paper-artifact inconsistency / Partially explained) on a setting that is not lambda: seed / initialisation alone, the Lipschitz constant L, bound_iterations, maxiter, K, standardisation, data generation;
- otherwise: missed (Unexplained / Inconclusive / Reproduced / Fits but unsupported on the wrong setting). A "Reproduced" verdict from a single favourable seed is a miss.
