"""Repo map, plain code, no LLM: file tree, build files, configs, every flag + default.

The flag scan is what makes `file:line` evidence checkable later: each Flag
records exactly where it was declared.
"""

from __future__ import annotations

import ast
import os
import re
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "build", "dist", "third-party", "third_party"}
BUILD_FILES = {"Makefile", "CMakeLists.txt", "setup.py", "pyproject.toml", "build.sh", "Cargo.toml", "BUCK"}
CONFIG_EXT = {".yaml", ".yml", ".json", ".toml", ".ini", ".cfg", ".conf"}
SCRIPT_EXT = {".sh", ".bash"}
CODE_EXT = {".cc", ".cpp", ".c", ".h", ".hpp", ".py", ".rs", ".go", ".java"}

# gflags: DEFINE_int32(name, default, "help")
_GFLAGS_RE = re.compile(r"\bDEFINE_(bool|int32|int64|uint32|uint64|double|string)\s*\(\s*(\w+)\s*,\s*([^,]+?)\s*,")
# absl / tf.app.flags (Python): flags.DEFINE_float('name', default, 'help'), DEFINE_enum('n', 'a', ['a', 'b'], ..)
_ABSL_RE = re.compile(r"\bDEFINE_(\w+)\s*\(\s*['\"](\w+)['\"]\s*,\s*([^,]+?)\s*,")
# argparse: add_argument("--name", ..., default=X)
_ARGPARSE_RE = re.compile(r"add_argument\(\s*['\"](--?[\w-]+)['\"](.*)$")
_DEFAULT_RE = re.compile(r"default\s*=\s*([^,)]+)")
_CHOICES_RE = re.compile(r"choices\s*=\s*(\[[^\]]*\]|\([^)]*\))")
# CMake: option(NAME "help" ON)
_CMAKE_OPT_RE = re.compile(r"^\s*option\s*\(\s*(\w+)\s+\"[^\"]*\"\s+(\w+)", re.IGNORECASE)
# Makefile: NAME ?= value
_MAKE_VAR_RE = re.compile(r"^\s*([A-Z][A-Z0-9_]+)\s*\??=\s*(.*)$")
# struct option defaults: `int max_write_buffer_number = 2;`
_OPTION_FIELD_RE = re.compile(
    r"^\s*(?:bool|int|int32_t|int64_t|uint32_t|uint64_t|size_t|double|std::string)\s+(\w+)\s*=\s*([^;]+);"
)
# Usage/help text: "  --rate_limit_mb N        cap compaction bandwidth (default 0)"
_USAGE_RE = re.compile(r"^\s{1,8}(--[a-z][\w-]*)(\s+[A-Z][A-Z0-9,.]*)?\s{2,}(.*?)\s*$")
_USAGE_DEFAULT_RE = re.compile(r"\(default:?\s*([^)]*)\)|\bdefault:?\s+([^\s,;)]+)")
# getenv("NAME")
_ENV_RE = re.compile(r"""(?:getenv|environ\.get|environ\[)\s*\(?\s*['"]([A-Z][A-Z0-9_]+)['"]""")


@dataclass
class Flag:
    name: str
    default: str | None
    kind: str  # gflags | absl | argparse | cmake | make | option_field | usage | env
    file: str  # repo-relative, posix
    line: int
    text: str  # the declaring line, verbatim
    choices: list[str] | None = None  # argparse choices=[...], when they are literals

    @property
    def ref(self) -> str:
        return f"{self.file}:{self.line}"


_KIND_RANK = {"gflags": 0, "absl": 0, "usage": 0, "option_field": 1, "cmake": 1, "make": 2, "argparse": 3, "env": 4}


@dataclass
class RepoMap:
    root: Path
    files: list[str] = field(default_factory=list)
    build_files: list[str] = field(default_factory=list)
    config_files: list[str] = field(default_factory=list)
    scripts: list[str] = field(default_factory=list)
    flags: list[Flag] = field(default_factory=list)
    readme: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["root"] = str(self.root)
        return d

    def summary(self, max_files: int = 400, max_flags: int = 600) -> str:
        """Compact text the LLM gets instead of the whole repo."""
        lines = [f"# Repo map of {self.root.name}", f"{len(self.files)} files", "## Build files"]
        lines += self.build_files[:50]
        lines += ["## Scripts"] + self.scripts[:100]
        lines += ["## Config files"] + self.config_files[:100]
        lines += ["## Flags and defaults (name = default  @ file:line)"]
        # choices are kept out of this text on purpose: it is part of the model prompts, and changing
        # it would invalidate every cached answer (the search reads choices from Flag.choices instead)
        lines += [f"{f.name} = {f.default}  @ {f.ref}  [{f.kind}]" for f in self.flags[:max_flags]]
        lines += ["## File tree (truncated)"] + self.files[:max_files]
        if self.readme:
            lines += ["## README (first 4000 chars)", self.readme[:4000]]
        return "\n".join(lines)

    def find_flag(self, name: str) -> list[Flag]:
        """Definitions first: a binary's own flag beats a wrapper script that passes it."""
        norm = name.lstrip("-").replace("-", "_").lower()
        hits = [f for f in self.flags if f.name.lstrip("-").replace("-", "_").lower() == norm]
        return sorted(hits, key=lambda f: _KIND_RANK.get(f.kind, 9))


def clone_or_path(repo: str, dest: Path) -> Path:
    """Local path is used as-is; a URL is shallow-cloned into `dest`."""
    p = Path(repo)
    if p.exists():
        return p.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    target = dest / re.sub(r"[^\w.-]", "_", repo.rstrip("/").split("/")[-1].removesuffix(".git"))
    if not target.exists():
        subprocess.run(["git", "clone", "--depth", "1", repo, str(target)], check=True)
    return target


def build_repo_map(root: str | Path, *, include_flag_dirs: tuple[str, ...] | None = None) -> RepoMap:
    root = Path(root).resolve()
    rm = RepoMap(root=root)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        for fn in sorted(filenames):
            full = Path(dirpath) / fn
            rel = full.relative_to(root).as_posix()
            rm.files.append(rel)
            ext = full.suffix.lower()
            if fn in BUILD_FILES or fn.endswith(".mk"):
                rm.build_files.append(rel)
            if ext in CONFIG_EXT:
                rm.config_files.append(rel)
            if ext in SCRIPT_EXT:
                rm.scripts.append(rel)
            if fn.lower().startswith("readme") and not rm.readme and Path(dirpath) == root:
                rm.readme = _read(full)
            if include_flag_dirs and not rel.startswith(include_flag_dirs):
                continue
            if ext in CODE_EXT or fn in BUILD_FILES or ext in SCRIPT_EXT:
                rm.flags.extend(_scan_flags(full, rel))
    return rm


def _literal_choices(window: str) -> list[str] | None:
    """`choices=["a", "b"]` or `choices=(1, 2)` as strings; None when absent or not a literal."""
    m = _CHOICES_RE.search(window)
    if not m:
        return None
    try:
        vals = ast.literal_eval(m.group(1))
    except (ValueError, SyntaxError):
        return None
    return [str(v) for v in vals] or None


def _read(path: Path) -> str:
    try:
        if path.stat().st_size > 2_000_000:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _absl_flags(text: str, rel: str, lines: list[str]) -> list[Flag] | None:
    """absl / tf.app.flags definitions in a Python file, from its syntax tree (multi-line calls, keyword
    arguments, DEFINE_enum choices). None when the file doesn't parse (e.g. Python 2), so the caller
    falls back to the line regex."""
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return None
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
        if not fn.startswith("DEFINE_"):
            continue
        kw = {k.arg: k.value for k in node.keywords if k.arg}
        name = node.args[0] if node.args else kw.get("name")
        if not (isinstance(name, ast.Constant) and isinstance(name.value, str)):
            continue  # e.g. a C-style gflags call, or a computed name
        default = node.args[1] if len(node.args) > 1 else kw.get("default")
        dtext = None
        if default is not None:
            # strings without their quotes; anything else as written (5e-4 stays 5e-4)
            if isinstance(default, ast.Constant) and isinstance(default.value, str):
                dtext = default.value
            else:
                dtext = ast.get_source_segment(text, default)
        choices = None
        if fn.startswith("DEFINE_enum"):
            enum = node.args[2] if len(node.args) > 2 else kw.get("enum_values")
            try:
                choices = [str(v) for v in ast.literal_eval(enum)] or None
            except (ValueError, TypeError):
                choices = None
        line = node.lineno
        out.append(Flag(name.value, dtext, "absl", rel, line, lines[line - 1].strip(), choices=choices))
    return sorted(out, key=lambda f: f.line)


def _scan_flags(path: Path, rel: str) -> list[Flag]:
    text = _read(path)
    if not text:
        return []
    out: list[Flag] = []
    is_py = path.suffix == ".py"
    is_header = path.suffix in {".h", ".hpp"}
    lines = text.splitlines()
    absl = _absl_flags(text, rel, lines) if is_py and "DEFINE_" in text else None
    if absl:
        out.extend(absl)
    for i, line in enumerate(lines, start=1):
        if is_py and absl is None and (m := _ABSL_RE.search(line)):
            out.append(Flag(m.group(2), m.group(3).strip().strip("'\""), "absl", rel, i, line.strip()))
        elif m := _GFLAGS_RE.search(line):
            out.append(Flag(m.group(2), m.group(3).strip(), "gflags", rel, i, line.strip()))
        elif is_py and "add_argument" in line and (m := _ARGPARSE_RE.search(line.strip())):
            # the call may continue over the next lines: look for default= up to the closing paren
            window = m.group(2)
            for nxt in lines[i : i + 6]:
                if 1 + window.count("(") - window.count(")") <= 0:  # the call's parentheses are closed
                    break
                window += " " + nxt.strip()
            d = _DEFAULT_RE.search(window)
            out.append(Flag(m.group(1), d.group(1).strip() if d else None, "argparse", rel, i, line.strip(),
                            choices=_literal_choices(window)))
        elif path.name == "CMakeLists.txt" and (m := _CMAKE_OPT_RE.match(line)):
            out.append(Flag(m.group(1), m.group(2), "cmake", rel, i, line.strip()))
        elif path.name == "Makefile" and (m := _MAKE_VAR_RE.match(line)):
            out.append(Flag(m.group(1), m.group(2).strip(), "make", rel, i, line.strip()))
        elif is_header and (m := _OPTION_FIELD_RE.match(line)):
            out.append(Flag(m.group(1), m.group(2).strip(), "option_field", rel, i, line.strip()))
        elif not is_py and (m := _USAGE_RE.match(line)):
            d = _USAGE_DEFAULT_RE.search(m.group(3))
            default = (d.group(1) or d.group(2)).strip() if d else None
            if default is None and m.group(2) is None:
                default = "false"  # a switch with no value is off unless passed
            out.append(Flag(m.group(1), default, "usage", rel, i, line.strip()))
        for m in _ENV_RE.finditer(line):
            out.append(Flag(m.group(1), None, "env", rel, i, line.strip()))
    return out
