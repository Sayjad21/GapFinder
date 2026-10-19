"""arXiv LaTeX source (gapfinder/ingest/arxiv_source.py): tables with exact symbols, and figure data."""

import io
import tarfile

from gapfinder.ingest.arxiv_source import detect_arxiv_id, supplement, unpack

MAIN = r"""\documentclass{article}
\begin{document}
\input{sections/setup}
% a commented-out table: \begin{table}\begin{tabular}{c} 9 & 9 \\ \end{tabular}\end{table}
\begin{figure}
\begin{tikzpicture}\begin{axis}
\addplot coordinates {(1, 0.70) (2, 0.75) (4, 0.79)};
\addlegendentry{Ours}
\addplot table [x=k, y=acc] {data/curve.csv};
\addlegendentry{Baseline}
\end{axis}\end{tikzpicture}
\caption{Accuracy against $K$.}
\end{figure}
\end{document}
"""
SETUP = r"""\section{Setup}
\begin{table}[t]
\caption{Hyper-parameter settings for each dataset.}
\begin{tabular}{l|cc}
\toprule
Dataset & $\lambda_1$ & $\eta$ \\
\midrule
MovieLens & $10^{-7}$ & $0.02$ \\
\textbf{Book} & $10^{-5}$ & $10^{-3}$ \\
\bottomrule
\end{tabular}
\end{table}
"""
CSV = "k,acc\n1,0.60\n2,0.66\n4,0.70\n"


def _eprint() -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as t:
        for name, text in (("main.tex", MAIN), ("sections/setup.tex", SETUP), ("data/curve.csv", CSV)):
            data = text.encode()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            t.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def test_tables_keep_symbols_and_figures_keep_their_data(tmp_path):
    src = unpack(_eprint(), tmp_path / "src")
    text = supplement(src)
    assert "Table: Hyper-parameter settings for each dataset." in text
    assert "Book | $10^{-5}$ | $10^{-3}$" in text and "Dataset | $\\lambda_1$ | $\\eta$" in text
    assert "9 | 9" not in text  # commented out
    assert "Figure data: Accuracy against $K$." in text
    assert "Ours: (1, 0.70), (2, 0.75), (4, 0.79)" in text and "Baseline: (1, 0.60), (2, 0.66), (4, 0.70)" in text


def test_a_pdf_only_submission_has_no_source(tmp_path):
    assert unpack(b"%PDF-1.5 ...", tmp_path / "x") is None


def test_the_arxiv_id_comes_from_the_stamp_or_the_file_name():
    assert detect_arxiv_id("... arXiv:1803.03467v4 [cs.IR] 25 Aug 2018 ...") == "1803.03467v4"
    assert detect_arxiv_id("no stamp here", "2405.00946v1.pdf") == "2405.00946v1"
    assert detect_arxiv_id("nothing", "paper.pdf") is None
