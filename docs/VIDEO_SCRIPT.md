# Video script and shot list

Target: 2:50 or shorter (the rule is under 3:00), public on YouTube, 1920x1080, audio that explains
how GapFinder uses Token Factory and Nemotron. This follows the "Demo guide" in
[docs/PLAN.md](PLAN.md) and replaces its bracketed numbers with the numbers the repo has. Every
number below names the file it comes from.

Two changes from the plan, on purpose:
- **Nano Omni is not in the script.** It is not served on Token Factory (feedback item 12), so
  GapFinder does not read figures. The plan's "Nano Omni reads the values off the figures" line would
  be false.
- **The "only a third of papers build in 30 minutes" statistic is out.** Nothing in the repo backs it.

The headline moments are the ones we can show with real data: a standard agent confidently wrong on a
task with no cause, the fork and the load-to-load noise on RusKey, a verdict of "Unexplained" with a
reason, and the blind-test counts.

## Before you record

- [ ] The numbers on screen match the final files. This script uses blind test **run 1**
  ([gapbench_test_v1_summary.json](../eval/results/gapbench_test_v1_summary.json)). If the second run
  on v1.0 is scored before you record, replace the scoreboard numbers in segment 7 with
  `[[V1.0: numbers from eval/results/gapbench_test_v2.json]]` and say that the second run was done
  on the frozen v1.0 tag. If it is not scored, say "run 1" out loud, as written.
- [ ] If someone other than Sayjad narrates, change "I'm Sayjad" and "my numbers" in segment 1.
- [ ] The public replay site loads logged out (see TEAM_HANDOFF.md, step a). Record from the public
  URL, not localhost, so the video shows what a judge sees.
- [ ] Hide notifications, bookmarks and any key in a terminal or the console. Browser zoom 125% or
  more. Do not open `.env`, the Nebius console or any page that shows the project ID.

## Script

About 330 spoken words (the placeholders count as words), about 2:35 at 130 words a minute, which
leaves room for pauses. The windows below add up to 2:52. Time each segment when you read it aloud.

### 1. 0:00 to 0:12, the founder story
- **On screen:** Sayjad on camera for 3 seconds, then Figure 6 of the RusKey paper next to the
  reproduction's numbers. Overlay, in red, the K10/K5 ratio: paper 1.48, our reproduction 0.92
  (median of 12 database loads; [ruskey_load_variance.json](../eval/results/ruskey_load_variance.json)).
- **Caption:** "RusKey, SIGMOD 2024, Figure 6".
- **Narration:** "I'm Sayjad, from BUET. For weeks I reproduced RusKey, a SIGMOD 2024 paper. My
  numbers don't match its Figure 6, and the paper doesn't say why."

### 2. 0:12 to 0:24, the idea
- **On screen:** the GapFinder title and the one-line tagline from the README, then a quick look at the
  Gap Report tab.
- **Narration:** "Everyone asks whether a paper reproduces. We ask why it doesn't. GapFinder runs
  controlled experiments to find the cause, and it says 'unexplained' when it can't."

### 3. 0:24 to 0:50, a standard agent on a task with no cause
- **On screen:** a condensed replay of the baseline's transcript (see "How to record: the baseline
  clip"). Show the commands scrolling, the repeated `RL_SEED_BASE=33` runs, and finally its answer
  naming `RL_SEED_BASE` as the cause. Shown at the speed it ran, with a 4x label if you speed it up.
- **Caption:** "Nemotron 3 Super · mini-swe-agent · dev task `dev-rl-nocause`, one run · same budget cap".
  Also in small text: "No setting explains this gap by design".
- **Narration:** "First, a standard coding agent on Nemotron 3 Super, with the same sandbox and the
  same budget. This task was built so that no setting explains the gap. The agent changed the random
  seed until the numbers moved, and reported seed 33 as the cause."
- **Source:** the run is in `eval/gapbench/runs/dev-rl-nocause/baseline-super/run1/` (prediction.json
  records 39 runs and the answer `RL_SEED_BASE=33`). It is the only run of that arm on that task. Say
  "one run" on screen; do not call it a median.

### 4. 0:50 to 1:14, reading the paper
- **On screen:** the RusKey claim ledger and the list of unstated settings (from
  `papers/ruskey/ledger_v5/`, shown as a scrolling file or the Gap Report's evidence lines). Highlight
  one quote and its source.
- **Caption (when each name is said):** "Nemotron 3 Ultra: claim ledger and assumptions" and
  "Nemotron 3 Super: result filter".
- **Narration:** "GapFinder starts by reading. Nemotron 3 Ultra turns the paper and the code into a
  claim ledger and a ranked list of unstated settings. Nemotron 3 Super filters the claims. Every
  quote has to match the PDF, or it's dropped."

### 5. 1:14 to 1:44, the fork and the noise
- **On screen:** the Replay tab at 16x on the RusKey run: one checkpoint fanning out, claim bars
  moving, weak branches greying out. Then the fork versus no-fork numbers from
  [ablation_ruskey.json](../eval/results/ablation_ruskey.json) as a two-column card: loads 8 vs 22,
  total cost $4.48 vs $8.07. Then a card: "5 identical loads, 5 different checkpoints".
- **Caption:** "16x" for the whole replay. Then "Token Factory Sandboxes". On the cost card:
  "Sandbox-reported cost, not billed in the Beta".
- **Narration:** "We build the program once, load the data once, and checkpoint it in Token Factory
  Sandboxes. Every hypothesis forks from that checkpoint. In a same-search test, forking needed 8 loads instead of 22, and cut the reported cost by
  45 percent. And five identical loads gave five different checkpoints, so GapFinder widens its noise
  band to match."

### 6. 1:44 to 2:12, verification and the verdict
- **On screen:** the Gap Report tab, RusKey run. Show the C5 card with the label "Unexplained", then
  the held-out claim line and the "Closest configurations" table. If time allows, a 3-second cut to
  the MC Dropout post-hoc report (`eval/external/mc-dropout/posthoc/run/gap_report.md`).
- **Caption:** "Unexplained" in the card's own colour. For MC Dropout: "External paper, documented
  cause, not blind".
- **Narration:** "Survivors are combined, then verified. Revert the change and the gap
  must come back. Held-out claims must not get worse. On RusKey, the setting that fixes two ratios
  breaks the third, so the verdict is Unexplained. On a paper with a documented cause, it found
  nothing and blamed nothing, and when we handed it the documented values, its checks rejected them."
- **Source:** [FINDINGS.md](../papers/ruskey/FINDINGS.md) (final-regime run) and
  [RESULT.md](../eval/external/mc-dropout/RESULT.md) (post-hoc diagnostic).

### 7. 2:12 to 2:39, the blind test
- **On screen:** the Scoreboard tab: the test-set table and the trust matrix for `gapfinder` and
  `baseline-super`. Highlight "false attribution" and the counts. End on a text card: "8 tasks. Not
  a proven win."
- **Caption:** "GapBench blind test, run 1: 8 tasks from a sealed generator, 3 runs each".
- **Narration:** "On eight blind tasks, GapFinder was confidently wrong in none of 24 runs. The standard agent was confidently wrong in 14 of 24. But GapFinder found the right
  cause in only four of the eight tasks in the median run, and versions that skipped its ranking found
  more. Eight tasks is small, so this is not a proven win."
- **Source:** [gapbench_test_v1_summary.json](../eval/results/gapbench_test_v1_summary.json):
  gapfinder 0 of 24 confidently wrong and 4 of 8 solved in the median run; baseline-super 14 of 24;
  gapfinder-random and gapfinder-noevidence 6 of 8.
- **If run 2 is final:** `[[V1.0: replace with the v1.0 numbers and say "on the frozen version"]]`.

### 8. 2:39 to 2:52, close
- **On screen:** the cost-per-tier table from the README ("How we use Nemotron on Token Factory", with
  "Nano: fallback log parser, exercised in a spike" in small text), then Sayjad on camera, then the
  repo URL and the demo URL on a plain card.
- **Caption:** "Ultra, Super, Nano" on the table. URLs: github.com/Sayjad21/GapFinder and
  sayjad21.github.io/GapFinder.
- **Narration:** "It's open source, every result is a replayable checkpoint, and the project's model
  calls cost [[V1.0: billed total in dollars from eval/results/spend_ledger.jsonl]]. Press 16x."

Word count check: run the counting command below on your edited narration.

```bash
python - <<'EOF'
import re
t = open("docs/VIDEO_SCRIPT.md", encoding="utf-8").read()
words = 0
for m in re.finditer(r"- \*\*Narration:\*\* \"(.*?)\"\n", t, re.S):
    words += len(m.group(1).split())
print(words, "narration words")
EOF
```

## Caption list (burned into the video)

Put the name on screen every time the voiceover says it.
- "Nemotron 3 Super" (segment 3, again in 4)
- "Nemotron 3 Ultra" (segment 4)
- "Token Factory Sandboxes" (segment 5)
- "16x" on every sped-up replay, and "4x" on any 4x clip; nothing sped up goes unlabelled
- "Sandbox-reported cost, not billed in the Beta" on any card with a Sandboxes dollar figure
- "8 tasks. Not a proven win." at the end of segment 7
- Add subtitles for the whole narration (YouTube auto-captions are not enough: check them).

## Shot list: what to record and how

Record every clip from a real run or the real site. Do not mock a screen.

Set up once: Windows 11, display at 1920x1080, browser at 125% zoom or more, full-screen window,
bookmarks bar hidden, notifications off (Focus assist), a clean browser profile. Use OBS Studio
(Display Capture, 1920x1080, 30 fps, MP4 or MKV) or the Windows Game Bar (Win+Alt+R). Record the
voiceover separately in a quiet room from the script above, then edit.

1. **Replay site, 16x (segments 2, 5).**
   - Open https://sayjad21.github.io/GapFinder/ logged out. It opens on the Replay tab.
   - In the run selector pick the RusKey run marked featured ("Figure 6, from the reproduction's final
     regime, in Token Factory Sandboxes"). It has 703 events.
   - Press 16x and record until the replay finishes; record a second take at 1x for a few seconds of
     the fork moment. Keep the "REPLAY, recorded <date>" badge in frame.
   - In the editor, add the "16x" label over the whole clip.
   - Local fallback if the public site is not up yet: `cd web && VITE_STATIC=1 npx vite build --outDir
     dist-static`, then `python scripts/export_static.py web/dist-static/data`, then
     `python -m http.server 8080 --directory web/dist-static` and open http://localhost:8080.
2. **Gap Report (segments 2, 6).**
   - Same site, Gap Report tab, same run. Scroll slowly through the cards. Stop on the C5 card
     ("Unexplained"), its held-out claim line and its "Closest configurations" table.
   - For the MC Dropout cut, open `eval/external/mc-dropout/posthoc/run/gap_report.md` in the editor or
     on GitHub, at the label line and the "closes this claim but makes held-out claims worse; rejected"
     line.
3. **Scoreboard and trust matrix (segment 7).**
   - Same site, Scoreboard tab, Test set section. Record the arms table (solved in the median run,
     false attribution) and scroll to the trust matrix for `gapfinder` and `baseline-super`.
   - The site reads the newest `gapbench_test*.json` in `eval/results/`. Before recording, check which
     file it shows (the heading names it). If it shows run 1, the narration matches. If a run 2 file
     was added and the site rebuilt, follow "Before you record".
4. **Terminal, `try_it.py` (use it in segment 2 or as a b-roll under segment 8).**
   - Git Bash, a dark theme, font 20 pt or more, window sized to fill the frame.
   - Run `python scripts/try_it.py` (16 to 20 s on the lead's machine, `dev-ml-threshold`; README "Quick start"). It prints the
     claim ledger step, the search and the Gap Report, and needs no `.env` and no network.
   - Record at real speed (no speed-up needed). Do not run it from a shell where keys are exported.
5. **Baseline transcript (segment 3).**
   - The agent's full transcript is `eval/gapbench/runs/dev-rl-nocause/baseline-super/run1/trajectory.json`.
     The raw file is too long to film, so print a condensed view and record that:
     ```bash
     python - <<'EOF'
     import json
     p = "eval/gapbench/runs/dev-rl-nocause/baseline-super/run1/trajectory.json"
     t = json.load(open(p))
     n = 0
     for m in t["messages"]:
         if m["role"] == "assistant" and m.get("extra") and m["extra"].get("actions"):
             n += 1
             print(n, m["extra"]["actions"][0]["command"][:150].replace("\n", " "))
     print()
     print(t["answer"]["attributions"][0])
     EOF
     ```
   - It lists the agent's 39 commands, the repeated `RL_SEED_BASE=33` runs near the end, and the answer
     it submitted. Scroll it at about 3x and label it "3x".
   - Read-only: do not re-run the baseline for the video, and do not touch `eval/gapbench/runs/`.
   - Honest choice rule (replaces the plan's "median of 5"): the dev set has one run per arm. Say
     "one run" on screen. If you prefer a median-run clip from the blind test instead, wait until
     the second test run is scored and the per-task rows are public; before then those rows are sealed.
6. **README and results files (segments 2, 4, 8).** Show the README's top block and its
   "How we use Nemotron on Token Factory" table (scrolled, not zoomed out). For segment 4 show a
   section of `papers/ruskey/ledger_v5/` with one quote.
7. **You on camera (segments 1 and 8).** A plain background, daylight, the voice recorded with the
   same microphone as the voiceover.

## After recording

1. Edit to 2:50 or shorter. Check the length in the exported file, not in the editor.
2. Watch the final cut once on a phone.
3. Upload to YouTube as **public** (not unlisted). Title: "GapFinder: why doesn't the paper
   reproduce?". Put the repo and demo URLs in the description.
4. Open the link in a logged-out browser (a private window) and check it plays and is under 3:00.
5. Put the URL into docs/DEVPOST.md (the `[[V1.0: YouTube URL...]]` placeholder) and into the
   Devpost form.
