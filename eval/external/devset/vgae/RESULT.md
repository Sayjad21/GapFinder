# Devset case 1: VGAE (Kipf & Welling 2016): the documented cause, found end to end

**Development set, not blind.** The cause is documented and was known (`../CANDIDATES.md`):
- tkipf/gae PR #25 changed `mask_test_edges(adj, test_percent=30., val_percent=20.)`, which every call
  uses as `mask_test_edges(adj)`;
- the paper held out 10% (test) and 5% (validation) of the edges;
- issue #54 shows the gap, and the revert reproduces the paper.

The case tests whether GapFinder's general machinery can find a cause that lives in code. Nothing in it is
specific to VGAE.

## Setup

- **Sandboxes image** (`case.json`, `../build_case.py`): python 3.7, TF 1.15.5, the repo at `e117287`. A cell
  runs the four Table 1 rows with features: VGAE and GAE, on Cora and Citeseer, two at a time. It takes
  about 80 s and peaks at 1.7 GB.
- **Target:** VGAE Cora AUC 91.4.
- **Held-out:** the other 7 numbers of the same rows. All share the split code, so none is tuned
  separately.
- **Knobs:** every tf flag that doesn't define the claim. The paper's stated values match their defaults.

## Three runs, each one after a fix

| Run | Code | Result |
|---|---|---|
| `run/` (120 runs) | `cf2b9fa` | "Fits but unsupported: `hidden1=320, dropout=0.5, learning_rate=0.002`". History matching said "**the naive configuration is within noise of every claim**" for a 5.8% gap, so no out-of-space diagnosis and no patch round. |
| `run2/` (+45) | discrepancy 0.05 → 0.01 | "Fits but unsupported: `hidden2=1600, learning_rate=0.002`". Now "2 configurations fit every claim": bigger layers partly make up for the removed training edges, so the case is in space and there is still no patch round. |
| `run3/` (+3) | patch round when unsupported; contrast quotes | **Paper-artifact inconsistency: `gae/preprocessing.py:32` `test_percent` 30 → 10, `val_percent` 20 → 5.** The gap goes from -5.8% to **+0.4%**. |

## What happened in run 3

1. **Static code check:** "`mask_test_edges(..., test_percent=30)`: a default no call in the repo
   overrides", and the same for `val_percent`.
2. **Contrast (one Super call):** both defaults against the paper's sentence "The validation and test sets
   contain 5% and 10% of citation links, respectively." The quote is verbatim in the paper and contains
   each value, so it becomes paper evidence.
3. **Patch round:** both defaults at the paper's values, together, in memory (no file edited).
4. **Verification:**
   - both counterfactuals: without `test_percent` the gap is -3.3%, without `val_percent` -2.2%;
   - all 8 held-out claims not worse beyond noise (VGAE and GAE, Cora and Citeseer, AUC and AP);
   - paper evidence;
   - the effect outside noise.

## The two general problems it exposed

1. **History matching's 5% discrepancy allowance** was meant for scaled-down surrogates (MC Dropout). With
   the 3-sigma cutoff, it let a gap of up to about 15% pass as noise.
   - The same thing happened on FastGCN (2.3%) and GraphMAE (2.2%).
   - It is now a harness property (`discrepancy` in the spec). A real-paper search without one uses 0.01,
     and MC Dropout's spec keeps 0.05.
2. **A code cause was only looked for when no setting fitted.** When settings fit only without evidence,
   and code leads exist, the contrast step and the patch round now run too. A patch replaces the answer
   only if it ranks better: here, with paper evidence, it does.

## Cost

- Nemotron: the ledger $0.10, plus the contrast call (cents).
- Sandboxes: 168 runs, unbilled.
