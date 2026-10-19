# batch-4: result after the reveal (code frozen at tag `batch-4`, `bae25f4`)

One paper was sealed (the first batch-4 sealer found none in 90 minutes; the second sealed one). The run was
committed in `fc47ad3` before the key was opened. The key matches its sealed hash (`09b93edc...7020`) and is copied to
`b4a/answer_key.md`.

| Case | Documented cause | GapFinder | Score (the key's pre-registered rule) |
|---|---|---|---|
| **b4a** RippleNet (CIKM 2018), Book-Crossing | The README command trains with main.py's argparse defaults, which are the MovieLens settings. Book-Crossing needs `lr` 1e-3 and `l2_weight` 1e-5 (paper Table 2; a commented-out block in `src/main.py`). The repo owner confirmed it in issue #4 | **Fits but unsupported, `lr = 0.001`**, partial: the 150-run budget ran out. AUC gap -11.9% → -5.1%; held-out ACC -7.4% → -3.8% | **partial**: lr is in range; l2_weight is not named |

**Running total of sealed blind real papers:**

| Batch | Result |
|---|---|
| blind-1 | missed |
| blind-2 | confidently wrong |
| devbatch-1 | 1 of 5 |
| devbatch-2 | 0 of 3 |
| batch-3 | 1 of 2 |
| batch-4 | 1 partial |

Since the confidence cap went in, nothing has been confidently wrong.

## Why only partial (each a class; fix after the batch, measure on the next one)

1. **An interaction with no effect on its own.**
   - `l2_weight = 1e-5` alone measured AUC 0.644 against the naive 0.650. It helps only together with
     `lr = 1e-3`.
   - Combine pairs only leads that moved the gap alone, so lr + l2_weight was never run.
   - The class: a setting whose effect depends on another (a regulariser matters once the learning rate stops
     overfitting).
   - The forward step should try every screened knob on top of the best single answer while a gap remains,
     not only the leads.
2. **The paper's table, in symbols, was not linked to the flags.**
   - Table 2 states "λ1 = 10⁻⁵, η = 0.001" for Book-Crossing, but the ledger recorded `--l2_weight` as unstated.
   - The flag's help text says "weight of the l2 regularization term" and the paper calls λ1 the L2 weight. The
     link was not made.
   - The class: hyperparameter tables written in symbols.
   - The assumption step should see each flag's help text, and the paper's symbol definitions next to its tables.
3. **Alternative settings kept in the repo, but not as code.**
   - `src/main.py` holds a commented-out (string) argparse block titled "default settings for Book-Crossing", with
     the exact values.
   - GapFinder's code checks parse code only.
   - The class: per-dataset settings in comments, strings, scripts or a README table.
   - A static check should read argparse blocks inside strings and comments as alternative defaults, with their
     location as evidence.

## The environment builder

- The environment worked: TensorFlow 1.4 on python:3.6.
- The goal command was parsed from the README as `python preprocess.py --dataset movie (or --dataset book)`,
  a bash syntax error, so the build was reported failed after 12 commands.
- Fixed after the batch (`7a1e0dd`): prose after a README command is dropped, and a `cd` on the line before is
  kept.

## Infrastructure

The first search attempt (`run_netfail/`) lost every naive run to a DNS outage on this machine and was
relaunched unchanged.
