# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-15 20:54 · 91 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -40.0% | +4.3% | ±3.3% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -40.0% → +4.3% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0041`, `B0042`, `B0043` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `7ae49f33-4879-430e-963f-8e9517e71fd4` and run
  ```
  RUN_TAG=daadda668b55 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 315.3, 315, 233.6, 214.3, 346.4, 318.3; gap after +4.3%; result checkpoint `8bbf3b8b-d057-4d89-8c41-4c44b5d2c8af`
- Effect: candidate 315.2 minus naive 181.3 = +133.8, 95% bootstrap interval [+37.86, +158.6] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 181.3 over 5 runs; repeats: 185.7, 167.2, 176.3, 181.3, 195.7
- Spread: range 167.2 to 195.7, noise band ±10.09 (2 x MAD), CV 5.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -40.0% (noise band ±3.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -40.0% (it comes back)
- PASS · Held-out claim: C2: +163.9% to +1.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +133.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (11.01 noise units, gap -3.2%); `max_steps=2000` (8.04 noise units, gap -13.1%); `max_steps=10000` (5.19 noise units, gap -22.6%); `max_steps=1000` (4.18 noise units, gap +26.0%)
- Near alternatives (closest across all claims):
  - `max_steps=400`: this claim -6.6%, mean |gap| 13.8% (6 runs)
  - `max_steps=10000`: this claim +0.4%, mean |gap| 14.0% (6 runs)
  - `max_steps=1000`: this claim +16.2%, mean |gap| 24.5% (6 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=500` (reported)
- `max_steps=400`
- `max_steps=1000`
- `max_steps=10000`
- `max_steps=2000`

### History matching (every measured configuration, all claims together)
- 4 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `max_steps`: max_steps=500 (max I 0.7); max_steps=400 (max I 0.78); max_steps=1000 (max I 2.65)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=2000 (max I 1.8)
- 2 separate islands (no single-knob move joins them): max_steps=500; max_steps=400; max_steps=1000 | lr_schedule=linear, max_steps=2000
- Equally good values: `max_steps` in {400, 500, 10000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=500; max_steps=400; max_steps=1000; max_steps=10000; max_steps=2000
- equally good values within one noise band (measured): max_steps in {400, 500, 10000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 6 | +4.3% | +1.6% | 2.9% |
| `max_steps=400` | 6 | -6.6% | -21.1% | 13.8% |
| `max_steps=10000` | 6 | +0.4% | -27.7% | 14.0% |
| `max_steps=1000` | 6 | +16.2% | -32.7% | 24.5% |
| `max_steps=2000`, `lr_schedule=linear` | 5 | -5.0% | +46.6% | 25.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
