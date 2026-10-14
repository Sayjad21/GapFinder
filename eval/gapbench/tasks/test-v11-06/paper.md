# A Simple Baseline for Synthetic Credit Data

## Abstract
We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.504 test accuracy.

## Experimental setup
The synthetic dataset has 1,200 rows with eight numeric features, 5% label noise. The first 80% of rows are used for training and the rest for testing (data seed 7). Features are used raw, without any scaling. The model is logistic regression trained by mini-batch SGD for 15 epochs (batch size 32, a constant learning rate of 0.05, no weight decay and no class weighting). Predictions use a decision threshold of 0.5. Numbers are medians over 7 runs with different shuffling seeds.

## Results
Table 1 reports the main result: test accuracy 0.504, balanced accuracy 0.504.

| Model | Test accuracy | Balanced accuracy |
|---|---|---|
| Logistic regression (ours) | 0.504 | 0.504 |
