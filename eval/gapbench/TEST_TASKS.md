# Writing the GapBench-mini test tasks

**Who:** someone who does *not* tune GapFinder's prompts or search settings.
The plan's honesty rule is that the person tuning never sees the test answer
keys. The dev tasks (`tasks/dev-*`) are for tuning; the test tasks are touched
exactly twice: once in M4 and once on the frozen v1.0.

## What to write

**8 test tasks:** 4 on `rlbench` / `mlbench` now, plus 4 on RocksDB `db_bench`
once Sandboxes access works. The plan asks for this type mix across all 12
tasks (4 dev + 8 test):

| Type | Total wanted | Already in dev |
|---|---|---|
| `single_unstated`: the paper never mentions the knob | 4 | 1 |
| `stated_code_differs`: the paper states a value, the code default differs | 4 | 1 |
| `interaction`: two knobs, neither enough alone | 3 | 1 |
| `no_cause`: nothing in the artifact explains the gap | 1 | 1 |

So the test set needs about: 3 single_unstated, 3 stated_code_differs,
2 interaction, 0 no_cause (add one more no_cause if you can make it clean).

## How

1. Copy a dev task folder as a template:
   `cp -r eval/gapbench/tasks/dev-ml-normalize eval/gapbench/tasks/test-<short-name>`
2. Edit `task.yaml`: set `id`, `split: test`, `type`, `hidden` (the answer),
   the `claims`, and write the mini-paper in `paper`. Delete the copied
   `paper.md`, `targets.json`, `answer.json` and `calibration.json`.
3. Explore knob effects first. Each run is free and takes about a second:
   `cd eval/gapbench/artifacts/mlbench && python train.py --normalize zscore`
4. Generate it: `python eval/gapbench/make_task.py eval/gapbench/tasks/test-<name>`.
   It rejects the task if the gap is under 3 noise bands. Then make the change
   bigger, or pick another knob.
5. Run `python eval/gapbench/leakage.py`. It must print `0 leaks`.

## Rules for a fair task

- The paper must be a believable setup section. State every knob you aren't
  testing, so it reads like a real paper.
- **single_unstated:** the hidden knob and its value appear nowhere in the
  paper or the artifact (the leakage script checks this).
- **stated_code_differs:** the paper states the hidden value in plain words,
  e.g. "decays as 0.1/(1+t/50)", ideally not as the literal flag value.
- **interaction:** check that each knob alone does *not* close the gap; run
  both alone with `make_task.py`-style repeats before committing.
- **no_cause:** use `offset`. Make sure no single knob reproduces both claims
  (use a held-out claim moving the other way, as `dev-rl-nocause` does).
- Don't add comments or files to the shared artifacts that hint at answers.
  If a task needs repo evidence (an authors' script with the real flag), say
  so in `task.yaml` and tell the team, because it changes what's fair.

## Keeping the keys away from the tuner

- Commit test tasks in **one commit** titled `Add GapBench test tasks`, and
  tell Sayjad not to open `tasks/test-*/answer.json` or `task.yaml`.
- Prompt or search changes after that point are suspect. Note them in the
  commit message, so a judge can see whether any tuning followed the test run.
