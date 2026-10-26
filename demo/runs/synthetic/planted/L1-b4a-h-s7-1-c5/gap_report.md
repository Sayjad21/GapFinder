# Gap Report: planted L1-b4a-h-s7-1

Artifact `b4a` · generated 2026-10-24 09:24 · 5 branch runs (0 build/load setups) · sandbox $21.2161

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C18 (c18_auc) | Explained by the reporting rule | -4.4% | +0.9% | ±1.0% | reporting rule `bestval` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C19 (`c19_acc`): paper 0.626, measured 0.6146 (-1.8%, band ±1.0%)

## C18: c18_auc (paper 0.671)
**Explained by the reporting rule** · gap -4.4% → +0.9% · 0 hypotheses tested
> Reporting rule: the paper reports the epoch with the best validation score (early stopping or model selection). Every claim fits under it, from the runs already made

### Which experiment changed it?
- None was recorded.

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `c18_auc` = 0.671.

### What did we measure?
- Naive median 0.6417 over 5 runs; repeats: 0.6417, 0.6416, 0.6463, 0.6461, 0.6386
- Spread: range 0.6386 to 0.6463, noise band ±0.006417 (2 x MAD), CV 0.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -4.4% (noise band ±1.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the paper reports the epoch with the best validation score (early stopping or model selection) | reporting | 39% | 0.6 sigma (fits every claim) | add early stopping on the validation score (or read the test metric at the best validation epoch) |
| 2 | the paper reports each metric's best epoch, chosen with the test labels | reporting | 29% | 0.6 sigma (fits every claim) | print the test metric per epoch: is the paper's number the maximum over epochs rather than the last value? |
| 3 | the paper picks one epoch by the headline metric on the test labels and reports every metric there | reporting | 25% | 0.6 sigma (fits every claim) | read every metric at the epoch where the headline test metric peaks |

Notes:
- the paper reports the epoch with the best validation score (early stopping or model selection): every claim fits within 2 sigma under this reading of the naive runs (C18 0.6769 vs 0.671, C19 0.6283 vs 0.626), while the numbers as printed at the end miss the target by 2.8 sigma; no settings search was needed
- equally good readings: the paper reports each metric's best epoch, chosen with the test labels; the paper picks one epoch by the headline metric on the test labels and reports every metric there; the paper reports the best run (seed) of several, not their mean

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C18 | C19 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | -4.4% | -1.8% | 3.1% |

## Runtime trace (one dry run)
5 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `lr`: rate (optimizer.learning_rate (AdamOptimizer) at src/model.py:150)
- `n_epoch`: count (range() bound at src/train.py:18)
- `n_hop`: count (range() bound at src/data_loader.py:100)

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d08d4078e66aeb719503dd3f13ced2c2de45c61e071421a5dab1c177f4e36703`
- Cost: Nemotron billed $0.0000, sandbox reported $21.2161 (total $21.2161; this search; ledger extraction is included only if it shared the search's router)
