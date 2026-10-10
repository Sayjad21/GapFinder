# TODO: make GapFinder trustworthy (renewed 2026-10-10)

**Goal:** show that GapFinder finds real causes on problems it did not create, says
"Unexplained" or "Inconclusive" when it should, and beats an ordinary agent given the same tools.
Make the evidence the product. No new agents, dashboards or model tiers until the P0 items are done.

**Deadline:** Devpost says submissions close **2026-10-30**. Confirm the exact time and time zone
on the Devpost page, and convert it to Dhaka time (UTC+6).

**Owners:** S = Sayjad, T = Tawhid, G = GapFinder development (done in this repo).
Account and key setup is finished; that checklist is now [docs/ACCOUNT_SETUP.md](docs/ACCOUNT_SETUP.md).

---

## P0-1. Blind test on a real, independently documented reproduction gap

The strongest evidence we can add: a paper we didn't build, whose gap someone else already
diagnosed.

**Candidate A: MC Dropout** (Gal & Ghahramani, ICML 2016, UCI regression, Table 1)
- Repo: https://github.com/yaringal/DropoutUncertaintyExps
- The author's README documents that results change with training length and depth. The current
  defaults (`--epochx 500`, `--hidden 2`) differ from the paper (40 epochs, 1 hidden layer).
- Caveats:
  - A second cause (BayesOpt replaced by grid search) is a code change GapFinder can't test, so
    the best possible result is partial.
  - The defaults are very slow.
  - It needs 2018-era Theano 0.8.2 and Keras 2.2.0.
- Not fully blind: the operator (G) already knows the documented cause. Report it as
  "semi-blind" and rely on the safeguards below.

**Candidate B (backup): Paragraph Vector on IMDB** (Le & Mikolov 2014; cause documented by
Mesnil, Mikolov et al. 2015). The cause is hierarchical softmax plus unshuffled data. Slower,
15-25 min per run, and the paper's 92.6% may not reappear.

Steps:
- [ ] **G: Feasibility check on Candidate A**, at no Nemotron cost. Check:
  - whether the old software installs in a sandbox (Python 3.6 image? network for pip?);
  - how long one small run takes;
  - whether the repo's defaults give numbers clearly different from the paper's.
  - Stop and report if any of these fail.
- [ ] **G: Seal the answer before running.** Write the documented cause, its sources and the
  scoring rule into `eval/external/<case>/answer_key.md`. Commit only its SHA-256 hash first,
  then reveal the file after the run. Anyone can then check it wasn't changed afterwards.
- [ ] **G: Freeze the system.** Tag the commit (e.g. `ext-eval-1`) and record the model IDs,
  prompt hashes and budget. No GapFinder changes for this paper.
- [ ] **G: Build the harness spec from GapFinder's own repo map** (all flags it finds), not by
  hand-picking the answer's flags. Commit the spec before the run.
- [ ] **G: Run once and record everything**, including a wrong attribution or "Unexplained".
- [ ] **G: Reveal and score.** A matching name alone doesn't count: re-run the predicted
  setting and confirm it actually moves the result.
  - Report the documented cause as "documented", not "proven", unless our runs confirm the
    effect.
  - Score partial credit, e.g. found the epochs but not the depth.
- [ ] **T: A truly blind second case.** T picks a paper and seals its answer; G never sees it
  until scoring.
- [ ] **G: Positive control on RusKey** (needs S's OK: about $5-10 of reported, unbilled sandbox
  cost, which is above our $60 guard).
  - T secretly changes one setting and records the "paper" numbers from that run.
  - GapFinder must name the change.
  - This tests whether GapFinder can find a real cause on the real system at all, which tells us
    how much RusKey's "Unexplained" is worth.

## P0-2. Hidden GapBench test tasks (T)

- [ ] **T: Write the 8 hidden tasks**, chosen without optimising them for the current
  implementation. Cover these categories:

| Category | What it tests |
|---|---|
| Known cause, one detectable setting | Can it find the cause? |
| Known cause, interacting settings | Can it handle two variables that only matter together? |
| No supported explanation | Does it correctly abstain? |
| Several plausible causes | Does it pick the true one over look-alikes? |
| Measurement noise only | Does it avoid calling random variation a cause? |
| Incomplete paper or artifact | Does it say its evidence is insufficient? |

- [ ] **G: Pre-register the scoring rule** in `eval/gapbench/PROTOCOL.md` before the test set is
  run: what counts as correct, partial, confidently wrong, a correct abstention, or a miss.
- [ ] **G: Run all arms once in M4, and once more on the frozen v1.0. No more than that.**
- [ ] **G: Report raw counts with uncertainty**, not just accuracy. For each arm:
  - correct attributions, confident wrong answers, correct abstentions, missed causes;
  - experiments used, wall time, cost;
  - with 8 tasks, a 95% interval (e.g. Wilson) on each rate.
  - Never claim a statistically conclusive win from 8 tasks.
- [ ] **G: Run GapFinder 3 times per task** (the artifacts are noisy), and report how often its
  answer changes between runs.

## P0-3. Noise as a first-class feature

Partly done: noise bands from repeats, more repeats for noisy metrics, `--noise-setups` with the
reproducibility check, and no labels from unconfirmed runs.
- [ ] **G: Add an "Inconclusive" verdict.** Use it when the noise band is so wide that the paper's
  value can't be told apart from a clearly different one. RusKey C5b now says "Reproduced" inside
  a ±16% band, which overstates it.
- [ ] **G: A significance test for effects**, alongside the 2×MAD rule:
  - a bootstrap confidence interval on (candidate − naive);
  - nothing counts as an effect unless the interval excludes zero.
- [ ] **G: Turn the setup check on by default** for artifacts that have a load or build stage
  (`noise_setups=3`). Do it only after measuring what it costs on GapBench and RusKey.
- [ ] **G: Report effect sizes with their uncertainty** in the Gap Report, not only "gap before
  → after".

## P1-1. A fair baseline comparison

- [ ] **G: Equal budgets, written down:**
  - the same model, paper, repo and sandbox tools;
  - the same run and dollar caps;
  - the same sealed answer key.
- [ ] **G: Give the baseline the same evidence** (paper text, repo map) and the same tools,
  except the capability being tested.
- [ ] **G: Random-search arm.** The same hypothesis space and budget, with random order and no
  ledger ranking. This shows whether the ranking adds anything.
- [ ] **G: Ultra baseline arm** (needs S's OK on cost; probably under $2).
- [ ] **G: Ablations in one table:** no-fork (done for RusKey), no-verification (exists),
  random search, and no evidence gate.

## P1-2. The Gap Report answers five questions at the top of each card

- [ ] **What did the paper report?** The claim, its quote and its page.
- [ ] **What did we measure?** The naive value, its repeats and spread, and the discrepancy.
- [ ] **Which experiment changed it?** The branch, command, config and output, as a link.
- [ ] **Why do we believe it?** Reversal test, held-out claims, independent evidence.
- [ ] **What remains unknown?** Untested assumptions, settings too large to test, alternative
  explanations, and setup reproducibility.
- [ ] Clearly separate **confirmed cause** (all checks pass), **plausible explanation** (fits,
  unsupported) and **interacting factors**.
- [ ] **Provenance on every report:** GapFinder commit, model IDs, prompt hashes, spec hash,
  and cost (Nemotron and sandbox).

## P1-3. Smarter search, but only if it measurably helps

- [ ] **G: Adaptive ranking**, done as an experiment rather than a feature:
  - update hypothesis priors from screen results;
  - spend repeats on the most promising first;
  - keep it only if it beats the current search on runs-to-answer against the random-search
    arm.
- [ ] **G: Improve setting recall** from 67% toward the 80% bar (the RusKey tuner's mode flags are
  missed). Measure on the external paper too, so this isn't tuned to RusKey.

## P1-4. Submission requirements (official rules)

- [ ] **Working app:** replay site live on GitHub Pages. S: make the repo public near the
  deadline, then Settings → Pages → Source: GitHub Actions.
- [ ] **Public repo** with the MIT license visible, setup instructions, and a test build.
- [ ] **Video:** public, under 3 minutes, with the audio explaining Token Factory and Nemotron
  usage. S records it; G writes the script from real numbers only.
- [ ] **NVIDIA open model on Token Factory:** done, Nemotron 3 Ultra, Super and Nano.
- [ ] **Built during the submission period:** the README must say exactly what was built when.
  GapFinder is new (git history from 2026-10-04); the RusKey reproduction is S's earlier work,
  used as a test case.
- [ ] **No illustrative numbers anywhere** (the old "38% to 4%", "11 minutes" targets): every
  number in the README, video and Devpost text must have a log behind it.
- [ ] **Feedback form:** from [docs/FEEDBACK_SUBMISSION.md](docs/FEEDBACK_SUBMISSION.md).
- [ ] **Code freeze:** tag v1.0, deploy that tag, final eval on it, then submit with a margin.

## P2. Only after everything above

- More paper types, more agents, more dashboard features, live mode on hosted infrastructure.

---

## Done so far (2026-10-04 to 2026-10-10)

- Claim ledger v5 on RusKey: precision 1.00, headline recall 1.00; setting recall 0.67 is below
  the bar.
- GapBench dev: GapFinder 4/4 with 0% false attribution; baseline 2/4 with 50%.
- RusKey Figure 6 end to end in Sandboxes; fork vs no-fork ablation (-64% setup cost).
- The setup-reproducibility check found that RusKey's database load is not reproducible.
- No labels from unconfirmed runs; in-flight runs are recorded when the budget runs out;
  Super triages failed branches.
- Static replay site (waits for Pages to be enabled); structured feedback write-up.
