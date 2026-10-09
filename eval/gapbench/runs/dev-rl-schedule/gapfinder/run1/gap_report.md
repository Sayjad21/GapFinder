# Gap Report: dev-rl-schedule

Artifact `rlbench` · generated 2026-10-09 12:38 · 11 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +32.4% | -4.5% | ±7.9% | `lr_schedule=inv` |

## C1: mean_reward (paper 139.35)
**Paper-artifact inconsistency** · gap +32.4% → -4.5% · 2 hypotheses tested

Evidence:
- `lr_schedule=inv`: supported, paper states 'inv (0.1 / (1 + t/50))'

Counterfactual (revert one knob; the gap must come back):
- without `lr_schedule`: gap +32.4% (ok)

Held-out claims (must not get worse beyond noise):
- C2: +159.0% → +2.8% (ok)

Replay: fork checkpoint `418343a7-13a6-427c-a860-4e8576630bbf` and run
```
RUN_TAG=9dddf1d0d1fe "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
```
(result checkpoint `5e265c88-6885-40f8-a57d-97ee2b54c0b3`; 3 repeat(s) recorded)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 3 | -4.5% | +2.8% | 3.6% |
| naive (reproduction as run) | 5 | +32.4% | +159.0% | 95.7% |
| `lr_schedule=linear` | 3 | +22.2% | +415.3% | 218.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `discretise_theta_range`, `discretise_omega_range`, `cartpole_g`, `cartpole_dt`, `reset_uniform_range`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `RUN_TAG`, `greedy_evaluation_policy`
