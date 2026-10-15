# TODO: make GapFinder trustworthy (handover)

This file is written for whoever picks up the work next. Read section 0 before touching anything.
Every item says why it matters, exactly what to do, which files change, what it costs, and when
it counts as done.

**Goal:** show that GapFinder finds real causes on problems it didn't create. It must also say
"Unexplained" or "Inconclusive" when it should, and beat an ordinary agent given the same tools.
**The evidence is the product.** Add no new agents, dashboards or model tiers until every P0
item is done.

**Owners:** S = Sayjad (project lead, the RusKey reproduction author); D = the developer doing
this handover. **No team member writes hidden tasks or answer keys.** They come from two
sources outside the team: a **sealed random task generator** and an **independent AI task
author** (see "Who writes hidden tasks" below).

---

## NEXT STEPS (updated 2026-10-13, after D's handover session; read this first)

**Update 2026-10-14 (after v1.1).** GapFinder v1.1 is tagged, and its sealed blind test is scored:
- 0/30 confidently wrong;
- 7 correct + 1 partial of 15 cause runs;
- the true configuration was measured in 12 of 15 cause runs.

Hypothesis coverage is largely solved, and phase 3 (selection) is done and measured. **Next: section B4
(phase 4)**; the bottlenecks are in docs/CONTEXT_v11.md §0.6. Earlier: section B3 and [docs/CONTEXT_v11.md](docs/CONTEXT_v11.md). Billed spend: $21.04.
The text below this update is the 2026-10-13 state.

**Where things stand.** Engineering and evaluation are done and pushed; GapFinder is frozen as tag
`v1.0`. Done in D's session (details lower down, and in the files linked):
- GapBench blind test **run twice** (run 2 on `v1.0`): GapFinder **0 of 48 runs confidently wrong**,
  18/18 correct abstentions, 4/8 then 6/8 tasks solved; the baseline was confidently wrong in 26/48.
  The random-order and evidence-off arms found as many or more causes
  ([gapbench_test_v1.json](eval/results/gapbench_test_v1.json), [gapbench_test_v2.json](eval/results/gapbench_test_v2.json)).
- MC Dropout external case: all 4 arms **Unexplained**, no false attribution. The documented cause
  (`epochx=10 hidden=1`) reproduces Energy in our runs but breaks held-out Yacht; the post-hoc run shows
  the verification rejects it, so the blind miss was hypothesis coverage
  ([RESULT.md](eval/external/mc-dropout/RESULT.md)).
- spec-draft live check passed on mlbench and rlbench ([spec_draft_live.md](eval/results/spec_draft_live.md)).
- Submission drafts: [DEVPOST.md](docs/DEVPOST.md), [VIDEO_SCRIPT.md](docs/VIDEO_SCRIPT.md),
  [FEEDBACK_SUBMISSION.md](docs/FEEDBACK_SUBMISSION.md); team steps in [TEAM_HANDOFF.md](TEAM_HANDOFF.md);
  research on improving recall in [RESEARCH_real_causes.md](docs/RESEARCH_real_causes.md).
- Billed: **$17.18** (cap in D's `.env`: $20). Sandboxes: diagnostic `cost` only, not billed in the Beta.

D is offline from 2026-10-14. Everything below is for S and the team.

### A. Must do for the submission (deadline 2026-10-30; aim for 27-28 Oct)
1. [ ] **S: make the repo public and enable Pages.** Settings → General → visibility; Settings → Pages →
   Source: GitHub Actions; run the `pages` workflow; open https://sayjad21.github.io/GapFinder/ logged out.
   Before going public: approve or remove the personal email in this file's "Git and honesty rules" and
   check commit author emails are acceptable.
2. [ ] **Team: record the video** from [docs/VIDEO_SCRIPT.md](docs/VIDEO_SCRIPT.md) (under 3 min,
   1920×1080, model names on screen, "16×" on sped-up replay). Upload to YouTube as public.
3. [ ] **Team: submit on Devpost.** Paste [docs/DEVPOST.md](docs/DEVPOST.md), fill the two remaining
   `[[V1.0: TODO ...]]` placeholders (the YouTube URL, and the AI-author bullet: fill it or delete it),
   add the repo and site links.
4. [ ] **Team: paste [docs/FEEDBACK_SUBMISSION.md](docs/FEEDBACK_SUBMISSION.md)** into the feedback form.
5. [ ] **Anyone: fresh-machine check.** Clone, follow SETUP.md, run `python scripts/try_it.py`, time it,
   and fix the README if the time or steps differ.

### B. Roadmap: fix hypothesis coverage now, then turn "Unexplained" into diagnoses (updated 2026-10-14)

**Why this order.** The run logs settle where capability is lost. In **14 of v1.0's 18 blind-test
misses, a true value was never tested at all** (e.g. `normalize=minmax`, `n=600`, MC Dropout's
`epochx=10`). In the other 4, the true value was tested but another value that fit about as well was
picked. Verification is not the bottleneck: 0 of 48 runs were confidently wrong. So phase 1 makes the
true value *reachable* and the answer *set-valued*, and phase 2 makes "Unexplained" informative. The
plan follows `unexplained_solution_proposal.md` (local file; methods M1-M5), adjusted to these findings.

**Money.** Search runs are free on the local backend, and the reported Sandboxes `cost` is unbilled in
the Beta, so run counts aren't the constraint (the proposal's "40-run envelope" is outdated). Only
model calls cost money, mostly the ledger stage. About $32.8 of credit is left, but billed spend
($17.18) is above the local cap (`GF_SPEND_CAP_USD=11`): **S must set a new cap before any paid item**,
marked $ below.

**Honesty rules for everything below.**
- The 8 former test tasks are now dev data, since their answers are public.
- Results on them, or on MC Dropout, are post-hoc and must be labelled so.
- A claim about v1.1 or v1.2 needs a **new sealed blind test** (new seed after the version tag).
- The always-"Unexplained" row is reported next to every scoreboard.

#### Phase 1: hypothesis coverage (now)

Done in v1.1 (commits `c7fb9a0`, `c5b1a93`, `1460855`; results in
[gapbench_v11_posthoc.md](eval/results/gapbench_v11_posthoc.md)):
- every argparse `choices` value is tried; a coarse-first log ladder for numbers, kept below 1 for
  fractions; 6 values per knob;
- the combine round pairs two values per knob;
- strict confirmation: fresh runs only, Bonferroni-corrected bootstrap;
- parsimony tie-break;
- `harness.py --ledger-from` for free like-for-like comparisons.
- Post-hoc on the 8 former test tasks: correct causes 7 → 8 plus 1 partial (interaction 0 → 2 plus 1
  partial, decoy 2 → 3, known cause 5 → 3), still 0 confidently wrong and 9/9 abstentions; dev 3/4.

Remaining, in order:
1. [x] **Done** (`eval/reachability.py`: v1.1 reaches every true value on the former test tasks). **Reachability metric and log re-analysis script** (free; proposal Part D, day 1).
   `eval/reachability.py`: for every run with a known answer, record:
   - whether each true value was in the candidate set;
   - its rank there;
   - whether the true combination was ever run;
   - the final label.

   Report the reachability rate per category, for v1.0 and v1.1. This turns "the grid couldn't reach
   it" into a number and shows what each later fix buys.
2. [x] **Done** (literal factors for multipliers, boundaries 1 and 0.0). **Multiplier, mode and boundary candidates from plain code** (free; M1 step 3-4).
   - In `search/hypotheses.py`, knobs whose name or help text marks a multiplier (`*x`, `*_mult`,
     `*_scale`, `*_factor`, help text "multiplier") get the literal factors {1, 2, 5, 10, 100};
     `epochx=10` then becomes deterministic.
   - Knobs named mode, tuner, policy or algo, enums and `choices` get all their levels (choices are
     done).
   - Integer knobs get the boundary values 0 or 1 where valid.
   - Target the RusKey tuner-mode flags behind setting recall 0.67: check, from the RusKey logs and
     `papers/ruskey/gold_assumptions.json`, whether the repo map or the model missed them.
3. [x] **Done** (`gapfinder/ingest/config_flow.py`: epochx scales n_epochs). **Static config flow (Python `ast`)** (free; M1 step 3 and proposal idea #3, reduced).
   - Mark a knob as multiplicative when it multiplies a loop bound or size (e.g.
     `int(n_epochs * epochs_multiplier)`), and record what it scales (`epochs = n_epochs.txt × epochx`).
   - The resolver in item 4 needs this to turn "10× PBP's 40 epochs" into `epochx = 10`.
   - Tree-sitter only if a C++ repo needs it (RusKey's gflags are already parsed).
4. [ ] **$ Anchor-aware quantity tuples, plus a deterministic resolver** (M1 steps 1-2; about $0.5-1.5 to
   validate).
   - The assumption step emits `{quantity, value | (anchor, operator, factor), direction, unit, table,
     quote}` (pydantic schema, validators, one re-ask with the validation error, and an output-token
     check against truncated JSON).
   - Code resolves the anchor against the ledger and repo defaults, and branches into every reading
     when ambiguous.
   - Record which table a claim comes from: MC Dropout's Table 1 already uses 10× epochs, and Table 2
     is a further 10×.
   - Validate by re-running only the ledger stage on MC Dropout (both ledgers, about $0.3) and RusKey
     (setting recall against the gold set). Post-hoc; report reachability and rank.
5. [ ] **$ Code-to-paper reverse pass** (Dude, arXiv 2609.03416). For every knob in the repo map, ask
   what the paper says about it: a stated value, a relative statement, or nothing. This targets setting
   recall directly; measure it on RusKey and MC Dropout.
6. [x] **Done** (value_sets, scorer `correct_set`). **Set-valued answers for equally good fits** (free; the bridge to phase 2).
   - Report every value of a knob, and every configuration, whose gaps stay within the noise band, as
     a range or "island", plus the parsimony pick.
   - Pre-register a v1.1 scoring rule: a set counts as correct if it contains the truth and excludes
     the default. Report it next to the exact-match score, never instead of it.
   - On the former test tasks this would turn gen-03 (`max_steps` 400 / 500 / 1000 all fit) into a
     correct range.
7. [ ] **Interaction screening as an addition, not a replacement** (free to build; M2).
   - Run a 16-run resolution-IV 2^(7-3) design (generators E=ABC, F=BCD, G=ACD) over the top 7 knobs,
     **in addition to** the multi-value screen.
   - Fit a weak-heredity sparse pairwise model (main effects plus pairs, at most about 6 terms per
     claim). Enumerate the 128 corners, and break aliases with 2-4 targeted runs.
   - Keep the multi-value screen: two levels per knob would bring value misses back, the main failure
     mode.
   - Validate first with the proposal's synthetic power study (the logged MC Dropout effect sizes plus
     the measured noise) against the current screen, at $0.
8. [x] **Done** (`harness.py --ledger-from`, `eval/gapbench/run_arms.py`: the `gapfinder` arm pays for the ledger once, the other GapFinder arms re-use its recorded answers). **$ Shared ledger across arms** (cost). The four GapFinder arms recompute the same claim
   extraction. Sharing one ledger per task takes a blind test from about $7.50 to about $2-3.
9a. [x] **Done** (rivals checked over GapFinder's whole search space). **Generator validity: reject tasks a simpler configuration explains** (free; found 2026-10-14).
    - On test-gen-05 (interaction: `eps_start=0.1` + `lr_schedule=inv`), the single change
      `eps_start=0.0` reproduces both claims (C1 +5.1%, C2 +0.8%) better than the planted pair does (C1
      +36%). So the planted answer isn't identifiable from the claims, and GapFinder's simpler answer is
      a valid explanation that the scorer marks wrong.
    - In `eval/gapbench/gen_tasks.py`, add a check: measure every single-knob candidate (or at least
      each planted knob's other candidate values) and reject a draw if any configuration simpler than
      the planted one lands within the noise band on every claim.
    - Re-check test-gen-06 run 15 (`n=5000` chosen instead of 600) the same way.
9. [x] **Done** (`eval/results/gapbench_test_v11.md`: GapFinder 0/30 confidently wrong, 7+1 of 15 causes, 15/15 abstentions, balanced 0.73 vs 0.50 trivial; the true configuration was tested in 12/15 cause runs; out-of-space tasks turned out pair-mimicable, so the generator's rival check needs pairs). **$ Fresh sealed blind test on v1.1** (tag `v1.1` first; new seed after the tag).
   - Add generator task types for order-of-magnitude changes, relative wording ("10× the baseline"),
     multiplier knobs and pure interactions.
   - Report the confidently-wrong count first, the always-Unexplained row, and exact binomial
     intervals.

#### Phase 2: turn "Unexplained" into answers (the real target)

10. [x] **Done** (`gapfinder/search/history.py` plus the label "Explains target, conflicts with held-out"; MC Dropout re-labelled accordingly; offline validation 11/12 on GapBench). **Multi-claim history matching** (M3; free to build, validated on logged runs).
    - Per claim and configuration, compute implausibility I = |paper − measured| / √(V_obs + V_noise +
      V_emul + V_disc). V_obs comes from the paper's reported spread, V_noise from fresh-load or
      fresh-setup variance, V_disc from a pre-registered discrepancy term for scaled surrogates.
    - Define NROY = max_i I_i ≤ 3 (the second-largest I when there are 5 or more claims).
    - Labels:

| Situation | Label |
|---|---|
| a verified configuration inside the joint NROY | Explained or Partially explained, with every NROY island listed |
| each claim fits alone, but no configuration fits them jointly | **"Out-of-space suspected: claims mutually inconsistent under every exposed condition"** |
| no claim fits | **"Out-of-space likely"** |

    - The second label is exactly MC Dropout: Energy fits, Energy plus Yacht doesn't, and the
      authors' README admits test-set contamination.
    - Calibrate V_disc on toy Explained or Reproduced cases, and report sensitivity under 2-3 settings.
    - Re-analyse MC Dropout, RusKey and GapBench logs first (no new runs).
11. [~] **Free static part done** (`gapfinder/ingest/code_checks.py`; leads attached when history matching says out of space; on MC Dropout all 3 documented out-of-flag differences are among 8 leads, `eval/results/code_checks_mcdropout.md`). Still to do: the paid Super ranking, and a way to *test* a lead (a patch knob). **$ Out-of-space checklist triage** (M3 step 4). When the label is "Out-of-space suspected/likely",
    Super checks a fixed list: train/test leakage, hyperparameters shared across splits, eval
    padding/EOS, loss-direction defaults, dataset version, metric definition. Each item is backed by a
    repo grep (code evidence, no runs). Report the top cause family.
12. [x] **Done** (`eval/noise_model.py`; engine rule `mde_inconclusive`: an Unexplained gap below the MDE at the confirmation repeats reads Inconclusive. Score-neutral: both are abstentions; on the recorded runs it re-labels 13 of 70 Unexplained claims, all gaps of 8-10%. Metamorphic relations not done). **Honest noise model** (M4; free).
    - Variance components from fresh loads × forks (one-way ANOVA; the RusKey logs already have many
      loads), and a pooled SD instead of 2×MAD-of-3.
    - A minimum detectable effect per claim: gap below the MDE becomes Inconclusive, which extends
      today's `reproduce_tol` rule.
    - Two or three metamorphic relations: MC error shrinks about as 1/√T; direction relations stated
      by the paper; ratio oracles only when the two sides' noise is correlated.
13. [x] **Done** (2 `out_of_space` tasks per set, bugs from patched copies in `eval/gapbench/variants.py`: mlbench `drop_scaled` and `clip5`, two different bugs per set; balanced scores and the always-Unexplained row in `score.py`; dry run with a throwaway seed passes). Risk to watch: a knob that closes most of such a gap (here `normalize=zscore`) can give "Partially explained", which scores as confidently wrong. **GapBench out-of-space category, plus balanced scoring** (free to build).
    - Tasks whose planted cause is not reachable through any knob: shared-split tuning (the MC Dropout
      mechanism), an eval padding bug, a loss-direction default, train/test overlap, a metric on the
      wrong split.
    - Report in-space recall, out-of-space specificity, their mean (balanced diagnostic accuracy; the
      abstainer is capped at 0.5), cause-family accuracy and the false-explanation rate.
14. [~] **Equifinality map and NROY islands done** (Gap Report "History matching" section; `history.islands`). Knob → claim graph not done. **Reporting views at zero extra runs** (proposal Part A, reduced):
    - an equifinality map (NROY configurations grouped by which knobs changed);
    - NROY "islands" as connected components under single-knob moves (a BFS);
    - a code-derived knob → claim graph, to predict which held-out claims a knob should not move.
15. [ ] **Evidence as a prior, and confirmation by racing** (M5; low priority). Our logs show the evidence
    gate was not the main cause of misses, so do this only if item 1's re-analysis says otherwise.
16. [x] **Done, partly right** (`eval/external/mc-dropout/RESULT_v11.md`: out-of-space suspected and the documented code leads; the label names `epochx=1, hidden=10`, an equally good Energy fit; the documented pair was measured once before the 150-run budget ran out; three engine fixes came out of it). **$ Post-hoc MC Dropout rerun on the new version.** Expected: "Partially explained (Energy) +
    Out-of-space suspected", with shared-split tuning as the top checklist item. Label it not blind.
17. [ ] **RusKey positive control** (this file, P0-1 "Positive control on RusKey"). It costs $0 billed but
    needs the sandbox guard raised and S's OK. It answers "can GapFinder find a real cause in a real
    system?"
18. [ ] **Independent AI-author tasks** (a coding agent from a different vendor than the one that built
    GapFinder; two-phase seal/reveal; commands in TEAM_HANDOFF.md step e). About $3; needs the cap
    raised.

**Not doing**, from theory.md, with the reasons in the proposal's Part A:
- **Rejected:** flux balance analysis, SMT over the training loop, latent diffusion over configurations,
  persistent homology beyond a BFS, quantum annealing.
- **Only in reduced form, as above:** MAP-Elites (as the equifinality map), the Ising model (as the
  pairwise surrogate in item 7), do-calculus (as the code graph in item 14), MDL (as the parsimony
  tie-break, done).

**Order if time is short:**
1. Items 1-3, 6 and 10: free, and they give the "found it / here is the range / this is out of space"
   story.
2. Then 4, 8 and 9, which are paid.
3. Then 13 and 16.

### B3. Phase 3: choose among equally good fits (the current bottleneck; written 2026-10-14)

**Why.**
- The sealed v1.1 test ([gapbench_test_v11.md](eval/results/gapbench_test_v11.md)) measured the exact
  true configuration in 12 of 15 cause runs, but scored 7 correct and 1 partial.
- The misses are now about what GapFinder picks and reports, not what it reaches. MC Dropout v1.1 is
  the same story ([RESULT_v11.md](eval/external/mc-dropout/RESULT_v11.md)).
- The full context is in [docs/CONTEXT_v11.md](docs/CONTEXT_v11.md).
- This plan uses the local PDF "Cross-Domain Equifinality Methodologies", checked against the recorded
  runs. What it gets right, wrong, or only half right is at the end of this section.

**What the recorded runs show for each miss** (checked against the run logs, not taken from the
proposal):

| Miss | What actually happened | Kind |
|---|---|---|
| test-v11-04 run 2: `lr=0.91` | 0.91 is a fraction-ladder value. Any default in (0, 1) gets complement steps, `1-(1-d)/k`, so lr 0.1 yields 0.91, 0.82 and 0.982: meaningless for a learning rate | **coverage bug** (bad candidate values), then a noise win |
| test-v11-05 runs 1-3: no `epochs=75` | the ladder for 15 is 2, 150, 1, 8, 30, 750, 3, **75**, …; after the ledger's 10 and 20, the 6-value cap cuts it | coverage cap |
| test-v11-10 run 2: extra `lr_schedule=linear` | `max_steps=100` alone gives 98.2-99.8 (plus one 88.4); with linear, 96.2-99.0 (paper 94.9). A 0.7-point tie fell in a different rounded "noise bucket", so the pair won | minimisation tie-break |
| test-v11-01 runs 1-2: `max_steps=2000` | paper mean 353.4, min 43.4. Truth (500 + γ 0.999): mean 322-400, min 49-136. `max_steps=2000`: mean 352-393, min 45-72, but SD 44-147 against a naive 4-20 | **not identifiable** from these two claims; also, `closes()` uses the candidate's own spread, so a noisier configuration gets a wider acceptance band |
| MC Dropout v1.1 | 5 configurations fit Energy. The documented pair broke Yacht least (worst I 5.78) but had 1 run; the label went to the first one repeated | ranking by single noisy runs; budget spent on 29 one-run pairs |

**Progress (2026-10-15).** Every check below is post-hoc on the 22 public dev tasks, with
`eval/dev_suite.py` (recorded ledgers, $0). One suite run is 66 searches; two replicates of the same
code differ by about ±2 correct runs.

| Code | Correct causes (of 39 cause runs), two replicates | Confidently wrong | Abstentions (of 27) | Search runs |
|---|---|---|---|---|
| v1.1 (tag) | 23, 25 | 0 | 27, 27 | ~6,100 |
| + items 2, 3, 4, 6 (`efb2f63`) | 29, 27 | 0 | 27, 27 | ~7,200 |
| + racing, item 5 (`6dc3dea`) | 29, 25 | 0 | 27, 27 | ~6,900 |
| tried and reverted: pairing values by "movement either way" | 21 | 0 | 27 | n/a |

- **Done:**
  - item 2: fraction steps only for fraction-like knobs; ladder (10, 2, 5, 50, 100); cap 6-10 from
    the budget;
  - item 3: a "consistent with the paper" tier, and likelihood ties instead of rounded buckets;
  - item 4: `ClaimResult.equivalent`, shown in the report and scored as `correct_in_set`;
  - item 6: an Occam margin for passenger knobs (an extra knob must buy more than one noise band);
    hedges no longer outrank evidence-backed fits; defaults are filtered in any spelling;
  - item 5: two-stage confirmation race.
- **What the fixes actually were:** the real causes found while fixing differ from the proposal's:
  - task 10's passenger won because a "Fits but unsupported" outranked a "Partially explained" even
    when it didn't close the gap;
  - TOST equivalence was the wrong test; the counterfactual's own margin is the right one.
- **Decision: no Inconclusive for large sets.** A set larger than K = 3 stays a hedge with the set
  reported, and is not turned into Inconclusive. Of 11 runs with a set larger than 3, the pick was
  right in 6 (chance is about 1 in 8), so the pick carries information.
- **Remaining misses are interactions:**
  - **test-gen-05 (0/6):** not identifiable at this noise; the truth itself measures 15-23 against a
    paper value of 17.3, and 8-9 configurations fit;
  - **test-v11-01:** also not identifiable (§4.13 of CONTEXT_v11.md);
  - **test-v11-05:** the pair `normalize=minmax + epochs=75` is often never formed, because 75 alone
    moves *away* from the paper and the combine round pairs values by their solo score. Ranking by
    movement either way fixed nothing and broke known-cause tasks, so it was reverted. The next idea
    is a forward step: pair the confirmed best single with each value of the other top knobs.
- **Item 9 (generator):** the standard-error rival test and the pair-rival test are built and unit
  tested. A dry generation with another seed failed (known_cause: 62 single-rival rejections), so
  the standard-error test may be too strict on mlbench. This is being checked before it is
  committed.

**After the v1.2 tests (2026-10-15):**
- **GapBench sealed v1.2:** 0/30 confidently wrong, 12/15 causes, balanced accuracy 0.90; all
  pre-registered criteria met ([gapbench_test_v12.md](eval/results/gapbench_test_v12.md)).
- **MC Dropout v1.2:** the search improved, but the label didn't
  ([RESULT_v12.md](eval/external/mc-dropout/RESULT_v12.md)).
- **Next (dev work, not blind):**
  - **Relabel rule:** history matching may label a repeated fit only when it is within the likelihood tie
    of the best fit; otherwise it reports the best fit as an unconfirmed lead. (`epochx=2`, I=24, was
    labelled over fits at I 6-9.)
  - **Combine confirmation order:** confirm the pairs closest to the paper first, so the closest pair
    gets its repeats before the budget runs out (the documented pair: +1.3%, 1 run).
  - **Equifinal ladder values on noisy RL** (`lr=1` on the v1.2 decoy): the remaining GapBench miss
    pattern.

**After v1.2, engine follow-ups (2026-10-15, commit `1c51bf3`).** Dev suite on 32 public tasks (now
including the v1.2 set), two replicates each, post-hoc:

| Code | Correct causes (of 54) | Interaction runs correct (of 21) | Abstentions (of 42) | Search runs |
|---|---|---|---|---|
| v1.2 tag | 42, 42 | 10, 10 | 42, 42 | ~9,900 |
| + combo order/race, one candidate order on every path, all-knobs Occam | 42, 41 (+1-2 partial) | 14, 12 | 42, 42 | ~9,500 |
| tried and reverted: keep the earlier candidate on a label tie | 37, 41 | n/a | 42 | n/a |

(`1c51bf3`'s message says "26 -> 32 of 36" for interactions; the table above has the right numbers.)
- **Root cause found:** 7 of the 15 v1.2 sealed cause runs had ended on the budget-exhausted path, which
  sorted configurations by median gap and bypassed phase 3's ordering. That is how `lr=1` won on
  test-v12-08.
- **The sealed v1.2 misses on test-v12-08 were largely invocation noise:** the v1.2 tag scores it 6/6 on
  the dev suite.

**v1.3 (2026-10-16):**
- **Sealed test** ([gapbench_test_v13.md](eval/results/gapbench_test_v13.md)):
  - 0/30 confidently wrong, 9/15 causes, balanced 0.80, out-of-space diagnosed 6/9;
  - two pre-registered criteria missed;
  - every miss is on the two interaction tasks.
- **Tried after it and reverted:** ±0.1/±0.2 steps for mid-range fractions (test-v13-01's threshold 0.4).
  The dev suite on 42 tasks gave 52 and 45 of 69, against 53 and 48 for the v1.3 tag, and no gain on
  test-v13-01 itself: `zscore + 0.3` fits as well as `minmax + 0.4`.
- **Replicate noise on this suite is now about ±5 runs.**

**Statistical power, read before claiming any engine gain (2026-10-16, `eval/compare_suites.py`).** The
paired per-task comparison (correct cause runs per task over two replicates per side, exact sign test
over the tasks that changed) gives:

| Comparison | Correct cause runs | Tasks better / worse | Sign test |
|---|---|---|---|
| v1.1 → phase 3 | 48 → 56 of 78 | 5 / 3 | p = 0.73 |
| v1.3 → fraction-ladder fix | 101 → 97 of 138 | 4 / 5 | p = 1.0 |

With 13-23 cause tasks, no engine change since v1.1 is significant at the task level. What is robust:
- 0 confidently wrong in every arm and every test;
- the real-paper (MC Dropout) results, which are qualitative.

A claim about accuracy gains needs more tasks (a larger sealed set or more dev tasks), not more
replicates of the same tasks.

**Order:** the free foundation first, then fixes checked on dev data, then one new sealed test. All
v1.0 and v1.1 tasks are dev data now. Nothing here needs paid model calls except the final sealed test
(about $4).

1. [~] **Replaced for GapBench by `eval/dev_suite.py`** (real local re-runs from recorded ledgers, $0). Still missing for MC Dropout: the recorded sandbox runs can't evaluate a new policy (it wants runs that were never made), so a policy check there needs a new sandbox run. **Replay simulator: a free test bench for selection policies** (`eval/replay_sim.py`, new).
   - **Why first:** CRN, racing and allocation change *which* runs happen, so `--resume` can't test
     them. Without this, every policy idea costs a full run.
   - **What it does:** build a per-configuration pool of recorded results, from all dev GapBench runs
     (v1.0 test, posthoc, v1.1 test: thousands of runs) and MC Dropout's 147. Simulate a search policy
     by drawing from those pools instead of running. Configurations that were never measured are "not
     available". Score with `score.py`'s rules, and count runs used.
   - **Acceptance:** replaying today's policy reproduces the recorded v1.1 outcomes closely, e.g. the
     same label in at least 80% of runs. Report how far it is from that.
   - **Limit:** it can only choose among measured configurations. A policy that wants a new
     configuration needs a real local run (free on GapBench).

2. [x] **Done** (`634d827`). **Fix candidate generation where it is plainly wrong** (`gapfinder/search/hypotheses.py`).
   - Complement steps `1-(1-d)/k` only for knobs bounded in [0, 1): names or help text with discount,
     gamma, decay, momentum, beta, dropout, prob, ratio, fraction or split. A learning rate,
     temperature or threshold gets the plain log ladder (lr 0.1 → 0.01, 1.0, 0.05, 0.2, …). Evidence:
     task 04 run 2.
   - Ladder order `(10, 2, 5, 50, 100)`, so ×10 stays first (coarse-first, the reason for the original
     order) and ×5 comes before ×50.
   - Per-knob cap `clamp(floor(B_screen / open_knobs), 6, 10)` instead of a fixed 6. Evidence: task 05.
   - **Free check:** `harness.py --ledger-from` on test-v11-04 and -05 (local). Unit tests: lr gets no
     0.91, epochs 15 gets 75 within the cap.
   - **Risk:** more values means more noise winners. That's why items 3-5 come next; don't ship this
     alone.

3. [x] **Done in revised form** (`efb2f63`: closes() unchanged for labels; ranking uses a consistency tier and likelihood ties). **Score with standard errors, not spreads; rank pessimistically** (`engine.py`: `closes`,
   `band_at`, the candidate sort).
   - Accept a candidate when its implausibility against the paper is at most 3. The variance term for
     the candidate's mean is `s_c^2/n_c`, with `s_c` = max(own SD, pooled naive SD), plus the paper's
     own uncertainty. A noisy candidate with few runs stays "not ruled out" (it goes into the set), but
     can't *win*.
   - Rank candidates by an upper bound of their implausibility (UCB), not their point estimate. This
     corrects the winner's curse of 60-100 one-run screens.
   - Evidence: task 01 (an SD-128 configuration accepted by its own wide band), MC Dropout (the first
     run's 1.657 decided the label).
   - **Free check:** the replay simulator, plus `--resume` re-labelling on the dev runs.
   - **Acceptance:** 0 confidently wrong stays 0, and none of the 4 v1.1 known-cause or decoy runs that
     were correct is lost.

4. [x] **Done** (`efb2f63`; large sets stay a hedge instead of Inconclusive, see Progress). **Answer with an equivalence set, and score it honestly** (`history.py`, `ClaimResult`,
   `gap_report.py`, `score.py`).
   - The answer is the set of configurations that can't be told apart from the best on every claim. Use
     a known-σ test with the calibrated noise, i.e. a light model-confidence set, not Hansen's
     bootstrap, which needs many replications per configuration. The set may mix knob subsets (e.g.
     `{max_steps=2000}` and `{max_steps=500, gamma=0.999}`).
   - **Selection is lexicographic:** fit the target first, then use the held-out claims only to order
     within that set.
     - The proposal's "race everything on the worst claim" would put `epochx=1, hidden=4` (worst
       I 5.04) ahead of the documented MC Dropout pair (5.78).
     - Using held-out claims for ranking has to be stated in the report, because they're no longer
       purely held out. The "must not get worse" check stays.
   - Labels: a set of size ≥ 2 is a hedge, "Fits but unsupported: one of {…}", never confident. A
     set larger than K (pre-registered, K = 3) is Inconclusive.
   - Scorer: a new `correct_in_set` (truth in the set, set size ≤ K), reported **next to** the exact
     score, never instead of it, and pre-registered before the next seed.
   - **Free check:** `--resume` on the dev runs. Task 01 runs 1-2 should return a set containing the
     true pair, and task 10 run 2 a set containing `{max_steps=100}`.

5. [x] **Done** (`6dc3dea` racing: cost only; `659f4e2` conditional forward step: interactions 11 -> 14 of 24). **Racing replaces "confirm by the first screen, then 40 one-run pairs"** (`engine.py` confirm and
   combine).
   - Successive halving, or top-two Thompson sampling, over the target-fit candidates, in batches sized
     to the available concurrency (sandbox runs are parallel, so batches beat OCBA's one-at-a-time
     allocation).
   - Pairs enter only if both their single-knob parts are not ruled out, ordered by fit, with at most
     about a third of the budget going to pairs.
   - Stop when the set is separated or the budget ends; the output is item 4's set.
   - Evidence: MC Dropout, where 29 pairs got one run each and the documented pair never got a second
     run in 150.
   - **Free check:** the replay simulator on MC Dropout's pools. Acceptance: the documented pair gets
     ≥2 runs and lands inside the reported set in most replays, within 150 runs. The replays are
     post-hoc: this case shaped the policy.

6. [x] **Done, as an Occam margin rather than TOST** (`e0f13d1`). **Minimisation by equivalence (TOST), without losing interactions** (`engine.py` bisect and the
   parsimony tie-break).
   - Drop a knob when the reduced configuration is equivalent within a margin δ (the noise band at the
     confirmation repeats) by two one-sided tests. Keep the dropped variant *in the set*, so a real
     interaction (task 01's γ, worth about +20-50 within noise) is reported, not erased.
   - Replace the rounded "noise bucket" with that test (the cause of task 10 run 2).
   - **Free check:** `--resume` on test-v11-10 run 2 (expected `{max_steps=100}` first in the set) and
     test-v11-01 (the pair still in the set).

7. [x] **Measured, not adopted** (`eval/crn_measure.py`, `eval/results/crn_measure.json`: variance reduction factor 0.25-0.97 on 7 of 8 configuration pairs, 2.1 on one; trajectories and SGD paths decorrelate under any setting change, so shared seeds buy nothing here). **Common random numbers: measure first, adopt only if it pays** (`gapfinder/sandbox/runner.py`
   `_tag`).
   - Today every run gets a random `RUN_TAG`, which seeds the GapBench artifacts and MC Dropout's
     splits. Instead, the k-th repeat of every configuration gets the same tag (derived from the search
     seed and k), so differences between configurations are paired.
   - **Measure first, free and local:** the correlation and variance-reduction factor of paired runs
     across 5-10 configuration pairs on rlbench and mlbench. Adopt only if the factor is at least about
     1.5.
   - **Caveats:**
     - CRN helps comparisons *between* configurations, not the distance to the paper's fixed number;
     - use a different seed block for confirmation than for screening (strict confirm);
     - RL trajectories decorrelate fast, so the gain may be small there;
     - real artifacts may ignore the tag (RusKey's load isn't reproducible).

8. [~] **Checked on MC Dropout** (recorded runs already hold `energy_ll` and `yacht_ll`; the paper reports LL -1.99 and -1.55). Adding them as held-out claims changes nothing: Energy LL agrees with all five Energy fits, and Yacht LL tracks Yacht RMSE. Claims from the same datasets are correlated, so only an independent dataset (Concrete) would add information, and that costs runs. **More claims = more identifiability** (ledger and harness).
   - Use every claim of the same experiment as a held-out claim. For MC Dropout that means the
     log-likelihoods and Concrete; check what `run_cell.sh` outputs.
   - Where a paper reports a spread (MC Dropout's ±0.19 over 20 splits), add it as a dispersion claim.
     This is the defensible version of the proposal's "second-moment fingerprinting".
   - Don't compare a candidate's variance to the naive variance. The paper doesn't report that, so it
     identifies nothing.
   - On generated tasks, consider a third reported number per paper (e.g. rlbench `max_reward` or a
     learning-curve point). That would change the benchmark, so pre-register it in item 9.

9. [x] **Done** (`1201f0c`: likelihood-aware single rivals, pair rivals, a fixed artifact per slot, quotas 1 out-of-space + 2 incomplete; a dry run gives 10 balanced tasks in about 1.5 h). **Generator: identifiability checked the way GapFinder can see it** (`gen_tasks.py`).
   - Rival check by implausibility with the rival's *own* standard error (I ≤ 3 on every claim), not
     "within one naive band". Task 01's `max_steps=2000` (SD up to 147) passed today's check.
   - Extend the check to the pairs the combine round can reach: the top 8 single settings by
     proximity, so 28 pairs, local runs.
   - Instead of only rejecting a draw, record the **answer set** (every configuration equivalent to the
     truth), and reject only when it has more than K members.
   - This also fixes the out-of-space category: on v1.1 every out-of-space task was mimicked by a pair,
     so `out_of_space_diagnosed` was 0/9. If no bug survives a pair check on mlbench, add a third claim
     (item 8) rather than drop the category.

10. [x] **Done** (`eval/results/gapbench_test_v12.md`: GapFinder 0/30 confidently wrong, 12/15 causes, 15/15 abstentions, balanced 0.90, out-of-space diagnosed 4/9; all four pre-registered criteria met; the sets differ from v1.1, see the file). **$ Sealed v1.2 test** (about $4; needs a cap raise; same protocol as v1.1).
    - Pre-register, before the seed:
      - set scoring (`correct_in_set`, K);
      - the generator changes (items 8-9);
      - the arms.
    - Tag `v1.2`, then make the seed, generate (`--set v12`), run with `run_arms.py`, and reveal.
    - **Success:**
      - confidently wrong 0/30 (exact upper bound ≤ 12%);
      - exact correct causes > 7/15, or the same with `correct_in_set` clearly higher;
      - balanced accuracy above v1.1's 0.73;
      - out-of-space diagnosed > 0 on tasks that are truly out of space.

**Order if time is short:** 2 and 6 (small, deterministic, free), then 3 and 4 (the core), then 1 and
5. Items 7 and 8 are optional. Then 9 and 10.

**What the PDF gets right, and what we drop or change.**
- **Kept:**
  - set answers instead of point answers: model confidence sets, made lighter (item 4);
  - racing instead of greedy confirmation: NSGS/OCBA, made batch-parallel (item 5);
  - TOST for minimisation (item 6);
  - CRN, but only after a measurement (item 7);
  - a dynamic per-knob cap (item 2);
  - pair rivals in the generator (item 9).
- **Corrected:**
  - `lr=0.91` is a bad-candidate bug, not only a noise win;
  - MC Dropout had 29 measured pairs, not 36, and 16, not 31, broke Yacht;
  - racing everything on the worst claim does *not* favour the documented pair; only lexicographic
    selection does. Nothing "guarantees" it;
  - the "Plackett-Burman sieve" is just top-k pairs.
- **Dropped:**
  - the stationary bootstrap: our runs aren't a time series, and 1-5 runs per configuration are too
    few for it. Use the calibrated σ instead;
  - Bartlett/Levene "variance vs naive" as identification: replaced by standard-error-aware acceptance
    (item 3) and reported-spread claims (item 8);
  - backward conformal e-sets: a pre-registered size cap K does the same job.
- **Added, not in the proposal:**
  - the replay simulator (item 1), without which none of the policy changes can be checked for free;
  - the warning that ranking on held-out claims spends them, so they stop being independent checks.

### B4. Phase 4: what to do about the post-v1.2 bottlenecks (written 2026-10-15)

The bottlenecks are in [docs/CONTEXT_v11.md](docs/CONTEXT_v11.md) §0.6. This plan reviews the local
file "Cross-Domain Solutions for GapFinder.md". Every factual premise was checked against the recorded
runs before deciding.

**Checks on the proposal's premises** (recorded runs, $0):

| Premise | Data | Verdict |
|---|---|---|
| Passengers are "sloppy" knobs, flat on their own 1D screen (lr=0.5 in test-v12-08, lr_schedule=linear in test-v11-10) | `lr` on test-v12-08 is one of the stiffest knobs: its ladder moves mean reward from 184 to 9-166. `lr_schedule` on test-v11-10 moves it 1.8-3 naive SDs (inv 145, linear 161, naive 184) | **False.** And a "flat alone, so penalise it" rule would delete true interaction partners: `gamma=0.999`, half of test-v11-01's truth, is exactly flat alone (184.9 vs naive 184.3) |
| A value-level ledger prior ("boost paper-mentioned values, penalise unmentioned coverage values like lr=1") breaks noisy ties toward the truth | Over 29 planted values on the dev tasks, **13 (45%) are coverage-only**, never proposed by the ledger. That includes test-v12-08's own truth, `max_steps=100`, coverage-only like the rival `lr=1` | **Harmful.** It would undo the v1.1 coverage gains and wouldn't resolve test-v12-08 |
| A KGE variance-ratio penalty: configurations whose variance far exceeds the naive one are noisy mimics | test-v11-01: the truth's own SD is 30-67 against a naive 4-20 | **False.** It would penalise the truth. The likelihood ranking already prefers the precise fit among equally close ones |
| Box-Hill discrimination: run the tied candidates under a perturbation (half n, half epochs) and see which "preserves the expected sensitivity" | There is nothing to compare the perturbed runs with: the paper reports no number at the perturbed condition | **Invalid** unless the paper reports that condition, which is then simply one more claim (item 5) |
| Trajectory signatures: a convergence ratio from logs as a third observable | Same problem: the paper must report the curve for it to discriminate | **Valid only as item 5** (paper-reported curves), or as a benchmark change (a pre-registered third number per generated paper) |

**Adopted, in order. All free to build and check on the dev suite; MC Dropout checks need sandbox runs:**

1. [x] **Built** (`3ae3c44`: hook, runner, patch round, toy end-to-end test; MC Dropout validation in the v1.3 run). **Patch knobs: test out-of-space leads without touching the files** (bottleneck 3; the proposal's
   "ephemeral AST patch knobs").
   - **How:** a static lead from `code_checks.py`, e.g. `net/net.py:70 batch_size = 128`, becomes a knob
     `@ast:net/net.py:70:batch_size`.
     - A run with that knob sets `GF_AST_PATCH=net/net.py:70:batch_size=32`.
     - A `sitecustomize.py` on `PYTHONPATH` (uploaded with the run, like `run_cell.sh`) installs a
       `sys.meta_path` loader. The loader reads the module source, swaps the literal on that line with
       `ast.NodeTransformer`, and compiles it in memory.
     - The main script is not imported through the import system, so it needs a wrapper:
       `python -m gf_patch_run experiment.py` uses `runpy` with the same hook.
     - Nothing on disk changes, so the diff guard, the repo map and the prompt caches are untouched.
   - **Rules:**
     - only when history matching says out of space;
     - only the top-weighted leads;
     - the same verification as any knob (counterfactual, held-out, likelihood ranking);
     - reported as a *code* change ("Explains with a code patch: batch_size 128 → 32"), never as a
       setting;
     - candidate values from the ladder, plus powers of two for batch- or size-like names (32 = 128/4 is
       not on today's ladder).
   - **Limits:**
     - Python-only;
     - literals only, so a grid search or a loop structure can't be patched this way;
     - MC Dropout's `T = 10000` is already patched by the harness for scale.
   - **Checks:**
     - unit tests: the hook swaps exactly one literal and leaves files byte-identical, and `test_try_it`
       still passes;
     - an integration test on a toy artifact with a hard-coded constant;
     - then an MC Dropout sandbox run (unbilled; needs S's OK): does `batch_size=32`, together with
       `epochx=10, hidden=1`, move Yacht toward the paper?
2. [x] **Done** (`cd8c8af`; dev suite 42, 41 of 54, about 6% fewer runs). **Confirmation escrow** (bottleneck 2).
   - Screening and combine may use at most about 75% of `max_runs`. The rest is held for the
     configurations most likely by the paper's numbers (target-fit set first) to reach their full
     repeats.
   - Evidence: MC Dropout v1.2, where the closest pair (+1.3%) had 1 run when the budget ended; 7 of 15
     sealed v1.2 cause runs hit the cap.
   - Check: two dev-suite replicates (cost and accuracy) and a free MC Dropout re-label of the recorded
     runs (`--resume`).
3. [x] **Done** (`cd8c8af`; no planted dev value sat behind flat coarse rungs). **Coarse-flat early stop on the ladder** (bottleneck 2; the proposal's monotone early stopping,
   adapted).
   - The ladder is coarse first (×10, ÷10). If both coarse rungs leave the metric within 0.5 noise bands,
     skip that knob's finer rungs.
   - The proposal's version (stop the extremes when the moderate rungs are flat) is the wrong way round
     for a coarse-first ladder.
   - **Risk:** non-monotone responses. Measure how many true values on the dev tasks sit behind a flat
     ×10/÷10 pair before adopting.
4. [ ] **Pooled screening of low-prior knobs** (bottleneck 2; group testing).
   - Pool about 3 low-prior knobs at one value each into one run. If the run stays within one band of
     naive, prune all three.
   - **Risks:**
     - masking (two effects cancelling);
     - pure-interaction partners pruned (gamma above is flat alone, so it would be pruned; a pool is
       only safe for knobs the combine round wouldn't pair anyway);
     - combinations that crash.
   - Adopt only if the dev suite shows fewer runs with no loss of interaction runs.
5. [ ] **More independent claims, including reported curves** (bottleneck 1; the valid part of the
   proposal's signature idea).
   - Targets beyond one target and one held-out claim: other datasets and figures, learning-curve points
     the paper plots, error bars.
   - This needs ledger support (the claim ledger already extracts claims; targets are chosen by hand).
   - For GapBench, a pre-registered third reported number per generated paper (benchmark change).

**Not adopted, with the evidence above:**
- the stiffness-weighted Occam margin;
- the value-level ledger prior;
- the KGE variance penalty;
- Box-Hill perturbation probes;
- single-split multi-fidelity screening (specific to MC Dropout, and the scaled surrogate is already
  noisy).

**Order:**
1. Items 2 and 3 first (small, free, measurable on the dev suite).
2. Then item 1 (the biggest structural gain: it turns "out of space" into a testable explanation).
3. Then item 4.
4. Item 5 when a real paper offers more claims.

A sealed v1.3 test after 1-3 (about $4; needs the cap raised).

### C. Optional / after the hackathon
10. [ ] Candidate B, Paragraph Vector on IMDB (P0-1): a second external case; 1-2 days, risky (the shuffle
    is a script line, so possibly no gap under the repo's defaults).
11. [ ] Run the search loop on GitHub Actions (6 h jobs) so long searches don't need a PC on.
12. [ ] Work through the research directions in D below, after v1.1.

### D. Research directions to make GapFinder find real causes (full list)
Source: [docs/RESEARCH_real_causes.md](docs/RESEARCH_real_causes.md) (5-angle literature review, key claims
independently verified). **Diagnosis:** the misses come from **hypothesis generation**, not verification.
Verification already rejects wrong causes (the post-hoc MC Dropout run shows this). Every change below is a
new version: evaluate it on **new blind tasks**, ablate any documentation-derived source, and check false
attributions stay at 0.

**Tier 1: quick, high impact (≤ 1 day each). Items 1-3, 6 and 7 are the v1.1 set in B6.**
- [ ] D1. **Typed setting records:** value + relation (absolute / multiplier_of / fraction_of / delta /
  qualitative) + reference + verbatim quote; YAML output, 5 few-shot examples including relative wording,
  strict schema. File: `gapfinder/ledger/assumptions.py`. Fixes the "10× more iterations" sign error.
- [ ] D2. **Deterministic resolver (PAL-style):** the LLM emits expressions like `knob.base * 10`; code
  substitutes the repo's defaults and per-dataset bases, so the direction is computed, not guessed
  (PAL: +15% absolute over chain-of-thought on GSM8K by offloading arithmetic).
- [ ] D3. **Branch on ambiguity:** two plausible readings give two candidate values (e.g. `epochx` 10 and >500);
  the experiments decide.
- [ ] D4. **Numeric direction check** before any run: is the effective quantity above or below the default,
  and does the paper say more or less? Disagreement means ambiguous, so branch.
- [ ] D5. **AST knob inventory first:** argparse (name, default, type, help), constants and config keys with
  file:line; every LLM setting must map to a knob ID or be marked "unmapped". File: `gapfinder/ingest/repo_map.py`.
- [ ] D6. **Log-ladder candidates** (×0.02, 0.1, 0.5, 2, 10, 50) with a direction hint from the gap sign,
  plus a 3-point log-linear fit to interpolate toward the target. File: `gapfinder/search/hypotheses.py`.
- [ ] D7. **New labels:** "explains target, conflicts with held-out (by X SD)" and "probable code-level cause
  (out of scope)" with a reason, instead of a silent Unexplained. Files: `search/engine.py`, `report/`.
- [ ] D8. **Noise floor and baseline precheck:** seeds and splits as a control, never as a cause; "can the
  baseline be reproduced at all?" before blaming any condition (the RusKey lesson).

**Tier 2: bigger changes (1-3 days each)**
- [ ] D9. **Paper-era commit diff:** choose the commit nearest the paper date (or one linked from the README),
  extract argparse, config and **literals at training call sites** via AST, align old→new; every changed
  value becomes a high-prior hypothesis with the old value as a candidate. Verified on MC Dropout: `a6259f1`
  uses `n_epochs*10` and one layer, HEAD uses `--epochx 500 --hidden 2`.
- [ ] D10. **README / changelog / committed-results-filename mining** (e.g. `*_100_xepochs_1_hidden_layers.txt`),
  every hypothesis tagged with its provenance. **Leak risk in blind evaluations:** always report with and
  without these sources.
- [ ] D11. **Measured screen instead of evidence-gate pruning:** cheap probes rank knobs by effect; the LLM
  prior only orders, and the evidence gate only labels (Explained vs Fits but unsupported). This addresses the
  blind-test finding that random order and evidence-off found more causes.
- [ ] D12. **Interaction search:** group screening (move all paper-direction values together, then bisect),
  then a 12-run foldover Plackett-Burman or 2×2 factorials on flagged pairs, then ddmin to a 1-minimal set.
  Targets the 0/12 interaction-task result; use when the single-knob screen finds nothing.
- [ ] D13. **Multiple-comparison control:** Benjamini-Hochberg for shortlists, Holm for the final claim,
  sequential (SPRT-style) repeats, so false attributions stay at 0 as the number of tests grows.
- [ ] D14. **Shared ledger across arms** (cost): one claim extraction per task and run, shared by all GapFinder
  arms. A test run drops from about $7.50 to about $2-3.
- [ ] D15. **Cross-operation sharding** for Sandboxes (one branch as several parallel operations plus a
  merge), to beat the 3,600 s cap for very large cells.

**Tier 3: research-level (later)**
- [ ] D16. Priors from **sibling repos and cited baselines** (paper lineage; PaperRepro-style, magnitude unverified).
- [ ] D17. **Issue/PR mining** with a date filter (ReproRepo surfaced related human blockers for about 90% of
  1,149 papers; method unverified).
- [ ] D18. **Dataflow tracing** of indirect knobs (effective quantity = flag × base, e.g. epochs = 40 × `epochx`).
- [ ] D19. **Level-set Gaussian process** over log values, to report the *range* of values consistent with the
  claim, with uncertainty.
- [ ] D20. **Environment default-change tables** (library defaults that changed silently between versions,
  e.g. scikit-learn's SVC `gamma`) as low-prior hypotheses.
- [ ] D21. **Multi-sample ledgers:** several independent extractions, take the union, rank by agreement and
  measured effect (hedges against one biased ledger).

**How to prove any of these honestly:** tag the version, run the sealed generator with a new seed afterwards
(add order-of-magnitude and relative-wording knob categories to `eval/gapbench/gen_tasks.py`), add the
AI-author tasks if available, ablate documentation-derived sources, and report confidently-wrong counts
next to every gain. Show any MC Dropout improvement only as post-hoc.

### Rules that still apply (unchanged; see section 0)
- Keys only privately. A new machine copies [eval/results/spend_ledger.jsonl](eval/results/spend_ledger.jsonl)
  to `.gf_cache/spend.jsonl` first; **one machine does paid work at a time**.
- Set `GF_SANDBOX_GUARD_USD=20000` for any run: the diagnostic sandbox total is far above the default $60
  guard, and it refuses even local runs otherwise.
- On Windows: run pytest from Git Bash; call the CLI as `python -m gapfinder.cli` if the launcher is missing.
- Never re-score the frozen evaluations after a code change; new claims need new blind tasks or a
  clear "post-hoc" label.

---

## 0. Read first: how things work here

### What GapFinder is

You give it a paper (PDF or text) and the paper's code repository.
1. **Claim ledger.** Nemotron 3 Ultra extracts the paper's claims, and a Super pass filters out
   non-results. Every quote must string-match the PDF.
2. **Assumption space.** Ultra lists settings the results could depend on, each tied to a paper
   quote or a `file:line` in the repo.
3. **Harness spec.** A human-confirmed YAML says how to build, load and run the artifact, and
   which knobs exist. Examples: `papers/ruskey/ruskey_fig6_final.yaml`,
   `eval/gapbench/mlbench.yaml`.
4. **Search** (`gapfinder/search/engine.py`). In Token Factory Sandboxes it builds and loads
   once, then forks one branch per hypothesis. It works in rounds: screen, confirm, combine,
   bisect, verify.
   - **Verification:** revert each knob (the gap must come back), check held-out claims (they
     must not get worse beyond noise), and require evidence that the authors used the value
     (paper, code, web).
5. **Gap Report** (`gapfinder/report/gap_report.py`). One card per claim, with a label:
   Explained, Paper-artifact inconsistency, Partially explained, Fits but unsupported,
   Unexplained, or Reproduced.

### Where things are

| Path | What |
|---|---|
| `gapfinder/` | the library: `ledger/`, `sandbox/` (backends, orchestrator, checkpoint tree, noise), `search/` (engine, verify, evidence, triage, bisect), `report/`, `api/server.py`, `cli.py` |
| `eval/gapbench/` | GapBench-mini: artifacts (`artifacts/rlbench`, `artifacts/mlbench`), task folders, `harness.py`, `score.py`, `make_task.py`, `leakage.py`, `TEST_TASKS.md` |
| `eval/baseline/` | the mini-swe-agent baseline (prompt, budgeted model, sandbox adapter) |
| `eval/results/` | every scored result file; the web scoreboard reads the highest version |
| `papers/ruskey/` | RusKey: gold sets, specs, harness scripts, every RusKey run, `FINDINGS.md` |
| `demo/runs/` | runs the web UI replays |
| `web/` | React UI; `VITE_STATIC=1` builds the server-free site |
| `scripts/` | `check_env.py`, `fetch_paper.py`, `export_static.py`, RusKey packaging |
| `docs/` | `PLAN.md` (original plan), `FEEDBACK_SUBMISSION.md`, `ACCOUNT_SETUP.md`, screenshots |

### Setup

Follow [SETUP.md](SETUP.md): Python 3.11 with uv, then `pytest -q`, which should show 97
passed. Keys go in `.env`, which is git-ignored, never committed and never pasted anywhere.
Ask S for them. They are the Token Factory key (also used for Sandboxes), the Nebius project ID
and the Tavily key.

### Money safety: do this before any paid or sandbox run (S, in the Nebius console)

Sandboxes **looked** free when we checked the console on 2026-10-08: the usage page billed only
Nemotron inference, and none of the sandbox "cost" appeared. That is an observation, not a
promise; the docs don't publish Beta pricing. The only ways to lose real money are:
- Nebius starting to bill sandboxes (end of the Beta) without us noticing;
- auto top-up on an attached card;
- the API key being used elsewhere.

Before anyone runs anything that touches Sandboxes or spends Nemotron credit:
1. [ ] **Billing → usage:** confirm there are still no sandbox charges. Reported sandbox cost is
   now **$55.40** in total.
2. [ ] **Payment method:** check whether a card is attached, and **turn off auto top-up** if it
   exists, so spending stops at the balance instead of charging the card.
3. [ ] **Budget alert:** set one at a low amount, e.g. $10 above what is already spent.
4. [ ] **Ask Nebius** (Discord, https://discord.gg/eXYTGhgnhK): "Is Sandboxes Beta usage free, and
   how will we be told before billing starts?" Write the answer here.
5. [ ] **Share keys only privately** (never in chat logs, commits or screenshots). If a key may
   have leaked, rotate it in the console.

**Until items 1-3 are done, run nothing on Sandboxes** (`--backend contree`). Local runs
(`--backend local`, GapBench, the toy suite, `GF_CACHE_ONLY=1`) are free and fine.

### Handing over to another machine

- **Spend ledger:** the guards (`GF_SPEND_CAP_USD`, `GF_SANDBOX_GUARD_USD`) count from
  `.gf_cache/spend.jsonl`, which is git-ignored and per machine. On a new machine it starts empty,
  so the guards would count from $0. Copy the snapshot first:
  `mkdir -p .gf_cache && cp eval/results/spend_ledger.jsonl .gf_cache/spend.jsonl`.
- **Only one machine runs paid or sandbox work at a time.** Each machine keeps its own ledger,
  so they can't see each other's spending; the Nebius console is the only shared source of
  truth.
- **Model and web caches** (`.gf_cache/llm/`, `.gf_cache/tavily/`): without them, anything
  already computed costs money again. They contain no keys. The model cache holds reasoning
  about RusKey with one-line code quotes, so S decides whether to share them privately or
  commit them.
- **Never shared through this repo:** `.gf_cache/ruskey_bin/`, `.gf_cache/ruskey_src.tar.gz`,
  `.gf_cache/repos/ruskey` (S's private research code), `.gf_cache/papers/` (re-download with
  `scripts/fetch_paper.py`), and `runs/` (scratch outputs; everything kept is copied into
  `eval/` or `papers/`).
- **The MC Dropout feasibility scripts** are in `eval/external/mc-dropout/scripts/`.

### Money rules (strict)

- **The whole project has about $50 of Token Factory credit, and only Nemotron inference is
  billed.** $1.92 is spent so far.
- `GF_SPEND_CAP_USD` in `.env` (currently 11) is a hard cap on billed spend across every process.
  Don't raise it without S's OK.
- **Sandboxes are unbilled during the Beta**, but every run reports a `cost` of about $0.01 per
  CPU-second. We still track it:
  - $55.40 has been reported so far (including $6.58 lost to one failed MC Dropout timing run);
  - `GF_SANDBOX_GUARD_USD` (default 60) refuses new sandbox runs past that total;
  - **ask S before any run that would cross it.** Any further sandbox work needs the guard
    raised, so it needs S's OK.
- Tag every paid experiment: `GF_SPEND_TAG=<name>`. Check spend at any time:
  `python -c "from gapfinder.models import budget; print(budget.spent_usd(), budget.sandbox_reported_usd())"`.
- `GF_CACHE_ONLY=1` reuses cached model answers and makes no paid call, so re-runs are free.
- `GF_SANDBOX_CPU_LIMIT_S` (default 300) is a per-process CPU-time limit inside sandboxes. Raise
  it only for a run you know needs more.

### Git and honesty rules

- **Commit identity:** `sayjad <2105021@cse.buet.ac.bd>`. The current developer commits under
  their own identity (NawrizTurjo). Commit after each piece of progress, with a message that
  says what changed and why.
- **No AI-assistant attribution anywhere:** no co-author lines, no tool names in commit messages,
  code comments or pushed files. Before each commit, check that the staged diff contains no keys,
  no project ID, no `.env`, and no assistant attribution.
- **Never open hidden answers** (`eval/gapbench/sealed/`, or any `answer.json` / `hidden` field of a
  test task) before scoring. The person who
  tunes GapFinder must never see them.
- **Every number in the README, the video and Devpost needs a log in the repo.** If a run fails,
  record the failure.
- **RusKey:** the source lives only on S's machine, in WSL at `/root/ruskey`. The Desktop
  `ruskey` folder is a dead copy; never use it. Never run two benchmarks at once in WSL. If a
  RusKey correctness test fails, stop and report to S. See "Getting RusKey" below for what the
  next developer needs.
- RusKey's database load is **not reproducible**: the same command gives a different layout and
  different ratios each time. Any new RusKey search must use `--noise-setups 5`. See
  `papers/ruskey/FINDINGS.md`.

---

### Getting RusKey (the source is only on S's PC)

**You don't need the RusKey source for almost anything.** The built RusKey program (the
stripped `ruskey_bench` driver and its libraries) was uploaded once into a Sandboxes snapshot in
our Nebius project. Every RusKey search starts from that snapshot:
`--adopt source=98e3e854-cf02-43c0-8cd2-5d5423de247a --adopt built=98e3e854-cf02-43c0-8cd2-5d5423de247a`.
With the project's API key and project ID in `.env`, you can use it from any machine. Also put
`GF_RUSKEY_SOURCE=98e3e854-cf02-43c0-8cd2-5d5423de247a` in `.env`: the RusKey specs read their
`base` from it.

| Work | Needs the RusKey source? | How |
|---|---|---|
| RusKey searches, the positive control, `--noise-setups` runs | No | adopt the snapshot above; the harness scripts are in `papers/ruskey/harness/` |
| Re-labelling or analysing past RusKey runs | No | the event logs are in `papers/ruskey/` (`search_final/`, `search_setups/`, `ablation/`) |
| The RusKey gold sets and ledger scoring | No | `papers/ruskey/gold_*.json`, `eval/ledger_eval.py`, frozen ledger in `papers/ruskey/ledger_v5/` |
| Re-running the RusKey claim ledger (P1-3, setting recall) | **Yes**: the assumption step reads the code | S shares a copy privately (below) |
| Rebuilding the RusKey binary (new driver or settings) | **Yes** | only S, in WSL: `scripts/prep_ruskey_bin.sh` |

S's steps so the next developer is never blocked:
1. [ ] **Keep the snapshot alive.** Untagged Sandboxes images can be cleaned up after about 180
   days. Tag it once, which costs no compute:
   `python -c "import asyncio; from gapfinder.config import settings; settings(); from gapfinder.sandbox.backend import ContreeBackend; asyncio.run(ContreeBackend().tag('98e3e854-cf02-43c0-8cd2-5d5423de247a', 'gf/ruskey/prebuilt'))"`
2. [ ] **Back up the binary bundle privately.** In WSL, run
   `bash scripts/prep_ruskey_bin.sh /root/ruskey /tmp/ruskey_bin`, then zip `/tmp/ruskey_bin`
   and share it privately (e.g. Google Drive). **Never commit it to this public repo**: it's S's
   research code. With it, the snapshot can be recreated by spike S3
   (`tests/spikes/s3_build_ruskey.py`; see `tests/spikes/README.md`). S3 uploads the bundle and
   prints new `GF_RUSKEY_SOURCE`, `GF_RUSKEY_BUILT` and `GF_RUSKEY_LOADED` IDs for `.env`; use
   those in the `--adopt` flags instead of `98e3e854…`.
3. [ ] **Only if the ledger must be re-run:** share the source privately, e.g. a **private**
   GitHub repo with the friend added as a collaborator. Don't put it in this public repo.

### Who writes hidden tasks (no team member does)

Blind tests only count if whoever tunes GapFinder can't know the answers. Two sources replace a
human task author, and they complement each other:
- **The generator** draws tasks at random, so nobody chooses them: no selection bias.
- **The AI author** writes tasks on purpose to fool GapFinder: adversarial pressure.

Use both, and report them separately.

#### Source 1: sealed random task generator (D builds it; the seed decides the tasks)

1. **Build `eval/gapbench/gen_tasks.py` and commit it before anything is frozen.** Everything that
   shapes the tasks is fixed in that commit, so it is pre-registered:
   - **category quotas:** the six categories in the P0-2 table, e.g. 2 + 2 + 1 + 1 + 1 + 1 for 8
     tasks;
   - **artifacts:** `rlbench` and `mlbench`;
   - **value pools per knob:** only plausible values, taken from the artifact's own argparse
     `choices`, its help text, or common values (e.g. factors of 2, 5 and 10 around the
     default). Never draw arbitrary numbers: a value nobody would write in a paper or code isn't
     findable by anyone, and that makes the task unfair rather than hard;
   - **paper templates:** a setup section that states every knob except the hidden one. For
     `stated_code_differs`, it states the hidden value in words (e.g. "decays as 0.1/(1+t/50)").
2. **Each draw, in order:** pick the category from the quota, then the artifact, then the hidden
   knob or knobs and their values from the pools, all with `random.Random(seed)`. Then write the
   paper and targets, and validate:
   - run `make_task.py` (the gap must exceed 3 noise bands) and `leakage.py` (0 leaks), and redraw
     on failure;
   - for interaction tasks, also check that each knob alone does *not* close the gap;
   - record how many draws were rejected, and why.
3. **Keep the answers out of the task folders.**
   - The generator writes each task's answer (`answer.json` and the hidden part of `task.yaml`)
     to `eval/gapbench/sealed/<task>/`, which is git-ignored until the reveal.
   - The task folder keeps only what GapFinder may see: paper text, targets, calibration.
   - Extend `eval/gapbench/score.py` with `--answers eval/gapbench/sealed`, so scoring reads the
     answers from there.
4. **The seed comes after the freeze.**
   - D tags GapFinder (`git tag pre-tasks-N && git push origin pre-tasks-N`).
   - Then D generates the seed: `python -c "import secrets; print(secrets.token_hex(16))" > eval/gapbench/sealed/seed.txt`.
   - Run the generator **without printing task details:** it should print only the number of
     tasks and the sha256 of the sealed folder (a tarball of `sealed/`, sorted).
   - Commit the task folders and `eval/gapbench/sealed.sha256`.
   - D must not look at the generator's logs, `sealed/`, or its make_task output.
5. **Dry runs are allowed** with a throwaway seed, to check that the generator produces valid
   tasks. Delete those tasks before the real seed, and don't tune GapFinder on them after the
   freeze.
6. **After scoring,** commit `sealed/` and `seed.txt`. Anyone can then check the hash, re-run the
   generator with the seed, and get exactly the same tasks.
7. **Honest wording:** "tasks drawn at random by a generator, from a seed created after GapFinder
   was frozen". Also state the limitation: we designed the generator's categories and value pools.
   That's why the pools are committed before the freeze, and why the AI author's tasks are
   reported alongside.

#### Source 2: an independent AI task author

An AI model that had no part in building GapFinder can write tasks on purpose to fool it. This
counts as independent if all of these hold:

1. **It is a coding agent with its own clone of the repo and a shell,** not a plain chat window.
   Every task must pass `make_task.py` and `leakage.py`. A chat model can't run them, and whoever
   pastes its answers in would then know them.
2. **It is a different model from the one that built and tuned GapFinder.** Another session of
   the same assistant shares its habits and tends to write tasks GapFinder already handles. Use
   a model from another vendor, e.g. ChatGPT or another company's coding agent.
3. **GapFinder is frozen before the tasks exist.** D tags the commit first
   (`git tag pre-tasks-N && git push origin pre-tasks-N`; the same tag the generator uses), and
   only then does the author commit tasks. Git history then proves no tuning followed. The author *may* read GapFinder's code and
   README and try to fool it; that makes the test harder, not weaker.
4. **D never opens the answers.** The author commits the tasks in one commit. D runs the
   harness, which reads only the paper text and targets, and the scorer, without opening
   `answer.json` or the `hidden` field of `task.yaml`.
5. **Honest wording everywhere:** "tasks written by an independent AI model with no part in
   building GapFinder", never "written by other people".

Briefing for the author: [eval/gapbench/TEST_TASKS.md](eval/gapbench/TEST_TASKS.md), the
category table in P0-2, the README (so it knows what it's trying to fool), and the instruction
"hide one cause per task so that GapFinder misses it if it can be fooled; every task must
still pass `make_task.py` and `leakage.py`."

## P0-1. Blind test on a real, independently documented reproduction gap

**Why:** so far GapFinder has only been checked on tasks our own team built, which can be
unconsciously easy. A paper whose gap was diagnosed by *other people* is the strongest evidence
we can add. Matching a name is not enough: the predicted setting must actually move the result
when re-run.

### Candidate A: MC Dropout (Gal & Ghahramani, ICML 2016, "Dropout as a Bayesian Approximation")

- **Repo:** https://github.com/yaringal/DropoutUncertaintyExps
- **Checked by reading the current repo:**
  - `experiment.py` takes `--dir` (dataset), `--epochx` (epoch multiplier, **default 500**) and
    `--hidden` (hidden layers, **default 2**).
  - Per-dataset settings are data files in `UCI_Datasets/<dir>/data/`. For Yacht:
    `n_epochs.txt`=40, `n_splits.txt`=20, `dropout_rates.txt`=0.005 0.01 0.05 0.1,
    `tau_values.txt`=0.25 0.5 0.75, `n_hidden.txt`=50.
  - `net/net.py` hard-codes `T = 10000` Monte Carlo test passes. That's a cost, and we can't
    change it without a code edit.
  - It imports `scipy.misc.logsumexp`, which modern scipy has removed, and uses the old Keras
    `nb_epoch` argument.
  - The README says the experiments ran with **Theano 0.8.2 and Keras 2.2.0**.
- **Documented cause:**
  - The author's README (current, and at commit `a6259f1`) reports that results change with
    10x training epochs and with 2 hidden layers instead of 1.
  - Mukhoti, Stenetorp and Gal (2018, arXiv 1811.09385) say the dropout baseline was stopped
    early.
  - **Verified from the PDF and the paper-era code** (see
    [FEASIBILITY.md](eval/external/mc-dropout/FEASIBILITY.md)):
    - the ICML paper (p.6) says "50 units" and "we used 10x more iterations", i.e. 400 epochs;
    - the paper-era code (`a6259f1`) used `n_epochs*10` and one hidden layer.
    - So the paper's setting is `--epochx 10 --hidden 1`, **not** 40 epochs, which an earlier
      draft of this TODO said.
    - Use the **ICML proceedings version** as the paper. The later arXiv version adds a Table 2
      that states the effect outright.
  - Claimed numbers (ICML Table 1, dropout RMSE): Concrete 5.23, Energy 1.66, Yacht 1.11.
- **Expected outcome if GapFinder works:** it names `epochx` and/or `hidden`, probably as a
  "Paper-artifact inconsistency" (the paper states one value and the code defaults to another).
- **Caveats** (write all of them in the answer key before running):
  - A second documented change, Bayesian optimisation replaced by grid search, is a code change
    GapFinder can't test. A perfect GapFinder is therefore only partly correct here; score
    partial credit.
  - The README's "paper" column (Yacht 0.70, Energy 1.08) is a later re-run, **not** the
    published Table 1. Decide which numbers count as "the paper's" (recommended: the published
    Table 1, quoted from the PDF) and record the choice in the answer key.
  - **Not fully blind:** this TODO already states the documented cause. Report the result as
    "semi-blind". The safeguards below (sealed key, frozen code, spec generated from the repo
    map) keep it honest, and the truly blind case (Step 6) comes later.
- **Datasets to use:** Yacht, Energy, Concrete (308-1,030 rows; CPU-friendly).

### Candidate B (backup): Paragraph Vector on IMDB (Le & Mikolov, ICML 2014)

- Reported 92.58% accuracy. Code: https://github.com/mesnilgr/iclr15 (`scripts/paragraph.sh`).
- Documented cause: Mesnil, Mikolov, Ranzato and Bengio (ICLR 2015 workshop, arXiv 1412.5335)
  say 92.6% appears only with hierarchical softmax (`-hs 1 -negative 0`) **and** unshuffled
  training/test data; with shuffling they got 88.73%.
- Risks: about 15-25 min per run on 4 CPUs (unverified); the 92.6% may not reappear with
  multi-threaded word2vec; the shuffle is a script line, not a flag.

### Status: decided (local Docker, scaled), Steps 1-2 done, freeze next

**Decision made:** option 2 below (local Docker), scaled like option 1: `T = 100` and 3-split
blocks. The status is no longer "blocked". Done so far:
- **Step 1:** go verdict in [FEASIBILITY.md](eval/external/mc-dropout/FEASIBILITY.md) (pinned
  image, timings, the gap seen).
- **Step 2:** answer key sealed; only its hash is in the repo (`eval/external/mc-dropout/answer_key.sha256`).
- **Targets:** Energy RMSE is the target claim. Yacht and Concrete are held out: Yacht alone was
  too weak (a gap of about 2 s.e.).
- **Code:** `evidence_gate` and `--no-evidence-gate` are done (commit "Search ablations: evidence-gate switch, random-search arm, fair baseline input").
- **Extra changes GapFinder can't test, recorded in FEASIBILITY.md:** grid search instead of
  Bayesian optimisation, and `batch_size` 128 instead of the paper's 32.

Still to do: Step 3 (the freeze tag) onward.

The text below is the original Sandboxes finding, kept as history.

Results are in [eval/external/mc-dropout/FEASIBILITY.md](eval/external/mc-dropout/FEASIBILITY.md).
- **Works:**
  - `python:3.6-slim` runs in Sandboxes, and sandboxes have network access;
  - the old stack installs in 65 s: numpy 1.13.3, scipy 1.1.0, Theano 0.8.2, Keras 2.2.0,
    h5py 2.8.0, plus `g++`;
  - it is checkpointed as `c6fbd1fc-a3aa-4aad-91c8-2ed7b35f65ff`.
- **Blocks:**
  - one hyperparameter setting costs about 650 CPU-seconds, because `net/net.py` makes
    `T = 10000` separate `model.predict` calls;
  - 13 settings run per split, so one split is about $85 of reported cost and the paper's 20
    splits about $1,700.
- **Lost:** $6.58 of reported time, on a run that crashed because our upload dropped the empty
  `results/` folder. That bug is fixed (`_empty_dirs` in `gapfinder/sandbox/backend.py`).

**Decision for S (made: option 2, scaled).** Options, with the recommended one first:
1. **Recommended: a scaled run.**
   - Use `T = 100` Monte Carlo samples instead of 10,000, and 3-5 splits instead of 20.
   - The harness spec's `build` stage applies one fixed, documented patch before anything runs:
     `sed -i 's/T = 10000/T = 100/' net/net.py`.
   - **`T` must not be a knob**: GapFinder searches only the repo's real conditions, and itself
     still edits no code.
   - Report it as a scaled reproduction, like RusKey's 2M keys instead of 100M. 100 samples
     estimate the predictive mean (RMSE) well; the test log-likelihood less so.
   - First measure one grid setting with `T = 100` (expected: tens of seconds), then size
     `--max-runs`.
   - Needs: the money safety checks above, and the guard raised (e.g.
     `GF_SANDBOX_GUARD_USD=80`).
2. **Run it locally in Docker:** the same pins on `python:3.6-slim`, with GapFinder's local
   backend inside a container. There's no sandbox cost, but it takes many hours of a laptop
   and loses the "in Sandboxes" part.
3. **Switch to Candidate B** (Paragraph Vector), or **do the RusKey positive control first.**

Once S decides, continue with Step 1 item 5 (check there is a gap) and then Step 2.

### Step 1: feasibility check on Candidate A (D). **Done**; see Status above and FEASIBILITY.md.

Cost: no Nemotron spend; a few cents of reported (unbilled) sandbox cost. Stop and tell S if any
check fails.

1. **Find a working software pin locally first** (WSL or Docker, free). Use Python 3.6 with
   Theano 0.8.2 and Keras 2.2.0, plus a numpy and scipy old enough that `scipy.misc.logsumexp`
   exists (scipy < 1.3) and Theano 0.8.2 works. Try numpy 1.13-1.16 and scipy 1.1-1.2, and
   record the exact set that imports `net/net.py` cleanly. Set `THEANO_FLAGS='device=cpu,floatX=float32'`.
2. **Check that a sandbox can run that environment.** The Sandboxes backend can start from a
   public Docker image by name (`ContreeBackend.base("python:3.6-slim")`). Write a throwaway
   script, outside the repo, that does the following, and run it with
   `GF_SPEND_TAG=mcdropout-feasibility`:
   - create the base from `python:3.6-slim`;
   - run `python --version; pip --version; nproc`;
   - run `timeout 40 pip download --no-deps -d /tmp/x theano==0.8.2 keras==2.2.0` to find out
     whether sandboxes have network access;
   - use `disposable=True` and a short timeout.
3. **If sandboxes have no network:**
   - download the wheels locally (`pip download` for Linux/py3.6 with
     `--platform manylinux1_x86_64 --python-version 36 --only-binary=:all:`);
   - put them in an artifact folder with the repo;
   - set the spec's base to `local:<folder>`, with `GF_CONTREE_LOCAL_IMAGE=python:3.6-slim`
     (the backend uploads the folder into `/work`);
   - install from those wheels in the spec's `build` stage with `pip install --no-index --find-links`.
4. **Time one small run** in a sandbox:
   - `python experiment.py --dir yacht --epochx 1 --hidden 1`, with `n_splits.txt` set to 2;
   - record wall time and CPU-seconds;
   - then time `--epochx 500 --hidden 2` (the defaults) on 1 split. That's the naive run, and it
     may be slow: if a single split takes more than ~10 minutes, plan a scaled run (fewer
     splits) and say so in the report, the way RusKey runs at 2M keys instead of 100M.
5. **Check there is a gap.** Defaults vs the paper's Table 1 numbers: the gap must be larger than
   the run-to-run noise (3 repeats). If the defaults land within noise of the paper, this case
   can't test anything. Switch to Candidate B or to the RusKey positive control.
6. **Write the result** in `eval/external/mc-dropout/FEASIBILITY.md`: software pins, network yes
   or no, timings, the gap seen, and a go/no-go. Commit it.

### Step 2: seal the answer before running (D writes it, S checks it). **Done** (`answer_key.sha256`)

1. Create `eval/external/mc-dropout/answer_key.md` with:
   - the paper's claimed numbers (dataset, metric, value, page);
   - the documented cause, with exact settings and values and every source URL;
   - what counts as full credit, partial credit and failure;
   - all the caveats above.
2. **Commit only its hash:** `sha256sum answer_key.md > answer_key.sha256`. Commit the
   `.sha256` file and keep `answer_key.md` out of git (move it outside the repo) until Step 5.
   Anyone can then check the key wasn't edited after the run.

### Step 3: freeze the system

- Tag the commit: `git tag ext-eval-1 && git push origin ext-eval-1`.
- Record the model IDs from `gapfinder/config.py`, the run and dollar budget you'll use, and the
  sha256 of each prompt (`CLAIM_PROMPT`, `FILTER_PROMPT`, `ASSUMPTION_PROMPT`, `TRIAGE_PROMPT`)
  in `eval/external/mc-dropout/FROZEN.md`.
- **No GapFinder code or prompt changes for this case until it is scored.** If something blocks
  the run (a crash, a missing parser), fix only that, and describe the fix in the results.

### Step 4: build the inputs without leaking the answer, then run once

1. Paper: get the PDF (arXiv 1506.02142), then run
   `gapfinder ledger <paper.pdf> --repo https://github.com/yaringal/DropoutUncertaintyExps --out runs/mcd-ledger`.
   This costs about $0.10-0.30 of Ultra, so run it once and keep the output.
2. Repo map: `gapfinder repomap <local clone>`. **The harness spec exposes every flag the repo map
   finds** (all argparse flags) plus the per-dataset data files as dataset knobs. Don't
   hand-pick `epochx` and `hidden`. The data files can be set by a wrapper script that writes
   the value into `UCI_Datasets/<dir>/data/<file>.txt` before running; add those paths to
   `allowed_paths`.
3. Output parsing:
   - `experiment.py` writes results to `UCI_Datasets/<dir>/results/*.txt` and prints a summary;
   - write a small wrapper (`harness/run_cell.sh`) that runs it and prints one `key=value` line
     per metric (e.g. `rmse=…`), so the `kv` parser reads it;
   - read lines 195-217 of `experiment.py` first to see what it prints.
4. Targets: a JSON file like `papers/ruskey/targets_fig6.json`, with one claim per dataset
   (Yacht RMSE as the target, Energy RMSE held out, for example). Commit the spec and targets
   **before** the search.
5. Run once:
   `GF_SPEND_TAG=ext-mcd gapfinder search --spec <spec> --targets <targets> --assumptions runs/mcd-ledger/assumptions.json --claims runs/mcd-ledger/claim_ledger.json --backend contree --max-runs <N> --out eval/external/mc-dropout/run1`.
   - Choose N from the feasibility timings.
   - There is no load stage, so `--noise-setups` isn't needed.
6. Keep everything, whatever the verdict: `gap_report.md`, `gap_report.json`, `events.jsonl`.
7. **Rule out "it just read the README".** The repo's own README describes the epochs and layers
   effect, and that text can reach GapFinder in two places: the evidence check, and the
   hypothesis list Ultra writes from the repo. Run these arms as well, all with the same
   budget, and pre-register them in `FROZEN.md`:

| Arm | What changes | What it shows |
|---|---|---|
| normal | nothing | the product as is |
| evidence off | the evidence check is skipped | the experiments alone carry the verdict |
| no README | the ledger runs on a clone with `README*`, `readme*` and `docs/` removed, and the evidence check is off | the cause was found without the documentation |
| all flags, random | hypotheses are every repo-map flag with its candidate values, in random order (the P1-1 random arm) | the ranking isn't what found it |

   - The evidence-off switch doesn't exist yet: add `evidence_gate: bool = True` to
     `SearchConfig` (`gapfinder/search/engine.py`) and a `--no-evidence-gate` flag to
     `gapfinder search` (`gapfinder/cli.py`). When off, the plausibility step is skipped and a
     closing value can be at most "Fits but unsupported".
   - Cost: each extra ledger run is about $0.10-0.30 of Ultra; the searches add sandbox time only.
   - Headline claim: the **strongest** arm that finds the cause, e.g. "found with no README and
     random order".

### Step 5: reveal and score

1. Put `answer_key.md` back, check `sha256sum -c answer_key.sha256`, and commit it.
2. Score against the pre-written rule. Then **re-run the predicted setting** (3 repeats) and
   confirm it moves the metric as claimed. A name match without the effect is not a success.
3. Call the cause "documented" unless our own runs confirm the effect; then call it
   "documented and confirmed here".
4. Write `eval/external/mc-dropout/RESULT.md` (verdict per arm, partial credit, cost, what went
   wrong), add a row to the README "Results" table, and add a replay to `demo/runs/`.

### Step 6: a truly blind second case (the independent AI task author)

The independent AI task author (rules in section 0) picks a paper with a documented
condition-type cause, using the criteria above (public repo, runs on 4 CPUs / 3.9 GB, the cause
is a setting not a code bug, documented by someone else). It writes the answer key and commits
only its sha256, the same way as Step 2, and hands D the paper, the repo and the claimed
numbers. D sees only the paper, the repo and the claimed numbers, never the
cause. Run the same four arms as in Step 4.

### Positive control on RusKey (needs S's OK first)

**Why:** RusKey's real verdict is "Unexplained", which only means something if GapFinder *can*
find a real cause on RusKey. Cost: about $5-10 of reported, unbilled sandbox cost, which takes us
past the $60 guard; S must approve and set `GF_SANDBOX_GUARD_USD` (e.g. 75).

1. **The setting is drawn at random, not chosen.** A small script (`papers/ruskey/gen_control.py`,
   committed before the draw) lists the candidate changes from `papers/ruskey/ruskey_fig6_final.yaml`:
   every knob's documented alternative values, kept within its `max`. It draws one with a fresh
   seed, created after the freeze tag as in the generator above.
2. The same script measures the drawn change on 5 independent loads (`--noise-setups 5` with that
   change). It writes `targets_control.json`, whose `paper_value`s are those medians, and puts
   the drawn setting and the measurement's event log in a git-ignored `papers/ruskey/sealed/`
   folder. It prints only the sha256 of that folder; commit the hash. D must not read the
   script's output or the sealed folder.
4. D runs:
   `gapfinder search --spec papers/ruskey/ruskey_fig6_final.yaml --targets targets_control.json --assumptions papers/ruskey/ledger_v5/assumptions.json --claims papers/ruskey/ledger_v5/claim_ledger.json --backend contree --adopt source=98e3e854-cf02-43c0-8cd2-5d5423de247a --adopt built=98e3e854-cf02-43c0-8cd2-5d5423de247a --noise-setups 5 --max-runs 60`.
   No upload is needed: the `--adopt` snapshot already contains the RusKey binary (see "Getting
   RusKey").
5. Score: did it name the planted setting with a confirmed label? Record the result in
   `papers/ruskey/FINDINGS.md` and the README.

---

## P0-2. Hidden GapBench test tasks (generator and AI author write them; D runs them)

**Status:** the tooling is done. Real generation is pending, after the freeze tag.
- Done: `eval/gapbench/gen_tasks.py` (sealed generator, answers outside the task folders);
  `eval/gapbench/PROTOCOL.md` (pre-registration); the `score.py` upgrades (categories, Wilson
  intervals, `--answers`, answer stability, results by source); the trust matrix on the
  Scoreboard; the dev set re-scored as `gapbench_dev_v7.json`.
- Pending: generating and running the real test tasks. Run `gen_tasks.py` only after the freeze tag.
- Limitation: RL noise is wide, so the interaction, decoy and no_cause categories land mostly on
  mlbench. Report that, don't hide it.

**Why:** 4 dev tasks built by our own team can't show generalisation. The hidden tasks are the
main evaluation. Both sources from section 0 contribute:
- **8 tasks from the sealed random generator:** unbiased selection;
- **up to 10 "fool GapFinder" tasks from the independent AI author:** adversarial.

Report the two sets separately and together. All of them use our two toy artifacts (rlbench,
mlbench), so describe them as "blind tasks", not as outside papers.

1. **Generate and write the tasks** under the rules in section 0. Both sources follow
   [eval/gapbench/TEST_TASKS.md](eval/gapbench/TEST_TASKS.md) (template, `make_task.py`, which
   rejects gaps under 3 noise bands, and `leakage.py`, which must print `0 leaks`) and cover these
   categories, which extend that file's type list:

| Category | How to build it | Correct outcome |
|---|---|---|
| Known cause, one setting | `single_unstated` or `stated_code_differs` | names the knob, confirmed |
| Interacting settings | `interaction`: two knobs, neither enough alone | names both |
| No supported explanation | `no_cause` with an `offset`, plus a held-out claim moving the other way | no confident attribution |
| Several plausible causes | a decoy knob that also moves the target but breaks a held-out claim | the true knob, not the decoy |
| Measurement noise only | the "paper" value is within the noise of the naive run | "Reproduced" or "Inconclusive", no attribution |
| Incomplete paper or artifact | the true knob isn't exposed by the harness spec | "Unexplained", with the reason in the report |

2. **Commit each source's tasks in one commit** (`Add generated GapBench test tasks`,
   `Add AI-authored GapBench test tasks`), after the freeze tag. D must not open the answers.
3. **D: before the first test run, write `eval/gapbench/PROTOCOL.md`**, a pre-registration. Commit
   it before any test run. It covers:
   - the arms (`gapfinder`, `gapfinder-noverify`, `baseline-super`, plus `gapfinder-random`
     and `baseline-ultra` if added, see P1-1);
   - the per-task dollar cap (`--cap 0.5`) and the baseline step limit (`--steps 40`);
   - runs per task (3);
   - the scoring rule for each category above: correct, partial, confidently wrong, correct
     abstention, missed;
   - the rule that the test set is run exactly twice, once now and once on frozen v1.0.
4. **D: extend `eval/gapbench/score.py`:**
   - read each task's category and report, per arm: correct attributions, confident wrong
     answers, correct abstentions, missed causes, proportion of the gap closed (`gap_closed`
     already exists), experiments used, wall time, cost;
   - add a 95% Wilson interval for each rate;
   - `CONFIDENT` is defined at line 39; add "Inconclusive" as an abstention once P0-3 adds it.
5. **D: run** each arm 3 times per task:
   `python eval/gapbench/harness.py eval/gapbench/tasks/<task> --arm <arm> --run <k> --cap 0.5`
   (add `--fresh` for GapFinder so repeats don't reuse cached model answers). Then
   `python eval/gapbench/score.py --split test --out eval/results/gapbench_test_v1.json`.
   - Expected cost for 8 tasks: under $1 for GapFinder and about $1-2 for the Super baseline. With
     10 extra tasks, roughly double it; still a few dollars.
   - Report how often GapFinder's answer changes across its 3 runs.
6. **D:** update the README Results table and the web Scoreboard (automatic from the results
   file). Present raw counts with intervals; never claim a statistically conclusive win from
   8 tasks.
7. **D: trust matrix.** One small grid per arm: rows are what the truth was (a cause, or none);
   columns are what the arm said (correct cause, wrong cause stated confidently, abstained,
   missed). Put it in the README and on the Scoreboard tab (`web/src/Scoreboard.jsx`). It is just a
   picture of the counts from step 4, but it shows in one glance whether the system knows when
   to abstain.

---

## P0-3. Noise as a first-class feature

**Status:** items 1, 2, 4 and 6 are done. Item 4: effect sizes with a bootstrap interval are on
every card. Item 6: forked repeats are too narrow compared with fresh loads on C5b and C3
(`eval/results/ruskey_fork_comparability.json`). Items 3 and 5 are open.

**Why:** the RusKey finding (identical loads giving different results) shows that a system which
changes settings until one run matches the paper will fool itself. Already done: noise bands from
repeats, extra repeats when CV > 5%, `--noise-setups` with the content-addressed reproducibility
check, and no labels from unconfirmed runs.

1. **Done.** **Add an "Inconclusive" verdict.** Today RusKey C5b is labelled "Reproduced" inside a ±16% band,
   which overstates it.
   - Add `inconclusive = "Inconclusive"` to `ConfidenceLabel` in `gapfinder/ledger/schemas.py`
     (line 124).
   - In `GapSearch` (`gapfinder/search/engine.py`, around line 276, where `res.status =
     "reproduced"`), call it Reproduced only if the band is at most a tolerance:
     `SearchConfig.reproduce_tol`, default 0.05 = ±5% of the paper value. Otherwise use
     Inconclusive, with a note saying how wide the band is.
   - Apply the same rule to a searched claim whose best candidate is within a band wider than
     the tolerance.
   - Update `gap_report.py`, `web/src/api.js` (`LABEL_CLASS`), `eval/gapbench/score.py` (as an
     abstention), and add tests in `tests/integration/test_search_toy.py`.
2. **Done** (dev set unchanged: 4/4, no false attributions; `eval/results/gapbench_dev_v6.json`).
   **A significance test for effects**, alongside the 2×MAD rule.
   - Add `bootstrap_diff_ci(a, b, n=2000, alpha=0.05, seed=0)` to `gapfinder/sandbox/noise.py`.
   - Use it in the confirm round (`units()` and `closes()` in `engine.py`): a candidate's effect
     counts only if the interval on (candidate − naive) excludes zero.
   - Test it on the toy suite and re-score the dev set. Expect the dev results not to get worse;
     if they do, find out why before keeping the change.
3. **Measure, then decide, whether `noise_setups=3` should be the default** for artifacts with a
   build or load stage. It costs 2 extra setups per search: about $0.5 reported for RusKey, and
   nothing for GapBench, which has no setup stage. Keep it opt-in if the cost isn't justified.
4. **Done.** **Report effect sizes with uncertainty** on each card: the candidate − naive difference, its
   interval, and the number of runs.
5. **Determinism X-ray:** a stage-by-stage version of the setup check.
   - Run each setup stage (build, load) twice from the same parent, and compare the checkpoint
     IDs. Identical IDs mean identical files.
   - For stages whose IDs differ, find *which* files differ. There's no file-diff API that we
     know of, so run a cheap command in each of the two checkpoints:
     `find /work -type f -print0 | sort -z | xargs -0 sha256sum`. Then diff the two lists.
   - Classify the result, because log files with timestamps differ on every run and would
     otherwise make everything look non-deterministic:
     - green: identical;
     - amber: only volatile files differ (logs, lock files, timestamps; keep a pattern list in
       the spec, e.g. `volatile: ["LOG*", "*.log", "LOCK"]`);
     - red: data files differ.
   - Separately, report whether the **measured result** differs across those setups (the
     `--noise-setups` band). That's the part that matters for the verdict.
   - Show it as a strip of pipeline stages, coloured, at the top of the Gap Report and in the
     replay. Files: `gapfinder/search/engine.py` (`_check_setups`), `gapfinder/sandbox/runner.py`,
     `gapfinder/report/gap_report.py`, `web/src/Report.jsx`, `web/src/Replay.jsx`.
   - Cost: for RusKey, about 2 extra loads plus 4 tiny hashing runs (about $0.6 reported,
     unbilled); free for GapBench, which has no setup stage.
   - Don't claim "no other tool can do this"; say what it does and show it.
6. **Done (`papers/ruskey/FINDINGS.md`, "Are forked runs comparable").** **Check that forked runs are comparable.** Measure the naive configuration on a forked
   checkpoint and on a fresh setup (this already exists in the RusKey runs; tabulate it in
   `eval/load_variance.py` output). Forked runs should fall within the across-setup noise band.
   If they don't, forking itself changes results; report that.

---

## P1-0. Minimal human input: GapFinder drafts its own harness spec

**Status:** the code is done (`gapfinder/spec_draft.py`, `gapfinder spec-draft`, tests with a
scripted fake model). Live evaluation done on mlbench and rlbench (both pass unedited, recall 100%, $0.0081; MC Dropout skipped), see eval/results/spec_draft_live.md.

**Why:** the Coding and Agentic Engineering track asks for an agent that plans, writes, tests and
iterates on a real repository with minimal human input. Today a person writes the harness spec
(how to build, load and run the artifact, which knobs exist, how to read the output). That is
GapFinder's biggest manual step, and judges will notice it.

1. Add `gapfinder spec-draft <repo> --out <spec.yaml>` (new module `gapfinder/spec_draft.py`, and
   a subcommand in `gapfinder/cli.py`):
   - inputs: the repo map (flags with defaults and `file:line`), build files (`setup.py`,
     `requirements*.txt`, `pyproject.toml`, `CMakeLists.txt`, `Makefile`), the README's usage
     section, and the paper's setup section from the ledger;
   - one Nemotron call (Super first; Ultra if Super's draft fails twice) drafts `base`, `build`,
     `load`, `run`, `knobs` (every repo-map flag, with layer and default), the output format
     and `allowed_paths`;
   - **smoke test in a sandbox:** build, one naive run, parse the metrics. On failure, pass the
     error to the existing triage (`gapfinder/search/triage.py`) and redraft, at most 3 attempts;
   - output the YAML plus a short report of what it tried. A human approves it, and approving
     should be the only manual step. Print a diff if the human edits it.
2. Evaluate it against the hand-written specs: `eval/gapbench/mlbench.yaml`,
   `eval/gapbench/rlbench.yaml`, and the MC Dropout spec from P0-1. Record:
   - whether the drafted spec runs without edits;
   - how many knobs it found compared with the hand-written spec;
   - how many attempts it took, and what it cost.
3. Done when: the drafted spec runs unedited on at least 2 of the 3 artifacts. The README's
   "How it works" and "Limitations" then say exactly how much human input is left.
4. Cost: a few cents of Nemotron per draft, plus a few minutes of unbilled sandbox time.

## P1-1. A fair baseline comparison

**Status:** items 2 and 3 are done, plus the evidence-off arm. The random arm is `gapfinder-random`
(`--rank random`), the evidence-off arm is `gapfinder-noevidence`, and the baseline now gets the
repo map (documented in `eval/baseline/prompt.md`). Not yet run on the test set.

1. Write down equal budgets in `PROTOCOL.md`: the same model, paper text, repo, sandbox tools,
   run cap, dollar cap, wall-time cap and sealed answer key for every arm.
2. Give the baseline the same evidence GapFinder gets: paper text plus the repo map output. The
   baseline prompt is `eval/baseline/prompt.md`, and the change must be documented.
3. **Random-search arm** (`gapfinder-random`): the same hypothesis space and budget, but in random
   order, with no ledger ranking and no strong-lead skip.
   - Add `rank: str = "ledger"` to `SearchConfig`; with `"random"`, shuffle `hypotheses()` with a
     fixed seed and make `_strong_lead()` return False.
   - Add the arm to `ARMS` in `eval/gapbench/harness.py` (line 44).
   - This shows whether the ledger's ranking actually helps.
4. **Ultra baseline arm** (`baseline-ultra`, already in `ARMS`): needs S's OK; probably under $2.
5. **One ablation table** in the README: no-fork (done for RusKey, `eval/results/ablation_ruskey.json`),
   no-verification (`gapfinder-noverify`), random search, and the evidence gate turned off.

## P1-2. The Gap Report answers five questions at the top of each card

**Status:** done. Five questions per card, the provenance block, effect sizes and the cause kind
are in the JSON, the Markdown and `Report.jsx`. The missing sentence is done too
(`--missing-sentence` and the `missing-sentence` subcommand). It is off by default and should be
enabled only after a confirmed cause on a real paper.

Change both `gapfinder/report/gap_report.py` (Markdown and JSON) and `web/src/Report.jsx`.
1. **What did the paper report?** The claim's quote and page. The ledger claims are passed to
   `GapSearch` (`claims=`); carry them into the report.
2. **What did we measure?** The naive median, its repeats and spread, the setup check, and the
   discrepancy.
3. **Which experiment changed it?** The branch, command, config and output, already in `replay`.
   Make it the first thing after the label.
4. **Why do we believe it?** The reversal test, held-out claims and evidence, labelled
   pass/fail in one line each.
5. **What remains unknown?** Untestable values, unmapped flags, the setup reproducibility
   result, unconfirmed leads, and alternative configurations that came close (from
   `closest_overall`).

Also:
- Separate "confirmed cause" (all checks pass), "plausible explanation" (fits but
  unsupported) and "interacting factors" visually.
- **Provenance block on every report:** GapFinder git commit (`git rev-parse HEAD`), model IDs,
  prompt hashes, a sha256 of the harness spec, and total cost (Nemotron billed, sandbox
  reported).
- **Claim robustness** (optional, cheap): for comparative claims ("A beats B"), report in how many
  of the configurations tested the conclusion still holds. Label it "over the configurations
  tested", because they aren't a random sample of settings.
- **"The sentence the paper was missing"**, only once there is a *confirmed* cause on a real
  paper (MC Dropout or the second blind case, not the toy tasks):
  - for each Explained or Paper-artifact inconsistency card, one Super call drafts the methods
    sentence the paper should have contained, shown as a green insertion in the paper's own
    setup paragraph;
  - also draft a polite GitHub issue for the artifact's repo as a file, **never posted
    automatically**;
  - cost: a few cents.
- Re-export the static site data after changing the report (`scripts/export_static.py`), and
  re-run the browser test: `pytest -m e2e tests/e2e`. It needs `npm --prefix web run build`,
  the static build, and `python -m playwright install chromium`.

## P1-3. Smarter search, but only if it measurably helps

1. **Adaptive ranking** as an experiment, not a feature:
   - update each hypothesis's prior from its screen result;
   - spend confirmation repeats on the most promising first;
   - keep it only if it beats the current search (and the random arm) on runs needed to reach
     the right answer across dev and test tasks.
2. **Setting recall** is 0.67 on RusKey, below the 0.80 bar: the tuner's mode flags are missed.
   - Look at the misses in `eval/results/ledger_ruskey_v5.json` (`missed_knobs`).
   - Improve the repo map or the assumption prompt generally, and measure on the external
     paper's ledger as well, so the change isn't tuned to RusKey.
   - The ledger evaluator is `eval/ledger_eval.py`.

## P1-4. Submission requirements (official rules)

- **Working app:** the static replay site.
  1. S makes the repo public (Settings → General → Danger Zone).
  2. S sets Settings → Pages → Source: **GitHub Actions**.
  3. Run the `pages` workflow from the Actions tab.
  4. Check https://sayjad21.github.io/GapFinder/ in a logged-out browser.
  - The workflow is `.github/workflows/pages.yml`; its deploy step fails until Pages is enabled,
    which is harmless.
- **"Try it yourself": option B chosen and done** (`scripts/try_it.py`, `demo/cache/`; README
  "Try it yourself"). Timing on a fresh machine is still open.
- **Decide what "try it yourself" means** (an outside reviewer asked that judges be able to give
  it a paper and repo and start an investigation). Pick one and write the choice and the reason
  in the README:
  - **A, replay only** (current): free and can't break, but judges can't start anything.
  - **B, run it locally for free (recommended):** commit the cached model answers for the
    GapBench dev tasks. Then `gapfinder` can run a full investigation on a dev task with
    `GF_CACHE_ONLY=1` and the local backend, needing no keys and spending nothing.
    - First check that the cache files contain only model outputs: no keys, no project ID,
      no assistant attribution.
    - Add a one-command quick start to the README, and time it on a fresh machine (the plan's
      bar is under 15 minutes).
    - **Done (option B chosen):** `python scripts/try_it.py` runs a dev task from `demo/cache/`
      (the 9 model answers the four dev tasks use; no RusKey content, no Tavily entries, because
      the GapBench harness doesn't use web evidence). Still open: time it on a fresh clone.
  - **C, hosted live mode:** a server with a run button, an access code, a dollar cap and a
    kill switch. It needs paid hosting outside the $50; only with S's approval.
- **Public repo** with the MIT license badge visible at the top, setup instructions (SETUP.md)
  and a test build.
- **Video:** public on YouTube, **under 3 minutes**, with the audio explaining how Token Factory
  and Nemotron are used.
  - The script outline is in `docs/PLAN.md` ("Demo guide"); fill it with real numbers only.
  - Put model names on screen whenever they're said, label sped-up footage ("16×"), and use
    1920×1080.
- **NVIDIA open model on Token Factory:** done (Nemotron 3 Ultra, Super, Nano). The README's
  "How we use Nemotron" table must be updated with final numbers from the spend ledger.
- **Built during the submission period:** state exactly what was built when.
  - GapFinder is new: its git history shows when it was built.
  - The RusKey reproduction is S's earlier research, used as a test case. The README's
    "Provenance" section says this; keep it accurate.
- **No illustrative numbers.** The original proposal (`docs/PLAN.md`, `docs/STRATEGY.pdf`)
  contains targets such as "38% gap to 4%" and "11 minutes". Add a line at the top of
  `docs/PLAN.md` saying its numbers are planning targets, not results, and make sure none of
  them appear in the README, video or Devpost text.
- **Devpost text:** follow the structure in `docs/PLAN.md` ("Devpost description"): inspiration,
  what it does, how it was built, evaluation, challenges, what's next. Every number must link
  to a file in `eval/results/` or `papers/ruskey/`.
- **Feedback form:** paste from [docs/FEEDBACK_SUBMISSION.md](docs/FEEDBACK_SUBMISSION.md),
  updated with anything new hit along the way.
- **Code freeze:**
  1. Tag `v1.0`; the Pages site rebuilds from main.
  2. Run the test set the second (and last) time on v1.0.
  3. Update the README numbers.
  4. Submit with a margin.

## P2. Only after everything above

- More paper types, more agents, more dashboard features.
- Live mode on hosted infrastructure (option C above).
- **Race replay for the video:** the baseline transcript and GapFinder's event log side by side,
  on the same clock, with both budget meters draining. Front-end only. First check that the
  baseline logs (`eval/baseline/logs/`, `eval/gapbench/runs/*/baseline-super/`) carry
  per-step timestamps; without them there is no shared clock.
- A README badge per paper (e.g. "2 claims: 1 unexplained, 1 reproduced") linking to the replay.

### Considered and rejected (don't redo these)

- **A sensitivity (tornado) chart from the 127-branch RusKey run.** That run used an outlier
  database load. Its load-stage settings were measured on different loads than the naive runs,
  and most settings have only 1-3 runs. A chart would make confounded numbers look precise. If
  a sensitivity map is wanted, build it from GapBench runs or from a new RusKey run with
  `--noise-setups`.
- **Claiming that anyone (e.g. Nebius staff) can re-run our branches from their checkpoint IDs.**
  The checkpoints live in our Sandboxes project, and other accounts probably can't fork them.
  Check first; until then, say "the command and checkpoint are recorded".
- **Fine-tuning a model, adding model tiers, or more paper types:** they spend credit and time on
  things judges weigh less than blind results.

---

## Reference: useful commands

```bash
pytest -q                                   # unit + integration (free)
pytest -m e2e tests/e2e                     # browser test of both sites (needs builds, see P1-2)
gapfinder ledger <paper.pdf> --repo <url-or-path> --out <dir>      # Ultra + Super, paid
gapfinder repomap <repo>                    # flags, defaults, file:line (free)
gapfinder search --spec <yaml> --targets <json> --assumptions <json> --claims <json> \
    --backend contree|local --max-runs N [--noise-setups K] [--resume <events.jsonl>] --out <dir>
python eval/gapbench/harness.py <task_dir> --arm <arm> --run <k> --cap 0.5 [--fresh]
python eval/gapbench/score.py --split dev|test --out eval/results/<file>.json
python eval/ledger_eval.py <ledger_run_dir> papers/ruskey --out eval/results/<file>.json
python eval/ablation_fork.py ...            # see its docstring
python eval/load_variance.py <run dirs...> --out eval/results/ruskey_load_variance.json
python scripts/export_static.py web/dist-static/data
```

Re-labelling a finished search from its recorded runs only, without any new run: pass
`--resume <its events.jsonl>` with `--max-runs` set to the number of recorded branches, and use
`--backend local` so nothing can reach Sandboxes.

## Done so far

- Claim ledger v5 on RusKey: precision 1.00 (in-sample), headline recall 1.00, all-claim recall
  0.93; setting recall 0.67 (below the bar).
- GapBench dev v5: GapFinder 4/4 with 0% false attribution, median $0.04 a task; the Super
  baseline 2/4 with 50%.
- RusKey Figure 6 end to end in Sandboxes (127 branches); fork vs no-fork ablation (-64% setup
  cost, -45% total).
- The setup reproducibility check found RusKey's load is not reproducible (12 loads, 12
  checkpoints), which corrected two earlier observations.
- No labels from unconfirmed runs; runs in flight are recorded when the budget stops; failing
  values aren't re-run; Nemotron 3 Super triages failed branches.
- Static replay site and Pages workflow (waits for the repo to go public and Pages to be
  enabled); structured feedback write-up; README with results and platform usage.
- An "Inconclusive" verdict (`--reproduce-tol`, default ±10%) and a bootstrap test that every
  confirmed effect must pass; GapBench dev v6 is still 4/4 with 0% false attribution.
- MC Dropout feasibility: the environment works in Sandboxes, but the cost blocked it there.
  Folder uploads now keep empty directories.
- `docs/PLAN.md` says its numbers are planning targets, not results.
- MC Dropout: local Docker decided (scaled, `T = 100`), feasibility go, answer key sealed,
  Energy chosen as the target (see P0-1 Status).
- GapBench tooling: sealed generator, PROTOCOL.md, category-aware scoring with Wilson intervals,
  trust matrix, dev v7 (`gapbench_dev_v7.json`); the random-search and evidence-off arms.
- Gap Report: five questions per card, effect sizes, provenance; the missing-sentence draft (off
  by default); `gapfinder spec-draft` code.
- Forked vs fresh-load comparability on RusKey: forked repeats are too narrow (FINDINGS.md).
- `scripts/try_it.py`: a free, keyless run of a dev task from `demo/cache/`.
