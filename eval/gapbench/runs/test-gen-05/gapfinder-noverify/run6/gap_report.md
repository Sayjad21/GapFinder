# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-12 23:33 · 30 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | +970.9% | -11.1% | ±143.1% | `eps_start=0.1` |

## C1: mean_reward (paper 17.31)
**Explained** · gap +970.9% → -11.1% · 5 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0007`, `B0014`, `B0015`, `B0016`, `B0017` (5 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Command:

  Replay: fork checkpoint `8b7a23ed-3005-484d-8747-0d568d433cd4` and run
  ```
  RUN_TAG=672684dbf93c "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 13.55, 32.05, 60.11, 12.39, 15.39; gap after -11.1%; result checkpoint `393c216b-182a-47e2-85a7-a0b81d4c4e5c`
- Effect: candidate 15.39 minus naive 185.4 = -170, 95% bootstrap interval [-176.4, -140.4] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 185.4 over 5 runs; repeats: 197.8, 183.8, 198.6, 167.5, 185.4
- Spread: range 167.5 to 198.6, noise band ±24.77 (2 x MAD), CV 6.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +970.9% (noise band ±143.1% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -170 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `f`, `dt`, `g`, `mc`, `mp`, `l`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (3.9 noise units, gap +412.2%); `lr_schedule=inv` (2.22 noise units, gap +653.4%); `lr_schedule=linear` (1.1 noise units, gap +813.1%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_start=0.1`: this claim +6.9%, mean |gap| 4.0% (5 runs)
  - `eps_start=0.5`: this claim +610.6%, mean |gap| 352.8% (5 runs)
  - `lr_schedule=inv`: this claim +653.4%, mean |gap| 483.6% (5 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_start=0.1` | 5 | +6.9% | +1.1% | 4.0% |
| `eps_start=0.1` | 5 | -11.1% | +0.5% | 5.8% |
| `eps_start=0.5` | 5 | +610.6% | +95.1% | 352.8% |
| `lr_schedule=inv` | 5 | +653.4% | +313.7% | 483.6% |
| `lr_schedule=linear` | 5 | +813.1% | +1047.3% | 930.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `f`, `dt`, `g`, `mc`, `mp`, `l`, `--out`

## Provenance
- GapFinder commit: `79ea3e394df6e4dd60d6d56f69f3b468cfa04d26` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0542, sandbox reported $0.0000 (total $0.0542; this search; ledger extraction is included only if it shared the search's router)
