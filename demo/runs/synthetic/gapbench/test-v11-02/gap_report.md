# Gap Report: test-v11-02

Artifact `mlbench` · generated 2026-10-23 17:49 · 159 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -18.7% | -18.7% | ±2.5% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.4848, measured 0.5424 (+11.9%, band ±4.2%)

## C1: test_accuracy (paper 0.6666)
**Unexplained** · gap -18.7% → -18.7% · 74 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (74 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.667 test accuracy and 0.485 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.6666 (headline claim)

### What did we measure?
- Naive median 0.5417 over 5 runs; repeats: 0.5125, 0.5458, 0.5417, 0.4667, 0.55
- Spread: range 0.4667 to 0.55, noise band ±0.0166 (2 x MAD), CV 6.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -18.7% (noise band ±2.5% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `math_module`, `floating_point`, `disk`, `network`, `system_load`, `--out`, `thread_count`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (5.52 noise units, gap -5.0%); `normalize=minmax` (3.26 noise units, gap -10.6%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim -10.6%, mean |gap| 6.9% (6 runs)
  - `normalize=minmax`, `lr_schedule=cosine`: this claim -10.6%, mean |gap| 6.9% (5 runs)
  - `lr_schedule=step`, `normalize=minmax`: this claim -10.6%, mean |gap| 6.9% (5 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting lr_schedule=cosine, normalize=minmax | settings | 51% | 1.8 sigma (fits every claim) | run with lr_schedule=cosine, normalize=minmax |
| 2 | the setting lr_schedule=step, normalize=minmax | settings | 17% | 1.8 sigma (fits every claim) | run with lr_schedule=step, normalize=minmax |
| 3 | the setting normalize=minmax | settings | 17% | 1.8 sigma (fits every claim) | run with normalize=minmax |

### History matching (every measured configuration, all claims together)
- 34 of 74 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 1.76); lr_schedule=step, normalize=minmax (max I 1.76)
  - `normalize`: normalize=minmax (max I 1.78)
  - `lr_schedule`: lr_schedule=step (max I 2.2)
  - `label_noise`: label_noise=0.005 (max I 2.2)
  - `batch_size`: batch_size=1 (max I 2.29); batch_size=16 (max I 2.37)
  - `batch_size, epochs`: batch_size=3, epochs=150 (max I 2.29)
  - `@ast:train.py:68:@mut.37.num.add1`: @ast:train.py:68:@mut.37.num.add1=1 (max I 2.37)
  - `epochs`: epochs=2 (max I 2.37)
- 11 separate islands (no single-knob move joins them): lr_schedule=cosine, normalize=minmax; lr_schedule=step, normalize=minmax; normalize=minmax | label_noise=0.005; label_noise=0.0; label_noise=0.525 | threshold=0.25; threshold=0.3; threshold=0.05 | data_seed=1; data_seed=4

Notes:
- {'lr_schedule': 'cosine'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr_schedule': 'cosine'} (gap -6.2%); it did not pass verification
- spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, n, positive_rate, split, threshold, weight_decay) were screened too; no better answer
- history matching: 34 of 74 tested configurations fit every claim within 3 sigma
- mutation round: none of 3 mutants moved C1 toward the paper

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 6 | -10.6% | +3.1% | 6.9% |
| `normalize=minmax`, `lr_schedule=cosine` | 5 | -10.6% | +3.1% | 6.9% |
| `lr_schedule=step`, `normalize=minmax` | 5 | -10.6% | +3.1% | 6.9% |
| `data_seed=42` | 6 | -21.9% | +7.3% | 14.6% |
| `data_seed=123` | 6 | -13.4% | +16.9% | 15.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `split=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `math_module`, `floating_point`, `disk`, `network`, `system_load`, `--out`, `thread_count`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `1fd3d59022925491b04c41fd5e5ed48e25739b360d0d1093aefdff9298c5fcf4`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
