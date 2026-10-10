# Gap Report: test-gen-02

Artifact `rlbench` · generated 2026-10-10 23:13 · 26 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +210.6% | +63.6% | ±22.9% | `lr=0.05`, `lr_schedule=inv` |

## C1: mean_reward (paper 59.35)
**Fits but unsupported** · gap +210.6% → +63.6% · 9 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0018`, `B0021`, `B0022` (3 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `0.05`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `1eb45b71-7f21-4829-b3de-23fdb0f4209f` and run
  ```
  RUN_TAG=12d3fd0a84c2 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.05 --lr_schedule inv --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 97.11, 100.2, 92.5; gap after +63.6%; result checkpoint `cd9ca4f2-8c14-4b4c-8b67-68bd4677f268`
- Effect: candidate 97.11 minus naive 184.3 = -87.21, 95% bootstrap interval [-97.01, -82.08] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 59.4 on CartPole; the worst of its seeds reaches 9.8.

- p. 1; value used: `mean_reward` = 59.35 reward (headline claim)

### What did we measure?
- Naive median 184.3 over 5 runs; repeats: 194.8, 177.5, 179.5, 184.3, 194.3
- Spread: range 177.5 to 194.8, noise band ±13.6 (2 x MAD), CV 4.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +210.6% (noise band ±22.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +140.4% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +116.4% (it comes back)
- PASS · Held-out claim: C2: +1258.4% to +41.1% (not worse beyond noise)
- FAIL · Evidence: `lr=0.05`: no evidence mentions '0.05'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -87.21 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `--eps_start`, `RL_SEED_BASE`, `RUN_TAG`, `CartPole physics constants (g, mc, mp, l, f, dt)`, `discretization theta clamp bounds`, `discretization omega clamp bounds`, `done condition: x threshold`, `done condition: theta threshold`, `reward per step (hardcoded)`, `initial state distribution (reset)`, `discretization formula`, `force magnitude (f)`, `gravity (g)`, `pole length (l)`, `cart mass (mc)`, `pole mass (mp)`, `time step (dt)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `init_q=1.0` (2.95 noise units, gap +142.9%)
- Near alternatives (closest across all claims):
  - `lr=0.05`, `init_q=1.0`: this claim +89.5%, mean |gap| 57.5% (3 runs)
  - `lr=0.05`: this claim +116.4%, mean |gap| 92.7% (3 runs)
  - `init_q=1.0`, `lr_schedule=inv`: this claim +142.8%, mean |gap| 280.0% (3 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=0.05`, `lr_schedule=inv` | 3 | +63.6% | +41.1% | 52.4% |
| `lr=0.05`, `init_q=1.0` | 3 | +89.5% | +25.4% | 57.5% |
| `lr=0.05` | 3 | +116.4% | +69.0% | 92.7% |
| `init_q=1.0`, `lr_schedule=inv` | 3 | +142.8% | +417.3% | 280.0% |
| `lr_schedule=inv` | 3 | +140.4% | +443.7% | 292.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--eps_start`, `RL_SEED_BASE`, `RUN_TAG`, `CartPole physics constants (g, mc, mp, l, f, dt)`, `discretization theta clamp bounds`, `discretization omega clamp bounds`, `done condition: x threshold`, `done condition: theta threshold`, `reward per step (hardcoded)`, `initial state distribution (reset)`, `discretization formula`, `force magnitude (f)`, `gravity (g)`, `pole length (l)`, `cart mass (mc)`, `pole mass (mp)`, `time step (dt)`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `16ad3c4a71eefac5fc45f4c9a201b3fc6f51a0c3cef30e8c3ea67682f56fab21`
- Cost: Nemotron billed $0.0383, sandbox reported $0.0000 (total $0.0383; this search; ledger extraction is included only if it shared the search's router)
