# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-15 20:54 · 99 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -40.0% | +1.5% | ±7.0% | `max_steps=400` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -40.0% → +1.5% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0014`, `B0030`, `B0031`, `B0041`, `B0042`, `B0043` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Command:

  Replay: fork checkpoint `bd4b5835-fc94-4792-9031-39025f7acb55` and run
  ```
  RUN_TAG=76aa7cd143e1 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 298, 264.1, 254.3, 314.9, 332.6, 315.2; gap after +1.5%; result checkpoint `04f8a506-4740-483a-99d5-236403b845c8`
- Effect: candidate 306.5 minus naive 181.4 = +125.1, 95% bootstrap interval [+80.75, +159.8] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 181.4 over 5 runs; repeats: 182.5, 181.4, 156.1, 191.9, 162.8
- Spread: range 156.1 to 191.9, noise band ±21.05 (2 x MAD), CV 8.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -40.0% (noise band ±7.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -40.0% (it comes back)
- PASS · Held-out claim: C2: +5.2% to -5.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +125.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=10000` (5.45 noise units, gap -2.0%); `max_steps=500` (3.3 noise units, gap -17.0%)
- Near alternatives (closest across all claims):
  - `max_steps=2000`: this claim +4.7%, mean |gap| 6.3% (6 runs)
  - `max_steps=500`: this claim -17.5%, mean |gap| 10.6% (6 runs)
  - `max_steps=10000`: this claim +16.1%, mean |gap| 21.0% (6 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=400` (reported)
- `max_steps=500`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=400 (max I 0.32); max_steps=500 (max I 2.23); max_steps=2000 (max I 2.78)
- Equally good values: `max_steps` in {400, 2000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=400; max_steps=500
- equally good values within one noise band (measured): max_steps in {400, 2000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=400` | 6 | +1.5% | -5.0% | 3.2% |
| `max_steps=2000` | 6 | +4.7% | -8.0% | 6.3% |
| `max_steps=500` | 6 | -17.5% | +3.7% | 10.6% |
| `max_steps=10000` | 6 | +16.1% | -26.0% | 21.0% |
| naive (reproduction as run) | 5 | -40.0% | +5.2% | 22.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
