# blind-1 result: FastGCN (ICLR 2018), the first blind real-paper case

**Verdict under the pre-registered rule: missed, and not confidently wrong.**
- GapFinder named the right setting (`learning_rate`) and moved it in the right direction, but chose
  0.005, with the careful label "Fits but unsupported".
- The documented value is 0.001, which is outside the sealed equivalence set {lr=0.001,
  lr=0.001 + epochs 100-200}.
- GapFinder tested 0.001, and on the target it was almost exact (0.817 against the paper's 0.818).
  It rejected 0.001 because the harness applied the same learning rate to the held-out inductive rows,
  and they got much worse.

## Timeline (all commits on `main`)

| Step | Commit |
|---|---|
| GapFinder frozen: tag `blind-1` | `b433ae0` |
| Sealer (a separate model) commits `case.md` and the answer-key hash | `485c080` |
| Runner builds the harness, runs the ledger and the search; the run and `PRE_REVEAL.md` are committed before the key is opened | `270a717` |
| Reveal: `sha256sum -c answer_key.sha256` gives `answer_key.md: OK` | this commit |

## The case (from `answer_key.md`)

- **Target:** Table 5, FastGCN-transductive on Cora, F1 0.818. Held-out claims: transductive Pubmed 0.776,
  inductive Cora 0.723, inductive Pubmed 0.721.
- **Documented cause** (repo issue #10, the repo owner): "For cora, the best learning rate is 0.001. You
  can also increase the total epoch to 200". The code's defaults are 0.01 and 100. The reporter then got
  81.4 ± 0.5.

## What GapFinder did (`run/gap_report.md`)

- **Calibration:** the default median was 0.799 over 5 runs, with a noise band of ±0.008. The gap is
  -2.3%.
- **Search:** 45 runs, all on `learning_rate`, which was the only knob any assumption named (see
  below). The values tried were 0.1, 0.001, 0.0001, 0.5, 0.02, 0.05, 0.0, 0.0002, 0.005 and 0.002.
- **Label:** "Fits but unsupported", `learning_rate=0.005`, gap -2.3% → -1.1%.
  - Counterfactual PASS.
  - All three held-out claims PASS.
  - Evidence FAIL ("0.005" appears nowhere).
  - The effect's interval excludes 0.

Medians of 4 runs per configuration (5 for the default):

| learning rate | trans Cora (paper 0.818) | trans Pubmed (0.776) | ind Cora (0.723) | ind Pubmed (0.721) |
|---|---|---|---|---|
| 0.01 (default) | 0.799 | 0.772 | 0.710 | 0.726 |
| **0.001 (documented)** | **0.817** | 0.770 | **0.641** | **0.686** |
| 0.002 | 0.815 | 0.766 | 0.685 | 0.722 |
| 0.005 (chosen) | 0.809 | 0.771 | 0.707 | 0.719 |

## Why it missed

1. **The held-out design, not the search.**
   - The harness runs all four Table 5 rows with *one* learning rate. At 0.001 the inductive model falls
     far below the paper on Cora (0.641 against 0.723), so the held-out check rejected the documented
     value. GapFinder then picked the closest value that harms nothing.
   - The sealer measured the same inductive drop. The owner's advice was about the transductive Cora run
     only. The paper's appendix says the learning rate was swept, so in effect each row had its own.
   - Sharing one setting across rows that were tuned separately turns a correct fix into a "conflict".
     This is the same structure as MC Dropout's per-split tuning, and in both cases GapFinder reported a
     conflict. On MC Dropout that was correct.
2. **A coverage gap that didn't matter here, but would have on another paper.**
   - The repo map doesn't read Python `tf.app.flags` (`flags.DEFINE_string('name', …)`), so the
     assumption step saw no flags. It invented names (`num_epochs`, `dropout_rate`, `hidden_dim`, …) and
     guessed wrong defaults (dropout "0.5" instead of 0.0, learning rate "0.001" instead of 0.01).
   - Only `learning_rate` matched a spec knob. The search screens knobs through assumptions, so
     `epochs`, `hidden1`, `dropout`, `weight_decay`, `early_stopping`, `max_degree` and `model` were never
     tested.
   - The documented cause happened to be the one knob that matched. If it had been `epochs`, GapFinder
     could not have found it.

## Post-hoc: not blind, and not counted

`posthoc-transductive/`: the same 45 recorded runs (resumed; no new sandbox runs, $0 billed), with only
the transductive Pubmed row as a held-out claim. That row is the same method as the target. This was
chosen *after* the reveal, so it is not evidence; it shows what the held-out choice did.
- **Label:** **Explained**, `learning_rate=0.001`, gap -2.3% → -0.2%.
  - Counterfactual PASS.
  - Held-out PASS.
  - **Evidence PASS:** the paper states the sweep set {0.01, 0.001, 0.0001}.
- **Equivalence set:** {0.001, 0.002, 0.005}, with 0.001 reported as the simplest.

## Safety and cost

- No confident label on a wrong setting.
- The first label was "Fits but unsupported": it told the reader that nothing supports 0.005, which is
  true.
- **Cost:** Nemotron $0.20 (the ledger); the search billed $0.00. The sandbox cost reported (unbilled in
  the Beta) was $11.88 for the search, plus $0.79 for the image build and smoke runs.

## Caveats

- **The sealer is an AI model, not a person:** a separate subagent (Claude Sonnet) the runner never read
  the key from. The runner also knew a few neutral facts from the sealer's hand-back (HARNESS.md).
- **One paper.** The harness (which rows share a knob) was the runner's choice, made before the reveal.

## Fixes made after the reveal, and what they do on FastGCN (post-hoc, not counted)

| Fix | Commit |
|---|---|
| 1. The repo map reads absl / `tf.app.flags` (multi-line calls, keyword arguments, `DEFINE_enum` choices; a line regex for files that don't parse) | `5fdae23` |
| 2. Ledger names map to spec knobs by their core words (`num_epochs` → `epochs`, `FLAGS.hidden1` → `hidden1`), and spec knobs no assumption names get a **fallback round**. It runs only when the ledger's knobs give no confident answer, so they don't take budget from the ledger's leads. | `e232bc9`, this commit |
| 3. Code defaults and paper-vs-code status are re-read from the code when it is available. A "code differs" the code can't confirm never yields "Paper-artifact inconsistency". | `e232bc9` |
| 4. `"tuned_separately": true` on a held-out claim: it is measured and shown as a NOTE, it isn't a veto, and it is left out of the joint history-matching fit | `4f763df` |
| 5. A fallback knob gets the paper's sentences that name it, matched by its whole name ("learning rate"), as evidence | this commit |

Post-hoc runs, all with the inductive rows marked `tuned_separately` and the target and transductive Pubmed
held-out unchanged:
- **`posthoc-fixed/` (fixes 1-4, a fresh ledger):**
  - The fresh ledger, which now saw the flags, came out different: 9 descriptive assumptions, and none
    named `learning_rate`. **Only the fallback round tested it.**
  - The label was "Fits but unsupported: `learning_rate=0.002`", with 0.001 in the set of equally good
    values.
- **`posthoc-fixed2/` (fixes 1-5, resumed from those runs):**
  - **Explained, `learning_rate=0.001`**, gap -2.4% → -0.2%.
  - Evidence: "We swept learning rate in the set {0.01, 0.001, 0.0001}".
  - The two inductive rows are shown as notes (worse under 0.001, as the sealer also measured).
  - It also lists 11 configurations the target alone can't tell apart (e.g. `epochs=10`): the
    documented answer is the simplest of them, not the only fit.

These runs were made with the answer known, so they show that the fixes work as designed. They are not
blind evidence. That needs blind-2.

**No regression on the dev suite.** Before = tag `blind-1`, runs 2600 and 2800. After = `4f763df`, fixes
1-4, runs 2700 and 2900. All 23 public tasks, 3 runs each, two replicates per side.
- **Correct causes:** 99/138 → 102/138, with 3 tasks better, 3 worse and 17 the same (sign test
  p = 1.0). This is within noise.
- **Confidently wrong:** 0 → 0.
- **Correct abstentions:** 114 → 114.

Fix 5 (paper-sentence evidence) is not exercised there, because the GapBench harness passes no paper
text. The practice tasks name their knobs plainly, so the fallback rarely runs. The fixes matter on
real repos like FastGCN, and the dev suite shows they cost nothing elsewhere.

## What to change (written at the reveal; done above, except where noted)

1. **Read `tf.app.flags` / absl flags in the repo map:** quoted names and `DEFINE_float` / `DEFINE_integer`.
2. **Screen every spec knob, even if no assumption names it,** with code-derived values. Also map
   assumption names to spec knobs by similarity (`num_epochs` → `epochs`).
3. **Check every LLM-guessed code default against the spec / repo map** before it is used.
4. **Held-out claims from separately tuned rows:**
   - let the harness give each row its own knob (`lr_trans`, `lr_ind`), or
   - mark held-out claims as "same configuration" or "separately tuned", and report a conflict with a
     separately tuned row as a note rather than a rejection.
   - This is a design question for the protocol, decided before the next blind case.
