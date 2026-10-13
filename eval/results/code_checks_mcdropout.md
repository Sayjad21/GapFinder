# Static out-of-space code checks on MC Dropout (offline, $0, not blind)

`gapfinder/ingest/code_checks.py` lists leads for causes outside the exposed settings. It reads the code
and runs nothing. The engine attaches the leads when history matching says "out of space"
(suspected or likely), and the Gap Report lists them under "History matching".

**Input:** yaringal/DropoutUncertaintyExps at commit 6eb4497 (the code the MC Dropout case runs), with
the harness knobs from `eval/external/mc-dropout/mcd_sandbox.yaml` excluded. Those knobs are `dir`,
`epochx`, `hidden`, `n_epochs`, `n_hidden`, `n_splits`, `dropout_rates` and `tau_values_*`.

**Command:** a re-label of the 30 recorded post-hoc runs, with no new runs and no model calls. Export
`GF_MCD_SOURCE` (a local clone of the repo), plus `GF_MCD_SANDBOX_BASE=relabel-only` and
`GF_CACHE_ONLY=1`, then run:

```
gapfinder search --spec eval/external/mc-dropout/mcd_sandbox.yaml \
  --targets eval/external/mc-dropout/targets_mcd.json \
  --assumptions eval/external/mc-dropout/posthoc/assumptions.json \
  --claims eval/external/mc-dropout/ledgers/normal/claim_ledger.json \
  --backend local --max-runs 30 --candidates-per-knob 2 --cap 0.5 \
  --resume eval/external/mc-dropout/posthoc/run/events.jsonl --out <dir>
```

**Result:** the label is the same as [posthoc-v11-relabel](../external/mc-dropout/posthoc-v11-relabel/):
"Explains target, conflicts with held-out" (`epochx=10`, `hidden=1`), with history matching saying out of
space. The new part is the 8 leads, best first:

| # | Lead | Location | Documented difference? (answer_key.md, "Other documented differences") |
|---|---|---|---|
| 1 | grid search keeps the best `tau` and `dropout` per split (over `dropout_rates` x `tau_values`) | `experiment.py:163` | **yes**: the paper used Bayesian optimisation (40 iterations); the code uses grid search re-tuned per split. The authors' 2018 README also says the paper-era code tuned hyperparameters shared across splits |
| 2 | `batch_size = 128` fixed | `net/net.py:70` | **yes**: the paper uses mini-batches of 32 |
| 3 | `lengthscale = 0.01` fixed | `net/net.py:71` | not documented |
| 4 | random seed fixed to 1 | `experiment.py:87` | not documented |
| 5 | validation fraction 0.8 fixed | `experiment.py:132` | not documented |
| 6 | `predict(..., batch_size=500)` (evaluation) | `net/net.py:122` | no effect on results (inference batch) |
| 7 | `T = 10000` fixed | `net/net.py:126` | **yes**: Monte Carlo passes. The harness patches it to 100, a documented deviation |
| 8 | `predict(..., batch_size=500)` (evaluation) | `net/net.py:128` | no effect on results |

All three documented out-of-flag differences are listed, at ranks 1, 2 and 7, out of 8 leads in a
356-line repo.

**Limits:**
- These are leads, not findings: none was tested.
- To test one, the harness has to expose it, e.g. as a patch knob. The diff guard keeps source edits out
  of the search today.
- Not blind: the documented differences were known when this check was written, and it was checked on
  this repo.
- The GapBench artifacts get no leads, because every setting there is a flag. Their out-of-space bugs
  live in patched copies the checks never see (`eval/gapbench/variants.py`).
