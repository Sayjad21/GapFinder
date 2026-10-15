# A blind real-paper case: protocol (the most important missing evidence)

**Why.**
- Every result on a real paper so far is post-hoc. MC Dropout's answer key was revealed before v1.1 was
  built, and v1.1 to v1.3 were shaped by it.
- The sealed GapBench tests are blind, but synthetic.
- One blind real paper, with its answer sealed before GapFinder sees anything, is what would show the
  method generalises.

**Why it can't be done alone.** Whoever builds and tunes GapFinder must not know the answer. That rules
out Paragraph Vector (TODO P0-1 Candidate B): its documented cause is already written in TODO.md. A
second person (the *sealer*: a teammate, a friend, or a different AI model with no part in GapFinder)
picks the paper and writes the answer key.

## Roles

| Role | Who | Sees the answer? |
|---|---|---|
| Sealer | anyone who has not worked on GapFinder's search code | yes, and never shares it before the reveal |
| Runner | the GapFinder builder | no, until the reveal |

## Step 1: the sealer picks a paper and writes the answer key

1. **Choose a paper with an independently documented reproduction gap and public code.** The cause must
   be documented by someone else, not guessed. Good sources:
   - ML Reproducibility Challenge reports (`rescience` / OpenReview "MLRC" tracks), which often name
     the setting that explains a gap;
   - a follow-up paper or a GitHub issue thread where the authors confirm the cause;
   - an erratum or a later version of the paper that states a changed setting.
2. **Practical limits** (so it can run here):
   - Python code with command-line flags or a config file;
   - CPU-friendly at a reduced scale: minutes per run, not hours;
   - a reported number that a scaled run can approach.
3. **Write `answer_key.md`:**
   - the paper, and the claims (numbers) used as targets;
   - the documented cause, as exact settings and values or as an out-of-flag code difference;
   - the sources;
   - the scoring rule, pre-registered:
     - **correct:** the named settings match, exactly or inside an equivalence set of at most 3;
     - **partial:** a strict subset of the settings;
     - **diagnosed out of space:** when the documented cause is in code or data;
     - **confidently wrong:** a confident label on the wrong setting.
4. **Hash it:** `sha256sum answer_key.md > answer_key.sha256`.
   - Commit only the `.sha256` file plus a `case.md` that gives the paper's title, the arXiv link, the
     repository URL and the commit.
   - Keep `answer_key.md` private until the reveal.
   - **Don't say why the paper was chosen.**

## Step 2: the runner freezes GapFinder, then builds the inputs (without the answer)

1. Tag GapFinder (`git tag blind-1 && git push origin blind-1`) **before** reading the paper.
2. Build the inputs the normal way:
   - **Claim ledger:** `gapfinder ledger --paper <pdf> --repo <clone>` (Nemotron; about $0.3-1).
   - **Harness spec:** draft it with `gapfinder spec-draft`, and keep every flag the repo map finds
     exposed. A human confirms the build/run commands only. Knobs are never hand-picked toward a guess.
   - **Targets:** the claims named in `case.md`, one target and every other reported number of the
     same experiment as held-out claims (more claims mean more identifiability).
3. Run once, on Sandboxes or local Docker, with a pre-stated budget (e.g. `--max-runs 200`):

   ```
   gapfinder search --spec <spec> --targets <targets> --assumptions <ledger>/assumptions.json \
       --claims <ledger>/claim_ledger.json --backend contree --max-runs 200 --out eval/external/<case>/run
   ```

4. Commit the run unchanged, before the reveal.

## Step 3: the reveal

1. The sealer publishes `answer_key.md`.
2. Check `sha256sum -c answer_key.sha256`.
3. Score with the pre-registered rule, and write `RESULT.md`:
   - the verdict;
   - the label and the equivalence set;
   - the history-matching diagnosis and the code leads;
   - patch-knob results, if any;
   - cost.
4. Report it whatever the outcome. A miss on a blind real paper is as informative as a hit.

## What GapFinder must not do during a blind case

- No engine change between the tag and the reveal.
- No re-run because of the result (re-runs only for infrastructure failures, listed).
- No reading of reproduction reports about the chosen paper before the reveal.
