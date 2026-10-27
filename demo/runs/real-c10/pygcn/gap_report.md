# Gap Report: pygcn (Kipf & Welling 2017)

Artifact `pygcn` · generated 2026-10-27 09:49 · 164 branch runs (0 build/load setups) · sandbox $27.4276

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_cora (cora_acc) | Fits but unsupported | +1.5% | -0.2% | ±1.2% | `weight_decay=0.0` |

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
**Fits but unsupported** · gap +1.5% → -0.2% · 50 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0018`, `B0019`, `B0036` (4 run(s) of the same config)
- Config: `weight_decay` naive `5e-4`, changed to `0.0`
- Command:

  Replay: fork checkpoint `69abd25a-45ee-4e12-8b94-2cfde545816c` and run
  ```
  @ast:pygcn/utils.py:69:@mut.14.Call.red.mean=0 @ast:pygcn/utils.py:70:@mut.11.BinOp.xdiv2=0 @ast:pygcn/utils.py:70:@mut.11.Name.xdiv2=0 @ast:pygcn/utils.py:70:@mut.11.BinOp.xmul2=0 @ast:pygcn/utils.py:70:@mut.11.Name.xmul2=0 @ast:pygcn/utils.py:70:@mut.21.Call.xdiv2=0 @ast:pygcn/train.py:17:default=False @ast:pygcn/train.py:19:default=False RUN_TAG=7c05fcf25091 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; mkdir -p out; S=$(( $(printf %s "$RUN_TAG" | cksum | cut -d" " -f1) % 100000 )); cd pygcn && PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --no-cuda --seed $S --epochs 200 --lr 0.01 --weight_decay 0.0 --hidden 16 --dropout 0.5 > ../out/run.log 2>&1; cd ..; bash gf_harness/emit.sh
  ```
- Output: `cora_acc` 81.3, 81.4, 80.3, 82.5; gap after -0.2%; result checkpoint `80d29d3b-736b-4553-b320-e7a7a6720fe6`
- Effect: candidate 81.35 minus naive 82.7 = -1.35, 95% bootstrap interval [-2.94, +0.94] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `cora_acc` = 81.5.

### What did we measure?
- Naive median 82.7 over 5 runs; repeats: 82.7, 83.2, 83.4, 80.9, 82.4
- Spread: range 80.9 to 83.4, noise band ±1 (2 x MAD), CV 1.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +1.5% (noise band ±1.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `weight_decay` the gap is +1.5% (it comes back)
- NOT CHECKED · Held-out claim: no held-out claims were checked
- FAIL · Evidence: `weight_decay=0.0`: no evidence mentions '0.0'; it fits, but nothing says the authors used it
- FAIL · Effect vs noise: candidate minus naive is -1.35 with a 95% bootstrap interval that includes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: `framework`, `--no-cuda`, `--seed`, `early_stopping_window`, `weight_initialization`, `feature_normalization`, `dataset_splits`, `test_set_size`, `validation_set_size`, `hyperparam_opt_dataset`, `adjacency_matrix`, `propagation_model`, `num_layers`, `residual_connections`, `--fastmode`, `label_rate`, `random_graph_hidden`, `random_graph_regularization`, `nell_preprocessing`, `optimizer`, `random_graph_feature_matrix`, `random_graph_edges`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `weight_decay=5e-06` (1.1 noise units, gap -0.1%)
- Near alternatives (closest across all claims):
  - `weight_decay=5e-06`: this claim +0.0%, mean |gap| 0.0% (4 runs)
  - `@ast:pygcn/train.py:19:default=True`, `weight_decay=0.0`: this claim -0.4%, mean |gap| 0.4% (3 runs)
  - `hidden=800`: this claim +0.7%, mean |gap| 0.7% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | no difference in reporting: the numbers as printed at the end of the run | settings | 32% | 0.8 sigma (fits every claim) | the settings search and the other classes |
| 2 | the setting weight_decay=0.0 | settings | 21% | 0.1 sigma (fits every claim) | run with weight_decay=0.0 |
| 3 | a code change: @ast:pygcn/train.py:19:default=True, weight_decay=0.0 | code | 7% | 0.2 sigma (fits every claim) | run with @ast:pygcn/train.py:19:default=True, weight_decay=0.0 (an in-memory code patch) |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `@ast:pygcn/train.py:17:default`: @ast:pygcn/train.py:17:default=True (max I 0.06)
  - `weight_decay`: weight_decay=0.0 (max I 0.09); weight_decay=5e-06 (max I 0.31); weight_decay=1e-5 (max I 0.46)
  - `@ast:pygcn/train.py:19:default, weight_decay`: @ast:pygcn/train.py:19:default=True, weight_decay=0.0 (max I 0.24)
  - `@ast:pygcn/train.py:17:default, weight_decay`: @ast:pygcn/train.py:17:default=True, weight_decay=0.0 (max I 0.43)
  - `hidden`: hidden=800 (max I 0.53); hidden=80 (max I 0.84)
  - `@ast:pygcn/train.py:19:default`: @ast:pygcn/train.py:19:default=True (max I 0.68)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:17`)
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:19`)
- Where the code differs from the paper (model-proposed, checked against the repo; literal ones were tried as patch knobs, structural ones are not tested):
  - `pygcn/utils.py:42`: paper says validation set of 500 labeled examples for hyperparameter optimization; code does validation set uses indices 200-499 (300 examples)
  - `pygcn/train.py:100`: paper says early stopping with a window size of 10, i.e. we stop training if the validation loss does not decrease for 10 consecutive epochs; code does trains for fixed number of epochs (args.epochs) without early stopping
  - `pygcn/models.py:16`: paper says dropout rate for all layers; code does dropout applied only after the first GCN layer
  - `pygcn/train.py:49`: paper says L2 regularization factor for the first GCN layer; code does weight_decay applied to all model parameters via Adam optimizer

Notes:
- no hypothesis moved the gap by more than 1 noise units
- spec knobs no ledger assumption names (dropout, epochs, hidden, lr) were screened too; no better answer
- the gap (+1.5%) is below the minimum detectable effect (±3.7% with 3 runs per configuration at 80% power): even a setting that closed it couldn't have been confirmed, so 'nothing explains it' can't be claimed either
- explained with a code patch (tested in memory, no file edited): pygcn/train.py line 19: default = False -> True
- weight_decay: values from 0 to 3.344e-05 fit every claim (a bisection, 3 runs a side, one run a value: approximate)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_cora | Mean |gap| |
|---|---|---|---|
| `weight_decay=5e-06` | 4 | +0.0% | 0.0% |
| `weight_decay=0.0` | 4 | -0.2% | 0.2% |
| `@ast:pygcn/train.py:19:default=True`, `weight_decay=0.0` | 3 | -0.4% | 0.4% |
| `hidden=800` | 4 | +0.7% | 0.7% |
| `weight_decay=1e-5` | 4 | +0.8% | 0.8% |

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
- GapFinder commit: `7e3568335cda944b166665fca73315f0b4a5e13a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fda96eca7742f5761e79cebbd776eea71f09237739dfb51f4056cc1eb7cce43b`
- Cost: Nemotron billed $0.0083, sandbox reported $27.4276 (total $27.4359; this search; ledger extraction is included only if it shared the search's router)
