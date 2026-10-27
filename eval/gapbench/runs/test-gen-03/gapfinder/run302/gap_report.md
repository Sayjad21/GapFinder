# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-14 21:42 · 99 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -42.8% | +0.8% | ±9.2% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -42.8% → +0.8% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0020`, `B0021`, `B0022` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `6b54de6a-61a9-4e10-8ac3-f3e62f2f3a00` and run
  ```
  RUN_TAG=f973d5cfa97c "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 267.2, 289.7, 350.8, 319.5, 296.3, 312.5; gap after +0.8%; result checkpoint `02a75086-d9a2-4ad1-97d9-8b634de5d322`
- Effect: candidate 304.4 minus naive 172.9 = +131.5, 95% bootstrap interval [+118.1, +183.7] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 172.9 over 5 runs; repeats: 140.9, 155.5, 175, 186.8, 172.9
- Spread: range 140.9 to 186.8, noise band ±27.69 (2 x MAD), CV 10.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -42.8% (noise band ±9.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -42.8% (it comes back)
- PASS · Held-out claim: C2: +1.3% to +5.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +131.5 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (4.54 noise units, gap -1.2%); `max_steps=2000` (2.6 noise units, gap -19.0%); `max_steps=1000` (2.12 noise units, gap +23.3%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim +16.2%, mean |gap| 10.2% (6 runs)
  - `max_steps=2000`: this claim +39.5%, mean |gap| 33.6% (6 runs)
  - `max_steps=10000`: this claim +63.0%, mean |gap| 35.6% (6 runs)

### History matching (every measured configuration, all claims together)
- 2 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 2 configurations
  - `max_steps`: max_steps=500 (max I 0.24); max_steps=400 (max I 1.8)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 6 | +0.8% | +5.0% | 2.9% |
| `max_steps=1000` | 6 | +16.2% | -4.1% | 10.2% |
| naive (reproduction as run) | 5 | -42.8% | +1.3% | 22.1% |
| `max_steps=2000` | 6 | +39.5% | -27.8% | 33.6% |
| `max_steps=10000` | 6 | +63.0% | -8.2% | 35.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
