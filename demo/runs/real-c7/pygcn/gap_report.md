# Gap Report: pygcn (Kipf & Welling 2017)

Artifact `pygcn` · generated 2026-10-26 18:17 · 158 branch runs (0 build/load setups) · sandbox $28.9321

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_cora (cora_acc) | Fits but unsupported | +2.1% | +0.2% | ±1.2% | `weight_decay=5e-06` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `framework`: "We compare results on a GPU and on a CPU-only implementation4 in TensorFlow (Abadi et al., 2015)." (p.8)
  - `--seed`: "We trained and tested our model on the same dataset splits as in Yang et al. (2016) and report mean accuracy of 100 runs with random weight initializations." (p.7)
  - `early_stopping_window`: "early stopping with a window size of 10, i.e. we stop training if the validation loss does not decrease for 10 consecutive epochs." (p.6)
  - `weight_initialization`: "We initialize weights using the initialization described in Glorot & Bengio (2010) and accordingly (row-)normalize input feature vectors." (p.6)
  - `feature_normalization`: "We initialize weights using the initialization described in Glorot & Bengio (2010) and accordingly (row-)normalize input feature vectors." (p.6)
  - `dataset_splits`: "We choose the same dataset splits as in Yang et al. (2016) with an additional validation set of 500 labeled examples for hyperparameter optimization" (p.6)

## C_cora: cora_acc (paper 81.5)
**Fits but unsupported** · gap +2.1% → +0.2% · 50 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0015`, `B0034`, `B0035`, `B0038` (4 run(s) of the same config)
- Config: `weight_decay` naive `5e-4`, changed to `5e-06`
- Command:

  Replay: fork checkpoint `69abd25a-45ee-4e12-8b94-2cfde545816c` and run
  ```
  RUN_TAG=f24dc8537312 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; mkdir -p out; S=$(( $(printf %s "$RUN_TAG" | cksum | cut -d" " -f1) % 100000 )); cd pygcn && PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --no-cuda --seed $S --epochs 200 --lr 0.01 --weight_decay 5e-06 --hidden 16 --dropout 0.5 > ../out/run.log 2>&1; cd ..; bash gf_harness/emit.sh
  ```
- Output: `cora_acc` 83.3, 81.6, 81.8, 81.3; gap after +0.2%; result checkpoint `d53ec605-97cf-4f55-95d9-bc446504815b`
- Effect: candidate 81.7 minus naive 83.2 = -1.5, 95% bootstrap interval [-2.713, +0.03333] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `cora_acc` = 81.5.

### What did we measure?
- Naive median 83.2 over 5 runs; repeats: 83.7, 83.2, 81.2, 82.9, 84.3
- Spread: range 81.2 to 84.3, noise band ±1 (2 x MAD), CV 1.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +2.1% (noise band ±1.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `weight_decay` the gap is +2.1% (it comes back)
- NOT CHECKED · Held-out claim: no held-out claims were checked
- FAIL · Evidence: `weight_decay=5e-06`: no evidence mentions '5e-06'; it fits, but nothing says the authors used it
- FAIL · Effect vs noise: candidate minus naive is -1.5 with a 95% bootstrap interval that includes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: `framework`, `--no-cuda`, `--seed`, `early_stopping_window`, `weight_initialization`, `feature_normalization`, `dataset_splits`, `test_set_size`, `validation_set_size`, `hyperparam_opt_dataset`, `adjacency_matrix`, `propagation_model`, `num_layers`, `residual_connections`, `--fastmode`, `label_rate`, `random_graph_hidden`, `random_graph_regularization`, `nell_preprocessing`, `optimizer`, `random_graph_feature_matrix`, `random_graph_edges`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `weight_decay=0.0` (1.7 noise units, gap +0.0%)
- Near alternatives (closest across all claims):
  - `weight_decay=0.0`: this claim -0.6%, mean |gap| 0.6% (4 runs)
  - `weight_decay=1e-5`: this claim +1.0%, mean |gap| 1.0% (4 runs)
  - `hidden=80`: this claim +1.3%, mean |gap| 1.3% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | no difference in reporting: the numbers as printed at the end of the run | settings | 28% | 1.0 sigma (fits every claim) | the settings search and the other classes |
| 2 | the setting weight_decay=5e-06 | settings | 23% | 0.3 sigma (fits every claim) | run with weight_decay=5e-06 |
| 3 | a cause outside every class tested | outside | 8% |  | look for code, data or evaluation differences the classes don't cover |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `weight_decay`: weight_decay=5e-06 (max I 0.32); weight_decay=0.0 (max I 0.42); weight_decay=1e-5 (max I 0.65)
  - `hidden`: hidden=80 (max I 0.71); hidden=128 (max I 0.84); hidden=160 (max I 0.84); hidden=800 (max I 0.88)
  - `dropout`: dropout=0.25 (max I 0.84); dropout=0.0 (max I 0.86)
  - `epochs`: epochs=300 (max I 0.92)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:17`)
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:19`)
- Where the code differs from the paper (model-proposed, checked against the repo; literal ones were tried as patch knobs, structural ones are not tested):
  - `pygcn/train.py:100`: paper says early stopping with a window size of 10, i.e. we stop training if the validation loss does not decrease for 10 consecutive epochs; code does trains for a fixed 200 epochs without early stopping
  - `pygcn/utils.py:42`: paper says an additional validation set of 500 labeled examples for hyperparameter optimization; code does validation set of 300 labeled examples (range 200-500)
- Equally good values: `weight_decay` in {0.0, 5e-06, 1e-5}

Notes:
- equally good values within one noise band (measured): weight_decay in {0.0, 5e-06, 1e-5}
- spec knobs no ledger assumption names (dropout, epochs, hidden, lr) were screened too; no better answer
- patch round: {'@ast:pygcn/train.py:17:default': 'True'} fits every claim but did not pass verification
- weight_decay: values from 4.205e-07 to 1.495e-05 fit every claim (a bisection, 3 runs a side, one run a value: approximate)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_cora | Mean |gap| |
|---|---|---|---|
| `weight_decay=5e-06` | 4 | +0.2% | 0.2% |
| `weight_decay=0.0` | 4 | -0.6% | 0.6% |
| `weight_decay=1e-5` | 4 | +1.0% | 1.0% |
| `hidden=80` | 4 | +1.3% | 1.3% |
| `hidden=128` | 4 | +1.5% | 1.5% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `dropout`: fraction (dropout.p (torch.nn.functional.dropout) at pygcn/models.py:16)
- `epochs`: count (range() bound at pygcn/train.py:100)
- `lr`: rate (optimizer.lr (Adam) at pygcn/train.py:49)
- `weight_decay`: rate0 (optimizer.weight_decay (Adam) at pygcn/train.py:49)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `framework`, `--no-cuda`, `--seed`, `early_stopping_window`, `weight_initialization`, `feature_normalization`, `dataset_splits`, `test_set_size`, `validation_set_size`, `hyperparam_opt_dataset`, `adjacency_matrix`, `propagation_model`, `num_layers`, `residual_connections`, `--fastmode`, `label_rate`, `random_graph_hidden`, `random_graph_regularization`, `nell_preprocessing`, `optimizer`, `random_graph_feature_matrix`, `random_graph_edges`

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `dbbcc15f384db7a3ca32fa8292dfa06643946a56da69654de5843c4c0d96b244`
- Cost: Nemotron billed $0.0074, sandbox reported $28.9321 (total $28.9395; this search; ledger extraction is included only if it shared the search's router)
