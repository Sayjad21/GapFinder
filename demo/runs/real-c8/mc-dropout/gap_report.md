# Gap Report: MC Dropout (Gal & Ghahramani 2016)

Artifact `mcd` · generated 2026-10-27 02:48 · 199 branch runs (1 build/load setups) · sandbox $2429.0913

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_energy_rmse (energy_rmse) | Explains target, conflicts with held-out | -77.0% | +5.6% | ±4.8% | `epochx=10`, `hidden=1` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Comparisons the runs reverse** (the paper's ordering doesn't hold, beyond noise):
  - paper: energy_rmse 1.66 > yacht_rmse 1.11; measured: energy_rmse 0.3818 < yacht_rmse 0.8842 (margin -0.502, noise 0.109)
- **Held-out claims outside noise:**
  - C_yacht_rmse (`yacht_rmse`): paper 1.11, measured 0.8842 (-20.3%, band ±6.6%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `n_hidden.txt`: "1024 hidden units" (p.5)
  - `dropout_placement`: "dropout applied before every weight layer" (p.2)
  - `normalization`: "We centred and normalised both datasets" (p.4)
  - `dropout_variant`: "our results carry to other variants of dropout as well (such as drop-connect (Wan et al., 2013), multiplicative Gaussian noise (Srivastava et al., 2014), etc.)" (p.2)
  - `RL_exploration_method`: "Thompson sampling (Thompson, 1933) can be used to learn much faster" (p.1)

## C_energy_rmse: energy_rmse (paper 1.66)
**Explains target, conflicts with held-out** · gap -77.0% → +5.6% · 56 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0101`, `B0137`, `B0166`, `B0167`, `B0168` (5 run(s) of the same config)
- Config: `epochx` naive `500`, changed to `10`
- Config: `hidden` naive `2`, changed to `1`
- Command: not recorded
- Output: `energy_rmse` 1.753, 1.855, 1.724, 1.648, 1.896; gap after +5.6%
- Effect: candidate 1.753 minus naive 0.3818 = +1.372, 95% bootstrap interval [+1.281, +1.521] (5 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `energy_rmse` = 1.66.

### What did we measure?
- Naive median 0.3818 over 5 runs; repeats: 0.3242, 0.4219, 0.3818, 0.3367, 0.4127
- Spread: range 0.3242 to 0.4219, noise band ±0.08014 (2 x MAD), CV 11.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -77.0% (noise band ±4.8% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +1.372 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `n_splits=30`, `n_splits=150`, `n_splits=300`
- Not settable with this harness: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochx=2` (11.03 noise units, gap +23.7%); `epochx=3` (8.5 noise units, gap -35.9%); `epochx=5` (4.28 noise units, gap -56.3%); `epochx=1` (4.24 noise units, gap +56.5%)
- Near alternatives (closest across all claims):
  - `epochx=50`: this claim -72.0%, mean |gap| 38.9% (6 runs)
  - `epochx=250`: this claim -76.5%, mean |gap| 40.9% (6 runs)
  - `epochx=100`: this claim -73.8%, mean |gap| 43.1% (6 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 98% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | the setting epochx=10, hidden=1 | settings | 2% | 3.7 sigma | run with epochx=10, hidden=1 |
| 3 | no difference in reporting: the numbers as printed at the end of the run | settings | 0% | 13.4 sigma | the settings search and the other classes |

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 4 tested configuration(s) fit C_energy_rmse, and every other claim (C_yacht_rmse) fits some tested configuration, but none of the 43 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- Fit C_energy_rmse alone (4; worst claim's implausibility in brackets, lowest is the least inconsistent): epochx=10, hidden=1 (10.03); epochx=1, hidden=5 (10.95); epochx=1, hidden=10 (13.05); epochx=1, hidden=20 (16.77)

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'epochx': '3', 'hidden': '5'} for 'confirm-combo')
- {'epochx': '10', 'hidden': '1'} (gap +5.6%) was verified from existing runs and rejected: {'epochx': '10', 'hidden': '1'} closes this claim but makes held-out claims worse; rejected
- {'hidden': '5', 'epochx': '1'} (gap -6.6%) was verified from existing runs and rejected: {'hidden': '5', 'epochx': '1'} closes this claim but makes held-out claims worse; rejected
- {'hidden': '10', 'epochx': '1'} (gap +10.4%) was verified from existing runs and rejected: counterfactual for epochx not checked: {'hidden': '10'} has no successful run; {'hidden': '10', 'epochx': '1'} closes this claim but makes held-out claims worse; rejected
- closest configuration not verified: {'hidden': '5', 'epochx': '3'} (gap -48.7%, 2 of 5 confirmation runs); the budget ran out first, so no attribution is made
- spec knobs no ledger assumption names (n_splits) were screened too; no better answer
- history matching: out-of-space suspected: 4 tested configuration(s) fit C_energy_rmse, and every other claim (C_yacht_rmse) fits some tested configuration, but none of the 43 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- {'epochx': '10', 'hidden': '1'} matches C_energy_rmse (I=1.2) but breaks C_yacht_rmse (I=10.03); no tested condition matches all claims, so the rest of the gap probably lies in code, data or evaluation, which GapFinder doesn't change
- epochx: values from 10 to 10 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- hidden: values from 1 to 1 fit every claim (a bisection, 3 runs a side, one run a value: approximate)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_energy_rmse | C_yacht_rmse | Mean |gap| |
|---|---|---|---|---|
| `epochx=50` | 6 | -72.0% | +5.8% | 38.9% |
| `epochx=250` | 6 | -76.5% | -5.4% | 40.9% |
| `epochx=100` | 6 | -73.8% | +12.3% | 43.1% |
| `hidden=4`, `epochx=5` | 2 | -60.4% | +29.8% | 45.1% |
| `epochx=50`, `hidden=1` | 2 | -65.0% | -27.9% | 46.5% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `epochx=5000`: other, The value 5000 for epochx likely exceeds the program's allowed maximum, causing it to reject the setting. A value like 2000 keeps the intent of using a large number of epochs while staying within a typical valid range. [not taken as invalid_value: the log shows no rejection]
- `hidden=20`: other, The program rejected hidden=20, likely because it expects a smaller integer (e.g., a power of two) and the closest valid value preserving the intent of a larger hidden layer is 16. [not taken as invalid_value: the log shows no rejection]
- `hidden=10`: other, The program likely expects hidden layer size to be a power of two (common defaults like 2,4,8,16). The value 10 is not a power of two, causing rejection. The nearest valid power of two is 8. [not taken as invalid_value: the log shows no rejection]
- `hidden=100`: other, The hidden=100 setting triggered a RecursionError during gradient computation, indicating the value is too large for the model's recursion depth. A smaller hidden size like 64 preserves the intent of increasing network capacity while staying within valid limits. [not taken as invalid_value: the log shows no rejection]
- `hidden=200`: crash, The RecursionError indicates the program crashed due to excessive recursion depth when computing gradients, likely caused by setting hidden to an excessively large value (200) that made the computational graph too deep for Theano's gradient routine

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `n_splits=30`, `n_splits=150`, `n_splits=300`

## Knob names
- Screened though no assumption named them (low prior, code-derived values): `n_splits`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`

## Provenance
- GapFinder commit: `1b6bf29f1932c85ef4fb628d082c8fc243a37b95` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `03cc5e006f242382f56af9ae32ddfb1e1ff0fcbbb9bf40c5b17ca7de3e0e2cb6`
- Cost: Nemotron billed $0.0038, sandbox reported $2429.0913 (total $2429.0951; this search; ledger extraction is included only if it shared the search's router)
