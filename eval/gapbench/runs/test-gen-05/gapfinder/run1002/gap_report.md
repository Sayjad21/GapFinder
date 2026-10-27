# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-15 00:18 · 111 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +963.4% | +39.9% | ±23.5% | `eps_start=0.02` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +963.4% → +39.9% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0014`, `B0034`, `B0035`, `B0043` (4 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.02`
- Command:

  Replay: fork checkpoint `e3738358-fad8-432f-bf7d-90ee27d24465` and run
  ```
  RUN_TAG=22e87bbd398f "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.02 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 26.38, 22.07, 11.24, 31.04; gap after +39.9%; result checkpoint `4846f0f1-4e14-492a-b894-c2c8c718f6d4`
- Effect: candidate 24.22 minus naive 184.1 = -159.9, 95% bootstrap interval [-176.1, -145.8] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 184.1 over 5 runs; repeats: 167.7, 184.1, 182, 190.8, 184.7
- Spread: range 167.7 to 190.8, noise band ±4.07 (2 x MAD), CV 4.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +963.4% (noise band ±23.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +963.4% (it comes back)
- PASS · Held-out claim: C2: +1062.1% to +0.3% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.02`: no evidence mentions '0.02'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -159.9 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.0` (39.83 noise units, gap +26.8%); `eps_start=0.1` (36.08 noise units, gap +115.2%); `eps_start=0.5` (26.71 noise units, gap +335.4%); `eps_start=0.2` (17.14 noise units, gap +560.5%); `lr_schedule=inv` (8.12 noise units, gap +772.6%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_start=0.0`, `lr_schedule=linear`: this claim -14.6%, mean |gap| 8.1% (3 runs)
  - `eps_start=0.0`: this claim +18.7%, mean |gap| 9.6% (4 runs)
  - `eps_start=0.02`, `lr_schedule=linear`: this claim -23.6%, mean |gap| 12.3% (3 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.02` (reported)
- `eps_start=0.0`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.0, lr_schedule=linear`
- `eps_start=0.0, lr_schedule=inv`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.2, lr_schedule=inv`
- `eps_start=0.02, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 10 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_start, lr_schedule`: eps_start=0.1, lr_schedule=inv (max I 0.06); eps_start=0.0, lr_schedule=linear (max I 0.47); eps_start=0.02, lr_schedule=linear (max I 0.47); eps_start=0.0, lr_schedule=inv (max I 0.7); +3 more
  - `eps_start`: eps_start=0.0 (max I 0.16); eps_start=0.02 (max I 0.9); eps_start=0.1 (max I 2.53)
- Equally good values: `eps_start` in {0.0, 0.02}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.02; eps_start=0.0; eps_start=0.02, lr_schedule=linear; eps_start=0.0, lr_schedule=linear; eps_start=0.0, lr_schedule=inv; eps_start=0.1, lr_schedule=inv; eps_start=0.2, lr_schedule=inv; eps_start=0.02, lr_schedule=inv
- equally good values within one noise band (measured): eps_start in {0.0, 0.02}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.0`, `lr_schedule=linear` | 3 | -14.6% | +1.6% | 8.1% |
| `eps_start=0.0` | 4 | +18.7% | +0.5% | 9.6% |
| `eps_start=0.02`, `lr_schedule=linear` | 3 | -23.6% | +1.1% | 12.3% |
| `eps_start=0.02` | 4 | +39.9% | +0.3% | 20.1% |
| `lr_schedule=inv`, `eps_start=0.1` | 3 | -42.4% | +0.5% | 21.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `hardware_os_python`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
