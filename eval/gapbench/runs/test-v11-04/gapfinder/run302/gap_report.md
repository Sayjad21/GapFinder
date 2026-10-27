# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 21:47 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +83.3% | +1.4% | ±19.4% | `lr=1` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +83.3% → +1.4% · 57 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0019`, `B0098`, `B0099`, `B0100`, `B0101`, `B0102` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `1`
- Command:

  Replay: fork checkpoint `e9347c46-9b29-45b7-922f-5e67ff166ec7` and run
  ```
  RUN_TAG=822bc84e4c15 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 88.16, 132.7, 69.29, 68.05, 130.7, 104.4; gap after +1.4%; result checkpoint `aea0843e-f105-4161-9e01-859b3e5903b2`
- Effect: candidate 96.26 minus naive 174 = -77.72, 95% bootstrap interval [-115, -43.21] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 174 over 5 runs; repeats: 164.8, 174, 172, 195.2, 188.9
- Spread: range 164.8 to 195.2, noise band ±18.39 (2 x MAD), CV 7.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +83.3% (noise band ±19.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +83.3% (it comes back)
- PASS · Held-out claim: C2: +67.0% to -80.2% (not worse beyond noise)
- FAIL · Evidence: `lr=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -77.72 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (4.28 noise units, gap -0.4%); `lr=0.02` (3.55 noise units, gap +14.5%); `lr=0.5` (3.53 noise units, gap -14.8%); `lr=0.01` (3.42 noise units, gap -17.0%); `eps_start=0.2` (3.09 noise units, gap +23.4%) (and 8 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim +3.5%, mean |gap| 21.1% (6 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -9.5%, mean |gap| 28.2% (5 runs)
  - `eps_start=0.5`, `lr_schedule=inv`, `lr=1`, `max_steps=100`: this claim +5.3%, mean |gap| 30.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 22 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=100 (max I 0.53)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.53); lr_schedule=inv, max_steps=100 (max I 0.92)
  - `eps_start, lr`: eps_start=0.5, lr=1 (max I 0.87)
  - `lr, max_steps`: lr=0.02, max_steps=1000 (max I 0.88)
  - `eps_start, max_steps`: eps_start=0.2, max_steps=1000 (max I 0.9); eps_start=0.5, max_steps=1000 (max I 0.9)
  - `eps_start, lr, lr_schedule, max_steps`: eps_start=0.5, lr=1, lr_schedule=inv, max_steps=100 (max I 1.03)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=inv (max I 1.09); eps_start=0.5, lr_schedule=linear (max I 1.1)
- 3 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; eps_start=0.5, lr=1 | eps_start=0.5, lr_schedule=inv; eps_start=0.5, lr_schedule=linear | eps_start=0.5, lr=1, lr_schedule=inv, max_steps=100

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '1000', 'lr': '1'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +3.5% | +38.7% | 21.1% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -9.5% | -47.0% | 28.2% |
| `eps_start=0.5`, `lr_schedule=inv`, `lr=1`, `max_steps=100` | 5 | +5.3% | +56.5% | 30.9% |
| `eps_start=0.5`, `max_steps=100` | 5 | -18.8% | -46.6% | 32.7% |
| `lr=1` | 6 | +1.4% | -80.2% | 40.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
