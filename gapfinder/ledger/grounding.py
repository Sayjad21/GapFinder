"""Grounding checker: anything the LLM cites must exist where it says it does.

Paper quotes must string-match the PDF text (after whitespace/hyphenation
normalisation). `file:line` refs must exist and the line must contain the
cited flag. Ungrounded items are dropped, never shown.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from gapfinder.ledger.schemas import Assumption, Claim, Evidence

_LIGATURES = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl", "−": "-", "–": "-", "—": "-", "×": "x"}


def normalise(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    for k, v in _LIGATURES.items():
        text = text.replace(k, v)
    # A hyphen at a line break is ambiguous ("read-\nheavy" is "read-heavy",
    # "compac-\ntion" is "compaction"), so hyphens are dropped everywhere.
    text = re.sub(r"-\s*\n\s*", "", text)
    text = text.replace("-", "")
    text = re.sub(r"[“”]", '"', text)
    text = re.sub(r"[‘’]", "'", text)
    text = re.sub(r"\s*([=<>+×/])\s*", r"\1", text)  # PDF math spacing varies: "K= 4" vs "K = 4"
    return re.sub(r"\s+", " ", text).strip().lower()


@dataclass
class GroundingReport:
    kept: list = field(default_factory=list)
    dropped: list[tuple[str, str]] = field(default_factory=list)  # (id, reason)


class Grounder:
    def __init__(self, paper_text: str, repo_root: str | Path | None = None, pages: dict[int, str] | None = None):
        self.paper = normalise(paper_text)
        self.pages = {n: normalise(t) for n, t in (pages or {}).items()}
        self.repo_root = Path(repo_root) if repo_root else None

    # -- primitives ---------------------------------------------------------
    def quote_in_paper(self, quote: str, page: int | None = None) -> bool:
        q = normalise(quote)
        if len(q) < 8:
            return False  # too short to be evidence of anything
        if page is not None and page in self.pages:
            # allow the quote to straddle into the neighbouring page
            window = " ".join(self.pages.get(p, "") for p in (page - 1, page, page + 1))
            return q in window
        return q in self.paper

    def code_ref_ok(self, ref: str, must_contain: str | None, quote: str | None = None) -> bool:
        if self.repo_root is None:
            return False
        m = re.fullmatch(r"(.+?):(\d+)", ref.strip())
        if not m:
            return False
        rel, line_no = m.group(1), int(m.group(2))
        path = (self.repo_root / rel).resolve()
        try:
            path.relative_to(self.repo_root.resolve())
        except ValueError:
            return False  # escapes the repo
        if not path.is_file():
            return False
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        if not 1 <= line_no <= len(lines):
            return False
        line = lines[line_no - 1]
        if must_contain and must_contain.lstrip("-").lower() not in line.lower():
            return False
        if quote and normalise(quote) not in normalise(line):
            return False
        return True

    # -- objects ------------------------------------------------------------
    def evidence_ok(self, ev: Evidence, knob: str | None = None) -> bool:
        if ev.kind == "paper":
            page = _page_of(ev.ref)
            return self.quote_in_paper(ev.quote, page)
        if ev.kind == "code":
            return self.code_ref_ok(ev.ref, knob)
        # web and measurement evidence are checked by their producers
        return bool(ev.quote.strip())

    def check_claims(self, claims: list[Claim]) -> GroundingReport:
        rep = GroundingReport()
        for c in claims:
            if self.quote_in_paper(c.quote, c.page) or self.quote_in_paper(c.quote):
                rep.kept.append(c)
            else:
                rep.dropped.append((c.id, "quote not found in paper"))
        return rep

    def check_assumptions(self, assumptions: list[Assumption]) -> GroundingReport:
        """Drop ungrounded evidence; drop an assumption whose evidence is all ungrounded."""
        rep = GroundingReport()
        for a in assumptions:
            good = [e for e in a.evidence if self.evidence_ok(e, a.knob)]
            if a.evidence and not good:
                rep.dropped.append((a.id, "no grounded evidence"))
                continue
            rep.kept.append(a.model_copy(update={"evidence": good}))
        return rep


def _page_of(ref: str) -> int | None:
    m = re.search(r"(\d+)", ref)
    return int(m.group(1)) if m else None
