# 10. Where every idea came from

GapFinder is mostly built from ideas that already worked somewhere else. This page lists every important
technique in the project, in plain words, with four questions answered for each:
- **Where is it from?** A published method (with its authors), an idea from another field, or our own design.
- **What does GapFinder do with it?**
- **Is it on in the current version (c5)?**
- **Did it help here?** Only what we actually measured. "Toy only" means it passes its own small test and
  nothing more is known.

A note on "ours": it means we found no published method that does the same thing. It is not a claim that
nobody ever had the idea. Where a code comment cites a source we did not check again, the table says so.

---

## A. Reading the paper

| Idea | Where it's from | What GapFinder does with it | On in c5? | Did it help here? |
|---|---|---|---|---|
| A **claim ledger** with exact quotes | ours | an AI model (Nemotron Ultra) lists every result the paper claims, each with a word-for-word quote; a second model (Super) drops non-results | yes | it is the input to everything; the blind GraphMAE mistake came from the reading step cutting off the appendix |
| **Numeric grounding** (a claim is kept only if its number is in its quote, page or table) | ours | numbers are matched in any spelling ("0.91", "91%") | yes | re-grounding the saved ledgers recovered about 350 claims that had been dropped, and dropped 0 new ones |
| **Table grids from the LaTeX source and the PDF**, checked cell by cell | "double entry" from accounting (two independent records must agree) | the paper's tables are read twice, from two sources, and only agreeing cells are trusted | yes | the source exists for about 93% of the papers we checked |
| **The appendix in its own reading** | a known failure of long-text reading (one long excerpt loses its end) | the appendix is read separately and merged | yes | built after GraphMAE's answer sat in an appendix table that was never read |
| **"As in [X]" setups fetched** | ours | when a paper says "we follow the setup of [X]", that setup is read too | yes | not measured separately |
| **Cheaper ledgers by cutting the paper** | considered, from cost-saving practice | measured, not built | no | output tokens are two thirds of the cost; cutting the input would save about 3%, so not worth it |

## B. Reading the code

| Idea | Where it's from | What GapFinder does with it | On in c5? | Did it help here? |
|---|---|---|---|---|
| **Repo map** (every flag, default and help text, without AI) | ordinary program analysis | argparse, gflags and absl flags; a commented-out block of settings is kept as an alternative | yes | the alternative block was RippleNet's real answer (lr and l2 together) |
| **Paper words to code flags**: BM25 search plus an ML word list | BM25 is a classic search-engine ranking (Robertson & Zaragoza) | "learning rate" in the paper is matched to `--lr`; then checked by what the value does at runtime, and by switching it off once (a "lesion", the neuroscience word for removing a part to see what changes) | yes | 86% right first guess on a 47-term test set; the decisive links 9 of 9 |
| **Runtime trace**: watch where each setting's value lands | the idea of following configuration values through a running program comes from systems research on misconfiguration (ConfAid, X-ray) | one short run records which value reaches the optimizer, a dropout layer, a loop length; each setting gets a role ("rate", "count", "fraction") | yes | found FastGCN's learning rate and epochs by watching them |
| **Static code checks** ("leads") | inspired by the literature on hidden choices in ML code, such as data leakage (Kapoor & Narayanan 2023) | hard-coded numbers that look like settings, fixed splits, selection loops that peek at test data | yes | MC Dropout's `batch_size = 128` lead; in c6, split sizes (`test_ratio`) were added as leads |
| **Paper numbers matched to code constants** (`matcher.py`) | ours | a number quoted from the paper and a constant with a similar name but a different value become a patch to test | yes | VGAE: the paper's 5% and 10% splits against the code's 30 and 20 |

## C. Deciding what to try

| Idea | Where it's from | What GapFinder does with it | On in c5? | Did it help here? |
|---|---|---|---|---|
| **A value ladder** around each default (×10, ÷10, ×2, ...) | ours (a coarse-to-fine grid, as in any parameter sweep) | values from the code itself, not only from the AI | yes | the true value was tried in 12 of 15 runs after it (v1.1), against rarely before |
| **The secant step** (estimate the crossing between two tried values) | the secant method, a classic way to find where a curve crosses a line | only when no tried value fits every claim | yes, guarded | it once manufactured wrong exact fits and cost 102 → 92 of 138 on the dev suite; the guard fixed that |
| **Roles from the trace** decide the values | ours | a "rate" gets ×10 steps, a "fraction" stays between 0 and 1, a seed is never tried | yes | fixed bugs where learning rates were treated as fractions |
| **Paper priors**: a value the paper states 0.9, a mentioned knob 0.6, an unmentioned one 0.4 | ours (hand-set weights) | break ties between equally good answers | yes | never measured on its own |
| **Priors from description length (MDL)** | Rissanen 1978 (minimum description length) | the same ordering with weights derived from how many alternatives the paper leaves open | **no** (built, off) | unmeasured: the planted tasks have no paper |

## D. Running the experiments

| Idea | Where it's from | What GapFinder does with it | On in c5? | Did it help here? |
|---|---|---|---|---|
| **Forking from saved checkpoints** | a feature of Token Factory Sandboxes, used like save points in a game | build and load once, start every test from the right checkpoint | yes | RusKey: 8 loads instead of 22, about 45% cheaper |
| **Measuring the noise first** (calibration) | standard experimental practice | the defaults run several times; a change smaller than the spread is treated as luck | yes | found that RusKey's database differs on every load |
| **A noise floor of 1% of the value** | ours (a safety margin) | a gap under 1% is called Reproduced, because real papers differ from our machines by small amounts | yes | kept on purpose after an outside review suggested removing it (see page 5) |
| **The diff guard** (no edit to the algorithm's code) | ours | a run may only write to allowed folders | yes | the rule that keeps every answer meaningful |
| **Patches in memory** (an import hook that edits the code as Python loads it, never the file) | ours; similar to how mutation-testing tools change code in memory | lets a hard-coded number, a function default or an operation be tested without touching the repo | yes | VGAE's split fractions, RippleNet's `np.mean` → `np.sum` |
| **Shards and segments** for jobs longer than the 3600-second limit | checkpoint and restart, a standard computing technique | independent jobs in parallel machines, or training resumed in pieces | yes | made long papers fit |
| **Memory-mapped large arrays** (copy-on-write) | an operating-system technique | arrays over 50 MB are shared, not copied, inside the 3.9 GB machines | yes | not measured on a paper yet |
| **The environment builder**, one install command at a time with rollback | Repo2Run (Hu et al. 2025) | an AI proposes one command; it is kept only if it worked | yes | ran unaided on about 2 of the last 6 unseen repositories |

## E. Searching for the cause

| Idea | Where it's from | What GapFinder does with it | On in c5? | Did it help here? |
|---|---|---|---|---|
| **Screen, confirm, combine, bisect, verify** | the overall shape of factor screening in experiment design | the backbone of the search | yes | see page 6 |
| **Racing**: repeats only for the best candidates | racing algorithms (Maron & Moore 1994, "Hoeffding races"; Birattari's F-race) | everyone gets 2 runs, then only the leaders get more | yes | kept the budget for combining |
| **Short screening runs** (multi-fidelity) | successive halving and Hyperband (Jamieson & Talwalkar 2016; Li et al. 2017) | long runs are screened at a quarter of their time first | yes | not measured on its own |
| **Bisecting a combination** (drop parts that don't matter) | delta debugging, ddmin (Zeller & Hildebrandt 2002) | removes settings that came along for the ride | yes | standard |
| **Escrow**: 25% of the budget kept for confirmation | ours | the best candidate always gets its repeats | yes | MC Dropout's documented pair was lost to the budget before it |
| **History matching** (every configuration against every claim; "implausibility" over 3 rules it out) | climate and oil-reservoir model calibration (Craig et al. 1997; Vernon et al. 2010); the 3-sigma rule is Pukelsheim's | finds whether any setting could explain all the claims ("in space") or none could ("out of space") | yes | turned MC Dropout's "Unexplained" into "look in the code"; a 5% model-discrepancy setting had silently blocked every real paper until it was set to 1% |
| **Model discrepancy** in the likelihood | Bayesian calibration of computer models (Kennedy & O'Hagan 2001) | an exact hit on one number can't beat a close fit on every number | yes | the "exact-hit guard" |
| **A differential diagnosis over six cause classes**, with "outside every class" as a real option | medical differential diagnosis, plus Bayesian model comparison | settings, reporting rules, library releases, code, data pipeline and "none of these" are scored against all the claims together | yes | lets the report say "probably the code" instead of naming a wrong setting |
| **Discriminating runs** for tied answers, chosen by expected information | Bayesian optimal experimental design for model discrimination (Box & Hill 1967; Lindley 1956) | runs at the conditions the paper reports, where the tied answers predict different numbers | yes | helps only when the paper reports such conditions |
| **Equally good configurations** listed, the simplest chosen | Occam's razor, plus the "equifinality" idea from hydrology (Beven & Binley 1992, GLUE) | the report shows every answer the numbers can't tell apart | yes | honest; does not raise the score |
| **"Not identifiable from the paper's numbers"** note | practical identifiability (profile likelihood; Raue et al. 2009; Liu, Maini & Baker 2025) | says when no reported number could separate the tied causes | yes | honest; does not raise the score |
| **Value intervals**: the range of values that fit, not one point | level-set estimation (Gotovos et al. 2013) and probabilistic bisection (Frazier, Henderson & Waeber 2019) | the answer's setting is bisected on both sides | yes | the scorer counts a planted value inside the range |
| **The minimum detectable effect** (Inconclusive when the gap is too small to detect) | statistical power analysis (Cohen) | uses a t-based formula with the measured spread | yes | correct abstentions on small gaps |
| **Common random numbers** (pair the random seeds of compared runs) | variance reduction in simulation | the j-th run of every configuration shares a seed | **no** (built, off) | on its toy it found the planted value 11 times against 13 without it, and once caused a confident mistake |
| **Sequential testing** (add repeats while the answer is unclear) | Wald's SPRT (1945); anytime-valid tests (Wang & Ramdas) | more repeats when a gap is between 1 and 3 MDE | **no** (built, off) | 12 against 13 on its toy: no gain |

## F. Causes outside the settings

| Idea | Where it's from | What GapFinder does with it | On in c5? | Did it help here? |
|---|---|---|---|---|
| **The scale probe**: "the paper's v is the code's c × v" | ours (a unit or counting convention between paper and code, found from a sweep the paper reports) | tries factors (×2, ÷2, ×10, ×0.01, +1 ...) that make every swept claim fit, then verifies by running | yes | the most reliable family: about 7 in 10 planted conventions found by c1. **Open defect:** trying several factors lets a wrong one fit by chance on noisy papers, and the confident label doesn't count how many were tried (seed 7) |
| **Reporting-rule probe** (the paper reported the best epoch, the best by validation, or the best of N seeds) | the ML evaluation literature on selection bias and reporting (Dodge et al. 2019, "Show your work") | read from the per-epoch values of runs already made, at zero cost | yes | 1 of 1 planted reporting rule found (both c3 and c5) |
| **Paper-year packages and the paper-era commit** as knobs | "time-travel" environments from software-repository mining, with delta debugging over packages and binary search over releases (git bisect) | the code and libraries as of the paper's date | yes | toy only: never plantable on our papers |
| **The patch round** (hard-coded literals tried in memory) | program repair: try a candidate fix and check it with the tests | the paper's numbers are the test | yes | VGAE found end to end |
| **Grounded operation swaps** (the paper says ELU, the code calls ReLU) | ours | the swap is tried only when the paper names the other operation | yes | toy |
| **Paper against trace** (an AI compares the paper's details with what the code did) | ours | proposes literal differences, each checked against the file, the line and the paper's sentence | yes, when a paper is given | VGAE |
| **The mutation round** (small edits: ×2, ÷2, mean ↔ sum, loop bounds, comparisons) | mutation-based fault localisation (MUSE, Moon et al. 2014; Metallaxis-FL, Papadakis & Le Traon 2015) | each edit is scored on every claim; a fit is a "code lead", never "Explained" | yes | the first planted code defect found (RippleNet `np.mean` → `np.sum`, c3); code overall 2 of 6 in c3 |
| **The metric's output slice** first (the code that computes the printed number) | thin slicing (Sridharan, Fink & Bodík 2007), from program slicing (Weiser 1981) | mutation sites are ranked by their distance from the line that prints the metric | yes | part of c3, the version that first found a code defect |
| **Group screening** of mutation sites | group testing (Dorfman 1943), sequential bifurcation (Bettonvil & Kleijnen 1997), probabilistic delta debugging (Wang et al. 2021) | many edits at once, split in half when the group moves the numbers | yes | toy only |
| **Interference control**: a mutant must move at least two claims that were off | the known problem of "interference" in mutation-based fault localisation (cited in the code as "FLIM 2025"; not re-checked) | stops an edit next to the output from "fixing" one number by force | yes | removed a confidently wrong path found on a toy |
| **Data-pipeline mutants** (`drop_last`, `shuffle`, split fractions, a scaler fit on all data) | ours, from common ML evaluation mistakes | the same in-memory edits for data loading | yes | PatchTST's real cause was `drop_last` |
| **Training data cut to a fraction** | DeepCrime's "remove training data" operator (Humbatova, Jahangirova & Tonella 2021) | an assignment to the training indices cut to 1/2 or 3/4 | yes | 1 of 4 independent planted cuts found (c5, seed 6) |
| **Operator classes take turns** after the first 6 mutants | operator-based mutant sampling (Zhang et al. 2013) | no class of edits can crowd out the others | yes | the first version (all mutants in turns) lost a planted constant (seed 5); keeping the first 6 in priority order fixed that |
| **A class scheduler** across cause classes | Bayesian search theory, used to find lost ships and planes (Koopman; Stone 1975) | up to 30% of the runs kept for code when no setting looks likely | yes | toy; part of the adopted c3 |
| **The early code screen** (cheap code tests before the settings use the budget) | value of information in sequential diagnosis (de Kleer & Williams 1987) | literal leads and the first mutants run right after the settings screen | yes | toy; part of c3 |
| **A model proposes code edits** when nothing fits | the pattern of Agentless (Xia et al. 2024) and LLM fault localisation (AutoFL): localise, propose, check by running | one cheap Super call on the executed code and the claims' ratios; at most 3 edits, each run like a patch | **no** (built, off by default) | no gain in three batches (seeds 5-7); it rarely triggers |

## G. Deciding what to say

| Idea | Where it's from | What GapFinder does with it | On in c5? | Did it help here? |
|---|---|---|---|---|
| **Three checks before "Explained"**: undo it (the gap must return), other numbers must not get worse, evidence the authors used it | counterfactual reasoning from causal inference; held-out checks from cross-validation; the evidence rule is ours | no confident label without all three | yes | without verification, 7 of 24 runs were confidently wrong on GapBench; with it, 0 |
| **A confident label must be earned** (a finished search, every setting tried, evidence beyond the code) | ours, after the GraphMAE mistake | anything less is "Fits but unsupported" | yes | nothing confidently wrong on real papers since it went in |
| **Code leads are never "Explained"** | ours | a code change that fits is reported as a lead to check | yes | keeps code fits from looking proven |
| **Protocol tests and the audit** | ML evaluation methodology (test-set selection, leakage) | every report lists protocol findings and held-out misses | yes | standard |

## H. Testing GapFinder itself

| Idea | Where it's from | What GapFinder does with it | Did it help? |
|---|---|---|---|
| **Sealed tests and pre-registration** | clinical trials and psychology's pre-registration; a hash published first is a commitment scheme from cryptography | the code is frozen, the success criteria are written down, then the tasks are made and their answers sealed | the only way the numbers mean anything |
| **GapBench**, a generator of small fake papers with one planted cause | ours | rejects tasks where another setting fits equally well | the main comparison against a coding agent (page 11) |
| **The dev suite** (every public task re-run for free) | regression testing | every change is checked against noise before it is kept | caught two regressions |
| **The planted-gap curriculum** (hidden changes in papers that already reproduce, graded from easy to hard) | fault injection and mutation testing, with DeepCrime's fault taxonomy, ordered like curriculum learning | the main development measurement since 2026-10-21 | showed which kinds of gap are found; also showed its own flaws (below) |
| **Controls** (tasks with nothing planted) | placebo controls from experiments | saying nothing is the right answer | 0 confident answers on 69 control searches |
| **Generator operators frozen at an old version** | ours, after a mistake | the engine is never tested on faults its own new operator generated | fixed the circular result of seed 5 |
| **A credible set and mean reciprocal rank** | the Top-k and MRR metrics of fault localisation | scores ties the claims can't break, apart from the main verdict | shows the cause in a small set more often in c5 |
| **The sign test** on tasks where two versions differ | standard statistics (also McNemar's test) | the only fair comparison of two versions on one batch | showed that none of our version comparisons was significant |

Next: [Compared with the state of the art →](11_versus_the_state_of_the_art.md)
