# batch-5: protocol (written before any case was seen)

A fresh sealed batch of 2-3 real papers: the first measure of the changes of 2026-10-19/20 (docs/CONTEXT_v11.md
section 7.1), and the first blind cases whose harness is built by `gapfinder harness`, not by a person or agent.

## Freeze

- Code: git tag `batch-5` (`0586e5c`). Runs use a worktree at that tag with its own `.env`.
- Nothing in `gapfinder/` changes until every run below is committed. A bug found on the way is written down
  in RESULT.md and fixed after the batch, never in it. Infrastructure failures (network, Sandboxes) may be
  re-run unchanged and are listed.
- Money: the owner's cap stays at $33 (about $1.1 left). If a case would pass the cap, it stops there and is
  reported as not run; the cap is not raised for this batch.

## Sealing

A separate sealer agent picks the papers (independently documented gap and cause, CPU-feasible in a Sandboxes
VM, arXiv source available, not used before), writes each answer key outside the repository, and commits
only `case.md` and `answer_key.sha256` here. The runner never opens a key before the run is committed.

## Per case, in order (no step is chosen with the answer in mind)

1. **Inputs:** the paper PDF at the arXiv version named in `case.md`; a local checkout at the named commit.
2. **Ledger:** `gapfinder ledger <pdf> --repo <checkout> --arxiv <id> --out <case>/ledger` (Ultra; the arXiv
   source supplement and the cited-setup step on).
3. **Claims:** the target and held-outs named in `case.md`. They are matched to ledger claims by value; a
   number the ledger missed is added to `<case>/claims.json` with the table and conditions `case.md` states
   (recorded). Held-outs that the paper tuned on their own get `tuned_separately` only from a quoted sentence.
4. **Harness:** `gapfinder harness <repo> --commit <sha> --local <checkout> --ledger <claims> --target <id>
   --repeats <n> --arxiv <id> --out <case>/harness`, with `n` the number of runs the paper averages (from
   `case.md`; 1 when it doesn't say). The runner reads HARNESS.md and may change only the commands, never
   the knobs; every change is recorded. If the harness stops at a step, the case is reported as
   "harness failed at <step>" and is not built by hand.
5. **Search:** `gapfinder search --spec <case>/harness/spec.yaml --targets <case>/harness/targets.json
   --assumptions <case>/ledger/assumptions.json --claims <case>/ledger/claim_ledger.json --backend contree
   --max-runs 150 --out <case>/run`.
6. Commit the run; then open the key, check its hash, score it with the key's own rule, write RESULT.md.

## What is measured

- Per case: the verdict under the key's rule (correct / partial / diagnosed out of space / missed /
  confidently wrong).
- The harness: how far `gapfinder harness` got unaided (step reached), and what a person had to change.
- Cost per case.

## Addendum (2026-10-20, after b5a's reveal): b5b and b5c under tag `batch-5b`

b5b and b5c stopped at the harness under `batch-5` (RESULT.md) and their keys were never opened. The harness
(not the engine) was then extended for the formats they exposed, each a general class: README help syntax and
alternative lists, READMEs in subfolders, metrics printed without a separator and line tags, the metric names
AP/NMI/ARI, a flag whose string value is one of the claim's conditions fixed as defining the claim, one copy at a
time when parallel copies fail, and two recorded approval levers (`--command`, `--bind`). b5b and b5c run under
tag `batch-5b` with the same steps as above. The levers are used only with what `case.md` states (its entry
point, its mapping of printed lines to columns), and every use is recorded. That the harness now builds these
two cases is not evidence for the harness changes (they were revealed by them); the searches' results are
evidence for the engine, which is unchanged since `batch-5`.
