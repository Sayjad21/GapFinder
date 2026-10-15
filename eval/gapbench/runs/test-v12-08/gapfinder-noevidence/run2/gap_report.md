# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 08:37 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +86.9% | -1.2% | ±20.7% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +86.9% → -1.2% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0058`, `B0059`, `B0070`, `B0071`, `B0072` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `8cecad99-be1b-4c36-a1a0-9fa872e7b68b` and run
  ```
  RUN_TAG=8349d70cb54b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.13, 96.78, 98.6, 94.36, 98.31, 87.69; gap after -1.2%; result checkpoint `90c65ba9-26c8-4fbf-ac49-911209b8a813`
- Effect: candidate 97.55 minus naive 184.5 = -86.92, 95% bootstrap interval [-102.3, -75.82] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 184.5 over 5 runs; repeats: 184.5, 195.2, 194.7, 177.3, 171.3
- Spread: range 171.3 to 195.2, noise band ±20.45 (2 x MAD), CV 5.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +86.9% (noise band ±20.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +86.9% (it comes back)
- PASS · Held-out claim: C2: +43.0% to -20.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -86.92 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.02` (3.78 noise units, gap -8.6%); `lr=1` (3.61 noise units, gap -12.2%); `lr=0.002` (3.51 noise units, gap -14.2%); `lr=0.5` (3.2 noise units, gap +20.7%); `lr=0.01` (3.07 noise units, gap -23.2%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -1.1%, mean |gap| 1.2% (5 runs)
  - `lr=0.5`, `max_steps=100`: this claim -0.7%, mean |gap| 8.6% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -10.0%, mean |gap| 40.7% (5 runs)

### History matching (every measured configuration, all claims together)
- 11 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.16); lr_schedule=inv, max_steps=100 (max I 1.51)
  - `max_steps`: max_steps=100 (max I 0.64)
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.7)
  - `lr, lr_schedule`: lr=0.02, lr_schedule=linear (max I 1.08); lr=0.002, lr_schedule=linear (max I 1.26); lr=0.002, lr_schedule=inv (max I 2.9)
  - `lr`: lr=1 (max I 1.94); lr=0.5 (max I 2.46); lr=0.002 (max I 2.54)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '40', 'lr': '0.5'} for 'confirm-combo')
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | -1.1% | -1.3% | 1.2% |
| `lr=0.5`, `max_steps=100` | 5 | -0.7% | -16.6% | 8.6% |
| `max_steps=100` | 6 | -1.2% | -20.0% | 10.6% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -10.0% | -71.3% | 40.7% |
| `lr=1` | 6 | -5.8% | -83.5% | 44.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
