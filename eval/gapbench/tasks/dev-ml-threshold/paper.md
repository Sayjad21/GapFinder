# Calibrated Decision Thresholds for Imbalanced Tabular Screening

## Abstract
On imbalanced screening data, accuracy depends as much on the decision rule
as on the model. We report logistic regression with a base-rate threshold.

## Experimental setup
We use a synthetic screening dataset of 1,200 rows with eight numeric
features, 30% positives and 5% label noise, split 80/20 (data seed 7). The
model is logistic regression trained by mini-batch SGD for 15 epochs (batch
size 32, learning rate 0.05, constant schedule, no weight decay, no class
weighting). Following common practice for imbalanced data, the decision
threshold is set to the positive rate of the training data rather than 0.5.
Results are medians over seven runs.

## Results
Table 2: test accuracy 0.758, balanced accuracy 0.784.

| Model | Test accuracy | Balanced accuracy |
|---|---|---|
| Logistic regression, base-rate threshold | 0.758 | 0.784 |
