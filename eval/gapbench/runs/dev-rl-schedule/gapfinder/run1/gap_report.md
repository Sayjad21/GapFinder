# Gap Report: dev-rl-schedule

Artifact `rlbench` · generated 2026-10-06 20:45 · 15 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +30.7% | -2.6% | ±8.2% | `lr_schedule=inv` |

## C1: mean_reward (paper 139.35)
**Paper-artifact inconsistency** · gap +30.7% → -2.6% · 2 hypotheses tested

Evidence:
- `lr_schedule=inv`: supported, paper states 'inv (0.1 / (1 + t/50))'

Counterfactual (revert one knob; the gap must come back):
- without `lr_schedule`: gap +30.7% (ok)

Held-out claims (must not get worse beyond noise):
- C2: +101.2% → +5.0% (ok)

Replay: fork checkpoint `c2a66d20-ab30-4375-b868-a892195b043b` and run
```
RUN_TAG=e140fc361b89 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
```
(result checkpoint `b944f551-50fb-4fdf-86aa-660965ff5d80`; 5 repeat(s) recorded)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `discretise_theta_range`, `discretise_omega_range`, `cartpole_g`, `cartpole_dt`, `reset_uniform_range`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `RUN_TAG`, `greedy_evaluation_policy`
