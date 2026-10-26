# Gap Report: BOND / DOMINANT (batch-5)

Artifact `harness-c7` · generated 2026-10-26 20:12 · 80 branch runs (0 build/load setups) · sandbox $883.7037

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_auc (c_auc) | Unexplained | -8.9% | -8.9% | ±1.1% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_ap (`c_ap`): paper 20, measured 16.95 (-15.3%, band ±7.5%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `B.1 Hardware configuration`: "Hardware configuration. All the experiments were performed on a Linux server with a 3.50GHz Intel Core i5 CPU, 64GB RAM, and 1 NVIDIA GTX 1080 Ti GPU with 12GB memory." (p.19)
  - `gpu`: "OOM denotes out of memory with regard to GPU (_G) and CPU (_C)" (p.6)

## C_auc: c_auc (paper 82.7)
**Unexplained** · gap -8.9% → -8.9% · 16 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (16 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `c_auc` = 82.7.

### What did we measure?
- Naive median 75.34 over 5 runs; repeats: 76.31, 75.79, 75.34, 75.06, 74.13
- Spread: range 74.13 to 76.31, noise band ±0.9 (2 x MAD), CV 1.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -8.9% (noise band ±1.1% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `B.1 Hardware configuration`, `init_model_hyperparams`, `num_trial`, `gpu`, `seed`, `oom_handling`, `time_limit`, `eval_roc_auc`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `@ast:benchmark/utils.py:11:weight_decay=0.002`: this claim -8.6%, mean |gap| 9.9% (4 runs)
  - `@ast:benchmark/utils.py:11:weight_decay=0.005`: this claim -9.2%, mean |gap| 9.9% (2 runs)
  - `@ast:benchmark/utils.py:11:weight_decay=0.1`: this claim -9.2%, mean |gap| 11.0% (4 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting gf_paper_era_code=1829421d5aea6f1c663a7dd7448d78a608eec634 | library | 35% | 0.3 sigma (fits every claim) | run with gf_paper_era_code=1829421d5aea6f1c663a7dd7448d78a608eec634 |
| 2 | the setting gf_paper_era_code=d5f28cce45a99c7c69a7159f84b79e68bbea0b30 | library | 11% | 0.4 sigma (fits every claim) | run with gf_paper_era_code=d5f28cce45a99c7c69a7159f84b79e68bbea0b30 |
| 3 | a code change: @ast:pygod/detector/dominant.py:98:weight=0.8441 | code | 11% | 0.5 sigma (fits every claim) | run with @ast:pygod/detector/dominant.py:98:weight=0.8441 (an in-memory code patch) |

### Library drift and the paper-era code
- Packages as of the paper's date change the numbers; the culprit: `pygod==0.3.0`, `pyod==1.0.2`, `scikit-learn==1.1.1`, `torch-geometric==2.0.4`, `tqdm==4.64.0`
- `pygod` 0.3.1 changed them (0.3.0 gives the older numbers)
- `pygod` 0.4.0 changed them (0.3.1 gives the older numbers)
- `pyod` 1.0.3 changed them (1.0.2 gives the older numbers)
- `pyod` 1.0.4 changed them (1.0.3 gives the older numbers)
- The repository's last commit before the paper, `7de5d925ef` (2022-06-25), gives other numbers than the given commit
  - commit `b960645e46` (add security check) changed them: .github/workflows/codeql.yml
  - commit `d06e683218` (FIX issue #39) changed them: benchmark/main.py

### History matching (every measured configuration, all claims together)
- 12 of 34 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `gf_paper_era_code`: gf_paper_era_code=1829421d5aea6f1c663a7dd7448d78a608eec634 (max I 0.35); gf_paper_era_code=d5f28cce45a99c7c69a7159f84b79e68bbea0b30 (max I 0.36); gf_paper_era_code=8c3af8625b54e2eccb5caef3728d0f6f9e38c7cd (max I 0.5); gf_paper_era_code=446965b08858705fb3c77fae8a86348c949ecd63 (max I 0.56); +4 more
  - `@ast:pygod/detector/dominant.py:98:weight`: @ast:pygod/detector/dominant.py:98:weight=0.8441 (max I 0.48); @ast:pygod/detector/dominant.py:98:weight=0.75 (max I 1.68)
- 2 separate islands (no single-knob move joins them): gf_paper_era_code=1829421d5aea6f1c663a7dd7448d78a608eec634; gf_paper_era_code=d5f28cce45a99c7c69a7159f84b79e68bbea0b30; gf_paper_era_code=8c3af8625b54e2eccb5caef3728d0f6f9e38c7cd | @ast:pygod/detector/dominant.py:98:weight=0.8441; @ast:pygod/detector/dominant.py:98:weight=0.75; @ast:pygod/detector/dominant.py:98:weight=0.95
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
- history matching: 12 of 34 tested configurations fit every claim within 3 sigma
- patch round stopped early: run budget of 80 reached (wanted 1 more run(s) of {'gf_paper_era_code': '1829421d5aea6f1c663a7dd7448d78a608eec634', '@ast:benchmark/utils.py:21:epoch': '3000'} for 'patch screen')
- mutation round: none of 4 mutants moved C_auc toward the paper
- library: pygod 0.3.0 and pyod 1.0.2 and scikit-learn 1.1.1 and torch-geometric 2.0.4 and tqdm 4.64.0 together gives the numbers of every package as of the paper's date
- library: pygod 0.3.1 changed the numbers (0.3.0 gives the older ones)
- library: pygod 0.4.0 changed the numbers (0.3.1 gives the older ones)
- library: pyod 1.0.3 changed the numbers (1.0.2 gives the older ones)
- library: pyod 1.0.4 changed the numbers (1.0.3 gives the older ones)
- paper-era code: the commit 7de5d925ef (2022-06-25) gives other numbers
- paper-era code: commit b960645e46 (add security check) changed the numbers; it changed .github/workflows/codeql.yml
- paper-era code: commit d06e683218 (FIX issue #39) changed the numbers; it changed benchmark/main.py

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_auc | C_ap | C_rec | Mean |gap| |
|---|---|---|---|---|---|
| `@ast:benchmark/utils.py:11:weight_decay=0.002` | 4 | -8.6% | -15.0% | +6.2% | 9.9% |
| `@ast:benchmark/utils.py:11:weight_decay=0.005` | 2 | -9.2% | -16.5% | +4.1% | 9.9% |
| naive (reproduction as run) | 5 | -8.9% | -15.3% | +5.8% | 10.0% |
| `@ast:benchmark/utils.py:11:weight_decay=0.1` | 4 | -9.2% | -14.3% | +9.5% | 11.0% |
| `@ast:pygod/detector/dominant.py:98:weight=0.95` | 3 | +0.6% | -14.0% | -18.7% | 11.1% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `@ast:benchmark/utils.py:21:epoch=3000`: other, The program likely validates epoch against a maximum allowed value; 3000 exceeds this limit causing rejection. A value of 1000 preserves the intent of using a large number of epochs while staying within typical bounds. [not taken as invalid_value: the log shows no rejection]

## Knob names
- Screened though no assumption named them (low prior, code-derived values): `@ast:benchmark/utils.py:11:weight_decay`, `@ast:benchmark/utils.py:15:batch_size`, `@ast:benchmark/utils.py:17:epoch`, `@ast:benchmark/utils.py:21:epoch`, `@ast:pygod/detector/adone.py:113:hid_dim`, `@ast:pygod/detector/adone.py:113:num_layers`, `@ast:pygod/detector/adone.py:113:lr`, `@ast:pygod/detector/adone.py:113:epoch`, `gf_paper_year_env`, `gf_paper_era_code`

## Runtime trace (one dry run)
3 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `@ast:benchmark/utils.py:11:weight_decay`: rate0 (optimizer.weight_decay (Adam) at pygod/detector/base.py:443)
- `@ast:benchmark/utils.py:21:epoch`: count (range() bound at pygod/detector/base.py:456)
- 2 sink value(s) shared by several knobs: no role assigned

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `B.1 Hardware configuration`, `init_model_hyperparams`, `num_trial`, `gpu`, `seed`, `oom_handling`, `time_limit`, `eval_roc_auc`

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `1d2ae10f49c75d62fa912e11d0e65a636fec58cfeb91d376ffbe858a289a85ba`
- Cost: Nemotron billed $0.0000, sandbox reported $883.7037 (total $883.7037; this search; ledger extraction is included only if it shared the search's router)
