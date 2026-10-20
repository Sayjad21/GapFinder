"""Paper terms to code flags (plan D4.1, D4.3, D4.4; docs/CONTEXT_v11.md section 7.3).

A paper says "the L2 weight λ", "K = 8 output attention heads", "a patience of 100 epochs"; the code has `l2_coef`,
`n_heads`, `patience`. Names alone mislead (Alor et al. 2025: most false links come from naming assumptions), so a link
is retrieved, then checked against what the code does with the value:

- **Retrieval** (D4.1): BM25 over the code's entities (each flag's split identifier, its help text and default; tf
  `DEFINE_*` flags and argparse alike) against the term (its name as written, its stated value's units, the paper's
  sentence), both sides expanded with an ML synonym lexicon (lr <-> learning rate, l2/coef/reg <-> weight decay,
  hid/dim/units <-> hidden size, nb/n/num <-> number, Greek letters spelled out). Identifier tokens count double.
- **Role check** (D4.3): the term's role from its words (a learning rate is a rate, weight decay a rate on the
  weights, dropout a fraction, a hidden size a size, epochs a count) against the role the runtime trace saw the flag's
  value play (gapfinder/search/trace.py: the optimiser's lr, its weight_decay, a dropout's p, a layer's width, a loop
  bound). A flag whose traced role contradicts the term's is dropped: a flag named like the term that feeds
  something else (a `weight` flag that is a class weight, not the L2 weight) is not the link.
- **Use** (D4.4): the engine links a ledger name to a knob deterministically when the top candidate passes the role
  check and leads the next by a clear margin; otherwise the candidates go to the model to choose among (or none).
"""

from __future__ import annotations

import ast
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

GREEK = {"λ": "lambda", "α": "alpha", "β": "beta", "γ": "gamma", "δ": "delta", "ε": "epsilon", "η": "eta",
         "τ": "tau", "ρ": "rho", "σ": "sigma", "μ": "mu", "θ": "theta", "κ": "kappa", "ω": "omega", "φ": "phi"}
# ML synonyms, both ways (a token expands to these words)
LEXICON = {
    "lr": "learning rate", "learning": "lr", "wd": "weight decay", "l2": "weight decay regularization lambda",
    "decay": "weight l2", "coef": "coefficient weight lambda", "coeff": "coefficient weight lambda",
    "reg": "regularization weight decay", "regularization": "reg l2 decay",
    "hid": "hidden units", "hidden": "units dimension size", "units": "hidden", "dim": "dimension hidden size",
    "dimension": "dim hidden size", "nb": "number", "n": "number", "num": "number", "number": "num n nb",
    "heads": "attention heads", "head": "attention heads", "drop": "dropout", "dropout": "drop",
    "epochs": "epoch iterations", "epoch": "epochs", "iters": "iterations steps", "iterations": "iters steps epochs",
    "bs": "batch size", "batch": "bs", "layers": "layer depth", "layer": "layers", "depth": "layers",
    "seq": "sequence length input", "len": "length", "length": "len", "win": "window", "window": "win",
    "patience": "early stopping", "nonlinearity": "activation", "activation": "nonlinearity", "act": "activation",
    "residual": "skip connections", "skip": "residual", "pool": "pooling readout", "pooling": "pool readout",
    "readout": "pooling pool", "lam": "lambda", "lambda": "lam weight coefficient trade", "ratio": "proportion fraction",
    "neg": "negative negatives sampling", "negative": "neg", "factors": "latent embedding dimension factor",
    "emb": "embedding", "embedding": "emb dimension", "eps": "epsilon", "epsilon": "eps", "temp": "temperature tau",
    "tau": "temperature", "mom": "momentum", "momentum": "mom", "hop": "hops depth", "hops": "hop depth",
    "context": "seq input length lookback", "lookback": "seq len input", "input": "seq", "pred": "prediction horizon",
    "horizon": "pred", "e": "encoder", "d": "decoder", "ff": "feedforward", "anormly": "anomaly", "k": "k",
}
_STOP = {"the", "a", "an", "of", "to", "in", "on", "for", "and", "or", "is", "are", "we", "with", "as", "by", "at",
         "be", "set", "use", "used", "this", "that", "each", "all", "our", "from", "which", "its", "it", "when"}


def tokens(text: str) -> list[str]:
    """Split identifiers and prose alike: snake, camel, digits; Greek letters spelled out."""
    for g, name in GREEK.items():
        text = text.replace(g, f" {name} ")
    text = re.sub(r"\\(lambda|alpha|beta|gamma|delta|epsilon|eta|tau|rho|sigma|mu|theta|kappa|omega|phi)", r" \1 ", text)
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    out = []
    for m in re.finditer(r"([A-Za-z]+)(\d*)|(\d+)", text.replace("_", " ").replace("-", " ").replace(".", " ")):
        letters, digits, num = m.group(1), m.group(2), m.group(3)
        if num:
            parts = [num]
        elif digits and len(letters) <= 2:
            parts = [letters + digits]  # l2, f1, k1: one name
        else:
            parts = [letters] + ([digits] if digits else [])  # hidden1 -> hidden, 1
        for w in parts:
            w = w.lower()
            if w not in _STOP:
                out.append(w)
    return out


def expand(toks: list[str]) -> list[str]:
    out = list(toks)
    for t in toks:
        out += LEXICON.get(t, "").split()
    return out


@dataclass
class Entity:
    name: str  # the knob
    help: str = ""
    default: str = ""
    role: str | None = None  # from the runtime trace
    toks: list[str] = field(default_factory=list)


def help_texts(root: str | Path) -> dict[str, str]:
    """flag -> its help text, from argparse `add_argument` and tf/absl `DEFINE_*` calls in the repo."""
    out: dict[str, str] = {}
    for p in Path(root).rglob("*.py"):
        if any(x.startswith(".") or x in ("site-packages", "venv", ".venv") for x in p.parts):
            continue
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except (SyntaxError, ValueError):
            continue
        for n in ast.walk(tree):
            if not isinstance(n, ast.Call):
                continue
            f = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id if isinstance(n.func, ast.Name) else ""
            strs = [a.value for a in n.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]
            kw = {k.arg: k.value.value for k in n.keywords if k.arg and isinstance(k.value, ast.Constant)}
            if f == "add_argument" and strs:
                name = next((s for s in strs if s.startswith("--")), strs[0]).lstrip("-").replace("-", "_")
                if isinstance(kw.get("help"), str):
                    out.setdefault(name, kw["help"])
                if isinstance(kw.get("dest"), str):
                    out.setdefault(kw["dest"], kw.get("help", "") if isinstance(kw.get("help"), str) else "")
            elif f.startswith("DEFINE_") and strs:
                name = strs[0]
                h = strs[-1] if len(strs) >= 2 else kw.get("help", "")
                if isinstance(h, str):
                    out.setdefault(name, h)
    return out


def entities(spec, root: str | Path | None) -> list[Entity]:
    helps = help_texts(root) if root else {}
    out = []
    for k, kn in spec.knobs.items():
        if k.startswith("@"):
            continue
        h = helps.get(k) or helps.get(k.replace("-", "_")) or ""
        e = Entity(k, h, str(kn.default), getattr(kn, "role", None))
        e.toks = expand(tokens(k)) * 2 + expand(tokens(h))
        out.append(e)
    return out


def _bm25(query: list[str], docs: list[list[str]], k1: float = 1.2, b: float = 0.75) -> list[float]:
    n = len(docs)
    avg = sum(len(d) for d in docs) / n if n else 1.0
    df: dict[str, int] = {}
    for d in docs:
        for t in set(d):
            df[t] = df.get(t, 0) + 1
    qtf: dict[str, int] = {}
    for t in query:  # the query's own weights: the term's words count more than its sentence's
        qtf[t] = qtf.get(t, 0) + 1
    scores = []
    for d in docs:
        tf: dict[str, int] = {}
        for t in d:
            tf[t] = tf.get(t, 0) + 1
        s = 0.0
        for t, w in qtf.items():
            if t not in tf:
                continue
            idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
            s += w * idf * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * len(d) / avg))
        scores.append(s)
    return scores


# ------------------------------------------------------------------ roles (D4.3)

_TERM_ROLE = [
    (re.compile(r"(?i)\b(learning[ _]?rate|lr|step[ _]?size)\b"), "rate"),
    (re.compile(r"(?i)(weight[ _]?decay|\bl2\b|l2[ _]|regulari[sz]|\bwd\b)"), "rate0"),
    (re.compile(r"(?i)(dropout|\bdrop|momentum|ratio|proportion|probabilit|fraction|percent|rate of)"), "fraction"),
    (re.compile(r"(?i)(batch|hidden|units|dimension|\bdim\b|width|channels|features|embedding|window|length|size)"), "size"),
    (re.compile(r"(?i)(epoch|iteration|\bsteps?\b|patience|\bruns\b|layers?\b|hops?\b)"), "count"),
    (re.compile(r"(?i)\bseed\b"), "seed"),
]
COMPATIBLE = {("size", "count"), ("count", "size"), ("count", "multiplier"), ("size", "multiplier")}


def term_role(term: str) -> str | None:
    for pat, role in _TERM_ROLE:
        if pat.search(term):
            return role
    return None


def role_ok(term: str, entity: Entity) -> bool | None:
    """True or False when both roles are known (a contradiction drops the link); None when either is unknown."""
    r = term_role(term)
    if r is None or entity.role is None:
        return None
    return r == entity.role or (r, entity.role) in COMPATIBLE


@dataclass
class Link:
    term: str
    knob: str
    score: float
    role: bool | None
    margin: float  # over the next candidate (a ratio, >= 1)


def link(term: str, context: str, ents: list[Entity], k: int = 5) -> list[Link]:
    """The best k candidates for one paper term, role-contradicting ones removed."""
    if not ents:
        return []
    # the sentences of the paper's quote that mention the term (a quote often sets several things at once:
    # "dropout with p = 0.6 ... L2 regularisation with lambda = 0.0005")
    own = set(expand(tokens(re.sub(r"\([^)]*\)", " ", term))))
    sentences = [s for s in re.split(r"(?<=[.;])\s+", context) if own & set(tokens(s))]
    context = " ".join(sentences) if sentences else context[:120]
    q = expand(tokens(term)) * 3 + expand(tokens(context))[:60]
    scores = _bm25(q, [e.toks for e in ents])
    ranked = sorted(zip(ents, scores), key=lambda x: -x[1])
    out = []
    for e, s in ranked:
        if s <= 0:
            break
        ok = role_ok(term + " " + context[:80], e)
        if ok is False:
            continue
        out.append(Link(term, e.name, round(s, 3), ok, 0.0))
    for i, l in enumerate(out):
        nxt = out[i + 1].score if i + 1 < len(out) else 0.0
        l.margin = round(l.score / nxt, 3) if nxt > 0 else float("inf")
    return out[:k]


_GENERIC = {"type", "function", "method", "value", "values", "implementation", "use", "using", "setting", "choice",
             "number", "num", "n", "nb", "size", "flag", "option", "param", "parameter", "hyperparameter", "vs"}


def covers(term: str, entity: Entity) -> bool:
    """Every content word of the term's name (its gloss in parentheses dropped, generic words ignored) is the flag's,
    directly or through the lexicon: `l2_reg_lambda` is covered by `l2_coef` (l2; reg -> regularization;
    lambda <- coef), `n_epochs_pretrain` is not covered by `train_epochs` (pretrain)."""
    name = re.sub(r"\([^)]*\)", " ", term)
    words = [w for w in tokens(name) if w not in _GENERIC]
    if not words:
        return False
    have = set(expand(tokens(entity.name)))
    return all(w in have or any(x in have for x in LEXICON.get(w, "").split()) for w in words)


def decisive(cands: list[Link], ents: list[Entity] | None = None, margin: float = 1.5,
             min_score: float = 2.0) -> Link | None:
    """The link to take without a model: the top candidate, clearly ahead, no role contradiction, and covering
    every content word of the term's name (otherwise the candidates go to the model, or nowhere)."""
    if not cands:
        return None
    top = cands[0]
    if top.score < min_score or top.margin < margin:
        return None
    ent = next((e for e in ents or [] if e.name == top.knob), None)
    if ent is not None and not covers(top.term, ent):
        return None
    return top
