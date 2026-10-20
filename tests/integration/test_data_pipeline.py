"""Plan D1.6 end to end: data-pipeline causes found by the mutation round, on new toy pipelines.

(a) The paper's numbers were computed with the last incomplete test batch dropped; the released code keeps it (its
    loader leaves `drop_last` at the default). No setting moves the numbers; the loader switch fits every claim.
(b) The code fits its scaler on all the data; the paper's numbers come from a scaler fit on the train split.
Both are code leads (an in-memory edit that fits every claim), never "Explained"."""

import textwrap

from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec

BENCH = textwrap.dedent('''\
    import argparse, hashlib, os
    import data
    p = argparse.ArgumentParser()
    p.add_argument("--lr", type=float, default=0.01)
    a = p.parse_args()
    noise = (int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 50000.0
    lr_used = a.lr
    m = data.run()
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("auc=%.5f\\nap=%.5f\\n" % (50 + 5 * m + noise, 40 + 4 * m + noise))
    ''')
LOADER = textwrap.dedent('''\
    def DataLoader(items, batch_size=1, shuffle=False, drop_last=False):
        batches = [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
        if drop_last and batches and len(batches[-1]) < batch_size:
            batches = batches[:-1]
        return batches

    def run():
        X = [i / 10.0 for i in range(100)]
        X_test = X[80:]
        test_loader = DataLoader(X_test, batch_size=8)
        seen = [x for b in test_loader for x in b]
        return sum(seen) / len(seen)
    ''')
SCALER = textwrap.dedent('''\
    class StandardScaler:
        def fit(self, X):
            self.m = sum(X) / len(X)
            return self
        def transform(self, X):
            return [x - self.m for x in X]

    def run():
        X = [i / 10.0 for i in range(100)]
        X_train, X_test = X[:80], X[80:]
        scaler = StandardScaler().fit(X)
        t = scaler.transform(X_test)
        return sum(t) / len(t)
    ''')


def _search(tmp_path, data_src: str, targets):
    art = tmp_path / "art"
    art.mkdir()
    (art / "bench.py").write_text(BENCH, encoding="utf-8")
    (art / "data.py").write_text(data_src, encoding="utf-8")
    (tmp_path / "s.yaml").write_text(textwrap.dedent(f"""\
        name: data
        base: "local:{art.as_posix()}"
        run:
          command: '"${{PYTHON:-python3}}" bench.py --lr {{lr}}'
          output: out/run.log
          format: kv
          timeout: 30
        knobs:
          lr: {{layer: config, default: "0.01"}}
        allowed_paths: ["out/"]
        metrics: [auc, ap]
        """), encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    return GapSearch(orch, targets, asm, SearchConfig(max_runs=200, trace=False, hm_disc=0.005, patch_knobs=False))


def _scores(m):
    return 50 + 5 * m, 40 + 4 * m


async def test_a_the_last_test_batch_dropped(tmp_path):
    first16 = [i / 10.0 for i in range(80, 96)]
    auc, ap = _scores(sum(first16) / 16)
    s = _search(tmp_path, LOADER, [Target("C1", "auc", auc), Target("C2", "ap", ap, held_out=True)])
    [r] = await s.run()
    assert any("@mut." in k and "kwset.drop_last" in k for k in r.changes), (r.changes, r.notes)
    assert r.attribution.confidence_label == "Fits but unsupported"
    assert any("a code lead, not a confirmed cause" in n for n in r.notes)


async def test_b_a_scaler_fit_on_everything(tmp_path):
    train_mean = sum(i / 10.0 for i in range(80)) / 80
    auc, ap = _scores(sum(i / 10.0 for i in range(80, 100)) / 20 - train_mean)
    s = _search(tmp_path, SCALER, [Target("C1", "auc", auc), Target("C2", "ap", ap, held_out=True)])
    [r] = await s.run()
    assert any("@mut." in k and ".Call.arg.0." in k for k in r.changes), (r.changes, r.notes)
    assert any("StandardScaler().fit(X_train)" in n for n in r.notes), r.notes
    assert r.attribution.confidence_label == "Fits but unsupported"
