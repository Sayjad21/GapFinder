# batch-3 b3a harness: Variational Fair Clustering (Ziko et al., AAAI 2021)

Written by the runner, who has not seen the answer key. Inputs: `case.md`, the paper and the repo. No repository
file is changed.

## Image: hand-built (the automatic build failed)

Stage 1 (`env_build.json`, frozen code at tag `batch-3`, README goal `sh evaluate_Fair_clustering.sh`) failed after
15 commands. It kept installing the repo's `requirements.txt`, whose `matplotlib==3.0` has no wheel and doesn't
build on those images, and it switched from python:3.9 to 3.6, which made it worse. Model cost $0.033.

Hand-built instead (`case.json`):
- python:3.8-slim (case.md: the code imports `sklearn.cluster.k_means_`, which needs scikit-learn 0.22);
- numpy 1.19.5, scipy 1.5.4, scikit-learn 0.22.2.post1, numba 0.53.1, numexpr 2.7.3, pandas 1.1.5,
  matplotlib 3.3.4, requests, pyflann3;
- `libflann-dev` from apt.

Checkpoint `507a8c7f-af37-4a64-ac24-1f373177be7d`.

## Claims (case.md: Table 3 Fair K-means and Table 2 Fair K-median, "Ours")

| Claim | Metric | Paper | Role |
|---|---|---|---|
| C_km_syn_obj | kmeans_synthetic_objective | 207.80 | target |
| C_km_syn_bal | kmeans_synthetic_balance | 1.00 | held-out |
| C_km_uneq_obj / C_km_uneq_bal | kmeans_unequal_objective / _balance | 159.75 / 0.33 | held-out |
| C_kmd_syn_obj / C_kmd_syn_bal | kmedian_synthetic_objective / _balance | 292.4 / 1.00 | held-out |
| C_kmd_uneq_obj / C_kmd_uneq_bal | kmedian_unequal_objective / _balance | 174.81 / 0.33 | held-out |

- "Balance" is the minimum over clusters. The paper says: "define the overall balance of the clustering as
  balance = min_Sk balance(Sk)".
- The fairness error claims are 0.00, which a relative gap can't use. They are printed as metrics, not claims.
- The tables give λ per dataset row (e.g. "Synthetic (N = 400, J = 2, λ = 10)"). So each (option, dataset) has its
  own λ knob, and no held-out claim is marked tuned separately.

## What a run is

One cell = Fair K-means and Fair K-median on Synthetic and Synthetic-unequal, each over seeds 0-9.
- case.md says a paper cell is the mean over seeds 0-9.
- Four processes at a time.
- Each (config, seed) gets a fresh `--data_dir`, because the script caches its initial centres there.
- `emit.sh` reports, per configuration, the mean over seeds of what the script prints last: the clustering
  energy, the fairness error, the min balance and the average balance.

## Knobs

Every argparse flag of `test_fair_clustering.py` that defines the experiment:
- `--lmbda`, one knob per (option, dataset), at the README script's active value 10;
- `--lmbda-tune`, at the script's False.

Left out:
- `--seed`: the protocol's 0-9;
- `-d` and `--cluster_option`: they define the claim;
- `--data_dir` and `--output_path`: paths;
- the four `--plot_option_*`: plots only.

## Smoke (naive cell)

24 s, 0.2 GB peak.

| Metric | Measured | Paper |
|---|---|---|
| K-means Synthetic objective | 205.00 | 207.80 |
| K-means Synthetic balance | 0.505 | 1.00 |
| K-means Synthetic fairness error | 1.651 | 0.00 |
| K-means Synthetic-unequal | 159.754 / 0.33 | 159.75 / 0.33 |
| K-median Synthetic | 288.54 / 0.437 | 292.4 / 1.00 |
| K-median Synthetic-unequal | 174.82 / 0.33 | 174.81 / 0.33 |
