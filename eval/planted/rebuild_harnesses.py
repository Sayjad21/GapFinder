"""Phase B of the planted curriculum: each reproduced paper's harness rebuilt by `gapfinder harness` (no model call:
the recorded environment checkpoint is given), so its spec records per-epoch values (reporting-rule gaps), the
packages as of the paper's date (library gaps) and the paper-era commit (later-commit gaps).

    python eval/planted/rebuild_harnesses.py [--cases pygcn,vgae,...]

Writes eval/planted/curriculum/harness/<case>/ (HARNESS.md, spec.yaml, targets.json) and a summary line per case.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import curriculum as C  # noqa: E402

PAPERS = {  # case -> (repo, commit, arXiv id, ledger dir under eval/external)
    "pygcn": ("https://github.com/tkipf/pygcn", "1600b5b748b3976413d1e307540ccc62605b4d6d", "1609.02907", "devset/pygcn"),
    "fastgcn": ("https://github.com/matenure/FastGCN", None, "1801.10247", "blind-1"),
    "b3a": ("https://github.com/imtiazziko/Variational-Fair-Clustering", None, "1906.08207", "batch3/b3a"),
    "b3c": ("https://github.com/lss-1138/SparseTSF", None, "2405.00946", "batch3/b3c"),
    "b4a": ("https://github.com/hwwang55/RippleNet", None, "1803.03467", "batch4/b4a"),
    "vgae": ("https://github.com/tkipf/gae", None, "1611.07308", "devset/vgae"),
}


COMMANDS = {  # the one run that produces the target claim, from the hand harness (README parsing missed these)
    "pygcn": "cd pygcn && python train.py --no-cuda",
    "fastgcn": "python pubmed-original_transductive_FastGCN.py --dataset cora",
    "b3a": "python test_fair_clustering.py -d Synthetic --cluster_option kmeans --lmbda 10 --seed 0",
    "b3c": ("python -u run_longExp.py --is_training 1 --root_path ./dataset/ --data_path ETTh2.csv --model_id ETTh2_720_336 "
            "--model SparseTSF --data ETTh2 --features M --seq_len 720 --pred_len 336 --period_len 24 --enc_in 7 "
            "--train_epochs 30 --patience 5 --itr 1 --batch_size 256 --learning_rate 0.02 --num_workers 0"),
    "vgae": "cd gae && python train.py --model gcn_vae --dataset cora",
}


# the printed label of the target, where the claim's metric name and the program's differ (FastGCN prints accuracy;
# the paper's Table 5 calls it micro-F1, the same number on single-label data)
BINDS = {"fastgcn": "accuracy"}


def _commit(case_dir: Path) -> str | None:
    import re

    for name in ("case.json", "case.md"):
        p = case_dir / name
        if p.exists():
            m = re.search(r"\b[0-9a-f]{40}\b", p.read_text(encoding="utf-8", errors="replace"))
            if m:
                return m.group(0)
    return None


def rebuild(case: str) -> str:
    repo, commit, arxiv, led = PAPERS[case]
    d = C.EXT / led
    commit = commit or _commit(d)
    env = C.case_env(case)
    targets = json.loads((d / "targets.json").read_text(encoding="utf-8"))
    main = next(t for t in targets if not t.get("held_out"))
    # the hand harness named its claims (C_cora); the ledger numbers them: the claim with the same number, from the
    # raw (pre-grounding) claims, which the old grounding had thinned
    claims = json.loads((d / "ledger" / "raw" / "claims.json").read_text(encoding="utf-8"))
    pv = float(main["paper_value"])
    hits = [c for c in claims if c.get("reported_value") is not None
            and any(abs(float(c["reported_value"]) * f - pv) <= 1e-6 * max(1.0, abs(pv)) for f in (1, 100, 0.01))]
    if not hits:
        return f"{case}: no ledger claim reports {pv:g} (the target's number)"
    target = hits[0]["id"]
    out = C.HERE / "harness" / case
    out.mkdir(parents=True, exist_ok=True)
    ledger_file = out / "ledger.json"
    ledger_file.write_text(json.dumps({"paper": "", "claims": claims}, indent=1), encoding="utf-8")
    py = str(C.ROOT / ".venv" / "Scripts" / "python.exe") if os.name == "nt" else sys.executable
    cmd = [py, "-m", "gapfinder.cli", "harness", repo, "--commit", commit, "--local", env["GF_DEV_SOURCE"],
           "--ledger", str(ledger_file), "--target", target, "--env-checkpoint", env["GF_DEV_BASE"],
           "--arxiv", arxiv, "--repeats", "3", "--out", str(out)] + (["--command", COMMANDS[case]] if case in COMMANDS else []) + (
        ["--bind", f"{target}={BINDS[case]}"] if case in BINDS else [])
    with open(out / "harness.log", "w", encoding="utf-8") as f:
        rc = subprocess.call(cmd, cwd=str(C.ROOT), stdout=f, stderr=subprocess.STDOUT,
                             env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    tail = (out / "harness.log").read_text(encoding="utf-8", errors="replace").strip().splitlines()[-2:]
    return f"{case}: exit {rc}: {' | '.join(tail)[:300]}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", default=",".join(PAPERS))
    a = ap.parse_args()
    with ThreadPoolExecutor(6) as ex:
        for line in ex.map(rebuild, a.cases.split(",")):
            print(line, flush=True)


if __name__ == "__main__":
    main()
