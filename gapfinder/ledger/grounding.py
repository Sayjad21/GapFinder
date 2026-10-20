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
    recovered: list[tuple[str, str]] = field(default_factory=list)  # kept by a fuzzy quote or a table cell (id, how)


class Grounder:
    def __init__(self, paper_text: str, repo_root: str | Path | None = None, pages: dict[int, str] | None = None,
                 grids: list | None = None):
        self.paper = normalise(paper_text)
        self.pages = {n: normalise(t) for n, t in (pages or {}).items()}
        self.repo_root = Path(repo_root) if repo_root else None
        self.grids = grids or []  # gapfinder/ingest/tables.py grids (LaTeX first, then PDF)

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

    def find_page(self, quote: str) -> int | None:
        """The page a quote actually starts on (models often cite section numbers as pages)."""
        q = normalise(quote)
        for n in sorted(self.pages):
            if q in self.pages[n]:
                return n
        for n in sorted(self.pages):  # quote straddles a page break
            if q in self.pages[n] + " " + self.pages.get(n + 1, ""):
                return n
        return None

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
            return self.quote_in_paper(ev.quote)  # page refs are corrected separately (fix_page)
        if ev.kind == "code":
            return self.code_ref_ok(ev.ref, knob)
        # web and measurement evidence are checked by their producers
        return bool(ev.quote.strip())

    def check_claims(self, claims: list[Claim]) -> GroundingReport:
        """Plan D3.1: a claim is kept when its quote is in the paper and its number (in any spelling: 0.729, 72.9,
        72.9%) is in the quote, on its page or in its table; a quote the model paraphrased is recovered by a fuzzy
        match whose window holds the number, or by the table cell that holds it under the claim's conditions.
        A number found nowhere is dropped (a value the model wrote, not the paper)."""
        rep = GroundingReport()
        for c in claims:
            v = c.reported_value
            if self.quote_in_paper(c.quote):
                page = self.find_page(c.quote)
                if v is not None and not (number_in_text(v, c.quote) or number_in_text(v, self._page_window(page))
                                          or self.table_cell(c) is not None):
                    rep.dropped.append((c.id, f"its number {v:g} is not in its quote, its page or its table"))
                    continue
                rep.kept.append(c.model_copy(update={"page": page}) if page and page != c.page else c)
                continue
            hit = self.fuzzy_find(c.quote)
            # wording may differ, numbers may not: every number the quote holds, and the claim's, is in the window
            if hit is not None and all(number_in_text(n, hit[0]) for n in _numbers(c.quote)) and (
                    v is None or number_in_text(v, hit[0])):
                page = self.find_page(hit[0])
                rep.kept.append(c.model_copy(update={"quote": hit[0], **({"page": page} if page else {})}))
                rep.recovered.append((c.id, f"quote matched at {hit[1]:.0%} similarity"))
                continue
            cell = self.table_cell(c) if v is not None else None
            if cell is not None:
                g, r, col, x = cell
                rep.kept.append(c.model_copy(update={"quote": f"{g.label or g.caption[:40]}: {x.text}"}))
                rep.recovered.append((c.id, f"its number is the cell {g.label} r{r}c{col} "
                                            f"({' / '.join(g.row_header(r) + g.col_header(col))})"))
                continue
            rep.dropped.append((c.id, "quote not found in paper"))
        return rep

    # -- numbers, fuzzy quotes and table cells (plan D3.1) ------------------
    def _page_window(self, page: int | None) -> str:
        if page is None or not self.pages:
            return ""
        return " ".join(self.pages.get(p, "") for p in (page - 1, page, page + 1))

    def fuzzy_find(self, quote: str, min_ratio: float = 0.85) -> tuple[str, float] | None:
        """The paper's text that a paraphrased or mis-transcribed quote came from: candidate places from the quote's
        word trigrams, each scored by sequence similarity over a window of the quote's length."""
        import difflib

        q = normalise(quote)
        words = q.split()
        if len(q) < 20 or len(words) < 4:
            return None
        starts = set()
        for i in range(len(words) - 2):
            tri = " ".join(words[i:i + 3])
            off = len(" ".join(words[:i])) + (1 if i else 0)
            pos = self.paper.find(tri)
            n = 0
            while pos != -1 and n < 20:
                starts.add(max(0, pos - off))
                pos = self.paper.find(tri, pos + 1)
                n += 1
            if len(starts) > 200:
                break
        best = None
        for s in starts:
            for shift in (-15, 0, 15):
                a = max(0, s + shift)
                window = self.paper[a:a + len(q)]
                r = difflib.SequenceMatcher(None, q, window, autojunk=False).ratio()
                if best is None or r > best[1]:
                    best = (window, r)
        return best if best and best[1] >= min_ratio else None

    def table_cell(self, c: Claim):
        """(grid, row, column, cell) holding the claim's number in its table, under its conditions when they say."""
        if not self.grids or c.reported_value is None:
            return None
        want = _table_no(c.figure_or_table)
        words = {w for v in (c.conditions or {}).values() for w in re.findall(r"[a-z0-9]{3,}", str(v).lower())}
        best = None
        for g in self.grids:
            if want is not None and _table_no(g.label) != want:
                continue
            for r, col, x in g.body():
                if not any(_print_close(c.reported_value, s) for s in (x.value,)):
                    continue
                head = " ".join(g.row_header(r) + g.col_header(col) + [g.caption]).lower()
                score = sum(w in head for w in words)
                if best is None or score > best[0]:
                    best = (score, (g, r, col, x))
        if best is None or (words and best[0] == 0 and want is None):
            return None  # a number found only in an unnamed table, under none of its conditions: a coincidence
        return best[1]

    def fix_page(self, ev: Evidence) -> Evidence:
        if ev.kind != "paper" or not self.pages:
            return ev
        page = self.find_page(ev.quote)
        return ev.model_copy(update={"ref": f"p.{page}"}) if page else ev

    def check_assumptions(self, assumptions: list[Assumption]) -> GroundingReport:
        """Drop ungrounded evidence; drop an assumption whose evidence is all ungrounded."""
        rep = GroundingReport()
        for a in assumptions:
            good = [self.fix_page(e) for e in a.evidence if self.evidence_ok(e, a.knob)]
            if a.evidence and not good:
                rep.dropped.append((a.id, "no grounded evidence"))
                continue
            update = {"evidence": good}
            # A value "stated in the paper" needs a grounded paper quote; otherwise it's unstated. A stated
            # number must also appear in one of those quotes (blind-2: the ledger wrote alpha_l's code default,
            # 2, as the paper's value, with a paper quote that held no number at all)
            stated = not a.paper_value.strip().lower().startswith("unstated")
            quotes = [e.quote for e in good if e.kind == "paper"]
            if stated and not quotes:
                update.update(paper_value="unstated", status="unstated")
                rep.dropped.append((a.id, f"paper_value {a.paper_value!r} had no paper quote; set to unstated"))
            elif stated and (nums := _numbers(a.paper_value.split("(")[0])) and not any(
                    any(_same_num(n, q) for q in _numbers(" ".join(quotes))) for n in nums):
                update.update(paper_value="unstated", status="unstated")
                rep.dropped.append((a.id, f"paper_value {a.paper_value!r}: no paper quote contains that number; "
                                          "set to unstated"))
            rep.kept.append(a.model_copy(update=update))
        return rep


_NUMBER = re.compile(r"(?<![\w.])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")


def _numbers(text: str) -> list[float]:
    out = []
    for m in _NUMBER.finditer(text.replace(",", "")):
        try:
            out.append(float(m.group(0)))
        except ValueError:
            pass
    return out


def _same_num(a: float, b: float) -> bool:
    return a == b or (a != 0 and abs(a - b) <= 1e-9 * max(abs(a), abs(b)))


def _decimals(x: float) -> int:
    s = f"{round(x, 8):.8f}".rstrip("0")
    return len(s.split(".")[1]) if "." in s else 0


def _print_close(a: float, b: float | None) -> bool:
    """The same number as printed, at the coarser precision of the two, or as a fraction against a percent."""
    if b is None:
        return False
    for x, y in ((a, b), (a * 100, b), (a, b * 100)):
        d = min(_decimals(x), _decimals(y))
        if d == 0:  # an integer on either side: only the same integer (a "1" is not 0.957 rounded)
            if abs(x - y) <= 1e-9 * max(1.0, abs(x)):
                return True
        elif abs(x - y) <= 0.5 * 10 ** -d + 1e-9:
            return True
    return False


_SCALE = {"K": 1e3, "k": 1e3, "M": 1e6, "B": 1e9, "G": 1e9}
_SUFFIXED = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s?([KkMBG])\b")
_POWER = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)\s*(?:x|×|\\times|\*)\s*10\s*\^?\s*\{?\s*([-+]?\d+)\s*\}?")
_TEN = re.compile(r"(?<![\w.])10\s*(?:\^\s*\{?\s*([-+]?\d+)\s*\}?|−(\d+))")  # 10^{-4}; a PDF's lost superscript: 10−4
_E = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)[eE]\s*([-+]?\d+)")


def _tol(printed: str, scale: float = 1.0) -> float:
    """Half a unit of the last printed digit (0 for an integer: only the same integer matches)."""
    d = len(printed.split(".")[1]) if "." in printed else 0
    return 0.5 * 10 ** -d * scale if d else 0.0


def numbers_with_precision(text: str) -> list[tuple[float, float]]:
    """(value, tolerance) of every number in the text, in any spelling: 72.9, 1,234, 0.92 K, 6.31M, 1e-4, 1e−4,
    5 x 10^{-3}, 10^{-4}, and a PDF's 10−4."""
    raw = text.replace("−", "−").replace(" ", " ")
    out = []
    for m in _TEN.finditer(raw):
        e = int((m.group(1) or "-" + (m.group(2) or "0")).replace("−", "-"))
        out.append((10.0 ** e, 0.0))
    for m in _POWER.finditer(raw.replace("−", "-")):
        e = int(m.group(2))
        out.append((float(m.group(1)) * 10.0 ** e, _tol(m.group(1), 10.0 ** e)))
    for m in _E.finditer(raw.replace("−", "-")):
        e = int(m.group(2))
        out.append((float(m.group(1)) * 10.0 ** e, _tol(m.group(1), 10.0 ** e)))
    for m in _SUFFIXED.finditer(raw):
        s = _SCALE[m.group(2)]
        out.append((float(m.group(1)) * s, _tol(m.group(1), s)))
    for m in _NUMBER.finditer(raw.replace("−", "-").replace(",", "")):
        try:
            out.append((float(m.group(0)), _tol(m.group(0).lstrip("+-"))))
        except ValueError:
            pass
    return out


def number_in_text(v: float, text: str | None) -> bool:
    """Whether `v` appears in the text in any spelling (0.729, 72.9, 72.90, 72.9%, 72.9±0.4, 0.92 K, 1e-4), at the
    coarser precision of the two, or as a fraction against a percent."""
    if not text:
        return False
    for n, tol_n in numbers_with_precision(text):
        for x in (v, v * 100, v / 100):
            tol_x = _tol(f"{round(x, 8):.8f}".rstrip("0").rstrip("."))
            if abs(x - n) <= max(tol_n, tol_x) + 1e-9 * max(1.0, abs(n)):
                return True
    return False


def _table_no(ref: str | None) -> str | None:
    m = re.search(r"(?i)\btab(?:le|\.)?\s*([0-9]+|[ivx]+)\b", ref or "")
    return m.group(1).lower() if m else None


def _page_of(ref: str) -> int | None:
    m = re.search(r"(\d+)", ref)
    return int(m.group(1)) if m else None
