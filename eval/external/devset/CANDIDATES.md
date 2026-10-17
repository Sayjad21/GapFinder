# GapFinder development set: candidate cases with documented reproduction gaps

Compiled 2026-10-17. This is a DEVELOPMENT set: causes are recorded in full.

## How to read this file

- "Verified" in this file means: I read the cited repo source files, issue threads, PDFs and papers directly (via raw GitHub files, the GitHub API and arXiv/Zenodo PDFs). **I did not run any of the 13 cases.** Every "Sandboxes fit" line is therefore an ESTIMATE from dataset and model sizes and from the repo's default loops, not a measurement. Estimates are marked with their basis.
- Commit hashes are the state at 2026-10-17 unless noted. For cases where the repo later fixed the problem, the gap commit is given explicitly.
- Sandboxes constraint applied: 4 vCPU, 3.9 GB RAM, no swap, no GPU, under 3600 s per run, data fetched at image build. Anything I judged likely above about 3 GB peak RSS or 1 h per run is excluded or restricted to a smaller dataset of the same experiment (stated per case). The GraphMAE COLLAB failure (dense graphs with large features, 5000 graphs) was used as the memory warning: COLLAB, REDDIT-B and PubMed-with-dense-adjacency are avoided where a smaller dataset gives the same experiment.
- Mix: 6 setting-driven cases, 5 code-driven, 3 noise or not-reproducible (some cases are tagged with two types because the maintainers cite more than one cause).

---

## Case 1. VGAE/GAE link prediction: changed negative-edge split (tkipf/gae)

- **Paper:** Kipf and Welling, "Variational Graph Auto-Encoders", NIPS Bayesian Deep Learning Workshop 2016. https://arxiv.org/abs/1611.07308
- **Repo:** https://github.com/tkipf/gae
- **Commit with the gap:** `e117287a8475c07c7df9fe483a469afc797b4b9c` (merge of PR #25 "Re-wrote mask_test_edges", 2019-12-05). The gap exists from this commit until the revert `0ebbe9b9a8` (2020-01-03, current HEAD). To see the gap, check out `e117287a84`; HEAD is the fixed state.
- **Target:** Table 1 of the paper, link prediction ROC AUC / AP, `gcn_vae` with features. Cora VGAE 91.4 / 92.6, Citeseer VGAE 90.8 / 92.0. Held-out claims from the same table: GAE (`--model gcn_ae`) on Cora and Citeseer, and the no-features variants (`--features 0`) that the paper reports in the same table.
- **Documented cause (code):** PR #25 rewrote `mask_test_edges` and changed its defaults to `test_percent=30., val_percent=20.` (the original held out 10% test and 5% validation positive edges). `train.py` calls `mask_test_edges(adj)` with no arguments, so more edges are removed from the training graph. Reported numbers drop to Cora AUC 84.8 / AP 87.8 and Citeseer 86.6 / 88.7.
- **Sources:** https://github.com/tkipf/gae/issues/54 ("can't reproduce the results in the paper"); PR https://github.com/tkipf/gae/pull/25 (diff shows the 30/20 defaults); revert commit `0ebbe9b9a8`.
- **Quote (tkipf, issue 54):** "This is potentially related to this pull request: https://github.com/tkipf/gae/pull/25 ... you could try rolling back this change". Reporter after rollback: "I reverted the code and now I can efficiently reproduce the results of the paper."
- **Cause type:** code (a changed procedure with a defaulted argument; the argument `test_percent/val_percent` is a clean knob for a harness that patches the call).
- **Feasibility:** Python 2.7 per README; works on Python 3 (the repo has a Python 3 adaptation commit `6771b3d`). TensorFlow 1.x (README says "TensorFlow 1.0 or later"), networkx, scikit-learn, scipy. Datasets (Cora, Citeseer) ship in `gae/data`. Flags via absl/tf flags: `--model gcn_vae --dataset cora --epochs 200 --features 1`. Checked it runs: **no**.
- **Sandboxes fit:** Cora/Citeseer only. Peak memory about 1 GB (estimate: N x N logits are 2708^2 x 4 B = 29 MB, 3327^2 x 4 B = 44 MB, plus TF1 overhead). Time about 1-3 min per run (200 epochs on a 2.7k-node graph). **Exclude Pubmed**: the code builds dense N x N tensors, and 19717^2 x 4 B = 1.55 GB per tensor, so with gradients it is over budget. Basis: dataset/model sizes.
- **Harness notes:** splits are random each run (the code NOTEs this), so use at least 10 seeds with `np.random.seed`. The environment needs TF1, so use Python 3.7 and `tensorflow==1.15.x`. The paper's reported seeds/runs are 10.

---

## Case 2. GAT on PubMed: dataset-specific heads, L2, and early-stopping rule (PetarV-/GAT)

- **Paper:** Velickovic et al., "Graph Attention Networks", ICLR 2018. https://arxiv.org/abs/1710.10903
- **Repo:** https://github.com/PetarV-/GAT, commit `5af87e7fce2b90ae1cbd621cd58059036a3c7436`.
- **Target:** Table 2, PubMed node classification accuracy 79.0 +- 0.3%. Held-out claims: Cora 83.0 +- 0.7, Citeseer 72.5 +- 0.7 from the same table (repo's `pre_trained/` Cora model gets 84.4% on a single run).
- **Documented cause (setting plus a code-level stopping rule):** The PubMed experiment needs settings different from the Cora defaults in `execute_cora_sparse.py`: `lr = 0.01` (default 0.005), `l2_coef = 0.001` (default 0.0005), `n_heads = [8, 8]` (default `[8, 1]`: K = 8 output heads), plus a different early-stopping rule. Running with the paper's stated hyperparameters gave 77.7 +- 0.8; after the author's early-stopping change the reporter got 78.8 +- 0.3.
- **Sources:** https://github.com/PetarV-/GAT/issues/12 (author PetarV- replied); paper Section 3.3 / Appendix A.
- **Quote (PetarV-, issue 12):** "Regarding the PubMed setup, we have found that slight changes to the early stopping strategy were necessary. Namely, we early stop based on the loss only in this case."
- **Cause type:** setting (three module constants) plus code (the early-stopping condition: shipped code saves when `val_acc >= best AND val_loss <= best`; PubMed needs `val_acc >= best OR val_loss <= best` with the checkpoint saved only when loss improves).
- **Feasibility:** README tested Python 3.5.2, numpy 1.14.1, scipy 1.0.0, networkx 2.1, tensorflow-gpu 1.6.0; use `tensorflow==1.15.x` on Python 3.7 (CPU). Constants are plain module-level names (`dataset = 'cora'`, `lr`, `l2_coef`, `n_heads`, `patience`); a harness must sed them. The repo ships only Cora data. `process.load_data('pubmed')` needs `ind.pubmed.*` files from https://github.com/tkipf/gcn/tree/master/gcn/data copied to `data/`. Checked it runs: **no**.
- **Sandboxes fit:** Peak memory about 1-1.5 GB (estimate: PubMed 19717 x 500 float features = 40 MB, 88k edges, sparse GAT with batch size 1, 8 x 8 hidden units). Time about 10-30 min per run (estimate: about 1-3 s per epoch on 4 CPUs, a few hundred epochs before patience 100 stops). Budget 5-10 seeds, not the paper's 100. Basis: dataset/model sizes.
- **Harness notes:** the sparse script (`execute_cora_sparse.py`) is the one that scales to PubMed; the dense `execute_cora.py` would need a 19717^2 dense adjacency (1.5 GB) and should not be used.

---

## Case 3. GIN on social graphs: defaults are not the paper's (powerful-gnns, setting)

- **Paper:** Xu, Hu, Leskovec, Jegelka, "How Powerful are Graph Neural Networks?", ICLR 2019. https://arxiv.org/abs/1810.00826
- **Repo:** https://github.com/weihua916/powerful-gnns, commit `9a2ce8ac3e99278307093a464a95caf0fb04b602`.
- **Target:** Table 1, GIN-0 (SUM-MLP) on IMDB-BINARY 75.1 +- 5.1; held-out: IMDB-MULTI 52.3 +- 2.8, MUTAG 89.4 +- 5.6, PROTEINS 76.2 +- 2.8, PTC 64.6 +- 7.0, NCI1 82.7 +- 1.7 (from the same table).
- **Documented cause (setting):** `main.py` defaults are bio/chem defaults. For social graphs the paper uses `--degree_as_tag` (one-hot degree features, needed for IMDB and COLLAB), average graph pooling (`--graph_pooling_type average`; sum pooling only for bio/chem), 64 hidden units for social vs 16/32 for bio, batch size from {32, 128}, dropout from {0, 0.5}, and a chosen epoch. Without these the accuracy is far off (COLLAB below 70% vs 80.2 in the paper).
- **Sources:** https://github.com/weihua916/powerful-gnns/issues/13 and https://github.com/weihua916/powerful-gnns/issues/2 and https://github.com/weihua916/powerful-gnns/issues/20 (reporter: "Thank you very much. It works for COLLAB").
- **Quote (owner weihua916, issue 13):** "Have you correctly specified --graph_pooling_type? We used the sum graph pooling for bio/chemistry datasets and the mean graph pooling for social network datasets. Have you added --deg_as_tag ... for IMDB and COLLAB?" Owner on defaults (issue 19): "I did not record them" (the exact per-dataset hyperparameters).
- **Cause type:** setting.
- **Feasibility:** README: PyTorch 0.4.1/1.0.0 tested, `pip install -r requirements.txt`; works on modern torch with small edits (unverified). `dataset.zip` (33 MB, in the repo) holds MUTAG, IMDBBINARY, IMDBMULTI, PROTEINS, PTC, NCI1, COLLAB, REDDIT. Flags via argparse (`--dataset IMDBBINARY --degree_as_tag --graph_pooling_type average --fold_idx k --epochs`). Checked it runs: **no**.
- **Sandboxes fit:** IMDB-BINARY (1000 graphs, 19.8 avg nodes): peak memory under 1 GB (estimate). Time: default 350 epochs x 50 iterations at batch 32 is about 5-10 min per fold on 1 CPU (estimate), so run folds in parallel (4 at a time) and cut epochs to about 100 (the owner says 350 is not needed, issue 2): about 15-25 min total for 10 folds. **Do not use COLLAB or REDDIT-B**: COLLAB is 5000 graphs with about 2.5k edges each, the same dense-graph pattern that OOM-killed GraphMAE; the code keeps python neighbor lists for all graphs, so more than 3 GB is likely. Basis: dataset sizes and loop counts.
- **Harness notes:** `--fold_idx` runs one fold per call; the script prints per-epoch train/"test" accuracy to stdout only (the `--filename` file is overwritten each epoch and keeps only the last epoch). Capture stdout.

---

## Case 4. GIN: the reported number is a model-selection score (powerful-gnns, protocol in code)

- **Paper:** same as Case 3.
- **Repo:** same repo and commit as Case 3 (a separate experiment on PROTEINS/MUTAG/PTC/NCI1).
- **Target:** Table 1 GIN-0 on PROTEINS 76.2 +- 2.8; held-out: MUTAG 89.4 +- 5.6, PTC 64.6 +- 7.0, NCI1 82.7 +- 1.7.
- **Documented cause (code/protocol):** In `main.py` the "test" set of each of the 10 folds is really the held-out fold, evaluated every epoch; the paper's number is the maximum over epochs of the fold-averaged accuracy curve, with that single best epoch chosen from the same curves. The README says so itself: "we first took average of validation curves across the 10 folds" and "selected a single epoch that achieved the maximum averaged validation accuracy". Errica et al. state: "they report the validation accuracy of 10-fold CV. In other words, reported results refer to model selection and not to model evaluation." Under a clean nested protocol GIN gets PROTEINS 73.3 +- 4.0 and NCI1 80.0 +- 1.4 (their Table 3), about 3 points lower, and they say published results differ "in most cases" with a consistent gap.
- **Sources:** Errica, Podda, Bacciu, Micheli, "A Fair Comparison of Graph Neural Networks for Graph Classification", ICLR 2020, https://arxiv.org/abs/1912.09893 (Sections 3, 4, 6.3, Table 3); README of the repo; https://github.com/weihua916/powerful-gnns/issues/19.
- **Cause type:** code (evaluation procedure: epoch selected on the fold-averaged held-out curve).
- **Feasibility:** as Case 3. Checked it runs: **no**. The honest-protocol number would need the harness to implement an inner validation split; Errica's own code is at https://github.com/diningphil/gnn-comparison (not examined).
- **Sandboxes fit:** PROTEINS (1113 graphs, 39 avg nodes) or MUTAG (188 graphs): peak memory under 1.5 GB, per fold about 10-20 min at 350 epochs (estimate); use 100-150 epochs and 4 parallel folds. Basis: dataset sizes, loop counts.
- **Harness notes:** to get the paper's number the harness must log per-epoch accuracy for all 10 folds and take the argmax of the mean curve. The gap is the difference between that and the final-epoch or inner-validation-selected accuracy.

---

## Case 5. PatchTST supervised: `drop_last=True` in the test loader (yuqinie98/PatchTST)

- **Paper:** Nie et al., "A Time Series is Worth 64 Words: Long-term Forecasting with Transformers", ICLR 2023. https://arxiv.org/abs/2211.14730
- **Repo:** https://github.com/yuqinie98/PatchTST, commit `204c21efe0b39603ad6e2ca640ef5896646ab1a9`. At this commit `PatchTST_supervised/data_provider/data_factory.py` still has `drop_last = True` for the test flag (checked in the raw file), although the authors said they would change it.
- **Target:** supervised PatchTST/64 on ETTh1 (lookback 336, MSE at horizons 96/192/336/720; paper values about 0.370 / 0.413 / 0.422 / 0.447, from memory, to be checked against the paper) and Illness/ILI (horizons 24/36/48/60). Held-out: other horizons and datasets in the same table.
- **Documented cause (code):** the test DataLoader drops the last incomplete batch, so a different subset of test windows is scored (and the subset depends on `--batch_size`); on small datasets (ETTh1, ETTh2, ILI) this lowers the reported error.
- **Sources:** https://github.com/yuqinie98/PatchTST/issues/7 (authors confirm); FITS README (https://github.com/VEWOXIC/FITS, "Description of the Bug") listing PatchTST, DLinear (reported version), Informer, Autoformer, FEDformer, FiLM as affected; SparseTSF https://arxiv.org/abs/2405.00946.
- **Quote (author namctin, issue 7):** "you are correct that setting drop_last=True will lead to the number of test samples not to be consistent with different choices of the batch size". Reporter oguiza: "the result is worse than the published one" on ILI with `drop_last=False`; ts-kim: "for the ETTh1, Traffic, and Illness datasets, there was a drop in performance, while there was no drop for the Weather dataset."
- **Cause type:** code (hard-coded flag in the data factory; not exposed on the command line). It needs a one-line patch.
- **Feasibility:** Python 3.8-3.10, torch, numpy, pandas, scikit-learn (`requirements.txt`). Scripts at `PatchTST_supervised/scripts/PatchTST/etth1.sh` (seq_len 336, batch 128, patch_len 16, stride 8, d_model 16, e_layers 3, n_heads 4, d_ff 128, lr 1e-4, epochs 100) and `illness.sh` (seq_len 104, batch 16, patch_len 24, stride 2, lr 0.0025, epochs 100). Note the shipped `illness.sh` has an undefined `$model_id_name_` variable. Data: the Autoformer Google Drive bundle (`all_six_datasets`) per the README; ETTh1.csv is also at https://raw.githubusercontent.com/zhouhaoyi/ETDataset/main/ETT-small/ETTh1.csv, but `national_illness.csv` is only on the Drive bundle, so mirror it at build time. Checked it runs: **no**.
- **Sandboxes fit:** peak memory about 1-1.5 GB (estimate: torch overhead; a 128 x 7-channel batch of 42 patches x 16 dims is a few MB). Time: ETTh1 about 10 s per epoch on 4 CPUs (about 66 iterations at batch 128, channel-independent so 896 sequences per batch), 100 epochs at most, early-stopped, so about 5-20 min per horizon; ILI about 5 min. Basis: model/dataset sizes.
- **Harness notes:** the effect is evaluation-only; the same trained model scored with `drop_last=False` gives the "true" number, so one training run yields both numbers.

---

## Case 6. Informer on ETTh2: per-dataset hyperparameters differ from the defaults (zhouhaoyi/Informer2020)

- **Paper:** Zhou et al., "Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting", AAAI 2021 (Best Paper). https://arxiv.org/abs/2012.07436
- **Repo:** https://github.com/zhouhaoyi/Informer2020, commit `29f2a739226a509202a092b464163da81fa74960`.
- **Target:** Table (multivariate) ETTh2, horizon 24 (the paper's table lists ETTh2 with horizon 48 MSE 0.720; the horizon-24 value must be read from the paper's multivariate table, I did not extract it). From the issue: the repo's default/Colab configuration gives ETTh2 MSE 0.869, MAE 0.762, whereas the authors' ETTh2 configuration gives MSE 0.490-0.539, MAE 0.539-0.578.
- **Documented cause (setting):** `main_informer.py` defaults (`seq_len 96, label_len 48, pred_len 24, e_layers 2, d_layers 1, d_ff 2048`; the Colab used `e_layers 3, d_layers 2, d_ff 512`) are tuned for ETTh1; ETTh2 needs different hyperparameters. The authors add that the code's data scaling was changed after the arXiv version, so the paper's numbers were produced under older scaling, and that the ETTm1/ETTm2 files in the ETDataset repo had swapped names.
- **Sources:** https://github.com/zhouhaoyi/Informer2020/issues/44 (collaborator cookieminions and owner replied).
- **Quote (cookieminions):** "ETTh2 has different characteristics compared to ETTh1, so you have to change hyper parameters. You can try `seq_len=48; label_len=24; pred_len=24; d_ff=2048; e_layer=2; d_layer=1`". And: "our current code has updated the data scaling way compared with the paper on arxiv".
- **Cause type:** setting (argparse flags).
- **Feasibility:** README pins Python 3.6, torch 1.8.0, numpy 1.19.4 (versions from the README, not rechecked; newer torch works with minor edits, unverified). Data from https://github.com/zhouhaoyi/ETDataset (`ETT-small/ETTh2.csv`; note the ETTm1/ETTm2 naming problem, so use ETTh2 only). Flags: `--model informer --data ETTh2 --features M --seq_len 48 --label_len 24 --pred_len 24 --e_layers 2 --d_layers 1 --d_ff 2048 --use_gpu False`. Beware: `--use_gpu` is `type=bool`, and the code also checks `torch.cuda.is_available()`, so on a CPU machine it falls back correctly. Checked it runs: **no**.
- **Sandboxes fit:** peak memory about 1.5 GB (estimate: d_model 512, batch 32, encoder length 48, ProbSparse attention). Time: about 270 iterations per epoch x about 0.5-1 s on CPU gives 2-5 min per epoch, 6 epochs with patience 3, so about 15-30 min per run (the default `--itr 2` doubles it, so set `--itr 1`). Basis: model/dataset sizes.
- **Harness notes:** Informer has the same `drop_last=True` test-loader bug as Case 5 (`exp/exp_informer.py` `_get_data`, test flag), so a second held-out factor exists; the maintainers did not document it in this issue, FITS did.

---

## Case 7. Anomaly Transformer: point-adjustment hard-coded in evaluation (thuml/Anomaly-Transformer)

- **Paper:** Xu et al., "Anomaly Transformer: Time Series Anomaly Detection with Association Discrepancy", ICLR 2022 (Spotlight). https://arxiv.org/abs/2110.02642
- **Repo:** https://github.com/thuml/Anomaly-Transformer, commit `b0ee470c8012bff857fb600462aec6209c4a18d9`.
- **Target:** main results table, F1 on SMD (paper about 92.3; from memory, not re-extracted). Held-out: precision and recall in the same table; the same model's raw (unadjusted) F1.
- **Documented cause (code):** `solver.py` `test()` applies "detection adjustment" (point adjustment): if any point in a ground-truth anomaly segment is flagged, the whole segment is marked correct, using the ground truth. The authors confirm it is used and say it is "just for computing the metric". Removing it collapses the score. Also, `vali()` is run on the test loader (`self.val = self.test` in the data loader) and the threshold is computed from train plus test energies.
- **Numbers from the issues:** MSL: with adjustment F1 0.9314 (P 0.9161, R 0.9473); without it F1 0.0199 (P 0.1120, R 0.0109). SMD: with 0.9061, without 0.0236. SMAP: with 0.9623, without about 0.02 (value truncated in the thread). A reviewer's fake prediction of one anomaly every 100 points gives MSL F1 0.8492 with the adjustment.
- **Sources:** https://github.com/thuml/Anomaly-Transformer/issues/4, https://github.com/thuml/Anomaly-Transformer/issues/14 (author wuhaixu2016 explains the choice), https://github.com/thuml/Anomaly-Transformer/issues/27 (validating on the test loader); independent analysis: Kim et al., "Towards a Rigorous Evaluation of Time-Series Anomaly Detection", AAAI 2022, https://arxiv.org/abs/2109.05257, and "Position: Quo Vadis, Unsupervised Time Series Anomaly Detection?", https://arxiv.org/abs/2405.02678 (a random scorer gets point-adjusted F1 0.931 on MSL and 0.961 on SMAP; unadjusted about 0.19 and 0.23).
- **Quote (wuhaixu2016, issue 14):** "the adjustment is a widely-used convention in time series anomaly detection ... we also adopt the adjustment for model evaluation" and (in Chinese) "this adjustment is only for computing the metric".
- **Cause type:** code (evaluation step hard-coded in `solver.py` lines about 339-360; no flag).
- **Feasibility:** README: Python 3.6, PyTorch >= 1.4. Datasets only via a shared Google Drive folder (SMD, MSL, SMAP, PSM; SWaT needs an application), so a harness must mirror them at build time (fragile). Scripts `scripts/SMD.sh` (10 epochs, batch 256, `--input_c 38 --anormly_ratio 0.5`; note the misspelled `anormly_ratio`). Checked it runs: **no**.
- **Sandboxes fit:** **SMD only.** SMD uses `step=100` windows (about 7k training windows, about 28 batches per epoch), while `MSL`, `SMAP` and `PSM` hard-code `step=1` (58k / 135k / 132k training windows per epoch), which would take hours on 4 CPUs. SMD memory: 708k x 38 float64 train plus test is about 430 MB plus scaler copies, so peak about 1.5-2.5 GB with torch (estimate, near the limit; use `float32` or load only one machine group if it is exceeded). Time: d_model 512, 3 layers, window 100, batch 256, about 5-10 s per batch, so about 5 min per epoch, 3-10 epochs, plus the test pass: about 20-60 min. Basis: dataset sizes and the `step` values read from `data_loader.py`.
- **Harness notes:** the harness should compute both adjusted and raw F1 from the same energies; the gap is that difference. Note `train()` checkpoints on a validation pass over the test set.

---

## Case 8. Neural Collaborative Filtering: best epoch picked on the test set (hexiangnan/neural_collaborative_filtering)

- **Paper:** He et al., "Neural Collaborative Filtering", WWW 2017. https://arxiv.org/abs/1708.05031
- **Repo:** https://github.com/hexiangnan/neural_collaborative_filtering, commit `4aab159e81c44b062c091bdaed0ab54ac632371f`.
- **Target:** ML-1M, HR@10 and NDCG@10 of NeuMF (paper about 0.730 / 0.447 at 8 predictive factors; from memory, to be checked against the paper's figures). Non-cherry-picked comparison numbers from Dacrema et al.: NeuMF (MLP+GMF) 0.7093 / 0.4349. Held-out: GMF, MLP, and Pinterest-20 columns.
- **Documented cause (code/protocol):** the training script evaluates on the test set every epoch (`evaluate_model(..., testRatings, testNegatives, ...)`) and keeps the epoch with the best test HR (`if hr > best_hr`), and the paper reports that best epoch. Verified in `GMF.py`: `best_hr, best_ndcg, best_iter` are updated from test metrics only.
- **Quote (Rendle et al.):** "the results for NeuMF and MLP in [16] were cherry-picked in the following sense: the metrics are reported for the best iteration selected on the test set."
- **Sources:** Rendle, Krichene, Zhang, Anderson, "Neural Collaborative Filtering vs. Matrix Factorization Revisited", RecSys 2020, https://arxiv.org/abs/2005.09683 (Section 3.4, Table 1); Dacrema, Cremonesi, Jannach, "Are We Really Making Much Progress?", RecSys 2019, https://arxiv.org/abs/1907.06902 and https://arxiv.org/abs/1911.07698; Anelli et al. (RecSys 2021) confirm reproducibility of the comparison, https://arxiv.org/abs/2107.13472.
- **Cause type:** code (evaluation protocol; leakage of the test set into stopping).
- **Feasibility:** README: Keras 1.0.7, Theano 0.8.0, Python 2.7 (`xrange` in the scripts); old but pip-installable in a py2.7 image (unverified, this is the main risk; a PyTorch port exists but would be a different codebase). Data ships in `Data/` (`ml-1m.train.rating` 21 MB, `ml-1m.test.rating`, `ml-1m.test.negative`, plus pinterest-20 at 21-27 MB each). Flags (argparse): `--epochs 20 --batch_size 256 --num_neg 4 --lr 0.001 --learner adam --num_factors 8 --out 0`. Checked it runs: **no**.
- **Sandboxes fit:** ML-1M: peak memory about 1 GB (estimate: 5M training instances x 3 int arrays about 120 MB, Theano overhead). Time: about 19k iterations per epoch at batch 256; about 1 min per epoch for GMF and perhaps 2 min for NeuMF on 4 CPUs (estimate), so GMF 20 epochs about 20 min and NeuMF without pretraining about 40 min: near the one-hour limit; reduce to 10-15 epochs if needed. Pinterest-20 has a larger training file (21 MB train, 27 MB negatives) and is not estimated; skip it. Basis: dataset sizes and iteration counts.
- **Harness notes:** to expose the gap the harness must log test HR per epoch and compare "best-epoch" with "last epoch" and with a validation-selected epoch (the repo has no validation split; leave-one-out latest item is the test item).

---

## Case 9. pygcn vs the GCN paper: split, normalization and input dropout (tkipf/pygcn)

- **Paper:** Kipf and Welling, "Semi-Supervised Classification with Graph Convolutional Networks", ICLR 2017. https://arxiv.org/abs/1609.02907
- **Repo:** https://github.com/tkipf/pygcn, commit `1600b5b748b3976413d1e307540ccc62605b4d6d`.
- **Target:** Cora test accuracy 81.5 (paper, Planetoid split, Table 2). In this repo the same default run gives a different value (a user reports 0.83 for pygcn vs 0.81 for the PyG and DGL GCN examples).
- **Documented cause (setting plus code):** the author lists the differences between the PyTorch port and the original TF code.
- **Quote (tkipf, issue 20):** "The data splits are different, the normalization of the adjacency matrix is slightly different ... there is no dropout on the first layer", clarified later: "the original TensorFlow-based implementation also uses Dropout on the input features directly (which is what I meant by first layer)". The PyG GCN example applies weight decay to the first convolution only (its code comment: "Only perform weight-decay on first convolution"); that this matches the original TF code is my recollection of the original code and is not verified here, so treat first-layer-only weight decay as a candidate extra factor.
- **Sources:** https://github.com/tkipf/pygcn/issues/20; https://github.com/pyg-team/pytorch_geometric/issues/891 (split differences between PyG, DGL and pygcn); PyG `examples/gcn.py`.
- **Cause type:** setting/code mix: three separate factors (split indices `range(140)/range(200,500)/range(500,1500)` in `utils.py` vs the Planetoid split; symmetric vs row normalization; input dropout; first-layer-only weight decay). It makes a good multi-factor attribution test.
- **Feasibility:** Python 3, PyTorch (any), scipy, numpy. Cora ships in `data/cora`. Flags via argparse: `--epochs 200 --lr 0.01 --weight_decay 5e-4 --hidden 16 --dropout 0.5 --seed 42 --no-cuda`. Checked it runs: **no**.
- **Sandboxes fit:** Cora, 2708 nodes, dense adjacency conversion in `utils.py` is sparse tensors; peak memory under 1 GB, time under 1 min per run (estimate). Basis: dataset size. No concerns.
- **Harness notes:** the split is hard-coded in `load_data()` (code); the Planetoid split would need the `ind.cora.*` files from tkipf/gcn. Run 10-100 seeds; the std is about 0.5-1 point.

---

## Case 10. GCN vs GAT on Cora/CiteSeer/PubMed: the ranking depends on the split (PyG benchmark, split/noise)

- **Papers:** GAT (Velickovic et al. 2018, Cora 83.0 +- 0.7) vs GCN (Kipf and Welling 2017, Cora 81.5). Documented by Shchur, Mumme, Bojchevski, Guennemann, "Pitfalls of Graph Neural Network Evaluation", 2018. https://arxiv.org/abs/1811.05868
- **Repo:** https://github.com/pyg-team/pytorch_geometric, `benchmark/citation/` (`gcn.py`, `gat.py`, `run.sh`); HEAD `79d33965a40b7fa83616a9f598a0f8619f25d939`; prefer a release tag such as `2.3.1` (`ff9fb3d7cdbaa2f2b8a848fb6cc5f4c3f465118c`) so the scripts match the installed package.
- **Target:** accuracy of GAT vs GCN on the Planetoid split (`python gat.py --dataset=Cora`, `python gcn.py --dataset=Cora`) and on random splits (`--random_splits`). Held-out: the same on CiteSeer and PubMed (PubMed GAT needs `--lr=0.01 --weight_decay=0.001 --output_heads=8`, as in `run.sh`).
- **Documented finding (noise/split):** Shchur et al. Table 2b, Planetoid split: GCN 81.9 +- 0.8, GAT 82.8 +- 0.5 on Cora; a random split with the same sizes: GCN 79.0 +- 0.7, GAT 77.9 +- 0.7, so the ranking flips. "If we ... consider a different random split ... the ranking of models is completely different, with GCN being first on CORA and CiteSeer." Also GAT on Cora on the Planetoid split at 100-run means is within noise of GCN on several seeds. A PyG maintainer says `benchmark/citation/gat.py` "achieves around 83.1% on Cora" (https://github.com/pyg-team/pytorch_geometric/issues/338), and that PyG vs TF differences "can differ by small margins".
- **Sources:** https://arxiv.org/abs/1811.05868 (abstract, Table 2); https://github.com/pyg-team/pytorch_geometric/issues/338; benchmark `run.sh` (cited command lines).
- **Cause type:** noise / split (documented finding is that the claimed GAT-over-GCN margin is within split variance and flips with the split).
- **Feasibility:** `pip install torch torch_geometric==2.3.1` (CPU), datasets downloaded by PyG from the planetoid GitHub repo at build time. Flags via argparse: `--dataset --random_splits --runs 100 --epochs 1000 --early_stopping 100 --lr --weight_decay --output_heads`. Checked it runs: **no**.
- **Sandboxes fit:** Cora/CiteSeer: peak memory about 1 GB (estimate), GCN about 2-4 s per run, GAT about 10-20 s per run on 4 CPUs, so 100 runs about 20-35 min. PubMed GAT: heavier (about 1 min per run, estimate): use 10-20 runs. Basis: dataset sizes and model sizes.
- **Harness notes:** `--random_splits` is the knob; treat the Planetoid-split number as the paper claim and the random-split number as the held-out claim.

---

## Case 11. G-Mixup: the improvement over vanilla GNNs is not statistically significant (ahxt/g-mixup, noise)

- **Paper:** Han, Jiang, Liu, Hu, "G-Mixup: Graph Data Augmentation for Graph Classification", ICML 2022. https://arxiv.org/abs/2202.07179
- **Repo:** https://github.com/ahxt/g-mixup, commit `0813bb32319abbfb29fe82b9ee0c353a6862a1ad`.
- **Target:** Table 2, GCN on IMDB-B: vanilla 72.18 +- 1.55 vs G-Mixup 72.87 +- 3.85 (paper); REDDIT-B 78.82 vs 89.81 (paper). Held-out: PROTEINS and the GIN rows of the same table; mixup ratio and graphon resolution ablations.
- **Documented finding (noise):** the ReScience C reproduction runs the authors' code with 10 seeds and finds G-Mixup differences within the standard deviation: IMDB-B vanilla 73.15 +- 2.5 vs G-Mixup 71.3 +- 3.3 (reversed), PROTEINS 58.52 +- 3.11 vs 64.66 +- 5.06, REDDIT-B 81.4 +- 5.49 vs 84.8 +- 4.75; "our experimental results do not provide statistically significant evidence" and "we are unsure how the original paper's standard deviations are much lower than ours with the same experimental setup of 10 random seeds".
- **Source:** Cordaro, Cox, Ren, Yu, "[~Re] G-Mixup: Graph Data Augmentation for Graph Classification", ReScience C 9(2) #34, 2023. https://doi.org/10.5281/zenodo.8173737 (code: https://github.com/shelbycox/EECS-553-GMixup-Reproduction); the second reproduction [Re] G-Mixup, #1, https://doi.org/10.5281/zenodo.8173650 (not read in detail).
- **Cause type:** noise (seed variance; the gap between paper and rerun is not a setting).
- **Feasibility:** README pins python 3.7, torch 1.7.1, torch_geometric 1.6.3 with matching torch_scatter/sparse/cluster/spline_conv wheels (CPU wheels exist for torch 1.7.x), plus opencv-python 4.5.3.56 and scikit-image 0.18.3. Run with `run_vinilla.sh` and `run_gmixup.sh` (no CLI flags documented; edit the shell scripts). Datasets download via PyG at build time. Checked it runs: **no**.
- **Sandboxes fit:** **IMDB-B and PROTEINS only.** IMDB-B (1000 graphs, up to 136 nodes) and PROTEINS (1113 graphs): peak memory about 1.5 GB (estimate). Time: the reproducers report about 10 GPU-minutes per experiment on a T4; on 4 CPUs I estimate 10-30 min per seed, so budget 3-5 seeds in parallel. **Exclude REDDIT-B**: the reproducers hit memory limits generating graphons on Colab (12 GB RAM). Basis: reproducer's reported runtimes and dataset sizes, not measured.
- **Harness notes:** the point of this case is that a tool should report "within noise" rather than hunt for a cause; use at least 10 seeds.

---

## Case 12. Deep Knowledge Tracing: duplicated rows in the ASSISTments 2009 file (hcnoh/knowledge-tracing-collection-pytorch) [UNVERIFIED]

- **Paper:** Piech et al., "Deep Knowledge Tracing", NeurIPS 2015. https://arxiv.org/abs/1506.05908
- **Repo:** https://github.com/hcnoh/knowledge-tracing-collection-pytorch, commit `6151f490db17a290b0f4674c1a7c15a1a60c35f6`.
- **Target:** DKT test AUC on ASSISTments 2009 skill-builder: paper about 0.86; the repo's README table reports 82.15 +- 0.05. Held-out: DKVMN (81.18), SAKT (81.06) from the same README table, ASSIST2015.
- **Documented cause (setting: dataset version):** the ASSISTments 2009 skill-builder file widely used for the 0.86 figure contained duplicated interaction rows, so a duplicate puts an interaction's own label inside its own history; after deduplication DKT AUC falls to about 0.73-0.75 (or about 0.82 on the corrected file under common preprocessing). The ASSISTments site distributes both `skill_builder_data.csv` and `skill_builder_data_corrected.csv`.
- **Sources (second-hand; not verified against the original text):** Xiong et al., "Going deeper with deep knowledge tracing" (EDM 2016, not on arXiv, authors from memory) as cited by https://arxiv.org/abs/2609.28502 ("Xiong et al. documented the artifact and showed that removing the duplicates moves reported DKT performance from approximately 0.86 to the 0.73-0.75 range") and https://arxiv.org/abs/2403.15304; Sarsa et al., https://arxiv.org/abs/2112.15072 (DKT replicability study: re-runs about 81.4 AUC).
- **Cause type:** setting (data file / dedup preprocessing), if confirmed. **Needs checking**: which of the two files the repo's loader expects, and whether it deduplicates.
- **Feasibility:** README: Python 3, PyTorch >= 1.7.0 (avoid 1.9.0), `pip install -r requirements.txt`; config via `config.json` (batch 256, epochs 100, seq_len 100, lr 0.001, Adam, train_ratio 0.9). The data must be downloaded manually from the ASSISTments site into `datasets/ASSIST2009/` (not scriptable from the README alone, so find a stable URL at build time). Checked it runs: **no**.
- **Sandboxes fit:** about 525k interactions, 4k students; peak memory about 1 GB, DKT on CPU about 5-15 min for 100 epochs (estimate; sequences chopped to 100, about 30 batches of 256 per epoch). Basis: dataset size and config.
- **Harness notes:** low confidence on the cause attribution; keep this case last and flag it if the source loader differs from what I assume.

---

## Case 13. DP-SGD paper, Figure 2: epsilon values depend on the accountant and on a plotting bug (tensorflow/privacy) [low priority]

- **Paper:** Abadi et al., "Deep Learning with Differential Privacy", CCS 2016. https://arxiv.org/abs/1607.00133
- **Repo:** https://github.com/tensorflow/privacy (HEAD `e0c409035f0d302483b480a92ac555c5ee30c7fe`; the RDP accountant module `tensorflow_privacy.privacy.analysis.rdp_accountant` was later removed, so pin an older release tag; I did not identify the exact last tag that has it).
- **Target:** the paper's MNIST text: epsilon 1.26 after 100 epochs and 2.55 after 400 epochs (sigma and sampling ratio as in the paper). Figure 2 of the paper shows about 5 at 400 epochs. A current accountant gives 1.04 and 2.21.
- **Documented cause:** Mironov (an author of the accountant): "The moments accountant and the RDP accountant are basically equivalent ... I don't have a good explanation why the figure disagrees with the text (with the text being accurate). Let's chalk up the discrepancy to some buggy code that produced the graph." Later: the small improvement (1.26 to 1.04) "can be explained with switching the original implementation to the Renyi DP accountant."
- **Source:** https://github.com/tensorflow/privacy/issues/85
- **Cause type:** noise / not reproducible (a figure that cannot be reproduced; the accountant version changes the numbers).
- **Feasibility:** no training needed; `compute_rdp` / `get_privacy_spent` calls. Checked it runs: **no**.
- **Sandboxes fit:** negligible memory and under 1 s per call (estimate). Basis: analytic computation.
- **Harness notes:** a cheap sanity case with a numerical, accountant-version cause rather than an ML cause; use only if a case with no training is useful.

---

## Summary table

| # | Paper (repo) | Target | Documented cause | Type | Sandboxes fit (peak RAM, time per run; estimates) | Run checked |
|---|---|---|---|---|---|---|
| 1 | VGAE (tkipf/gae @ e117287) | Cora VGAE AUC 91.4 / AP 92.6 | `mask_test_edges` default split 30%/20% instead of 10%/5% | code | ~1 GB, 1-3 min (Cora/Citeseer only; Pubmed excluded) | no |
| 2 | GAT (PetarV-/GAT @ 5af87e7) | PubMed 79.0 | lr 0.01, l2 0.001, 8 output heads, loss-only early stop | setting + code | ~1-1.5 GB, 10-30 min | no |
| 3 | GIN (powerful-gnns) | IMDB-B 75.1 | `--degree_as_tag`, mean pooling, 64 hidden vs defaults | setting | <1 GB, 15-25 min / 10 folds (no COLLAB) | no |
| 4 | GIN (powerful-gnns) | PROTEINS 76.2 | max over epochs of fold-averaged held-out curve = model selection (Errica: 73.3) | code/protocol | <1.5 GB, 10-20 min per fold | no |
| 5 | PatchTST (yuqinie98) | ETTh1 336/96 MSE ~0.370; ILI | test loader `drop_last=True` | code | ~1-1.5 GB, 5-20 min | no |
| 6 | Informer (zhouhaoyi) | ETTh2 h=24 (default cfg 0.869 vs authors' cfg ~0.49-0.54) | per-dataset hyperparameters (seq_len 48, d_ff 2048, e_layers 2, d_layers 1) | setting | ~1.5 GB, 15-30 min | no |
| 7 | Anomaly Transformer (thuml) | SMD F1 ~92.3 (0.906 adjusted vs 0.024 raw in issue) | point adjustment hard-coded in `solver.py` | code | ~1.5-2.5 GB (near limit), 20-60 min; SMD only | no |
| 8 | NCF (hexiangnan) | ML-1M NeuMF HR@10 ~0.730 (clean 0.709) | best epoch selected on test set | code | ~1 GB, 20-40 min (Python 2.7 / Theano risk) | no |
| 9 | GCN (tkipf/pygcn) | Cora 81.5 | splits, normalization, input dropout, first-layer weight decay | setting + code | <1 GB, <1 min | no |
| 10 | GCN vs GAT (PyG benchmark/citation) | Planetoid vs random split ranking | split variance flips ranking | noise | ~1 GB, 20-35 min per 100 runs | no |
| 11 | G-Mixup (ahxt/g-mixup) | IMDB-B 72.87 vs 72.18 | not significant over 10 seeds | noise | ~1.5 GB, 10-30 min per seed (no REDDIT-B) | no |
| 12 | DKT (hcnoh/...pytorch) | ASSIST2009 AUC ~0.86 | duplicated rows in the original 2009 file (second-hand source) | setting (data) | ~1 GB, 5-15 min | no |
| 13 | DP-SGD (tensorflow/privacy) | eps 1.26 / 2.55 (text) vs Fig. 2 | figure from buggy plotting code; accountant version | noise | negligible | no |

## Excluded after checking (so they are not re-researched)

- **Shifty / Fairness Guarantees under Demographic Shift** (MLRC 2022 reproduction): 115 CPU hours in total, and the code/paper deviations are not itemised. Over budget.
- **CrossWalk** (original https://github.com/ahmadkhajehnejad/CrossWalk and its ReScience reproductions): documented code-vs-paper discrepancy (the code adds 0.001 to the colorfulness estimate; the paper does not), but the reproduction needed 11 CPU-hours for 50 trials and the target numbers are read from plots. Not a clean numeric target.
- **Neural Arithmetic Units / NALU** (https://github.com/AndreasMadsen/stable-nalu): one run is 5 x 10^6 iterations, about 6 hours on one CPU core, per the authors.
- **ReLU'(0) paper** (ReScience #17): documented effect appears only in 16-bit training on GPU; no paper-vs-code gap.
- **[Re] Hierarchical Shrinkage** (ReScience #19): the cause is only "hyperparameter tuning of the RF regularizers was not specified"; no concrete setting.
- **SpectralNet** (https://github.com/KlugerLab/SpectralNet/issues/1): the thread suggests Python/TF versions but the maintainers never confirm a cause; also an MNIST/Reuters Keras model with old TF.
- **MVGRL** (https://github.com/kavehhassani/mvgrl/issues/2 and 7): the owner admits the DGL Cora split differs from the public split, but the owner never states that this explains the gap in issue 7.
- **LightGCN, MAML, Prototypical Networks, BERT4Rec**: the gap is documented in places but runs exceed the memory/time budget on 4 CPUs.
