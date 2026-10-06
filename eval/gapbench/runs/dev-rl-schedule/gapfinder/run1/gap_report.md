# Gap Report: dev-rl-schedule

Artifact `rlbench` · generated 2026-10-06 21:37 · 15 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +30.9% | +0.0% | ±8.7% | `lr_schedule=inv` |

## C1: mean_reward (paper 139.35)
**Paper-artifact inconsistency** · gap +30.9% → +0.0% · 2 hypotheses tested

Evidence:
- `lr_schedule=inv`: supported, paper states 'inv (0.1 / (1 + t/50))'

Counterfactual (revert one knob; the gap must come back):
- without `lr_schedule`: gap +30.9% (ok)

Held-out claims (must not get worse beyond noise):
- C2: +86.4% → +31.2% (ok)

Replay: fork checkpoint `2f51b34f-9681-47d5-b040-20fccba3473e` and run
```
RUN_TAG=89fc9900f4bb "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
```
(result checkpoint `9196b824-f393-4cb3-898d-99c5092e6f31`; 5 repeat(s) recorded)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `discretise_theta_range`, `discretise_omega_range`, `cartpole_g`, `cartpole_dt`, `reset_uniform_range`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `RUN_TAG`, `greedy_evaluation_policy`
