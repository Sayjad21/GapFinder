# Gap Report: test-v13-10

Artifact `mlbench` · generated 2026-10-23 18:12 · 161 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -41.2% | -41.2% | ±3.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.8102, measured 0.482 (-40.5%, band ±3.0%)

## C1: test_accuracy (paper 0.8292)
**Unexplained** · gap -41.2% → -41.2% · 61 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (61 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.829 test accuracy and 0.810 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.8292 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4875, 0.475, 0.4792, 0.5458, 0.5625
- Spread: range 0.475 to 0.5625, noise band ±0.025 (2 x MAD), CV 8.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -41.2% (noise band ±3.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--normalize`, `PYTHON_VERSION`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (5.33 noise units, gap -25.1%); `class_weight=balanced` (2.67 noise units, gap -33.2%); `lr_schedule=step` (2.17 noise units, gap -34.7%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`: this claim -25.1%, mean |gap| 24.5% (6 runs)
  - `class_weight=balanced`, `lr_schedule=cosine`: this claim -26.1%, mean |gap| 25.0% (5 runs)
  - `data_seed=123`: this claim -29.4%, mean |gap| 28.9% (6 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 100% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | a code change: train.py:68: `16` -> `17` | code | 0% | 6.3 sigma | run with @ast:train.py:68:@mut.37.num.add1=1 (an in-memory code patch) |
| 3 | no difference in reporting: the numbers as printed at the end of the run | settings | 0% | 6.5 sigma | the settings search and the other classes |

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, C2, among 60 tested

Notes:
- its runs spread 0.2x the naive run's noise band (reported, not used to judge)
- closest configuration tried: {'lr_schedule': 'cosine'} (gap -25.1%); it did not pass verification
- spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, n, positive_rate, split, threshold, weight_decay) were screened too; no better answer
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C1, C2, among 60 tested
- mutation round: no mutant fits every claim (train.py:68: `16` -> `32`: worst 6.4 sigma; train.py:68: `16` -> `17`: worst 6.3 sigma)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine` | 6 | -25.1% | -23.8% | 24.5% |
| `class_weight=balanced`, `lr_schedule=cosine` | 5 | -26.1% | -23.9% | 25.0% |
| `data_seed=123` | 6 | -29.4% | -28.5% | 28.9% |
| `split=0.9` | 3 | -30.7% | -28.2% | 29.4% |
| `class_weight=balanced`, `lr_schedule=step` | 5 | -32.2% | -30.3% | 31.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `split=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--normalize`, `PYTHON_VERSION`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `0f039fdc282711cf8fae8046ee483f168c2fd2a36c2cd699ff6da459b9236b95`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
