# Blind case b5b

- Paper: Structural Deep Clustering Network
- Authors: Deyu Bo, Xiao Wang, Chuan Shi, Meiqi Zhu, Emiao Lu, Peng Cui
- Venue/year: WWW 2020
- Paper version URL: https://arxiv.org/abs/2002.01633v3 (PDF: https://arxiv.org/pdf/2002.01633v3). Use this version only.
- Repo: https://github.com/bdy9527/SDCN
- Commit: f97d142bc4ff86129ccaae180ad106b21c2277a8

## Experiment and claims
Table 2 (clustering results, mean±std), ACM dataset block:
- Main target: SDCN ACC 90.45.
- Held-out (same run): SDCN NMI 68.31, ARI 73.91, F1 90.42; SDCN_Q ACC 86.95, NMI 58.90, ARI 65.25, F1 86.84.
- Out of scope: the other five datasets of Table 2 (USPS, HHAR, Reuters, DBLP, Citeseer), which are separate runs (the HHAR, Reuters and Citeseer feature files are not in the repository); the ablation tables and the figures.

Entry point: `python sdcn.py --name acm` (README, "Code" section). One run trains SDCN on ACM starting from the pretrained autoencoder in `data/acm.pkl`.
Per the paper, each reported number is the mean over 10 runs; SDCN takes distribution Z as the final clustering result, and SDCN_Q is the variant that uses distribution Q. The program prints `acc`, `nmi`, `ari` and `f1` lines for distributions Q, Z and P; the Z lines correspond to the SDCN column and the Q lines to the SDCN_Q column.

## Data
- ACM paper network (3,025 nodes, 1,870 features, 3 classes), shipped in the repository: `data/acm.txt` (11 MB), `data/acm_label.txt`, `graph/acm_graph.txt`, and the pretrained autoencoder weights `data/acm.pkl` (18 MB).
- No download or login needed.

## CPU feasibility (sealer's estimate, not measured)
- Under 2 minutes per run on 4 vCPUs (a laptop CPU finished one run in about 30 s); 10 runs fit in about 10-15 minutes. Peak memory well under 1 GB (dense 3,025 x 1,870 features, d-500-500-2000-10 autoencoder plus GCN).
- Environment: `requirements.txt` pins torch 1.3.1, numpy 1.17.2, scipy 1.3.1, scikit-learn 0.22.1, pandas 0.25.1, h5py 2.9.0, munkres 1.0.12. The code also runs with current torch and scikit-learn (torch 2.x prints a deprecation warning for the sparse tensor constructor). It uses CUDA when available and falls back to the CPU.

## Seal
- SHA-256 of the answer key: see `answer_key.sha256` next to this file.
- Date: 2026-10-20
