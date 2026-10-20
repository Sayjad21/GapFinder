# Answer key b5c (SEALED: do not show to the runner before the run is committed)

## Paper and claims

- Paper: "BOND: Benchmarking Unsupervised Outlier Node Detection on Static Attributed Graphs", Kay Liu et al., NeurIPS 2022 Datasets and Benchmarks Track. arXiv 2206.10071v2.
- Repo: https://github.com/pygod-team/pygod, commit 61dd13f322cf598acb22976010217aecfd17380c (2023-08-16, "fix torch.mean(), max(), std()"). Its parent 987776c12dce665874b490a898dc319c90430c3e (2023-07-30) is the main-branch HEAD the issue below was filed against (2023-08-04); 61dd13f changes only `benchmark/main.py` so that the final print does not crash on Python lists. It is the first commit of PR #86, merged into main as 2508cd17f3bbf8da30eb624344f1ca6320c0f72b. Library version at this commit: PyGOD 1.0.0.
- Entry point: `cd benchmark && python main.py --model dominant --dataset inj_cora --gpu -1` (20 trials, hyperparameters drawn with `random.choice` from the grid in `benchmark/utils.py`).

Claims (DOMINANT, Cora with synthetic outliers = `inj_cora`, avg ± std (max) over the trials):

| table | metric | value |
|---|---|---|
| Table 3 | ROC-AUC (%) | **82.7** (main target) ± 5.6 (max 84.3) |
| Table 9 | Average Precision (%) | 20.0 ± 3.0 (20.8) |
| Table 11 | Recall@k (%) | 23.8 ± 4.0 (26.1) |

## Documented cause (setting that stopped taking effect after a library API change)

DOMINANT's balance weight between the attribute-reconstruction and structure-reconstruction errors. The paper's numbers were produced with PyGOD v0.3.1, where `DOMINANT(alpha=None)` (which `benchmark/utils.py` passes for every `inj_*`/`gen_*` dataset: lines 37-41, comment "auto balancing on injected dataset") triggers an automatic, data-dependent choice in `pygod/models/dominant.py` (v0.3.1, lines 132-135): `alpha = std(A) / (std(X) + std(A))`. For `inj_cora` this gives about 0.84. In PyGOD 1.0.0 (this commit) the parameter is called `weight`, has a fixed default of 0.5 and no automatic balancing; the benchmark still passes `alpha=choice([None])`, which lands in `**kwargs` and is silently dropped (torch_geometric 2.3's `MessagePassing.__init__` accepts and ignores unknown keyword arguments; on newer torch_geometric the same call raises `TypeError: ... unexpected keyword argument 'alpha'`). So every trial runs with weight 0.5.

Fix (any of): set DOMINANT `weight` to the auto-balanced value (about 0.84 on inj_cora; i.e. restore `weight = std(A)/(std(X)+std(A))`), or run the benchmark with PyGOD v0.3.1, the version used for the paper. The repo's later change (PR #86: rename to `weight`, draw it from [0.8, 0.5, 0.2]) moves results part of the way.

### Sources

1. https://github.com/pygod-team/pygod/issues/83 "Inconsistency with BOND paper" (opened 2023-08-04 by CaptainJuice; DOMINANT inj_cora "AUC: 0.7566±0.0332 (0.7751)" vs the paper's 82.7±5.6 (84.3)). Maintainer kayzliu (pygod-team member, first author of the paper), 2023-08-06: "you can reproduce the results by downgrading to the original version used by the benchmark v0.3.1 via `pip install pygod=0.3.1`." ... "the difference in the performance is mainly caused by the changes of parameter `weight` (`alpha` in v0.3.1) of `DOMINANT`. In the original benchmark, we apply a heuristic method [link to pygod/models/dominant.py#L132-L135 at a87e918, i.e. v0.3.1] to select the weight for `DOMINANT` (and some other methods) on injected datasets." ... "current benchmark script is out of date, ignoring the selection of `weight`." Contributor ParthaPratimBanik, 2023-08-17, after the rename to `weight` with the grid [0.8, 0.5, 0.2]: "now I got a maximum of ~0.8367 and a maximum average of ~0.78 on v1.0.0" (before that, "always within 0.75-0.77").
2. PR #86 (commits 61dd13f, 63ae71a "from alpha to weight", 1253451 "removing heuristic selection of weight", 65e02d2, 5563a1c), merged 2023-08-17.
3. Sealer's own check (laptop CPU, torch 2.8, torch_geometric 2.8.1 + pyg-lib, PyGOD installed from this commit; the `alpha` key removed from the detector kwargs to mimic the silent drop of torch_geometric 2.3; same `init_model` grid; 4 trials per arm, ROC-AUC):
   - weight 0.5 (what this commit runs): 0.7663, 0.7821, 0.7669, 0.7669, mean 0.771, max 0.782 (the issue reporter's 20 trials: 0.7566 ± 0.0332, max 0.7751).
   - weight = std(A)/(std(X)+std(A)) = 0.8432 (the v0.3.1 auto-balancing): 0.8430, 0.8427, 0.8420, 0.7090 (lr 0.1 trial), mean 0.809, max 0.843, i.e. the paper's 82.7 ± 5.6 (84.3) pattern of a high max with occasional low trials.
   - One trial took 65-145 s with 2 threads while another process ran in parallel.

### Decoys (not the cause)

- lr, dropout, hidden size, weight decay, epochs: the grid in `benchmark/utils.py` matches the paper's appendix grid and the contributor found no setting of these reaching AUC 0.80 with weight 0.5 / None on v1.0.0 (max ~0.769).
- The `main.py` print crash at 987776c (fixed by the named commit) is cosmetic.
- Random trial noise: the paper's std is 5.6, but trials at weight 0.5 stay near 0.75-0.77 while auto-balanced trials sit near 0.84.

## Pre-registered scoring rule

- **Correct**: the tool names DOMINANT's attribute/structure balance weight as the cause: the benchmark's `alpha` (auto-balancing via `alpha=None`) no longer has any effect in PyGOD 1.0.0, so the weight stays at the 0.5 default. Equivalence set (any one, at most 3): (a) set `weight` to the automatic value std(A)/(std(X)+std(A)) (about 0.84 on inj_cora) or a value in about 0.75-0.9; (b) run with PyGOD v0.3.1 (the library version used for the paper), naming the `alpha` auto-balancing as the reason; (c) pass the weight correctly (`weight=` instead of `alpha=`) together with restoring the auto-balanced value.
- **Partial**: names the weight/`alpha` parameter but not the right value or mechanism (for example "rename alpha to weight and draw from [0.8, 0.5, 0.2]", which only partly closes the gap), or says "use PyGOD v0.3.1" without identifying the weight as the factor.
- **Diagnosed out of space**: credited if the tool concludes that no flag of `main.py` explains the gap and attributes it to a library/code change between PyGOD versions (the cause lives in the library and the benchmark's kwargs, not in a command-line flag).
- **Confidently wrong**: a confident label on lr, dropout, hidden size, weight decay, epoch count, number of trials, the data version, the evaluation metric code, or random seed.
- **Not explained / inconclusive**: anything else.

Sealed 2026-10-20.
