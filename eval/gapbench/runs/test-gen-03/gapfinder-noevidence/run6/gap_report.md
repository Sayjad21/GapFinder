# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-13 00:06 · 22 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -43.5% | +7.9% | ±2.9% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -43.5% → +7.9% · 5 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0010`, `B0011`, `B0012`, `B0013` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `d85a2d32-78da-4dc9-ba46-143ff0c4d8cc` and run
  ```
  RUN_TAG=95b95158932a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 345.5, 393.5, 164.8, 325.9, 291; gap after +7.9%; result checkpoint `08121547-ec8d-4c4f-8781-d34875cbe3ff`
- Effect: candidate 325.9 minus naive 170.6 = +155.3, 95% bootstrap interval [+55.42, +188.3] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1, Figure 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 170.6 over 5 runs; repeats: 170.6, 166.2, 174.6, 164.3, 193.9
- Spread: range 164.3 to 193.9, noise band ±8.87 (2 x MAD), CV 6.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -43.5% (noise band ±2.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -43.5% (it comes back)
- PASS · Held-out claim: C2: +36.4% to +9.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +155.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `g`, `mc`, `mp`, `l`, `f`, `dt`, `RUN_TAG`, `RL_SEED_BASE`, `out`, `os`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim +45.5%, mean |gap| 26.2% (5 runs)
  - `lr_schedule=linear`, `max_steps=500`: this claim -30.7%, mean |gap| 114.6% (5 runs)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 5 | +7.9% | +9.6% | 8.8% |
| `max_steps=1000` | 5 | +45.5% | -6.8% | 26.2% |
| naive (reproduction as run) | 5 | -43.5% | +36.4% | 39.9% |
| `lr_schedule=linear`, `max_steps=500` | 5 | -30.7% | +198.4% | 114.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `g`, `mc`, `mp`, `l`, `f`, `dt`, `RUN_TAG`, `RL_SEED_BASE`, `out`, `os`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0488, sandbox reported $0.0000 (total $0.0488; this search; ledger extraction is included only if it shared the search's router)
