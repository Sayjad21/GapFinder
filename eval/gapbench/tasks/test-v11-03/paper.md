# Logistic Regression with SGD for Imbalanced Tabular Screening

## Abstract
A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

## Experimental setup
The synthetic dataset has 1,200 rows with eight numeric features. The first 80% of rows are used for training and the rest for testing (data seed 7). Features are used raw, without any scaling. The model is logistic regression trained by mini-batch SGD for 15 epochs (a constant learning rate of 0.05, no weight decay and no class weighting). Predictions use a decision threshold of 0.5. Numbers are medians over 7 runs with different shuffling seeds.

## Results
Table 1 reports the main result: test accuracy 0.783, balanced accuracy 0.752.

| Model | Test accuracy | Balanced accuracy |
|---|---|---|
| Logistic regression (ours) | 0.783 | 0.752 |
