# Spec draft report for mlbench.yaml

**Status:** verified: the spec built, ran and parsed its metrics

- backend: local; attempts with a smoke test: 2; model calls: 2
- Nemotron cost: $0.0036 billed, $0.0036 without the cache; sandbox cost reported: $0.0000
- knobs in the spec: 14; repo-map flags shown to the model: 15 of 15

## Attempts

| # | tier | stage | cost | what happened |
|---|---|---|---|---|
| 1 | super | run | $0.0016 | smoke / /usr/bin/bash: line 1: G:/Competitions/GapFinder/.venv/Scripts/python.exe:-python3: No such file or directory  |
| 2 | super | ok | $0.0020 | ok |

## Metrics parsed by the smoke test

balanced_accuracy, test_accuracy

## Knobs

| knob | layer | default | env |
|---|---|---|---|
| n | dataset | `1200` |  |
| positive_rate | dataset | `0.3` |  |
| label_noise | dataset | `0.05` |  |
| split | dataset | `0.8` |  |
| normalize | config | `none` |  |
| epochs | config | `15` |  |
| batch_size | config | `32` |  |
| lr | config | `0.05` |  |
| lr_schedule | config | `const` |  |
| weight_decay | config | `0.0` |  |
| class_weight | config | `none` |  |
| threshold | config | `0.5` |  |
| data_seed | dataset | `7` |  |
| RUN_TAG | environment | `` | yes |

## Warnings

- 1 repo-map flags are not knobs: out

## The model's own uncertainty

Uncertain about exact metric names output by train.py; assumed JSON output. All flags affecting measurement included as knobs; RUN_TAG treated as environment knob that does not alter measurements.

## Knob recall against the hand-written spec (mlbench)

- recall: 13/13 = 100%
- found: n, positive_rate, label_noise, split, data_seed, normalize, epochs, batch_size, lr, lr_schedule, weight_decay, class_weight, threshold
- missing: (none)
- extra (in the draft only): RUN_TAG
- same default: 13/13; same layer: 13/13

## For the person approving

Read the commands and knob defaults against the repo, then use the spec. `gapfinder spec-draft --diff draft.yaml edited.yaml` shows what you changed.
