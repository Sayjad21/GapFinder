# Answer key: blind-1 (PRIVATE, sealed 2026-10-16)

## Paper
- Title: FastGCN: Fast Learning with Graph Convolutional Networks via Importance Sampling
- Authors: Jie Chen, Tengfei Ma, Cao Xiao (IBM Research)
- Venue/year: ICLR 2018
- Version the runner reads: https://arxiv.org/abs/1801.10247v1 (the only arXiv version; PDF https://arxiv.org/pdf/1801.10247v1)
- The paper (App. B.2) says only "We swept learning rate in the set {0.01, 0.001, 0.0001}" and does not state the selected value or the epoch count, so it does not give away the cause.

## Repo
- https://github.com/matenure/FastGCN
- Commit: b8e6e6412d8cb696e0adb7910832ed1ae7243ac9 (HEAD of master, 2019-04-08)
- Entry point used: `pubmed-original_transductive_FastGCN.py` (flags: --dataset cora|citeseer|pubmed, --learning_rate, --epochs, --hidden1, --dropout, --weight_decay, --early_stopping). Data for Cora/Citeseer/Pubmed ships in `data/` (Planetoid format). Seed is hard-coded at module level (123), sample size is main(400), mini-batch is hard-coded to 20.

## Targets (paper Table 5, appendix C.2, "original data split", micro-F1)
- MAIN TARGET: FastGCN-transductive, Cora: 0.818.
- Held-out claims from the same experiment:
  - FastGCN-transductive, Pubmed: 0.776
  - FastGCN (inductive script `pubmed-original_inductive_FastGCN.py`), Cora: 0.723, Pubmed: 0.721
  - GCN (original), Cora 0.814, Pubmed 0.795 (not run by sealer; train.py)

## Sealer's measurements (CPU, 10 seeds each, SEED env var patched into the module-level seed; TF2.21 compat.v1 shim, Python 3.12; 3-8 s per run)
Transductive script, Cora, accuracy (code prints accuracy, not F1):
- defaults (lr 0.01, epochs 100): mean 0.7969 sd 0.0035
- lr 0.001 only (epochs 100): mean 0.8156 sd 0.0048
- epochs 200 only (lr 0.01): mean 0.7920 sd 0.0040
- lr 0.001 + epochs 200: mean 0.8170 sd 0.0030  (paper 0.818)
Transductive script, Pubmed (control, no gap): defaults 0.7768 (paper 0.776); lr 0.001 + epochs 200: 0.7696.
Inductive script (controls, no gap): Cora defaults 0.7130 (paper 0.723), Pubmed defaults 0.7233 (paper 0.721); lr 0.001 + epochs 200 gives 0.692 / 0.705 (worse).

## Documented cause (a SETTING, paper value vs code default)
- Learning rate: 0.001 (code default 0.01). This alone closes the Cora gap (0.797 -> 0.816).
- Epochs: 200 (code default 100). Recommended by the repo owner together with the lr; on its own it does not close the gap, and with lr 0.001 it adds little.
- Applies to Cora (transductive script). Pubmed already matches at defaults.
- Equivalence set (<= 3 configs counted as correct): {lr=0.001}, {lr=0.001, epochs=200}, {lr=0.001, any epochs 100-200}. "Lower learning rate (0.001)" as the named lever is correct.
- Not part of the documented cause: hidden size, dropout, weight decay, early stopping, sample size (400), hard-coded mini-batch 20 (paper says 256 for Cora), seed, F1 vs accuracy. Naming any of these as THE explanation is confidently wrong.
- Also noted in the thread but unresolved by the owner: a commenter remarked the paper reports F1 while the code prints accuracy (numerically close).

## Sources
1. https://github.com/matenure/FastGCN/issues/10 ("Test accuracy on Cora, Citeseer, and Pubmed using original split")
   - Reporter (unlimitedsaber, 2019-01-21): Pubmed "close to the report result (77.6)"; Cora ran seeds 0-64, avg 79.8, below the paper's 81.8. Tiiiger: "I am having the same problem."
   - Owner matenure, 2019-01-25: "As I mentioned in other issues, the learning rate is one of the most important hyperparameters here. For cora, the best learning rate is 0.001. You can also increase the total epoch to 200."
   - Reporter, 2019-01-26: "For cora, the new result is avg 81.4 +-0.5".
   - cai-lw, 2019-04-02: paper reports F1, code computes accuracy, values very close.
2. Paper v1, Table 5 and appendix B.2 (hyperparameter sweep stated, selected values not).

## Pre-registered scoring rule
- correct: GapFinder's named settings match the documented ones, exactly or inside an equivalence set of at most 3 configurations;
- partial: a strict subset of the documented settings;
- diagnosed out of space: when the documented cause is in code or data, GapFinder says out of space (suspected or likely), ideally with a code lead at the right place;
- confidently wrong: a confident label (Explained / Paper-artifact inconsistency / Partially explained) on a setting that is not part of the documented cause;
- otherwise: missed (Unexplained / Inconclusive / Fits but unsupported on the wrong setting).
Clarification for this case (written before the run): the documented settings are {learning_rate=0.001, epochs=200}; the equivalence set above applies; epochs alone (without lr) is "partial".
