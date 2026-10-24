# 9. Glossary

Short definitions of every special word used in these pages, in alphabetical order.

| Word | Meaning |
|---|---|
| **Arm** | one version of the system in a test (e.g. GapFinder without verification), compared side by side |
| **Artifact** | the code published with a paper |
| **Assumption** | a setting the paper's result might depend on, with values to try and evidence |
| **Assumption space** | the full list of assumptions for one paper |
| **Backend** | where code runs: your computer (local), Docker, or cloud Sandboxes |
| **Balanced accuracy** | the average of "found the cause when there was one" and "blamed nothing when there was none"; always saying "Unexplained" scores 0.50 |
| **Baseline** | the comparison system: a general coding agent with the same AI model and budget |
| **Bisect** | removing the parts of a combination that aren't needed |
| **Bootstrap interval** | a statistical range for an effect; if it excludes zero, the effect is probably real |
| **Branch** | one experiment run, started from a checkpoint |
| **Calibration** | running the default settings several times to measure the noise |
| **Checkpoint** | a saved state of the experiment (built, loaded) that other runs start from |
| **Claim** | one result the paper reports, such as "Energy RMSE 1.66" |
| **Claim ledger** | the list of all claims from a paper, each with an exact quote |
| **Coarse rungs** | the first, big steps of the value ladder (×10, ÷10) |
| **Code lead** | a line in the code where a hidden cause could live (e.g. `batch_size = 128`) |
| **Combine** | trying pairs of settings together |
| **Confidently wrong** | a confident label on the wrong cause, the worst kind of error |
| **Confirm** | repeating a promising change to make sure it isn't luck |
| **Config flow** | following a setting through the code to see what it controls (e.g. epochx multiplies epochs) |
| **Counterfactual** | undo a change and check the gap comes back |
| **Coverage** | whether the right value is tried at all |
| **Dev suite** | re-running the search on all public tasks, to measure a change for free |
| **Diff guard** | the rule that blocks any edit to the algorithm's code |
| **Equally good configurations** | answers the paper's numbers can't tell apart |
| **Equifinality** | when several different causes produce the same result |
| **Escrow** | budget kept aside for confirming the best candidates |
| **Evidence check** | is there a quote in the paper or code showing the authors used this value? |
| **Fork** | starting a new experiment from a saved checkpoint instead of from scratch |
| **Forward step** | pairing the best setting with every value of the other top settings, to find interactions |
| **Gap** | the difference between what the code gives and what the paper reports |
| **GapBench** | our benchmark of small artificial papers with planted causes |
| **Gap Report** | GapFinder's output: one card per claim, with a label, proof and replay |
| **Harness spec** | a YAML file, approved by a person, saying how to build and run the code and what can change |
| **Held-out claim** | a paper number GapFinder must not make worse while fixing the main one |
| **History matching** | scoring every tested configuration against all claims at once; finds "out of space" causes |
| **Hypothesis** | one setting and one value to test |
| **Implausibility** | how unlikely the paper's number is under a configuration, counting noise; over 3 means ruled out |
| **In space / out of space** | whether some setting GapFinder can change could explain all the claims |
| **Inconclusive** | the measurements are too noisy to decide |
| **Interaction** | two settings that only matter together |
| **Knob** | a setting GapFinder may change (a flag, an environment variable, a data choice) |
| **Ladder** | the coarse-to-fine sequence of values tried around a default |
| **Likelihood** | how well a configuration's measured spread explains the paper's number; used to rank fits fairly |
| **Minimum detectable effect (MDE)** | the smallest gap the runs can reliably detect |
| **Nemotron** | the family of AI models GapFinder uses (Ultra, Super, Nano) |
| **Noise band** | how much a number varies between identical runs |
| **NROY** | "Not Ruled Out Yet": a configuration still consistent with a claim |
| **Occam's margin** | an extra setting must improve the fit by more than the noise, or it's dropped |
| **Patch knob** | a hard-coded number in the code, changed in memory for a test, without editing any file |
| **Pre-registration** | writing down the test plan and success criteria before running the test |
| **Racing** | giving repeats only to the best candidates, step by step |
| **Repo map** | the list of settings, defaults and file locations, read from the code without AI |
| **Reproduction gap** | when running a paper's code doesn't give the paper's numbers |
| **Router** | the one place every AI call goes through: cache, JSON repair, spending cap |
| **Sandbox** | a cloud machine where the code runs safely (Token Factory Sandboxes) |
| **Screen** | trying each candidate value once |
| **Sealed test** | a test whose tasks are made after the code is frozen and whose answers stay hidden until scoring |
| **Sign test** | a simple statistical test that counts how many tasks got better against how many got worse |
| **Static code checks** | reading the code, without running it, for hidden causes |
| **Token Factory** | the service that runs the Nemotron models and the Sandboxes |
| **Triage** | reading why a run failed and, if a value was rejected, trying a valid one |
| **Verification** | the three checks: counterfactual, held-out claims, evidence |

## Words added since the planted curriculum (2026-10-21 onwards)

| Word | Meaning |
|---|---|
| **c1 ... c6** | frozen versions of GapFinder (git tags `planted-c1` ... `planted-c6`); c5 is the current adopted one |
| **Cause class** | one kind of cause: setting, reporting rule, library or paper-era code, code defect, data pipeline, or "outside every class" |
| **Circular task** | a planted task made by the same operator the engine searches with; it tests the engine on its own faults, so it doesn't count |
| **Class scheduler** | the rule that keeps part of the budget for code tests when no setting looks likely |
| **Code lead** | a code edit or a line that could hold the cause; never labelled "Explained" |
| **Code proposer** | one cheap AI call that proposes at most 3 code edits when nothing fits; off by default |
| **Control** | a planted task with nothing planted; the right answer is to blame nothing |
| **Credible set** | the answer plus the configurations the claims can't tell apart from it; "in a credible set of at most 3" means the cause is among at most 3 |
| **DeepCrime** | a published set of fault types taken from real deep-learning bugs (removing training data, a bias, weight decay) |
| **Differential** | every candidate cause from every class, scored against all the claims together, like a doctor's list of possible diagnoses |
| **Discrimination** | runs chosen so that tied candidate answers predict different numbers |
| **Early code screen** | cheap code tests (top constants, first mutants) run right after the settings screen |
| **Family** | the kind of change the curriculum plants (setting, scale, code, data, reporting, ...) |
| **Fresh batch** | planted tasks made after the version being tested was frozen; the only fair test of it |
| **Group screening** | many code edits applied at once, the group split in half when it moves the numbers |
| **Identifiable** | the claims can tell the cause apart from every other candidate; "not identifiable" means they can't |
| **Interference control** | the rule that a code edit must move at least two claims that were off, so an edit next to the output can't "fix" one number by force |
| **Level (curriculum)** | how hard a planted task is: level 1 is a clear effect (at least 5 run-to-run spreads), level 2 subtle (3-5) |
| **MRR (mean reciprocal rank)** | 1 if the cause is the answer, 1/2 if it's second in the tied set, and so on, averaged |
| **Mutation round** | small edits to the code (×2, ÷2, mean ↔ sum, a loop bound, a data switch), each tested in memory on every claim |
| **Operator** | one kind of mutation edit (for example "swap mean and sum") |
| **Output slice** | the part of the code that computes the number the program prints; edits there are tried first |
| **Planted-gap curriculum** | the test bench of hidden changes in papers that already reproduce |
| **Reporting rule** | how the paper chose which number to report (the final epoch, the best epoch, the best seed) |
| **Scale probe** | the test for "the paper's v is the code's c × v": a unit or counting convention between paper and code |
| **Seed (curriculum)** | the number that decides which tasks a batch contains; a new seed makes a fresh batch |
| **Sign test** | counts the tasks where the new version won against those where it lost; it needs enough differing tasks to mean anything |
| **Structural switch** | a layer's on/off setting, such as `bias=True` or `affine=True` |
| **Training-data cut** | the paper trained on part of the data (a half, 40%, ...) |
| **Value interval** | the range of values of the answer's setting that fit every claim, not just one point |

Next: [Where the ideas came from →](10_where_the_ideas_came_from.md) · ← Back to [the start](README.md)
