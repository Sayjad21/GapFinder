# Gap Report: dev-rl-schedule

Artifact `rlbench` · generated 2026-10-07 16:20 · 11 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +33.4% | -22.1% | ±6.3% | `lr_schedule=inv` |

## C1: mean_reward (paper 139.35)
**Paper-artifact inconsistency** · gap +33.4% → -22.1% · 2 hypotheses tested

Evidence:
- `lr_schedule=inv`: supported, paper states 'inv (0.1 / (1 + t/50))'

Counterfactual (revert one knob; the gap must come back):
- without `lr_schedule`: gap +33.4% (ok)

Held-out claims (must not get worse beyond noise):
- C2: +348.5% → -55.2% (ok)

Replay: fork checkpoint `dce5cb3c-153d-4119-8f3b-2b114b73da30` and run
```
RUN_TAG=c5d00f8e63f1 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
```
(result checkpoint `ee38aa68-69fa-46e7-bedc-c293fe7a2e6e`; 3 repeat(s) recorded)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `discretise_theta_range`, `discretise_omega_range`, `cartpole_g`, `cartpole_dt`, `reset_uniform_range`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `RUN_TAG`, `greedy_evaluation_policy`
