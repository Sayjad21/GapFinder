# Blind case b5c

- Paper: BOND: Benchmarking Unsupervised Outlier Node Detection on Static Attributed Graphs
- Authors: Kay Liu, Yingtong Dou, Yue Zhao, Xueying Ding, Xiyang Hu, Ruitong Zhang, Kaize Ding, Canyu Chen, Hao Peng, Kai Shu, Lichao Sun, Jundong Li, George H. Chen, Zhihao Jia, Philip S. Yu
- Venue/year: NeurIPS 2022 (Datasets and Benchmarks Track)
- Paper version URL: https://arxiv.org/abs/2206.10071v2 (PDF: https://arxiv.org/pdf/2206.10071v2). Use this version only.
- Repo: https://github.com/pygod-team/pygod (the PyGOD library; the paper's benchmark scripts are in `benchmark/`)
- Commit: 61dd13f322cf598acb22976010217aecfd17380c

## Experiment and claims
DOMINANT on the Cora dataset with synthetic outliers (`inj_cora`); each cell is "avg ± std (max)" over the benchmark's hyperparameter trials:
- Main target: Table 3 (ROC-AUC, %), DOMINANT, Cora: average 82.7.
- Held-out (same run): Table 3 ROC-AUC std 5.6 and max 84.3; Table 9 (Average Precision, %) 20.0 ± 3.0 (20.8); Table 11 (Recall@k, %) 23.8 ± 4.0 (26.1).
- Out of scope: the other detectors and datasets of these tables (separate runs; Amazon and Flickr are much larger), the organic-outlier tables, the outlier-type, time and memory tables.

Entry point: from `benchmark/`, `python main.py --model dominant --dataset inj_cora --gpu -1` (benchmark/README.md, "Usage"), after installing PyGOD from this checkout (`pip install .`) and the benchmark requirements (`pip install -r benchmark/requirements.txt`).
Per the paper, each algorithm is run over a fixed hyperparameter grid (Appendix) and the tables report the average, the standard deviation and the maximum over those trials. The script prints one line, `inj_cora DOMINANT AUC: avg±std (max)  AP: avg±std (max)  Recall: avg±std (max)`, with values as fractions.

## Data
- `inj_cora` (2,708 nodes, 1,433 features, injected contextual and structural outliers) from the public PyGOD data repository https://github.com/pygod-team/data (`inj_cora.pt.zip`, 0.2 MB; 16 MB unzipped). `pygod.utils.load_data` downloads it on first use into `~/.pygod/data`. No login needed.

## CPU feasibility (sealer's estimate, not measured)
- One run is 20 trials of full-batch DOMINANT training (300 epochs each, hidden size up to 256, dense 2,708 x 2,708 structure reconstruction). Roughly 40-150 s per trial on a 4-vCPU CPU depending on the sampled hidden size, so about 15-40 minutes per run; peak memory about 1-1.5 GB.
- Environment: PyGOD 1.0.0 (July 2023) as checked out, which expects torch 2.0-era and torch_geometric 2.3-era releases (torch_geometric must be installed separately, with pyg-lib or torch-sparse for its neighbor sampler), plus `pyod` and `tqdm` for the benchmark. With torch 2.6 or later, `torch.load` in `pygod.utils.load_data` needs `weights_only=False` to read the dataset file.

## Seal
- SHA-256 of the answer key: see `answer_key.sha256` next to this file.
- Date: 2026-10-20
