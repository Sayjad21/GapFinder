# Blind case b3a

- Paper: Variational Fair Clustering
- Authors: Imtiaz Masud Ziko, Eric Granger, Jing Yuan, Ismail Ben Ayed
- Venue/year: AAAI 2021
- Paper version URL: https://arxiv.org/abs/1906.08207v5 (PDF: https://arxiv.org/pdf/1906.08207v5)
- Repo: https://github.com/imtiazziko/Variational-Fair-Clustering
- Commit: eb1bb2cf91bb0c54ed0104c807b6ed988203f241

## Experiment and claims
Table 3 (Fair K-means, "Ours" column): clustering objective, and fairness error / balance.
- Main target: Synthetic, objective 207.80.
- Held-out (same row): Synthetic fairness error 0.00, balance 1.00.
- Held-out (same table): Synthetic-unequal objective 159.75, fairness error 0.00, balance 0.33.
- Further held-out (Table 2, Fair K-median, a different clustering objective): Synthetic 292.4, fairness error 0.00, balance 1.00; Synthetic-unequal 174.81, 0.00 / 0.33.

Entry point: `test_fair_clustering.py` (`-d Synthetic|Synthetic-unequal`, `--cluster_option kmeans|kmedian`). One run prints the fairness error, average balance and minimum balance, and the clustering energy. Note that the default command line runs a sweep and leaves the seed unset.
The paper reports one number per cell and gives no seed. Evaluate each configuration as the mean over seeds 0-9.

## Data
Both synthetic datasets (400 2-D points, two demographic groups) are generated in `src/dataset_load.py` with `sklearn.datasets.make_blobs(random_state=1)`. Nothing is downloaded.

## CPU feasibility (sealer's estimate)
- N = 400 and K = 2. The bound update and K-means steps are small dense numpy operations. One run took about 5 s on a laptop CPU. Ten seeds × the claims above is under 5 minutes.
- Memory: the code opens `multiprocessing.Pool(processes=20)` per run (fork on Linux). The workers share the parent's pages, so the estimate is well under 1 GB in total.
- Environment: Python 3.8 with scikit-learn 0.22.x, because `src/fair_clustering.py` imports `sklearn.cluster.k_means_`. Also needed are numba, numexpr, scipy and pandas. `pyflann3`, imported at module load by `src/utils.py`, comes as a source distribution only and may need the system FLANN library.

## Seal
- SHA-256 of the answer key: see `answer_key.sha256` next to this file.
- Date: 2026-10-18

Sealed by an independent model (the sealer). The answer key is held outside the repository until the reveal.
