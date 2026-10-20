# HARNESS.md (written by `gapfinder harness`)

**Status:** ready for approval

A person reads the commands below and approves them (about 5 minutes). The knobs are mechanical: every flag of the script at its default, so they need no approval.

## Claims

Rule: the target, then every other cell of its table row (same conditions, another metric) as held-outs.

| claim | role | metric | paper | spec metric |
|---|---|---|---|---|
| C_t3_5 | target | test accuracy | 0.721 | `c_t3_5_acc` |

Only one claim: history matching can't tell configurations apart, so labels stay cautious.

## Claims at other settings (identifiability)

Cells with the target's setup and one other setting. A claim at a fixed knob value is run with that value on top of each candidate; a learning-curve point is read from the same run's per-epoch log.

- C_t3_10: test accuracy 0.673 at `perturb_ratio=0.10`
- C_t3_15: test accuracy 0.633 at `perturb_ratio=0.15`
- C_t3_20: test accuracy 0.598 at `perturb_ratio=0.20`
- C_t3_0: test accuracy 0.819 at `perturb_ratio=0`

## Command

Picked by the claims' words in the command's arguments (README and shell scripts):

**picked** `python attack.py --model_dir=nat_cora` (README.md:67; matched cora)
- `python train.py` (README.md:46; matched nothing)
- `python adv_train_pgd.py` (README.md:57; matched nothing)

One run, at every default:

```
"${PYTHON:-python}" attack.py --model_dir nat_cora --dataset cora --steps 100 --learning_rate 0.001 --hidden1 16 --dropout 0. --early_stopping 10 --method PGD --perturb_ratio 0.05 --weight_decay 5e-4
```

### Knobs

| knob | default | declared at |
|---|---|---|
| steps | `100` | attack.py:25 |
| learning_rate | `0.001` | attack.py:26 |
| hidden1 | `16` | attack.py:27 |
| dropout | `0.` | attack.py:28 |
| early_stopping | `10` | attack.py:29 |
| method | `PGD` | attack.py:30 |
| perturb_ratio | `0.05` | attack.py:31 |
| weight_decay | `5e-4` | attack.py:32 |

### Fixed (not knobs)

- `model_dir`: how to run (paths, devices, logging), not the method
- `dataset`: dataset: defines the claim

## Environment

Image `python:3.6-slim`; checkpoint `9b380d15-e2d6-43d5-82da-4e25a124d8fd`; recipe:

```
(none needed)
```

## Data kept in the base checkpoint

0 files, 0.0 MB (new since the environment: downloads, preprocessing, dataset loaders' caches). 1 other new files deleted (outputs, logs, model checkpoints).


## Smoke run

1 run(s) in parallel; exit 0 after 55.0 s

- `c_t3_5_acc`: 0.684

Seeds vary: **no: identical runs; the noise band will be zero**

## Metric binding

Test before unqualified before validation before train; final before best; on the paper's scale. A tie is a refusal.

| claim | printed label | value | scale | alternatives |
|---|---|---|---|---|
| C_t3_5 | `test accuracy` | 0.684 | 1 | `val_acc`, `val accuracy`, `train accuracy` |

## Paper-year environment (knob `gf_paper_year_env`)

Packages as of 2019-07-01 (Python 3.6.15): none older than installed.

- matplotlib: installed 3.0.3 is already from then
- networkx: installed 2.2 is already from then
- numpy: installed 1.16.4 is already from then
- scipy: installed 1.2.1 is already from then
- seaborn: installed 0.9.0 is already from then
- tensorflow: installed 1.13.1 is already from then

## Fit in one Sandboxes operation (3600 s)

as is: about 55 s fits one operation

Model spend: $0.0000
