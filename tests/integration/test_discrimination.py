"""Plans D2.2, D2.3 and D7.3 end to end, on new toy instances.

(a) D2.2: three settings fit the target equally (k = 10); the paper also reports k = 20 and k = 40, where only the
    truth's effect grows with k. Verification measures only its first candidate there and history matching none
    (verify_candidates = 1, point_configs = 0: equal fits outnumbering what they check); the scheduler chooses the
    runs that tell the rest apart, and the truth becomes the answer.
(b) D2.3: a decoy hits the target exactly and leaves the held-out where it was; the truth is within the noise floor
    on the target and fits the held-out. The tie on the target goes to the held-out: the truth first.
(c) D7.3: two settings fit every claim identically; the paper mentions one knob. In a tie, the mentioned one comes
    first; when the paper mentions the other, the truth is still listed as equally good and nothing is confirmed."""

import textwrap

from gapfinder.ledger.schemas import Evidence
from gapfinder.sandbox.backend import LocalBackend
from gapfinder.sandbox.events import EventLog
from gapfinder.sandbox.runner import Orchestrator
from gapfinder.sandbox.spec import HarnessSpec
from gapfinder.search.engine import GapSearch, SearchConfig, Target
from gapfinder.search.hypotheses import assumptions_from_spec

NOISE = '(int(hashlib.md5(os.environ.get("RUN_TAG", "").encode()).hexdigest(), 16) % 100 - 50) / 2000.0'
SWEEP = textwrap.dedent(f'''\
    import argparse, hashlib, os
    p = argparse.ArgumentParser()
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--wd", type=float, default=0.0005)
    p.add_argument("--drop", type=float, default=0.5)
    p.add_argument("--k", type=int, default=10)
    a = p.parse_args()
    acc = 60 + 0.5 * a.k
    acc += 3 if abs(a.lr - 0.02) < 1e-12 else 0  # flat in k
    acc += 3 * 10.0 / a.k if abs(a.drop - 0.25) < 1e-12 else 0  # shrinks with k
    acc += 3 * (a.k / 10.0) ** 2 if abs(a.wd - 0.0025) < 1e-12 else 0  # the truth: grows with k, not linearly
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("acc=%.4f\\n" % (acc + {NOISE}))
    ''')
TIE = textwrap.dedent(f'''\
    import argparse, hashlib, os
    p = argparse.ArgumentParser()
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--wd", type=float, default=0.0005)
    a = p.parse_args()
    auc, ap = 75.0, 60.0
    if abs(a.lr - 0.02) < 1e-12:
        auc, ap = auc + LR_AUC, ap + LR_AP
    if abs(a.wd - 0.0025) < 1e-12:
        auc, ap = auc + WD_AUC, ap + WD_AP
    n = {NOISE}
    os.makedirs("out", exist_ok=True)
    open("out/run.log", "w").write("auc=%.4f\\nap=%.4f\\n" % (auc + n, ap + n))
    ''')


def _search(tmp_path, src, knobs, metrics, targets, cfg=None, mention=None, conditions=()):
    art = tmp_path / "art"
    art.mkdir()
    (art / "bench.py").write_text(src, encoding="utf-8")
    flags = " ".join(f"--{k} {{{k}}}" for k in knobs)
    ks = "\n".join(f'  {k}: {{layer: config, default: "{v}"' + (", condition: true" if k in conditions else "") + "}"
                   for k, v in knobs.items())
    (tmp_path / "s.yaml").write_text(
        f'name: disc\nbase: "local:{art.as_posix()}"\nrun:\n  command: \'"${{PYTHON:-python3}}" bench.py {flags}\'\n'
        f"  output: out/run.log\n  format: kv\n  timeout: 30\nknobs:\n{ks}\nallowed_paths: [\"out/\"]\n"
        f"metrics: [{', '.join(metrics)}]\n", encoding="utf-8")
    spec = HarnessSpec.load_yaml(tmp_path / "s.yaml")
    orch = Orchestrator(LocalBackend(tmp_path / "sbx"), spec, EventLog(tmp_path / "ev.jsonl"))
    asm, _ = assumptions_from_spec(spec)
    if mention:  # the paper names the knob (not the value): "weight decay is tuned"
        asm = [a.model_copy(update={"evidence": [Evidence(kind="paper", ref="p.6", quote=mention[1])]})
               if a.knob == mention[0] else a for a in asm]
    return GapSearch(orch, targets, asm, cfg or SearchConfig(max_runs=260, trace=False, hm_disc=0.005,
                                                             patch_knobs=False, mutations=False, library_probe=False))


def _acc(k, truth=True):
    return 60 + 0.5 * k + (3 * (k / 10.0) ** 2 if truth else 0)


async def test_a_the_runs_that_tell_equal_fits_apart(tmp_path):
    targets = [Target("C1", "acc", _acc(10))] + [Target(f"K{k}", "acc", _acc(k), held_out=True, at={"k": str(k)})
                                                 for k in (20, 40)]
    # verification checks one candidate at the other conditions, history matching none: the scheduler must choose
    cfg = SearchConfig(max_runs=260, trace=False, hm_disc=0.005, patch_knobs=False, mutations=False,
                       library_probe=False, point_configs=0, verify_candidates=1)
    s = _search(tmp_path, SWEEP, {"lr": "0.01", "wd": "0.0005", "drop": "0.5", "k": "10"}, ["acc"], targets, cfg,
                conditions={"k"})  # the sweep's axis is a reported condition (plan D2.1), never searched itself
    assert "k" not in s.assumptions
    [r] = await s.run()
    assert r.changes == {"wd": "0.0025"}, (r.changes, r.notes)
    d = r.discrimination
    assert d and d["posterior"][0]["config"] == {"wd": "0.0025"} and d["posterior"][0]["posterior"] >= 0.9, d
    assert d["tests"], d  # the scheduler chose runs


def _tie(lr, wd):
    return (TIE.replace("LR_AUC", str(lr[0])).replace("LR_AP", str(lr[1]))
               .replace("WD_AUC", str(wd[0])).replace("WD_AP", str(wd[1])))


async def test_b_an_exact_hit_on_the_target_loses_to_the_held_out(tmp_path):
    src = _tie(lr=(3.0, 0.0), wd=(2.6, 3.0))  # the decoy: exact on auc, ap unchanged; the truth: auc -0.4, ap fits
    s = _search(tmp_path, src, {"lr": "0.01", "wd": "0.0005"}, ["auc", "ap"],
                [Target("C1", "auc", 78.0), Target("C2", "ap", 63.0, held_out=True)])
    [r] = await s.run()
    assert r.changes == {"wd": "0.0025"}, (r.changes, r.notes)


async def test_c_a_tie_goes_to_the_knob_the_paper_mentions(tmp_path):
    src = _tie(lr=(3.0, 3.0), wd=(3.0, 3.0))  # identical everywhere
    targets = [Target("C1", "auc", 78.0), Target("C2", "ap", 63.0, held_out=True)]
    s = _search(tmp_path, src, {"lr": "0.01", "wd": "0.0005"}, ["auc", "ap"], targets,
                mention=("wd", "weight decay is tuned on the validation set"))
    [r] = await s.run()
    assert r.changes == {"wd": "0.0025"}, (r.changes, r.notes)  # wd's change is larger, but the paper names it


async def test_c2_a_mention_is_a_weight_not_a_veto(tmp_path):
    src = _tie(lr=(3.0, 3.0), wd=(3.0, 3.0))
    targets = [Target("C1", "auc", 78.0), Target("C2", "ap", 63.0, held_out=True)]
    s = _search(tmp_path, src, {"lr": "0.01", "wd": "0.0005"}, ["auc", "ap"], targets,
                mention=("lr", "the learning rate follows the original implementation"))
    [r] = await s.run()
    assert r.changes == {"lr": "0.02"}
    assert {"wd": "0.0025"} in [e["config"] for e in r.equivalent]  # the other fit is reported as equally good
    assert r.attribution.confidence_label != "Explained"  # a mention is not the paper stating the value
