"""Assumption space (Ultra): setup section + repo map + relevant files -> ranked Assumption[]."""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import BaseModel

from gapfinder.ingest.pdf import PaperText
from gapfinder.ingest.repo_map import RepoMap
from gapfinder.ledger.grounding import Grounder, GroundingReport
from gapfinder.ledger.schemas import Assumption, AssumptionStatus, Claim
from gapfinder.models.router import Router

ASSUMPTION_PROMPT = """You are enumerating the experimental assumptions behind a paper's results,
so that a reproduction gap can be searched knob by knob.

An assumption is any experimental condition that could change the measured
numbers WITHOUT editing the algorithm. Go through every family:
- build options (optimisation level, compile flags);
- system configuration flags (buffer, cache, file and I/O settings, threads,
  rate limits);
- learning or tuning hyperparameters exposed as flags (thresholds, margins,
  hold times, exploration settings, which component is active), including
  defaults the paper never mentions;
- dataset (size, key/value sizes, distribution, load order);
- workload shape (operation mix, key skew, fraction of lookups for absent
  keys, range queries, run length, warm-up);
- hardware and environment (CPU, memory size, storage device and its spare
  bandwidth, OS settings). Include the paper's stated hardware as an
  environment assumption, since a reproduction's machine almost always differs.
Read the whole flag list in the repo map, not only the first entries.

For each knob:
- `knob`: the exact flag / option / env var name as it appears in the code.
- `layer`: build | dataset | config | workload | environment.
- `paper_value`: the value the paper states, or "unstated".
- `code_default`: the default in the repo, from the repo map.
- `status`: "unstated"; "stated_matches" (paper value == code default);
  or "stated_code_differs" (the paper states a value the default does not
  match -- a paper-artifact inconsistency, flag these).
- `candidate_values`: 1-3 plausible values to try, prioritising the paper's
  stated value and values used in other scripts in the repo.
- `evidence`: for paper evidence use kind "paper", ref "p.N", and a verbatim
  quote; for code evidence use kind "code", ref "path:line" exactly as listed
  in the repo map. Evidence that is not verbatim will be discarded.
- `prior_score`: 0-1, how likely this knob explains a gap in the claims below.
- `affects_claims`: claim ids.

Return the 30 most promising, highest prior first. Ids A1, A2, ...

CLAIMS:
{claims}

PAPER EXPERIMENTAL SETUP:
{setup}

REPO MAP:
{repo_map}

RELEVANT FILES:
{files}
"""

SETUP_HEADINGS = r"^\s*\d+(\.\d+)?\s+(experimental (setup|evaluation)|evaluation|experiments)\s*$"


class _Assumptions(BaseModel):
    assumptions: list[Assumption]


def relevant_files(rm: RepoMap, claims: list[Claim], limit: int = 20, max_bytes: int = 12_000) -> str:
    """Pick the files most likely to matter: run scripts, build files, flag-heavy sources."""
    flag_counts: dict[str, int] = {}
    for f in rm.flags:
        flag_counts[f.file] = flag_counts.get(f.file, 0) + 1
    words = {w.lower() for c in claims for w in re.findall(r"[a-zA-Z_]{4,}", c.metric + " " + " ".join(c.conditions.values()))}
    def score(path: str) -> float:
        s = flag_counts.get(path, 0) * 2 + (10 if path in rm.scripts else 0) + (8 if path in rm.build_files else 0)
        s += sum(3 for w in words if w in path.lower())
        return s
    # Ties broken by path: set order varies between processes, and a reordered prompt misses the cache.
    ranked = sorted({*flag_counts, *rm.scripts, *rm.build_files}, key=lambda p: (-score(p), p))[:limit]
    chunks = []
    for rel in ranked:
        try:
            text = (rm.root / rel).read_text(encoding="utf-8", errors="replace")[:max_bytes]
        except OSError:
            continue
        numbered = "\n".join(f"{i:5d}| {line}" for i, line in enumerate(text.splitlines(), 1))
        chunks.append(f"=== {rel} ===\n{numbered}")
    return "\n\n".join(chunks)


async def build_assumption_space(router: Router, paper: PaperText, rm: RepoMap, claims: list[Claim]) -> list[Assumption]:
    setup = paper.section(SETUP_HEADINGS, max_chars=25_000) or paper.full_text[:25_000]
    # per-experiment hyperparameter tables are often in an appendix, past the excerpt (blind-2: GraphMAE's
    # Table 8 stated alpha_l = 1 for COLLAB, and the ledger never saw it)
    tables = [t for t in hyperparameter_tables(paper.full_text) if t[:120] not in setup]
    if tables:
        setup += "\n\n## Hyperparameter tables found elsewhere in the paper\n" + "\n\n".join(tables)
    prompt = ASSUMPTION_PROMPT.format(
        claims="\n".join(f"{c.id}: {c.metric} = {c.reported_value} {c.unit or ''} ({c.figure_or_table}) {c.conditions}" for c in claims),
        setup=setup,
        repo_map=rm.summary(max_files=300, max_flags=500),
        files=relevant_files(rm, claims),
    )
    out = await router.structured("ultra", [{"role": "user", "content": prompt}], _Assumptions)
    found = list(out.assumptions)
    # one long excerpt loses the appendix (SA-Bench: single-call extraction skips appendices as attention
    # decays; GraphMAE's alpha_l = 1 for COLLAB was in appendix Table 8): read the appendix in its own call
    appendix = paper.section(APPENDIX_HEADINGS, max_chars=25_000)
    if appendix and appendix[:200] not in setup:
        prompt2 = ASSUMPTION_PROMPT.format(
            claims="\n".join(f"{c.id}: {c.metric} = {c.reported_value} {c.unit or ''} ({c.figure_or_table}) {c.conditions}" for c in claims),
            setup=appendix,
            repo_map=rm.summary(max_files=300, max_flags=500),
            files=relevant_files(rm, claims),
        )
        out2 = await router.structured("ultra", [{"role": "user", "content": prompt2}], _Assumptions)
        found = merge_assumptions(found, out2.assumptions)
    return _fill_defaults(found, rm)


APPENDIX_HEADINGS = r"^\s*(?:(?:Appendix|APPENDIX|Supplementary|SUPPLEMENTARY)\b[^\n]{0,80}|[A-H](?:\.\d+)?\s+[A-Z][A-Za-z ,&-]{2,60})\s*$"


def merge_assumptions(first: list[Assumption], second: list[Assumption]) -> list[Assumption]:
    """One entry per knob: a stated paper value beats "unstated", the higher prior wins, evidence and
    candidate values are combined."""
    def norm(k: str) -> str:
        return k.strip().lstrip("-").replace("-", "_").lower()

    out: dict[str, Assumption] = {}
    for a in list(first) + list(second):
        key = norm(a.knob)
        if key not in out:
            out[key] = a
            continue
        b = out[key]
        stated_a = not a.paper_value.strip().lower().startswith("unstated")
        stated_b = not b.paper_value.strip().lower().startswith("unstated")
        keep = a if (stated_a and not stated_b) or (stated_a == stated_b and a.prior_score > b.prior_score) else b
        other = b if keep is a else a
        out[key] = keep.model_copy(update={
            "evidence": list(keep.evidence) + [e for e in other.evidence if e not in keep.evidence],
            "candidate_values": list(dict.fromkeys([str(v) for v in keep.candidate_values] + [str(v) for v in other.candidate_values])),
            "prior_score": max(keep.prior_score, other.prior_score),
            "affects_claims": list(dict.fromkeys(list(keep.affects_claims) + list(other.affects_claims)))})
    return list(out.values())


_TABLE_CAPTION = re.compile(r"(?m)^\s*(Table\s+[A-Z]?\d+[.:])")
_HYPER = re.compile(r"hyper-?\s?parameter|setting|configuration|implementation detail|training detail", re.I)


def hyperparameter_tables(text: str, max_chars: int = 4000, max_tables: int = 4) -> list[str]:
    """Every table whose caption mentions hyper-parameters, settings or configuration, wherever it is in the
    paper: the caption and what follows it (PDF tables come out as one cell per line), up to the next
    caption."""
    caps = list(_TABLE_CAPTION.finditer(text))
    out = []
    for i, m in enumerate(caps):
        caption = text[m.start(): m.start() + 300]
        if not _HYPER.search(" ".join(caption.split("\n")[:2])):  # the caption only, not the table body
            continue
        end = caps[i + 1].start() if i + 1 < len(caps) else len(text)
        out.append(text[m.start(): min(end, m.start() + max_chars)].strip())
        if len(out) >= max_tables:
            break
    return out


def _fill_defaults(assumptions: list[Assumption], rm: RepoMap) -> list[Assumption]:
    """Code defaults come from the repo map, and status is computed, not taken from the model."""
    fixed = []
    for a in assumptions:
        flags = [f for f in rm.find_flag(a.knob) if f.default not in (None, "None")]
        if flags:
            a = a.model_copy(update={"code_default": flags[0].default})
        fixed.append(a.model_copy(update={"status": derive_status(a.paper_value, a.code_default, a.status)}))
    return sorted(fixed, key=lambda a: a.prior_score, reverse=True)


_UNITS = {"k": 1e3, "kb": 1e3, "kib": 1024, "m": 1e6, "mb": 1e6, "mib": 1024**2, "g": 1e9, "gb": 1e9,
          "gib": 1024**3, "million": 1e6, "billion": 1e9}
_BOOLS = {"true": True, "on": True, "yes": True, "enabled": True, "1": True,
          "false": False, "off": False, "no": False, "disabled": False, "0": False}


def _value(v: str | None):
    """Parse '2 MB', '2097152', '100 million', 'true' into comparable values; None if unparseable."""
    if v is None:
        return None
    s = str(v).strip().lower().strip("\"'").split("(")[0].strip().rstrip(",")
    if s in _BOOLS:
        return _BOOLS[s]
    m = re.fullmatch(r"([-+]?\d+(?:\.\d+)?)\s*([a-z]*)", s.replace(",", "").replace("_", ""))
    if m:
        mult = _UNITS.get(m.group(2), 1 if not m.group(2) else None)
        if mult is not None:
            return float(m.group(1)) * mult
    return None


def derive_status(paper_value: str, code_default: str | None, model_status: str) -> str:
    if paper_value.strip().lower().startswith("unstated"):
        return AssumptionStatus.unstated.value
    p, c = _value(paper_value), _value(code_default)
    if p is None or c is None:
        return model_status  # can't compare mechanically; keep the model's judgement
    if isinstance(p, float) and isinstance(c, float):
        # binary/decimal megabytes ('2MB' vs 2097152) count as the same value
        same = abs(p - c) <= 0.05 * max(abs(p), abs(c), 1e-12)
    else:
        same = p == c
    return (AssumptionStatus.stated_matches if same else AssumptionStatus.stated_code_differs).value


def ground_assumptions(paper: PaperText, repo_root: Path, assumptions: list[Assumption]) -> GroundingReport:
    g = Grounder(paper.full_text, repo_root, pages={p.number: p.text for p in paper.pages})
    return g.check_assumptions(assumptions)


def inconsistencies(assumptions: list[Assumption]) -> list[Assumption]:
    return [a for a in assumptions if a.status == AssumptionStatus.stated_code_differs.value]
