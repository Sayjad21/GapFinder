# HARNESS.md (written by `gapfinder harness`)

**Status:** stopped at smoke: the smoke run failed (exit 120): .softmax_cross_entropy_with_logits_v2`.

WARNING:tensorflow:From /usr/local/lib/python3.6/site-packages/tensorflow/python/ops/math_ops.py:3066: to_int32 (from tensorflow.python.ops.math_ops) is deprecated and will be removed in a future version.
Instructions for updating:
Use tf.cast instead.
2026-10-20 05:01:54.123646: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 AVX512F FMA
2026-10-20 05:01:54.145377: I tensorflow/core/platform/profile_utils/cpu_utils.cc:94] CPU Frequency: 2397245000 Hz
2026-10-20 05:01:54.146493: I tensorflow/compiler/xla/service/service.cc:150] XLA service 0x55555567a1d0 executing computations on platform Host. Devices:
2026-10-20 05:01:54.146583: I tensorflow/compiler/xla/service/service.cc:158]   StreamExecutor device (0): <undefined>, <undefined>
WARNING:tensorflow:From /usr/local/lib/python3.6/site-packages/tensorflow/python/training/saver.py:1266: checkpoint_exists (from tensorflow.python.training.checkpoint_management) is deprecated and will be removed in a future version.
Instructions for updating:
Use standard file APIs to check for files with this prefix.



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
bash -c 'echo "deb http://archive.debian.org/debian/ stretch main" > /etc/apt/sources.list && echo "deb http://archive.debian.org/debian-security/ stretch/updates main" >> /etc/apt/sources.list && apt-get update && apt-get install -y --no-install-recommends wget ca-certificates && pip install --no-cache-dir --upgrade pip setuptools && pip install --no-cache-dir numpy==1.16.4 scipy==1.2.1 matplotlib==3.0.3 networkx==2.2 seaborn==0.9.0 tensorflow==1.13.1'
python train.py
```

## Data kept in the base checkpoint

0 files, 0.0 MB (new since the environment: downloads, preprocessing, dataset loaders' caches). 4 other new files deleted (outputs, logs, model checkpoints).


## Smoke run

4 run(s) in parallel; exit 120 after 80.0 s

Model spend: $0.0147
