# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-14 00:28 · 51 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -40.1% | +4.6% | ±0.6% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -40.1% → +4.6% · 12 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0014`, `B0015`, `B0016`, `B0017`, `B0018` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `f663469d-37e6-41d8-95c3-fcbd33d17a57` and run
  ```
  RUN_TAG=890d445a8614 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 305, 327.2, 247.6, 284, 327.2, 347; gap after +4.6%; result checkpoint `11cb8382-e27c-4894-89a4-9aa142455b2a`
- Effect: candidate 316.1 minus naive 180.9 = +135.2, 95% bootstrap interval [+77.99, +160.8] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 180.9 over 5 runs; repeats: 198.5, 181.1, 180.2, 180.9, 170.6
- Spread: range 170.6 to 198.5, noise band ±1.809 (2 x MAD), CV 5.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -40.1% (noise band ±0.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -40.1% (it comes back)
- PASS · Held-out claim: C2: +69.3% to +6.3% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +135.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (51.64 noise units, gap -9.2%); `max_steps=2000` (44.83 noise units, gap +13.3%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim +8.4%, mean |gap| 4.9% (6 runs)
  - `max_steps=2000`: this claim +21.6%, mean |gap| 39.2% (6 runs)
  - `max_steps=100`: this claim -67.6%, mean |gap| 69.1% (6 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 6 | +8.4% | -1.4% | 4.9% |
| `max_steps=500` | 6 | +4.6% | +6.3% | 5.5% |
| `max_steps=2000` | 6 | +21.6% | -56.8% | 39.2% |
| naive (reproduction as run) | 5 | -40.1% | +69.3% | 54.7% |
| `max_steps=100` | 6 | -67.6% | +70.7% | 69.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`

## Provenance
- GapFinder commit: `ab5d0e01d517ea012f76706719410d70d422f3f9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fedcbdf1b57461a1273eeb81ccb09c30931e58de34a306249ffd0422bbf51ae6`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
