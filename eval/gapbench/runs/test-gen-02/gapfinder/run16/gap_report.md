# Gap Report: test-gen-02

Artifact `rlbench` · generated 2026-10-14 00:52 · 24 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +209.9% | +104.3% | ±29.3% | `lr_schedule=inv`, `reward_norm=on` |

## C1: mean_reward (paper 59.35)
**Fits but unsupported** · gap +209.9% → +104.3% · 5 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0019`, `B0021`, `B0022`, `B0023`, `B0024` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Config: `reward_norm` naive `off`, changed to `on`
- Command:

  Replay: fork checkpoint `808b61db-67f3-42c1-9b47-7d7c5b57d469` and run
  ```
  RUN_TAG=643c1de72ab6 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm on --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 108.7, 130.7, 121.2, 111.7, 135.9; gap after +104.3%; result checkpoint `0962cf37-fa97-42ed-aa8e-b8e9ef71098d`
- Effect: candidate 121.2 minus naive 183.9 = -62.67, 95% bootstrap interval [-75.13, -37.18] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 59.4 on CartPole; the worst of its seeds reaches 9.8.

- p. 1; value used: `mean_reward` = 59.35 reward (headline claim)

### What did we measure?
- Naive median 183.9 over 5 runs; repeats: 194.9, 176.9, 192.6, 183.9, 151.8
- Spread: range 151.8 to 194.9, noise band ±17.38 (2 x MAD), CV 9.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +209.9% (noise band ±29.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +234.2% (it comes back)
- FAIL · Counterfactual (reversal test): without `reward_norm` the gap is +118.6% (it did NOT come back)
- PASS · Held-out claim: C2: +872.6% to +224.9% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- FAIL · Evidence: `reward_norm=on`: no evidence mentions 'on'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -62.67 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `eps_start`, `hardware_cpu`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (1.24 noise units, gap +173.5%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +118.6%, mean |gap| 205.9% (6 runs)
  - `lr_schedule=linear`: this claim +175.4%, mean |gap| 771.8% (6 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, among 5 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `reward_norm=on` | 5 | +104.3% | +224.9% | 164.6% |
| `lr_schedule=inv` | 6 | +118.6% | +293.1% | 205.9% |
| naive (reproduction as run) | 5 | +209.9% | +872.6% | 541.2% |
| `lr_schedule=linear` | 6 | +175.4% | +1368.3% | 771.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `eps_start`, `hardware_cpu`

## Provenance
- GapFinder commit: `e89cebde86417c8c65704c51b94620ddb20a97ce` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `e323442c06dc23e2a59acc0ba37f900485ab760e6844bc4ffbd19ace981376ca`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
