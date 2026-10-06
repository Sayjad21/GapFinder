# Gap Report: dev-rl-schedule

Artifact `rlbench` · generated 2026-10-06 20:40 · 66 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +30.0% | +1.1% | ±10.7% | `eps_start=0.5` |

## C1: mean_reward (paper 139.35)
**Fits but unsupported** · gap +30.0% → +1.1% · 33 hypotheses tested

Evidence:
- `eps_start=0.5`: UNSUPPORTED, no evidence mentions '0.5'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `eps_start`: gap +30.0% (ok)

Held-out claims (must not get worse beyond noise):
- C2: +266.6% → -43.4% (ok)

Replay: fork checkpoint `74032552-74bc-492d-a38d-9210fee7484b` and run
```
RUN_TAG=7e552f279c0a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.5 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
```
(result checkpoint `47b68f83-4aa2-4d29-bf80-08aeb00604da`; 3 repeat(s) recorded)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `discretise_theta_range`, `discretise_omega_range`, `cartpole_g`, `cartpole_dt`, `reset_uniform_range`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `RUN_TAG`, `greedy_evaluation_policy`
