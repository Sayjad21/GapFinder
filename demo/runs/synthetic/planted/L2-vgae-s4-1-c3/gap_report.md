# Gap Report: planted L2-vgae-s4-1

Artifact `vgae` · generated 2026-10-22 18:32 · 150 branch runs (0 build/load setups) · sandbox $797.7116

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_vgae_cora_auc (vgae_cora_auc) | Fits but unsupported | +3.1% | +0.9% | ±1.0% | `learning_rate=0.015` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **How the code computes the reported number** (test-score selection, label-based edits, switches fixed for evaluation):
  - `gae/preprocessing.py:76`: `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed
  - `gae/preprocessing.py:79`: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed
  - `gae/preprocessing.py:106`: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed
- **Held-out claims outside noise:**
  - C_vgae_cora_ap (`vgae_cora_ap`): paper 86.17, measured 88.13 (+2.3%, band ±1.0%)
  - C_vgae_citeseer_auc (`vgae_citeseer_auc`): paper 83.6, measured 86.9 (+3.9%, band ±1.0%)
  - C_vgae_citeseer_ap (`vgae_citeseer_ap`): paper 86.15, measured 88.83 (+3.1%, band ±1.0%)
  - C_gae_cora_auc (`gae_cora_auc`): paper 82.98, measured 84.78 (+2.2%, band ±1.3%)
  - C_gae_cora_ap (`gae_cora_ap`): paper 85.03, measured 87.38 (+2.8%, band ±1.5%)
  - C_gae_citeseer_auc (`gae_citeseer_auc`): paper 82.92, measured 85.76 (+3.4%, band ±1.4%)
  - C_gae_citeseer_ap (`gae_citeseer_ap`): paper 84.1, measured 87.61 (+4.2%, band ±3.4%)

## C_vgae_cora_auc: vgae_cora_auc (paper 83.18)
**Fits but unsupported** · gap +3.1% → +0.9% · 49 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0043`, `B0082`, `B0083`, `B0091` (4 run(s) of the same config)
- Config: `learning_rate` naive `0.01`, changed to `0.015`
- Command:

  Replay: fork checkpoint `b87946e7-74f5-4d81-bf4d-f55f3eafc206` and run
  ```
  @ast:gae/preprocessing.py:32:test_percent=30.0 @ast:gae/preprocessing.py:32:val_percent=20.0 @ast:gae/preprocessing.py:76:replace=True @ast:gae/preprocessing.py:40:@mut.11.Call.red.mean=0 @ast:gae/optimizer.py:15:@mut.22.Call.xdiv2=0 @ast:gae/optimizer.py:15:@mut.22.Call.xmul2=0 @ast:gae/optimizer.py:16:@mut.26.Call.xdiv2=0 @ast:gae/optimizer.py:16:@mut.26.Call.xmul2=0 @ast:gae/optimizer.py:37:@mut.22.Call.xdiv2=0 RUN_TAG=c03f595a19d7 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; export TF_CPP_MIN_LOG_LEVEL=2 OMP_NUM_THREADS=2; mkdir -p out; A="--learning_rate 0.02 --epochs 200 --hidden1 32 --hidden2 16 --weight_decay 0.0 --dropout 0.0 --features 1"; cd gae; for ds in cora citeseer; do PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_vae --dataset $ds $A > ../out/vgae_$ds.log 2>&1 & PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --model gcn_ae --dataset $ds $A > ../out/gae_$ds.log 2>&1 & wait; done; cd ..; bash gf_harness/emit.sh
  ```
- Output: `vgae_cora_auc` 83.97, 83.88, 84.38, 83.84; gap after +0.9%; result checkpoint `ca497663-99fb-46f9-a9a5-bbb9122d7178`
- Effect: candidate 83.92 minus naive 85.8 = -1.87, 95% bootstrap interval [-3.562, -1.214] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `vgae_cora_auc` = 83.18.

### What did we measure?
- Naive median 85.8 over 5 runs; repeats: 85.8, 85.53, 85.42, 87.89, 86.05
- Spread: range 85.42 to 87.89, noise band ±0.8579 (2 x MAD), CV 1.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +3.1% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `learning_rate` the gap is +3.1% (it comes back)
- PASS · Held-out claim: C_vgae_cora_auc@learning_rate=0.005 at learning_rate=0.0075: n/a to +0.7% (not worse beyond noise)
- PASS · Held-out claim: C_vgae_cora_auc@learning_rate=0.02 at learning_rate=0.03: n/a to -0.2% (not worse beyond noise)
- FAIL · Evidence: `learning_rate=0.015`: no evidence mentions '0.02'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -1.87 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `learning_rate=0.05` (2.94 noise units, gap -0.1%); `hidden2=80` (2.78 noise units, gap -0.3%); `hidden2=3` (2.56 noise units, gap -0.5%); `hidden1=3200` (2.54 noise units, gap +0.5%); `epochs=800` (2.39 noise units, gap -0.7%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `learning_rate=0.02`: this claim -0.6%, mean |gap| 0.8% (4 runs)
  - `hidden2=80`: this claim +1.0%, mean |gap| 1.1% (4 runs)
  - `hidden1=3200`: this claim +0.4%, mean |gap| 1.1% (4 runs)

### Equally good configurations
The target claim can't tell these 7 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `learning_rate=0.02` (reported)
- `hidden1=3200`
- `epochs=600`
- `learning_rate=0.015`
- `hidden2=80`
- `hidden2=3`
- `@ast:gae/preprocessing.py:76:replace=False, epochs=600`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting epochs=600 | settings | 32% | 1.0 sigma (fits every claim) | run with epochs=600 |
| 2 | the setting learning_rate=0.015 | settings | 26% | 1.2 sigma (fits every claim) | run with learning_rate=0.015 |
| 3 | the setting hidden1=3200 | settings | 19% | 1.4 sigma (fits every claim) | run with hidden1=3200 |

### History matching (every measured configuration, all claims together)
- 14 of 66 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs`: epochs=600 (max I 1.04); epochs=400 (max I 1.77)
  - `learning_rate`: learning_rate=0.02 (max I 1.16); learning_rate=0.015 (max I 1.69)
  - `hidden1`: hidden1=3200 (max I 1.26); hidden1=16 (max I 1.81); hidden1=1600 (max I 2.45)
  - `hidden2`: hidden2=32 (max I 1.63); hidden2=80 (max I 1.91)
  - `hidden1, hidden2`: hidden1=3200, hidden2=80 (max I 1.7)
- 5 separate islands (no single-knob move joins them): hidden1=3200; hidden2=32; hidden1=3200, hidden2=80 | epochs=600; epochs=400; epochs=800 | learning_rate=0.02; learning_rate=0.015 | @ast:gae/preprocessing.py:32:val_percent=40
- Leads outside the settings (static code checks, nothing run; check these first):
  - eval switch: `choice(..., replace=True)` on evaluation data: it changes how the evaluation is computed (`gae/preprocessing.py:76`)
  - eval switch: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed (`gae/preprocessing.py:79`)
  - eval switch: `in1d(..., assume_unique=True)` on evaluation data: it changes how the evaluation is computed (`gae/preprocessing.py:106`)
  - unexposed setting: `mask_test_edges(..., test_percent=30)`: a default no call in the repo overrides (1 call(s)) (`gae/preprocessing.py:32`)
  - unexposed setting: `mask_test_edges(..., val_percent=20)`: a default no call in the repo overrides (1 call(s)) (`gae/preprocessing.py:32`)
  - unexposed setting: `choice(..., replace=True)`: a switch fixed in the call; no flag sets it (`gae/preprocessing.py:76`)
  - unexposed setting: `in1d(..., assume_unique=True)`: a switch fixed in the call; no flag sets it (`gae/preprocessing.py:78`)
  - unexposed setting: `in1d(..., assume_unique=True)`: a switch fixed in the call; no flag sets it (`gae/preprocessing.py:79`)
- Equally good values: `learning_rate` in {0.015, 0.02}

Notes:
- configurations the target claim can't tell apart from the answer: learning_rate=0.02; hidden1=3200; epochs=600; learning_rate=0.015; hidden2=80; hidden2=3
- equally good values within one noise band (measured): learning_rate in {0.015, 0.02}
- discrimination: the paper's other conditions (C_vgae_cora_auc@learning_rate=0.005, C_vgae_cora_auc@learning_rate=0.02) don't yet tell the equally good fits apart: learning_rate=0.02 49%; epochs=600 22%; learning_rate=0.015 14%
- scale probe: the code's learning_rate as 1.5 x the paper's fits every swept claim after 8 runs at g(v) (C_vgae_cora_auc at learning_rate=0.015, C_vgae_cora_auc@learning_rate=0.005 at learning_rate=0.0075, C_vgae_cora_auc@learning_rate=0.02 at learning_rate=0.03)
- scale probe: only 0 of the 3 swept claims were off as run, so the factor is at most an unsupported fit
- labelled Fits but unsupported: one factor (1.5 x the paper's) makes every one of the 3 swept claims fit; it replaces {'learning_rate': '0.02'}
- patch round: {'@ast:gae/preprocessing.py:76:replace': 'False', 'epochs': '600'} also fits every claim (Fits but unsupported), but doesn't beat {'learning_rate': '0.015'}
- patch round: {'@ast:gae/preprocessing.py:76:replace': 'False', 'epochs': '600'} fits every claim as well as the answer; the claims can't tell them apart
- mutation round: none of 6 mutants moved C_vgae_cora_auc toward the paper
- value interval stopped early: run budget of 150 reached (wanted 1 more run(s) of {'learning_rate': '0.01061'} for 'interval learning_rate=0.01061')
- not identifiable from the paper's numbers: 3 configurations of different knobs fit every claim as well as the answer (hidden1=3200; learning_rate=0.015; learning_rate=0.02), and the paper's other conditions (C_vgae_cora_auc@learning_rate=0.005, C_vgae_cora_auc@learning_rate=0.02) don't separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_vgae_cora_auc | C_vgae_cora_ap | C_vgae_citeseer_auc | C_vgae_citeseer_ap | C_gae_cora_auc | C_gae_cora_ap | C_gae_citeseer_auc | C_gae_citeseer_ap | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| `learning_rate=0.02` | 4 | -0.6% | -0.9% | +1.6% | +1.1% | +0.7% | -0.1% | +1.1% | +0.1% | 0.8% |
| `hidden2=80` | 4 | +1.0% | +0.6% | -2.3% | -2.2% | +0.4% | +1.3% | -0.5% | -0.4% | 1.1% |
| `hidden1=3200` | 4 | +0.4% | -0.0% | -0.3% | -1.0% | +0.6% | +1.5% | +1.7% | +3.5% | 1.1% |
| `learning_rate=0.015` | 4 | +0.9% | +0.3% | +1.6% | +1.1% | +0.6% | +0.2% | +2.3% | +2.5% | 1.2% |
| `epochs=600` | 4 | +0.9% | +0.5% | +0.8% | +0.5% | -1.4% | -0.1% | -3.8% | -1.9% | 1.2% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
4 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `epochs`: count (range() bound at gae/train.py:142)
- `learning_rate`: rate (optimizer.learning_rate (AdamOptimizer) at gae/optimizer.py:37)

## Provenance
- GapFinder commit: `96f43d9d872690442737d0ad342eeb7d86352416` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `c4c29fe426cb05636b2801a35a0720a28235827c742cd4be4e3cf17305e715e5`
- Cost: Nemotron billed $0.0000, sandbox reported $797.7116 (total $797.7116; this search; ledger extraction is included only if it shared the search's router)
