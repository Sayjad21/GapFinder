# Spec draft report for rlbench.yaml

**Status:** verified: the spec built, ran and parsed its metrics

- backend: local; attempts with a smoke test: 2; model calls: 2
- Nemotron cost: $0.0045 billed, $0.0045 without the cache; sandbox cost reported: $0.0000
- knobs in the spec: 16; repo-map flags shown to the model: 17 of 17

## Attempts

| # | tier | stage | cost | what happened |
|---|---|---|---|---|
| 1 | super | run | $0.0022 | smoke / Traceback (most recent call last):   File "C:\Users\Turjo\AppData\Local\Temp\gf-spec-draft-q75fy71k\images\077482c4-d3c1-48bf-9de5-16a28c8c3fc4\cartpole_q.py", line 114, in <module>     main()   File "C:\Users\Turjo\AppData\Local |
| 2 | super | ok | $0.0023 | ok |

## Metrics parsed by the smoke test

max_reward, mean_reward, min_reward

## Knobs

| knob | layer | default | env |
|---|---|---|---|
| episodes | config | `400` |  |
| gamma | config | `0.99` |  |
| lr | config | `0.1` |  |
| lr_schedule | config | `const` |  |
| eps_start | config | `1.0` |  |
| eps_end | config | `0.05` |  |
| eps_decay | config | `0.99` |  |
| theta_bins | config | `6` |  |
| omega_bins | config | `6` |  |
| reward_norm | config | `off` |  |
| max_steps | config | `200` |  |
| init_q | config | `0.0` |  |
| seeds | config | `10` |  |
| eval_episodes | config | `20` |  |
| RUN_TAG | environment | `` | yes |
| RL_SEED_BASE | environment | `0` | yes |

## Warnings

- 1 repo-map flags are not knobs: out

## The model's own uncertainty

Fixed RL_SEED_BASE default to avoid empty string causing ValueError. Uncertain about exact metric names produced by the script; output format treated as auto.

## Knob recall against the hand-written spec (rlbench)

- recall: 14/14 = 100%
- found: episodes, gamma, lr, lr_schedule, eps_start, eps_end, eps_decay, theta_bins, omega_bins, reward_norm, max_steps, init_q, seeds, eval_episodes
- missing: (none)
- extra (in the draft only): RUN_TAG, RL_SEED_BASE
- same default: 14/14; same layer: 11/14
  - layer of max_steps: hand workload, draft config
  - layer of seeds: hand workload, draft config
  - layer of eval_episodes: hand workload, draft config

## For the person approving

Read the commands and knob defaults against the repo, then use the spec. `gapfinder spec-draft --diff draft.yaml edited.yaml` shows what you changed.
