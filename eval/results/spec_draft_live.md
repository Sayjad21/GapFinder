# Live evaluation of `gapfinder spec-draft`

Run on 2026-10-13, local backend, Nemotron Super, `--compare` against the hand-written specs.
Drafted specs and reports: [spec_draft/](spec_draft/). Raw numbers: [spec_draft_live.json](spec_draft_live.json).

| artifact | smoke | attempts | tier | knob recall (found/missing/extra) | runs unedited | Nemotron cost |
|---|---|---|---|---|---|---|
| mlbench | pass | 2 | Super | 13/13, 0 missing, 1 extra (RUN_TAG) | yes | $0.0036 |
| rlbench | pass | 2 | Super | 14/14, 0 missing, 2 extra (RUN_TAG, RL_SEED_BASE) | yes | $0.0045 |
| MC Dropout | not run | | | | | |

- "Runs unedited" means `gapfinder fanout --spec <drafted>.yaml --knobs [{}] --noise 0 --backend local`
  produced 1/1 successful branches with the metrics parsed. It is a naive-run check, not a search.
- Both first drafts failed the smoke test and the second passed: mlbench on the Python launcher
  expression (`${PYTHON:-python3}` under Windows Git Bash), rlbench on an empty `RL_SEED_BASE` default.
  The redraft after the error fixed both. The Windows launcher failure is likely specific to this machine.
- Knob defaults matched the hand-written specs 13/13 and 14/14. Layers matched 13/13 and 11/14
  (rlbench `max_steps`, `seeds`, `eval_episodes` drafted as config, hand-written as workload).
- The extras are environment variables (run tag, seed base), not repo flags.
- MC Dropout was skipped: its repo is large and Docker-based. The "2 of 3" bar is therefore met only
  as 2 of the 2 artifacts tried; MC Dropout is untested.
- Caveat: mlbench and rlbench are small artifacts we built ourselves (single script, argparse flags).
  Results on real research repos may be worse.
- Cost: $0.0081 of Nemotron in total, no billed sandbox time.
