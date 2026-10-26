# Gap Report: GCN topology attack (batch-5)

Artifact `harness` · generated 2026-10-26 19:44 · 195 branch runs (0 build/load setups) · sandbox $424.8720

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_t3_5 (c_t3_5_acc) | Paper-artifact inconsistency | -5.1% | +3.1% | ±0.9% | `perturb_ratio=0.025` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `dataset`: "We evaluate our methods on two well-known datasets: Cora and Citeseer" (p.5)
  - `discrete`: "a randomization sampling [Liu et al., 2016] is suited for generating a near-optimal binary topology perturbation" (p.3)
  - `model_dir`: "In min-max attacks (CE-min-max and CW-min-max), we show misclassification rates against both natural and retrained models from Algorithm 3" (p.5)

## C_t3_5: c_t3_5_acc (paper 0.721)
**Paper-artifact inconsistency** · gap -5.1% → +3.1% · 58 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0185`, `B0186` (2 run(s) of the same config)
- Config: `perturb_ratio` naive `0.05`, changed to `0.025`
- Command:

  Replay: fork checkpoint `dd76b337-f894-4e8e-92cd-a2fcab421114` and run
  ```
  RUN_TAG=ecdf8b7300ec export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; mkdir -p out; rm -f out/run*.log; GF_SEED=$("${PYTHON:-python}" -c "import os, zlib; print(zlib.crc32(os.environ.get('RUN_TAG', 'x').encode('utf-8')) % 100000)"); r=1; ("${PYTHON:-python}" attack.py --model_dir nat_cora --dataset cora --steps 100 --learning_rate 0.001 --hidden1 16 --dropout 0.3 --early_stopping 10 --method PGD --perturb_ratio 0.05 --weight_decay 5e-4) > out/run1.log 2>&1; "${PYTHON:-python}" gf_harness/emit.py
  ```
- Output: `c_t3_5_acc` 0.743, 0.743; gap after +3.1%; result checkpoint `3d764020-a09c-4f77-b400-4fdfd123b8b1`
- Effect: candidate 0.743 minus naive 0.684 = +0.059, 95% bootstrap interval [+0.059, +0.059] (2 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `c_t3_5_acc` = 0.721.

### What did we measure?
- Naive median 0.684 over 5 runs; repeats: 0.684, 0.684, 0.684, 0.684, 0.684
- Spread: range 0.684 to 0.684, noise band ±0.00684 (2 x MAD), CV 0.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -5.1% (noise band ±0.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `dropout` the gap is -5.1% (it comes back)
- PASS · Held-out claim: C_t3_10 at perturb_ratio=0.05: n/a to +1.6% (not worse beyond noise)
- PASS · Held-out claim: C_t3_15 at perturb_ratio=0.075: n/a to +1.9% (not worse beyond noise)
- PASS · Held-out claim: C_t3_20 at perturb_ratio=0.1: n/a to +2.2% (not worse beyond noise)
- PASS · Held-out claim: C_t3_0 at perturb_ratio=0: n/a to +0.1% (not worse beyond noise)
- FAIL · Evidence: `dropout=None`: no evidence mentions '0.3'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.059 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `steps=10000`
- Not settable with this harness: `dataset`, `epochs`, `discrete`, `max_degree`, `model_dir`, `seed`, `xi`, `mu`, `warm_start`, `lmd`, `train_test_split_variability`, `confidence_kappa`, `projection_bisection_tolerance`, `train/test splits`, `TensorFlow version`, `hardware`, `save_dir`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `dropout=0.5` (5.41 noise units, gap +0.0%); `perturb_ratio=0.03` (4.24 noise units, gap +1.1%); `dropout=0.3` (3.36 noise units, gap -1.9%); `steps=20` (3.07 noise units, gap -2.2%); `dropout=0.2` (1.46 noise units, gap -3.7%)
- Near alternatives (closest across all claims):
  - `dropout=0.5`: this claim +0.0%, mean |gap| 0.0% (4 runs)
  - `dropout=0.5`, `learning_rate=0.002`: this claim +0.0%, mean |gap| 0.0% (4 runs)
  - `dropout=0.5`, `learning_rate=0.01`: this claim +0.0%, mean |gap| 0.0% (4 runs)

### Equally good configurations
The target claim can't tell these 15 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `dropout=0.3` (reported)
- `dropout=0.3, steps=20`
- `dropout=0.5`
- `steps=20`
- `perturb_ratio=0.03`
- `dropout=0.5, learning_rate=0.002`
- `dropout=0.5, learning_rate=0.01`
- `dropout=0.5, steps=300`
- `dropout=0.5, steps=20`
- `learning_rate=0.002, perturb_ratio=0.03`
- `learning_rate=0.01, perturb_ratio=0.03`
- `perturb_ratio=0.03, steps=300`
- `dropout=0.3, perturb_ratio=0.03`
- `dropout=0.3, learning_rate=0.002`
- `dropout=0.5, perturb_ratio=0.03`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the code's perturb_ratio is 0.5 x the paper's (a unit or convention differs between paper and code) | code | 100% | 1.9 sigma (fits every claim) | find where perturb_ratio enters the computation and compare its unit with the paper's |
| 2 | a cause outside every class tested | outside | 0% |  | look for code, data or evaluation differences the classes don't cover |
| 3 | the setting dropout=0.3, steps=20 | settings | 0% | 4.9 sigma | run with dropout=0.3, steps=20 |

### History matching (every measured configuration, all claims together)
- 6 of 77 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `dropout, steps`: dropout=0.5, steps=300 (max I 0.55); dropout=0.5, steps=20 (max I 0.83)
  - `learning_rate, perturb_ratio`: learning_rate=0.002, perturb_ratio=0.03 (max I 1.11); learning_rate=0.01, perturb_ratio=0.03 (max I 1.11)
  - `perturb_ratio, steps`: perturb_ratio=0.03, steps=300 (max I 1.25)
  - `dropout, learning_rate`: dropout=0.3, learning_rate=0.002 (max I 1.94)
- 4 separate islands (no single-knob move joins them): dropout=0.5, steps=300; dropout=0.5, steps=20 | learning_rate=0.002, perturb_ratio=0.03; learning_rate=0.01, perturb_ratio=0.03 | perturb_ratio=0.03, steps=300 | dropout=0.3, learning_rate=0.002
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `uniform(..., scale=0.05)`: a default no call in the repo overrides (2 call(s)) (`inits.py:5`)
  - unexposed setting: `model_func(..., logging=False)`: a switch fixed in the call; no flag sets it (`adv_train_pgd.py:84`)
  - unexposed setting: `model_func(..., logging=False)`: a switch fixed in the call; no flag sets it (`attack.py:67`)
  - unexposed setting: `Dense(..., sparse_inputs=True)`: a switch fixed in the call; no flag sets it (`models.py:131`)
  - unexposed setting: `GraphConvolution(..., sparse_inputs=False)`: a switch fixed in the call; no flag sets it (`models.py:252`)
  - unexposed setting: `model_func(..., logging=False)`: a switch fixed in the call; no flag sets it (`train.py:69`)
  - unexposed setting: `construct_feed_dict(..., train=True)`: a switch fixed in the call; no flag sets it (`train.py:78`)
  - unexposed setting: `construct_feed_dict(..., train=True)`: a switch fixed in the call; no flag sets it (`train.py:93`)

Notes:
- skipped learning_rate='schedule:200/sqrt(t)': knob value 'schedule:200/sqrt(t)' has shell metacharacters
- configurations the target claim can't tell apart from the answer: dropout=0.5; perturb_ratio=0.03; dropout=0.3; steps=20; dropout=0.5, learning_rate=0.002; dropout=0.5, learning_rate=0.01; dropout=0.3, steps=20; dropout=0.5, steps=300; dropout=0.5, steps=20; learning_rate=0.002, perturb_ratio=0.03; learning_rate=0.01, perturb_ratio=0.03; perturb_ratio=0.03, steps=300; dropout=0.3, perturb_ratio=0.03; dropout=0.3, learning_rate=0.002; dropout=0.5, perturb_ratio=0.03
- capped at Fits but unsupported (was Explained): the only support for dropout=0.5 is code evidence, which shows what the code does, not what the authors ran
- {'dropout': '0.5'} doesn't fit C_t3_15, C_t3_20 (claims at fixed settings); no other tested configuration fits every claim
- discrimination: the paper's other conditions favour dropout=0.3 (posterior 99% after 0 run(s) chosen by expected information)
- dropout=0.5 and dropout=0.3 fit the target equally well; the paper's other conditions favour dropout=0.3 (posterior 99%), so it is the answer
- scale probe: the code's perturb_ratio as 0.5 x the paper's fits every swept claim after 15 runs at g(v) (C_t3_5 at perturb_ratio=0.025, C_t3_10 at perturb_ratio=0.05, C_t3_15 at perturb_ratio=0.075, C_t3_20 at perturb_ratio=0.1, C_t3_0 at perturb_ratio=0)
- labelled Paper-artifact inconsistency: one factor (0.5 x the paper's) makes every one of the 5 swept claims fit; it replaces {'dropout': '0.3'}
- mutation round: no room left in the run budget
- perturb_ratio: values from 0.025 to 0.025 fit every claim (a bisection, 3 runs a side, one run a value: approximate)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_t3_5 | Mean |gap| |
|---|---|---|---|
| `dropout=0.5` | 4 | +0.0% | 0.0% |
| `dropout=0.5`, `learning_rate=0.002` | 4 | +0.0% | 0.0% |
| `dropout=0.5`, `learning_rate=0.01` | 4 | +0.0% | 0.0% |
| `steps=20`, `dropout=0.3` | 4 | -0.1% | 0.1% |
| `dropout=0.5`, `steps=300` | 4 | -0.6% | 0.6% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `steps=10000`

## Knob names
- Ledger names mapped to spec knobs: `train_steps` → `steps`, `att_steps` → `steps`, `ε (perturbation budget for robust training)` → `perturb_ratio`
- Code defaults read from the code instead of the ledger: `perturb_ratio` 0.05 at attack.py:31 (ledger said 0.05 (hardcoded in adv_train_pgd.py:109))

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `dataset`, `epochs`, `discrete`, `max_degree`, `model_dir`, `seed`, `xi`, `mu`, `warm_start`, `lmd`, `train_test_split_variability`, `confidence_kappa`, `projection_bisection_tolerance`, `train/test splits`, `TensorFlow version`, `hardware`, `save_dir`

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `93d941f1d25423ac8df95bea1cd9b8cec9da2f48d2e5f39fa3e8aee8634b941c`
- Cost: Nemotron billed $0.0012, sandbox reported $424.8720 (total $424.8732; this search; ledger extraction is included only if it shared the search's router)
