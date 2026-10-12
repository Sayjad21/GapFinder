# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-12 23:51 · 22 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +958.5% | +8.4% | ±127.9% | `eps_start=0.1`, `lr_schedule=inv` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +958.5% → +8.4% · 5 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0018`, `B0019`, `B0020`, `B0021`, `B0022` (5 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `bb3b04aa-f7e0-4937-aa78-9283bfbc7383` and run
  ```
  RUN_TAG=f4ad57da16dc "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 22.27, 10.45, 17.16, 18.77, 22.62; gap after +8.4%; result checkpoint `43c847ab-57c9-4c18-876e-e7267ab6726a`
- Effect: candidate 18.77 minus naive 183.2 = -164.5, 95% bootstrap interval [-177.5, -155.1] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> Figure 1 (final evaluation): mean reward 17.3; worst seed 9.1.

- p. 1, Figure 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 183.2 over 5 runs; repeats: 200, 164.9, 183.2, 194.3, 182.1
- Spread: range 164.9 to 200, noise band ±22.14 (2 x MAD), CV 7.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +958.5% (noise band ±127.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +622.6% (it comes back)
- FAIL · Counterfactual (reversal test): without `lr_schedule` the gap is +93.4% (it did NOT come back)
- PASS · Held-out claim: C2: +1358.8% to -0.5% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -164.5 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `eps_start=0.1`: this claim +93.4%, mean |gap| 47.0% (5 runs)
  - `lr_schedule=inv`: this claim +622.6%, mean |gap| 452.5% (5 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.1`, `lr_schedule=inv` | 5 | +8.4% | -0.5% | 4.5% |
| `eps_start=0.1` | 5 | +93.4% | +0.5% | 47.0% |
| `lr_schedule=inv` | 5 | +622.6% | +282.4% | 452.5% |
| naive (reproduction as run) | 5 | +958.5% | +1358.8% | 1158.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0468, sandbox reported $0.0000 (total $0.0468; this search; ledger extraction is included only if it shared the search's router)
