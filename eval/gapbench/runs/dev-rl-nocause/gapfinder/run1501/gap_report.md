# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 19:10 · 127 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +42.9% | +18.7% | ±22.8% | `lr_schedule=inv` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +42.9% → +18.7% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0026`, `B0124`, `B0125`, `B0126`, `B0127` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `d524f385-5863-4af9-856f-92701d9f9505` and run
  ```
  RUN_TAG=c6d86c33f9af "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 143.5, 82.08, 133, 141.1, 152.1; gap after +18.7%; result checkpoint `5be8e25a-e345-46eb-bc94-0f857489b9e5`
- Effect: candidate 141.1 minus naive 169.9 = -28.75, 95% bootstrap interval [-91.2, -14.9] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 169.9 over 5 runs; repeats: 156.3, 193.6, 158.5, 169.9, 192.9
- Spread: range 156.3 to 193.6, noise band ±27.17 (2 x MAD), CV 10.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +42.9% (noise band ±22.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +42.9% (it comes back)
- PASS · Held-out claim: C2: +25.5% to -66.6% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -28.75 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=30` (1.68 noise units, gap -4.5%); `theta_bins=12` (1.02 noise units, gap +19.6%)
- Near alternatives (closest across all claims):
  - `theta_bins=12`: this claim +47.7%, mean |gap| 27.5% (6 runs)
  - `eps_end=0.025`, `lr_schedule=inv`: this claim +23.9%, mean |gap| 27.6% (5 runs)
  - `theta_bins=4`, `lr_schedule=inv`: this claim +19.5%, mean |gap| 28.2% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=inv` (reported)
- `eps_end=0.001, lr_schedule=inv`
- `lr_schedule=inv, theta_bins=4`

### History matching (every measured configuration, all claims together)
- 32 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, lr_schedule`: eps_end=0.001, lr_schedule=inv (max I 0.84); eps_end=0.025, lr_schedule=linear (max I 1.87)
  - `lr_schedule`: lr_schedule=inv (max I 0.87); lr_schedule=linear (max I 1.83)
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=4 (max I 1.16); lr_schedule=linear, theta_bins=12 (max I 1.43); lr_schedule=inv, theta_bins=12 (max I 1.61)
  - `eps_end, theta_bins`: eps_end=0.001, theta_bins=12 (max I 1.2); eps_end=0.025, theta_bins=12 (max I 1.76)
  - `eps_end`: eps_end=0.1 (max I 1.39)
- Equally good values: `lr_schedule` in {inv, linear}

Notes:
- theta_bins dropped: with repeats, {'theta_bins': '4', 'lr_schedule': 'inv'} fits {'lr_schedule': 'inv'}'s gap by less than one noise band, so it is not needed
- configurations the target claim can't tell apart from the answer: lr_schedule=inv; eps_end=0.001, lr_schedule=inv; lr_schedule=inv, theta_bins=4
- equally good values within one noise band (measured): lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `theta_bins=12` | 6 | +47.7% | +7.4% | 27.5% |
| `eps_end=0.025`, `lr_schedule=inv` | 5 | +23.9% | -31.2% | 27.6% |
| `theta_bins=4`, `lr_schedule=inv` | 5 | +19.5% | -36.8% | 28.2% |
| `lr_schedule=inv`, `eps_end=0.001` | 5 | +7.1% | -53.7% | 30.4% |
| naive (reproduction as run) | 5 | +42.9% | +25.5% | 34.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
