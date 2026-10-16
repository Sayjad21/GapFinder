# blind-1: the run, and what the runner saw, written before the reveal

Written after the search finished and before `answer_key.md` was opened. The run in `run/` is committed
unchanged with this file.

## Inputs and command

- GapFinder at tag `blind-1` (`b433ae0`). The engine (`gapfinder/`) is unchanged since the tag. The report's
  provenance line names `485c080` only because the case files were committed after the tag.
- Ledger: `ledger/` (Nemotron, $0.20): 19 claims and 28 assumptions.
- Spec: `fastgcn.yaml`. Targets: `targets.json`. Harness: `HARNESS.md`. Image build: `build.py`
  (checkpoint `e6a5358e-5cb8-4cb3-afcb-7190e86cebb7`).
- Command:
  ```
  gapfinder search --spec eval/external/blind-1/fastgcn.yaml --targets eval/external/blind-1/targets.json \
      --assumptions eval/external/blind-1/ledger/assumptions.json --claims eval/external/blind-1/ledger/claim_ledger.json \
      --backend contree --concurrency 10 --max-runs 200 --paper "FastGCN (ICLR 2018)" --out eval/external/blind-1/run
  ```
- Environment:
  - `GF_B1_BASE` is the checkpoint above, and `GF_B1_SOURCE` is a local clone at `b8e6e64`;
  - `GF_SANDBOX_GUARD_USD=1000000`;
  - `GF_SANDBOX_CPU_LIMIT_S=6000`;
  - `GF_SPEND_CAP_USD=33`.

## Result

- **Label:** `C_trans_cora_f1` is **Fits but unsupported**, with `learning_rate=0.005`. The gap goes from
  -2.3% to -1.1%, the noise band is ±1.0%, and the held-out claims are not worse.
- **History matching:** "the naive configuration is within noise of every claim".
- **Budget:** 45 branch runs of the 200 allowed, and no patch round. Nemotron billed $0.00 in the search;
  the sandbox cost reported (unbilled) was $11.88.

## What went wrong in GapFinder (diagnosed from the run, before the reveal)

1. **The repo map found no flags.** FastGCN defines its settings with
   `flags.DEFINE_string('name', default, help)`, and `repo_map.py` only reads argparse and C++ gflags
   (an unquoted name). So the ledger's assumption step saw no flags and no defaults.
2. **So the assumptions used invented names and guessed defaults.** Ultra named them `num_epochs`,
   `dropout_rate`, `hidden_dim`, `early_stopping_patience`, `sample_size_layer1`, and so on. Several
   defaults are wrong: `dropout_rate` code default "0.5" (the code's is 0.0), `learning_rate` "0.001"
   (it's 0.01), `num_epochs` "200" (it's 100).
3. **Only `learning_rate` matched a spec knob by name.** The other 26 assumptions were reported as "not
   settable with this harness", although `epochs`, `dropout`, `hidden1` and `early_stopping` are spec
   knobs. The search screens knobs through assumptions, and spec knobs that no assumption names are never
   screened. So `epochs`, `hidden1`, `dropout`, `weight_decay`, `early_stopping`, `max_degree` and
   `model` were **never tested**, and the search ended at 45 runs with nothing left to try.
4. **The hard-coded sample size and batch size were not tested.** History matching put the naive
   configuration within noise of every claim, so the case never counted as out of space, and the patch
   round (which needs "out of space") never ran.

Whatever the key says, these are real limitations, found blind:
- a flag dialect the repo map doesn't read;
- no fallback that screens spec knobs which no assumption names, or maps assumption names to them;
- an LLM-guessed code default that isn't checked against the code.

**Protocol:** no re-run and no engine change before the reveal. Any fix and re-run after the reveal is
post-hoc and will be labelled so.
