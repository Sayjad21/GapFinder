# Gap Report: planted L2-fastgcn-s2-1

Artifact `fastgcn` · generated 2026-10-21 23:24 · 150 branch runs (0 build/load setups) · sandbox $47.8970

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_trans_cora_f1 (trans_cora_acc) | Fits but unsupported | +4.2% | -0.8% | ±1.0% | `learning_rate=0.02` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: trans_pubmed_acc 0.773 > trans_cora_acc 0.767; measured: trans_pubmed_acc 0.776 < trans_cora_acc 0.799 (margin -0.023, noise 0.0113)

## C_trans_cora_f1: trans_cora_acc (paper 0.767)
**Fits but unsupported** · gap +4.2% → -0.8% · 88 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0053`, `B0054`, `B0067` (4 run(s) of the same config)
- Config: `learning_rate` naive `0.01`, changed to `0.02`
- Command:

  Replay: fork checkpoint `e6a5358e-5cb8-4cb3-afcb-7190e86cebb7` and run
  ```
  RUN_TAG=e29fd1213250 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; export GF_SEED_FROM_RUN_TAG=1 OMP_NUM_THREADS=1 TF_CPP_MIN_LOG_LEVEL=2; mkdir -p out; A="--model gcn_mix --learning_rate 0.02 --epochs 100 --hidden1 16 --dropout 0.0 --weight_decay 5e-4 --early_stopping 10 --max_degree 3"; python pubmed-original_transductive_FastGCN.py --dataset cora $A > out/trans_cora.log 2>&1 & python pubmed-original_transductive_FastGCN.py --dataset pubmed $A > out/trans_pubmed.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset cora $A > out/ind_cora.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset pubmed $A > out/ind_pubmed.log 2>&1 & wait; bash gf_harness/emit.sh
  ```
- Output: `trans_cora_acc` 0.776, 0.692, 0.746, 0.783; gap after -0.8%; result checkpoint `f3d3884e-67ae-4a7f-9c0a-d658af1e8a53`
- Effect: candidate 0.761 minus naive 0.799 = -0.038, 95% bootstrap interval [-0.1092, -0.0146] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `trans_cora_acc` = 0.767.

### What did we measure?
- Naive median 0.799 over 5 runs; repeats: 0.799, 0.804, 0.795, 0.798, 0.801
- Spread: range 0.795 to 0.804, noise band ±0.00799 (2 x MAD), CV 0.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +4.2% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `learning_rate` the gap is +4.2% (it comes back)
- PASS · Held-out claim: C_trans_pubmed_f1: +0.4% to -0.1% (not worse beyond noise)
- PASS · Held-out claim: C_ind_cora_f1: -0.4% to -0.3% (not worse beyond noise)
- PASS · Held-out claim: C_ind_pubmed_f1: +1.0% to +0.8% (not worse beyond noise)
- PASS · Held-out claim: C_trans_cora_f1@learning_rate=0.005 at learning_rate=0.005: +1.2% to +1.2% (not worse beyond noise)
- PASS · Held-out claim: C_trans_cora_f1@learning_rate=0.02 at learning_rate=0.02: +2.8% to +2.8% (not worse beyond noise)
- FAIL · Evidence: `learning_rate=0.02`: no evidence mentions '0.02'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -0.038 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=5000`, `epochs=10000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `hidden1=80` (2.75 noise units, gap -1.3%); `hidden1=7` (2.13 noise units, gap +2.0%); `early_stopping=5` (1.38 noise units, gap +2.7%); `weight_decay=0.001` (1.13 noise units, gap +3.0%); `weight_decay=0.005` (1 noise units, gap +3.1%)
- Near alternatives (closest across all claims):
  - `learning_rate=0.02`, `epochs=200`: this claim +0.1%, mean |gap| 0.5% (4 runs)
  - `hidden1=80`: this claim -0.3%, mean |gap| 0.5% (4 runs)
  - `epochs=1000`, `learning_rate=0.025`: this claim -1.3%, mean |gap| 0.6% (3 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting learning_rate=0.02 | settings | 26% | 0.7 sigma (fits every claim) | run with learning_rate=0.02 |
| 2 | the setting epochs=200, learning_rate=0.02 | settings | 16% | 0.7 sigma (fits every claim) | run with epochs=200, learning_rate=0.02 |
| 3 | the setting early_stopping=20, learning_rate=0.02 | settings | 11% | 1.3 sigma (fits every claim) | run with early_stopping=20, learning_rate=0.02 |

### History matching (every measured configuration, all claims together)
- 20 of 88 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `early_stopping, hidden1`: early_stopping=5, hidden1=80 (max I 0.69); early_stopping=20, hidden1=80 (max I 2.4)
  - `epochs, hidden1`: epochs=200, hidden1=80 (max I 1.55); epochs=200, hidden1=7 (max I 2.64)
  - `early_stopping, epochs`: early_stopping=20, epochs=1000 (max I 1.78)
  - `early_stopping, learning_rate`: early_stopping=20, learning_rate=0.02 (max I 1.82)
  - `learning_rate`: learning_rate=0.02 (max I 2.08)
  - `epochs, learning_rate`: epochs=200, learning_rate=0.02 (max I 2.35)
  - `epochs, weight_decay`: epochs=200, weight_decay=0.001 (max I 2.56)
  - `early_stopping, weight_decay`: early_stopping=20, weight_decay=0.001 (max I 2.64)
- 3 separate islands (no single-knob move joins them): early_stopping=5, hidden1=80; epochs=200, hidden1=80; early_stopping=20, epochs=1000 | max_degree=2; max_degree=6 | hidden1=32
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
- stopped early: run budget of 150 reached (wanted 1 more run(s) of {'early_stopping': '20', 'weight_decay': '0.001'} for 'confirm-combo')
- verified from runs already made, after the budget ran out
- scale probe: the code's learning_rate as 2 x the paper's does not fit every swept claim after 9 runs at g(v) (C_trans_cora_f1 at learning_rate=0.02, C_trans_cora_f1@learning_rate=0.005 at learning_rate=0.01, C_trans_cora_f1@learning_rate=0.02 at learning_rate=0.04)
- patch round stopped early: run budget of 150 reached (wanted 1 more run(s) of {'early_stopping': '5', 'hidden1': '80', '@ast:layers.py:203:rank': '10'} for 'patch screen')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_trans_cora_f1 | C_trans_pubmed_f1 | C_ind_cora_f1 | C_ind_pubmed_f1 | Mean |gap| |
|---|---|---|---|---|---|---|
| `learning_rate=0.02`, `epochs=200` | 4 | +0.1% | +0.1% | -0.8% | +0.8% | 0.5% |
| `learning_rate=0.02` | 4 | -0.8% | -0.1% | -0.3% | +0.8% | 0.5% |
| `hidden1=80` | 4 | -0.3% | +0.4% | +0.7% | +0.8% | 0.5% |
| `epochs=1000`, `learning_rate=0.025` | 3 | -1.3% | +0.5% | +0.0% | +0.7% | 0.6% |
| `hidden1=80`, `early_stopping=5` | 3 | -1.3% | +0.6% | +1.1% | +0.6% | 0.9% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=5000`, `epochs=10000`

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at pubmed-original_transductive_FastGCN.py:139)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at models.py:58)

## Provenance
- GapFinder commit: `1c8f0f8b4a997137c12c0ee6716ab6adeed88fc3`
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `83e356bf80ca130044addf7e60e14552865ed192207afe9d979410f591b79062`
- Cost: Nemotron billed $0.0000, sandbox reported $47.8970 (total $47.8970; this search; ledger extraction is included only if it shared the search's router)
