# Gap Report: mcd

Artifact `mcd` · generated 2026-10-12 19:55 · 26 branch runs (1 build/load setups) · sandbox $584.6619

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_energy_rmse (energy_rmse) | Unexplained | -76.5% | -76.5% | ±0.6% | — |

## C_energy_rmse: energy_rmse (paper 1.66)
**Unexplained** · gap -76.5% → -76.5% · 9 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (9 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `energy_rmse` = 1.66.

### What did we measure?
- Naive median 0.3903 over 5 runs; repeats: 0.3705, 0.4138, 0.3903, 0.3952, 0.3863
- Spread: range 0.3705 to 0.4138, noise band ±0.00985 (2 x MAD), CV 4.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -76.5% (noise band ±0.6% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: `n_splits=30`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `hidden=1` (9.79 noise units, gap -70.7%); `n_splits=2` (3.4 noise units, gap -74.5%); `hidden=4` (1.18 noise units, gap -75.8%)
- Near alternatives (closest across all claims):
  - `epochx=250`, `n_splits=2`: this claim -78.1%, mean |gap| 42.0% (3 runs)
  - `n_splits=2`: this claim -75.9%, mean |gap| 44.8% (3 runs)
  - `hidden=4`: this claim -75.8%, mean |gap| 48.2% (3 runs)

Notes:
- {'hidden': '1', 'epochx': '250'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'hidden': '1', 'epochx': '250'} (gap -68.5%); it did not pass verification

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_energy_rmse | C_yacht_rmse | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | -76.5% | -4.3% | 40.4% |
| `epochx=250`, `n_splits=2` | 3 | -78.1% | +6.0% | 42.0% |
| `n_splits=2` | 3 | -75.9% | -13.7% | 44.8% |
| `hidden=4` | 3 | -75.8% | -20.6% | 48.2% |
| `hidden=1`, `n_splits=2` | 3 | -73.6% | -36.8% | 55.2% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `n_splits=30`

## Provenance
- GapFinder commit: `7c103057f622b7175731d31bb1941906178b10a2` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `ba8391a105883d412eb8a18ac545f3f8adf5b9bdb0e5903e196fd26c52f845ef`
- Cost: Nemotron billed $0.0000, sandbox reported $584.6619 (total $584.6619; this search; ledger extraction is included only if it shared the search's router)
