"""Paper tables as grids (plan D3.2-D3.4, docs/CONTEXT_v11.md section 7.2).

Claims extracted by a language model from flattened text drop cells and invent some (DTBench); a table's numbers are
better read from its structure. This module builds grids deterministically and never lets a model write a number:

- **LaTeX grids**: `tabular` bodies split into rows and cells (escaped `\\&` and braces respected), `\\multicolumn`
  and `\\multirow` spans placed, rules dropped; the header rows are those above the first `\\midrule` (else the rows
  before the first mostly numeric one), the header columns the leading columns with no number in the body.
- **PDF grids**: PyMuPDF's table finder on each page, the same cell parsing.
- **Cells**: a number in any spelling (`72.9`, `72.9%`, `0.729`, `72.9 ± 0.4`, `$72.9_{\\pm 0.4}$`, `72.9 (0.4)`,
  `1,234`), its spread, bold and underline (the paper's best and second best), significance marks dropped;
  `-`, `N/A`, `OOM` are no value.
- **Cell claims** (D3.3): every numeric body cell, with its row and column header paths as conditions. Which axis
  holds the metrics and which rows are the paper's method come from `label()`: a metric lexicon and the paper's own
  name for its method (or bold majority), or an optional labeller (a model choosing coordinates, never numbers).
- **Double entry** (D3.4): a LaTeX grid and a PDF grid of the same table, matched by caption number or by their
  numbers, reconciled cell by cell; a cell that differs beyond rounding, or is missing on one side, is flagged.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

# ------------------------------------------------------------------------ cells

_NUM = r"[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:[eE][-+]?\d+)?|[-+]?\.\d+"
_PM = re.compile(rf"^({_NUM})\s*(?:\\pm|±|\+/-|\+-)\s*({_NUM})$")
_PAREN = re.compile(rf"^({_NUM})\s*\(\s*({_NUM})\s*\)$")
_ONE = re.compile(rf"^({_NUM})$")
_MISSING = {"-", "--", "---", "–", "—", "n/a", "na", "oom", "oot", "x", "/", "", "nan", "*"}
_FORMAT = re.compile(r"\\(?:textbf|textit|textsc|textrm|textsf|texttt|textcolor\{[^}]*\}|text|emph|mathbf|mathrm|"
                     r"mathit|mathsf|underline|uline|boldsymbol|bm|cellcolor\{[^}]*\}|color\{[^}]*\}|mbox|hbox|"
                     r"makecell|shortstack|bf|it|rm|em|sf|tt|sl|bfseries|itshape)(?![A-Za-z])\s*")


@dataclass
class Cell:
    text: str
    value: float | None = None
    std: float | None = None
    percent: bool = False
    bold: bool = False
    underline: bool = False
    row: int = 0
    col: int = 0
    rowspan: int = 1
    colspan: int = 1

    @property
    def numeric(self) -> bool:
        return self.value is not None


def _strip_braces(s: str) -> str:
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\{([^{}]*)\}", r"\1", s)
    return s


def plain(tex: str) -> str:
    """A LaTeX cell as plain text (formatting, math markers and spacing commands removed)."""
    s = tex
    s = re.sub(r"\\(cite|citep|citet|ref|label|footnote|footnotemark)\*?(\[[^\]]*\])?\{[^}]*\}", "", s)
    s = re.sub(r"\\multi(column|row)\{[^}]*\}\{[^}]*\}", "", s)
    s = re.sub(r"\\resizebox\{[^}]*\}\{[^}]*\}", "", s)  # its third argument is the content
    s = re.sub(r"\\(rotatebox|scalebox|raisebox)(\[[^\]]*\])?\{[^}]*\}", "", s)  # their second argument is
    s = re.sub(r"\\(Checkmark|checkmark|ding\{\d+\}|cmark|xmark|XSolidBrush|times)(?![A-Za-z])", "", s)
    s = _FORMAT.sub("", s)
    s = s.replace("\\%", "%").replace("\\&", "&").replace("\\#", "#").replace("\\_", "_").replace("~", " ")
    s = s.replace("\\,", " ").replace("\\ ", " ")
    s = re.sub(r"\\(quad|qquad|hfill|centering|small|footnotesize|scriptsize|tiny|large|Large)\b", " ", s)
    s = _strip_braces(s).replace("$", "")
    return " ".join(s.split())


def parse_number(text: str) -> tuple[float | None, float | None, bool]:
    """(value, spread, percent) of a cell as written; (None, None, False) when it holds no single number."""
    s = text.replace("\\pm", "±").replace("$", "").replace("{", "").replace("}", "")
    s = re.sub(r"\\(?:textbf|textit|textsc|mathbf|mathrm|underline|boldsymbol|bm|emph|text|bf|it|rm|bfseries)(?![A-Za-z])\s*", "", s)
    s = re.sub(r"\^\s*\\?(\*+|dagger|ddagger|†|‡|\w)", "", s)  # significance marks: 72.9^{*}, 72.9^\dagger
    s = re.sub(r"[*†‡§]+$", "", s.strip())
    s = re.sub(r"_\s*±", "±", s)  # 72.9_{\pm 0.4}
    pct = "%" in s or "\\%" in s
    s = s.replace("\\%", "").replace("%", "").strip()
    if s.lower() in _MISSING:
        return None, None, False
    for pat in (_PM, _PAREN):
        m = pat.match(s)
        if m:
            return float(m.group(1).replace(",", "")), float(m.group(2).replace(",", "")), pct
    m = _ONE.match(s)
    if m:
        return float(m.group(1).replace(",", "")), None, pct
    m = re.match(rf"^({_NUM})\s?([KkMB])$", s)  # 0.92K, 6.31 M (parameter counts)
    if m:
        return float(m.group(1).replace(",", "")) * {"K": 1e3, "k": 1e3, "M": 1e6, "B": 1e9}[m.group(2)], None, pct
    return None, None, False


def make_cell(tex: str, row: int, col: int, rowspan: int = 1, colspan: int = 1, from_latex: bool = True) -> Cell:
    bold = bool(re.search(r"\\(textbf|mathbf|bm|boldsymbol|bf|bfseries)(?![A-Za-z])", tex)) if from_latex else False
    under = bool(re.search(r"\\(underline|uline)\b", tex)) if from_latex else False
    text = plain(tex) if from_latex else " ".join(str(tex or "").split())
    v, sd, pct = parse_number(text)
    return Cell(text, v, sd, pct, bold, under, row, col, rowspan, colspan)


# ------------------------------------------------------------------------ grids


@dataclass
class Grid:
    caption: str
    source: str  # "latex" or "pdf:p<page>"
    rows: list[list[Cell]] = field(default_factory=list)  # rectangular; a spanning cell repeats over its span
    header_rows: int = 0
    header_cols: int = 0
    label: str | None = None  # "Table 3" when the caption or the source numbers it

    @property
    def shape(self) -> tuple[int, int]:
        return len(self.rows), max((len(r) for r in self.rows), default=0)

    def col_header(self, c: int) -> list[str]:
        out = []
        for r in range(self.header_rows):
            if c < len(self.rows[r]):
                t = self.rows[r][c].text
                if t and (not out or out[-1] != t):
                    out.append(t)
        return out

    def row_header(self, r: int) -> list[str]:
        out = []
        for c in range(self.header_cols):
            if c < len(self.rows[r]):
                t = self.rows[r][c].text
                if t and (not out or out[-1] != t):
                    out.append(t)
        return out

    def body(self):
        for r in range(self.header_rows, len(self.rows)):
            for c in range(self.header_cols, len(self.rows[r])):
                cell = self.rows[r][c]
                if cell.numeric and cell.row == r and cell.col == c:  # each spanning cell once
                    yield r, c, cell

    def values(self) -> list[float]:
        return [cell.value for _, _, cell in self.body()]

    def to_dict(self) -> dict:
        return {"caption": self.caption, "source": self.source, "label": self.label, "header_rows": self.header_rows,
                "header_cols": self.header_cols, "rows": [[asdict(c) for c in row] for row in self.rows]}


def _split_top(s: str, sep: str) -> list[str]:
    """Split on `sep` outside braces (and not escaped)."""
    out, depth, cur, i = [], 0, [], 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s):
            if s.startswith(sep, i) and sep.startswith("\\") and depth == 0:
                out.append("".join(cur))
                cur = []
                i += len(sep)
                continue
            cur.append(s[i:i + 2])
            i += 2
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth = max(0, depth - 1)
        if depth == 0 and s.startswith(sep, i):
            out.append("".join(cur))
            cur = []
            i += len(sep)
            continue
        cur.append(ch)
        i += 1
    out.append("".join(cur))
    return out


_TABLE = re.compile(r"\\begin\{(table\*?)\}(.*?)\\end\{\1\}", re.S)
_CAPTION = re.compile(r"\\caption(?:\[[^\]]*\])?\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}", re.S)
_LABEL = re.compile(r"\\label\{([^}]*)\}")
_TABULAR = re.compile(r"\\begin\{(tabular\*?|tabularx|longtable|tabulary)\}(?:\{[^}]*\})?\{(?:[^{}]|\{[^{}]*\})*\}"
                      r"(.*?)\\end\{\1\}", re.S)
_RULE = re.compile(r"\\((hline|toprule|bottomrule)(\[[^\]]*\])?|cmidrule(\([^)]*\))?\{[^}]*\}|cline\{[^}]*\}|"
                   r"specialrule\{[^}]*\}\{[^}]*\}\{[^}]*\}|addlinespace(\[[^\]]*\])?|hhline\{[^}]*\})")
_MULTICOL = re.compile(r"^\s*\\multicolumn\{(\d+)\}\{[^}]*\}\{(.*)\}\s*$", re.S)
_MULTIROW = re.compile(r"^\s*\\multirow\{(-?\d+)\}(?:\[[^\]]*\])?\{[^}]*\}\{(.*)\}\s*$", re.S)


def _grid_from_rows(raw_rows: list[list[str]], caption: str, source: str, midrule_at: int | None) -> Grid | None:
    placed: dict[tuple[int, int], Cell] = {}
    width = 0
    for r, cells in enumerate(raw_rows):
        c = 0
        for tex in cells:
            if (r, c) in placed and not plain(tex):  # the empty placeholder under a multirow from above
                c += 1
                continue
            while (r, c) in placed:  # a multirow from above occupies this column (no placeholder written)
                c += 1
            span, inner = 1, tex
            m = _MULTICOL.match(tex)
            if m:
                span, inner = int(m.group(1)), m.group(2)
            rspan = 1
            m2 = _MULTIROW.match(inner)
            if m2:
                rspan, inner = abs(int(m2.group(1))), m2.group(2)
            cell = make_cell(inner, r, c, rspan, span)
            for dr in range(rspan):
                for dc in range(span):
                    if dr == 0 or not placed.get((r + dr, c + dc)):
                        placed[(r + dr, c + dc)] = cell
            c += span
        width = max(width, c)
    if not placed:
        return None
    n = len(raw_rows)
    rows = [[placed.get((r, c)) or Cell("", row=r, col=c) for c in range(width)] for r in range(n)]
    # a multirow's later rows hold an empty cell in the source: the spanning cell fills it (set above, kept here)
    g = Grid(caption, source, rows)
    guess = _guess_header_rows(rows)
    # a rule ends the header only when the rows above it hold no data (a \hline low in the table separates groups)
    g.header_rows = midrule_at if midrule_at is not None and 0 < midrule_at < n and midrule_at <= max(guess, 1) + 1 \
        and all(sum(c.numeric for c in rows[r] if c.text) < max(1, len([c for c in rows[r] if c.text]) // 2)
                for r in range(midrule_at)) else guess
    g.header_cols = _guess_header_cols(rows, g.header_rows)
    # a sensitivity table's axis (0, 5, 10, 15, 20) at the edge of the body is a header, not data
    if g.header_rows < n - 1 and _axis([c.value for c in rows[g.header_rows][g.header_cols:] if c.numeric]):
        g.header_rows += 1
    col = [rows[r][g.header_cols].value for r in range(g.header_rows, n)
           if g.header_cols < len(rows[r]) and rows[r][g.header_cols].numeric]
    if g.header_cols < width - 1 and _axis(col) and len(col) == n - g.header_rows:
        g.header_cols += 1
    m = re.search(r"(?i)\btable\s*(\d+)", caption)
    g.label = f"Table {m.group(1)}" if m else None
    return g


def _axis(vals: list[float | None]) -> bool:
    """A setting's sweep values: at least three integers, strictly increasing, evenly or geometrically spaced."""
    v = [x for x in vals if x is not None]
    if len(v) < 3 or len(v) != len(vals) or any(abs(x - round(x)) > 1e-9 for x in v):
        return False
    d = [b - a for a, b in zip(v, v[1:])]
    if any(x <= 0 for x in d):
        return False
    even = max(d) - min(d) < 1e-9
    geometric = v[0] > 0 and max(b / a for a, b in zip(v, v[1:])) - min(b / a for a, b in zip(v, v[1:])) < 1e-9
    return even or geometric


def _guess_header_rows(rows: list[list[Cell]]) -> int:
    for r, row in enumerate(rows):
        cells = [c for c in row if c.text]
        if cells and sum(c.numeric for c in cells) >= max(1, len(cells) // 2):
            return r
    return 1 if rows else 0


def _guess_header_cols(rows: list[list[Cell]], header_rows: int) -> int:
    width = max((len(r) for r in rows), default=0)
    body = rows[header_rows:]
    k = 0
    for c in range(width):
        if any(c < len(r) and r[c].numeric for r in body):
            break
        k += 1
    return min(k, max(0, width - 1))


_BEGIN_TAB = re.compile(r"\\begin\{(tabular\*?|tabularx|longtable|tabulary)\}")


def _skip_args(s: str, i: int) -> int:
    """Past the optional [pos] and the {width}{colspec} arguments that follow \\begin{tabular...}."""
    while i < len(s):
        while i < len(s) and s[i].isspace():
            i += 1
        if i < len(s) and s[i] in "[{":
            close = "]" if s[i] == "[" else "}"
            depth, j = 0, i
            while j < len(s):
                if s[j] in "[{" and (s[j] == s[i]):
                    depth += 1
                elif s[j] == close:
                    depth -= 1
                    if depth == 0:
                        break
                elif s[j] == "{":
                    depth += 1
                elif s[j] == "}":
                    depth -= 1
                j += 1
            i = j + 1
            continue
        return i
    return i


def tabular_bodies(text: str) -> list[str]:
    """The bodies of the outermost tabulars, nested ones (a tabular inside a \\multirow cell) left inside."""
    out, pos = [], 0
    while True:
        m = _BEGIN_TAB.search(text, pos)
        if not m:
            return out
        env = m.group(1)
        start = _skip_args(text, m.end())
        depth, j = 1, start
        pat = re.compile(r"\\(begin|end)\{" + re.escape(env).replace("\\*", "\\*") + r"\}")
        end = None
        for mm in pat.finditer(text, start):
            depth += 1 if mm.group(1) == "begin" else -1
            if depth == 0:
                end = mm
                break
        if end is None:
            return out
        out.append(text[start:end.start()])
        pos = end.end()
        del j


def _flatten_nested(cell: str) -> str:
    """A tabular inside a cell (stacked header words) as its words: `\\begin{tabular}{c}fixed\\\\model\\end{tabular}`."""
    def flat(m):
        body = m.group(0)
        inner = tabular_bodies(body)
        words = re.split(r"\\\\|&", inner[0]) if inner else [body]
        return " ".join(w.strip() for w in words if w.strip())
    prev = None
    while prev != cell:
        prev = cell
        cell = re.sub(r"\\begin\{tabular\*?\}(?:(?!\\begin\{tabular).)*?\\end\{tabular\*?\}", flat, cell, flags=re.S)
    return cell


_NEWCMD = re.compile(r"\\(?:re)?newcommand\*?\s*\{?\\([A-Za-z]+)\}?\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}")
_DEF = re.compile(r"\\def\s*\\([A-Za-z]+)\s*\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}")


def expand_macros(doc: str) -> str:
    """The paper's own zero-argument macros expanded (`\\newcommand{\\model}{GraphMAE}`): a method named by a
    macro is otherwise invisible in its table (batch-5 b5b)."""
    macros = {}
    for pat in (_NEWCMD, _DEF):
        for m in pat.finditer(doc):  # the first definition wins, as \newcommand does
            macros.setdefault(m.group(1), m.group(2).replace("\\xspace", "").strip())
    if not macros:
        return doc
    body = _NEWCMD.sub("", _DEF.sub("", doc))
    names = sorted(macros, key=len, reverse=True)
    pat = re.compile(r"\\(" + "|".join(re.escape(n) for n in names) + r")(?![A-Za-z])\s?")
    for _ in range(3):  # macros defined with other macros
        new = pat.sub(lambda m: macros[m.group(1)] + " ", body)
        if new == body:
            break
        body = new
    return body


def latex_grids(doc: str) -> list[Grid]:
    doc = expand_macros(doc)
    """Every `table` environment's tabulars as grids (a table without a caption is skipped: nothing names it)."""
    out = []
    numbered = 0
    for m in _TABLE.finditer(doc):
        body = m.group(2)
        cap = _CAPTION.search(body)
        if not cap:
            continue
        numbered += 1
        caption = plain(cap.group(1))
        lab = _LABEL.search(body)
        for text in tabular_bodies(body):
            text = _flatten_nested(text)
            raw, midrule_at = [], None
            for chunk in _split_top(text, "\\\\"):
                chunk = re.sub(r"^\s*\[[^\]]*\]", "", chunk)  # \\[2pt]
                if re.search(r"\\midrule|\\hline", chunk) and midrule_at is None and raw:
                    pre = re.split(r"\\midrule|\\hline", chunk)[0]
                    if not plain(_RULE.sub("", pre)):
                        midrule_at = len(raw)
                chunk = re.sub(r"\\midrule(\[[^\]]*\])?", "", _RULE.sub("", chunk))
                cells = _split_top(chunk, "&")
                if any(plain(x) for x in cells):
                    raw.append([x.strip() for x in cells])
            g = _grid_from_rows(raw, caption, "latex", midrule_at)
            if g is not None:
                g.label = g.label or f"Table {numbered}"
                if lab:
                    g.source = f"latex:{lab.group(1)}"
                out.append(g)
    return out


def pdf_grids(pdf: str | Path) -> list[Grid]:
    """Tables PyMuPDF finds on each page, as grids (captions from the nearest "Table N" line above)."""
    import pymupdf

    out = []
    doc = pymupdf.open(str(pdf))
    for pno, page in enumerate(doc, 1):
        try:
            found = page.find_tables()
        except Exception:  # noqa: BLE001 (a page the finder can't read)
            continue
        text = page.get_text("text")
        caps = re.findall(r"(?im)^\s*(table\s*\d+[.:]?[^\n]*)", text)
        for i, t in enumerate(found.tables):
            data = t.extract()
            if not data:
                continue
            raw_rows = [[(x or "").replace("\n", " ") for x in row] for row in data]
            rows = [[make_cell(x, r, c, from_latex=False) for c, x in enumerate(row)] for r, row in enumerate(raw_rows)]
            hdr = len(t.header.names) and 1 or 0
            g = Grid(caps[i] if i < len(caps) else "", f"pdf:p{pno}", rows, hdr if hdr else _guess_header_rows(rows))
            g.header_cols = _guess_header_cols(rows, g.header_rows)
            m = re.search(r"(?i)\btable\s*(\d+)", g.caption)
            g.label = f"Table {m.group(1)}" if m else None
            out.append(g)
    return out


# ------------------------------------------------------------------------ labels and cell claims

METRICS = re.compile(r"(?i)\b(acc(uracy)?|auc|roc|f1|f-?score|micro|macro|ndcg|recall|precision|prec|mrr|hit(s|@\w+)?|"
                     r"map|ari|nmi|purity|mse|mae|rmse|mape|bleu|rouge\w*|meteor|ppl|perplexity|loss|error|err|top-?[15]|"
                     r"r@\d+|p@\d+|em|exact\s*match|spearman|pearson|kendall|r2|psnr|ssim|fid|iou|miou|dice|wer|cer|"
                     r"time|speed|throughput|latency|memory|params?)\b")


@dataclass
class Labels:
    metric_axis: str  # "col" (metrics across the top) or "row"
    method_rows: list[int]  # body rows (or columns, when metric_axis is "row") that are the paper's method
    why: str = ""


def label(g: Grid, method_names: list[str] | None = None) -> Labels:
    """Which axis holds the metrics and which rows are the paper's method: a metric lexicon on the headers; the
    paper's name for its method (or "ours"/"proposed"), else the rows holding most of the bold cells."""
    colh = [" ".join(g.col_header(c)) for c in range(g.header_cols, g.shape[1])]
    rowh = [" ".join(g.row_header(r)) for r in range(g.header_rows, g.shape[0])]
    col_hits = sum(bool(METRICS.search(h)) for h in colh)
    row_hits = sum(bool(METRICS.search(h)) for h in rowh)
    axis = "row" if row_hits > col_hits else "col"
    names = [n.lower() for n in (method_names or []) if n] + ["ours", "proposed", "our method", "(ours)"]
    method = [g.header_rows + i for i, h in enumerate(rowh) if any(n in h.lower() for n in names)]
    why = "named"
    if not method:
        bold = {}
        for r, c, cell in g.body():
            if cell.bold:
                bold[r] = bold.get(r, 0) + 1
        if bold:
            top = max(bold.values())
            method = sorted(r for r, n in bold.items() if n == top)
            why = "bold majority"
    return Labels(axis, method, why)


def cell_claims(g: Grid, labels: Labels | None = None, method_only: bool = True, prefix: str = "T") -> list[dict]:
    """Ledger-shaped claims for the numeric body cells (the method's rows only, by default): the number read from
    the grid, the metric from the metric axis, the other header path as conditions."""
    labels = labels or label(g)
    out = []
    for r, c, cell in g.body():
        if method_only and labels.method_rows and r not in labels.method_rows:
            continue
        rh, ch = g.row_header(r), g.col_header(c)
        metric_path, cond_path = (ch, rh) if labels.metric_axis == "col" else (rh, ch)
        metric = next((h for h in reversed(metric_path) if METRICS.search(h)), None)
        if metric is None:  # a sensitivity table: the headers are a setting's values, the metric is in the caption
            m = METRICS.search(g.caption)
            metric = m.group(0) if m else (metric_path[-1] if metric_path else "value")
        conds = {}
        others = [h for h in metric_path if h != metric]
        if others:
            conds["column" if labels.metric_axis == "col" else "row"] = " / ".join(others)
        if cond_path:
            conds["method" if labels.metric_axis == "col" else "dataset"] = " / ".join(cond_path)
        out.append({"id": f"{prefix}{g.label.split()[-1] if g.label else ''}r{r}c{c}", "metric": metric,
                    "reported_value": cell.value, "std": cell.std, "unit": "%" if cell.percent else "",
                    "type": "absolute", "figure_or_table": g.label or g.caption[:40], "conditions": conds,
                    "quote": cell.text, "source": f"{g.source} r{r}c{c}", "bold": cell.bold})
    return out


# ------------------------------------------------------------------------ double entry


def _close(a: float, b: float) -> bool:
    """The same number at the precision either side prints (72.93 and 72.9; 0.729 and 72.9 as percent)."""
    for x, y in ((a, b), (a * 100, b), (a, b * 100)):
        if abs(x - y) <= 0.5 * 10 ** -min(_decimals(x), _decimals(y)) + 1e-9:
            return True
    return False


def _decimals(x: float) -> int:
    s = f"{round(x, 8):.8f}".rstrip("0")
    return len(s.split(".")[1]) if "." in s else 0


def match(latex: list[Grid], pdf: list[Grid]) -> list[tuple[Grid, Grid]]:
    """Pairs of the same table: by label, else by the overlap of their numbers (at least 60%)."""
    pairs, used = [], set()
    for a in latex:
        cand = [b for b in pdf if id(b) not in used and a.label and b.label == a.label]
        if not cand:
            av = a.values()
            scored = []
            for b in pdf:
                if id(b) in used or not av:
                    continue
                bv = b.values()
                hit = sum(any(_close(x, y) for y in bv) for x in av)
                scored.append((hit / max(len(av), len(bv)), b))
            cand = [b for s, b in sorted(scored, key=lambda x: -x[0]) if s >= 0.6][:1]
        if cand:
            used.add(id(cand[0]))
            pairs.append((a, cand[0]))
    return pairs


def reconcile(a: Grid, b: Grid) -> list[dict]:
    """Cells of one table read twice that disagree: aligned by position when the shapes agree, else by headers."""
    out = []
    same_shape = a.shape == b.shape
    bmap = {}
    if not same_shape:
        for r, c, cell in b.body():
            bmap[(" ".join(b.row_header(r)).lower(), " ".join(b.col_header(c)).lower())] = cell
    for r, c, ca in a.body():
        if same_shape:
            cb = b.rows[r][c] if c < len(b.rows[r]) else None
        else:
            cb = bmap.get((" ".join(a.row_header(r)).lower(), " ".join(a.col_header(c)).lower()))
        where = {"row": " / ".join(a.row_header(r)), "col": " / ".join(a.col_header(c)), "r": r, "c": c}
        if cb is None or not cb.numeric:
            out.append({**where, "kind": "missing", "latex": ca.text, "pdf": cb.text if cb else None})
        elif not _close(ca.value, cb.value):
            out.append({**where, "kind": "differs", "latex": ca.text, "pdf": cb.text})
    return out
