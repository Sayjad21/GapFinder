# Answer key b5b (SEALED: do not show to the runner before the run is committed)

## Paper and claims

- Paper: "Structural Deep Clustering Network" (SDCN), Deyu Bo, Xiao Wang, Chuan Shi, Meiqi Zhu, Emiao Lu, Peng Cui. WWW 2020.
- arXiv 2002.01633v3 (the Table 2 numbers below are identical in v1 and v3; checked in the LaTeX source of both).
- Repo: https://github.com/bdy9527/SDCN, commit f97d142bc4ff86129ccaae180ad106b21c2277a8 (2020-12-02, "Update sdcn.py"). This is the HEAD the issue below was filed against (issue opened 2021-09-28; the only later commit, da6bb00 on 2021-10-11, edits README.md only).
- Entry point: `python sdcn.py --name acm` (README "Code" section). ACM data, graph and pretrained autoencoder ship in the repo.

Claims, Table 2 ("Clustering results on six datasets (mean±std)"), ACM block:

| column | ACC | NMI | ARI | F1 |
|---|---|---|---|---|
| SDCN (distribution Z) | **90.45±0.18** (main target) | 68.31±0.25 | 73.91±0.40 | 90.42±0.19 |
| SDCN_Q (distribution Q, same run) | 86.95±0.08 | 58.90±0.17 | 65.25±0.19 | 86.84±0.09 |

Paper protocol text (Sec. 4.2): "We run all methods 10 times and report the average results"; "We choose the soft assignments in distribution Z as the final clustering results" (Sec. 3).

## Documented cause (evaluation/reporting difference, not a flag)

The paper's SDCN numbers are best-epoch numbers: for each run, the maximum over the training epochs of the label-based metrics (the code evaluates against the ground-truth labels after every epoch), not the value at the end of training. `sdcn.py` at this commit trains for a hard-coded 200 epochs (`for epoch in range(200):`, line 138) and calls `eva(y, res2, str(epoch) + 'Z')` every epoch (lines 145-150, `res2 = pred.argmax(1)` is distribution Z). Read at the end of training (the `199Z` line), the run gives about ACC 88.7 / NMI 64.0 / ARI 69.6 / F1 88.6, i.e. a gap of about 1.8 ACC, 4.3 NMI, 4.3 ARI points against the paper (paper std 0.18-0.40). Taking the per-run maximum over the 200 epochs (the peak is usually at epoch 15-26) gives about 90.1 / 67.3 / 72.9 / 90.1, which closes most of the gap. No command-line flag (`--lr`, `--k`, `--n_z`, `--n_clusters`, `--pretrain_path`) controls this.

The held-out SDCN_Q column (distribution Q, printed by the same run as `199Q`) reproduces at the final epoch (Q is nearly constant over training), so the gap is specific to the Z line.

### Sources

1. GitHub issue https://github.com/bdy9527/SDCN/issues/23 "Results for citeseer and acm" by gayanku (not a maintainer), opened 2021-09-28. The opening post lists `python sdcn.py --name acm` epoch-199 numbers, e.g. run 1 `199Z :acc 0.8797 , nmi 0.6253 , ari 0.6792 , f1 0.8783` and run 2 `199Z :acc 0.8846 , nmi 0.6376 , ari 0.6915 , f1 0.8839`, and asks "Is there probably some missing config or setting in the paper or the code?". The same reporter closed it on 2021-11-01 with: "Pls ignore. Results are as published. (need to take max, not last epoch)."
2. Sealer's own check (CPU, torch 2.8, sklearn 1.5; about 30 s per run), mean of 5 runs at f97d142, distribution Z:
   - final epoch (199): ACC 88.66, NMI 63.96, ARI 69.56, F1 88.62
   - epoch 49: ACC 88.87, NMI 64.71, ARI 70.13, F1 88.83
   - per-run max over epochs: ACC 90.07, NMI 67.25, ARI 72.92, F1 90.09
   - distribution Q, final epoch: ACC 86.79, NMI 58.82, ARI 64.91, F1 86.70 (paper SDCN_Q 86.95 / 58.90 / 65.25 / 86.84)
   Also 4 runs at the paper-era commit 0e0af8e10e86c7fefafbbdb019a4afb5795e0d20 (before the 2020-12-02 change to the GCN/AE mixing in `forward`): final epoch Z 88.63 / 63.86 / 69.50 / 88.59; per-run max 89.66 / 66.38 / 72.01 / 89.62 (one of the four runs collapsed to about 87; the other three average about 90.4 / 67.9 / 73.8). So the final-epoch gap does not come from that code change.

### Known decoys (verified not to be the cause)

- The paper says graph datasets were trained for 50 epochs while the code runs 200. Reading the run at epoch 49 gives 88.87 / 64.71 / 70.13 / 88.83, still far from the paper: training length alone does not explain the gap.
- The 2020-12-02 change of the delivery operator (`h + tra1` to `(1-sigma)*h + sigma*tra1`, sigma = 0.5): the final-epoch gap is the same before and after it (see source 2).
- Learning rate, kNN `k`, `n_z`, the pretrained autoencoder file, KMeans `n_init`: the paper and the code agree on these for ACM (lr 1e-3, original graph, d-500-500-2000-10, n_init 20).

## Pre-registered scoring rule

- **Correct**: the tool attributes the gap to which training epoch the paper's number corresponds to: the paper reports the best epoch per run (maximum of the label-based metrics over training, i.e. epoch selection with the ground-truth labels), whereas the run read at its end gives lower Z numbers. Equivalence set (any one of these, at most 3): (a) "report the per-run maximum over epochs / best epoch by ACC (or by the reported metrics)"; (b) "stop training at the early peak (about epoch 10-30) chosen by the label-based metrics"; (c) "the paper's number is an oracle/label-selected checkpoint rather than the final one". Naming this together with a minor secondary factor still counts as correct.
- **Partial**: the cause is a single factor, so partial is given only if the tool says the number depends on which epoch is reported (epoch choice) but does not identify that the paper's value is the label-selected best epoch (for example, it only says "fewer epochs" without the selection, or proposes the paper's 50 epochs and also notes the early peak as a possibility without committing).
- **Diagnosed out of space**: the documented cause is in the evaluation/reporting, not in any flag. Credited if the tool concludes that no command-line or config setting explains the gap and points to the evaluation/reporting protocol (or says the paper's number cannot be obtained from the final-epoch output without a different selection rule).
- **Confidently wrong**: a confident label on a setting or code change that does not close the final-epoch gap, e.g. the 50-epoch schedule from the paper, `--lr`, `--k`, `--n_z`, the sigma / delivery-operator change, the pretrained autoencoder, KMeans initialisation, random seed alone, or library versions.
- **Not explained / inconclusive**: anything else, including "noise" without a mechanism (the gap is 4 NMI points against a paper std of 0.25; five sealer runs at this commit all fall 3.4-5.6 NMI points below at the final epoch).

Sealed 2026-10-20.
