# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-12 22:23 · 30 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +1032.1% | +383.4% | ±26.3% | `lr_schedule=inv`, `eps_start=0.5` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +1032.1% → +383.4% · 5 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0026`, `B0027`, `B0028`, `B0029`, `B0030` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Config: `eps_start` naive `1.0`, changed to `0.5`
- Command:

  Replay: fork checkpoint `d17286ae-147d-43fc-8dfe-2338c47cfb21` and run
  ```
  RUN_TAG=79fc592c6320 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 0.5 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 83.69, 31.38, 102, 88.02, 76.72; gap after +383.4%; result checkpoint `3e5616b2-86f0-4556-86ce-0b3c26c64b06`
- Effect: candidate 83.69 minus naive 196 = -112.3, 95% bootstrap interval [-137.7, -88.69] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 196 over 5 runs; repeats: 198.2, 197.6, 196, 159.1, 192.1
- Spread: range 159.1 to 198.2, noise band ±4.55 (2 x MAD), CV 8.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +1032.1% (noise band ±26.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +658.8% (it comes back)
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +607.4% (it comes back)
- PASS · Held-out claim: C2: +1865.4% to +8.2% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- FAIL · Evidence: `eps_start=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -112.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.8` (8.66 noise units, gap +804.5%); `lr_schedule=linear` (7.12 noise units, gap +845.0%)
- Near alternatives (closest across all claims):
  - `eps_start=0.5`: this claim +658.8%, mean |gap| 401.6% (5 runs)
  - `lr_schedule=inv`: this claim +607.4%, mean |gap| 486.6% (5 runs)
  - `eps_start=0.8`: this claim +838.1%, mean |gap| 636.6% (5 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_start=0.5` | 5 | +383.4% | +8.2% | 195.8% |
| `eps_start=0.5` | 5 | +658.8% | +144.5% | 401.6% |
| `lr_schedule=inv` | 5 | +607.4% | +365.9% | 486.6% |
| `eps_start=0.8` | 5 | +838.1% | +435.2% | 636.6% |
| `lr_schedule=linear` | 5 | +885.8% | +1467.0% | 1176.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`

## Provenance
- GapFinder commit: `56779a9cc2cef642dbf91ede59da97a848c305cd` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0444, sandbox reported $0.0000 (total $0.0444; this search; ledger extraction is included only if it shared the search's router)
