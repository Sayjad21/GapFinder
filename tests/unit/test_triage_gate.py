"""Deterministic gates around Super's failure triage (real log lines from the MC Dropout v1.1 run)."""

from types import SimpleNamespace

from gapfinder.search.triage import looks_like_infra, shows_rejection

THEANO_RACE = ("    rval = __import__(module_name, {}, {}, [module_name])\nModuleNotFoundError: No module named "
               "'tmpek3zj8go'\nWARNING (theano.gof.cmodule): Removing key file /root/.theano/compiledir_Linux-7.0.6/"
               "tmpek3zj8go/key.pkl because the correspon")
RECURSION = "  File \"theano/gradient.py\", line 1279, in access_grad_cache\n    term = access_term_cache(node)[idx]\nRecursionError"
ARGPARSE = "usage: bench.py [-h] [--alpha ALPHA]\nbench.py: error: argument --alpha: invalid float value: 'two'"


def b(note):
    return SimpleNamespace(note=note)


def test_compile_cache_race_is_infra_not_a_rejection():
    assert looks_like_infra(b(THEANO_RACE)) and not shows_rejection(b(THEANO_RACE))


def test_argparse_error_is_a_rejection_not_infra():
    assert shows_rejection(b(ARGPARSE)) and not looks_like_infra(b(ARGPARSE))


def test_a_real_crash_is_neither():
    assert not looks_like_infra(b(RECURSION)) and not shows_rejection(b(RECURSION))
