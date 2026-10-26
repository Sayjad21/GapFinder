"""c7 (E): static leads on code the dry run executed rank first, before the cut. A vendored copy of a module and the
defaults of functions the run never calls had taken the slots, sorted by file path (PatchTST and BOND c5 reruns)."""

from gapfinder.ingest.code_checks import code_checks, coverage

LOADER = '''\
def data_provider(flag, dataset):
    if flag == 'test':
        drop_last = True
    else:
        drop_last = False
    return DataLoader(dataset, drop_last=drop_last)
'''

DETECTOR = '''\
def build(weight=0.5, hid=64):
    model = {"weight": weight}
    return model


def run():
    return build()
'''


def _repo(tmp_path):
    for rel in ("Aaa_vendored/data_provider/data_factory.py", "main_pkg/data_provider/data_factory.py"):
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(LOADER, encoding="utf-8")
    for rel in ("lib/detector/adone.py", "lib/detector/dominant.py"):
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(DETECTOR, encoding="utf-8")
    return tmp_path


def test_a_live_copy_ranks_before_a_dead_one(tmp_path):
    root = _repo(tmp_path)
    # the run imported the main package's loader (its train branch only) and never the vendored copy
    executed = {"main_pkg/data_provider/data_factory.py": [1, 2, 4, 5, 6]}
    leads = [x for x in code_checks(root, executed=executed, limit=80) if x.family == "eval_switch"]
    assert leads[0].file == "main_pkg/data_provider/data_factory.py", [(x.file, x.line) for x in leads]
    without = [x for x in code_checks(root, limit=80) if x.family == "eval_switch"]
    assert without[0].file.startswith("Aaa_vendored")  # c5's order: by path


def test_a_default_counts_as_used_when_its_body_ran(tmp_path):
    root = _repo(tmp_path)
    # both modules were imported (their def lines ran); only dominant's builder body ran
    executed = {"lib/detector/adone.py": [1, 6], "lib/detector/dominant.py": [1, 2, 3, 6, 7]}
    leads = [x for x in code_checks(root, executed=executed, limit=80) if x.name == "weight"]
    assert [x.file for x in leads][:1] == ["lib/detector/dominant.py"], [(x.file, x.line) for x in leads]
    assert coverage(leads[0], executed) == 0 and coverage(leads[1], executed) == 1


def test_without_a_trace_the_order_is_unchanged(tmp_path):
    root = _repo(tmp_path)
    assert [(x.file, x.line, x.family) for x in code_checks(root, limit=80)] == \
           [(x.file, x.line, x.family) for x in code_checks(root, limit=80, executed=None)]


def test_g_the_value_the_paper_states_for_the_targets_dataset():
    """c7 (G): a ledger value listed per dataset gives the target's own; a plain one applies everywhere."""
    from gapfinder.search.engine import _stated_for

    words = {"gat", "pubmed", "acc"}
    assert _stated_for("0.01 (Pubmed), 0.005 (Cora, Citeseer, PPI)", words) == "0.01"
    assert _stated_for("8 (transductive first layer), 8 (Pubmed output), 4 (inductive first layers)", words) == "8"
    assert _stated_for("True (inductive), False (transductive implied)", words) is None
    assert _stated_for("0.6", words) == "0.6"
    assert _stated_for("unstated", words) is None
    assert _stated_for("cross-entropy loss and accuracy (transductive)", words) is None
