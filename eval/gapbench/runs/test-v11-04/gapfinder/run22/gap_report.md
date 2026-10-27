# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 21:13 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +99.8% | +2.7% | ±21.4% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +99.8% → +2.7% · 57 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0033`, `B0133`, `B0134`, `B0135`, `B0136`, `B0137` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `6c772077-5c72-4c12-ac1c-13150d83f2da` and run
  ```
  RUN_TAG=ff9395e7d5cd "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 98.72, 98.84, 96.28, 99.75, 93.81, 95.52; gap after +2.7%; result checkpoint `45599271-e6da-4803-9986-ae36ad92eeba`
- Effect: candidate 97.5 minus naive 189.7 = -92.16, 95% bootstrap interval [-103.6, -77.85] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 189.7 over 5 runs; repeats: 179.5, 200, 198.6, 172.5, 189.7
- Spread: range 172.5 to 200, noise band ±20.28 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +99.8% (noise band ±21.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +99.8% (it comes back)
- PASS · Held-out claim: C2: +160.5% to +21.9% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -92.16 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=1` (4.62 noise units, gap -1.0%); `eps_start=0.2` (4.55 noise units, gap -2.7%); `lr=0.01` (4.15 noise units, gap -11.2%); `lr=0.02` (4.12 noise units, gap +11.7%); `lr=0.05` (3.53 noise units, gap +24.3%) (and 10 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=0.05`: this claim +23.0%, mean |gap| 29.4% (6 runs)
  - `lr=1`, `eps_start=0.2`: this claim +3.0%, mean |gap| 39.5% (5 runs)
  - `lr_schedule=inv`: this claim +31.0%, mean |gap| 40.3% (6 runs)

### History matching (every measured configuration, all claims together)
- 15 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=inv, max_steps=100 (max I 0.17); lr_schedule=linear, max_steps=100 (max I 0.37)
  - `max_steps`: max_steps=100 (max I 0.3)
  - `eps_start, lr`: eps_start=0.2, lr=1 (max I 1.05); eps_start=0.5, lr=1 (max I 1.13)
  - `lr`: lr=0.02 (max I 1.11); lr=1 (max I 1.46); lr=0.01 (max I 1.58)
  - `lr, lr_schedule`: lr=0.01, lr_schedule=linear (max I 1.3)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.91)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr': '0.01', 'eps_start': '0.5'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +2.7% | +21.9% | 12.3% |
| `lr=0.05` | 6 | +23.0% | -35.8% | 29.4% |
| `lr=1`, `eps_start=0.2` | 5 | +3.0% | -75.9% | 39.5% |
| `lr_schedule=inv` | 6 | +31.0% | -49.6% | 40.3% |
| `lr=0.02` | 6 | +3.5% | -80.2% | 41.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `958fafed572bbbf30aedd8af86ba04a1fefc05c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
