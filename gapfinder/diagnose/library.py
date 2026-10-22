"""Library drift, narrowed to a package, a release and a call site (plan D1.3-D1.5, docs/CONTEXT_v11.md 7.2).

The paper-year knob (gapfinder/env_year.py) says whether the packages as of the paper's date change the numbers.
This module narrows a "yes" down in three steps, each run in the VM like any configuration:

1. **Which packages.** Delta debugging (Zeller and Hildebrandt's ddmin) over the old packages, on the test "this
   subset gives the numbers all of them give" (every claim within noise). The screen's single-package runs come
   first, so a single culprit costs no extra run; a round's subsets run in parallel.
2. **Which release.** A binary search over the culprit's releases from the paper's to the installed one, on "gives
   the same numbers as the older end". A release that matches neither end is a second change point, searched for in
   turn (two changes between the paper and now are common: a default in one release, an API in another).
3. **Which call.** The repository's call sites into the culprit (static: each file's import map, and instances of its
   classes for method calls), and in the VM the called objects under the two releases at the change point: their
   signatures, their source, and the source of the package functions they call. Keyword arguments the newer release
   no longer takes are the silent case when it has **kwargs and never reads them (the keyword is dropped without an
   error); the parameter it was renamed to is ranked by name, default and position. Defaults that changed for
   parameters the call doesn't pass, positional parameters that moved, and called functions whose source changed are
   leads too. A signature lead becomes an in-memory code edit (rename the keyword; pass the older default) that the
   engine runs on the newer release: one that gives the older release's numbers is verified at that call site.

Compared with the API-breaking-change detectors this follows (Default Argument Breaking Changes, 2024; willitbreak),
the diff is limited to what the repository calls, is computed by importing both releases rather than parsing their
code, and is confirmed by running the paper's experiment rather than by type checks.
"""

from __future__ import annotations

import ast
import asyncio
import base64
import difflib
import json
import re
import zlib
from dataclasses import asdict, dataclass, field
from pathlib import Path

# ----------------------------------------------------------------------------- 1. which packages


async def ddmin(items: list[str], test, known: dict[frozenset, bool] | None = None,
                max_tests: int | None = None) -> tuple[list[str], int, bool]:
    """A minimal subset of `items` that still passes `test` (assumed to pass on all of them): Zeller and
    Hildebrandt's ddmin, each round's subsets (then complements) tested in parallel. `known`: outcomes already
    measured (a subset -> passes). Returns (subset, tests run, whether the result is 1-minimal)."""
    cache: dict[frozenset, bool] = dict(known or {})
    cache.setdefault(frozenset(items), True)
    ran = 0

    async def t(s: list[str]) -> bool:
        nonlocal ran
        key = frozenset(s)
        if key not in cache:
            ran += 1
            cache[key] = bool(await test(list(s)))
        return cache[key]

    def over() -> bool:
        return max_tests is not None and ran >= max_tests

    c, n = list(items), 2
    while len(c) >= 2:
        size = len(c)
        chunks = [c[i * size // n:(i + 1) * size // n] for i in range(n)]
        chunks = [ch for ch in chunks if ch]
        if over():
            return c, ran, False
        hit = next((ch for ch in chunks if cache.get(frozenset(ch))), None)  # already known to pass: no run
        if hit is None:
            res = await asyncio.gather(*(t(ch) for ch in chunks))
            hit = next((ch for ch, ok in zip(chunks, res) if ok), None)
        if hit is not None:
            c, n = hit, 2
            continue
        comps = [[x for x in c if x not in ch] for ch in chunks] if n > 2 else []
        if comps and not over():
            hit = next((cm for cm in comps if cache.get(frozenset(cm))), None)
            if hit is None:
                res = await asyncio.gather(*(t(cm) for cm in comps))
                hit = next((cm for cm, ok in zip(comps, res) if ok), None)
            if hit is not None:
                c, n = hit, max(n - 1, 2)
                continue
        if n >= len(c):
            break
        n = min(len(c), 2 * n)
    return c, ran, True


# ----------------------------------------------------------------------------- 2. which release


async def first_differing(seq: list[str], same, lo: int = 0, hi: int | None = None) -> int:
    """The first index in (lo, hi] whose element gives numbers different from seq[lo]'s, given that seq[hi]'s do
    (binary search: the change is assumed to persist once made)."""
    hi = len(seq) - 1 if hi is None else hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if await same(seq[mid], seq[lo]):
            lo = mid
        else:
            hi = mid
    return hi


async def change_points(seq: list[str], same, max_points: int = 2) -> list[tuple[str, str]]:
    """Each (last element like the one before, first element that differs) from seq[0] to seq[-1]: one change, or a
    second when the first differing element doesn't match seq[-1] either."""
    out, lo = [], 0
    while lo < len(seq) - 1 and len(out) < max_points:
        if await same(seq[-1], seq[lo]):
            break
        i = await first_differing(seq, same, lo)
        out.append((seq[i - 1], seq[i]))
        lo = i
    return out


# ----------------------------------------------------------------------------- 3. which call


@dataclass
class CallSite:
    file: str
    line: int
    col: int
    qual: str  # e.g. pygod.models.DOMINANT, or pygod.models.DOMINANT.fit for a method on an instance
    keywords: list[str] = field(default_factory=list)
    n_args: int = 0
    star: bool = False  # *args or **kwargs at the call: its arguments can't be read statically
    bound: bool = False  # a method called on an instance (its first parameter is `self`)
    executed: bool | None = None

    def where(self) -> str:
        return f"{self.file}:{self.line}"


_SKIP_DIRS = {".git", "gf_harness", "site-packages", "node_modules", "__pycache__", "venv", ".venv", "env"}


def call_sites(root: str | Path, modules: list[str], exclude: list[str] | None = None,
               executed: dict[str, list[int]] | None = None, limit: int = 300) -> list[CallSite]:
    """Calls in the repository's code into the given top-level modules, through each file's imports (`import x as
    y`, `from x.m import C`) and through instances of their classes (`m = C(...)`; `m.fit(...)`). `exclude`: repo
    directories left out (the package's own code, when the repository is the library). Executed sites first."""
    root = Path(root)
    tops = {m.split(".")[0] for m in modules}
    excl = [e.strip("/") + "/" for e in exclude or []]
    out: list[CallSite] = []
    for p in sorted(root.rglob("*.py")):
        rel = p.relative_to(root).as_posix()
        if any(part in _SKIP_DIRS or part.startswith(".") for part in p.relative_to(root).parts[:-1]):
            continue
        if any(rel.startswith(e) for e in excl):
            continue
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except (SyntaxError, ValueError, OSError):
            continue
        alias: dict[str, str] = {}
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for a in n.names:
                    if a.name.split(".")[0] in tops:
                        alias[a.asname or a.name.split(".")[0]] = a.name if a.asname else a.name.split(".")[0]
            elif isinstance(n, ast.ImportFrom) and n.module and not n.level and n.module.split(".")[0] in tops:
                for a in n.names:
                    if a.name != "*":
                        alias[a.asname or a.name] = f"{n.module}.{a.name}"
        if not alias:
            continue

        def resolve(e) -> str | None:
            if isinstance(e, ast.Name):
                return alias.get(e.id)
            if isinstance(e, ast.Attribute):
                base = resolve(e.value)
                return f"{base}.{e.attr}" if base else None
            return None

        def key(e) -> str | None:
            if isinstance(e, ast.Name):
                return "n:" + e.id
            if isinstance(e, ast.Attribute) and isinstance(e.value, ast.Name) and e.value.id == "self":
                return "a:" + e.attr
            return None

        types: dict[str, str] = {}
        for n in ast.walk(tree):
            if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.value, ast.Call):
                q, k = resolve(n.value.func), key(n.targets[0])
                if q and k and q.split(".")[-1][:1].isupper():
                    types[k] = q
        ex = set((executed or {}).get(rel, []))
        for n in ast.walk(tree):
            if not isinstance(n, ast.Call):
                continue
            q, bound = resolve(n.func), False
            if q is None and isinstance(n.func, ast.Attribute) and (k := key(n.func.value)) in types:
                q, bound = f"{types[k]}.{n.func.attr}", True
            if not q:
                continue
            star = any(isinstance(a, ast.Starred) for a in n.args) or any(kw.arg is None for kw in n.keywords)
            out.append(CallSite(rel, n.lineno, n.col_offset, q, [kw.arg for kw in n.keywords if kw.arg],
                                len([a for a in n.args if not isinstance(a, ast.Starred)]), star, bound,
                                (n.lineno in ex) if executed else None))
    out.sort(key=lambda c: (c.executed is False, not c.keywords, c.file, c.line))
    return out[:limit]


# The probe run in the VM under each release: signatures, sources, and the sources of the package functions the
# called objects call (one level down). Python 3.6+; prints one compressed JSON line per side.
PROBE_SOURCE = r'''
import ast, base64, importlib, inspect, json, os, sys, textwrap, zlib
sys.path.insert(1, os.getcwd())
side, names = sys.argv[1], json.load(open(sys.argv[2]))
MAX = 30000

def resolve(q):
    parts = q.split(".")
    for i in range(len(parts), 0, -1):
        try:
            obj = importlib.import_module(".".join(parts[:i]))
        except Exception:
            continue
        try:
            for a in parts[i:]:
                obj = getattr(obj, a)
            return obj, None, i
        except AttributeError as e:
            return None, "attribute: %s" % e, i
    return None, "no module", 0

def params(obj):
    try:
        s = inspect.signature(obj)
    except (TypeError, ValueError):
        return None
    out = []
    for p in s.parameters.values():
        d = None if p.default is inspect.Parameter.empty else repr(p.default)[:200]
        out.append([p.name, p.kind.name, d])
    return out

def source(obj):
    try:
        return inspect.getsource(obj)[:MAX]
    except Exception:
        return None

def callees(fn, text, cls, top):
    out = {}
    try:
        tree = ast.parse(textwrap.dedent(text))
    except Exception:
        return out
    g = getattr(fn, "__globals__", {})
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        f, obj, label = n.func, None, None
        if isinstance(f, ast.Name) and f.id in g:
            obj, label = g[f.id], f.id
        elif isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id == "self" and cls is not None:
            obj, label = getattr(cls, f.attr, None), "self." + f.attr
        if obj is None or label in out or not callable(obj):
            continue
        if not (getattr(obj, "__module__", "") or "").startswith(top):
            continue
        s = source(obj)
        if s:
            out[label] = s
        if len(out) >= 15:
            break
    return out

res = {"versions": {}, "objects": {}}
for q in names:
    obj, err, depth = resolve(q)
    top = q.split(".")[0]
    m = sys.modules.get(top)
    if m is not None and top not in res["versions"]:
        res["versions"][top] = [getattr(m, "__version__", None), getattr(m, "__file__", None)]
    if obj is None:
        res["objects"][q] = {"ok": False, "error": err}
        continue
    is_cls = inspect.isclass(obj)
    target = obj.__init__ if is_cls else obj
    cls = obj if is_cls else None
    if cls is None and "." in q:
        owner, _, _ = resolve(q.rsplit(".", 1)[0])
        cls = owner if inspect.isclass(owner) else None
    text = source(target) or ""
    sub = callees(target, text, cls, top) if text else {}
    if is_cls:  # keyword arguments forwarded to a base class are read there
        for base in obj.__mro__[1:4]:
            if (getattr(base, "__module__", "") or "").startswith(top) and "__init__" in vars(base):
                s = source(base.__init__)
                if s:
                    sub["base:%s.__init__" % base.__name__] = s
    res["objects"][q] = {"ok": True, "kind": "class" if is_cls else type(obj).__name__, "params": params(obj),
                         "source": text, "callees": sub}
blob = base64.b64encode(zlib.compress(json.dumps(res).encode("utf-8"))).decode("ascii")
print("GF_API_%s %s" % (side, blob))
'''


def parse_probe(stdout: str, side: str) -> dict | None:
    m = re.search(rf"GF_API_{side} (\S+)", stdout or "")
    if not m:
        return None
    try:
        return json.loads(zlib.decompress(base64.b64decode(m.group(1))).decode("utf-8"))
    except Exception:  # noqa: BLE001 (truncated output)
        return None


def _params(rec: dict, bound: bool) -> list[list]:
    ps = [p for p in (rec.get("params") or [])]
    if bound and ps and ps[0][0] in ("self", "cls"):
        ps = ps[1:]
    return ps


def _literal(src: str | None) -> bool:
    if src is None:
        return False
    try:
        ast.literal_eval(src)
        return True
    except (ValueError, SyntaxError):
        return False


def _mentions(name: str, rec: dict) -> bool:
    """Whether the source reads `name` by its string (kwargs.get('alpha'), kwargs['alpha'], **dict lookups)."""
    texts = [rec.get("source") or ""] + list((rec.get("callees") or {}).values())
    pat = re.compile(rf"""['"]{re.escape(name)}['"]""")
    return any(pat.search(t) for t in texts)


@dataclass
class ApiLead:
    kind: str  # swallowed | removed | renamed | default | positional | source
    site: str  # file:line
    qual: str
    detail: str
    op: str | None = None  # the mutation operator that undoes it at the call (kw.OLD.NEW or kwset.NAME.B64)
    file: str = ""
    line: int = 0
    col: int = 0
    rank: float = 0.0
    diff: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def compare(sites: list[CallSite], old: dict, new: dict, old_label: str = "old", new_label: str = "new",
            max_diff: int = 30) -> list[ApiLead]:
    """Leads from the two probes (parse_probe), best first."""
    from gapfinder.sandbox.ast_patch import kwset_op

    leads: list[ApiLead] = []
    oo, no = old.get("objects", {}), new.get("objects", {})
    seen_source: set[str] = set()
    for s in sites:
        a, b = oo.get(s.qual), no.get(s.qual)
        if not a or not b or not a.get("ok") or not b.get("ok"):
            continue
        pa, pb = _params(a, s.bound), _params(b, s.bound)
        if pa is not None and pb is not None and (pa or pb):
            na = {p[0]: p for p in pa}
            nb = {p[0]: p for p in pb}
            var_kw_a = any(p[1] == "VAR_KEYWORD" for p in pa)
            var_kw_b = any(p[1] == "VAR_KEYWORD" for p in pb)
            fresh = [p for p in pb if p[0] not in na and p[1] not in ("VAR_KEYWORD", "VAR_POSITIONAL")]
            for kw in s.keywords:
                takes_a = kw in na or (var_kw_a and _mentions(kw, a))
                if takes_a and kw not in nb:
                    if kw not in na:  # read from **kwargs in both: compare the reads
                        na[kw] = [kw, "KEYWORD_ONLY", None]
                        pa = pa + [na[kw]]
                    if var_kw_b and not _mentions(kw, b):
                        # the silent case: accepted by **kwargs, never read
                        cand = sorted(fresh, key=lambda p: (-(p[2] == na[kw][2]),
                                                            -difflib.SequenceMatcher(None, kw, p[0]).ratio(),
                                                            abs(pb.index(p) - pa.index(na[kw]))))
                        to = cand[0][0] if cand else None
                        leads.append(ApiLead(
                            "swallowed", s.where(), s.qual,
                            f"`{kw}=` is not a parameter of {s.qual} in {new_label}: **kwargs takes it and nothing "
                            f"reads it, so it is silently ignored" + (f"; {new_label} has `{to}` (default "
                            f"{cand[0][2]}) in its place" if to else ""),
                            f"kw.{kw}.{to}" if to else None, s.file, s.line, s.col, 10.0 + (2 if to else 0)))
                    elif var_kw_b:
                        leads.append(ApiLead("renamed", s.where(), s.qual,
                                             f"`{kw}=` is no longer a named parameter of {s.qual} in {new_label} "
                                             "(read from **kwargs instead)", None, s.file, s.line, s.col, 3.0))
                    else:
                        leads.append(ApiLead("removed", s.where(), s.qual,
                                             f"`{kw}=` was removed from {s.qual} in {new_label} (the call would "
                                             "raise there: this site may not run)", None, s.file, s.line, s.col, 1.0))
            passed = set(s.keywords)
            pos = [p for p in pa if p[1] in ("POSITIONAL_ONLY", "POSITIONAL_OR_KEYWORD")]
            passed |= {p[0] for p in pos[: s.n_args]}
            if not s.star:
                for name, (_, _, da) in ((p[0], p) for p in pa):
                    if name in passed or name not in nb:
                        continue
                    db = nb[name][2]
                    if da is not None and db is not None and da != db:
                        leads.append(ApiLead(
                            "default", s.where(), s.qual,
                            f"the call doesn't pass `{name}`; its default went from {da} ({old_label}) to {db} "
                            f"({new_label})", kwset_op(name, da) if _literal(da) else None, s.file, s.line, s.col,
                            8.0 if _literal(da) else 4.0))
                pos_b = [p for p in pb if p[1] in ("POSITIONAL_ONLY", "POSITIONAL_OR_KEYWORD")]
                for i in range(min(s.n_args, len(pos), len(pos_b))):
                    if pos[i][0] != pos_b[i][0]:
                        leads.append(ApiLead("positional", s.where(), s.qual,
                                             f"positional argument {i + 1} is `{pos[i][0]}` in {old_label} and "
                                             f"`{pos_b[i][0]}` in {new_label}", None, s.file, s.line, s.col, 6.0))
                        break
        if s.qual in seen_source:
            continue
        seen_source.add(s.qual)
        changed = []
        if (a.get("source") or "") != (b.get("source") or ""):
            changed.append((s.qual, a.get("source") or "", b.get("source") or ""))
        for label, src in (a.get("callees") or {}).items():
            other = (b.get("callees") or {}).get(label)
            if other is not None and other != src:
                changed.append((f"{s.qual} -> {label}", src, other))
        for what, sa, sb in changed:
            d = [ln for ln in difflib.unified_diff(sa.splitlines(), sb.splitlines(), old_label, new_label, n=1,
                                                   lineterm="")][2:]
            body = [ln for ln in d if ln[:1] in "+-" and ln.strip("+- ")]
            if not body:
                continue
            leads.append(ApiLead("source", s.where(), what,
                                 f"the source of {what} changed ({len(body)} line(s))", None, s.file, s.line, s.col,
                                 2.0 + min(len(body), 20) / 20, diff=d[:max_diff]))
    best: dict[tuple, ApiLead] = {}
    for x in leads:  # one lead per (kind, site, what)
        k = (x.kind, x.site, x.qual, x.op)
        if k not in best or x.rank > best[k].rank:
            best[k] = x
    out = sorted(best.values(), key=lambda x: -x.rank)
    return out


def probe_files(quals: list[str]) -> dict[str, bytes]:
    return {".gf_lib/probe.py": PROBE_SOURCE.encode(), ".gf_lib/names.json": json.dumps(sorted(set(quals))).encode()}


def probe_command(prefix_a: str, prefix_b: str) -> str:
    """Both sides in one operation, each in a subshell with its own GF_LIB_DIRS (env_year.run_prefix's value)."""
    run = '"${PYTHON:-python}" .gf_lib/probe.py'
    return (f"({prefix_a}{run} A .gf_lib/names.json; echo GF_API_RC_A=$?); "
            f"({prefix_b}{run} B .gf_lib/names.json; echo GF_API_RC_B=$?)")
