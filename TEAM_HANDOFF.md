# Team handoff (written 2026-10-12, updated 2026-10-13 after both test runs were scored)

For the teammates who carry GapFinder to submission after the project lead's PC goes offline
(tomorrow night, 2026-10-13). The submission is due **2026-10-30**. Check the exact cut-off time and
time zone on the Devpost page and convert it to Dhaka time (UTC+6). Plan to submit around
**27 to 28 October**, so a broken upload costs nothing.

Read this file top to bottom once. Then work through section 3, steps a to h. Related files:
[TODO.md](TODO.md) (the full plan and rules), [SETUP.md](SETUP.md) (install),
[docs/DEVPOST.md](docs/DEVPOST.md), [docs/VIDEO_SCRIPT.md](docs/VIDEO_SCRIPT.md),
[docs/FEEDBACK_SUBMISSION.md](docs/FEEDBACK_SUBMISSION.md).

Rules that apply to everything below:
- **Never put keys, the Nebius project ID or anyone's email in a file, commit, issue, screenshot or
  chat.** Keys are shared privately only.
- **No AI-assistant attribution** in commits, code comments or pushed files. Commit under your own name.
- **Every number in the README, the video and Devpost must point to a file in the repo.** If a run fails,
  record the failure. Never claim a conclusive win from 8 tasks.
- **The generator tasks' sealed answers are public now** (`eval/gapbench/sealed/`, revealed after both
  test runs). Any AI-authored tasks are a new blind source: do not open their answers
  (`eval/gapbench/sealed-ai/`, any `answer.json` or the `hidden` field of a `test-ai-*` task) before
  they are scored. Whoever tunes GapFinder must not see them.

## 1. What is done

| Item | State | Where |
|---|---|---|
| GapFinder pipeline (claim ledger, assumption space, checkpoint tree, search, Gap Report) | done | [README](README.md), `gapfinder/` |
| RusKey Figure 6 end to end in Sandboxes: 127 branches from 13 loads, **Unexplained**; load not reproducible | done | [papers/ruskey/FINDINGS.md](papers/ruskey/FINDINGS.md) |
| Fork vs no-fork ablation (setup cost -64%, total -45%, reported cost) | done | [eval/results/ablation_ruskey.json](eval/results/ablation_ruskey.json) |
| GapBench-mini dev set: 4/4, no false attribution | done | [eval/results/gapbench_dev_v7.json](eval/results/gapbench_dev_v7.json) |
| GapBench blind test **run 1** (8 generator tasks, 5 arms, 3 runs each) | done, scored, per-task rows published | [eval/results/gapbench_test_v1.json](eval/results/gapbench_test_v1.json), [PROTOCOL.md](eval/gapbench/PROTOCOL.md) |
| GapBench blind test **run 2** on the frozen `v1.0` (same arms, runs 4 to 6) | done, scored, per-task rows published; sealed answers and seed revealed | [eval/results/gapbench_test_v2.json](eval/results/gapbench_test_v2.json), `eval/gapbench/sealed/` |
| Spend ledger snapshot | refreshed 2026-10-13 ($17.17 billed in total) | [eval/results/spend_ledger.jsonl](eval/results/spend_ledger.jsonl) |
| README, Devpost text and video script numbers | updated with both runs | [README](README.md), [docs/DEVPOST.md](docs/DEVPOST.md), [docs/VIDEO_SCRIPT.md](docs/VIDEO_SCRIPT.md) |
| MC Dropout external case (4 arms, confirmation runs, post-hoc diagnostic) | done, all arms Unexplained | [eval/external/mc-dropout/RESULT.md](eval/external/mc-dropout/RESULT.md) |
| Replay site code and the Pages workflow | done, **not yet deployed** (repo is private) | `web/`, [.github/workflows/pages.yml](.github/workflows/pages.yml) |
| Keyless try-it script (`scripts/try_it.py`) | done, not timed on a fresh clone | [README](README.md#quick-start-no-keys-free) |
| Feedback write-up (14 items) | done | [docs/FEEDBACK_SUBMISSION.md](docs/FEEDBACK_SUBMISSION.md) |
| Devpost text | drafted; two TODO placeholders left (YouTube URL, AI-author bullet) | [docs/DEVPOST.md](docs/DEVPOST.md) |
| Video script and shot list | drafted, not recorded | [docs/VIDEO_SCRIPT.md](docs/VIDEO_SCRIPT.md) |
| Git tags `pre-tasks-1`, `ext-eval-1`, `v1.0` | on `origin` | `git ls-remote --tags origin` |

**Blind test run 2 (frozen `v1.0`) is finished and scored.** The protocol says the test set is run
exactly twice, so there is no third generator run. Both result files have per-task rows, and the sealed
answers and the seed are committed. Run 2 notes (also in the PROTOCOL.md amendments): the first launch
failed because the sandbox guard refused every run (see section 3g), it was relaunched with
`GF_SANDBOX_GUARD_USD=20000`, and one `gapfinder-random` run hit a `BadJSONError` and is scored missed.
No GapFinder code changed between `v1.0` and the scoring (checked with `git diff v1.0 -- gapfinder
eval/baseline eval/gapbench/harness.py`).

Two `[[V1.0: ...]]` placeholders are left in docs/DEVPOST.md, both marked TODO: the YouTube URL and the
AI-author bullet. Search for them with `grep -rn "\[\[V1.0" docs/ TEAM_HANDOFF.md`. Each must be filled or
its sentence deleted before submission.

## 2. Before the lead goes offline (the lead's list)

These need the lead's machine or the lead's accounts. If any is not done by tomorrow night, tell the
team which one, because nobody else can do it.
1. [ ] **Push everything:** `git push origin main`. The tags are already on `origin`.
2. [x] **Run 2 finished and scored** (done 2026-10-13). The sealed folder is public in the repo, so
   teammates no longer need it from the lead's PC. Only an AI-author flow would need its own
   `sealed-ai/` folder (section 3e).
3. [x] **Spend ledger snapshot refreshed** (done 2026-10-13, committed; it holds only time, kind, cost,
   tag and token counts, no keys). Teammates copy it into their own `.gf_cache` (section 3g).
4. [ ] **Share the keys privately** with whoever will run paid work (Token Factory key, the Nebius
   project ID, the Tavily key). One person only, and say who in the chat.
5. [ ] **Share the model cache** if teammates will re-run anything: `.gf_cache/llm/` (no keys in it;
   it holds model answers about RusKey with short code quotes, so it is the lead's call).
6. [ ] **RusKey items from TODO.md "Getting RusKey"** if not done: tag the Sandboxes snapshot so it
   is not cleaned up, and back up the binary bundle privately. Never commit either.
7. [ ] **Nebius console:** confirm there is still no Sandboxes charge, auto top-up is off and a budget
   alert is set (TODO.md, "Money safety").
8. [ ] **Give a teammate admin rights on the GitHub repo**, or make it public now (step a). Making a
   repo public needs an admin.

## 3. What remains for humans

### a. Make the repo public and turn on GitHub Pages

The judges' replay site is a static build of the web UI. It only exists once these four things are done.
1. **Check the repo is safe to publish.** In Git Bash, from the repo root:
   - `git ls-files .env` must print nothing.
   - This must print nothing (it searches every commit's diff; it runs in a second):
     `git log --all --oneline -G "nvapi-[A-Za-z0-9_-]{8}|tvly-[A-Za-z0-9]{8}|(TOKEN_FACTORY_API_KEY|NEBIUS_API_KEY|TAVILY_API_KEY)=[A-Za-z0-9]" -- . ':!.env.example'`
   - Also search for the Nebius project ID, copied from the console into the command only (never into a
     file): `git log --all --oneline -S"<the id>"` must print nothing.
   - Personal emails: TODO.md (the "Commit identity" line) names a team member's university email, and
     commit author emails are in the git history. Making the repo public publishes both. Ask the person
     concerned whether that is fine before step 2. Editing TODO.md does not remove it from history.
   - Do not commit `.gf_cache/`, `runs/`, `eval/gapbench/sealed/` (before the reveal) or `.local/`.
2. **Make it public.** GitHub, repo `Sayjad21/GapFinder`, Settings, General, scroll to Danger Zone,
   Change visibility, Make public. This needs admin rights. The MIT license badge shows at the top of
   the README.
3. **Turn on Pages.** Settings, Pages, Build and deployment, Source: **GitHub Actions**.
4. **Run the workflow.** Actions tab, the `pages` workflow, Run workflow on `main`. Wait for the build and
   deploy jobs to go green (a few minutes). The deploy job fails until Pages is enabled, so if you
   ran it before step 3, run it again. The workflow also runs on every push to `main`.
5. **Check the site logged out.** Open https://sayjad21.github.io/GapFinder/ in a private window and check:
   - it opens on the Replay tab with a "REPLAY, recorded <date>" badge;
   - the run selector lists the RusKey runs, and pressing 16x plays the recording;
   - the Gap Report tab shows cards with labels, and the Scoreboard tab shows the test table and the
     trust matrix;
   - the README renders on the repo page with its images, and the License file is visible.
   If you get a 404, wait two minutes and check Settings, Pages for the published URL and the Actions log
   for the failing step.
6. After step 5, tell the team the site is up. The video (step b) is recorded from it.

### b. Record and upload the video

Follow [docs/VIDEO_SCRIPT.md](docs/VIDEO_SCRIPT.md): the script with timestamps, narration, captions,
and the shot list of what to record and how (the replay site at 16x, the Gap Report, the Scoreboard
trust matrix, the `try_it.py` terminal). Summary:
1. Decide whose voice it is and edit the "I'm Sayjad" lines if it is not him.
2. Run 2 is scored and segment 7 already has both runs' numbers. Check them against the Scoreboard
   tab before you record.
3. Record at 1920x1080, label sped-up clips (16x), put model names on screen when said.
4. Export at 2:50 or shorter. Upload to YouTube as **public**. Check it in a private window.
5. Put the URL in docs/DEVPOST.md (the `[[V1.0: TODO ... the public YouTube URL ...]]` placeholder) and commit.

### c. Paste the description into Devpost and submit (about 27 to 28 October)

1. Resolve the two remaining `[[V1.0: ...]]` placeholders in [docs/DEVPOST.md](docs/DEVPOST.md) (the
   YouTube URL, and the AI-author bullet: fill it from step e or delete it as the bullet says). Delete
   the HTML comment block at the top of the file.
2. Go to the hackathon's Devpost page and create or edit the project. Fill:
   - name GapFinder and the one-line tagline from the README;
   - the project story: paste everything under the `---` line of docs/DEVPOST.md (Markdown headings,
     lists and links; it has no tables on purpose);
   - gallery: `docs/img/report.png`, `docs/img/scoreboard.png`, `docs/img/replay.png`;
   - built with: Nemotron 3 Ultra, Nemotron 3 Super, Nemotron 3 Nano, Nebius Token Factory, Token
     Factory Sandboxes, Python, React, mini-swe-agent, Tavily;
   - links: the repo and the replay site; video: the YouTube URL;
   - track: Coding and Agentic Engineering;
   - if a team member attended a Builders & Brews event, select its city;
   - team members: add everyone.
3. Check the submission checklist in [docs/PLAN.md](docs/PLAN.md) (M6): repo public, license visible,
   demo URL works logged out and lands on replay, video public and under 3:00, description complete,
   feedback submitted.
4. Click Submit. Then open the project page in a private window and check the video, the links
   and the images.

### d. Paste the feedback form

Paste from [docs/FEEDBACK_SUBMISSION.md](docs/FEEDBACK_SUBMISSION.md), which has 14 items, each with
issue, steps, impact, suggestion and evidence. The form is linked from the hackathon page (the link is
not stored in this repo). If it asks for the fields one by one, copy each item's text into the matching
field. Ten $100 awards go to the most valuable feedback. Include only what is in the file: every item was
hit, except item 8, which says it was not.

### e. Optional: tasks from an independent AI author

This adds a second blind test source, reported separately from the generator tasks. It is only worth
doing if there is time before about 25 October. Rules are in TODO.md ("Source 2: an independent AI task
author"). In short:
- The author is a **coding agent from another vendor** with its own clone and a shell (not a chat window,
  and not a model used to build or tune GapFinder). It must run `make_task.py` and
  `leakage.py` itself.
- **GapFinder is frozen first.** The `v1.0` tag is the freeze. The author clones the repo at `v1.0`.
- Nobody on the team opens the AI tasks' answers before scoring. This needs its own sealed folder,
  `sealed-ai/`, because the generator's `sealed/` folder is public now. Wording everywhere: "tasks written by an independent AI model
  with no part in building GapFinder".

**Phase 1, the author writes and seals the tasks.**
1. Brief the author with [eval/gapbench/TEST_TASKS.md](eval/gapbench/TEST_TASKS.md), the category table in
   TODO.md section P0-2, the README, and this instruction: "Hide one cause per task so that GapFinder
   misses it if it can be fooled. Every task must still pass `make_task.py` and `leakage.py`. Name
   the tasks `test-ai-<name>` and set `split: test`."
2. For each task, the author follows TEST_TASKS.md, and then **moves the answers out of the task folder**,
   in the same layout the generator uses (compare the folder names under `eval/gapbench/tasks/test-gen-01/`
   and `eval/gapbench/sealed/test-gen-01/`; the generator's answers are public now, so you may open
   those as an example):
   - the task folder `eval/gapbench/tasks/test-ai-<name>/` keeps `paper.md`, `targets.json`,
     `calibration.json` and a `task.yaml` **without** the `hidden`, `category` and `type` fields;
   - a sealed folder `eval/gapbench/sealed-ai/test-ai-<name>/` gets `answer.json`, `calibration.json`
     and a `task.yaml` that holds the hidden fields.
3. The author commits the **task folders** in one commit, "Add AI-authored GapBench test tasks", and the
   hash of the sealed folder, but not the sealed folder:
   ```bash
   python - <<'EOF' > eval/gapbench/sealed-ai.sha256
   import sys
   sys.path.insert(0, "eval/gapbench")
   from pathlib import Path
   from gen_tasks import hash_tree
   print(hash_tree(Path("eval/gapbench/sealed-ai")))
   EOF
   ```
   Add `eval/gapbench/sealed-ai/` to `.gitignore` (same reason as `sealed/`).
4. The author hands the `sealed-ai/` folder to whoever scores, privately. The scorer copies it into place
   without opening it, and checks the hash with the same command (it must equal `sealed-ai.sha256`).

**Phase 2, run the arms.** Only `gapfinder` and `baseline-super`, 3 runs each, on the `v1.0` code. Use
run numbers 4 to 6, so that "runs 4 to 6" always means "the frozen v1.0 code", for every task.
1. Check the code is still v1.0:
   `git diff v1.0 --stat -- gapfinder eval/baseline eval/gapbench/harness.py` must print nothing.
2. Check the keys, cap and ledger (step g), then run. This calls Nemotron, so it costs money. Set
   `GF_SANDBOX_GUARD_USD=20000` or the guard refuses every GapFinder run (step g):
   ```bash
   export GF_SANDBOX_GUARD_USD=20000
   export GF_SPEND_TAG=test-ai-v1.0
   for t in eval/gapbench/tasks/test-ai-*; do
     for k in 4 5 6; do
       python eval/gapbench/harness.py "$t" --arm gapfinder --run $k --cap 0.5 --fresh
       python eval/gapbench/harness.py "$t" --arm baseline-super --run $k --cap 0.5 --steps 40
     done
   done
   ```
3. **Budget:** about $3.50 for 8 tasks, from run 2: gapfinder $1.47 plus baseline-super $1.95 for 24 runs
   each ([gapbench_test_v2.json](eval/results/gapbench_test_v2.json)), so roughly $0.43 per task for the
   two arms. Check `budget.spent_usd()` before and after (step g). Do not run the other three arms.
4. Do not open `eval/gapbench/sealed-ai/` or any task's `answer.json`.

**Phase 3, score and reveal.**
1. The scorer reads answers from one folder, so put both sources' answers in one scratch folder (it is
   under `runs/`, which is git-ignored):
   ```bash
   mkdir -p runs/answers_all
   cp -r eval/gapbench/sealed/test-gen-* runs/answers_all/     # public, in the repo
   cp -r eval/gapbench/sealed-ai/test-ai-* runs/answers_all/   # the AI author's, until scored
   ```
2. Score runs 4 to 6 (`--runs` picks run numbers; the output has a `by_source` entry per source,
   `generator` and `ai_author`):
   ```bash
   python eval/gapbench/score.py --split test --answers runs/answers_all --runs 4,5,6 --out runs/score_v1_0.json
   ```
   Only two arms (gapfinder, baseline-super) are run on the AI tasks, so the other three arms will have
   no rows for `test-ai-*`. Check how `score.py` reports that before you publish, and report each source
   separately. Do not overwrite `gapbench_test_v2.json`: if you publish the scored file, give it a new
   name (for example `eval/results/gapbench_test_v2_ai.json`).
   This re-runs each proposed configuration 3 times locally (free). If it stops with a
   missing-`answer.json` error, a task's answers are missing from `runs/answers_all`.
   I wrote this flow from reading `score.py`; no one has run it on AI tasks yet.
3. Report the two sources separately and together (PROTOCOL.md section 8). Add an entry to the
   "Amendments" section of [PROTOCOL.md](eval/gapbench/PROTOCOL.md): the AI-authored tasks were added
   after test run 1, run once on `v1.0` with two arms, and are reported separately.
4. After scoring, commit `sealed-ai/` too (remove it from `.gitignore` first), together with the
   scored file, as the generator's answers are published at the reveal (below).

**Scoring run 2 (the generator tasks, on `v1.0`) and the reveal: done 2026-10-13.** The scored files
are `eval/results/gapbench_test_v1.json` (runs 1 to 3) and `eval/results/gapbench_test_v2.json` (runs 4
to 6), both made with `score.py --split test --answers eval/gapbench/sealed --runs <list> --out <file>`.
`eval/gapbench/sealed/` and its seed are committed, and the folder's hash equals
`eval/gapbench/sealed.sha256` (check it with `hash_tree`, as in the AI flow above). The PROTOCOL.md
amendments list the code changes between run 1 and `v1.0`, the failed first attempt and the `BadJSONError`
miss. The README, Devpost text and video script carry both runs' numbers.

### f. Optional: Candidate B and the RusKey positive control

Both are in TODO.md. Neither is needed for the submission. Do them only with the lead's OK.
- **Candidate B, Paragraph Vector on IMDB (TODO P0-1):** a second external case with a documented
  cause. The steps are the ones MC Dropout followed (feasibility, sealed answer key, freeze, run the
  four arms, reveal), and the answer key must be written by someone who will not tune GapFinder. The
  MC Dropout run took days of wall time, so allow for that. Pre-register before running.
- **RusKey positive control (TODO "Positive control on RusKey"):** plant a setting, drawn at random
  by a script written before the draw, and see whether GapFinder finds it. `papers/ruskey/gen_control.py`
  does not exist yet and must be written first. It needs Sandboxes work (`--backend contree`,
  `--noise-setups 5`), the lead's OK, and `GF_SANDBOX_GUARD_USD` raised (step g). The RusKey source
  stays private; the built snapshot is enough (TODO "Getting RusKey").

### g. Money and keys

- **The Token Factory credit is about $50 for the whole project, and only Nemotron inference is billed.**
  The README's billed total is $17.17 (2026-10-13, from the refreshed ledger): each blind test run cost
  about $7.5, the MC Dropout ledgers about $0.28 and everything before that about $1.9. The Nebius
  console is the only shared source of truth, so look there before any run that costs more than $1.
- **`GF_SPEND_CAP_USD`** in `.env` is a hard cap on billed spend, checked before every call, per machine.
  TODO.md says 11, which was written before the two test runs, so the lead has raised it. Do not raise
  it again without the lead's OK.
- **Sandboxes are not billed in the Beta**, according to the Nebius console (no Sandboxes charge on
  2026-10-08, and none for 6 to 12 October, see
  [FROZEN.md](eval/external/mc-dropout/FROZEN.md) Deviation 2). The `cost` the API reports is about
  $0.01 per CPU-second, is diagnostic, and is still counted by our guard.
- **`GF_SANDBOX_GUARD_USD=20000` is needed for any GapFinder run, including GapBench.** The default is
  60, and the reported Sandboxes total is far over that ($2,665.07 in the ledger; the MC Dropout runs
  alone reported $2,495.31: arms 3 and 4, the confirmation runs and the post-hoc diagnostic). Without it,
  every GapFinder run is refused, local backend included: that is how the first launch of test run 2
  failed. The `cost` field is diagnostic and is not billed in the Beta. Ask the lead before any new
  Sandboxes run, and check the console for a Sandboxes charge first. Also set `GF_SANDBOX_CPU_LIMIT_S` (default
  300) only for runs that need more CPU time per process.
- **One machine does paid or Sandboxes work at a time.** Each machine keeps its own ledger, so they cannot
  see each other's spending. On a new machine, copy the snapshot first, or the guards count from $0:
  `mkdir -p .gf_cache && cp eval/results/spend_ledger.jsonl .gf_cache/spend.jsonl`.
  (The snapshot was refreshed on 2026-10-13.)
- Tag every paid experiment (`GF_SPEND_TAG=<name>`). Check spend any time:
  `python -c "from gapfinder.models import budget; print(budget.spent_usd(), budget.sandbox_reported_usd())"`.
- `GF_CACHE_ONLY=1` reuses cached model answers and refuses to call the API on a miss, so re-runs are
  free. `scripts/try_it.py` sets it itself.
- Keys live in `.env` (git-ignored). `scripts/check_env.py` checks them without spending anything.

### h. How to run anything

Install from [SETUP.md](SETUP.md) (Python 3.11, uv, Git for Windows). Windows notes:
- Use **`python -m gapfinder.cli`** instead of `gapfinder`: the `gapfinder.exe` launcher may be missing
  in the venv. Example:
  `python -m gapfinder.cli fanout --spec eval/toy/hidden_knob.yaml --knobs eval/toy/knobs.json --backend local`.
  Use the venv's Python: `.venv/Scripts/python` in Git Bash (or activate the venv).
- Run **pytest from Git Bash**, not PowerShell or cmd: `.venv/Scripts/python -m pytest -q`. The
  integration tests call tools from Git's `usr/bin`. The count has grown since TODO.md's "97"; the
  MC Dropout record shows 237 passing at one point. Free, no keys.
- If `uv pip install` fails with `failed to open file ...WHEEL`, set `UV_CACHE_DIR` to a fresh folder and
  `UV_LINK_MODE=copy`.
- Try it without keys: `python scripts/try_it.py` (a dev task, 16 to 20 s). Nobody has timed a fresh clone
  yet; the plan's bar is 15 minutes including the install. If you have a clean machine, time it and
  write the number in the README.
- Web UI: `npm --prefix web ci && npm --prefix web run build`, then
  `.venv/Scripts/python -m uvicorn gapfinder.api.server:app --port 8000`.
- Other commands are in TODO.md, "Reference: useful commands".

## 4. README fixes after run 2 (done 2026-10-13)

The README was updated on 2026-10-13: the status block, the Results table (both test runs, with a
per-arm table), "How we use Nemotron on Token Factory" with the $17.17 total, the Sandboxes reported
total ($2,665.07, diagnostic and not billed) and the "Honest limitations" line about the test set. If
the AI-author tasks are run, add their row to the Results table and update the limitation that says
there is no result from them.

## 5. What's next for the product

After the submission. Each comes from something we saw, with its file.
- **Candidate values derived from the paper's own numbers.** The MC Dropout search never tried
  `epochx=10` because the ledger read the paper's "10x more iterations" as unstated, and the generic grid
  started at 250 ([RESULT.md](eval/external/mc-dropout/RESULT.md)). A phrase like "10x" should become
  `epochx=10`.
- **Wider generic grids**, so the random-order search can reach values far from the defaults (arm 4's
  lowest `epochx` was 250; the paper's is 10).
- **A label for "explains the target but conflicts with a held-out claim".** Today the documented
  `epochx=10 hidden=1` ends as Unexplained, because it fixes Energy and breaks Yacht. A separate label
  would say exactly that, instead of staying silent.
- **Cross-operation sharding for Sandboxes.** An operation is capped at 3,600 s wall time. We shard a
  cell over the VM's 4 cores, but cells such as `n_splits=20` still time out (5 of 22 runs in arm 3).
  Splitting one experiment over several operations would fix that
  ([FROZEN.md](eval/external/mc-dropout/FROZEN.md), Deviation 3).
- **Setting recall on RusKey is 0.67, below our 0.80 bar** (the tuner's mode flags are missed,
  [ledger_ruskey_v5.json](eval/results/ledger_ruskey_v5.json)): improve the repo map or assumption prompt
  in general, and measure it on the external paper too.
- Evaluate `gapfinder spec-draft` live against the hand-written specs, and time a fresh clone of `try_it.py`.
- A second external case where the cause is hidden from us, a RusKey positive control, and, longer term,
  artifact-evaluation committees as users.
