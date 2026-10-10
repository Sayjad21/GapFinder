"""Write the freeze record (FROZEN.md) for the MC Dropout external case.

    .venv/Scripts/python scripts/freeze_record.py --tag ext-eval-1 \\
        --out eval/external/mc-dropout/FROZEN.md --max-runs 40 --budget-usd 5

Run it at tag time, on a clean checkout, before the first search. It records: the git commit GapFinder
will run from (and the tag to create), the model IDs from the config, the sha256 of every prompt
(`gapfinder.report.provenance.prompt_hashes`), the sha256 of the harness spec, the targets, the cell
script, the Dockerfile and the sealed answer key's hash, the pre-registered arms with their exact
commands, and the run and dollar budget. It never reads the answer key itself, only the committed
`answer_key.sha256`. It doesn't create the tag or commit anything.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gapfinder.config import tiers  # noqa: E402
from gapfinder.report.provenance import git_state, prompt_hashes  # noqa: E402
from gapfinder.search.engine import SearchConfig  # noqa: E402

DEFAULT_CANDIDATES = SearchConfig().candidates_per_knob  # the product default, unchanged for this case

CASE = Path("eval/external/mc-dropout")
C = CASE.as_posix()  # for text: always forward slashes

# arm name -> (what changes, what it shows, extra `gapfinder search` flags, ledger directory)
ARMS = [
    ("normal", "nothing", "the product as is", "", "runs/mcd-ledger"),
    ("evidence off", "the evidence check is skipped; a closing value is at most 'Fits but unsupported'",
     "the experiments alone carry the verdict", "--no-evidence-gate", "runs/mcd-ledger"),
    ("no README",
     "the ledger runs on a clone with README*, readme* and docs/ removed (scripts/strip_docs.py), "
     "and the evidence check is off",
     "the cause was found without the documentation", "--no-evidence-gate", "runs/mcd-ledger-nodocs"),
    ("all flags, random",
     "hypotheses are every knob of the harness spec with generated candidate values, uniform priors, no "
     "paper values, no ledger; random order",
     "the ranking is not what found it", "--hypotheses repomap --rank random --seed {seed}", None),
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def docker_image_id(image: str = "gf-mcdropout") -> str | None:
    try:
        out = subprocess.run(["docker", "image", "inspect", image, "--format", "{{.Id}}"], capture_output=True,
                             text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 and out.stdout.strip() else None


def arm_command(name: str, flags: str, ledger: str | None, *, max_runs: int, budget_usd: float, seed: int,
                candidates_per_knob: int) -> str:
    slug = name.replace(" ", "-").replace(",", "")
    parts = ["GF_SPEND_TAG=ext-mcd", "GF_MAX_CONCURRENCY=6", "gapfinder search",
             f"--spec {C}/mcd.yaml", f"--targets {C}/targets_mcd.json"]
    if ledger:
        parts += [f"--assumptions {ledger}/assumptions.json", f"--claims {ledger}/claim_ledger.json"]
    if flags:
        parts.append(flags.format(seed=seed))
    parts += ["--backend local", f"--max-runs {max_runs}", f"--candidates-per-knob {candidates_per_knob}",
              f"--cap {budget_usd:g}", f"--out {C}/run-{slug}"]
    return " ".join(parts)


def build_record(*, tag: str, max_runs: int, budget_usd: float, seed: int, root: Path, allow_dirty: bool,
                 candidates_per_knob: int = DEFAULT_CANDIDATES) -> str:
    state = git_state()
    if not state["commit"]:
        raise SystemExit("not a git checkout: the freeze must name a commit")
    if state["dirty"] and not allow_dirty:
        raise SystemExit("the working tree has uncommitted changes; commit them first, then freeze")
    case = root / CASE
    files = {
        f"{C}/mcd.yaml": case / "mcd.yaml",
        f"{C}/targets_mcd.json": case / "targets_mcd.json",
        f"{C}/harness/run_cell.sh": case / "harness" / "run_cell.sh",
        f"{C}/docker/Dockerfile": case / "docker" / "Dockerfile",
        f"{C}/answer_key.sha256": case / "answer_key.sha256",
    }
    missing = [name for name, p in files.items() if not p.is_file()]
    if missing:
        raise SystemExit("missing: " + ", ".join(missing))

    lines = [f"# Freeze record: MC Dropout external case ({tag})", "",
             f"Written {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())} by `scripts/freeze_record.py`, "
             "before any GapFinder search on this case. Nothing below may change until the case is scored.", "",
             "No GapFinder code, prompt, spec or target changes for this case after this record. If something "
             "blocks a run (a crash, a missing parser), fix only that, and describe the fix in RESULT.md.", "",
             "## Code", "",
             f"- GapFinder commit: `{state['commit']}`" + ("  (working tree was dirty)" if state["dirty"] else ""),
             f"- Tag to create on that commit: `git tag {tag} {state['commit'][:12]} && git push origin {tag}`", "",
             "## Models (from the config; environment overrides are applied)", "",
             "| Tier | Model ID |", "|---|---|"]
    lines += [f"| {name} | `{t.model_id}` |" for name, t in tiers().items()]
    lines += ["", "## Prompts (sha256)", "", "| Prompt | sha256 |", "|---|---|"]
    lines += [f"| {n} | `{h}` |" for n, h in sorted(prompt_hashes().items())]
    lines += ["", "## Inputs (sha256)", "", "| File | sha256 |", "|---|---|"]
    lines += [f"| `{name}` | `{sha256_file(p)}` |" for name, p in files.items()]
    image = docker_image_id()
    lines += ["", f"- Docker image `gf-mcdropout`: {'`' + image + '`' if image else 'not built on this machine'}",
              "- Artifact: Gal & Ghahramani's DropoutUncertaintyExps at the commit pinned in the Dockerfile, "
              "with the one documented patch `T = 10000` to `T = 100`.", "",
             "## Budget", "",
             f"- Branch runs per search: `--max-runs {max_runs}` (each arm gets the same).",
             f"- Dollar cap per search (Nemotron, billed): `--cap {budget_usd:g}`. The runs are local Docker "
             "cells, so there is no sandbox cost; ledger extraction is separate, about $0.10-0.30 of Ultra "
             "per run (one for the normal and evidence-off arms, one on the stripped clone).",
             f"- Values tried per knob in the screen: `--candidates-per-knob {candidates_per_knob}` (every arm).",
             f"- Seed for the random arm: `{seed}`.", "",
             "## Arms (pre-registered)", "",
             "All arms use the same spec, targets, budget and build. Energy RMSE is the target claim; Yacht "
             "RMSE is held out. Concrete is not searched.", "",
             "| Arm | What changes | What it shows |", "|---|---|---|"]
    lines += [f"| {n} | {what} | {shows} |" for n, what, shows, _, _ in ARMS]
    lines += ["", "Commands (after the ledgers exist; see TODO P0-1 Step 4):", "", "```bash"]
    lines += [arm_command(n, flags, ledger, max_runs=max_runs, budget_usd=budget_usd, seed=seed,
                          candidates_per_knob=candidates_per_knob)
              for n, _, _, flags, ledger in ARMS]
    lines += ["```", "",
              "Ledger inputs:", "",
              "```bash",
              f"gapfinder ledger <paper.pdf> --repo <clone> --out runs/mcd-ledger",
              f"python scripts/strip_docs.py <clone> <clone>-nodocs",
              f"gapfinder ledger <paper.pdf> --repo <clone>-nodocs --out runs/mcd-ledger-nodocs",
              "```", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tag", required=True, help="the git tag the freeze will carry, e.g. ext-eval-1")
    ap.add_argument("--out", required=True, help="where to write FROZEN.md")
    ap.add_argument("--max-runs", type=int, required=True, help="branch-run budget per search")
    ap.add_argument("--budget-usd", type=float, required=True, help="dollar cap per search (Nemotron, billed)")
    ap.add_argument("--seed", type=int, default=0, help="seed of the random arm")
    ap.add_argument("--candidates-per-knob", type=int, default=DEFAULT_CANDIDATES,
                    help="values tried per knob in the screen, recorded for every arm (default: the product's)")
    ap.add_argument("--allow-dirty", action="store_true", help="record a dirty working tree anyway (for tests)")
    args = ap.parse_args(argv)
    text = build_record(tag=args.tag, max_runs=args.max_runs, budget_usd=args.budget_usd, seed=args.seed,
                        root=ROOT, allow_dirty=args.allow_dirty, candidates_per_knob=args.candidates_per_knob)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
