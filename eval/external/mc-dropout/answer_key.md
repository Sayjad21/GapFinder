# Answer key: MC Dropout (Gal & Ghahramani, ICML 2016), semi-blind external case

Sealed before any GapFinder run on this case. Only the sha256 of this file is committed
(`eval/external/mc-dropout/answer_key.sha256`). Written 2026-10-10.

## 1. What "the paper's" numbers are (a choice, recorded here)

"The paper's numbers" are the **published ICML 2016 proceedings Table 1** (PMLR v48, p.7,
http://proceedings.mlr.press/v48/gal16.pdf), dropout column, quoted from the PDF. They are NOT
the README "paper" column of the code repository (Yacht 0.70, Energy 1.08), which is a later re-run,
and NOT the arXiv version (1506.02142v6), which adds a Table 2 stating the effect.

| Dataset | Metric | Claimed value | Listed spread | Page |
|---|---|---|---|---|
| Concrete Strength | avg. test RMSE (dropout, MC) | 5.23 | +- 0.53 | p.7, Table 1 |
| Energy Efficiency | avg. test RMSE (dropout, MC) | 1.66 | +- 0.19 | p.7, Table 1 |
| Yacht Hydrodynamics | avg. test RMSE (dropout, MC) | 1.11 | +- 0.38 | p.7, Table 1 |
| Concrete / Energy / Yacht | avg. test log-likelihood (dropout) | -3.04 / -1.99 / -1.55 | +- 0.09 / 0.09 / 0.12 | p.7, Table 1 |

The header says "Std. Errors"; the arXiv version corrects these to standard deviations over the
20 splits. The RMSE of the dropout column is the MC-dropout predictive mean (p.7: "Dropout's RMSE
in table 1 is given by averaging stochastic forward passes through the network following eq. (6)
(MC dropout)"). In the harness the metric `rmse` is the MC RMSE (the second number experiment.py
logs); `rmse_single` is the first.

## 2. The documented cause

The published numbers were produced with a different training budget and depth than the code's
current defaults:

| Setting | Paper / paper-era code | Current code default |
|---|---|---|
| `--epochx` (epoch multiplier) | **10**: paper-era code `n_epochs*10` with `n_epochs.txt` = 40, i.e. 400 epochs; ICML p.6: "after finding the optimal parameter values we used 10x more iterations" | **500** (20,000 epochs) |
| `--hidden` (hidden layers) | **1**: paper-era code `[ n_hidden ]`; ICML p.6 "50 units" in the Hernandez-Lobato & Adams setup, one hidden layer | **2** |

Exact predicted setting: `--epochx 10 --hidden 1`, other data files unchanged (`n_epochs.txt` = 40,
`n_hidden.txt` = 50).

Sources (every URL):
- ICML paper (use this version): http://proceedings.mlr.press/v48/gal16.pdf (p.6: "50 units",
  dropout 0.05 and 0.005, BO with 40 iterations then "10x more iterations"; p.7: Table 1, the
  MC-dropout RMSE note; mini-batches of size 32, Adam).
- Code, current master (6eb4497628d12b0f300f4b4f6bdc386bebad565c):
  https://github.com/yaringal/DropoutUncertaintyExps (`experiment.py` defaults `--epochx 500`,
  `--hidden 2`; the README says results change with 10x epochs and with 2 layers instead of 1).
- Code, paper-era commit a6259f1 of the same repository (`yacht/net/experiment.py`:
  `n_epochs*10`, `[ n_hidden ]`).
- Later authors on the baseline being under-trained: Mukhoti, Stenetorp, Gal (2018),
  https://arxiv.org/abs/1811.09385 (the dropout baseline was stopped early).
- arXiv version, NOT used as "the paper" because it states the effect:
  https://arxiv.org/abs/1506.02142 (v6, Table 2 and the October 2016 update).

Other documented differences GapFinder cannot test (not in the flags):
- The paper used Bayesian optimisation (40 iterations) for dropout rate and tau; the code uses
  grid search over dropout {0.005, 0.01, 0.05, 0.1} x tau {0.25, 0.5, 0.75} (Concrete: tau
  {0.025, 0.05, 0.075}), re-tuned per split.
- Mini-batch size: paper 32, code `batch_size = 128` (hard-coded in `net/net.py`).
- Monte Carlo passes: the code has T = 10000; this reproduction fixes T = 100 (harness patch, not
  a knob).

## 3. Scoring rule

Target and held-out claims are chosen in Step 4 from these three datasets; any of the three
counts. A name match without the effect is not a success: after the search, the predicted setting
is re-run (3 repeats on disjoint split sets, since identical splits are bit-identical) and must
move the metric toward the paper beyond the noise band.

- **Full credit.** The report names **both** `epochx` (lower, towards 10; any value that closes
  the gap in the same direction counts, 10 is the documented value) and `hidden` = 1 as the
  confirmed cause of at least one target claim, with a confirmed label ("Explained" or
  "Paper-artifact inconsistency"), where the closing run's effect exceeds the noise band. The
  card must not claim the residual is fully explained when the remaining gap exceeds noise (the
  grid-search/BO change is untestable, so a complete closure is not required). It must be found
  from experiments; a label resting only on README or paper text (evidence only) is capped at
  partial.
- **Partial credit.** Any one of: names exactly one of `epochx` / `hidden`, correctly confirmed;
  names both but only as "Partially explained" or "Fits but unsupported"; names `epochx` or
  `hidden` in the right direction with a closing run but a different value; flags the grid-search
  vs BO difference as a likely, untestable contributor while also finding one of the two knobs.
  Partial credit exists because grid search vs BO is untestable (so a closure may stay partial)
  and because the effect size of each knob may differ.
- **Failure.** Names no relevant knob; names only an irrelevant knob (`n_splits`, `n_hidden`
  alone, `dropout_rates` or `tau_values` alone) as the cause; labels a claim "Reproduced" when the
  defaults are outside the noise band of the paper value; or confirms a cause whose re-run shows
  no effect beyond noise (a name match without the effect).

## 4. Caveats (all of them)

1. **Semi-blind.** The TODO states the documented cause in the repository. Sealing, the frozen
   system and a spec generated from the repo map keep it honest, but the truly blind case is a
   separate, later one.
2. **The defaults are better than the paper, not worse.** In the gap check (defaults, T = 100,
   3 repeats x 3 disjoint splits) the MC RMSE was: Yacht 0.914 vs 1.11 (-18%, 1.9 split standard
   errors), Energy 0.394 vs 1.66 (-76%, far outside noise), Concrete 4.42 vs 5.23 (-15%, 2.9 split
   standard errors; the 3 repeat means span 3.90 to 4.93). Only Energy is a gap clearly beyond
   noise; Yacht and Concrete are weaker. The documented direction (more training and a deeper net
   give a lower RMSE, so the paper's smaller budget gives a higher one) matches. These runs used
   the defaults only; the documented setting was not run before sealing.
3. **Grid search vs Bayesian optimisation, and batch size 32 vs 128**, are changes GapFinder
   cannot test; a perfect run is only partly explanatory.
4. **Scaled reproduction.** T = 100 Monte Carlo passes (patch `sed -i 's/T = 10000/T = 100/'
   net/net.py`, fixed, documented, not a knob) and 3 splits instead of 20. The RMSE of the mean
   prediction is barely affected; the log-likelihood is more affected.
5. **Identical settings and splits are deterministic.** experiment.py seeds numpy; repeats of the
   same settings and splits are bit-identical, so run-to-run noise must be measured over disjoint
   split sets, and it is large relative to some effects (per-split RMSE sd 0.3 on Yacht, 0.8 on
   Concrete).
6. **README "paper" column** (Yacht 0.70, Energy 1.08) is a later re-run, not Table 1; it is not
   used. Mukhoti et al. report the same direction (baseline under-trained).
7. **Which RMSE**: the MC-dropout RMSE (`rmse`), not the single-pass one.
8. The ICML "+-" values are standard deviations although labelled standard errors (the arXiv
   version corrects the label).
