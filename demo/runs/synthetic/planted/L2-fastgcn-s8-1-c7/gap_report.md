# Gap Report: planted L2-fastgcn-s8-1

Artifact `fastgcn` · generated 2026-10-26 11:08 · 142 branch runs (0 build/load setups) · sandbox $46.3261

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_trans_cora_f1 (trans_cora_acc) | Fits but unsupported | +3.0% | +2.2% | ±1.0% | `@ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.div2=1` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_trans_pubmed_f1 (`trans_pubmed_acc`): paper 0.756, measured 0.772 (+2.1%, band ±1.0%)

## C_trans_cora_f1: trans_cora_acc (paper 0.772)
**Fits but unsupported** · gap +3.0% → +2.2% · 80 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0056`, `B0141`, `B0142` (3 run(s) of the same config)
- Config: `@ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.div2` naive `0`, changed to `1`
- Command: not recorded
- Output: `trans_cora_acc` 0.787, 0.797, 0.789; gap after +2.2%
- Effect: candidate 0.789 minus naive 0.795 = -0.006, 95% bootstrap interval [-0.014, +0.0032] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `trans_cora_acc` = 0.772.

### What did we measure?
- Naive median 0.795 over 5 runs; repeats: 0.795, 0.8, 0.792, 0.805, 0.792
- Spread: range 0.792 to 0.805, noise band ±0.00795 (2 x MAD), CV 0.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +3.0% (noise band ±1.0% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- FAIL · Effect vs noise: candidate minus naive is -0.006 with a 95% bootstrap interval that includes 0

### What remains unknown?
- Untestable within the budget: `epochs=5000`, `epochs=10000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `learning_rate=0.015` (2.14 noise units, gap -0.8%); `hidden1=7` (1.89 noise units, gap +1.0%); `learning_rate=0.02` (1.13 noise units, gap -1.8%); `max_degree=1` (1.13 noise units, gap +1.8%)
- Near alternatives (closest across all claims):
  - `@ast:pubmed-original_transductive_FastGCN.py:57:@mut.18.Subscript.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLndoZXJlKHRyYWluX21hc2spWzBdKQ=1`: this claim +1.3%, mean |gap| 0.9% (3 runs)
  - `max_degree=150`, `learning_rate=0.015`: this claim +1.2%, mean |gap| 0.9% (4 runs)
  - `learning_rate=0.015`: this claim +1.9%, mean |gap| 1.1% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a code change: pubmed-original_transductive_FastGCN.py:57: `np.where(train_mask)[0]` -> `(lambda _v: _v[:max(1, len(_v) * 3 // 4)])(np.where(train_mask)[0])` | code | 38% | 0.8 sigma (fits every claim) | run with @ast:pubmed-original_transductive_FastGCN.py:57:@mut.18.Subscript.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLndoZXJlKHRyYWluX21hc2spWzBdKQ=1 (an in-memory code patch) |
| 2 | no difference in reporting: the numbers as printed at the end of the run | settings | 16% | 2.2 sigma (fits every claim) | the settings search and the other classes |
| 3 | a code change: @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.div2=1 | code | 12% | 1.7 sigma (fits every claim) | run with @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.div2=1 (an in-memory code patch) |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `@ast:pubmed-original_inductive_FastGCN.py:144:@mut.35.Call.red.mean`: @ast:pubmed-original_inductive_FastGCN.py:144:@mut.35.Call.red.mean=1 (max I 1.53)
  - `max_degree`: max_degree=150 (max I 1.62)
  - `hidden1, learning_rate`: hidden1=7, learning_rate=0.02 (max I 1.71)
  - `@ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.div2`: @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.div2=1 (max I 1.85)
  - `epochs, max_degree`: epochs=1000, max_degree=1 (max I 1.89)
  - `epochs, hidden1`: epochs=1000, hidden1=7 (max I 1.98)
  - `hidden1, max_degree`: hidden1=8, max_degree=150 (max I 2.07)
  - `learning_rate`: learning_rate=0.05 (max I 2.08); learning_rate=0.015 (max I 2.15)
  - `@ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.mul2`: @ast:pubmed-original_inductive_FastGCN.py:101:@mut.47.num.mul2=1 (max I 2.08)
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
- closest configuration tried: {'max_degree': '1', 'epochs': '200'} (gap +1.9%); it did not pass verification
- history matching: the naive configuration is within noise of every claim
- patch round: {'@ast:pubmed-original_inductive_FastGCN.py:144:@mut.35.Call.red.mean': '1'} fits every claim but did not pass verification
- mutation round: 2 equivalent code change(s) fit every claim (worst 1.7 sigma): pubmed-original_inductive_FastGCN.py:101: `0.0` -> `0.0`; pubmed-original_transductive_FastGCN.py:57: `np.where(train_mask)[0]` -> `(lambda _v: _v[:max(1, len(_v) * 3 // 4)])(np.where(train_mask)[0])`
- explained with a code change (tested in memory, no file edited): pubmed-original_inductive_FastGCN.py:101: `0.0` -> `0.0`; a code lead, not a confirmed cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_trans_cora_f1 | C_trans_pubmed_f1 | C_ind_cora_f1 | C_ind_pubmed_f1 | Mean |gap| |
|---|---|---|---|---|---|---|
| `@ast:pubmed-original_transductive_FastGCN.py:57:@mut.18.Subscript.set.KGxhbWJkYSBfdjogX3ZbOm1heCgxLCBsZW4oX3YpICogMyAvLyA0KV0pKG5wLndoZXJlKHRyYWluX21hc2spWzBdKQ=1` | 3 | +1.3% | +0.9% | +1.3% | -0.1% | 0.9% |
| `max_degree=150`, `learning_rate=0.015` | 4 | +1.2% | +2.4% | -0.1% | +0.0% | 0.9% |
| `learning_rate=0.015` | 4 | +1.9% | +2.2% | -0.1% | +0.3% | 1.1% |
| `epochs=200`, `max_degree=1` | 3 | +1.9% | +2.9% | +0.3% | +0.1% | 1.3% |
| `early_stopping=500`, `learning_rate=0.02` | 3 | +1.9% | +3.2% | -0.3% | +0.0% | 1.4% |

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
- Harness spec sha256: `75065126be3c800f85a528a91d20372d728e4e6bc0f5e33795bed37308a597d3`
- Cost: Nemotron billed $0.0000, sandbox reported $46.3261 (total $46.3261; this search; ledger extraction is included only if it shared the search's router)
