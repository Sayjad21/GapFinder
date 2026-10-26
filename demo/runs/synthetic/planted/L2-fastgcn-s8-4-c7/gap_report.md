# Gap Report: planted L2-fastgcn-s8-4

Artifact `fastgcn` · generated 2026-10-26 23:31 · 150 branch runs (0 build/load setups) · sandbox $45.4590

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_trans_cora_f1 (trans_cora_acc) | Fits but unsupported | -1.0% | +0.0% | ±1.0% | `epochs=50` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_ind_cora_f1 (`ind_cora_acc`): paper 0.703, measured 0.712 (+1.3%, band ±1.0%)

## C_trans_cora_f1: trans_cora_acc (paper 0.805)
**Fits but unsupported** · gap -1.0% → +0.0% · 66 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0133`, `B0143` (3 run(s) of the same config)
- Config: `epochs` naive `100`, changed to `50`
- Command: not recorded
- Output: `trans_cora_acc` 0.804, 0.806, 0.801; gap after +0.0%
- Effect: candidate 0.804 minus naive 0.797 = +0.007, 95% bootstrap interval [+0.0024, +0.0096] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `trans_cora_acc` = 0.805.

### What did we measure?
- Naive median 0.797 over 5 runs; repeats: 0.796, 0.8, 0.799, 0.797, 0.795
- Spread: range 0.795 to 0.8, noise band ±0.00797 (2 x MAD), CV 0.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -1.0% (noise band ±1.0% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- PASS · Held-out claim: C_trans_cora_f1@epochs=50 at epochs=25: n/a to +0.6% (not worse beyond noise)
- PASS · Held-out claim: C_trans_cora_f1@epochs=200 at epochs=100: n/a to +0.1% (not worse beyond noise)
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.007 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=5000`, `epochs=10000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `@ast:pubmed-original_inductive_FastGCN.py:106:logging=False`, `epochs=50`: this claim +0.0%, mean |gap| 0.3% (3 runs)
  - `learning_rate=0.005`, `epochs=200`: this claim -0.7%, mean |gap| 0.4% (4 runs)
  - `learning_rate=0.005`, `early_stopping=20`: this claim +0.2%, mean |gap| 0.5% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | no difference in reporting: the numbers as printed at the end of the run | settings | 32% | 0.8 sigma (fits every claim) | the settings search and the other classes |
| 2 | the setting epochs=50 | settings | 19% | 0.9 sigma (fits every claim) | run with epochs=50 |
| 3 | the setting epochs=200, learning_rate=0.005 | settings | 10% | 0.6 sigma (fits every claim) | run with epochs=200, learning_rate=0.005 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `learning_rate`: learning_rate=0.005 (max I 0.58)
  - `epochs, learning_rate`: epochs=200, learning_rate=0.005 (max I 0.76)
  - `early_stopping`: early_stopping=2 (max I 0.77); early_stopping=50 (max I 0.77); early_stopping=100 (max I 0.92)
  - `epochs`: epochs=50 (max I 0.78); epochs=200 (max I 0.78)
  - `early_stopping, learning_rate`: early_stopping=20, learning_rate=0.005 (max I 0.79)
  - `@ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.div2`: @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.div2=1 (max I 0.82)
  - `early_stopping, epochs`: early_stopping=5, epochs=50 (max I 0.85)
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
- no hypothesis moved the gap by more than 1 noise units
- history matching: the naive configuration is within noise of every claim
- scale probe: the code's epochs as 0.5 x the paper's fits every swept claim after 9 runs at g(v) (C_trans_cora_f1 at epochs=50, C_trans_cora_f1@epochs=50 at epochs=25, C_trans_cora_f1@epochs=200 at epochs=100)
- scale probe: only 1 of the 3 swept claims were off as run, so the factor is at most an unsupported fit
- labelled Fits but unsupported: one factor (0.5 x the paper's) makes every one of the 3 swept claims fit
- patch round: {'@ast:pubmed-original_inductive_FastGCN.py:106:logging': 'False', 'epochs': '50'} fits every claim but did not pass verification
- mutation round: none of 1 mutants moved C_trans_cora_f1 toward the paper
- value interval stopped early: run budget of 150 reached (wanted 1 more run(s) of {'epochs': '35'} for 'interval epochs=35')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_trans_cora_f1 | C_trans_pubmed_f1 | C_ind_cora_f1 | C_ind_pubmed_f1 | Mean |gap| |
|---|---|---|---|---|---|---|
| `@ast:pubmed-original_inductive_FastGCN.py:106:logging=False`, `epochs=50` | 3 | +0.0% | +0.0% | +0.3% | -1.1% | 0.3% |
| `learning_rate=0.005`, `epochs=200` | 4 | -0.7% | -0.1% | +0.8% | +0.1% | 0.4% |
| `learning_rate=0.005`, `early_stopping=20` | 4 | +0.2% | -0.3% | +0.9% | -0.5% | 0.5% |
| `early_stopping=5`, `epochs=50` | 4 | -0.2% | -0.1% | +1.1% | -0.3% | 0.5% |
| `learning_rate=0.005`, `early_stopping=5` | 4 | -0.1% | -0.4% | -0.8% | -1.2% | 0.6% |

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
- Harness spec sha256: `157698c36f03fdffbf86da038e6d9ea538fa9a1a48eceb949b48dd8edeff2e42`
- Cost: Nemotron billed $0.0000, sandbox reported $45.4590 (total $45.4590; this search; ledger extraction is included only if it shared the search's router)
