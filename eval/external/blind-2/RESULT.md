# blind-2 result: GraphMAE (KDD 2022), the second blind real-paper case

**Verdict under the pre-registered rule: confidently wrong.**
- GapFinder labelled COLLAB "Explained" by `mask_rate=0.5`.
- The documented cause is `alpha_l=1`, the scaling factor γ of the SCE loss. The authors confirm it in
  issue #16, and their fix commit adds `alpha_l: 1` to COLLAB's `configs.yml` (and corrects the `pool:` key
  to `pooling:`).
- The sealed key lists `mask_rate` as "confidently wrong if the label is Explained".
- **This is GapFinder's first confident mistake on any blind test.** Before it: 0 in 90 sealed GapBench
  runs, and on blind-1 (FastGCN) a miss, not a confident mistake.

## Timeline (all on `main`)

| Step | Commit |
|---|---|
| GapFinder frozen: `v1.4` = `blind-2` | `e0568b6` |
| Sealer commits `case.md` and the key hash | `66a5056` |
| Harness, spec, targets and ledger committed before the search | `19d9adf` |
| Run and `PRE_REVEAL.md` committed before the key was opened | `8641e2f` |
| Reveal: `sha256sum -c` gives `answer_key.md: OK` | this commit |

## What happened

- **The run:** 59 Docker runs (COLLAB does not fit a Sandboxes VM; see HARNESS.md).
  - Naive median 78.56. The paper says 80.32; the issue reporter measured 78.78.
  - `mask_rate=0.5` gave 80.52, 80.22 and 79.58.
  - It passed the counterfactual, the held-out notes and the effect test. Its evidence was code evidence:
    the argparse default `--mask_rate 0.5` and `run_graph.sh`.
- **`alpha_l` was never tested.** This is the chain that led there:
  1. **The ledger never saw the paper's Table 8.** The assumption prompt carries the paper's setup
     section, capped at 25,000 characters. GraphMAE's per-dataset hyperparameters are in appendix
     Table 8, after the cut. Table 8 says COLLAB uses scaling factor γ = **1**, masking rate **0.75**,
     pooling **max** and hidden size **512**.
  2. **So the ledger wrote code values as paper values.** It recorded `--alpha_l` paper value "2.0", and its
     only evidence for the number is the argparse line `default=2`. Its paper quote doesn't contain it.
     The same happened to `pooling` ("mean") and `num_hidden` ("256").
  3. **The search skipped `alpha_l` as "stated and already matching".** A knob whose stated paper value
     equals the naive run's value is dropped from the screen, as one that "can't cause the gap". Paper "2"
     against naive 2 dropped the true cause before a single run.
  4. **`mask_rate=0.5` was an equally good fit, and its evidence was too weak to count.** It really does
     move COLLAB to the paper's number (equifinality). The evidence check accepted the argparse default,
     but for COLLAB that default is overridden by `configs.yml`, and Table 8 says 0.75. A default the
     authors' config replaces is not evidence that they used it.
- **The run was also partial:** the 60-run budget ended in the confirmation race. The label was verified
  from 3 runs. A full budget would not have helped here, though, because `alpha_l` was never a hypothesis.

## What GapFinder got right

- The pre-run disclosure: `pooling=max` (the `pool:` key) was screened and was not a lead (0.81 noise
  units). The sealer's own check agrees that pooling isn't needed (alpha_l alone: 80.50; with pooling max:
  80.46).
- **Fixes 1-4 worked as designed:**
  - the ledger used the code's real flag names (fix 1);
  - code defaults were read from the code (fix 3);
  - the held-out rows tuned separately were reported as notes (fix 4).

## Cost

- Nemotron $0.20 (the ledger); the search billed $0.00.
- Local Docker: about 14 hours of this machine.
- Sandboxes: the image build, the timing runs and the OOM diagnosis, all unbilled.

## What to change (post-reveal; for a later version)

1. **Read the whole paper's hyperparameter tables.** Append every table whose caption mentions
   hyper-parameters, settings or configuration, wherever it is, to the setup excerpt the assumption step
   sees. GraphMAE's answer was in plain sight in Table 8.
2. **A paper value needs a paper quote that contains it.** Grounding should demote a "stated" value whose
   number appears only in code evidence to "unstated".
3. **Don't drop a knob because its stated value matches the naive run; rank it last.** The ledger's stated
   values can be wrong, and the drop is irreversible.
4. **Code evidence must be about the configuration that runs.** An argparse default that the dataset's
   config overrides, or that the paper contradicts for this dataset, doesn't support a value.
5. **Normalise values before treating them as changes.** `False` and `false` are the default, not a
   candidate (PRE_REVEAL item 2).
6. **Consider no confident label from a partial run with fewer than the full confirmation repeats.**
