# MC Dropout post-hoc run, re-labelled by v1.1 (history matching), NOT blind

The same 30 recorded branch runs as [../posthoc/](../posthoc/), with the documented values in the
hypothesis set, re-labelled from the recorded runs only: `--resume`, `--max-runs 30`, `--backend local`.
No new runs, no model calls, $0.

| | v1.0 label | v1.1 label |
|---|---|---|
| Energy RMSE (target 1.66) | Unexplained (the documented pair breaks held-out Yacht) | **Explains target, conflicts with held-out**: `epochx=10`, `hidden=1` (gap -76.7% → +3.8%) |
| History matching | none | **out-of-space suspected**: 1 tested configuration fits Energy and others fit Yacht, but none fits both |

This matches the documented truth: the paper's 10× epochs and one hidden layer, plus the authors'
2018 README admission that the paper-era code tuned hyperparameters shared across splits (test-set
contamination), a code-level cause that no setting can recreate.

**Not blind:** the documented values were added to the hypothesis set after the answer key was
revealed (see ../posthoc/README.md). The blind v1.0 arms never tested `epochx=10`. v1.1's multiplier
candidates would propose it from the code alone, but that hasn't been run blind yet.
