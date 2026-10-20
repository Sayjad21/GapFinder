# Blind case b5a

- Paper: Topology Attack and Defense for Graph Neural Networks: An Optimization Perspective
- Authors: Kaidi Xu, Hongge Chen, Sijia Liu, Pin-Yu Chen, Tsui-Wei Weng, Mingyi Hong, Xue Lin
- Venue/year: IJCAI 2019
- Paper version URL: https://arxiv.org/abs/1906.04214v3 (PDF: https://arxiv.org/pdf/1906.04214v3). Use v3 only.
- Repo: https://github.com/KaidiXu/GCN_ADV_Train
- Commit: 7ace67ad2a54804f6a138e52e78ea7fdab34d009

## Experiment and claims
Table 3 (misclassification rate in %, CE-PGD attack, Cora), column "epsilon in robust training = 0" (the natural model):
- Main target: 5% perturbed edges: 27.9 (test accuracy 0.721).
- Held-out (same natural model, other attack budgets): 10%: 32.7; 15%: 36.7; 20%: 40.2.
- Held-out (same natural model, no attack): 0%: 18.1.
- Held-out (Table 1, fixed natural model, 5% perturbed edges, Cora): CE-PGD 28.0; CW-PGD 27.8.
- Out of scope: the robust-model columns of Table 3 (adversarial training, a separate experiment) and the Citeseer columns.

Entry point (README): `python train.py` (trains the natural Cora GCN, saves it in `nat_cora/` and writes `label_cora.npy`), then `python attack.py --model_dir=nat_cora`. The attack budget is the flag `--perturb_ratio` of `attack.py` (one run per budget); `--method=CW` selects the CW-type attack (the default is PGD with the CE loss).
`attack.py` prints the test accuracy after the attack ("Test set results: ... accuracy="); `train.py` prints the clean test accuracy. Misclassification rate = 100 x (1 - accuracy).
The paper states that each experiment is repeated 5 times on different splits of training/testing nodes and reports the mean misclassification rate on the test nodes.

## Data
Cora in the Planetoid format (`ind.cora.*`), shipped in the repo under `data/`. No download or login is needed.

## CPU feasibility (sealer's estimate, not measured)
- `train.py`: a 2-layer GCN on Cora, at most 100 epochs: well under a minute.
- `attack.py`: 100 attack steps on dense 2708 x 2708 matrices plus 20 random samples: a few minutes per budget on 4 vCPUs; peak memory about 1-1.5 GB. All five budgets plus the CW run fit in well under an hour.
- Environment: the README targets Python 3.6 and TensorFlow 1.13 (`tf.app.flags`, `tf.placeholder`, `tf.Session`); the CPU build of TensorFlow 1.13-1.15 works. `utils.py` imports `scipy.sparse.linalg.eigen.arpack` (use scipy < 1.8) and networkx; `attack.py` imports matplotlib. Use numpy < 1.17 with TF 1.13.

## Seal
- SHA-256 of the answer key: see `answer_key.sha256` next to this file.
- Date: 2026-10-20

Sealed by an independent model (the sealer). The answer key is held outside the repository until the reveal.
