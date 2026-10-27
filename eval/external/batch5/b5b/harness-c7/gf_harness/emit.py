# written by `gapfinder harness`: each claim's number from every run's log (out/run*.log), averaged over the
# cell's runs. The labels were bound from the smoke run (HARNESS.md); a label a run doesn't print is left out.
from __future__ import print_function
import glob, io, re
BIND = {'c_q_acc': ('Q acc', 100.0), 'c_q_acc__0': ('P acc', 100.0), 'c_q_acc__1': ('Q acc', 100.0), 'c_q_acc__2': ('Z acc', 100.0), 'c_q_ari': ('Q ari', 100.0), 'c_q_ari__0': ('P ari', 100.0), 'c_q_ari__1': ('Q ari', 100.0), 'c_q_ari__2': ('Z ari', 100.0), 'c_q_f1': ('Q f1', 100.0), 'c_q_f1__0': ('P f1', 100.0), 'c_q_f1__1': ('Q f1', 100.0), 'c_q_f1__2': ('Z f1', 100.0), 'c_q_nmi': ('Q nmi', 100.0), 'c_q_nmi__0': ('P nmi', 100.0), 'c_q_nmi__1': ('Q nmi', 100.0), 'c_q_nmi__2': ('Z nmi', 100.0), 'c_z_acc': ('Z acc', 100.0), 'c_z_acc__0': ('P acc', 100.0), 'c_z_acc__1': ('Q acc', 100.0), 'c_z_acc__2': ('Z acc', 100.0), 'c_z_ari': ('Z ari', 100.0), 'c_z_ari__0': ('P ari', 100.0), 'c_z_ari__1': ('Q ari', 100.0), 'c_z_ari__2': ('Z ari', 100.0), 'c_z_f1': ('Z f1', 100.0), 'c_z_f1__0': ('P f1', 100.0), 'c_z_f1__1': ('Q f1', 100.0), 'c_z_f1__2': ('Z f1', 100.0), 'c_z_nmi': ('Z nmi', 100.0), 'c_z_nmi__0': ('P nmi', 100.0), 'c_z_nmi__1': ('Q nmi', 100.0), 'c_z_nmi__2': ('Z nmi', 100.0)}
TRAJ = {'c_q_acc': {'label': 'Q acc', 'scale': 100.0, 'dir': 1, 'val': None, 'target': False}, 'c_q_ari': {'label': 'Q ari', 'scale': 100.0, 'dir': 1, 'val': None, 'target': False}, 'c_q_f1': {'label': 'Q f1', 'scale': 100.0, 'dir': 1, 'val': None, 'target': False}, 'c_q_nmi': {'label': 'Q nmi', 'scale': 100.0, 'dir': 1, 'val': None, 'target': False}, 'c_z_acc': {'label': 'Z acc', 'scale': 100.0, 'dir': 1, 'val': None, 'target': True}, 'c_z_ari': {'label': 'Z ari', 'scale': 100.0, 'dir': 1, 'val': None, 'target': False}, 'c_z_f1': {'label': 'Z f1', 'scale': 100.0, 'dir': 1, 'val': None, 'target': False}, 'c_z_nmi': {'label': 'Z nmi', 'scale': 100.0, 'dir': 1, 'val': None, 'target': False}}  # claim metric -> {"label", "scale", "dir": 1 higher is better / -1 lower, "val": validation label}
PAIR = re.compile('([A-Za-z][\\w@./ -]{0,40}?)\\s*[:=]\\s*([-+]?\\d+(?:\\.\\d+)?(?:[eE][-+]?\\d+)?)\\s*(%?)')
QUAL = re.compile('(?i)\\b(test|testing|val|valid|validation|dev|eval|train|training|best)\\b')
PREFIX = re.compile('(?i)^(?:epoch|step|iter|iteration|round|run|seed)\\s*\\d+\\S*\\s*')
BARE = re.compile('(?<![\\w.])([A-Za-z][\\w@-]{0,15})\\s+([-+]?\\d*\\.\\d+(?:[eE][-+]?\\d+)?)(%?)(?![\\w.])')
LINE_TAG = re.compile('^\\s*\\d*([A-Za-z][\\w-]{0,7})?\\s*:(?=\\s*[A-Za-z])')
SYNONYMS = [('acc', ['acc', 'accuracy', 'top-1', 'top1']), ('auc', ['auc', 'roc', 'roc_auc', 'rocauc']), ('f1', ['f-score', 'f1', 'f1score', 'f_score', 'fscore']), ('ap', ['ap', 'average_precision', 'averageprecision', 'avgprecision']), ('precision', ['prec', 'precision']), ('nmi', ['nmi']), ('ari', ['ari']), ('recall', ['rec', 'recall']), ('mse', ['mse']), ('mae', ['mae']), ('rmse', ['rmse']), ('ndcg', ['ndcg']), ('hr', ['hit', 'hr']), ('map', ['map']), ('mrr', ['mrr']), ('loss', ['loss']), ('bleu', ['bleu']), ('ppl', ['perplexity', 'ppl'])]


def family(label):
    low = label.lower().replace("-", " ")
    if re.search(r"\bmean\s+average\s+precision\b", low):
        return "map"
    text = re.sub(r"\b(average|avg)\s+precision\b", "averageprecision", low)
    toks = re.findall(r"[a-z0-9@]+", text)
    for fam, syn in SYNONYMS:
        if any(t in syn or t.split("@")[0] in syn for t in toks):
            return fam
    return None


def qual_of(w):
    w = w.lower()
    return "test" if w.startswith("test") else "train" if w.startswith("train") else "best" if w == "best" else "val"


def labelled(log, tail_lines=40):
    found = {}
    for line in log.splitlines()[-tail_lines:]:
        best = bool(re.search(r"(?i)\bbest\b", line))
        t = LINE_TAG.match(line)
        tag = t.group(1) if t and t.group(1) and not QUAL.match(t.group(1) + "$") else None
        if tag:
            line = line[t.end():]
        spans = []
        for m in BARE.finditer(line):
            if family(m.group(1)) is None:
                continue
            spans.append((m.start(), m.end()))
            quals = [qual_of(q.group(1)) for q in QUAL.finditer(line[: m.end(1)]) if q.group(1).lower() != "best"]
            key = " ".join((["best"] if best else []) + ([quals[-1]] if quals else []) + ([tag] if tag else [])
                           + [m.group(1)])
            found[key] = float(m.group(2)) / (100 if m.group(3) else 1)
        for m in PAIR.finditer(line):
            if any(a <= m.start(2) < b for a, b in spans):
                continue
            raw = PREFIX.sub("", " ".join(m.group(1).split()).strip(" -"))
            quals = [qual_of(q.group(1)) for q in QUAL.finditer(line[: m.end(1)]) if q.group(1).lower() != "best"]
            base = " ".join(QUAL.sub("", raw).split()).strip(" -_:")
            if not base:
                continue
            key = " ".join((["best"] if best else []) + ([quals[-1]] if quals else []) + ([tag] if tag else [])
                           + [base])
            found[key] = float(m.group(2)) / (100 if m.group(3) else 1)
    return found


EPOCH = re.compile(r"(?i)\bepoch\s*[:#\[]?\s*(\d+)")


def per_epoch(log):
    """epoch -> labels printed on that epoch's lines (a learning curve's points)."""
    out = {}
    for line in log.splitlines():
        m = EPOCH.search(line)
        if m:
            out.setdefault(int(m.group(1)), {}).update(labelled(line, 1))
    return out


def series(log):
    """label -> every value it printed, in order (one per epoch when the program prints per epoch)."""
    out = {}
    for line in log.splitlines():
        for k, v in labelled(line, 1).items():
            out.setdefault(k, []).append(v)
    return out


def trajectory_stats(s, t):
    """One run's trajectory of a claim's label: the final value, the best (in the metric's direction) and where,
    the test value at the best validation value, the mean of the last five."""
    xs = [v * t["scale"] for v in s.get(t["label"], [])]
    if not xs:
        return None
    d = t["dir"]
    i = max(range(len(xs)), key=lambda j: d * xs[j])
    out = {"best": xs[i], "argbest": i + 1, "len": len(xs), "last5": sum(xs[-5:]) / len(xs[-5:]), "final": xs[-1],
           "_xs": xs, "_i": i}
    vs = s.get(t["val"] or "", [])
    if t["val"] and len(vs) == len(xs) and len(xs) > 1:
        k = max(range(len(vs)), key=lambda j: d * vs[j])
        out["bestval"] = xs[k]
        out["_k"] = k
    return out


vals = {}
stats = {}
curve_acc = {}
runs = 0
for f in sorted(glob.glob("out/run*.log")):
    text = io.open(f, encoding="utf-8", errors="replace").read()
    found = labelled(text)
    if TRAJ:
        ser = series(text)
        got = dict((name, trajectory_stats(ser, TRAJ[name])) for name in TRAJ)
        tname = [n for n in TRAJ if TRAJ[n].get("target")]
        tst = got.get(tname[0]) if tname else None
        for name in TRAJ:
            st = got[name]
            if st is None:
                continue
            if tst is not None and name != tname[0] and st["len"] == tst["len"] and st["len"] > 1:
                st["attarget"] = st["_xs"][tst["_i"]]  # this claim at the epoch where the target is best
                if "_k" in tst:  # ... and where the target's validation score is best (early stopping)
                    st["atbestval"] = st["_xs"][tst["_k"]]
            stats.setdefault(name, []).append(st)
            if TRAJ[name].get("target"):  # the target per epoch (plan D7.7)
                for e, x in enumerate(st["_xs"], 1):
                    if e <= 100 or (e <= 1000 and e % 10 == 0) or e % 100 == 0:
                        curve_acc.setdefault((name, e), []).append(x)
    curve = None
    hit = False
    for name in sorted(BIND):
        b = BIND[name]
        if len(b) == 3:  # (label, scale, epoch): the paper's epoch e, counted from 1
            if curve is None:
                curve = per_epoch(text)
            e = b[2] - (1 if curve and min(curve) == 0 else 0)
            if e in curve and b[0] in curve[e]:
                vals.setdefault(name, []).append(curve[e][b[0]] * b[1])
        elif b[0] in found:
            vals.setdefault(name, []).append(found[b[0]] * b[1])
            hit = True
    runs += hit
for name in sorted(vals):
    print("%s=%.6g" % (name, sum(vals[name]) / len(vals[name])))
for name in sorted(stats):  # reporting-rule statistics (plan D1.2): the cell's mean of each, and across its runs
    rs = stats[name]
    for key in ("best", "argbest", "len", "last5", "bestval", "attarget", "atbestval"):
        xs = [r[key] for r in rs if key in r]
        if xs:
            print("%s__x_%s=%.6g" % (name, key, sum(xs) / len(xs)))
    finals = sorted(r["final"] for r in rs)
    print("%s__x_maxrun=%.6g" % (name, finals[-1]))
    print("%s__x_minrun=%.6g" % (name, finals[0]))
    m = len(finals)
    print("%s__x_medrun=%.6g" % (name, (finals[m // 2] + finals[(m - 1) // 2]) / 2.0))
for (name, e) in sorted(curve_acc):  # a run cut early is compared with the as-run curve at its last epoch
    xs = curve_acc[(name, e)]
    print("%s__x_e%d=%.6g" % (name, e, sum(xs) / len(xs)))
print("gf_runs=%d" % runs)
