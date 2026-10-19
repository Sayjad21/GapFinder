"""Grounded operation swaps (plan item 17): the paper says ELU, the code calls ReLU; no setting fits every claim,
so the patch round tries the paper's operation, in memory, and the swap fits."""

import textwrap
from pathlib import Path

from gapfinder.ledger.schemas import Assumption
from gapfinder.sandbox import ast_patch
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.op_swaps import op_swap_leads

OPS = textwrap.dedent('''\
    import math
    def relu(x):
        return max(0.0, x)
    def elu(x):
        return x if x > 0 else math.exp(x) - 1
    ''')
MODEL = textwrap.dedent('''\
    import ops
    def forward(xs):
        return sum(ops.relu(x) for x in xs) / len(xs)
    ''')
BENCH = textwrap.dedent('''\
    import argparse, os
    import model
    p = argparse.ArgumentParser()
    p.add_argument("--alpha", type=float, default=1.0)
    a = p.parse_args()
    os.makedirs("out", exist_ok=True)
    score = 100 * a.alpha * model.forward([-1.0, -0.5, 0.5, 1.0, 2.0])
    aux = 50 * model.forward([-2.0, 1.0])
    open("out/run.log", "w").write("score=%.4f\\naux=%.4f\\n" % (score, aux))
    ''')


def _repo(root: Path) -> Path:
    root.mkdir(parents=True)
    for name, src in (("ops.py", OPS), ("model.py", MODEL), ("bench.py", BENCH)):
        (root / name).write_text(src, encoding="utf-8")
    return root


def test_leads_only_where_the_paper_names_the_other_operation(tmp_path):
    root = _repo(tmp_path / "r")
    (root / "net.py").write_text("import torch.nn as nn, torch.nn.functional as F\n"
                                 "act = nn.ReLU()\nconv = GCNConv(16, 16, aggr='add')\n", encoding="utf-8")
    leads = op_swap_leads(root, "We use ELU activations and mean aggregation over neighbours.")
    got = {(x["file"], x["name"], x["paper_value"]) for x in leads}
    assert ("model.py", "@call.relu", "elu") in got and ("net.py", "@call.ReLU", "ELU") in got
    assert ("net.py", "aggr", "'mean'") in got
    # the paper names ReLU too: no activation swap
    both = op_swap_leads(root, "Hidden layers use ReLU; the output layer uses an ELU.")
    assert not [x for x in both if x["op_family"] == "activation"]
    assert op_swap_leads(root, "We train for 100 epochs.") == []


def test_the_hook_swaps_every_call_in_the_file():
    src = "import torch.nn.functional as F\ny = F.relu(x)\nz = F.relu(y) + relu(x)\nact = F.relu\n"
    out = ast_patch.apply_source(src, 0, "@call.relu", "elu")
    assert out.count("F.elu") == 3 and "elu(x)" in out and "relu" not in out


async def test_an_operation_swap_explains_what_no_setting_can(tmp_path):
    art = _repo(tmp_path / "art")
    (tmp_path / "s.yaml").write_text(textwrap.dedent(f"""\
        name: swap
        base: "local:{art.as_posix()}"
        run:
          command: '"${{PYTHON:-python3}}" bench.py --alpha {{alpha}}'
          output: out/run.log
          format: kv
          timeout: 30
        knobs:
          alpha: {{layer: config, default: "1.0"}}
        allowed_paths: ["out/"]
        metrics: [score, aux]
        """), encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    # the paper's numbers come from ELU: score 49.5, aux 3.38 (ReLU: 70, 25)
    targets = [Target("C1", "score", 49.4954), Target("C2", "aux", 3.3834, held_out=True)]
    a = Assumption(id="A1", knob="alpha", layer="config", paper_value="unstated", candidate_values=["0.7"],
                   evidence=[], prior_score=0.5, status="unstated")
    s = GapSearch(orch, targets, [a], SearchConfig(max_runs=120, trace=False),
                  paper_text="All hidden units use the exponential linear unit (ELU).")
    [r] = await s.run()
    knob = ast_patch.knob_name("model.py", 0, "@call.relu")
    assert r.changes == {knob: "elu"}, (r.changes, r.notes)
    assert any("explained with a code patch" in n for n in r.notes)
    assert (art / "model.py").read_text(encoding="utf-8") == MODEL  # nothing on disk changed
