# Gap Report: SparseTSF (batch-3)

Artifact `b3c` · generated 2026-10-26 03:37 · 8 branch runs (0 build/load setups) · sandbox $22.8610

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_h2_336 (etth2_336_mse) | Reproduced | -0.4% | n/a | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Found, but the test failed**: `data_provider/data_factory.py:19` `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size; with it switched off the program didn't finish (protocol test | no metrics parsed from output: ''). The code may assume it.
- **Held-out claims outside noise:**
  - C_h2_96 (`etth2_96_mse`): paper 0.267, measured 0.2778 (+4.0%, band ±1.0%)
  - C_h1_96 (`etth1_96_mse`): paper 0.359, measured 0.3539 (-1.4%, band ±1.0%)

## C_h2_336: etth2_336_mse (paper 0.312)
**Reproduced**: naive gap -0.4% is inside the noise band ±1.0%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `etth2_336_mse` = 0.312.

### What did we measure?
- Naive median 0.3107 over 5 runs; repeats: 0.3107, 0.3107, 0.3107, 0.3107, 0.3107
- Spread: range 0.3107 to 0.3107, noise band ±0.003107 (2 x MAD), CV 0.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -0.4% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `--decomposition`, `--enc_in`, `--pred_len`, `--kernel_size`, `--revin`, `--gpu`, `--data_path`, `--num_workers`, `--use_amp`, `--freq`, `--features`, `--target`, `--individual`, `CUDA_VISIBLE_DEVICES`, `--checkpoints`, `--do_predict`, `--model_id`, `--is_training`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

Notes:
- naive run is within the noise band of the paper's value

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_h2_336 | C_h2_96 | C_h2_192 | C_h2_720 | C_h1_96 | C_h1_192 | C_h1_336 | C_h1_720 | Mean |gap| |
|---|---|---|---|---|---|---|---|---|---|---|
| naive (reproduction as run) | 5 | -0.4% | +4.0% | +0.4% | +0.2% | -1.4% | +0.2% | +0.3% | +0.2% | 0.9% |

## Knob names
- Ledger names mapped to spec knobs: `--learning_rate` → `etth1_learning_rate, etth2_learning_rate`
- Screened though no assumption named them (low prior, code-derived values): `embed`

## Runtime trace (one dry run)
9 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `train_epochs`: size (width.out_features (Linear) at models/SparseTSF.py:21)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--decomposition`, `--enc_in`, `--pred_len`, `--kernel_size`, `--revin`, `--gpu`, `--data_path`, `--num_workers`, `--use_amp`, `--freq`, `--features`, `--target`, `--individual`, `CUDA_VISIBLE_DEVICES`, `--checkpoints`, `--do_predict`, `--model_id`, `--is_training`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `a047365bda559d40284883caa767a5f45e7e6e052f6eab233ed37f86fa4a7d08`
- Cost: Nemotron billed $0.0012, sandbox reported $22.8610 (total $22.8622; this search; ledger extraction is included only if it shared the search's router)
