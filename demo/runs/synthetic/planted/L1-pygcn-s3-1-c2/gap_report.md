# Gap Report: planted L1-pygcn-s3-1

Artifact `pygcn` · generated 2026-10-22 02:29 · 120 branch runs (0 build/load setups) · sandbox $17.2283

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_cora (cora_acc) | Fits but unsupported | +79.8% | -2.6% | ±1.8% | `lr=0.0025` |

## C_cora: cora_acc (paper 46.1)
**Fits but unsupported** · gap +79.8% → -2.6% · 49 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0054`, `B0065`, `B0066`, `B0082` (4 run(s) of the same config)
- Config: `lr` naive `0.01`, changed to `0.0025`
- Command:

  Replay: fork checkpoint `69abd25a-45ee-4e12-8b94-2cfde545816c` and run
  ```
  RUN_TAG=4e5a2ecf4e00 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; mkdir -p out; S=$(( $(printf %s "$RUN_TAG" | cksum | cut -d" " -f1) % 100000 )); cd pygcn && PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python train.py --no-cuda --seed $S --epochs 200 --lr 0.0025 --weight_decay 5e-4 --hidden 16 --dropout 0.5 > ../out/run.log 2>&1; cd ..; bash gf_harness/emit.sh
  ```
- Output: `cora_acc` 42.1, 44.1, 47.6, 45.7; gap after -2.6%; result checkpoint `b2042f9b-b0b2-4775-a273-a20590483076`
- Effect: candidate 44.9 minus naive 82.9 = -38, 95% bootstrap interval [-38.92, -33.8] (4 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `cora_acc` = 46.1.

### What did we measure?
- Naive median 82.9 over 5 runs; repeats: 83.2, 80.9, 83.1, 82.9, 81.1
- Spread: range 80.9 to 83.2, noise band ±0.829 (2 x MAD), CV 1.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +79.8% (noise band ±1.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +79.8% (it comes back)
- NOT CHECKED · Held-out claim: no held-out claims were checked
- FAIL · Evidence: `lr=0.0025`: no evidence mentions '0.0025'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -38 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `epochs=10000`, `epochs=20000`
- Not settable with this harness: none
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `dropout=0.95` (43.06 noise units, gap -2.4%); `hidden=2` (42.1 noise units, gap +4.1%); `weight_decay=0.005` (41.86 noise units, gap -4.6%); `epochs=60` (40.41 noise units, gap +7.2%); `lr=0.002` (35.59 noise units, gap -15.8%) (and 25 more in the JSON)
- Near alternatives (closest across all claims):
  - `epochs=60`: this claim -3.5%, mean |gap| 3.5% (4 runs)
  - `dropout=0.95`: this claim +4.7%, mean |gap| 4.7% (4 runs)
  - `weight_decay=0.005`: this claim -6.2%, mean |gap| 6.2% (4 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=0.0025` (reported)
- `epochs=60`
- `hidden=2`
- `dropout=0.95`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting lr=0.0025 | settings | 59% | 0.5 sigma (fits every claim) | run with lr=0.0025 |
| 2 | the setting epochs=60 | settings | 20% | 0.1 sigma (fits every claim) | run with epochs=60 |
| 3 | the setting hidden=2 | settings | 8% | 1.1 sigma (fits every claim) | run with hidden=2 |

### History matching (every measured configuration, all claims together)
- 3 of 47 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `epochs`: epochs=60 (max I 0.31)
  - `lr`: lr=0.0025 (max I 0.9)
  - `weight_decay`: weight_decay=0.005 (max I 2.1)
- 3 separate islands (no single-knob move joins them): epochs=60 | lr=0.0025 | weight_decay=0.005
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:17`)
  - unexposed setting: `add_argument(..., default=False)`: a switch fixed in the call; no flag sets it (`pygcn/train.py:19`)

Notes:
- configurations the target claim can't tell apart from the answer: lr=0.0025; epochs=60; hidden=2; dropout=0.95
- patch round: {'@ast:pygcn/train.py:19:default': 'True', 'epochs': '60'} also fits every claim (Fits but unsupported), but doesn't beat {'lr': '0.0025'}
- mutation round: no mutant fits every claim (pygcn/utils.py:41: `140` -> `70`: worst 21.0 sigma; pygcn/train.py:67: `F.nll_loss(output[idx_train], labels[idx_train])` -> `(F.nll_loss(output[idx_train], labels[idx_train])) / 2`: worst 24.2 sigma; pygcn/train.py:47: `labels.max().item()` -> `(labels.max().item()) * 2`: worst 19.9 sigma)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_cora | Mean |gap| |
|---|---|---|---|
| `lr=0.0025` | 4 | -2.6% | 2.6% |
| `epochs=60` | 4 | -3.5% | 3.5% |
| `dropout=0.95` | 4 | +4.7% | 4.7% |
| `weight_decay=0.005` | 4 | -6.2% | 6.2% |
| `epochs=60`, `@ast:pygcn/train.py:19:default=True` | 3 | -8.2% | 8.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `dropout=2.5`: other, The dropout parameter expects a probability between 0 and 1; value 2.5 is outside this range, causing the program to reject it. [not taken as invalid_value: the log shows no rejection]
- `dropout=5`: other, The training script expects dropout to be a probability in the range [0,1]; supplying '5' is outside this range, causing the script to reject the value and produce no metrics. [not taken as invalid_value: the log shows no rejection]

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `epochs=10000`, `epochs=20000`

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `dropout`: fraction (dropout.p (torch.nn.functional.dropout) at pygcn/models.py:16)
- `epochs`: count (range() bound at pygcn/train.py:100)
- `lr`: rate (optimizer.lr (Adam) at pygcn/train.py:49)
- `weight_decay`: rate0 (optimizer.weight_decay (Adam) at pygcn/train.py:49)

## Provenance
- GapFinder commit: `ca4a5e297839f0c50559b58914404255594c81fb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `7aa31a94455723bae4aefe57ec3917cb5f1774f15f4cb0b1319641eee0b9c978`
- Cost: Nemotron billed $0.0010, sandbox reported $17.2283 (total $17.2294; this search; ledger extraction is included only if it shared the search's router)
