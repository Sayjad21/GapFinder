# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 21:01 · 93 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +71.6% | -1.3% | ±34.7% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +71.6% → -1.3% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0016`, `B0033`, `B0034`, `B0035`, `B0036`, `B0037` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `bddbfef1-549e-4ca6-9b37-5fa880a1e5ba` and run
  ```
  RUN_TAG=0e80777d0ca4 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.7, 93.58, 93.18, 93.78, 99.56, 90.2; gap after -1.3%; result checkpoint `0a821fc5-a57b-4d0d-8912-f01241c81ced`
- Effect: candidate 93.68 minus naive 162.9 = -69.26, 95% bootstrap interval [-92.46, -58.92] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 (headline claim)

### What did we measure?
- Naive median 162.9 over 5 runs; repeats: 194.1, 162.9, 146.5, 161.1, 184.9
- Spread: range 146.5 to 194.1, noise band ±32.94 (2 x MAD), CV 11.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +71.6% (noise band ±34.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +71.6% (it comes back)
- PASS · Held-out claim: C2: -31.6% to -13.3% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -69.26 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.1` (1.06 noise units, gap -34.8%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -1.0%, mean |gap| 1.6% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -9.1%, mean |gap| 19.6% (5 runs)
  - `eps_start=0.5`, `max_steps=100`: this claim -15.6%, mean |gap| 45.9% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`
- `eps_start=0.5, lr_schedule=linear`

### History matching (every measured configuration, all claims together)
- 13 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=100 (max I 0.01); max_steps=40 (max I 2.58)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.05); lr_schedule=inv, max_steps=100 (max I 0.58); lr_schedule=linear, max_steps=40 (max I 2.52)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.23)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.32); eps_start=0.5, lr_schedule=inv (max I 1.61)
  - `eps_start`: eps_start=0.2 (max I 1.81)
  - `lr_schedule`: lr_schedule=inv (max I 2.05)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100; eps_start=0.5, lr_schedule=linear

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | -1.0% | +2.1% | 1.6% |
| `max_steps=100` | 6 | -1.3% | -13.3% | 7.3% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -9.1% | -30.2% | 19.6% |
| `eps_start=0.5`, `max_steps=100` | 5 | -15.6% | -76.2% | 45.9% |
| `eps_start=0.5`, `lr_schedule=linear` | 5 | -9.2% | -84.0% | 46.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
