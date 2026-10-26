# Gap Report: test-gen-01

Artifact `mlbench` · generated 2026-10-23 17:39 · 169 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -30.4% | -30.4% | ±7.1% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.4111, measured 0.4889 (+18.9%, band ±13.4%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `aggregation`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)
  - `num_runs`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)

## C1: test_accuracy (paper 0.7069)
**Unexplained** · gap -30.4% → -30.4% · 67 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (67 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.707 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7069 (headline claim)

### What did we measure?
- Naive median 0.4917 over 5 runs; repeats: 0.5375, 0.5375, 0.4833, 0.4667, 0.4917
- Spread: range 0.4667 to 0.5375, noise band ±0.05 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.4% (noise band ±7.1% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation`, `SCALES`, `WEIGHTS`, `num_runs`, `weight_init_std`, `sigmoid_clamp`, `CPU`, `OS`, `Python_version`, `random_module`, `floating_point_precision`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (2.75 noise units, gap -11.0%); `normalize=minmax` (2.08 noise units, gap -15.7%); `normalize=zscore` (1.94 noise units, gap +16.7%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim -15.7%, mean |gap| 18.7% (6 runs)
  - `normalize=minmax`, `lr_schedule=cosine`: this claim -15.7%, mean |gap| 18.7% (5 runs)
  - `lr_schedule=step`, `normalize=minmax`: this claim -15.7%, mean |gap| 18.7% (5 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 95% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | the setting lr_schedule=cosine, normalize=minmax | settings | 3% | 2.8 sigma (fits every claim) | run with lr_schedule=cosine, normalize=minmax |
| 3 | the setting lr_schedule=step, normalize=minmax | settings | 1% | 2.8 sigma (fits every claim) | run with lr_schedule=step, normalize=minmax |

### History matching (every measured configuration, all claims together)
- 3 of 65 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 2.79); lr_schedule=step, normalize=minmax (max I 2.79)
  - `normalize`: normalize=minmax (max I 2.86)

Notes:
- its runs spread 0.2x the naive run's noise band (reported, not used to judge)
- {'lr_schedule': 'cosine'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr_schedule': 'cosine'} (gap -12.8%); it did not pass verification
- spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, n, positive_rate, split, threshold, weight_decay) were screened too; no better answer
- history matching: 3 of 65 tested configurations fit every claim within 3 sigma
- mutation round: none of 2 mutants ran

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 6 | -15.7% | +21.6% | 18.7% |
| `normalize=minmax`, `lr_schedule=cosine` | 5 | -15.7% | +21.6% | 18.7% |
| `lr_schedule=step`, `normalize=minmax` | 5 | -15.7% | +21.6% | 18.7% |
| `split=0.98` | 6 | -32.2% | +14.9% | 23.5% |
| `lr=0.1` | 6 | -31.0% | +17.5% | 24.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `split=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `aggregation`, `SCALES`, `WEIGHTS`, `num_runs`, `weight_init_std`, `sigmoid_clamp`, `CPU`, `OS`, `Python_version`, `random_module`, `floating_point_precision`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `7be36dde35aa5fcbe1cffeee1216997d960b4211d0ed734a6433b1f16ca8950d`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
