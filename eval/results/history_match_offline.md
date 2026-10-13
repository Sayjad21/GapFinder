# Multi-claim history matching, validated offline on recorded runs (post-hoc)

`eval/history_match.py` scores every measured configuration against every claim with an implausibility
I = |paper - measured mean| / sqrt(s^2/p + s^2/n + (d * paper)^2), where:
- s is the naive run-to-run SD;
- p is the number of runs behind the paper's number;
- d is a discrepancy fraction for scaled surrogates.

It keeps configurations with I <= 3 on every claim (NROY). No new runs, no model calls. These tasks'
answers are public, so this is a check of the method, not blind evidence.

**GapBench (12 tasks; p = 4.5, since the generator's paper value is a median of 7; d = 0.02):**

| Truth | Tasks | Diagnosis |
|---|---|---|
| setting cause (known cause, decoy, interaction; dev and former test) | 10 | 10 × "in-space explanation possible" |
| noise only (test-gen-07) | 1 | "reproduced within noise" |
| no cause (test-gen-01) | 1 | "out-of-space suspected" |
| incomplete: true knob not exposed (test-gen-02) | 1 | "out-of-space likely" |
| no cause (dev-rl-nocause) | 1 | **wrong**: "in-space explanation possible" (7 configs fit both claims within 3σ on a noisy RL metric) |

11 of 12 correct. The miss is equifinality on a noisy metric, and both GapFinder versions also gave no
confident answer there.

**MC Dropout (all logged arms, confirmation and post-hoc runs; p = 6.7, since the paper averages 20
splits and our runs average 3):**

| d | Diagnosis |
|---|---|
| 0 | out-of-space likely for Energy: no tested condition within 3σ, because the scaled surrogate (T=100, 3 splits) can't match at zero discrepancy |
| 0.05 | out-of-space suspected: Energy fits only (epochx=10, hidden=1); Yacht fits 7 others; none fits both |
| 0.10 | out-of-space suspected (the same picture) |

That is the authors' own explanation: the paper-era code shared tuned hyperparameters across splits
(test-set contamination), a code-level cause no setting can recreate. "Unexplained" becomes "Partially
explained (Energy) + out-of-space suspected". Data: `history_match_mcdropout.json`.
