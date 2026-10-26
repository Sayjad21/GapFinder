"""Build the web app's showcase from runs that are already recorded and scored. Nothing here runs or costs anything.

    python scripts/build_showcase.py            # writes meta.json per run and demo/runs/showcase.json

Three groups, each labelled for what it is:
- real: earlier real papers re-run post-hoc on c5 and c7 (all 16; demo/runs/real, real-c7), and some again on c8
  and c9 (real-c8, real-c9). Their causes are documented, and the engine's fixes since c5 were found on these very
  runs: a demonstration, never evidence. The tally is c7's, the one version every paper was re-run on.
- planted: planted-gap curriculum tasks a frozen version solved, copied from eval/planted/curriculum/tasks, with
  the planted change and the verdict from the scorer's own output (scores-*.json). The scorer opened the sealed
  answers; this script reads only its output.
- gapbench: GapBench dev-suite runs of c5 scored correct, one per task. The suite is the development measurement,
  so these tasks were seen while tuning.
The manifest also carries every round's full totals, misses included, so a page can show rates as well as wins.
Each case carries its gauge: the paper's number, the code's as run, and the code's after GapFinder's change.
"""

from __future__ import annotations

import collections
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demo" / "runs"
CUR = ROOT / "eval" / "planted" / "curriculum"
C5_RUNS = ROOT.parent / "gf-c5" / "eval" / "gapbench" / "runs"
COPY = ("events.jsonl", "gap_report.json", "gap_report.md", "claims.json", "assumptions.json", "prediction.json")

VERSIONS = {  # scores file run -> version, frozen date, adopted (c1 the baseline; c7 adopted on seed 8)
    "run-c5": ("c5", "2026-10-23", True), "run-c3": ("c3", "2026-10-22", True),
    "run-c2": ("c2", "2026-10-22", False), "run": ("c1", "2026-10-21", True),
    "run-c4": ("c4", "2026-10-22", False), "run-c6": ("c6", "2026-10-24", False),
    "run-c7": ("c7", "2026-10-26", True), "run-c8": ("c8", "2026-10-26", False),
    "run-c9": ("c9", "2026-10-27", False), "run-c10": ("c10", "2026-10-27", False),
}
PAPERS = {"pygcn": "pygcn (GCN, Kipf & Welling)", "fastgcn": "FastGCN", "b3a": "Variational Fair Clustering",
          "b3c": "SparseTSF", "b4a": "RippleNet", "vgae": "VGAE (graph autoencoder)"}
KIND = {"setting": "a changed setting", "scale": "a scale or unit convention", "code": "a code defect",
        "data": "a training-data cut", "reporting": "a reporting rule", "control": "no gap (a control)"}

# Verdicts, by the documented cause (each case's answer key where it has one):
#   found: the documented cause named and tested; partial: the right setting or part of it;
#   no_gap: the code reproduces the paper within its noise, and GapFinder says so;
#   missed: a gap the search did not explain, or explained with something else.
VERDICT_WORDS = {"found": "Found the documented cause", "partial": "Found part of it", "no_gap": "Correctly found no gap",
                 "missed": "Missed it"}

# slug -> title, venue, documented cause, the c7 run folder when it isn't the slug
REAL = {
    "gcn-attack": ("Topology attack on GCNs", "IJCAI 2019", "The attack budget counts each edge twice, so the code's "
                   "5% perturbs twice the paper's edges."),
    "sdcn": ("Structural Deep Clustering Network (SDCN)", "WWW 2020", "The paper reports each metric's best epoch, "
             "chosen with the test labels; the code's final epoch is lower."),
    "fastgcn-v15": ("FastGCN", "ICLR 2018", "A learning rate of 0.001 for the transductive Cora result."),
    "fair-clustering": ("Variational Fair Clustering", "AISTATS 2021", "The paper's fairness weight λ=10 is a typo; the "
                        "authors ran λ=100."),
    "ripplenet": ("RippleNet", "CIKM 2018", "Book-Crossing needs lr 1e-3 and L2 weight 1e-5, not the defaults."),
    "mc-dropout": ("Dropout as a Bayesian approximation (MC Dropout)", "ICML 2016", "The paper ran 10x the base epochs "
                   "and one hidden layer; the current code runs 500x and two."),
    "bond": ("BOND: outlier detection benchmark (DOMINANT)", "NeurIPS 2022", "A library update made the balance weight "
             "stop taking effect: 0.5 runs instead of the auto-balanced 0.84."),
    "vgae": ("Variational Graph Auto-Encoders (VGAE)", "NeurIPS 2016 workshop", "The code splits 30% / 20% of edges "
             "for test and validation; the paper used 10% / 5%."),
    "pygcn": ("pygcn, the PyTorch GCN", "ICLR 2017 (GCN)", "Splits, normalization, input dropout and first-layer-only "
              "weight decay differ from the paper's setup."),
    "patchtst": ("PatchTST", "ICLR 2023", "The test loader drops its last incomplete batch (drop_last=True)."),
    "gat": ("Graph Attention Networks (GAT)", "ICLR 2018", "PubMed used its own settings: lr 0.01, L2 0.001, 8 output "
            "heads, early stopping on loss only."),
    "sparsetsf": ("SparseTSF", "ICML 2024", "The test loader drops its last incomplete batch."),
    "at": ("Anomaly Transformer", "ICLR 2022", "A point-adjustment step the paper states is applied in evaluation."),
    "ncf": ("Neural Collaborative Filtering (NCF)", "WWW 2017", "The best epoch is picked on the test set."),
    "gmixup": ("G-Mixup", "ICML 2022", "The gain over plain GNNs is within the run-to-run noise."),
    "pyg": ("GAT vs GCN in PyTorch Geometric", "benchmark", "The ranking of GAT and GCN depends on the data split."),
}
VERSION_DIRS = {"c5": "real", "c7": "real-c7", "c8": "real-c8", "c9": "real-c9"}
TALLY_VERSION = "c7"  # every paper was re-run on it; c8 and c9 re-ran a few
RUN_DIR = {("c7", "bond"): "bond.cut2"}  # BOND on c7: three searches (48, 60, 80 runs); the 60-run one is shown

# slug -> version -> (verdict, one line): our reading of each run against the documented cause
READING = {
    "gcn-attack": {"c5": ("missed", "An unsupported dropout=0.3; the scale probe ruled out every factor."),
                   "c7": ("found", "The code's budget is 0.5x the paper's: labelled a paper-code inconsistency.")},
    "sdcn": {"c5": ("missed", "Unexplained: the old harness recorded only the final epoch."),
             "c7": ("found", "Explained by the reporting rule: each metric's best epoch, picked with the test labels.")},
    "fastgcn-v15": {"c5": ("found", "Explained: lr=0.001."), "c7": ("found", "Explained: lr=0.001.")},
    "fair-clustering": {"c5": ("found", "λ=100 fits all 8 claims; unsupported, since the paper prints 10."),
                        "c7": ("found", "λ=100 fits all 8 claims; unsupported, since the paper prints 10.")},
    "ripplenet": {"c5": ("partial", "lr=0.002 closes half the gap; the documented lr=0.001 tied and lost."),
                  "c7": ("partial", "lr=0.001, the documented value; the L2 weight is still missing."),
                  "c9": ("missed", "Unexplained: the documented lr 1e-3 and L2 1e-5 block fit closest, one run short of "
                                   "its confirmation, while 30 runs sat held for a patch round that needed none.")},
    "mc-dropout": {"c5": ("missed", "The search crashed three times before a report."),
                   "c7": ("partial", "epochx=10 and hidden=1, the documented pair: it fits Energy, breaks held-out Yacht."),
                   "c8": ("partial", "epochx=10 and hidden=1 again: Energy fits, held-out Yacht breaks.")},
    "bond": {"c5": ("missed", "Unexplained; the library probe never ran on the old harness."),
             "c7": ("partial", "The balance weight, patched 0.5 to 0.95; the key accepts 0.75-0.9. An 80-run search "
                               "missed it."),
             "c8": ("missed", "Unexplained: the balance weight at 0.95 fit the target on one run and was never repeated, "
                              "with 13 of 60 runs left.")},
    "vgae": {"c5": ("missed", "The split pair fits, but a cut made on one run demoted it."),
             "c7": ("missed", "The split constants are written `30.`, a form the value ladder couldn't read."),
             "c9": ("found", "A paper-code inconsistency: the split constants at the paper's 10% and 5% close the gap "
                             "(-5.4% to +0.3%).")},
    "pygcn": {"c5": ("missed", "weight_decay=0, unsupported."),
              "c7": ("partial", "Lists the validation split (500 vs 300) and the missing early stopping."),
              "c9": ("missed", "weight_decay=1e-5, unsupported; this time the paper-code contrast named no difference.")},
    "patchtst": {"c5": ("missed", "Unexplained."),
                 "c7": ("missed", "drop_last tested on the live line: no effect here. The target is the 512-step "
                                  "PatchTST/64; the harness runs /42."),
                 "c8": ("missed", "Unexplained, as on c7: the 512-step variant the paper reports isn't in the harness.")},
    "gat": {"c5": ("missed", "Inconclusive: the gap is under the minimum detectable effect."),
            "c7": ("no_gap", "Reproduced: this run's naive spread covers the -2.2% gap.")},
    "sparsetsf": {"c5": ("no_gap", "Reproduced within noise (-0.4%)."), "c7": ("no_gap", "Reproduced within noise.")},
    "at": {"c5": ("no_gap", "Reproduced."), "c7": ("no_gap", "Reproduced.")},
    "ncf": {"c5": ("no_gap", "Reproduced."), "c7": ("no_gap", "Reproduced.")},
    "gmixup": {"c5": ("no_gap", "Reproduced."), "c7": ("no_gap", "Reproduced.")},
    "pyg": {"c5": ("no_gap", "Reproduced."), "c7": ("no_gap", "Reproduced.")},
}
POSTHOC = ("Post-hoc rerun. The cause is documented, and the engine's fixes since c5 were found on these very runs, "
           "so this is a demonstration, not evidence. The blind record is in docs/CONTEXT_v11.md 5.1.")
BLIND = {"papers": 8, "correct": 1, "partial": 1, "missed": 5, "confidently_wrong": 1,
         "note": "Sealed blind real papers, all run before the planted curriculum (c1-c8)."}
DEV_SUITE = [  # pooled over two replicates, 138 cause runs, 114 abstentions all correct (eval/results/dev_suite_run*.json)
    {"version": "c1", "runs": [5000, 9100], "correct": 100, "adopted": True},
    {"version": "c4", "runs": [8000, 8100], "correct": 96, "adopted": False},
    {"version": "c5", "runs": [10000, 10100], "correct": 99, "adopted": True},
    {"version": "c7", "runs": [12000, 12100], "correct": 100, "adopted": True},
    {"version": "c8", "runs": [13000, 13100], "correct": 92, "adopted": False},
    {"version": "c9", "runs": [15000, 15100], "correct": 96, "adopted": False},
]


def _json(p: Path):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def _write(p: Path, obj) -> None:
    p.write_text(json.dumps(obj, indent=1, ensure_ascii=False), encoding="utf-8")


def _copy(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for f in COPY:
        if (src / f).exists():
            shutil.copyfile(src / f, dst / f)


def _rid(d: Path) -> str:
    return str(d.relative_to(DEMO)).replace("\\", "/").replace("/", "~")


def gauge(rep: dict) -> dict | None:
    """The target claim's three readings: the paper's number, the code's as run, the code's after the answer."""
    claims = [c for c in rep.get("claims", []) if not (c.get("target") or {}).get("held_out")]
    if not claims:
        return None
    c = claims[0]
    t = c["target"]
    pv, g0, g1 = t.get("paper_value"), c.get("gap_before"), c.get("gap_after")
    if pv is None or g0 is None:
        return None
    a = c.get("attribution") or {}
    return {"claim": t.get("claim_id"), "metric": t.get("metric"), "paper": pv,
            # after: the answer's reading (a reporting rule changes no setting, yet moves the number)
            "code": pv * (1 + g0), "after": None if g1 is None or abs(g1 - g0) < 1e-9 else pv * (1 + g1),
            "band": c.get("band"), "changes": c.get("changes") or {}, "label": a.get("confidence_label", "Reproduced"),
            "runs": rep.get("runs"), "quote": (t.get("quote") or (c.get("paper_claim") or {}).get("quote")),
            "figure": t.get("figure") or (c.get("paper_claim") or {}).get("figure")}


def real() -> list[dict]:
    rows = []
    for slug, (title, venue, cause) in REAL.items():
        versions = {}
        for ver, base in VERSION_DIRS.items():
            d = DEMO / base / RUN_DIR.get((ver, slug), slug)
            rep = _json(d / "gap_report.json")
            if rep is None:
                continue
            verdict, line = READING.get(slug, {}).get(ver, (None, None))
            meta = {"title": f"{title} (on {ver})", "kind": "real", "group": "real", "version": ver, "slug": slug,
                    "posthoc": True, "documented_cause": cause, "verdict": verdict, "reading": line, "note": POSTHOC}
            _write(d / "meta.json", meta)
            versions[ver] = {"id": _rid(d), "verdict": verdict, "reading": line, "gauge": gauge(rep)}
        if not versions:
            continue
        current = TALLY_VERSION if versions.get(TALLY_VERSION, {}).get("verdict") else max(
            versions, key=lambda v: (versions[v]["verdict"] is not None, int(v[1:])))
        rows.append({"slug": slug, "title": title, "venue": venue, "documented_cause": cause, "current": current,
                     "versions": versions})
    return rows


def planted() -> tuple[list[dict], list[dict]]:
    """Every gap task a frozen adopted version scored correct, newest version first, and the newest adopted version's controls."""
    best, totals = {}, []
    order = ["run-c7", "run-c5", "run-c3", "run-c2", "run"]
    for f in sorted(CUR.glob("scores-*.json")):
        s = _json(f)
        ver, frozen, adopted = VERSIONS[s["run"]]
        rows = s["rows"]
        gaps = [r for r in rows if r["kind"] != "control"]
        ctl = [r for r in rows if r["kind"] == "control"]
        seed = int(f.stem.rsplit("-s", 1)[1])
        by_kind = collections.defaultdict(list)
        for r in gaps:
            by_kind[r["kind"]].append(r)
        totals.append({"version": ver, "adopted": adopted, "seed": seed,
                       "gaps": len(gaps), "found": sum(r["verdict"] == "correct" for r in gaps),
                       "confidently_wrong": sum(r["verdict"] == "confidently wrong" for r in rows),
                       "controls": len(ctl), "controls_correct": sum(r["verdict"] == "correct" for r in ctl),
                       "by_kind": {k: [sum(r["verdict"] == "correct" for r in v), len(v)]
                                   for k, v in sorted(by_kind.items())}})
        if s["run"] not in order:
            continue
        for r in rows:
            keep = r["verdict"] == "correct" and (r["kind"] != "control" or s["run"] == order[0])
            if not keep:
                continue
            prev = best.get(r["task"])
            if prev is None or order.index(s["run"]) < order.index(prev[0]):
                best[r["task"]] = (s["run"], seed, r)
    out = []
    for task, (run, seed, r) in sorted(best.items()):
        ver, frozen, _ = VERSIONS[run]
        src = CUR / "tasks" / task / run
        if not (src / "gap_report.json").exists():
            continue
        d = DEMO / "synthetic" / "planted" / f"{task}-{ver}"
        _copy(src, d)
        case = r["case"].removesuffix("-h")
        paper = PAPERS.get(case, case) + (" (rebuilt harness)" if r["case"].endswith("-h") else "")
        what = KIND.get(r["kind"], r["kind"])
        meta = {"title": f"Planted {what} in {paper}", "kind": "planted", "group": "planted", "featured": False,
                "version": ver, "frozen": frozen, "seed": seed, "level": r["level"], "case": r["case"],
                "family": r["kind"], "planted": r["planted"], "found": r["found"], "label": r["label"],
                "verdict": r["verdict"], "tied": r.get("tied"), "rank": r.get("rr"),
                "note": (f"Synthetic: one hidden change planted into {paper}, whose code reproduces; the paper's "
                         f"numbers are the mean of 3 runs with it. Searched by {ver} (frozen {frozen}) on seed "
                         f"{seed}, scored by the curriculum's sealed scorer. A development measurement.")}
        _write(d / "meta.json", meta)
        out.append({"id": _rid(d), "gauge": gauge(_json(d / "gap_report.json")), "paper": paper,
                    **{k: meta[k] for k in ("title", "version", "seed", "family", "planted", "found", "label")}})
    return out, totals


CATEGORY = {"known_cause": "a known cause", "decoy": "a cause behind a decoy",
            "interaction": "two settings that matter only together", "no_cause": "no cause: must abstain",
            "noise_only": "noise only: must abstain", "out_of_space": "a cause outside the search space",
            "incomplete": "incomplete information: must abstain"}


def gapbench() -> tuple[list[dict], dict]:
    out, seen = [], set()
    for base in (10000, 10100):
        s = _json(ROOT / "eval" / "results" / f"dev_suite_run{base}.json")
        for r in s["rows"]:
            if r["task"] in seen or r["outcome"] not in ("correct", "correct_abstention"):
                continue
            src = C5_RUNS / r["task"] / "gapfinder" / f"run{r['run']}"
            if not (src / "gap_report.json").exists():
                continue
            seen.add(r["task"])
            d = DEMO / "synthetic" / "gapbench" / r["task"]
            _copy(src, d)
            hidden = (_json(ROOT / "eval" / "gapbench" / "tasks" / r["task"] / "answer.json") or {}).get("hidden") \
                if r["task"].startswith("dev-") else None
            found = {c: {"label": v["label"], "changes": v["knobs"]} for c, v in r["claims"].items()}
            meta = {"title": f"GapBench {r['task']}: {CATEGORY.get(r['category'], r['category'])}", "kind": "gapbench",
                    "group": "gapbench", "featured": False, "version": "c5", "category": r["category"],
                    "type": r["type"], "outcome": r["outcome"], "found": found, "hidden": hidden,
                    "gap_closed": r.get("gap_closed"),
                    "note": ("Synthetic GapBench task, searched by c5 (dev_suite_run%d, run %d) and scored correct. "
                             "These tasks are the development suite, seen while tuning." % (base, r["run"]))}
            _write(d / "meta.json", meta)
            out.append({"id": _rid(d), "gauge": gauge(_json(d / "gap_report.json")),
                        **{k: meta[k] for k in ("title", "category", "outcome", "found")}})
    s = _json(ROOT / "eval" / "results" / "dev_suite_run10000.json")
    return out, {"run": 10000, "version": "c5", "runs": s["runs"], "outcomes": s["outcomes"],
                 "by_category": s["by_category"]}


def main() -> None:
    r = real()
    p, totals = planted()
    g, suite = gapbench()
    tally = collections.Counter(x["versions"][x["current"]]["verdict"] for x in r)
    size = sum(f.stat().st_size for f in DEMO.rglob("*") if f.is_file())
    _write(DEMO / "showcase.json", {
        "note": ("Recorded runs for the web app. Real papers are post-hoc reruns; planted and GapBench cases are "
                 "development measurements. The only clean evidence is the sealed blind record (docs/CONTEXT_v11.md "
                 "5.1). Totals include every miss."),
        "verdict_words": VERDICT_WORDS, "real": r, "real_tally": dict(tally), "tally_version": TALLY_VERSION,
        "real_versions": list(VERSION_DIRS), "blind": BLIND, "dev_suite": DEV_SUITE,
        "planted": p, "planted_totals": totals, "gapbench": g, "gapbench_totals": suite})
    print(f"real {len(r)} {dict(tally)}, planted {len(p)}, gapbench {len(g)}; demo/runs {size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
