# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-14 00:27 · 47 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -40.9% | +8.1% | ±7.3% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -40.9% → +8.1% · 12 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0014`, `B0015`, `B0016`, `B0017`, `B0018` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `fc1fd7c2-90fb-4ca3-9f83-aa90f351407d` and run
  ```
  RUN_TAG=bc6be46524a7 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 354.1, 287.6, 336.4, 316.4, 299.8, 378.9; gap after +8.1%; result checkpoint `454042be-50ff-49e3-ae94-0c5b764765c3`
- Effect: candidate 326.4 minus naive 178.5 = +147.9, 95% bootstrap interval [+111.1, +191.5] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 178.5 over 5 runs; repeats: 189.4, 177.5, 193.6, 178.5, 149.1
- Spread: range 149.1 to 193.6, noise band ±21.93 (2 x MAD), CV 9.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -40.9% (noise band ±7.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -40.9% (it comes back)
- PASS · Held-out claim: C2: +55.2% to +27.9% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +147.9 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=2000` (1.74 noise units, gap +28.3%)
- Near alternatives (closest across all claims):
  - `max_steps=2000`: this claim +27.4%, mean |gap| 15.2% (6 runs)
  - `max_steps=1000`: this claim +35.7%, mean |gap| 18.4% (6 runs)
  - `max_steps=100`: this claim -68.0%, mean |gap| 55.5% (6 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=2000` | 6 | +27.4% | +3.0% | 15.2% |
| `max_steps=500` | 6 | +8.1% | +27.9% | 18.0% |
| `max_steps=1000` | 6 | +35.7% | -1.1% | 18.4% |
| naive (reproduction as run) | 5 | -40.9% | +55.2% | 48.1% |
| `max_steps=100` | 6 | -68.0% | +43.1% | 55.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `ab5d0e01d517ea012f76706719410d70d422f3f9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fedcbdf1b57461a1273eeb81ccb09c30931e58de34a306249ffd0422bbf51ae6`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
