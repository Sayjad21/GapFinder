# Answer key (SEALED) - blind case b3c

Sealed: 2026-10-18 by the sealer (independent model). Do not open before the reveal.

## Case
- Paper: "SparseTSF: Modeling Long-term Time Series Forecasting with 1k Parameters", Shengsheng Lin, Weiwei Lin, Wentai Wu, Haojun Chen, Junjie Yang. ICML 2024.
- Version given to the runner: https://arxiv.org/abs/2405.00946v1 (2 May 2024). v1 does NOT mention the cause; v2 (3 Jun 2024) and later do (footnote 4 and Appendix D.1), so the runner must use v1.
- Repo: https://github.com/lss-1138/SparseTSF
- Commit given to the runner: f5cb1753a2420227378b13f6b77f213789e781d3 (2024-06-02, "Update README.md"), the last commit before the fix. Fix commit (do not show the runner): 8ae055490fb8878fd302e5b6bd43803beb5bb763 (2024-07-01, "Fix bug and updated readme"). Its README explains the cause.

## Claims
Table 2 (MSE, multivariate, look-back 720, mean of 5 runs), SparseTSF row, arXiv v1:
- MAIN target: ETTh2, horizon 336: 0.312 (+-0.004).
- Held-out (same row): ETTh2 96 / 192 / 720: 0.267 / 0.314 / 0.370; ETTh1 96 / 192 / 336 / 720: 0.359 / 0.397 / 0.404 / 0.417.
- Electricity and Traffic cells are out of scope (too heavy for the VM, and the effect there is small).

## Documented cause (evaluation protocol: the metric is computed on a truncated test set)
The test DataLoader drops the last incomplete batch. In `data_provider/data_factory.py`, `data_provider()`, branch `if flag == 'test':`, the code sets `drop_last = True`, with `batch_size = args.batch_size` (256 in scripts/SparseTSF/etth1.sh and etth2.sh). So the reported MSE/MAE leave out the final test windows: for ETTh2 at horizon 336 that is 241 of 2545 windows (9.5%); at 96, 225 of 2785. Because of this, the test metric depends on the batch size. The fix sets `drop_last = False` and changes exp/exp_main.py `test()` from `np.array(preds)` to `np.concatenate(preds, axis=0)`, so the ragged last batch works. In the hierarchy of cause types, this is a hard-coded true/false switch in code that changes how the reported number is computed (protocol). It is not a command-line flag.

Under the full test set (the authors' own corrected numbers, arXiv v2 Table 11), SparseTSF scores: ETTh1 0.362 / 0.403 / 0.434 / 0.426; ETTh2 0.294 / 0.339 / 0.359 / 0.383. Running the code at the given commit reproduces the paper's Table 2 numbers, because they were produced with the truncated test set. The correct finding is to name the truncation, not to "explain" a gap.

## Sources
- The authors, arXiv v2 (https://arxiv.org/abs/2405.00946v2), Appendix D.1, "Comparison Results after Fixing the Code Bug": "Recent research has discovered a long-standing bug in the popular codebase used in the field since the introduction of the Informer (Zhou et al., 2021). This bug, which affected the calculation of test set metrics, caused the data that did not fill an entire batch to be discarded (Qiu et al., 2024). As a result, the batch size setting influenced the results. ... This bug significantly improved the performance on ETTh1 and ETTh2 datasets when the batch size was large". Table 11 gives the corrected numbers above. Footnote 4 (main text): "Recent works discovered a long-standing bug in the current benchmark framework, which may affect model performance on small datasets (Xu et al., 2024; Qiu et al., 2024)."
- Fix commit https://github.com/lss-1138/SparseTSF/commit/8ae055490fb8878fd302e5b6bd43803beb5bb763: data_factory.py `drop_last = True` -> `drop_last = False  # fix bug` (test branch); exp_main.py `np.array(preds)` -> `np.concatenate(preds, axis=0)`. README: "There was a longstanding bug in our current framework where the last batch of data was discarded during the testing phase ... This might have affected the model's performance, especially when using a large batch size on small datasets."
- Independent: Qiu et al., "TFB: Towards Comprehensive and Fair Benchmarking of Time Series Forecasting Methods", PVLDB 2024 (arXiv 2403.20150), the "drop last" trick. Xu, Zeng, Xu, FITS (ICLR 2024), README of https://github.com/VEWOXIC/FITS.

## Sealer's private check (not for the runner)
Laptop CPU (Windows), torch 2.x CPU. To run on CPU, `map_location="cuda:0"` in exp_main.py was changed to "cpu" (it only affects checkpoint loading). Scripts' settings: seq_len 720, period_len 24, batch 256, lr 0.03 (ETTh2) / 0.02 (ETTh1), 30 epochs, patience 5; one run each, about 25 s per horizon.

| | 96 | 192 | 336 | 720 |
|---|---|---|---|---|
| ETTh1, commit f5cb175 | 0.354 | 0.398 | 0.405 | 0.418 |
| ETTh1, fix commit 8ae0554 | 0.362 | 0.404 | 0.435 | 0.426 |
| ETTh2, commit f5cb175 | 0.278 | 0.315 | 0.311 | 0.371 |
| ETTh2, fix commit 8ae0554 | 0.294 | 0.340 | 0.360 | 0.383 |

- ETTh1 paper values: 0.359 / 0.397 / 0.404 / 0.417. ETTh2 paper values: 0.267 / 0.314 / 0.312 / 0.370.
- Commit f5cb175 with `--batch_size 32` on ETTh2: 0.293 (96) and 0.359 (336). With batch 32 almost the whole test set is kept, so these sit close to the fixed numbers. Batch size is therefore the exposed knob that moves the test claims, but only through the dropped windows.

## Equivalence set (counted as correct), written before the runner starts
- E1: the report names the test DataLoader's `drop_last=True` (data_provider/data_factory.py, test branch) as dropping the last partial batch of test windows from the reported metric. It may come as an audit/selection-in-code finding, a code lead, or a measured protocol test (e.g. a full-test-set evaluation that gives about 0.36 at ETTh2-336).
- E2: the report finds that the test metrics depend on the batch size because test samples are discarded / not all test windows are evaluated. The incomplete-batch truncation must be named in words, even without the variable name.
- E3: verdict "Reproduced" or "Paper-artifact inconsistency" together with E1 or E2.

## Pre-registered scoring rule (adapted to a protocol cause)
- correct: the report names the protocol (E1-E3), by a measured protocol test or by an audit finding pointing at the right code;
- partial: the report flags that test-set metrics move with `batch_size` (e.g. batch_size found to move the claims, or marked suspicious) but does not say why, i.e. no mention of dropped/incomplete test batches;
- diagnosed out of space: a code lead at data_factory.py / the test loader, or at exp_main.py `test()`, labelled as a suspected out-of-space cause, without saying what it does. This scores as partial;
- confidently wrong: a confident label (Explained / Paper-artifact inconsistency / Partially explained) naming a setting that is not part of the cause: learning rate, seq_len, period_len, train_epochs, patience, seed, normalisation/RevIN, model size;
- otherwise: missed. "Reproduced" without naming the truncation is a correct abstention but scores as a miss of the cause, as in devbatch-2.
