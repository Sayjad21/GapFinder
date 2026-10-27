# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-15 19:39 · 131 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +888.6% | +15.2% | ±65.2% | `eps_start=0.0` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +888.6% → +15.2% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0010`, `B0026`, `B0027`, `B0040`, `B0041`, `B0042` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.0`
- Command:

  Replay: fork checkpoint `8d78dc98-3059-41f1-803a-18bbc6eef094` and run
  ```
  RUN_TAG=d13bcd6f0710 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 9.75, 36.05, 15.85, 33.51, 9.98, 24.02; gap after +15.2%; result checkpoint `43e9e711-e112-44e5-a342-911492237143`
- Effect: candidate 19.94 minus naive 171.1 = -151.2, 95% bootstrap interval [-176.3, -136.1] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 171.1 over 5 runs; repeats: 165.5, 171.1, 169.5, 194.7, 195.3
- Spread: range 165.5 to 195.3, noise band ±11.28 (2 x MAD), CV 8.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +888.6% (noise band ±65.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +888.6% (it comes back)
- PASS · Held-out claim: C2: +737.4% to +0.3% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.0`: no evidence mentions '0.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -151.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.1` (13.05 noise units, gap +38.5%); `eps_start=0.02` (12.96 noise units, gap -43.9%); `eps_start=0.2` (8.02 noise units, gap +365.7%); `lr_schedule=inv` (2.92 noise units, gap +698.2%); `eps_start=0.5` (2.24 noise units, gap +742.7%)
- Near alternatives (closest across all claims):
  - `eps_start=0.02`: this claim -19.2%, mean |gap| 10.0% (6 runs)
  - `eps_start=0.02`, `lr_schedule=linear`: this claim -24.4%, mean |gap| 12.2% (5 runs)
  - `lr_schedule=inv`, `eps_start=0.1`: this claim +24.4%, mean |gap| 12.5% (5 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.0` (reported)
- `eps_start=0.02`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.1, lr_schedule=linear`

### History matching (every measured configuration, all claims together)
- 9 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `eps_start, lr_schedule`: eps_start=0.1, lr_schedule=linear (max I 0.24); eps_start=0.1, lr_schedule=inv (max I 0.3); eps_start=0.02, lr_schedule=linear (max I 0.33); eps_start=0.0, lr_schedule=inv (max I 0.59); +2 more
  - `eps_start`: eps_start=0.02 (max I 0.26); eps_start=0.0 (max I 0.46); eps_start=0.1 (max I 1.89)
- Equally good values: `eps_start` in {0.0, 0.02}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.0; eps_start=0.02; eps_start=0.02, lr_schedule=linear; eps_start=0.1, lr_schedule=inv; eps_start=0.1, lr_schedule=linear
- equally good values within one noise band (measured): eps_start in {0.0, 0.02}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.0` | 6 | +15.2% | +0.3% | 7.7% |
| `eps_start=0.02` | 6 | -19.2% | +0.8% | 10.0% |
| `eps_start=0.02`, `lr_schedule=linear` | 5 | -24.4% | +0.0% | 12.2% |
| `lr_schedule=inv`, `eps_start=0.1` | 5 | +24.4% | +0.5% | 12.5% |
| `lr_schedule=linear`, `eps_start=0.1` | 5 | -26.1% | +0.5% | 13.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
