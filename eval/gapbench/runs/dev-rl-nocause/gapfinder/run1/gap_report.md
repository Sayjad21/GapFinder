# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-10 17:15 · 38 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +56.0% | +12.0% | ±17.8% | `lr_schedule=inv`, `eps_end=0.01` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +56.0% → +12.0% · 9 hypotheses tested

Evidence:
- `lr_schedule=inv`: UNSUPPORTED, no evidence mentions 'inv'; it fits, but nothing says the authors used it
- `eps_end=0.01`: UNSUPPORTED, no evidence mentions '0.01'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `lr_schedule`: gap +39.2% (ok)
- without `eps_end`: gap +18.9% (gap did NOT return)

Held-out claims (must not get worse beyond noise):
- C2: -19.8% → -62.8% (ok)

Replay: fork checkpoint `3222dcc7-461c-4f11-a209-9bfbffc1e28f` and run
```
RUN_TAG=d18cb2d03a97 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.01 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
```
(result checkpoint `9404d55e-0957-4beb-9583-f53b4293f7db`; 5 repeat(s) recorded)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 5 | +18.9% | -18.0% | 18.4% |
| `lr_schedule=linear` | 5 | +37.5% | -2.0% | 19.8% |
| `theta_bins=4` | 5 | +48.4% | -3.4% | 25.9% |
| `lr_schedule=inv`, `eps_end=0.01` | 5 | +12.0% | -62.8% | 37.4% |
| naive (reproduction as run) | 5 | +56.0% | -19.8% | 37.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`
