# Gap Report: GCN topology attack (batch-5)

Artifact `harness` · generated 2026-10-26 04:17 · 200 branch runs (0 build/load setups) · sandbox $210.8582

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_t3_5 (c_t3_5_acc) | Fits but unsupported | -5.1% | -1.9% | ±0.9% | `dropout=0.3` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `dataset`: "We evaluate our methods on two well-known datasets: Cora and Citeseer" (p.5)
  - `att_steps`: "We run 20 steps for inner minimization." (p.5)
  - `discrete`: "a randomization sampling [Liu et al., 2016] is suited for generating a near-optimal binary topology perturbation" (p.3)
  - `model_dir`: "In min-max attacks (CE-min-max and CW-min-max), we show misclassification rates against both natural and retrained models from Algorithm 3" (p.5)

## C_t3_5: c_t3_5_acc (paper 0.721)
**Fits but unsupported** · gap -5.1% → -1.9% · 68 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0032`, `B0058`, `B0059`, `B0097` (4 run(s) of the same config)
- Config: `dropout` naive `0.`, changed to `0.3`
- Command:

  Replay: fork checkpoint `dd76b337-f894-4e8e-92cd-a2fcab421114` and run
  ```
  RUN_TAG=a6197bf63420 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; mkdir -p out; rm -f out/run*.log; GF_SEED=$("${PYTHON:-python}" -c "import os, zlib; print(zlib.crc32(os.environ.get('RUN_TAG', 'x').encode('utf-8')) % 100000)"); r=1; ("${PYTHON:-python}" attack.py --model_dir nat_cora --dataset cora --steps 100 --learning_rate 0.001 --hidden1 16 --dropout 0.3 --early_stopping 10 --method PGD --perturb_ratio 0.05 --weight_decay 5e-4) > out/run1.log 2>&1; "${PYTHON:-python}" gf_harness/emit.py
  ```
- Output: `c_t3_5_acc` 0.707, 0.707, 0.707, 0.707; gap after -1.9%; result checkpoint `dda13b8d-610a-4a01-bf61-570ce2ecf0ab`
- Effect: candidate 0.707 minus naive 0.684 = +0.023, 95% bootstrap interval [+0.023, +0.023] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `c_t3_5_acc` = 0.721.

### What did we measure?
- Naive median 0.684 over 5 runs; repeats: 0.684, 0.684, 0.684, 0.684, 0.684
- Spread: range 0.684 to 0.684, noise band ±0.00684 (2 x MAD), CV 0.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -5.1% (noise band ±0.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `dropout` the gap is -5.1% (it comes back)
- PASS · Held-out claim: C_t3_10 at perturb_ratio=0.10: -9.2% to -7.7% (not worse beyond noise)
- PASS · Held-out claim: C_t3_15 at perturb_ratio=0.15: -14.7% to -10.4% (not worse beyond noise)
- PASS · Held-out claim: C_t3_20 at perturb_ratio=0.20: -19.1% to -13.9% (not worse beyond noise)
- PASS · Held-out claim: C_t3_0 at perturb_ratio=0: +0.1% to +0.1% (not worse beyond noise)
- FAIL · Evidence: `dropout=0.3`: no evidence mentions '0.3'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.023 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `steps=10000`
- Not settable with this harness: `train_steps`, `dataset`, `att_steps`, `epochs`, `discrete`, `max_degree`, `model_dir`, `seed`, `xi`, `mu`, `warm_start`, `lmd`, `train_test_split_variability`, `confidence_kappa`, `projection_bisection_tolerance`, `train/test splits`, `TensorFlow version`, `hardware`, `ε (perturbation budget for robust training)`, `save_dir`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `dropout=0.5` (5.41 noise units, gap +0.0%); `steps=10` (5.26 noise units, gap +0.1%); `perturb_ratio=0.03` (4.24 noise units, gap +1.1%); `steps=50` (1.9 noise units, gap -3.3%); `dropout=0.2` (1.46 noise units, gap -3.7%)
- Near alternatives (closest across all claims):
  - `dropout=0.5`: this claim +0.0%, mean |gap| 0.0% (4 runs)
  - `learning_rate=0.002`, `dropout=0.5`: this claim +0.0%, mean |gap| 0.0% (4 runs)
  - `learning_rate=0.01`, `dropout=0.5`: this claim +0.0%, mean |gap| 0.0% (4 runs)

### Equally good configurations
The target claim can't tell these 19 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `dropout=0.3` (reported)
- `dropout=0.5`
- `steps=10`
- `perturb_ratio=0.03`
- `dropout=0.5, learning_rate=0.002`
- `dropout=0.5, learning_rate=0.01`
- `learning_rate=0.002, steps=10`
- `learning_rate=0.01, steps=10`
- `dropout=0.5, steps=50`
- `learning_rate=0.002, perturb_ratio=0.03`
- `learning_rate=0.01, perturb_ratio=0.03`
- `dropout=0.3, perturb_ratio=0.03`
- `dropout=0.3, steps=10`
- `dropout=0.3, steps=50`
- `perturb_ratio=0.03, steps=50`
- `dropout=0.3, learning_rate=0.002`
- `dropout=0.3, learning_rate=0.01`
- `dropout=0.5, steps=10`
- `dropout=0.5, perturb_ratio=0.03`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 100% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | the setting dropout=0.5 | settings | 0% | 5.1 sigma | run with dropout=0.5 |
| 3 | the setting dropout=0.5, learning_rate=0.002 | settings | 0% | 5.1 sigma | run with dropout=0.5, learning_rate=0.002 |

### History matching (every measured configuration, all claims together)
- 11 of 83 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `learning_rate, steps`: learning_rate=0.002, steps=10 (max I 0.14); learning_rate=0.01, steps=10 (max I 0.14)
  - `dropout, steps`: dropout=0.5, steps=50 (max I 0.28); dropout=0.3, steps=10 (max I 1.39); dropout=0.3, steps=50 (max I 1.53)
  - `learning_rate, perturb_ratio`: learning_rate=0.002, perturb_ratio=0.03 (max I 1.11); learning_rate=0.01, perturb_ratio=0.03 (max I 1.11)
  - `perturb_ratio, steps`: perturb_ratio=0.03, steps=50 (max I 1.8)
  - `dropout, learning_rate`: dropout=0.3, learning_rate=0.002 (max I 1.94); dropout=0.3, learning_rate=0.01 (max I 1.94)
- 5 separate islands (no single-knob move joins them): dropout=0.5, steps=50; dropout=0.3, steps=10; dropout=0.3, steps=50 | learning_rate=0.002, steps=10; learning_rate=0.01, steps=10 | learning_rate=0.002, perturb_ratio=0.03; learning_rate=0.01, perturb_ratio=0.03 | dropout=0.3, learning_rate=0.002; dropout=0.3, learning_rate=0.01
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
- configurations the target claim can't tell apart from the answer: dropout=0.5; steps=10; perturb_ratio=0.03; dropout=0.3; dropout=0.5, learning_rate=0.002; dropout=0.5, learning_rate=0.01; learning_rate=0.002, steps=10; learning_rate=0.01, steps=10; dropout=0.5, steps=50; learning_rate=0.002, perturb_ratio=0.03; learning_rate=0.01, perturb_ratio=0.03; dropout=0.3, perturb_ratio=0.03; dropout=0.3, steps=10; dropout=0.3, steps=50; perturb_ratio=0.03, steps=50; dropout=0.3, learning_rate=0.002; dropout=0.3, learning_rate=0.01; dropout=0.5, steps=10; dropout=0.5, perturb_ratio=0.03
- capped at Fits but unsupported (was Explained): the only support for dropout=0.5 is code evidence, which shows what the code does, not what the authors ran
- {'dropout': '0.5'} doesn't fit C_t3_15, C_t3_20 (claims at fixed settings); no other tested configuration fits every claim
- discrimination: the paper's other conditions favour dropout=0.3 (posterior 100% after 0 run(s) chosen by expected information)
- dropout=0.5 and dropout=0.3 fit the target equally well; the paper's other conditions favour dropout=0.3 (posterior 100%), so it is the answer
- patch round stopped early: run budget of 200 reached (wanted 1 more run(s) of {'learning_rate': '0.002', 'steps': '10', '@ast:adv_train_pgd.py:84:logging': 'True'} for 'patch screen')
- value interval stopped early: run budget of 200 reached (wanted 1 more run(s) of {'dropout': '0.2449'} for 'interval dropout=0.2449')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_t3_5 | Mean |gap| |
|---|---|---|---|
| `dropout=0.5` | 4 | +0.0% | 0.0% |
| `learning_rate=0.002`, `dropout=0.5` | 4 | +0.0% | 0.0% |
| `learning_rate=0.01`, `dropout=0.5` | 4 | +0.0% | 0.0% |
| `steps=10` | 4 | +0.1% | 0.1% |
| `steps=10`, `learning_rate=0.002` | 4 | +0.1% | 0.1% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `steps=10000`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `train_steps`, `dataset`, `att_steps`, `epochs`, `discrete`, `max_degree`, `model_dir`, `seed`, `xi`, `mu`, `warm_start`, `lmd`, `train_test_split_variability`, `confidence_kappa`, `projection_bisection_tolerance`, `train/test splits`, `TensorFlow version`, `hardware`, `ε (perturbation budget for robust training)`, `save_dir`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `29db980c8ea40fd1a5f7f8e78ba6507f1c426834ba5748622f3362d82debe3d1`
- Cost: Nemotron billed $0.0016, sandbox reported $210.8582 (total $210.8598; this search; ledger extraction is included only if it shared the search's router)
