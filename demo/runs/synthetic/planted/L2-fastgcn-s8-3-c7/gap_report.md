# Gap Report: planted L2-fastgcn-s8-3

Artifact `fastgcn` · generated 2026-10-26 23:21 · 150 branch runs (0 build/load setups) · sandbox $38.9262

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_trans_cora_f1 (trans_cora_acc) | Fits but unsupported | +5.6% | +3.3% | ±1.1% | `learning_rate=0.02` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: trans_pubmed_acc 0.773 > trans_cora_acc 0.753; measured: trans_pubmed_acc 0.774 < trans_cora_acc 0.795 (margin -0.021, noise 0.0111)

## C_trans_cora_f1: trans_cora_acc (paper 0.753)
**Fits but unsupported** · gap +5.6% → +3.3% · 62 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0063`, `B0064`, `B0085` (4 run(s) of the same config)
- Config: `learning_rate` naive `0.01`, changed to `0.02`
- Command:

  Replay: fork checkpoint `e6a5358e-5cb8-4cb3-afcb-7190e86cebb7` and run
  ```
  @ast:layers.py:192:sparse=True @ast:models.py:258:sparse_inputs=False @ast:pubmed-original_inductive_FastGCN.py:106:logging=True @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.add1=0 @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.div2=0 @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.mul2=0 @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.sub1=0 @ast:pubmed-original_inductive_FastGCN.py:144:@mut.35.Call.red.mean=0 @ast:pubmed-original_inductive_FastGCN.py:151:@mut.77.num.add1=0 RUN_TAG=4c53d4b1c77e export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; export GF_SEED_FROM_RUN_TAG=1 OMP_NUM_THREADS=1 TF_CPP_MIN_LOG_LEVEL=2; mkdir -p out; A="--model gcn_mix --learning_rate 0.05 --epochs 100 --hidden1 16 --dropout 0.0 --weight_decay 5e-4 --early_stopping 10 --max_degree 3"; python pubmed-original_transductive_FastGCN.py --dataset cora $A > out/trans_cora.log 2>&1 & python pubmed-original_transductive_FastGCN.py --dataset pubmed $A > out/trans_pubmed.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset cora $A > out/ind_cora.log 2>&1 & python pubmed-original_inductive_FastGCN.py --dataset pubmed $A > out/ind_pubmed.log 2>&1 & wait; bash gf_harness/emit.sh
  ```
- Output: `trans_cora_acc` 0.784, 0.679, 0.781, 0.774; gap after +3.3%; result checkpoint `77f5e3ba-63ac-4d2d-8368-f76dd85ca831`
- Effect: candidate 0.7775 minus naive 0.795 = -0.0175, 95% bootstrap interval [-0.1202, -0.013] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `trans_cora_acc` = 0.753.

### What did we measure?
- Naive median 0.795 over 5 runs; repeats: 0.793, 0.792, 0.8, 0.803, 0.795
- Spread: range 0.792 to 0.803, noise band ±0.00795 (2 x MAD), CV 0.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +5.6% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `learning_rate` the gap is +5.6% (it comes back)
- PASS · Held-out claim: C_trans_cora_f1@learning_rate=0.005 at learning_rate=0.01: n/a to -0.4% (not worse beyond noise)
- PASS · Held-out claim: C_trans_cora_f1@learning_rate=0.02 at learning_rate=0.04: n/a to -2.5% (not worse beyond noise)
- FAIL · Evidence: `learning_rate=0.02`: no evidence mentions '0.05'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -0.0175 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=5000`, `epochs=10000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `hidden1=4` (5.16 noise units, gap -0.1%); `learning_rate=0.05` (4.65 noise units, gap -0.7%); `hidden1=80` (4.03 noise units, gap +1.3%); `hidden1=5` (3.4 noise units, gap +2.0%); `learning_rate=0.04` (3.02 noise units, gap -2.4%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `hidden1=160`: this claim -0.5%, mean |gap| 0.3% (4 runs)
  - `learning_rate=0.05`: this claim -1.1%, mean |gap| 0.8% (4 runs)
  - `hidden1=80`: this claim +2.4%, mean |gap| 1.2% (4 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `learning_rate=0.05` (reported)
- `learning_rate=0.04`
- `hidden1=160`
- `learning_rate=0.02`
- `hidden1=80`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting learning_rate=0.02 | settings | 37% | 0.7 sigma (fits every claim) | run with learning_rate=0.02 |
| 2 | the code's learning_rate is 2 x the paper's (a unit or convention differs between paper and code) | code | 26% | 0.4 sigma (fits every claim) | find where learning_rate enters the computation and compare its unit with the paper's |
| 3 | the setting learning_rate=0.05 | settings | 15% | 0.7 sigma (fits every claim) | run with learning_rate=0.05 |

### History matching (every measured configuration, all claims together)
- 4 of 71 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `hidden1`: hidden1=80 (max I 1.37)
  - `learning_rate`: learning_rate=0.02 (max I 1.52); learning_rate=0.05 (max I 1.52)
  - `hidden1, learning_rate`: hidden1=80, learning_rate=0.02 (max I 2.58)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `dot(..., sparse=True)`: a switch fixed in the call; no flag sets it (`layers.py:192`)
  - unexposed setting: `Dense(..., sparse_inputs=False)`: a switch fixed in the call; no flag sets it (`models.py:258`)
  - unexposed setting: `model_func(..., logging=True)`: a switch fixed in the call; no flag sets it (`pubmed-original_inductive_FastGCN.py:106`)
  - unexposed setting: `iterate_minibatches_listinputs(..., shuffle=True)`: a switch fixed in the call; no flag sets it (`pubmed-original_inductive_FastGCN.py:137`)
  - unexposed setting: `model_func(..., logging=True)`: a switch fixed in the call; no flag sets it (`pubmed-original_transductive_FastGCN.py:112`)
  - unexposed setting: `iterate_minibatches_listinputs(..., shuffle=True)`: a switch fixed in the call; no flag sets it (`pubmed-original_transductive_FastGCN.py:143`)
  - unexposed setting: `__init__(..., rank=100)`: a default no call in the repo overrides (8 call(s)) (`layers.py:203`)
  - unexposed setting: `dot(..., sparse=True)`: a switch fixed in the call; no flag sets it (`layers.py:243`)

Notes:
- configurations the target claim can't tell apart from the answer: learning_rate=0.05; learning_rate=0.04; hidden1=160; learning_rate=0.02; hidden1=80
- discrimination: the paper's other conditions (C_trans_cora_f1@learning_rate=0.005, C_trans_cora_f1@learning_rate=0.02) don't yet tell the equally good fits apart: learning_rate=0.02 51%; learning_rate=0.05 27%; hidden1=80 22%
- scale probe: the code's learning_rate as 2 x the paper's fits every swept claim after 13 runs at g(v) (C_trans_cora_f1 at learning_rate=0.02, C_trans_cora_f1@learning_rate=0.005 at learning_rate=0.01, C_trans_cora_f1@learning_rate=0.02 at learning_rate=0.04)
- scale probe: only 1 of the 3 swept claims were off as run, so the factor is at most an unsupported fit
- labelled Fits but unsupported: one factor (2 x the paper's) makes every one of the 3 swept claims fit; it replaces {'learning_rate': '0.05'}
- patch round: none of 6 code-patch configurations fits every claim
- mutation round: none of 6 mutants moved C_trans_cora_f1 toward the paper
- value interval stopped early: run budget of 150 reached (wanted 1 more run(s) of {'learning_rate': '0.01'} for 'interval learning_rate=0.01')
- not identifiable from the paper's numbers: 4 configuration(s) of other knobs fit every claim as well as the answer (learning_rate=0.02: hidden1=160; hidden1=80; learning_rate=0.04; learning_rate=0.05), and the paper's other conditions (C_trans_cora_f1@learning_rate=0.005, C_trans_cora_f1@learning_rate=0.02) don't separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_trans_cora_f1 | C_trans_pubmed_f1 | C_ind_cora_f1 | C_ind_pubmed_f1 | Mean |gap| |
|---|---|---|---|---|---|---|
| `hidden1=160` | 4 | -0.5% | +0.6% | -0.1% | +0.1% | 0.3% |
| `learning_rate=0.05` | 4 | -1.1% | -0.9% | -1.2% | +0.1% | 0.8% |
| `learning_rate=0.02` | 4 | +3.3% | +0.3% | -0.6% | +0.3% | 1.1% |
| `hidden1=80` | 4 | +2.4% | +0.4% | +0.9% | +1.1% | 1.2% |
| `learning_rate=0.04` | 4 | -4.1% | -0.8% | -1.0% | +0.2% | 1.5% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=5000`, `epochs=10000`

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at pubmed-original_transductive_FastGCN.py:139)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at models.py:58)

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `679aa38905294bd24919c4fd19098f3284e8378ed022a797bb4af9dc42eeff19`
- Cost: Nemotron billed $0.0000, sandbox reported $38.9262 (total $38.9262; this search; ledger extraction is included only if it shared the search's router)
