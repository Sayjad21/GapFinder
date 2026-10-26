# Gap Report: MC Dropout (Gal & Ghahramani 2016)

Artifact `mcd` · generated 2026-10-26 20:42 · 200 branch runs (1 build/load setups) · sandbox $2877.0220

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_energy_rmse (energy_rmse) | Explains target, conflicts with held-out | -74.6% | +4.3% | ±2.6% | `epochx=10`, `hidden=1` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: energy_rmse 1.66 > yacht_rmse 1.11; measured: energy_rmse 0.4217 < yacht_rmse 0.8941 (margin -0.472, noise 0.208)
- **Held-out claims outside noise:**
  - C_yacht_rmse (`yacht_rmse`): paper 1.11, measured 0.8941 (-19.5%, band ±18.3%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `n_hidden.txt`: "1024 hidden units" (p.5)
  - `dropout_placement`: "dropout applied before every weight layer" (p.2)
  - `normalization`: "We centred and normalised both datasets" (p.4)
  - `dropout_variant`: "our results carry to other variants of dropout as well (such as drop-connect (Wan et al., 2013), multiplicative Gaussian noise (Srivastava et al., 2014), etc.)" (p.2)
  - `RL_exploration_method`: "Thompson sampling (Thompson, 1933) can be used to learn much faster" (p.1)

## C_energy_rmse: energy_rmse (paper 1.66)
**Explains target, conflicts with held-out** · gap -74.6% → +4.3% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0089`, `B0128`, `B0149`, `B0150`, `B0151` (5 run(s) of the same config)
- Config: `epochx` naive `500`, changed to `10`
- Config: `hidden` naive `2`, changed to `1`
- Command: not recorded
- Output: `energy_rmse` 1.754, 1.694, 1.669, 1.879, 1.731; gap after +4.3%
- Effect: candidate 1.731 minus naive 0.4217 = +1.31, 95% bootstrap interval [+1.261, +1.457] (5 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `energy_rmse` = 1.66.

### What did we measure?
- Naive median 0.4217 over 5 runs; repeats: 0.432, 0.4217, 0.3521, 0.4429, 0.3473
- Spread: range 0.3473 to 0.4429, noise band ±0.04244 (2 x MAD), CV 11.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -74.6% (noise band ±2.6% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +1.31 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `n_splits=30`, `n_splits=150`, `n_splits=300`
- Not settable with this harness: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochx=2` (24.7 noise units, gap +11.5%); `epochx=5` (8.06 noise units, gap -54.0%); `epochx=1` (4.7 noise units, gap +62.6%)
- Near alternatives (closest across all claims):
  - `epochx=50`, `hidden=5`: this claim -69.7%, mean |gap| 35.7% (2 runs)
  - `epochx=100`: this claim -73.6%, mean |gap| 38.0% (6 runs)
  - `epochx=250`: this claim -76.6%, mean |gap| 40.1% (6 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 83% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | the setting epochx=10, hidden=1 | settings | 17% | 2.9 sigma (fits every claim) | run with epochx=10, hidden=1 |
| 3 | no difference in reporting: the numbers as printed at the end of the run | settings | 0% | 13.0 sigma | the settings search and the other classes |

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 4 tested configuration(s) fit C_energy_rmse, and every other claim (C_yacht_rmse) fits some tested configuration, but none of the 42 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- Fit C_energy_rmse alone (4; worst claim's implausibility in brackets, lowest is the least inconsistent): epochx=10, hidden=1 (13.29); epochx=1, hidden=20 (17.46); epochx=1, hidden=5 (19.38); epochx=2 (23.67)

Notes:
- {'epochx': '2'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'epochx': '2'} (gap +9.4%); it did not pass verification
- spec knobs no ledger assumption names (n_splits) were screened too; no better answer
- history matching: out-of-space suspected: 4 tested configuration(s) fit C_energy_rmse, and every other claim (C_yacht_rmse) fits some tested configuration, but none of the 42 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- {'epochx': '10', 'hidden': '1'} matches C_energy_rmse (I=0.88) but breaks C_yacht_rmse (I=13.29); no tested condition matches all claims, so the rest of the gap probably lies in code, data or evaluation, which GapFinder doesn't change
- value interval stopped early: run budget of 200 reached (wanted 1 more run(s) of {'epochx': '15', 'hidden': '1'} for 'interval epochx=15')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_energy_rmse | C_yacht_rmse | Mean |gap| |
|---|---|---|---|---|
| `epochx=50`, `hidden=5` | 2 | -69.7% | +1.7% | 35.7% |
| `epochx=100` | 6 | -73.6% | -2.4% | 38.0% |
| `epochx=250` | 6 | -76.6% | -3.6% | 40.1% |
| `epochx=100`, `hidden=5` | 2 | -69.3% | -11.0% | 40.2% |
| `hidden=1`, `epochx=50` | 5 | -63.4% | -17.0% | 40.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `epochx=5000`: other, The value 5000 exceeds the allowed maximum for epochx (likely 2000), causing the program to reject it; a lower but still large value like 2000 preserves the intent of many training epochs. [not taken as invalid_value: the log shows no rejection]
- `hidden=20`: other, The program rejected hidden=20, likely because it expects hidden size to be a power of two or within a specific range; 16 is the nearest valid value that maintains the intent of increasing the hidden layer size beyond the default. [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `n_splits=30`, `n_splits=150`, `n_splits=300`

## Knob names
- Screened though no assumption named them (low prior, code-derived values): `n_splits`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `03cc5e006f242382f56af9ae32ddfb1e1ff0fcbbb9bf40c5b17ca7de3e0e2cb6`
- Cost: Nemotron billed $0.0024, sandbox reported $2877.0220 (total $2877.0244; this search; ledger extraction is included only if it shared the search's router)
