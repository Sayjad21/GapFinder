# M0 feasibility spikes

Each spike is a script that writes `eval/results/spikes/S<n>.json` and stays
in the repo as a smoke test. If its credentials are missing it exits with code 2
and prints `SKIP`.

| # | Script | Needs | What it decides |
|---|---|---|---|
| S1 | `s1_lifecycle.py` | Sandboxes | Chaining, branching, isolation, 40× concurrency, timeout, log download; records `nproc`/memory/disk speed |
| S2 | `s2_dedup.py` | Sandboxes | Whether identical commands re-execute (the `RUN_TAG` decision) |
| S3 | `s3_build_ruskey.py` | Sandboxes + source tarball | RusKey fork builds and loads; the loaded image fits in 12 GiB |
| S4 | `s4_noise.py` | S3's checkpoints in `.env` | CV ≤ 10% on the within-VM latency ratios the search targets |
| S5 | `s5_models.py` | Token Factory key | All four Nemotron tiers return valid JSON; real Ultra context limit; model IDs and base URL |
| S6 | `papers/ruskey/S6_gap_check.md` | — | RusKey has ≥ 2 claims off by more than 2× noise (draft says yes) |
| S7 | `s7_baseline.py` | Token Factory key (+ Sandboxes for the real pass) | mini-swe-agent completes one task in a sandbox; transcript saved |

## Run order

```bash
cp .env.example .env            # fill TOKEN_FACTORY_API_KEY, NEBIUS_API_KEY, NEBIUS_PROJECT_ID
python tests/spikes/s5_models.py                 # needs only the inference key
python tests/spikes/s7_baseline.py --backend local   # adapter check without Sandboxes
python tests/spikes/s1_lifecycle.py
python tests/spikes/s2_dedup.py
wsl -d Ubuntu-24.04 -u root -- bash scripts/pack_ruskey.sh /root/ruskey "/mnt/c/Users/Legion/Downloads/nvidia hackathon/gapfinder-repo/.gf_cache/ruskey_src.tar.gz"
python tests/spikes/s3_build_ruskey.py --tarball .gf_cache/ruskey_src.tar.gz --num-keys 2000000
# S3 prints GF_RUSKEY_SOURCE / GF_RUSKEY_BUILT / GF_RUSKEY_LOADED: paste them into .env
python tests/spikes/s4_noise.py
python tests/spikes/s7_baseline.py --backend contree
```

**Exit gate:** go if S1, S3 and S5 pass, and either S4 or its fallback works.
S6 decides whether RusKey is the live case. If S1 or S3 fails outright, stop
and rethink the plan.
