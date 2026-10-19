"""Deterministic pieces of the automatic harness (plan items 3-6, docs/CONTEXT_v11.md sections 4 and 7).

No model calls. Each piece proposes, and refuses rather than guesses when the evidence is ambiguous:
- `pick_commands`: the README's and shell scripts' experiment commands, ranked by how many of the claim's words
  (dataset, model, metric) appear in their arguments (item 3);
- `download_steps`: the repo's own data scripts (`download*.sh`, `get_data*`, `prepare*data*`) (item 4);
- `bind_metrics`: which printed number is which claim, from a smoke run's output (item 5). Test beats val and
  train; final beats best; a scale mismatch (0-1 against 0-100) is a mismatch; two equally good candidates are a
  refusal, not a choice. "Best" values are kept as extra metrics so a best-epoch protocol stays visible;
- `shrink_plan`: the fixed rule for fitting a Sandboxes operation (item 6): shards or segments first, shrinking
  only past the limit, with a discrepancy allowance recorded.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path

_STOP = {"the", "a", "of", "on", "in", "and", "for", "with", "ours", "our", "model", "method", "test", "result",
         "results", "table", "figure", "mean", "score", "dataset", "data"}


def claim_words(claim: dict) -> set[str]:
    """The words of a claim that should appear in the command that produces it (dataset, model, setting names)."""
    text = " ".join([str(claim.get("metric", ""))] + [str(v) for v in (claim.get("conditions") or {}).values()])
    words = set()
    for w in re.findall(r"[a-z][a-z0-9_-]*", text.lower()):
        words.add(w)
        words.update(p for p in re.split(r"[-_]", w) if len(p) >= 3)  # "book-crossing" also as "book", "crossing"
    return {w for w in words if w not in _STOP and len(w) >= 2}


@dataclass
class Command:
    cmd: str
    source: str  # README.md:12, scripts/run.sh:3
    score: int = 0
    matched: list[str] = field(default_factory=list)


_PY_CMD = re.compile(r"^[ \t>$]*((?:cd [\w./-]+ *(?:&&|;) *)?(?:python[23]?(?:\.\d+)?(?: +-[A-Za-z]+)* +(?!setup\.py\b)"
                     r"[\w./-]+\.py\b|(?:bash|sh) +[\w./-]+\.sh\b)[^\n`#]*)", re.M)


def _commands_in(path: Path, rel: str) -> list[Command]:
    text = path.read_text(encoding="utf-8", errors="replace")
    # join shell line continuations so a multi-line command is one command
    joined = re.sub(r"\\\r?\n\s*", " ", text)
    out = []
    for m in _PY_CMD.finditer(joined):
        line = joined[: m.start()].count("\n") + 1
        cmd = re.split(r"\s+\((?:or|e\.g\.|note|optional|see)\b", m.group(1), maxsplit=1)[0].strip().rstrip(";")
        out.append(Command(cmd, f"{rel}:{line}"))
    return out


def pick_commands(root: str | Path, claims: list[dict], limit: int = 5) -> list[Command]:
    """Experiment commands from the README and shell scripts, best match to the claims first."""
    root = Path(root)
    words = set().union(*(claim_words(c) for c in claims)) if claims else set()
    cands: list[Command] = []
    for p in sorted(root.glob("README*")) + sorted(root.rglob("*.sh")):
        if any(part.startswith(".") for part in p.relative_to(root).parts):
            continue
        cands += _commands_in(p, p.relative_to(root).as_posix())
    for c in cands:
        toks = set(re.findall(r"[a-z][a-z0-9_-]*", c.cmd.lower()))
        c.matched = sorted(w for w in words if w in toks or any(w in t for t in toks if len(w) >= 4))
        c.score = len(c.matched)
    seen, out = set(), []
    for c in sorted(cands, key=lambda c: (-c.score, c.source)):
        if c.cmd not in seen:
            seen.add(c.cmd)
            out.append(c)
    return out[:limit]


_DATA_SCRIPT = re.compile(r"(?i)^(download|get_data|get-data|fetch_data|prepare[_-]?data|setup_data|data_download)"
                          r"[\w.-]*\.(sh|py)$")


def download_steps(root: str | Path) -> list[str]:
    """Shell commands that run the repo's own data scripts, shallowest first."""
    root = Path(root)
    out = []
    for p in sorted(root.rglob("*"), key=lambda p: (len(p.parts), str(p))):
        if p.is_file() and _DATA_SCRIPT.match(p.name) and not any(x.startswith(".") for x in p.relative_to(root).parts):
            rel = p.relative_to(root)
            run = f"bash {p.name}" if p.suffix == ".sh" else f"python {p.name}"
            out.append(f"cd /work/{rel.parent.as_posix()} && {run}" if str(rel.parent) != "." else f"cd /work && {run}")
    return out


# ------------------------------------------------------------------------ metric binding

_METRIC_SYNONYMS = {
    "acc": {"acc", "accuracy", "top1", "top-1"}, "auc": {"auc", "roc", "rocauc", "roc_auc"},
    "f1": {"f1", "f-score", "fscore", "f_score", "f1score"}, "precision": {"precision", "prec"},
    "recall": {"recall", "rec"}, "mse": {"mse"}, "mae": {"mae"}, "rmse": {"rmse"}, "ndcg": {"ndcg"}, "hr": {"hr", "hit"},
    "map": {"map"}, "mrr": {"mrr"}, "loss": {"loss"}, "bleu": {"bleu"}, "ppl": {"ppl", "perplexity"},
}
_PAIR = re.compile(r"([A-Za-z][\w@./ -]{0,40}?)\s*[:=]\s*([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\s*(%?)")


def _family(label: str) -> str | None:
    toks = re.findall(r"[a-z0-9@]+", label.lower().replace("-", ""))
    for fam, syn in _METRIC_SYNONYMS.items():
        if any(t in syn or t.split("@")[0] in syn for t in toks):
            return fam
    return None


_QUAL = re.compile(r"(?i)\b(test|testing|val|valid|validation|dev|eval|train|training|best)\b")
_PREFIX = re.compile(r"(?i)^(?:epoch|step|iter|iteration|round|run|seed)\s*\d+\S*\s*")


def _qual_of(word: str) -> str:
    w = word.lower()
    return "test" if w.startswith("test") else "train" if w.startswith("train") else "best" if w == "best" else "val"


def labelled_numbers(log: str, tail_lines: int = 40) -> dict[str, float]:
    """(label -> last printed value) over the last lines of a run's output. A label takes the nearest test, val or
    train word before it on its line ("test auc: 0.65  acc: 0.62": the acc is test acc), and a line that says
    "best" marks its numbers as best ("End. Best Iteration 3: HR = 0.68": the best epoch, not the last)."""
    found: dict[str, float] = {}
    for line in log.splitlines()[-tail_lines:]:
        best = bool(re.search(r"(?i)\bbest\b", line))
        for m in _PAIR.finditer(line):
            raw = _PREFIX.sub("", " ".join(m.group(1).split()).strip(" -"))
            quals = [_qual_of(q.group(1)) for q in _QUAL.finditer(line[: m.end(1)]) if q.group(1).lower() != "best"]
            base = _QUAL.sub("", raw).strip(" -_:")
            if not base:
                continue
            key = " ".join(([("best")] if best else []) + ([quals[-1]] if quals else []) + [base])
            found[key] = float(m.group(2)) / (100 if m.group(3) else 1)
    return found


@dataclass
class Binding:
    claim_id: str
    label: str | None
    value: float | None = None
    scale: float = 1.0  # multiply the printed number by this to get the paper's unit (0-1 printed, % in the paper: 100)
    alternatives: list[str] = field(default_factory=list)
    refused: str = ""


def bind_metrics(log: str, claims: list[dict], tail_lines: int = 40) -> list[Binding]:
    """For each claim, the printed label that is its number: same metric family (accuracy, AUC, F1, NDCG@k, MSE,
    ...), test before unqualified before val before train, final before best, on the paper's scale (0-1 or %).
    Two equally good labels are a refusal, not a choice; the others are kept as alternatives (extra metrics)."""
    found = labelled_numbers(log, tail_lines)
    out = []
    for c in claims:
        fam = _family(str(c.get("metric", "")))
        k = re.search(r"@\s*(\d+)", str(c.get("metric", "")))
        paper = c.get("paper_value")
        cands = []
        for label, v in found.items():
            if fam is None or _family(label) != fam:
                continue
            if k and not re.search(rf"@\s*{k.group(1)}\b", label):
                continue
            words = label.split()
            q = next((w for w in words if w in ("test", "val", "train")), "")
            rank = {"test": 0, "": 1, "val": 2, "train": 3}[q]
            scale = 1.0
            if paper is not None and v:
                ratio = abs(float(paper)) / abs(v)
                scale = 100.0 if 30 < ratio < 300 else 0.01 if 0.003 < ratio < 0.03 else 1.0
            cands.append((rank, words[0] == "best", label, v, scale))
        if not cands:
            out.append(Binding(c["claim_id"], None, refused=f"no printed number looks like {c.get('metric')!r}"))
            continue
        cands.sort()
        top = [x for x in cands if (x[0], x[1]) == (cands[0][0], cands[0][1])]
        if len(top) > 1:
            out.append(Binding(c["claim_id"], None, alternatives=[x[2] for x in cands],
                               refused="several printed numbers fit equally well: " + ", ".join(x[2] for x in top)))
            continue
        _, _, label, v, scale = top[0]
        out.append(Binding(c["claim_id"], label, v, scale, alternatives=[x[2] for x in cands if x is not top[0]]))
    return out


# ------------------------------------------------------------------------ fitting the Sandbox

OPERATION_LIMIT_S = 3600


@dataclass
class ShrinkPlan:
    action: str  # "as is" | "shards" | "segments" | "shrink"
    factor: float = 1.0  # for "shrink": the fraction of the work kept (epochs, runs or folds)
    discrepancy: float | None = None
    note: str = ""


def shrink_plan(estimated_s: float, independent_jobs: int = 1, resumable: bool = False,
                budget_frac: float = 0.8) -> ShrinkPlan:
    """The fixed rule: run as is when it fits 80% of one operation; else split the cell into shards (independent
    jobs) or segments (resumable training); only then shrink, halving until it fits, and record a discrepancy
    allowance (0.05 as in the dev-set harnesses that were scaled down)."""
    limit = OPERATION_LIMIT_S * budget_frac
    if estimated_s <= limit:
        return ShrinkPlan("as is", note=f"about {estimated_s:.0f} s fits one operation")
    if independent_jobs > 1 and estimated_s / independent_jobs <= limit:
        return ShrinkPlan("shards", note=f"{independent_jobs} independent jobs of about {estimated_s / independent_jobs:.0f} s")
    if resumable:
        n = math.ceil(estimated_s / limit)
        return ShrinkPlan("segments", note=f"{n} resumable pieces of about {estimated_s / n:.0f} s")
    per = estimated_s / max(1, independent_jobs)
    factor = 1.0
    while per * factor > limit:
        factor /= 2
    return ShrinkPlan("shrink", factor=factor, discrepancy=0.05,
                      note=f"halved to {factor:g} of the work to fit; history matching allows 5% model discrepancy")


# ------------------------------------------------------------------------ before spending on a ledger

GPU_ONLY = {"flash_attn", "triton", "cupy", "apex", "deepspeed", "bitsandbytes", "xformers", "tensorrt", "pycuda",
            "megatron", "vllm"}
MAX_FILE_MB = 500


def compute_blockers(root: str | Path) -> list[str]:
    """Reasons a repo can't run on a CPU-only, 3.9 GB Sandboxes VM, found statically (plan item 9): imports of
    GPU-only packages, GPU-only requirements, and files larger than MAX_FILE_MB. An empty list is no guarantee."""
    import ast

    root = Path(root)
    out = []
    for p in sorted(root.rglob("*.py")):
        if any(x.startswith(".") for x in p.relative_to(root).parts):
            continue
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except (SyntaxError, ValueError):
            continue
        for n in ast.walk(tree):
            names = [a.name for a in n.names] if isinstance(n, ast.Import) else (
                [n.module] if isinstance(n, ast.ImportFrom) and n.module else [])
            for name in names:
                top = name.split(".")[0]
                if top in GPU_ONLY:
                    out.append(f"imports {top} ({p.relative_to(root).as_posix()}:{n.lineno})")
    for req in list(root.glob("requirements*.txt")) + list(root.glob("environment*.yml")):
        text = req.read_text(encoding="utf-8", errors="replace").lower()
        for pkg in sorted(GPU_ONLY):
            if re.search(rf"(?m)^\s*-?\s*{re.escape(pkg)}\b", text):
                out.append(f"requires {pkg} ({req.name})")
    for p in root.rglob("*"):
        if p.is_file() and p.stat().st_size > MAX_FILE_MB * 2**20:
            out.append(f"{p.relative_to(root).as_posix()} is {p.stat().st_size / 2**20:.0f} MB")
    return sorted(set(out))
