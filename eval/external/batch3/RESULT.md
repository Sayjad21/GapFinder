# batch-3: results after the reveal (code frozen at tag `batch-3`, `92b1faa`)

The papers were picked and sealed by an independent sealer. The runs were committed in `bbddb9d` before the keys
were opened. Both keys match their sealed hashes:
- b3a: `9d95d74b...6269`
- b3c: `d8f08214...ecc3`

The keys are copied next to the cases (`b3a/answer_key.md`, `b3c/answer_key.md`). b3b is still with the sealer.

| Case | Documented cause | GapFinder | Score (the key's pre-registered rule) |
|---|---|---|---|
| **b3a** Variational Fair Clustering (AAAI 2021) | The paper states λ = 10 for Synthetic; the authors told the reproducers the value is wrong, and λ = 100 gives the reported numbers. Correct range: 60-1500 | **Fits but unsupported, `kmeans_synthetic_lmbda = 100`.** With it, all four K-means claims match exactly (objective and balance, +0.0%). The K-median Synthetic balance stays out of space, which the key says cannot be fully closed | **correct**: the named setting and value match (E1) |
| **b3c** SparseTSF (ICML 2024) | `drop_last = True` in the test loader (`data_provider/data_factory.py`, test branch): the reported MSE leaves out the last partial batch of test windows (ETTh2-336: 241 of 2545) | **Reproduced** (target -0.4%). The audit flags ETTh2-96 +4.0% and ETTh1-96 -1.4%, but not the truncation | **missed**: a correct abstention, cause not named |

**So far: 1 of 2 causes found, 0 confidently wrong.** This is the first sealed blind real paper where GapFinder named
the documented cause: blind-1 missed, blind-2 was confidently wrong, devbatch-1 found 1 of 5, devbatch-2 0 of 3.

## What went wrong, and its class

- **b3a, the label.**
  - GapFinder found the right value but couldn't say "the paper states λ = 10, and 100 fits", which would be a
    Paper-artifact inconsistency.
  - The cause: the harness splits `--lmbda` into one knob per (option, dataset) (`kmeans_synthetic_lmbda`, ...),
    and the ledger's λ didn't map to those names. The paper's 10 never became evidence on the knob, and the knobs
    were searched only in the fallback round.
  - The class: one program flag run as several knobs (also PyG's `gat_lr` and `gcn_lr`). The name mapping should
    map a paper setting to every knob that carries its flag, with the paper's per-row value where the paper gives
    one.
- **b3c, a reproduced number with a fixed switch in the test loader.**
  - Static checks now find `drop_last = True` (a switch passed to the DataLoader).
  - But when the target reproduces, nothing tests switches, and the audit lists only test-score selection and
    label edits.
  - The class (devbatch-2 again: a reproduced number is not audited): the protocol tests should cover switches
    in evaluation code (a test loader's `drop_last`) as they cover selection and label edits.

## The environment builder on these unseen repos

- b3c: built and ran (python:3.8, the requirements and the README's datasets, via gdown).
- b3a: failed after 15 commands. The repo pins `matplotlib==3.0`, which has no wheel and doesn't build on those
  images, and the switch to python:3.6 made it worse. Hand-built on python:3.8.
