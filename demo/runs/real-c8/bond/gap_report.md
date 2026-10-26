# Gap Report: BOND / DOMINANT (batch-5)

Artifact `harness-c7` · generated 2026-10-27 01:12 · 47 branch runs (0 build/load setups) · sandbox $1503.3407

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_auc (c_auc) | Unexplained | -8.2% | -8.2% | ±1.3% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_ap (`c_ap`): paper 20, measured 17.09 (-14.6%, band ±4.2%)
  - C_rec (`c_rec_recall`): paper 23.8, measured 25.29 (+6.3%, band ±2.1%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `B.1 Hardware configuration`: "Hardware configuration. All the experiments were performed on a Linux server with a 3.50GHz Intel Core i5 CPU, 64GB RAM, and 1 NVIDIA GTX 1080 Ti GPU with 12GB memory." (p.19)
  - `gpu`: "OOM denotes out of memory with regard to GPU (_G) and CPU (_C)" (p.6)

## C_auc: c_auc (paper 82.7)
**Unexplained** · gap -8.2% → -8.2% · 14 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (14 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `c_auc` = 82.7.

### What did we measure?
- Naive median 75.89 over 5 runs; repeats: 75.04, 76.43, 76.31, 73.89, 75.89
- Spread: range 73.89 to 76.43, noise band ±1.08 (2 x MAD), CV 1.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -8.2% (noise band ±1.3% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `B.1 Hardware configuration`, `init_model_hyperparams`, `num_trial`, `gpu`, `seed`, `oom_handling`, `time_limit`, `eval_roc_auc`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 100% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | library drift: pygod==0.3.0, pyod==1.0.2, scikit-learn==1.1.1, torch-geometric==2.0.4, tqdm==4.64.0 (as of the paper's date) | library | 0% | 4.2 sigma | run with gf_paper_year_env=all |
| 3 | no difference in reporting: the numbers as printed at the end of the run | settings | 0% | 5.0 sigma | the settings search and the other classes |

### Library drift and the paper-era code
- Packages as of the paper's date change the numbers; the culprit: `pygod==0.3.0`, `pyod==1.0.2`, `scikit-learn==1.1.1`, `torch-geometric==2.0.4`, `tqdm==4.64.0`

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 1 tested configuration(s) fit C_auc, and every other claim (C_ap, C_rec) fits some tested configuration, but none of the 20 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `weight_decay = 0.01` is fixed in the code; no flag sets it (`benchmark/utils.py:11`)
  - unexposed setting: `epoch = 300` is fixed in the code; no flag sets it (`benchmark/utils.py:21`)
  - unexposed setting: `__init__(..., weight=0.5)`: a default no call in the repo overrides (31 call(s)) (`pygod/detector/dominant.py:98`)
  - unexposed setting: `logger(..., train=True)`: a switch fixed in the call; no flag sets it (`pygod/detector/base.py:485`)
  - unexposed setting: `batch_size = 64` is fixed in the code; no flag sets it (`benchmark/utils.py:15`)
  - unexposed setting: `epoch = 2` is fixed in the code; no flag sets it (`benchmark/utils.py:17`)
  - unexposed setting: `__init__(..., w1=0.2)`: a default no call in the repo overrides (31 call(s)) (`pygod/detector/adone.py:113`)
  - unexposed setting: `__init__(..., w2=0.2)`: a default no call in the repo overrides (31 call(s)) (`pygod/detector/adone.py:113`)

Notes:
- no hypothesis moved the gap by more than 1 noise units
- spec knobs no ledger assumption names (@ast:benchmark/utils.py:11:weight_decay, @ast:benchmark/utils.py:15:batch_size, @ast:benchmark/utils.py:17:epoch, @ast:benchmark/utils.py:21:epoch, @ast:pygod/detector/adone.py:113:hid_dim, @ast:pygod/detector/adone.py:113:num_layers, @ast:pygod/detector/adone.py:113:lr, @ast:pygod/detector/adone.py:113:epoch, gf_paper_year_env, gf_paper_era_code) were screened too; no better answer
- history matching: out-of-space suspected: 1 tested configuration(s) fit C_auc, and every other claim (C_ap, C_rec) fits some tested configuration, but none of the 20 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- closest fit {'@ast:pygod/detector/dominant.py:98:weight': '0.95'} (I=0.56) has a single run; not labelled until it is repeated
- patch round: none of 14 code-patch configurations fits every claim
- mutation round: none of 4 mutants moved C_auc toward the paper
- library: pygod 0.3.0 and pyod 1.0.2 and scikit-learn 1.1.1 and torch-geometric 2.0.4 and tqdm 4.64.0 together gives the numbers of every package as of the paper's date
- library probe stopped early: its share of the run budget (15 runs) is used

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_auc | C_ap | C_rec | Mean |gap| |
|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | -8.2% | -14.6% | +6.3% | 9.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `@ast:benchmark/utils.py:21:epoch=3000`: other, The benchmark utility likely enforces a maximum epoch count (e.g., 1000) and rejects values above that; 3000 exceeded the limit, causing the failure. [not taken as invalid_value: the log shows no rejection]

## Knob names
- Screened though no assumption named them (low prior, code-derived values): `@ast:benchmark/utils.py:11:weight_decay`, `@ast:benchmark/utils.py:15:batch_size`, `@ast:benchmark/utils.py:17:epoch`, `@ast:benchmark/utils.py:21:epoch`, `@ast:pygod/detector/adone.py:113:hid_dim`, `@ast:pygod/detector/adone.py:113:num_layers`, `@ast:pygod/detector/adone.py:113:lr`, `@ast:pygod/detector/adone.py:113:epoch`, `gf_paper_year_env`, `gf_paper_era_code`

## Runtime trace (one dry run)
3 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `@ast:benchmark/utils.py:11:weight_decay`: rate0 (optimizer.weight_decay (Adam) at pygod/detector/base.py:443)
- `@ast:benchmark/utils.py:21:epoch`: count (range() bound at pygod/detector/base.py:456)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `B.1 Hardware configuration`, `init_model_hyperparams`, `num_trial`, `gpu`, `seed`, `oom_handling`, `time_limit`, `eval_roc_auc`

## Provenance
- GapFinder commit: `1b6bf29f1932c85ef4fb628d082c8fc243a37b95` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `1d2ae10f49c75d62fa912e11d0e65a636fec58cfeb91d376ffbe858a289a85ba`
- Cost: Nemotron billed $0.0015, sandbox reported $1503.3407 (total $1503.3422; this search; ledger extraction is included only if it shared the search's router)
