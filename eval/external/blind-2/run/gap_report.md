# Gap Report: GraphMAE (KDD 2022)

Artifact `graphmae` · generated 2026-10-17 09:04 · 59 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_collab (collab_acc) | Explained | -2.2% | -0.1% | ±1.0% | `mask_rate=0.5` |

## C_collab: collab_acc (paper 80.32)
**Explained** · gap -2.2% → -0.1% · 40 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0046`, `B0047` (3 run(s) of the same config)
- Config: `mask_rate` naive `0.75`, changed to `0.5`
- Command:

  Replay: fork checkpoint `10ae53ef-a9d2-46a0-9460-73bd3bb5c7f9` and run
  ```
  RUN_TAG=dc0a6afb56c5 set -o pipefail; F="$(cat gf_harness/run_graph_flags)"; S=$(( $(printf %s "$RUN_TAG" | cksum | cut -d" " -f1) % 100000 )); mkdir -p out; python gf_harness/apply_knobs.py --datasets COLLAB,IMDB-BINARY,IMDB-MULTI,MUTAG -- activation=relu alpha_l=2 attn_drop=0.1 batch_size=32 concat_hidden=false decoder=gin deg4feat=false drop_edge_rate=0.0 encoder=gin in_drop=0.2 linear_prob=true loss_fn=sce lr=0.00015 lr_f=0.001 mask_rate=0.5 max_epoch=20 max_epoch_f=0 negative_slope=0.2 norm=batchnorm num_heads=2 num_hidden=256 num_layers=2 num_out_heads=1 optimizer=adam pooling=mean replace_rate=0.0 residual=false scheduler=true warmup_steps=-1 weight_decay=0.0 weight_decay_f=0.0 || exit 3; for ds in COLLAB IMDB-BINARY IMDB-MULTI MUTAG; do t=1; [ $ds = COLLAB ] && t=6; ( s=$(date +%s); OMP_NUM_THREADS=$t MKL_NUM_THREADS=$t python main_graph.py --device -1 --dataset $ds $F --seeds $S > out/$ds.log 2>&1; echo gf_wall_s=$(( $(date +%s) - s )) >> out/$ds.log ) & done; wait; bash gf_harness/emit.sh
  ```
- Output: `collab_acc` 80.52, 80.22, 79.58; gap after -0.1%; result checkpoint `704edabd-9193-40da-b6dc-42153e3679ee`
- Effect: candidate 80.22 minus naive 78.56 = +1.66, 95% bootstrap interval [+0.868, +1.66] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `collab_acc` = 80.32.

### What did we measure?
- Naive median 78.56 over 5 runs; repeats: 78.84, 78.48, 78.56, 78.72, 78.56
- Spread: range 78.48 to 78.84, noise band ±0.7856 (2 x MAD), CV 0.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -2.2% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `mask_rate` the gap is -2.2% (it comes back)
- NOTE · Held-out claim, tuned separately: C_imdb_b: -0.6% to -0.4% (not worse beyond noise)
- NOTE · Held-out claim, tuned separately: C_imdb_m: +0.6% to +1.5% (not worse beyond noise)
- NOTE · Held-out claim, tuned separately: C_mutag: -4.7% to -2.3% (not worse beyond noise)
- PASS · Evidence: `mask_rate=0.5`: code evidence at graphmae/utils.py:73: 'parser.add_argument("--mask_rate", type=float, default=0.5)'
- PASS · Effect vs noise: candidate minus naive is +1.66 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: `max_epoch=200`, `max_epoch=300`, `max_epoch=100`, `max_epoch=500`, `max_epoch=1000`, `max_epoch=2000`
- Not settable with this harness: `--use_cfg`, `--seed / --runseed`, `--split (scaffold/random)`, `--device`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `mask_rate=0.3` (1.93 noise units, gap +0.3%); `encoder=gat` (1.63 noise units, gap +0.6%); `in_drop=0.3` (1.04 noise units, gap -1.2%)
- Near alternatives (closest across all claims):
  - `deg4feat=True`: this claim -2.4%, mean |gap| 1.4% (3 runs)
  - `encoder=gat`: this claim +0.6%, mean |gap| 2.3% (3 runs)
  - `decoder=gat`: this claim -8.4%, mean |gap| 3.1% (3 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `mask_rate`: mask_rate=0.5 (max I 0.05); mask_rate=0.3 (max I 0.06)
  - `encoder`: encoder=gat (max I 0.15)
  - `in_drop`: in_drop=0.3 (max I 0.23); in_drop=0.1 (max I 0.35)
  - `batch_size`: batch_size=64 (max I 0.27)
  - `pooling`: pooling=max (max I 0.28)
  - `negative_slope`: negative_slope=0.01 (max I 0.28); negative_slope=0.1 (max I 0.31)
  - `activation`: activation=prelu (max I 0.3)

Notes:
- stopped early: run budget of 60 reached (wanted 2 more run(s) of {'mask_rate': '0.3'} for 'confirm (race)')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_collab | C_imdb_b | C_imdb_m | C_mutag | Mean |gap| |
|---|---|---|---|---|---|---|
| `mask_rate=0.5` | 3 | -0.1% | -0.4% | +1.5% | -2.3% | 1.1% |
| `deg4feat=True` | 3 | -2.4% | -0.8% | +1.5% | +0.7% | 1.4% |
| naive (reproduction as run) | 5 | -2.2% | -0.6% | +0.6% | -4.7% | 2.0% |
| `encoder=gat` | 3 | +0.6% | -1.9% | -2.5% | -4.1% | 2.3% |
| `decoder=gat` | 3 | -8.4% | -1.2% | +1.6% | -1.1% | 3.1% |

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `max_epoch=200`, `max_epoch=300`, `max_epoch=100`, `max_epoch=500`, `max_epoch=1000`, `max_epoch=2000`

## Knob names
- Screened though no assumption named them (low prior, code-derived values): `concat_hidden`, `linear_prob`, `lr_f`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `--use_cfg`, `--seed / --runseed`, `--split (scaffold/random)`, `--device`

## Provenance
- GapFinder commit: `19d9adf7abaecf5b98363ce2986008b6ae66411f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d9f86df4f9334a380340018fb3a868fdaf7b992428e2b40422a354737aa93e54`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
