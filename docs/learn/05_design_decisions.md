# 5. Why it's built this way

Every big design choice in GapFinder answers one question: **how do we find real causes without fooling
ourselves?** This page explains the main choices in plain words, each with the reason behind it.

---

## "I don't know" is better than a confident wrong answer

**Choice:** GapFinder has many labels, and most of them are careful: Fits but unsupported, Inconclusive,
Unexplained. Only an answer that passes every check is "Explained".

**Why:** a researcher who reads "Explained: learning rate" will believe it and move on. If that's wrong,
we've done harm. A careful "I don't know, but here are the leads" is still useful. That's why safety
(being confidently wrong 0 times) is the number we report first.

## Run real experiments, don't just read

**Choice:** every answer comes from experiments that actually ran, and each can be replayed from its saved
checkpoint.

**Why:** an AI that only reads the paper and code can sound convincing and still be wrong. The general
coding agent we compared against did exactly that: confidently wrong in about half its runs. Experiments
are evidence. Reading is a guess.

## Change conditions, never the algorithm

**Choice:** GapFinder may only change settings: command-line flags, data choices, environment. A "diff
guard" blocks any edit to the code itself. Even patch knobs change numbers in memory only, and are
reported separately as code changes.

**Why:** if a tool may edit the algorithm, it can "fix" any gap by writing code that outputs the paper's
number. That explains nothing. Restricting changes to conditions keeps every answer meaningful.

## Fork from save points

**Choice:** build and load once, save checkpoints, and start every test from the right checkpoint.

**Why:** loading a database or a dataset can take a long time. On RusKey, forking needed 8 loads instead of
22 and cut the cost by about 45%. Checkpoints also make every result replayable.

## Measure the noise before believing anything

**Choice:** first run the defaults several times to see how much results vary. Any effect smaller than
that variation is treated as luck. Repeats are checked with a statistical test.

**Why:** machine-learning results wobble from run to run. Without this, GapFinder would "discover" causes
that are just noise. We even found that one paper's setup (RusKey) gives a different database each time it
is loaded, so GapFinder can widen its noise band to include that.

## Three independent checks before "Explained"

**Choice:** counterfactual (undo it and the gap must return), held-out claims (other numbers must not get
worse), and evidence (the authors must have plausibly used this value).

**Why:** each check catches a different kind of mistake.
- The counterfactual catches settings that came along for the ride.
- Held-out claims catch "fixes" that break something else, which is how GapFinder spotted that MC Dropout
  has a cause in the code.
- Evidence catches lucky fits.

## Prefer the simplest answer among equally good ones, and say when there are several

**Choice:** among answers that fit equally well, GapFinder picks the one with the fewest and smallest
changes, and lists the others as "equally good configurations".

**Why:** the paper's numbers often can't tell two answers apart. Pretending to know which one is right
would be dishonest. Listing them lets a person decide, maybe using information GapFinder doesn't have.

## Look at all the claims together

**Choice:** history matching scores every tested configuration against *all* the paper's claims at once.

**Why:** one number can be matched by many settings. Several numbers together are much harder to match,
so they reveal more. They also reveal when no setting can be the whole story ("out of space"). That
turned MC Dropout's bare "Unexplained" into a real diagnosis.

## Use AI for reading, plain code for counting

**Choice:**
- AI models read the paper, suggest assumptions and read error messages.
- Ordinary code does everything that must be exact: the repo map, candidate values, statistics,
  verification.

**Why:** AI is good at understanding text and bad at being reliably exact. Each part does what it's good
at. Every AI output that matters is checked: quotes must match the PDF, and code references must exist.

## Spend money only on purpose

**Choice:** a hard spending cap is checked before every AI call, every answer is cached, and there's a
separate guard on cloud costs. The free practice mode can't spend anything at all.

**Why:** the project had a small budget (about $50). We never wanted a bug to burn it. The whole project
cost about $29 of AI calls.

## Test honestly: sealed tests and pre-registration

**Choice:** see [how we test it](06_how_we_test_it.md).
1. The code is frozen first.
2. Only then are new test tasks generated, from a random seed.
3. Their answers are sealed until the run is finished.
4. The success criteria are written down before the test.

**Why:** if you tune a tool while looking at the test answers, the test measures nothing. We report the
results even when they fall short. v1.3 missed two of its four goals, and the README says so.

## Things we chose *not* to do, and why

| Idea | Why not |
|---|---|
| Let the AI edit the code to match the paper | it would "explain" everything and prove nothing |
| Trust the AI's suggested values alone | early versions never tried the right value. Code-derived values fixed that |
| Penalise values the paper doesn't mention | 45% of true causes were values only the code suggested |
| Penalise configurations that make results noisier | the true cause often makes results noisier too |
| Pair random seeds across experiments to reduce noise | we measured it: it didn't reduce noise on our artifacts |
| Call a large set of equally good answers "Inconclusive" | the top pick was still right more often than chance, so we keep it and show the set |

Next: [How we test it →](06_how_we_test_it.md)
