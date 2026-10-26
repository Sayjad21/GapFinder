# Gap Report: planted L2-pygcn-s6-2

Artifact `pygcn` · generated 2026-10-23 21:21 · 5 branch runs (0 build/load setups) · sandbox $0.6952

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_cora (cora_acc) | Reproduced | +0.4% | n/a | ±1.0% | — |

## C_cora: cora_acc (paper 82.57)
**Reproduced**: naive gap +0.4% is inside the noise band ±1.0%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `cora_acc` = 82.57.

### What did we measure?
- Naive median 82.9 over 5 runs; repeats: 82.8, 83.8, 82.9, 83.2, 82.8
- Spread: range 82.8 to 83.8, noise band ±0.829 (2 x MAD), CV 0.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +0.4% (noise band ±1.0% of the paper value)

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

| Configuration | Runs | C_cora | Mean |gap| |
|---|---|---|---|
| naive (reproduction as run) | 5 | +0.4% | 0.4% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `dropout`: fraction (dropout.p (torch.nn.functional.dropout) at pygcn/models.py:16)
- `epochs`: count (range() bound at pygcn/train.py:100)
- `lr`: rate (optimizer.lr (Adam) at pygcn/train.py:49)
- `weight_decay`: rate0 (optimizer.weight_decay (Adam) at pygcn/train.py:49)

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `8142ea3e751e0b113ef55c227c8642b84177f98ff01eb9ec545b910efe081eb3`
- Cost: Nemotron billed $0.0000, sandbox reported $0.6952 (total $0.6952; this search; ledger extraction is included only if it shared the search's router)
