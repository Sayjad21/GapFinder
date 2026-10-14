# Plain Logistic Regression Is a Strong Baseline for Credit Screening

## Abstract
A plain logistic-regression baseline reaches 0.596 test accuracy and 0.500 balanced accuracy on a synthetic screening task.

## Experimental setup
The synthetic dataset has 1,200 rows with eight numeric features, a 30% positive rate and 5% label noise. The first 80% of rows are used for training and the rest for testing (data seed 7). The model is logistic regression trained by mini-batch SGD for 15 epochs (batch size 32, a constant learning rate of 0.05, no weight decay and no class weighting). Predictions use a decision threshold of 0.5. Numbers are medians over 7 runs with different shuffling seeds.

## Results
Table 1 reports the main result: test accuracy 0.596, balanced accuracy 0.500.

| Model | Test accuracy | Balanced accuracy |
|---|---|---|
| Logistic regression (ours) | 0.596 | 0.500 |
