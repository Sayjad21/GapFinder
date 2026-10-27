# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 21:02 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +87.7% | +0.2% | ±24.6% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +87.7% → +0.2% · 56 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0033`, `B0072`, `B0073`, `B0076`, `B0077`, `B0078` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `8d5a4e30-f653-4eb9-a311-aed9bf2bb421` and run
  ```
  RUN_TAG=69a80c546c94 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 96.15, 96.22, 94.06, 94.14, 94.16, 97.55; gap after +0.2%; result checkpoint `3cce93c3-6a3c-4c10-9eb6-4018c2d31918`
- Effect: candidate 95.15 minus naive 178.2 = -83.04, 95% bootstrap interval [-96.52, -57.6] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 178.2 over 5 runs; repeats: 191.8, 178.2, 169.9, 189.9, 148.9
- Spread: range 148.9 to 191.8, noise band ±23.37 (2 x MAD), CV 9.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +87.7% (noise band ±24.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +87.7% (it comes back)
- PASS · Held-out claim: C2: -13.8% to -8.5% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -83.04 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.05` (3.35 noise units, gap +5.2%); `eps_start=0.5` (3.17 noise units, gap +9.7%); `lr=1` (3.12 noise units, gap +11.0%); `lr=0.5` (3.05 noise units, gap +12.7%); `lr=0.001` (2.77 noise units, gap -19.4%) (and 8 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +3.1%, mean |gap| 24.1% (5 runs)
  - `eps_start=0.2`, `lr=1`: this claim -2.9%, mean |gap| 32.4% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -6.4%, mean |gap| 40.3% (5 runs)

### History matching (every measured configuration, all claims together)
- 23 of 56 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=100 (max I 0.07)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.44); lr_schedule=inv, max_steps=100 (max I 0.85)
  - `eps_start, lr`: eps_start=0.2, lr=1 (max I 0.95); eps_start=0.5, lr=0.05 (max I 1.16); eps_start=0.5, lr=1 (max I 1.21)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.25)
  - `lr`: lr=0.02 (max I 1.26)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.29)
  - `lr, max_steps`: lr=0.05, max_steps=100 (max I 1.36)

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'max_steps': '100', 'lr': '1'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +0.2% | -8.5% | 4.4% |
| `max_steps=100`, `lr_schedule=linear` | 5 | +3.1% | +45.1% | 24.1% |
| `eps_start=0.2`, `lr=1` | 5 | -2.9% | -61.8% | 32.4% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -6.4% | -74.3% | 40.3% |
| `max_steps=100`, `lr=0.05` | 5 | -13.8% | -72.0% | 42.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
