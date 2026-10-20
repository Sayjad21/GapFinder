"""Paper terms to code flags (gapfinder/ingest/links.py, plans D4.1, D4.3)."""

import textwrap
from types import SimpleNamespace

from gapfinder.ingest.links import Entity, covers, decisive, entities, expand, help_texts, link, role_ok, term_role, tokens
from gapfinder.sandbox.spec import Knob

TRAIN = textwrap.dedent('''\
    import argparse
    import tensorflow as tf
    flags = tf.app.flags
    flags.DEFINE_float('l2_coef', 0.0005, 'Weight for L2 loss on embedding matrix.')
    p = argparse.ArgumentParser()
    p.add_argument("--hid_units", type=int, default=8, help="number of hidden units per attention head")
    p.add_argument("--n_heads", type=int, default=8, help="number of attention heads")
    p.add_argument("--lr", type=float, default=0.005, help="learning rate")
    p.add_argument("--weight", type=float, default=0.5, help="class weight of the positive class in the loss")
    ''')


def _spec(**defaults):
    return SimpleNamespace(knobs={k: Knob(layer="config", default=v) for k, v in defaults.items()})


def test_tokens_and_the_lexicon():
    assert tokens("numAttentionHeads") == ["num", "attention", "heads"]
    assert tokens("λ_1 = 0.5") == ["lambda", "1", "0", "5"]
    assert "rate" in expand(["lr"]) and "decay" in expand(["wd"])


def test_help_texts_from_argparse_and_tf_flags(tmp_path):
    (tmp_path / "train.py").write_text(TRAIN, encoding="utf-8")
    h = help_texts(tmp_path)
    assert h["l2_coef"].startswith("Weight for L2") and h["hid_units"].startswith("number of hidden units")


def test_retrieval_ranks_by_meaning(tmp_path):
    (tmp_path / "train.py").write_text(TRAIN, encoding="utf-8")
    ents = entities(_spec(l2_coef="0.0005", hid_units="8", n_heads="8", lr="0.005", weight="0.5"), tmp_path)
    assert link("learning_rate", "We use Adam with a learning rate of 0.005", ents)[0].knob == "lr"
    assert link("l2_reg_lambda", "L2 regularization with lambda = 0.0005", ents)[0].knob == "l2_coef"
    assert link("features_per_head", "K = 8 attention heads computing 8 features each", ents)[0].knob in ("hid_units", "n_heads")


def test_a_decisive_link_must_cover_the_term():
    e = Entity("train_epochs", toks=expand(tokens("train_epochs")) * 2)
    assert covers("n_epochs_finetune", e) is False and covers("epochs", e) is True
    assert covers("l2_reg_lambda", Entity("l2_coef")) and covers("readout function (sum vs mean)", Entity("graph_pooling_readout"))
    assert decisive(link("n_epochs_pretrain", "", [e]), [e]) is None


def test_roles_from_words_and_the_name_decoy():
    assert term_role("weight decay") == "rate0" and term_role("learning rate") == "rate"
    assert term_role("dropout rate p = 0.6") == "fraction" and term_role("hidden size") == "size"
    # a flag named like the term that feeds something else: the trace saw `weight` reach no optimizer's
    # weight_decay but a loss's class weight (recorded here as another role), so the link is dropped
    decoy = Entity("weight", "class weight", "0.5", role="fraction", toks=expand(tokens("weight")) * 2)
    real = Entity("l2", "L2 regularisation", "0.0005", role="rate0", toks=expand(tokens("l2 regularisation")) * 2)
    assert role_ok("weight decay", decoy) is False and role_ok("weight decay", real) is True
    got = link("weight decay", "", [decoy, real])
    assert [c.knob for c in got] == ["l2"]
    assert role_ok("weight decay", Entity("wd")) is None  # no traced role: not decided here
