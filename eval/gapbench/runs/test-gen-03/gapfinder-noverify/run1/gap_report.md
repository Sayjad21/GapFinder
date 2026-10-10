# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-10 22:55 · 30 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | -39.8% | +9.3% | ±5.5% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Explained** · gap -39.8% → +9.3% · 9 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0012`, `B0013`, `B0014`, `B0015` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `a500dbfb-c383-4194-8722-aa58b0caf193` and run
  ```
  RUN_TAG=e1d395b117a0 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 276.5, 330, 257.4, 373.3, 354; gap after +9.3%; result checkpoint `4539feb1-5414-4567-a1e5-e12c0c80ac92`
- Effect: candidate 330 minus naive 181.9 = +148.1, 95% bootstrap interval [+98.48, +179.9] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 181.9 over 5 runs; repeats: 189.1, 158.9, 171, 190.2, 181.9
- Spread: range 158.9 to 190.2, noise band ±16.48 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -39.8% (noise band ±5.5% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +148.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `reward per step`, `RL_SEED_BASE`, `RUN_TAG`, `evaluation action selection`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `init_q=1.0`, `max_steps=500`: this claim -6.0%, mean |gap| 5.5% (5 runs)
  - `max_steps=1000`: this claim +49.1%, mean |gap| 48.3% (5 runs)
  - `max_steps=500`, `lr_schedule=linear`: this claim -41.4%, mean |gap| 122.6% (5 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `init_q=1.0`, `max_steps=500` | 5 | -6.0% | +5.1% | 5.5% |
| `max_steps=500` | 5 | +9.3% | +3.3% | 6.3% |
| naive (reproduction as run) | 5 | -39.8% | +12.2% | 26.0% |
| `max_steps=1000` | 5 | +49.1% | +47.5% | 48.3% |
| `max_steps=500`, `lr_schedule=linear` | 5 | -41.4% | +203.8% | 122.6% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The program expects a float for --init_q but received the string 'zero', which cannot be parsed as a number

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `reward per step`, `RL_SEED_BASE`, `RUN_TAG`, `evaluation action selection`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.1361, sandbox reported $0.0000 (total $0.1361; this search; ledger extraction is included only if it shared the search's router)
