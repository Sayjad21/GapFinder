# Gap Report: BOND / DOMINANT (batch-5)

Artifact `harness-c7` · generated 2026-10-27 09:41 · 59 branch runs (0 build/load setups) · sandbox $1938.3419

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_auc (c_auc) | Fits but unsupported | -8.0% | -3.4% | ±1.2% | `@ast:pygod/detector/dominant.py:98:weight=0.75` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C_ap (`c_ap`): paper 20, measured 17.61 (-12.0%, band ±3.1%)
  - C_rec (`c_rec_recall`): paper 23.8, measured 26.41 (+11.0%, band ±3.4%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `B.1 Hardware configuration`: "Hardware configuration. All the experiments were performed on a Linux server with a 3.50GHz Intel Core i5 CPU, 64GB RAM, and 1 NVIDIA GTX 1080 Ti GPU with 12GB memory." (p.19)
  - `gpu`: "OOM denotes out of memory with regard to GPU (_G) and CPU (_C)" (p.6)

## C_auc: c_auc (paper 82.7)
**Fits but unsupported** · gap -8.0% → -3.4% · 15 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0048`, `B0052`, `B0053` (3 run(s) of the same config)
- Config: `@ast:pygod/detector/dominant.py:98:weight` naive `0.5`, changed to `0.75`
- Command:

  Replay: fork checkpoint `aaa2e17a-0318-463c-ba00-52858edbf951` and run
  ```
  @ast:benchmark/utils.py:11:weight_decay=0.01 @ast:benchmark/utils.py:15:batch_size=64 @ast:benchmark/utils.py:17:epoch=2 @ast:benchmark/utils.py:19:batch_size=0 @ast:benchmark/utils.py:21:epoch=300 @ast:pygod/detector/adone.py:113:hid_dim=64 @ast:pygod/detector/adone.py:113:num_layers=4 @ast:pygod/detector/adone.py:113:dropout=0.0 @ast:pygod/detector/adone.py:113:weight_decay=0.0 @ast:pygod/detector/adone.py:113:lr=0.004 @ast:pygod/detector/adone.py:113:epoch=100 @ast:pygod/detector/adone.py:113:batch_size=0 @ast:pygod/detector/dominant.py:98:weight=0.75 @ast:benchmark/main.py:14:@mut.16.Call.xdiv2=0 @ast:benchmark/main.py:14:@mut.16.Call.xmul2=0 @ast:pygod/detector/base.py:435:@mut.17.Call.kwset.drop_last.VHJ1ZQ=0 @ast:pygod/detector/base.py:435:@mut.17.Call.kwset.shuffle.VHJ1ZQ=0 RUN_TAG=fe5554cabb00 export PYTHONPATH="${WORK:-$PWD}/.gf_patch${PYTHONPATH:+${GF_PATHSEP:-:}$PYTHONPATH}"; e="0"; if [ "$e" = 1 ]; then cp -rf "${GF_ERA_DIR:-/opt/gf_paper_era}/." ./; elif [ "$e" != 0 ]; then d="${GF_ERA_REL:-/tmp/gf_era}/$e"; [ -d "$d" ] || "${PYTHON:-python}" gf_harness/era_fetch.py "$e" "$d" >/dev/null 2>&1 || echo "GF_ERA_FETCH_FAIL $e" >&2; cp -rf "$d/." ./; fi; v="0"; if [ "$v" != 0 ]; then gf_pip() { if [ -n "$GF_PIP" ]; then $GF_PIP "$@"; else "${PYTHON:-python}" -m pip "$@"; fi; }; [ "$v" = 1 ] && v=all; r="${GF_PY_ROOT:-/opt/gf_py}"; [ "$v" = all ] && v="$(ls "$r" 2>/dev/null | tr "\n" ",")"; GF_LIB_DIRS=""; for p in $(echo "$v" | tr "," " "); do case "$p" in *==*) d="${GF_PY_REL:-/tmp/gf_py}/$p"; case "$p" in torch==*|torchvision==*|torchaudio==*) ix="--index-url https://download.pytorch.org/whl/cpu";; *) ix="";; esac; [ -d "$d" ] || PIP_NO_CACHE_DIR=1 gf_pip install -q --no-deps $ix --target "$d" "$p" >/dev/null 2>&1 || echo "GF_LIB_INSTALL_FAIL $p" >&2;; *) d="$r/$p";; esac; GF_LIB_DIRS="${GF_LIB_DIRS:+$GF_LIB_DIRS|}$d"; done; export GF_LIB_DIRS; fi; mkdir -p out; rm -f out/run*.log; GF_SEED=$("${PYTHON:-python}" -c "import os, zlib; print(zlib.crc32(os.environ.get('RUN_TAG', 'x').encode('utf-8')) % 100000)"); r=1; (timeout ${GF_TIME_CUT:-0} "${GF_BASH:-bash}" -c 'cd benchmark && PYTHONPATH="$OLDPWD${PYTHONPATH:+${GF_PATHSEP:-:}$PYTHONPATH}" "${PYTHON:-python}" main.py --model dominant --dataset inj_cora --gpu -1') > out/run1.log 2>&1; "${PYTHON:-python}" gf_harness/emit.py
  ```
- Output: `c_auc` 80.37, 78.34, 79.87; gap after -3.4%; result checkpoint `83ff08c0-1cb9-4942-8e4f-f5a6e965fdec`
- Effect: candidate 79.87 minus naive 76.05 = +3.82, 95% bootstrap interval [+2.602, +5.255] (3 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `c_auc` = 82.7.

### What did we measure?
- Naive median 76.05 over 5 runs; repeats: 75.54, 76.69, 73.55, 76.05, 76.27
- Spread: range 73.55 to 76.69, noise band ±1.02 (2 x MAD), CV 1.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -8.0% (noise band ±1.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `@ast:pygod/detector/dominant.py:98:weight` the gap is -8.0% (it comes back)
- PASS · Held-out claim: C_ap: -12.0% to -7.9% (not worse beyond noise)
- PASS · Held-out claim: C_rec: +11.0% to -4.2% (not worse beyond noise)
- FAIL · Evidence: `@ast:pygod/detector/dominant.py:98:weight=0.75`: no assumption record for this knob, so no evidence
- PASS · Effect vs noise: candidate minus naive is +3.82 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `B.1 Hardware configuration`, `init_model_hyperparams`, `num_trial`, `gpu`, `seed`, `oom_handling`, `time_limit`, `eval_roc_auc`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a code change: @ast:pygod/detector/dominant.py:98:weight=0.75 | code | 76% | 1.9 sigma (fits every claim) | run with @ast:pygod/detector/dominant.py:98:weight=0.75 (an in-memory code patch) |
| 2 | a code change: @ast:pygod/detector/dominant.py:98:weight=0.95 | code | 17% | 1.8 sigma (fits every claim) | run with @ast:pygod/detector/dominant.py:98:weight=0.95 (an in-memory code patch) |
| 3 | a cause outside every class tested | outside | 7% |  | look for code, data or evaluation differences the classes don't cover |

### Library drift and the paper-era code
- Packages as of the paper's date change the numbers; the culprit: `pygod==0.3.0`, `pyod==1.0.2`, `scikit-learn==1.1.1`, `torch-geometric==2.0.4`, `tqdm==4.64.0`

### History matching (every measured configuration, all claims together)
- 2 of 28 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 2 configurations
  - `@ast:pygod/detector/dominant.py:98:weight`: @ast:pygod/detector/dominant.py:98:weight=0.95 (max I 1.79); @ast:pygod/detector/dominant.py:98:weight=0.75 (max I 1.93)
- Leads outside the settings (static code checks, nothing run; check these first):
  - unexposed setting: `weight_decay = 0.01` is fixed in the code; no flag sets it (`benchmark/utils.py:11`)
  - unexposed setting: `epoch = 300` is fixed in the code; no flag sets it (`benchmark/utils.py:21`)
  - unexposed setting: `__init__(..., weight=0.5)`: a default no call in the repo overrides (31 call(s)) (`pygod/detector/dominant.py:98`)
  - unexposed setting: `logger(..., train=True)`: a switch fixed in the call; no flag sets it (`pygod/detector/base.py:485`)
  - unexposed setting: `batch_size = 64` is fixed in the code; no flag sets it (`benchmark/utils.py:15`)
  - unexposed setting: `epoch = 2` is fixed in the code; no flag sets it (`benchmark/utils.py:17`)
  - unexposed setting: `__init__(..., w1=0.2)`: a default no call in the repo overrides (31 call(s)) (`pygod/detector/adone.py:113`)
  - unexposed setting: `__init__(..., w2=0.2)`: a default no call in the repo overrides (31 call(s)) (`pygod/detector/adone.py:113`)

Notes:
- no hypothesis moved the gap by more than 1 noise units
- spec knobs no ledger assumption names (@ast:benchmark/utils.py:11:weight_decay, @ast:benchmark/utils.py:15:batch_size, @ast:benchmark/utils.py:17:epoch, @ast:benchmark/utils.py:21:epoch, @ast:pygod/detector/adone.py:113:hid_dim, @ast:pygod/detector/adone.py:113:num_layers, @ast:pygod/detector/adone.py:113:lr, @ast:pygod/detector/adone.py:113:epoch, gf_paper_year_env, gf_paper_era_code) were screened too; no better answer
- history matching: 1 of 21 tested configurations fit every claim within 3 sigma
- explained with a code patch (tested in memory, no file edited): pygod/detector/dominant.py line 98: weight = 0.5 -> 0.75
- @ast:pygod/detector/dominant.py:98:weight: values from 0.75 to 0.7957 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- library: pygod 0.3.0 and pyod 1.0.2 and scikit-learn 1.1.1 and torch-geometric 2.0.4 and tqdm 4.64.0 together gives the numbers of every package as of the paper's date
- library probe stopped early: its share of the run budget (15 runs) is used

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_auc | C_ap | C_rec | Mean |gap| |
|---|---|---|---|---|---|
| `@ast:pygod/detector/dominant.py:98:weight=0.75` | 3 | -3.4% | -7.9% | -4.2% | 5.2% |
| naive (reproduction as run) | 5 | -8.0% | -12.0% | +11.0% | 10.3% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `@ast:benchmark/utils.py:21:epoch=3000`: other, The value '3000' for epoch exceeds the allowed maximum, causing the program to reject it as an invalid value. [not taken as invalid_value: the log shows no rejection]

## Knob names
- Screened though no assumption named them (low prior, code-derived values): `@ast:benchmark/utils.py:11:weight_decay`, `@ast:benchmark/utils.py:15:batch_size`, `@ast:benchmark/utils.py:17:epoch`, `@ast:benchmark/utils.py:21:epoch`, `@ast:pygod/detector/adone.py:113:hid_dim`, `@ast:pygod/detector/adone.py:113:num_layers`, `@ast:pygod/detector/adone.py:113:lr`, `@ast:pygod/detector/adone.py:113:epoch`, `gf_paper_year_env`, `gf_paper_era_code`

## Runtime trace (one dry run)
3 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.
- `@ast:benchmark/utils.py:11:weight_decay`: rate0 (optimizer.weight_decay (Adam) at pygod/detector/base.py:443)
- `@ast:benchmark/utils.py:21:epoch`: count (range() bound at pygod/detector/base.py:456)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `B.1 Hardware configuration`, `init_model_hyperparams`, `num_trial`, `gpu`, `seed`, `oom_handling`, `time_limit`, `eval_roc_auc`

## Provenance
- GapFinder commit: `7e3568335cda944b166665fca73315f0b4a5e13a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `1d2ae10f49c75d62fa912e11d0e65a636fec58cfeb91d376ffbe858a289a85ba`
- Cost: Nemotron billed $0.0014, sandbox reported $1938.3419 (total $1938.3432; this search; ledger extraction is included only if it shared the search's router)
