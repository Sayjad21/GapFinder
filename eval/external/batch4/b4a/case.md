# Blind case b4a

- Paper: RippleNet: Propagating User Preferences on the Knowledge Graph for Recommender Systems
- Authors: Hongwei Wang, Fuzheng Zhang, Jialin Wang, Miao Zhao, Wenjie Li, Xing Xie, Minyi Guo
- Venue/year: CIKM 2018
- Paper version URL: https://arxiv.org/abs/1803.03467v4 (PDF: https://arxiv.org/pdf/1803.03467v4). Use v4 only (earlier versions have different Book-Crossing numbers).
- Repo: https://github.com/hwwang55/RippleNet
- Commit: 05459f1e6a47080375a0556aa70b6a286fa5b636

## Experiment and claims
Table 3 (CTR prediction, RippleNet row), Book-Crossing:
- Main target: Book-Crossing AUC 0.729.
- Held-out (same run): Book-Crossing ACC 0.662.
- Out of scope: MovieLens-1M (needs the separately downloaded ratings file) and Bing-News (not released).

Entry point: per the README, `cd src; python preprocess.py --dataset book; python main.py --dataset book`.
`src/train.py` prints train / eval / test AUC and ACC after every epoch.
The paper reports the mean of 5 repeated runs and does not name an epoch. Evaluate each configuration as the test AUC and ACC printed at the last epoch, averaged over 5 runs. `main.py` fixes the numpy seed (555) but sets no TensorFlow seed, so runs differ.

## Data
Shipped in the repo under `data/book/`: `BX-Book-Ratings.csv` (Book-Crossing ratings), `item_index2entity_id_rehashed.txt` and `kg_rehashed.txt` (knowledge graph). `preprocess.py --dataset book` writes `ratings_final.txt` and `kg_final.txt` (about 78k entities, 25 relations). No download or login is needed.

## CPU feasibility (sealer's estimate)
- Preprocessing takes seconds. One training run (10 epochs, batch 1024) took 1-2 minutes on a laptop CPU. 5 runs per configuration take about 10 minutes.
- Memory is well under 1 GB.
- Environment: the code targets TensorFlow 1.x (README: tensorflow-gpu 1.4.0, numpy 1.14.5, scikit-learn 0.19.1, Python 3.6). On a current stack (for example tensorflow-cpu 2.15 on Python 3.11, numpy < 2), use `import tensorflow.compat.v1 as tf; tf.disable_v2_behavior()` in `src/model.py` and `src/train.py`, and replace `tf.contrib.layers.xavier_initializer()` (three uses in `src/model.py`) with `tf.glorot_uniform_initializer()`, which is the same initializer.

## Seal
- SHA-256 of the answer key: see `answer_key.sha256` next to this file.
- Date: 2026-10-19

Sealed by an independent model (the sealer). The answer key is held outside the repository until the reveal.
