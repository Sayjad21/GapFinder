# How to make GapFinder find real causes: research synthesis

*2026-10-13. Method: 5 parallel research agents (Sonnet), one per angle, using web search and
fetched sources; then an adversarial verification pass on the 10 most important claims (verdicts in §7).
Unverified items are marked.*

---

## 1. Bottom line

GapFinder's blind miss on MC Dropout, and its low recall on real papers in general, come from
**hypothesis generation**, not verification. Verification already behaves correctly (the post-hoc run proved it).
The research points to **five fixes**. Together they would have reached the documented MC Dropout cause without
weakening the zero-false-attribution property:

1. **Extract settings as typed relations and compute the value, don't guess it.** Record "10× more iterations"
   as `multiplier_of(10, reference=…)`, then resolve it in code against the repo's real knob
   (`epochx` × base 40 epochs). That's PAL-style arithmetic offloading, plus a numeric direction check.
2. **Mine the repo's history and docs as hypothesis sources.** Diff the paper-era commit against HEAD
   (old hard-coded literals → new flags), read the README and changelog, and parse committed result filenames.
   On MC Dropout, every one of these sources names the cause.
3. **Search magnitudes on a log scale** (×0.02 … ×50), guided by the gap's direction, instead of ×/÷ 2, 5, 10.
4. **Use the LLM for ordering, never for pruning; rank by cheap measured effects.** This matches our own finding
   that random order and evidence-off found more causes.
5. **Find interactions explicitly:** group screening, then a small foldover or pairwise design, then ddmin to a
   1-minimal set. Add a label for "explains the target but conflicts with held-out" instead of a silent Unexplained.

Calibration: this is a frontier problem. On PaperBench, agents score **about 0–1.4% on result matching** (§3).
No benchmark measures "which hidden condition explains the gap", so GapBench-style evaluation looks novel.

---

## 2. Diagnosis: why GapFinder missed (mapped to the evidence)

| Failure observed | Root cause | What the literature says |
|---|---|---|
| The ledger read "we used 10x more iterations" as *more* training than the default (500) | relative wording resolved by guessing, with no reference and no arithmetic | No published method handles relative values as such (angle 1 found none; under-studied). LLM *relation* extraction for hyperparameters is very weak: HyperPIE LLM RE F1 ≤ 7.8 (fine-tuned RE about 39) |
| The random arm's grid (×/÷ 2, 5, 10 around 500) couldn't reach 10 | candidate generator not magnitude-aware | Training-budget and hyperparameter omissions are the most-cited failure cause; true values are often orders of magnitude off |
| The full pipeline found *fewer* causes than random order or evidence-off on the blind tasks | LLM priors and the evidence gate prune candidates | Execution feedback beats self-critique: in PaperRepro, removing execution-feedback refinement was the most damaging ablation; SUPER's reflection added only +3.8 points (unverified magnitudes) |
| Interaction tasks were never solved (0/12) | one-at-a-time screening can't see "each alone ≈ 0, together large" | OAT designs can't detect interactions by construction; foldover and pairwise designs can |
| MC Dropout's true cause fixes Energy but breaks Yacht, labelled Unexplained with no explanation | binary held-out rule; code-level causes out of scope | Tuning contamination and leakage are a major real-world cause class (Kapoor & Narayanan: 294 papers, 17 fields) and need an explicit out-of-scope report |
| RusKey: nothing found; the load itself wasn't reproducible | baseline not reproducible before blaming conditions | Run a "can the baseline be reproduced?" precheck first; systems artifact evaluation lists data and scale as recurring problems |

---

## 3. How hard the problem is (verified calibration)

- **PaperBench** (replicate 20 ICML papers from scratch): best BasicAgent **21.0%** (Claude 3.5 Sonnet); o1 with
  IterativeAgent 24.4%; ML PhDs 41.4% on a 3-paper subset. **Result Match: 0.0-1.4% for agents.** Matching
  reported numbers is the hardest part.
- **SUPER** (set up and execute research repos): best end-to-end **16.3%** (SWE-Agent + GPT-4o, expert set).
- **SciCoQA** (detect paper-vs-code discrepancies): best models **46.7%**. It *excludes* hyperparameter mismatches
  that the code supports via config or CLI, which is exactly GapFinder's niche.
- **Reproducibility base rates:** Raff 2019, 162/255 (63.5%) independently reproduced, and code release wasn't
  significantly associated; Collberg & Proebsting, 32.3% of 402 systems papers built within 30 min; ReScience,
  unreproducible studies missed hyperparameter details 19.9% more often (relative wording in the paper).
- **Implication:** GapFinder's 0/48 confidently wrong is strong against this backdrop. Its recall ceiling is
  set mainly by hypothesis generation, the part everyone finds hardest.

---

## 4. Recommended plan (prioritized)

### Tier 1: quick, high impact (each ≤ 1 day)
| # | Change | Where in GapFinder | Fixes | Evidence |
|---|---|---|---|---|
| 1 | **Typed setting records:** value + relation (absolute / multiplier_of / fraction_of / delta / qualitative) + reference + verbatim quote; YAML output, 5 few-shot examples including relative cases, strict schema | `ledger/assumptions.py` prompt and schema | the misread direction | HyperPIE: YAML beat JSON for entity recognition by ~5.5 F1; few-shot helps (older models) |
| 2 | **Deterministic resolver:** LLM emits `knob.base * 10`-style expressions; code substitutes defaults and per-dataset bases from the repo; direction is computed | new resolver after the ledger | the misread direction | PAL: +15% absolute over chain-of-thought on GSM8K by offloading arithmetic |
| 3 | **Branch on ambiguity:** if a relative claim has 2 readings, emit both candidate values (e.g. `epochx` 10 *and* >500); experiments decide | candidate generation | reaching 10 | follows from the architecture; single-reading extraction is unreliable (SciCoQA 46.7%) |
| 4 | **Numeric direction check:** "with value V, is the effective quantity above or below default, and what does the paper say?" Disagreement means ambiguous, so branch | after the resolver | catches sign errors before any run | indirect (SciReplicate-Bench: models understand concepts but implement poorly) |
| 5 | **AST knob inventory first:** argparse (name, default, type, help), constants, configs, each with file:line; the LLM must map every setting to a knob ID or mark it "unmapped" | `ingest/repo_map.py` (already partly there) | hallucinated knobs, recall | SUPER: top failures were skipping repo exploration and hallucinating arguments |
| 6 | **Log-ladder candidates** (×0.02, 0.1, 0.5, 2, 10, 50) with a direction hint from the gap sign; a 3-point log-linear fit to interpolate toward the target | `search/hypotheses.py`, candidate generator | 50× changes | multiplicative ranges are modelled in log space (BO practice); budget omissions are top-cited |
| 7 | **New labels:** "explains target, conflicts with held-out (by X SD)" and "probable code-level cause (out of scope)" with a reason | verify round, report | the silent Unexplained on MC Dropout | design from principles; leakage and contamination are a common real cause class |
| 8 | **Noise floor first:** seeds and splits as a control, never as a cause; a "baseline reproducible?" precheck | calibration | RusKey-style failures | seed and implementation variance can reach several % (Pham et al.) |

### Tier 2: bigger changes (1-3 days each)
| # | Change | Fixes | Notes and risks |
|---|---|---|---|
| 9 | **Paper-era commit diff:** choose the commit nearest the paper date (or one linked in the README), extract argparse, config **and literals** at training call sites by AST, align old→new; every changed value becomes a high-prior hypothesis with the old value as a candidate | would have produced `epochx=10`, `hidden=1` on MC Dropout | **verified on the repo:** `a6259f1` (2016) has no argparse, `n_epochs*10` (base from n_epochs.txt) and one layer; HEAD `--epochx 500 --hidden 2`; the README links `a6259f1` as the paper's code. Alignment is noisy under refactors |
| 10 | **README / changelog / results-filename mining** (e.g. `*_100_xepochs_1_hidden_layers.txt`), tagged by provenance | strong hypotheses cheaply | **a leak in blind evaluations:** log provenance and report with and without these sources |
| 11 | **Measured screen instead of evidence-gate pruning:** cheap probes rank knobs by effect; the gate only labels (Explained vs Fits but unsupported) | the recall loss found in the blind test | consistent with our ablation |
| 12 | **Interaction search:** group screening (move all paper-direction values, then bisect), then a 12-run foldover Plackett-Burman or 2×2 factorial on flagged pairs, then ddmin to a 1-minimal set | 0/12 interaction tasks | PB foldover is resolution IV; costs 40-60% of a 40-run budget, so use it when the single-knob screen finds nothing |
| 13 | **Multiple-comparison control:** Benjamini-Hochberg for shortlists, Holm for the final claim; sequential (SPRT-style) repeats | protects 0-false-attribution as tests grow | standard statistics |

### Tier 3: research-level (later)
- Priors from **sibling repos and cited baselines** (PaperRepro-style lineage; claimed big gains, unverified).
- **Issue/PR mining** with a date filter (ReproRepo: an agent surfaced a related human blocker for ~90% of 1,149 papers; abstract only).
- **Dataflow tracing** of indirect knobs (effective quantity = flag × base).
- **Level-set GP** to report the value *range* consistent with the claim.
- Environment default-change tables (library default changes silently alter results).

---

## 5. What the plan would have done on MC Dropout (walkthrough)
1. The AST inventory finds `--epochx` (default 500, help "Multiplier for the number of epochs") and `--hidden` (default 2); dataflow shows epochs = n_epochs.txt (40) × epochx.
2. The ledger records "we used 10x more iterations" as `multiplier_of(10, reference = base epochs)`. The resolver computes `epochx = 10`; the direction check flags that 10 < 500 contradicts a "more than default" reading, so it **branches** with both 10 and >500.
3. Tier 2 history diff: `a6259f1` → `n_epochs*10`, `[n_hidden]` (1 layer) gives the high-prior pair (10, 1). The README sentence "10x epochs one layer" confirms it (provenance-tagged).
4. Search: `epochx=10` alone moves Energy by about 4 noise units; the interaction stage tests the pair → Energy 1.72 (paper 1.66). It's a 2-knob interaction, which the Tier 2 interaction search targets.
5. Verify: held-out Yacht +79-170%, so the **new label** reads "explains Energy; conflicts with held-out Yacht; probable code-level cause: shared-hyperparameter tuning (README 2018 update)". That's a correct, informative answer instead of a silent Unexplained.

---

## 6. How to prove the improvement honestly
- Any change makes a **new version (v1.1)**. The existing blind results can't be re-scored; show v1.1 on MC Dropout
  only as **post-hoc**.
- Credible evidence needs **new blind tasks:** run the sealed generator with a fresh seed after tagging v1.1
  (generator categories should add *order-of-magnitude* and *relative-wording* knobs), plus the AI-author tasks.
- **Ablate the provenance sources** (README, history, issues) on every evaluation, so judges can see how much comes
  from experiments versus reading documentation.
- **Check for false attributions every time.** The project's core claim is 0 confidently wrong.

### Within the hackathon (by 30 Oct), realistic scope for a teammate
- **Do:** Tier 1 items 1-3, 6 and 7 (about 2-3 days), then a post-hoc v1.1 MC Dropout demo, plus *optionally* a fresh
  blind generator run (about $2-4 with a shared ledger; about $7.50 as currently designed).
- **Skip until after:** Tier 2 items 9 and 12 (alignment and interaction designs need careful testing), and Tier 3.
- **Narrative:** "v1.0 is honest but conservative; v1.1 shows how typed, computed paper values and repo history
  close the MC Dropout miss" (post-hoc, clearly labelled).

---

## 7. Verification of key claims (adversarial pass)
| Claim | Verdict | Correct figure / note |
|---|---|---|
| PaperBench 21.0% best BasicAgent; o1 IterativeAgent 24.4%; PhDs 41.4% (3-paper subset); Result Match ~0% | CONFIRMED | Result Match 0.0-1.4% for agents |
| SUPER 16.3% end-to-end (expert) | CONFIRMED | |
| Raff 162/255 = 63.5%; code release not significant | CONFIRMED | reproduced *without* the authors' code |
| ReScience: missing hyperparameters 19.9 more often | PARTLY | the paper says "19.91% more often" (not "percentage points") |
| HyperPIE: ER F1 79; LLM RE 34-44; YAML > JSON | PARTLY / **REFUTED in part** | fine-tuned RE ≈ 38.8; **LLM RE ≤ 7.8**; YAML > JSON for entities only |
| PAL +15% absolute on GSM8K | CONFIRMED | ICML version (v1 said 8%) |
| SciCoQA ~46%; excludes configurable hyperparameter mismatches | PARTLY | **46.7%**; exclusion applies when the code supports the paper's settings |
| Kapoor & Narayanan 294 papers, 17 fields | CONFIRMED | Patterns 2023 version (preprint said 329) |
| MC Dropout repo facts (a6259f1 vs HEAD, README) | CONFIRMED, minor nits | experiment.py files are per dataset under `<dataset>/net/`; base epochs come from a data file |
| Collberg & Proebsting 32.3% of 402 built ≤ 30 min | CONFIRMED | from the technical report behind the CACM article |

Not verified (treat as indicative): PaperRepro and RePro magnitudes, Curie 3.4×, ReproRepo method details,
Unicorn numbers, SA-Bench appendix-detail figures, ESEM 2026 AST study numbers, DoVer's 18-28% recovery.

---

## 8. Sources
- PaperBench: https://arxiv.org/abs/2504.01848 · SUPER: https://arxiv.org/abs/2409.07440 · CORE-Bench: https://hal.cs.princeton.edu/corebench_hard
- REPRO-Bench: https://arxiv.org/abs/2507.18901 · EXP-Bench: https://arxiv.org/pdf/2505.24785v2 · ResearchCodeBench: https://arxiv.org/pdf/2506.02314 · MLAgentBench: https://arxiv.org/pdf/2310.03302
- PaperRepro: https://arxiv.org/html/2603.01801 · AutoReproduce: https://arxiv.org/abs/2505.20662 · RePro: https://arxiv.org/pdf/2512.02812 · ReproRepo: https://arxiv.org/abs/2606.18237
- HyperPIE: https://arxiv.org/html/2312.10638v1 · PAL: https://proceedings.mlr.press/v202/gao23f · SciCoQA: https://arxiv.org/abs/2601.12910 · SciReplicate-Bench: https://arxiv.org/html/2504.00255v2 · SA-Bench: https://arxiv.org/pdf/2608.24252
- Raff 2019: https://arxiv.org/pdf/1909.06674 · Gundersen & Kjensmo: https://ojs.aaai.org/index.php/AAAI/article/view/11503 · Fostiropoulos et al.: https://arxiv.org/abs/2305.12571 · Dacrema et al.: https://arxiv.org/abs/1907.06902
- Henderson et al. (deep RL that matters): https://arxiv.org/pdf/1709.06560 · Melis et al.: https://arxiv.org/pdf/1707.05589 · Musgrave et al.: https://arxiv.org/pdf/2003.08505 · Kapoor & Narayanan: https://pmc.ncbi.nlm.nih.gov/articles/PMC10499856
- Pham et al. (variance): https://www.cs.purdue.edu/homes/lintan/publications/variance-ase20.pdf · Bouthillier et al.: https://arxiv.org/pdf/2103.03098 · Collberg & Proebsting TR: http://reproducibility.cs.arizona.edu/v2/RepeatabilityTR.pdf
- Sequential bifurcation (Bettonvil & Kleijnen): https://research.wur.nl/en/publications/screening-for-the-important-factors-in-large-discrete-event-simul/ · Group testing: https://arxiv.org/pdf/1902.06002 · PB foldover: https://statease.com/publications/stat-teaser-newsletter/statteaser-0915
- Hyperband: https://arxiv.org/pdf/1603.06560 · BOHB: https://arxiv.org/pdf/1807.01774 · Delta debugging: https://www.st.cs.uni-saarland.de/publications/files/hildebrandt-issta-2000.pdf · Unicorn: https://arxiv.org/abs/2201.08413 · Siegmund et al.: https://www.se.cs.uni-saarland.de/publications/docs/SGA+15.pdf
- MC Dropout repo: https://github.com/yaringal/DropoutUncertaintyExps (README "Update (2018)", commit a6259f1)
- Default-argument breaking changes: https://pure.etsmtl.ca/en/publications/unboxing-default-argument-breaking-changes-in-1-2-data-science-li
