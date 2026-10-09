# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-09 12:39 · 42 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +51.4% | +14.1% | ±8.2% | `lr_schedule=inv`, `eps_end=0.1` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +51.4% → +14.1% · 9 hypotheses tested

Evidence:
- `lr_schedule=inv`: UNSUPPORTED, no evidence mentions 'inv'; it fits, but nothing says the authors used it
- `eps_end=0.1`: UNSUPPORTED, no evidence mentions '0.1'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `lr_schedule`: gap +27.8% (ok)
- without `eps_end`: gap +19.7% (gap did NOT return)

Held-out claims (must not get worse beyond noise):
- C2: -8.6% → -10.8% (ok)

Replay: fork checkpoint `761bcc5b-a2c6-42bd-b2eb-156acf79b10d` and run
```
RUN_TAG=29639ca36d36 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.1 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
```
(result checkpoint `8a4d0973-f99d-49f1-b5f2-c3a5110e278b`; 5 repeat(s) recorded)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_end=0.1` | 5 | +14.1% | -10.8% | 12.4% |
| `eps_end=0.1` | 5 | +27.8% | -29.6% | 28.7% |
| `lr_schedule=inv` | 5 | +19.7% | -39.2% | 29.4% |
| naive (reproduction as run) | 5 | +51.4% | -8.6% | 30.0% |
| `lr_schedule=inv`, `theta_bins=8` | 5 | +9.3% | -63.7% | 36.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`
