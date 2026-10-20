# Gap Report: BOND: DOMINANT on inj_cora (b5c)

Artifact `harness` · generated 2026-10-20 16:20 · 17 branch runs (0 build/load setups) · sandbox $815.8741

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_auc (c_auc) | Unexplained | -9.2% | -9.2% | ±2.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_ap (`c_ap`): paper 20, measured 17.33 (-13.4%, band ±3.6%)
  - C_rec (`c_rec_recall`): paper 23.8, measured 26.56 (+11.6%, band ±3.6%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `B.1 Hardware configuration`: "Hardware configuration. All the experiments were performed on a Linux server with a 3.50GHz Intel Core i5 CPU, 64GB RAM, and 1 NVIDIA GTX 1080 Ti GPU with 12GB memory." (p.19)
  - `gpu`: "OOM denotes out of memory with regard to GPU (_G) and CPU (_C)" (p.6)

## C_auc: c_auc (paper 82.7)
**Unexplained** · gap -9.2% → -9.2% · 1 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (1 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `c_auc` = 82.7.

### What did we measure?
- Naive median 75.07 over 5 runs; repeats: 72.78, 75.88, 75.88, 74.37, 75.07
- Spread: range 72.78 to 75.88, noise band ±1.62 (2 x MAD), CV 1.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -9.2% (noise band ±2.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `B.1 Hardware configuration`, `init_model_hyperparams`, `num_trial`, `gpu`, `seed`, `oom_handling`, `time_limit`, `eval_roc_auc`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `@ast:pygod/detector/base.py:0:@call.Adam=SGD`, `@ast:pygod/detector/anomalous.py:0:@call.Adam=SGD`: this claim -7.2%, mean |gap| 11.3% (3 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C_auc, C_ap, among 0 tested
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `weight_decay = 0.01` is fixed in the code; no flag sets it (`benchmark/utils.py:11`)
  - unexposed setting: `batch_size = 64` is fixed in the code; no flag sets it (`benchmark/utils.py:15`)
  - unexposed setting: `epoch = 2` is fixed in the code; no flag sets it (`benchmark/utils.py:17`)
  - unexposed setting: `epoch = 300` is fixed in the code; no flag sets it (`benchmark/utils.py:21`)
  - unexposed setting: `DOMINANT(..., num_layers=4)`: fixed in the call; no flag sets it (`docs/examples/intro.py:64`)
  - unexposed setting: `DOMINANT(..., epoch=100)`: fixed in the call; no flag sets it (`docs/examples/intro.py:64`)
  - unexposed setting: `__init__(..., w1=0.2)`: a default no call in the repo overrides (31 call(s)) (`pygod/detector/adone.py:113`)
  - unexposed setting: `__init__(..., w2=0.2)`: a default no call in the repo overrides (31 call(s)) (`pygod/detector/adone.py:113`)
- Where the code differs from the paper (model-proposed, checked against the repo; literal ones were tried as patch knobs, structural ones are not tested):
  - `benchmark/main.py:13`: paper says we apply the same hyperparameter grid (see Appx. B) to each applicable algorithm and report its avg. performance (i.e., "algorithm performance in expectation"), along with the standard deviation (i.e., "algorithm stability") and the max (i.e., "algorithm potential").; code does runs a single configuration per dataset and does not compute average, std dev, or max across hyperparameter runs.
  - `pygod/detector/base.py:456`: paper says score converges (i.e., the score increment of consequence epochs is less than 0.5%), we mark the current epoch as optimal.; code does trains for a fixed 300 epochs without early stopping based on score convergence.

Notes:
- no hypothesis moved the gap by more than 1 noise units
- spec knobs no ledger assumption names (gf_paper_year_env) were screened too; no better answer
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C_auc, C_ap, among 0 tested
- patch round: {'@ast:pygod/detector/anomalous.py:0:@call.Adam': 'SGD', '@ast:pygod/detector/base.py:0:@call.Adam': 'SGD'} fitted every claim on one run, not after repeats

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_auc | C_ap | C_rec | Mean |gap| |
|---|---|---|---|---|---|
| `@ast:pygod/detector/base.py:0:@call.Adam=SGD`, `@ast:pygod/detector/anomalous.py:0:@call.Adam=SGD` | 3 | -7.2% | -8.0% | +18.7% | 11.3% |
| naive (reproduction as run) | 5 | -9.2% | -13.4% | +11.6% | 11.4% |

## Knob names
- Screened though no assumption named them (low prior, code-derived values): `gf_paper_year_env`

## Runtime trace (one dry run)
3 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `B.1 Hardware configuration`, `init_model_hyperparams`, `num_trial`, `gpu`, `seed`, `oom_handling`, `time_limit`, `eval_roc_auc`

## Provenance
- GapFinder commit: `e925a0fae7f1cc50e5f09a1b495decf401d47b77`
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `190cb22492d419505f57e466638b40f5832d36ed2dcddfe89eb466475d503291`
- Cost: Nemotron billed $0.0042, sandbox reported $815.8741 (total $815.8783; this search; ledger extraction is included only if it shared the search's router)
