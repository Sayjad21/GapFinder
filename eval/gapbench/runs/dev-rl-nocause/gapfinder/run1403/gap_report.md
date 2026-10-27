# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 18:46 · 135 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +42.0% | +5.3% | ±30.9% | `theta_bins=12`, `lr_schedule=linear` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +42.0% → +5.3% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0092`, `B0105`, `B0109`, `B0110`, `B0111` (5 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `12`
- Config: `lr_schedule` naive `const`, changed to `linear`
- Command:

  Replay: fork checkpoint `6fa9196e-300b-42f8-be2b-4132c0afc339` and run
  ```
  RUN_TAG=615b46aecc72 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule linear --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 12 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 117.8, 109.6, 129.5, 152, 125.2; gap after +5.3%; result checkpoint `0a6ce8cd-0916-4f19-82af-84d991b82526`
- Effect: candidate 125.2 minus naive 168.9 = -43.69, 95% bootstrap interval [-76.55, -18.99] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 168.9 over 5 runs; repeats: 162.1, 150.6, 195.6, 198.6, 168.9
- Spread: range 150.6 to 198.6, noise band ±36.69 (2 x MAD), CV 12.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +42.0% (noise band ±30.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +37.7% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +43.5% (it comes back)
- PASS · Held-out claim: C2: -22.5% to -67.3% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=12`: no evidence mentions '12'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=linear`: no evidence mentions 'linear'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -43.69 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `theta_bins=60`, `eps_end=0.981`: this claim +3.2%, mean |gap| 9.6% (5 runs)
  - `theta_bins=12`: this claim +43.5%, mean |gap| 26.1% (6 runs)
  - `theta_bins=60`, `eps_end=0.525`: this claim +2.4%, mean |gap| 27.8% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=linear, theta_bins=12` (reported)
- `eps_end=0.981, theta_bins=60`
- `eps_end=0.525, theta_bins=60`

### History matching (every measured configuration, all claims together)
- 36 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, theta_bins`: eps_end=0.981, theta_bins=60 (max I 0.29); eps_end=0.905, theta_bins=60 (max I 0.75); eps_end=0.1, theta_bins=1 (max I 0.8); eps_end=0.525, theta_bins=60 (max I 0.89); +2 more
  - `lr_schedule, theta_bins`: lr_schedule=linear, theta_bins=12 (max I 0.81); lr_schedule=inv, theta_bins=1 (max I 1.19)
  - `lr_schedule`: lr_schedule=inv (max I 1.04)
  - `theta_bins`: theta_bins=30 (max I 1.21)
- Equally good values: `lr_schedule` in {inv, linear}

Notes:
- configurations the target claim can't tell apart from the answer: lr_schedule=linear, theta_bins=12; eps_end=0.981, theta_bins=60; eps_end=0.525, theta_bins=60
- equally good values within one noise band (measured): lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `theta_bins=60`, `eps_end=0.981` | 5 | +3.2% | -15.9% | 9.6% |
| `theta_bins=12` | 6 | +43.5% | +8.7% | 26.1% |
| `theta_bins=60`, `eps_end=0.525` | 5 | +2.4% | -53.2% | 27.8% |
| naive (reproduction as run) | 5 | +42.0% | -22.5% | 32.3% |
| `lr_schedule=inv`, `eps_end=0.1` | 5 | +17.4% | -48.8% | 33.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
