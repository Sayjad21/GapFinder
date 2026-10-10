# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-10 23:40 · 14 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -41.8% | -0.8% | ±1.5% | `max_steps=1000` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -41.8% → -0.8% · 5 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0012`, `B0013` (3 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `dbc4a5b7-91f7-4650-9d97-a8f199f524ae` and run
  ```
  RUN_TAG=d74a00030ea3 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 299.6, 299.3, 341.9; gap after -0.8%; result checkpoint `8e6a0b2c-1dcd-47a1-becf-e65ba682a455`
- Effect: candidate 299.6 minus naive 175.9 = +123.7, 95% bootstrap interval [+118.2, +163.5] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1, Figure 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 175.9 over 5 runs; repeats: 175.9, 175.9, 178.1, 188.2, 165.4
- Spread: range 165.4 to 188.2, noise band ±4.38 (2 x MAD), CV 4.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -41.8% (noise band ±1.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -41.8% (it comes back)
- PASS · Held-out claim: C2: +12.7% to +3.9% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +123.7 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (12.13 noise units, gap -24.2%)
- Near alternatives (closest across all claims):
  - `max_steps=500`: this claim +19.1%, mean |gap| 32.0% (3 runs)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 3 | -0.8% | +3.9% | 2.4% |
| naive (reproduction as run) | 5 | -41.8% | +12.7% | 27.3% |
| `max_steps=500` | 3 | +19.1% | +45.0% | 32.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.1318, sandbox reported $0.0000 (total $0.1318; this search; ledger extraction is included only if it shared the search's router)
