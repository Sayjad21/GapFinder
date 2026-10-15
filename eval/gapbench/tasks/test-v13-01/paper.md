# Logistic Regression with SGD for Imbalanced Tabular Screening

## Abstract
We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.758 test accuracy.

## Experimental setup
The synthetic dataset has 1,200 rows with eight numeric features, a 30% positive rate and 5% label noise. The first 80% of rows are used for training and the rest for testing (data seed 7). The model is logistic regression trained by mini-batch SGD for 15 epochs (batch size 32, a constant learning rate of 0.05, no weight decay and no class weighting). Numbers are medians over 7 runs with different shuffling seeds.

## Results
Table 1 reports the main result: test accuracy 0.758, balanced accuracy 0.748.

| Model | Test accuracy | Balanced accuracy |
|---|---|---|
| Logistic regression (ours) | 0.758 | 0.748 |
