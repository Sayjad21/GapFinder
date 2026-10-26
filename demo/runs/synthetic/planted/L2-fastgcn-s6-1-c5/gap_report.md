# Gap Report: planted L2-fastgcn-s6-1

Artifact `fastgcn` · generated 2026-10-23 21:13 · 150 branch runs (0 build/load setups) · sandbox $44.5672

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_trans_cora_f1 (trans_cora_acc) | Fits but unsupported | -1.4% | +0.1% | ±1.0% | `epochs=50` |

## C_trans_cora_f1: trans_cora_acc (paper 0.807)
**Fits but unsupported** · gap -1.4% → +0.1% · 42 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0052`, `B0053`, `B0062` (4 run(s) of the same config)
- Config: `epochs` naive `100`, changed to `50`
- Command:

  Replay: fork checkpoint `e6a5358e-5cb8-4cb3-afcb-7190e86cebb7` and run
  ```
  RUN_TAG=aa08048ccc21 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; export GF_SEED_FROM_RUN_TAG=1 OMP_NUM_THREADS=1 TF_CPP_MIN_LOG_LEVEL=2; mkdir -p out; A="--model gcn_mix --learning_rate 0.01 --epochs 50 --hidden1 16 --dropout 0.0 --weight_decay 5e-4 --early_stopping 10 --max_degree 3"; python pubmed-original_transductive_FastGCN.py --dataset cora $A > out/trans_cora.log 2>&1 & python pubmed-original_transductive_FastGCN.py --dataset pubmed $A > out/trans_pubmed.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset cora $A > out/ind_cora.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset pubmed $A > out/ind_pubmed.log 2>&1 & wait; bash gf_harness/emit.sh
  ```
- Output: `trans_cora_acc` 0.805, 0.81, 0.805, 0.812; gap after +0.1%; result checkpoint `e3c0c13f-e8b9-4143-8720-cc53d1f56f5b`
- Effect: candidate 0.8075 minus naive 0.796 = +0.0115, 95% bootstrap interval [+0.003, +0.01653] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `trans_cora_acc` = 0.807.

### What did we measure?
- Naive median 0.796 over 5 runs; repeats: 0.794, 0.796, 0.796, 0.806, 0.802
- Spread: range 0.794 to 0.806, noise band ±0.00796 (2 x MAD), CV 0.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -1.4% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is -1.4% (it comes back)
- PASS · Held-out claim: C_trans_pubmed_f1: +0.9% to +0.2% (not worse beyond noise)
- PASS · Held-out claim: C_ind_cora_f1: +0.7% to +1.4% (not worse beyond noise)
- PASS · Held-out claim: C_ind_pubmed_f1: +0.1% to -0.1% (not worse beyond noise)
- PASS · Held-out claim: C_trans_cora_f1@epochs=50 at epochs=50: -0.2% to -0.2% (not worse beyond noise)
- PASS · Held-out claim: C_trans_cora_f1@epochs=200 at epochs=200: -0.9% to -0.9% (not worse beyond noise)
- FAIL · Evidence: `epochs=50`: no evidence mentions '50'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.0115 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=5000`, `epochs=10000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `weight_decay=0.00025` (1.26 noise units, gap -0.1%); `learning_rate=0.005` (1.13 noise units, gap -0.2%); `learning_rate=0.001` (1.13 noise units, gap -0.2%); `weight_decay=0.0001` (1.13 noise units, gap +0.2%); `hidden1=8` (1.01 noise units, gap -0.4%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `weight_decay=0.0001`, `early_stopping=1`: this claim -0.1%, mean |gap| 0.3% (4 runs)
  - `early_stopping=1`, `epochs=50`: this claim -0.4%, mean |gap| 0.5% (4 runs)
  - `early_stopping=1`, `weight_decay=0.00025`: this claim +0.2%, mean |gap| 0.5% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | no difference in reporting: the numbers as printed at the end of the run | settings | 33% | 0.7 sigma (fits every claim) | the settings search and the other classes |
| 2 | the setting epochs=50 | settings | 19% | 0.9 sigma (fits every claim) | run with epochs=50 |
| 3 | the code's epochs is 0.5 x the paper's (a unit or convention differs between paper and code) | code | 10% | 0.5 sigma (fits every claim) | find where epochs enters the computation and compare its unit with the paper's |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `early_stopping, weight_decay`: early_stopping=1, weight_decay=0.0001 (max I 0.31); early_stopping=1, weight_decay=0.00025 (max I 0.65)
  - `early_stopping`: early_stopping=2 (max I 0.48)
  - `early_stopping, learning_rate`: early_stopping=2, learning_rate=0.005 (max I 0.48); early_stopping=1, learning_rate=0.005 (max I 0.55)
  - `early_stopping, epochs`: early_stopping=1, epochs=50 (max I 0.56)
  - `max_degree`: max_degree=6 (max I 0.65); max_degree=300 (max I 0.71)
  - `epochs, learning_rate`: epochs=50, learning_rate=0.005 (max I 0.7); epochs=200, learning_rate=0.005 (max I 0.74)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `__init__(..., rank=100)`: a default no call in the repo overrides (8 call(s)) (`layers.py:203`)
  - unexposed setting: `dot(..., sparse=True)`: a switch fixed in the call; no flag sets it (`layers.py:192`)
  - unexposed setting: `dot(..., sparse=True)`: a switch fixed in the call; no flag sets it (`layers.py:243`)
  - unexposed setting: `dot(..., sparse=True)`: a switch fixed in the call; no flag sets it (`layers.py:271`)
  - unexposed setting: `Dense(..., sparse_inputs=True)`: a switch fixed in the call; no flag sets it (`models.py:113`)
  - unexposed setting: `GraphConvolution(..., sparse_inputs=True)`: a switch fixed in the call; no flag sets it (`models.py:163`)
  - unexposed setting: `GraphConvolution(..., sparse_inputs=False)`: a switch fixed in the call; no flag sets it (`models.py:210`)
  - unexposed setting: `Dense(..., sparse_inputs=False)`: a switch fixed in the call; no flag sets it (`models.py:258`)

Notes:
- stopped early: run budget of 150 reached (wanted 3 more run(s) of {'learning_rate': '0.005', 'early_stopping': '2'} for 'confirm-combo (early)')
- verified from runs already made, after the budget ran out
- early code screen stopped: run budget of 150 reached (wanted 1 more run(s) of {'@ast:layers.py:203:rank': '10'} for 'patch screen (early)')
- scale probe: the code's epochs as 0.5 x the paper's does not fit every swept claim after 9 runs at g(v) (C_trans_cora_f1 at epochs=50, C_trans_cora_f1@epochs=50 at epochs=25, C_trans_cora_f1@epochs=200 at epochs=100)
- scale probe: the code's epochs as 0.2 x the paper's does not fit every swept claim after 2 runs at g(v) (C_trans_cora_f1 at epochs=20, C_trans_cora_f1@epochs=50 at epochs=10, C_trans_cora_f1@epochs=200 at epochs=40)
- patch round stopped early: run budget of 150 reached (wanted 1 more run(s) of {'early_stopping': '1', 'weight_decay': '0.0001', '@ast:layers.py:203:rank': '10'} for 'patch screen')
- value interval stopped early: run budget of 150 reached (wanted 1 more run(s) of {'epochs': '32'} for 'interval epochs=32')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_trans_cora_f1 | C_trans_pubmed_f1 | C_ind_cora_f1 | C_ind_pubmed_f1 | Mean |gap| |
|---|---|---|---|---|---|---|
| `weight_decay=0.0001`, `early_stopping=1` | 4 | -0.1% | -0.5% | -0.4% | +0.2% | 0.3% |
| `epochs=50` | 4 | +0.1% | +0.2% | +1.4% | -0.1% | 0.4% |
| `early_stopping=1`, `epochs=50` | 4 | -0.4% | -0.8% | -0.1% | -0.6% | 0.5% |
| `early_stopping=1`, `weight_decay=0.00025` | 4 | +0.2% | -0.8% | +0.7% | -0.1% | 0.5% |
| `learning_rate=0.005`, `epochs=50` | 4 | +0.9% | -0.8% | +0.0% | +0.3% | 0.5% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=5000`, `epochs=10000`

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at pubmed-original_transductive_FastGCN.py:139)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at models.py:58)

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `83e356bf80ca130044addf7e60e14552865ed192207afe9d979410f591b79062`
- Cost: Nemotron billed $0.0000, sandbox reported $44.5672 (total $44.5672; this search; ledger extraction is included only if it shared the search's router)
