"""Grounded operation swaps (plan item 17, docs/CONTEXT_v11.md section 7): the paper names one operation and the
code uses another of the same kind.

The patch round could already swap a hard-coded number. Some reported gaps come from a different operation:
the paper says ELU and the code calls ReLU; mean pooling against a sum; min-max scaling against z-scores; SGD
against Adam. A swap is a lead only when the paper grounds it:
- the paper names member B of a family of interchangeable operations;
- the code calls member A of the same family (a call, a class, or a string keyword such as `aggr="add"`);
- the paper never names A (a paper that names both uses both, e.g. ReLU hidden layers and a sigmoid output).

The swap is file-wide (every call of A in that file becomes B: an operation choice is a design decision, not
one line), tested in memory by the patch hook, and only in the patch round (no setting fits every claim). The
only value tried is the paper's. It is reported as a code change, never as "Explained".

Families are pairs of drop-in replacements (the same arguments work for both); calls used for many unrelated
things (`.sum()`, `max()`) are not in them.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

# family -> member -> (paper regex, code spellings). Spellings with the same index across members of one
# family are each other's replacements in the same style (functional, class, keyword string)
FAMILIES: dict[str, dict[str, tuple[str, list[str]]]] = {
    "activation": {
        "relu": (r"\bReLUs?\b|rectified linear", ["relu", "ReLU", "'relu'"]),
        "elu": (r"\bELUs?\b|exponential linear", ["elu", "ELU", "'elu'"]),
        "leaky_relu": (r"\bleaky[- ]?ReLUs?\b", ["leaky_relu", "LeakyReLU", "'leaky_relu'"]),
        "gelu": (r"\bGELUs?\b", ["gelu", "GELU", "'gelu'"]),
        "tanh": (r"\btanh\b|hyperbolic tangent", ["tanh", "Tanh", "'tanh'"]),
        "selu": (r"\bSELUs?\b|scaled exponential", ["selu", "SELU", "'selu'"]),
    },
    "pooling": {
        "sum": (r"\b(sum|add|additive|summation)[- ](pool\w*|aggregat\w*|readout)", ["global_add_pool", "SumPooling", "'add'", "'sum'"]),
        "mean": (r"\b(mean|average|averag\w+)[- ](pool\w*|aggregat\w*|readout)", ["global_mean_pool", "AvgPooling", "'mean'", "'mean'"]),
        "max": (r"\bmax(imum)?[- ](pool\w*|aggregat\w*|readout)", ["global_max_pool", "MaxPooling", "'max'", "'max'"]),
    },
    "pool2d": {
        "avg": (r"\b(average|avg|mean)[- ]pool", ["avg_pool2d", "AvgPool2d", "avg_pool1d", "AvgPool1d"]),
        "max": (r"\bmax[- ]pool", ["max_pool2d", "MaxPool2d", "max_pool1d", "MaxPool1d"]),
    },
    "scaler": {
        "standard": (r"\bz[- ]?scores?\b|\bstandardi[sz]", ["StandardScaler"]),
        "minmax": (r"\bmin[- ]?max (normali[sz]\w*|scal\w*)", ["MinMaxScaler"]),  # not "min-max optimisation"
        "robust": (r"\brobust scal", ["RobustScaler"]),
    },
    "optimizer": {
        "adam": (r"\bAdam\b(?!W)", ["Adam", "'adam'"]),
        "adamw": (r"\bAdamW\b", ["AdamW", "'adamw'"]),
        "sgd": (r"\bSGD\b|stochastic gradient descent", ["SGD", "'sgd'"]),
        "rmsprop": (r"\bRMS ?[Pp]rop\b", ["RMSprop", "'rmsprop'"]),
        "adagrad": (r"\bAda[Gg]rad\b", ["Adagrad", "'adagrad'"]),
    },
    "init": {
        "xavier_uniform": (r"\b(Xavier|Glorot)\b[^.]{0,30}\buniform\b|\buniform\b[^.]{0,30}\b(Xavier|Glorot)\b",
                           ["xavier_uniform_", "glorot_uniform"]),
        "xavier_normal": (r"\b(Xavier|Glorot)\b[^.]{0,30}\bnormal\b|\bnormal\b[^.]{0,30}\b(Xavier|Glorot)\b",
                          ["xavier_normal_", "glorot_normal"]),
        "kaiming_uniform": (r"\b(He|Kaiming)\b[^.]{0,30}\buniform\b", ["kaiming_uniform_", "he_uniform"]),
        "kaiming_normal": (r"\b(He|Kaiming)\b[^.]{0,30}\bnormal\b", ["kaiming_normal_", "he_normal"]),
    },
    "regression_loss": {
        "mse": (r"\bMSE\b|mean squared error|\bL2 loss", ["MSELoss", "mse_loss", "'mse'"]),
        "mae": (r"\bMAE\b|mean absolute error|\bL1 loss", ["L1Loss", "l1_loss", "'mae'"]),
        "huber": (r"\bHuber\b|smooth L1", ["SmoothL1Loss", "smooth_l1_loss", "'huber'"]),
    },
}
# keywords whose string value names an operation (aggr="add", activation="relu", optimizer="adam")
STRING_KEYWORDS = {"aggr", "aggregation", "reduce", "readout", "pooling", "pool", "activation", "act", "optimizer",
                   "optim", "loss", "nonlinearity", "global_pool", "graph_pooling", "neighbor_aggr"}


def _sentence(text: str, m: re.Match) -> str:
    s = text.rfind(".", 0, m.start()) + 1
    e = text.find(".", m.end())
    return " ".join(text[s: e + 1 if e > 0 else m.end() + 80].split())[:300]


def _calls(tree: ast.AST) -> list[tuple[int, str, str]]:
    """(line, name, kind) for every call's function name (`F.relu(x)`: relu; `nn.ReLU()`: ReLU; `relu(x)`: relu),
    every attribute reference (`act=F.relu`), and every keyword string (`aggr="add"`: 'add', keyword aggr)."""
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                out.append((n.lineno, f.id, "call"))
            for kw in n.keywords:
                if kw.arg in STRING_KEYWORDS and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                    out.append((n.lineno, f"'{kw.value.value.lower()}'", "kw:" + kw.arg))
        elif isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Load):
            out.append((n.lineno, n.attr, "call"))
    return out


def op_swap_leads(root: str | Path, paper_text: str, files: list[str] | None = None, limit: int = 6) -> list[dict]:
    """Patch leads for operation swaps the paper grounds. `files`: repo-relative paths to look in (default every
    .py file outside tests and docs)."""
    root = Path(root)
    if not paper_text:
        return []
    named = {}  # (family, member) -> the paper's sentence
    for fam, members in FAMILIES.items():
        for mem, (rx, _) in members.items():
            m = re.search(rx, paper_text, re.I if fam not in ("optimizer",) else 0)
            if m:
                named[(fam, mem)] = _sentence(paper_text, m)
    if not named:
        return []
    paths = [root / f for f in files] if files else [
        p for p in sorted(root.rglob("*.py")) if not any(x.startswith(".") or x in ("tests", "test", "docs")
                                                         for x in p.relative_to(root).parts)]
    spell = {}  # code spelling -> (family, member, index)
    for fam, members in FAMILIES.items():
        for mem, (_, names) in members.items():
            for i, nm in enumerate(names):
                spell.setdefault(nm.lower() if nm.startswith("'") else nm, (fam, mem, i))
    leads, seen = [], set()
    for p in paths:
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except (SyntaxError, ValueError, OSError):
            continue
        rel = p.relative_to(root).as_posix()
        for line, name, kind in _calls(tree):
            hit = spell.get(name)
            if hit is None:
                continue
            fam, mem, i = hit
            if (fam, mem) in named:  # the paper names the code's own choice: no swap
                continue
            for (f2, m2), quote in named.items():
                if f2 != fam:
                    continue
                names = FAMILIES[fam][m2][1]
                new = names[i] if i < len(names) else None
                if not new or new == name:
                    continue
                if kind.startswith("kw:"):  # a keyword string: the literal patch, on its line
                    key = (rel, line, kind)
                    lead = {"file": rel, "line": line, "name": kind[3:], "value": name, "paper_value": new}
                else:  # a call or a reference: every one in the file
                    key = (rel, name, new)
                    lead = {"file": rel, "line": 0, "name": f"@call.{name}", "value": name, "paper_value": new}
                if key in seen:
                    continue
                seen.add(key)
                leads.append({**lead, "family": "unexposed_setting", "source": "swap", "op_family": fam,
                              "quote": quote, "detail": f"the paper names {m2} ({fam}); {rel} uses {name}"})
    # files the entry script imports first would be better; without a trace, fewer swaps per family first
    by_fam: dict[str, int] = {}
    out = []
    for x in leads:
        if by_fam.get(x["op_family"], 0) < 2:
            by_fam[x["op_family"]] = by_fam.get(x["op_family"], 0) + 1
            out.append(x)
    return out[:limit]
