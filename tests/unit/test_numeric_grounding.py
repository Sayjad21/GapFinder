"""Plan D3.1: numeric grounding (gapfinder/ledger/grounding.py) with table grids (gapfinder/ingest/tables.py)."""

from gapfinder.ingest.tables import latex_grids
from gapfinder.ledger.grounding import Grounder, number_in_text
from gapfinder.ledger.schemas import Claim

TEX = r"""
\begin{table}
\caption{Results on CTR prediction (AUC).}
\begin{tabular}{lcc}
\toprule
Model & MovieLens-1M & Book-Crossing \\
\midrule
DKN & 0.655 & 0.621 \\
RippleNet & \textbf{0.921} & \textbf{0.729} \\
\bottomrule
\end{tabular}
\end{table}
"""
PAGE1 = ("RippleNet: propagating user preferences on the knowledge graph for recommender systems. We propose "
         "RippleNet, an end-to-end framework.")
PAGE5 = ("Table 1: Results on CTR prediction. RippleNet achieves gains of 2.0% to 40.6% in AUC over the "
         "baselines on movie recommendation. Model MovieLens-1M Book-Crossing DKN 0.655 0.621 RippleNet 0.921 0.729")


def _g(grids=True):
    pages = {1: PAGE1, 5: PAGE5}
    return Grounder(PAGE1 + "\n" + PAGE5, pages=pages, grids=latex_grids(TEX) if grids else None)


def _claim(cid, quote, value, table="Table 1", **cond):
    return Claim(id=cid, figure_or_table=table, metric="AUC", reported_value=value, conditions=cond or {},
                 type="absolute", quote=quote)


def test_numbers_in_any_spelling():
    assert number_in_text(0.921, "an AUC of 92.1% on MovieLens")
    assert number_in_text(92.1, "AUC 0.921") and number_in_text(0.92, "0.921")  # the paper's coarser precision
    assert not number_in_text(0.931, "AUC 0.921")
    assert number_in_text(40.6, "gains of 2.0% to 40.6% in AUC")


def test_a_number_the_model_wrote_is_dropped_even_when_the_quote_is_real():
    rep = _g().check_claims([_claim("C1", "RippleNet achieves gains of 2.0% to 40.6% in AUC", 0.957)])
    assert not rep.kept and "not in its quote, its page or its table" in rep.dropped[0][1]


def test_true_claims_are_kept_and_recovered():
    claims = [
        _claim("C1", "RippleNet achieves gains of 2.0% to 40.6% in AUC", 40.6),  # verbatim, number in the quote
        _claim("C2", "Results on CTR prediction", 0.921, dataset="MovieLens-1M", model="RippleNet"),  # on the page
        _claim("C3", "RippleNet achieves gain of 2.0% to 40.6% in AUC over baselines on movie recommendations", 40.6),
        _claim("C4", "RippleNet reaches 0.729 AUC on books", 0.729, dataset="Book-Crossing"),  # paraphrase: its cell
    ]
    rep = _g().check_claims(claims)
    kept = {c.id: c for c in rep.kept}
    assert set(kept) == {"C1", "C2", "C3", "C4"}, rep.dropped
    assert kept["C2"].page == 5
    how = dict(rep.recovered)
    assert "similarity" in how["C3"] and "Table 1" in how["C4"] and "Book-Crossing" in how["C4"]


def test_without_the_table_a_paraphrase_with_no_number_is_still_dropped():
    rep = _g(grids=False).check_claims([_claim("C4", "RippleNet reaches 0.729 AUC on books", 0.729,
                                               dataset="Book-Crossing")])
    assert not rep.kept


def test_a_number_in_an_unnamed_table_under_none_of_its_conditions_is_not_taken():
    rep = _g().check_claims([_claim("C5", "an invented sentence about something else entirely", 0.655, table=None,
                                    dataset="Yelp")])
    assert not rep.kept


def test_suffixes_powers_and_unicode_minus():
    assert number_in_text(920.0, "SparseTSF (Ours) 0.92 K") and number_in_text(6310000.0, "PatchTST 6.31 M")
    assert not number_in_text(930.0, "0.92 K")
    assert number_in_text(0.0001, "a learning rate of 1e−4") and number_in_text(0.0001, "lr = 10−4")
    assert number_in_text(0.005, "5 x 10^{-3}") and number_in_text(0.0001, "10^{-4}")
    assert not number_in_text(0.957, "Table 1")  # an integer is only that integer
