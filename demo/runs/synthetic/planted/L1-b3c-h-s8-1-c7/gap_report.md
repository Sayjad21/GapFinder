# Gap Report: planted L1-b3c-h-s8-1

Artifact `b3c` · generated 2026-10-26 13:35 · 8 branch runs (0 build/load setups) · sandbox $16.3466

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C16 (c16_mse) | Reproduced | -0.1% | n/a | ±1.0% | — |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- Tested: switching this code off moved no claim beyond noise: `data_provider/data_factory.py:19` `drop_last = True` is fixed in the evaluation branch: it drops the last incomplete batch, so part of the evaluation data is never scored and the metric depends on the batch size; switched off (3 runs):

## C16: c16_mse (paper 0.309)
**Reproduced**: naive gap -0.1% is inside the noise band ±1.0%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `c16_mse` = 0.309.

### What did we measure?
- Naive median 0.3087 over 5 runs; repeats: 0.3087, 0.3087, 0.3087, 0.3087, 0.3087
- Spread: range 0.3087 to 0.3087, noise band ±0.003087 (2 x MAD), CV 0.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -0.1% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

Notes:
- naive run is within the noise band of the paper's value

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C16 | Mean |gap| |
|---|---|---|---|
| naive (reproduction as run) | 5 | -0.1% | 0.1% |

## Knob names
- Code defaults read from the code instead of the ledger: `seq_len` 96 at run_longExp.py:27 (ledger said 720), `pred_len` 96 at run_longExp.py:29 (ledger said 336), `train_epochs` 100 at run_longExp.py:72 (ledger said 30), `patience` 100 at run_longExp.py:74 (ledger said 5), `itr` 2 at run_longExp.py:71 (ledger said 1), `batch_size` 128 at run_longExp.py:73 (ledger said 256), `learning_rate` 0.0001 at run_longExp.py:75 (ledger said 0.02), `distil` True at run_longExp.py:59 (ledger said 1), `output_attention` False at run_longExp.py:66 (ledger said 0), `use_amp` False at run_longExp.py:80 (ledger said 0), `test_flop` False at run_longExp.py:87 (ledger said 0)

## Runtime trace (one dry run)
5 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Provenance
- GapFinder commit: `74c9414da0388b40a5f1bbeaaf040a4ed05a6bdb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `40b251ab834315bade8c231d09c3da53aaae8cd8393896b76d2ad72f72071358`
- Cost: Nemotron billed $0.0000, sandbox reported $16.3466 (total $16.3466; this search; ledger extraction is included only if it shared the search's router)
