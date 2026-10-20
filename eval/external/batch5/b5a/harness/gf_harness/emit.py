# written by `gapfinder harness`: each claim's number from every run's log (out/run*.log), averaged over the
# cell's runs. The labels were bound from the smoke run (HARNESS.md); a label a run doesn't print is left out.
from __future__ import print_function
import glob, io, re
BIND = {'c_t3_5_acc': ('test accuracy', 1.0), 'c_t3_5_acc__0': ('val_acc', 1.0), 'c_t3_5_acc__1': ('val accuracy', 1.0), 'c_t3_5_acc__2': ('train accuracy', 1.0)}
PAIR = re.compile('([A-Za-z][\\w@./ -]{0,40}?)\\s*[:=]\\s*([-+]?\\d+(?:\\.\\d+)?(?:[eE][-+]?\\d+)?)\\s*(%?)')
QUAL = re.compile('(?i)\\b(test|testing|val|valid|validation|dev|eval|train|training|best)\\b')
PREFIX = re.compile('(?i)^(?:epoch|step|iter|iteration|round|run|seed)\\s*\\d+\\S*\\s*')


def qual_of(w):
    w = w.lower()
    return "test" if w.startswith("test") else "train" if w.startswith("train") else "best" if w == "best" else "val"


def labelled(log, tail_lines=40):
    found = {}
    for line in log.splitlines()[-tail_lines:]:
        best = bool(re.search(r"(?i)\bbest\b", line))
        for m in PAIR.finditer(line):
            raw = PREFIX.sub("", " ".join(m.group(1).split()).strip(" -"))
            quals = [qual_of(q.group(1)) for q in QUAL.finditer(line[: m.end(1)]) if q.group(1).lower() != "best"]
            base = " ".join(QUAL.sub("", raw).split()).strip(" -_:")
            if not base:
                continue
            key = " ".join((["best"] if best else []) + ([quals[-1]] if quals else []) + [base])
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


vals = {}
runs = 0
for f in sorted(glob.glob("out/run*.log")):
    text = io.open(f, encoding="utf-8", errors="replace").read()
    found = labelled(text)
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
print("gf_runs=%d" % runs)
