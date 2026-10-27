# Gap Report: MC Dropout (Gal & Ghahramani 2016)

Artifact `mcd` · generated 2026-10-27 09:21 · 200 branch runs (1 build/load setups) · sandbox $2610.4146

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_energy_rmse (energy_rmse) | Explains target, conflicts with held-out | -78.4% | +2.1% | ±3.1% | `epochx=10`, `hidden=1` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: energy_rmse 1.66 > yacht_rmse 1.11; measured: energy_rmse 0.3594 < yacht_rmse 0.9746 (margin -0.615, noise 0.158)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `n_hidden.txt`: "1024 hidden units" (p.5)
  - `dropout_placement`: "dropout applied before every weight layer" (p.2)
  - `normalization`: "We centred and normalised both datasets" (p.4)
  - `dropout_variant`: "our results carry to other variants of dropout as well (such as drop-connect (Wan et al., 2013), multiplicative Gaussian noise (Srivastava et al., 2014), etc.)" (p.2)
  - `RL_exploration_method`: "Thompson sampling (Thompson, 1933) can be used to learn much faster" (p.1)

## C_energy_rmse: energy_rmse (paper 1.66)
**Explains target, conflicts with held-out** · gap -78.4% → +2.1% · 55 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0089`, `B0093`, `B0094`, `B0095`, `B0096`, `B0097` (6 run(s) of the same config)
- Config: `epochx` naive `500`, changed to `10`
- Config: `hidden` naive `2`, changed to `1`
- Command: not recorded
- Output: `energy_rmse` 1.696, 1.717, 1.693, 1.633, 1.737, 1.682; gap after +2.1%
- Effect: candidate 1.695 minus naive 0.3594 = +1.335, 95% bootstrap interval [+1.284, +1.378] (6 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `energy_rmse` = 1.66.

### What did we measure?
- Naive median 0.3594 over 5 runs; repeats: 0.3358, 0.3594, 0.3854, 0.3878, 0.3286
- Spread: range 0.3286 to 0.3878, noise band ±0.05198 (2 x MAD), CV 7.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -78.4% (noise band ±3.1% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +1.335 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `n_splits=30`, `n_splits=150`, `n_splits=300`
- Not settable with this harness: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochx=2` (21.94 noise units, gap +9.6%); `epochx=5` (8.09 noise units, gap -53.0%); `epochx=1` (2.98 noise units, gap +69.0%); `epochx=50` (2.17 noise units, gap -71.6%); `epochx=100` (1.19 noise units, gap -74.6%)
- Near alternatives (closest across all claims):
  - `epochx=10`, `hidden=4`: this claim -64.0%, mean |gap| 35.2% (2 runs)
  - `hidden=5`, `epochx=50`: this claim -65.6%, mean |gap| 38.4% (2 runs)
  - `epochx=100`, `hidden=4`: this claim -71.6%, mean |gap| 38.5% (2 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting epochx=10, hidden=1 | settings | 56% | 2.4 sigma (fits every claim) | run with epochx=10, hidden=1 |
| 2 | a cause outside every class tested | outside | 44% |  | look for code, data or evaluation differences the classes don't cover |
| 3 | no difference in reporting: the numbers as printed at the end of the run | settings | 0% | 14.7 sigma | the settings search and the other classes |

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 5 tested configuration(s) fit C_energy_rmse, and every other claim (C_yacht_rmse) fits some tested configuration, but none of the 42 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- Fit C_energy_rmse alone (5; worst claim's implausibility in brackets, lowest is the least inconsistent): epochx=10, hidden=1 (9.89); epochx=1, hidden=10 (14.98); epochx=1, hidden=5 (20.38); epochx=1, hidden=20 (21.76); epochx=2 (29.05)

Notes:
- {'epochx': '10', 'hidden': '1'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'epochx': '10', 'hidden': '1'} (gap +2.1%); it did not pass verification
- spec knobs no ledger assumption names (n_splits) were screened too; no better answer
- history matching: out-of-space suspected: 5 tested configuration(s) fit C_energy_rmse, and every other claim (C_yacht_rmse) fits some tested configuration, but none of the 42 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- {'epochx': '10', 'hidden': '1'} matches C_energy_rmse (I=0.37) but breaks C_yacht_rmse (I=9.89); no tested condition matches all claims, so the rest of the gap probably lies in code, data or evaluation, which GapFinder doesn't change
- value interval stopped early: run budget of 200 reached (wanted 1 more run(s) of {'epochx': '9', 'hidden': '1'} for 'interval epochx=9')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_energy_rmse | C_yacht_rmse | Mean |gap| |
|---|---|---|---|---|
| `epochx=10`, `hidden=4` | 2 | -64.0% | +6.4% | 35.2% |
| `hidden=5`, `epochx=50` | 2 | -65.6% | +11.1% | 38.4% |
| `epochx=100`, `hidden=4` | 2 | -71.6% | +5.4% | 38.5% |
| `epochx=50` | 6 | -71.7% | +11.7% | 41.7% |
| `epochx=10` | 6 | -64.9% | +19.9% | 42.4% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `epochx=5000`: other, The value 5000 exceeds the allowed range for epochx (likely a maximum like 1000 or 2000), causing the program to reject it as invalid. [not taken as invalid_value: the log shows no rejection]
- `hidden=20`: other, The program rejected hidden=20, likely because hidden must be a power of two or within a specific range; 16 is the closest valid value to 20 that is not the default 2. [not taken as invalid_value: the log shows no rejection]
- `hidden=10`: other, The program likely expects the hidden layer size to be a power of two (or within a specific set) and rejected the value 10. The nearest valid setting preserving the intent of a larger hidden layer is 8. [not taken as invalid_value: the log shows no rejection]
- `hidden=100`: other, Setting hidden to 100 caused a RecursionError in Theano's gradient computation, indicating the value is too large for the model's recursion depth; a smaller hidden size like 64 retains the intent of a larger hidden layer while avoiding the recursion limit. [not taken as invalid_value: the log shows no rejection]
- `hidden=200`: crash, Setting hidden=200 created a neural network with a large hidden layer, causing Theano's gradient computation to recurse deeply and exceed Python's recursion limit, resulting in a RecursionError and crash

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `n_splits=30`, `n_splits=150`, `n_splits=300`

## Knob names
- Screened though no assumption named them (low prior, code-derived values): `n_splits`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`

## Provenance
- GapFinder commit: `7e3568335cda944b166665fca73315f0b4a5e13a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `03cc5e006f242382f56af9ae32ddfb1e1ff0fcbbb9bf40c5b17ca7de3e0e2cb6`
- Cost: Nemotron billed $0.0044, sandbox reported $2610.4146 (total $2610.4190; this search; ledger extraction is included only if it shared the search's router)
