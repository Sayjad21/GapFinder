"""The paper's LaTeX source from arXiv: tables and figure data as plain text (plan item 2).

PDF text extraction loses what the source states exactly:
- symbols (RippleNet's table gives "λ1 = 10⁻⁵"; the PDF text came out as a symbol the ledger couldn't link to the
  `--l2_weight` flag; the source says `$\\lambda_1 = 10^{-5}$`);
- table layout (GraphMAE's per-dataset values in an appendix table);
- figure data, when the figure is drawn in the source (pgfplots `\\addplot coordinates {...}`, or a bundled
  .csv/.dat file read by `\\addplot table`).

About 93% of arXiv papers have their source available (arXiv e-print, `https://arxiv.org/e-print/<id>`). This module
fetches it, flattens `\\input`/`\\include`, drops comments, and writes the tables and figure series as a plain-text
supplement to the paper. The PDF text stays the main text (page numbers and quote grounding use it); the supplement
is appended, so quotes from it are grounded too. Nothing here calls a model.
"""

from __future__ import annotations

import gzip
import io
import re
import tarfile
import urllib.request
from pathlib import Path

_ARXIV_ID = re.compile(r"arXiv:\s*(\d{4}\.\d{4,5})(v\d+)?", re.I)
_ARXIV_URL = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(v\d+)?", re.I)


def detect_arxiv_id(text: str, filename: str = "") -> str | None:
    """The paper's arXiv id from its first pages (the arXiv stamp) or its file name, with the version if given."""
    for rx in (_ARXIV_ID, _ARXIV_URL):
        m = rx.search(text[:20000])
        if m:
            return m.group(1) + (m.group(2) or "")
    m = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", filename)
    return (m.group(1) + (m.group(2) or "")) if m else None


def fetch_source(arxiv_id: str, cache_dir: Path, timeout: float = 120) -> Path | None:
    """Download and unpack the e-print into cache_dir/<id>/ (cached). None when there is no source."""
    dest = Path(cache_dir) / arxiv_id.replace("/", "_")
    if dest.is_dir() and any(dest.rglob("*.tex")):
        return dest
    req = urllib.request.Request(f"https://arxiv.org/e-print/{arxiv_id}",
                                 headers={"User-Agent": "gapfinder (research reproduction tool)"})
    try:
        data = urllib.request.urlopen(req, timeout=timeout).read()
    except Exception:
        return None
    return unpack(data, dest)


def unpack(data: bytes, dest: Path) -> Path | None:
    """An e-print is a (gzipped) tar of the source, or one gzipped .tex file; a PDF-only submission has no source."""
    dest.mkdir(parents=True, exist_ok=True)
    try:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as t:
            t.extractall(dest, filter="data")
        return dest if any(dest.rglob("*.tex")) else None
    except tarfile.TarError:
        pass
    try:
        text = gzip.decompress(data)
    except OSError:
        text = data
    if text[:4] == b"%PDF":
        return None
    (dest / "main.tex").write_bytes(text)
    return dest


def main_tex(src: Path) -> Path | None:
    cands = [p for p in src.rglob("*.tex") if "\\documentclass" in p.read_text("utf-8", "replace")]
    cands.sort(key=lambda p: ("\\begin{document}" not in p.read_text("utf-8", "replace"), len(p.parts), p.name))
    return cands[0] if cands else None


def _strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", text)


def flatten(path: Path, root: Path, depth: int = 0) -> str:
    """The document with \\input{x} and \\include{x} replaced by the files' text (recursively), comments dropped."""
    text = _strip_comments(path.read_text("utf-8", "replace"))
    if depth > 8:
        return text

    def sub(m):
        name = m.group(2).strip()
        for cand in (root / name, root / f"{name}.tex", path.parent / name, path.parent / f"{name}.tex"):
            if cand.is_file():
                return flatten(cand, root, depth + 1)
        return ""
    return re.sub(r"\\(input|include)\{([^}]+)\}", sub, text)


_TABLE = re.compile(r"\\begin\{(table\*?)\}(.*?)\\end\{\1\}", re.S)
_CAPTION = re.compile(r"\\caption(?:\[[^\]]*\])?\{((?:[^{}]|\{[^{}]*\})*)\}", re.S)
_TABULAR = re.compile(r"\\begin\{tabular\*?\}(?:\{[^}]*\})?\{(?:[^{}]|\{[^{}]*\})*\}(.*?)\\end\{tabular\*?\}", re.S)
_RULES = re.compile(r"\\(hline|toprule|midrule|bottomrule|cmidrule(\([^)]*\))?\{[^}]*\}|cline\{[^}]*\}|specialrule\{[^}]*\}\{[^}]*\}\{[^}]*\})")


def _plain(cell: str) -> str:
    """A LaTeX cell as text: keep math and symbols as written (\\lambda_1 stays), drop formatting commands."""
    cell = re.sub(r"\\(textbf|textit|emph|mathbf|underline|textrm|text|mathrm|bm|boldsymbol)\{([^{}]*)\}", r"\2", cell)
    cell = re.sub(r"\\multi(column|row)\{[^}]*\}\{[^}]*\}\{([^{}]*)\}", r"\2", cell)
    cell = re.sub(r"\\(cite|ref|label)\{[^}]*\}", "", cell)
    return " ".join(cell.replace("~", " ").split())


def tables(doc: str) -> list[str]:
    out = []
    for m in _TABLE.finditer(doc):
        body = m.group(2)
        cap = _CAPTION.search(body)
        caption = _plain(cap.group(1)) if cap else ""
        rows = []
        for tab in _TABULAR.finditer(body):
            for row in _RULES.sub("", tab.group(1)).split("\\\\"):
                cells = [_plain(c) for c in row.split("&")]
                if any(cells):
                    rows.append(" | ".join(cells))
        if rows:
            out.append(f"Table: {caption}\n" + "\n".join(rows))
    return out


_FIGURE = re.compile(r"\\begin\{(figure\*?)\}(.*?)\\end\{\1\}", re.S)
_ADDPLOT = re.compile(r"\\addplot\+?(?:\[[^\]]*\])?\s*(coordinates\s*\{([^}]*)\}|table\s*(?:\[[^\]]*\])?\s*\{([^}]+)\})", re.S)
_LEGEND = re.compile(r"\\addlegendentry\{([^}]*)\}")


def figure_data(doc: str, root: Path, max_points: int = 60) -> list[str]:
    """Series drawn in the source: pgfplots coordinates, or a data file read by `\\addplot table`."""
    out = []
    for m in _FIGURE.finditer(doc):
        body = m.group(2)
        cap = _CAPTION.search(body)
        caption = _plain(cap.group(1)) if cap else ""
        legends = _LEGEND.findall(body)
        series = []
        for i, a in enumerate(_ADDPLOT.finditer(body)):
            name = legends[i] if i < len(legends) else f"series {i + 1}"
            if a.group(2) is not None:
                pts = re.findall(r"\(\s*([^,()]+?)\s*,\s*([^,()]+?)\s*\)", a.group(2))
            else:
                f = root / a.group(3).strip()
                pts = []
                if f.is_file():
                    lines = [l for l in f.read_text("utf-8", "replace").splitlines() if l.strip()]
                    for l in lines[1:]:  # first line: column names
                        parts = re.split(r"[,\s\t]+", l.strip())
                        if len(parts) >= 2:
                            pts.append((parts[0], parts[1]))
            if pts:
                series.append(f"{name}: " + ", ".join(f"({x}, {y})" for x, y in pts[:max_points]))
        if series:
            out.append(f"Figure data: {caption}\n" + "\n".join(series))
    return out


def supplement(src: Path) -> str:
    """The plain-text supplement: tables and figure data from the source ('' when there is none)."""
    main = main_tex(src)
    if main is None:
        return ""
    doc = flatten(main, main.parent)
    parts = tables(doc) + figure_data(doc, main.parent)
    if not parts:
        return ""
    return "## From the LaTeX source (tables and figure data, symbols as written)\n\n" + "\n\n".join(parts)
