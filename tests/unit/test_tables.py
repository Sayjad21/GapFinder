"""Paper tables as grids (gapfinder/ingest/tables.py, plans D3.2-D3.4)."""

from pathlib import Path

import pytest

from gapfinder.ingest.tables import Grid, cell_claims, label, latex_grids, make_cell, match, parse_number, reconcile

TEX = r"""
\begin{table*}[t]
\caption{Node classification accuracy (\%) on three datasets. Best in bold.}
\label{tab:main}
\begin{tabular}{l|ccc}
\toprule
\multirow{2}{*}{Method} & \multicolumn{3}{c}{Accuracy} \\
 & Cora & Citeseer & Pubmed \\
\midrule
GCN~\cite{kipf} & 81.5 & 70.3 & 79.0 \\
GAT & $83.0 \pm 0.7$ & 72.5$_{\pm 0.7}$ & 79.0 (0.3) \\
\textsc{GraphX} (ours) & \textbf{84.2}$^{*}$ & \textbf{73.1} & \underline{79.4} \\
MLP & -- & OOM & 1,234 \\
\bottomrule
\end{tabular}
\end{table*}
"""


def test_numbers_in_every_spelling():
    assert parse_number("72.9") == (72.9, None, False)
    assert parse_number("72.9\\%") == (72.9, None, True)
    assert parse_number("$72.9 \\pm 0.4$") == (72.9, 0.4, False)
    assert parse_number("72.9$_{\\pm 0.4}$") == (72.9, 0.4, False)
    assert parse_number("72.9 (0.4)") == (72.9, 0.4, False)
    assert parse_number("\\textbf{84.2}$^{*}$") == (84.2, None, False)
    assert parse_number("1,234") == (1234.0, None, False)
    assert parse_number(".95") == (0.95, None, False)
    for missing in ("--", "OOM", "N/A", "-", ""):
        assert parse_number(missing)[0] is None
    assert parse_number("GCN")[0] is None and parse_number("2-layer")[0] is None


def test_a_latex_table_with_spans_becomes_a_grid():
    [g] = latex_grids(TEX)
    assert g.label == "Table 1" and g.source == "latex:tab:main" and "accuracy" in g.caption.lower()
    assert g.header_rows == 2 and g.header_cols == 1 and g.shape == (6, 4)
    assert g.col_header(2) == ["Accuracy", "Citeseer"]  # the multicolumn spans every dataset
    assert g.row_header(0) == ["Method"] and g.row_header(1) == ["Method"]  # the multirow fills its second row
    gat = g.rows[3]
    assert (gat[1].value, gat[1].std) == (83.0, 0.7) and (gat[2].value, gat[2].std) == (72.5, 0.7)
    ours = g.rows[4]
    assert ours[1].bold and ours[1].value == 84.2 and ours[3].underline
    assert g.rows[5][1].value is None and g.rows[5][3].value == 1234.0


def test_labels_and_cell_claims():
    [g] = latex_grids(TEX)
    lab = label(g, ["GraphX"])
    assert lab.metric_axis == "col" and lab.method_rows == [4] and lab.why == "named"
    assert label(g).method_rows == [4] and label(g).why in ("named", "bold majority")  # "(ours)" or the bold cells
    claims = cell_claims(g, lab)
    assert [c["reported_value"] for c in claims] == [84.2, 73.1, 79.4]
    c0 = claims[0]
    assert c0["metric"] == "Accuracy" and c0["conditions"] == {"column": "Cora", "method": "GraphX (ours)"}
    assert c0["figure_or_table"] == "Table 1" and c0["bold"] and c0["unit"] == ""
    assert len(cell_claims(g, lab, method_only=False)) == 10  # every numeric body cell (3 + 3 + 3 + 1)


def _pdf_like(g: Grid, change: dict | None = None) -> Grid:
    rows = []
    for r, row in enumerate(g.rows):
        out = []
        for c, cell in enumerate(row):
            text = (change or {}).get((r, c), cell.text)
            out.append(make_cell(text, r, c, from_latex=False))
        rows.append(out)
    return Grid("Table 1: Node classification accuracy", "pdf:p5", rows, g.header_rows, g.header_cols, "Table 1")


def test_double_entry_finds_an_injected_mismatch():
    [g] = latex_grids(TEX)
    clean = _pdf_like(g)
    assert match([g], [clean]) == [(g, clean)] and reconcile(g, clean) == []
    bad = _pdf_like(g, {(4, 2): "71.3", (3, 3): "--"})
    found = {(x["r"], x["c"], x["kind"]) for x in reconcile(g, bad)}
    assert found == {(4, 2, "differs"), (3, 3, "missing")}
    rounded = _pdf_like(g, {(4, 1): "84.20", (2, 1): "0.815"})  # another precision; a fraction for a percent
    assert reconcile(g, rounded) == []


RIPPLE = Path(__file__).resolve().parents[2] / ".gf_cache" / "arxiv" / "1803.03467v4" / "ripple.tex"


@pytest.mark.skipif(not RIPPLE.exists(), reason="the cached RippleNet source (a dev-set paper)")
def test_a_real_paper_s_tables():
    grids = latex_grids(RIPPLE.read_text(encoding="utf-8", errors="replace"))
    assert grids and all(g.shape[0] >= 2 for g in grids)
    numeric = [g for g in grids if g.values()]
    assert numeric, [g.caption for g in grids]
    for g in numeric:
        assert g.header_rows >= 1 and all(isinstance(v, float) for v in g.values())


NESTED = r"""
\begin{table}[htb]
\caption{Misclassification rates (\%) under 5\% perturbed edges}
\begin{tabular}{c|c|cc}
\toprule[1pt]
\multirow{3}{*}{\begin{tabular}[c]{@{}c@{}}fixed\\natural\\ model\end{tabular}} && Cora & Citeseer \\
\cline{2-4}
&clean & $18.2 \pm 0.1$ & $28.9 \pm 0.3 $ \\
&\textbf{CE-PGD} & $\mathbf{28.0\pm 0.1}$ & $36.0\pm 0.2$ \\
\bottomrule
\end{tabular}
\end{table}
"""


def test_a_tabular_nested_in_a_cell():
    [g] = latex_grids(NESTED)
    assert g.shape == (3, 4), g.shape
    assert g.rows[1][2].value == 18.2 and g.rows[2][2].bold and g.rows[2][3].value == 36.0
    assert g.rows[1][0].text == "fixed natural model" and g.header_cols == 2
