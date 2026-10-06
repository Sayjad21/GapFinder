# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-06 20:41 · 89 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +63.9% | +0.2% | ±6.6% | `gamma=0.9` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +63.9% → +0.2% · 34 hypotheses tested

Evidence:
- `gamma=0.9`: UNSUPPORTED, no evidence mentions '0.9'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `gamma`: gap +63.9% (ok)

Held-out claims (must not get worse beyond noise):
- C2: +160.1% → -75.0% (ok)

Replay: fork checkpoint `6e9b0a58-4cd0-4947-8741-308bdfb1d4af` and run
```
RUN_TAG=779858ef08e3 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.9 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
```
(result checkpoint `1be1409a-ac84-4d0a-a97c-93bb2993ff55`; 3 repeat(s) recorded)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`
