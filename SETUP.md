# Team setup

How to get GapFinder running on your own machine. You don't need the RusKey
source code for any of it. See "What needs RusKey" below.

## 1. Install (about 5 minutes)

You need Python 3.11+, git and [uv](https://docs.astral.sh/uv/). On Windows,
also install Git for Windows: the local sandbox backend runs commands through
its bash.

```bash
git clone https://github.com/Sayjad21/GapFinder.git
cd GapFinder
uv venv --python 3.11 .venv
uv pip install --python .venv -e ".[dev,baseline]"
```

Windows: if `uv pip install` fails with `failed to open file ...WHEEL`, set
`UV_CACHE_DIR` to a fresh folder and `UV_LINK_MODE=copy`, then retry.

Windows: run `pytest` from Git Bash, not from PowerShell or cmd. The integration tests call
tools from Git's `usr/bin` (for example `head`), which only Git Bash puts on `PATH`.

Check that everything works. No keys needed, and it costs nothing:

```bash
.venv/bin/pytest -q                  # Windows: .venv\Scripts\pytest -q
.venv/bin/gapfinder fanout --spec eval/toy/hidden_knob.yaml --knobs eval/toy/knobs.json --backend local
```

To see a full investigation without any keys, run `python scripts/try_it.py`. It replays
recorded model answers from `demo/cache/` and runs the experiments locally (see "Try it
yourself" in the README).

## Browser (e2e) tests, optional

`pytest -m e2e tests/e2e` drives both sites in a headless browser. Set it up once:

```bash
uv pip install --python .venv playwright
.venv/bin/python -m playwright install chromium
npm --prefix web ci && npm --prefix web run build                  # web/dist, for the API site
(cd web && VITE_STATIC=1 npx vite build --outDir dist-static)      # the server-free site
.venv/bin/python scripts/export_static.py web/dist-static/data     # its data files
```

A test is skipped, not failed, when its build is missing.

## 2. Get the paper (free)

Papers aren't committed. Download the exact arXiv version the gold set was
checked against:

```bash
.venv/bin/python scripts/fetch_paper.py
```

## 3. Keys (only for work that calls models or sandboxes)

We share **one Token Factory account with about $50 in total**. Ask Sayjad for
the keys privately. Never commit them, and don't paste them in issues or chats.

```bash
cp .env.example .env      # then fill in the keys you were given
```

Handing over from another machine:
- Copy the spend-ledger snapshot first, or the guards count from $0:
  `mkdir -p .gf_cache && cp eval/results/spend_ledger.jsonl .gf_cache/spend.jsonl`.
- Only one machine does paid or sandbox work at a time. Each machine keeps its own ledger, so
  they can't see each other's spending. See TODO.md, "Handing over to another machine".

Budget rules:
- `GF_SPEND_CAP_USD` is a hard cap, but it's **per machine**: each checkout
  keeps its own ledger in `.gf_cache/spend.jsonl`. Keep yours at `2` unless
  agreed otherwise. The Token Factory console balance is the only
  shared truth, so check it before any big run.
- Re-runs of anything already computed should use `GF_CACHE_ONLY=1`. It refuses
  to call the API on a cache miss.
- Say in the team chat before any run expected to cost more than $1.

Verify the keys (free):

```bash
.venv/bin/python scripts/check_env.py
```

## What needs RusKey, and what doesn't

| Work | Needs RusKey source? | How |
|---|---|---|
| Search logic, Gap Report, UI, GapBench-mini, baseline | No | Toy artifact + local backend |
| RusKey claim ledger and assumptions | No | Frozen results in `papers/ruskey/ledger_v5/`, signed-off gold sets in `papers/ruskey/` |
| RusKey sandbox experiments | No | Fork from the prebuilt snapshot in our Nebius project: `--adopt source=98e3e854-cf02-43c0-8cd2-5d5423de247a --adopt built=98e3e854-cf02-43c0-8cd2-5d5423de247a`, with `GF_RUSKEY_SOURCE` set to the same ID in `.env` (see TODO.md, "Getting RusKey") |
| Building RusKey into a sandbox (spike S3) | Yes | Sayjad runs it, from his machine |
| Re-running the RusKey ledger from scratch | Yes | Sayjad runs it |

## Contributing

- Branch from `main` and open a pull request; don't push to `main` directly.
- Run `pytest -q` before pushing.
- Commits use your own name and email. Don't add AI co-author trailers or
  "generated with" lines to commit messages or PR descriptions.
