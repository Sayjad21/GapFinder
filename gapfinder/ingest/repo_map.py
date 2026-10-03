"""Repo map, plain code, no LLM: file tree, build files, configs, every flag + default.

The flag scan is what makes `file:line` evidence checkable later: each Flag
records exactly where it was declared.
"""

from __future__ import annotations

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
# argparse: add_argument("--name", ..., default=X)
_ARGPARSE_RE = re.compile(r"add_argument\(\s*['\"](--?[\w-]+)['\"](.*?)\)\s*$", re.DOTALL)
_DEFAULT_RE = re.compile(r"default\s*=\s*([^,)]+)")
# CMake: option(NAME "help" ON)
_CMAKE_OPT_RE = re.compile(r"^\s*option\s*\(\s*(\w+)\s+\"[^\"]*\"\s+(\w+)", re.IGNORECASE)
# Makefile: NAME ?= value
_MAKE_VAR_RE = re.compile(r"^\s*([A-Z][A-Z0-9_]+)\s*\??=\s*(.*)$")
# struct option defaults: `int max_write_buffer_number = 2;`
_OPTION_FIELD_RE = re.compile(
    r"^\s*(?:bool|int|int32_t|int64_t|uint32_t|uint64_t|size_t|double|std::string)\s+(\w+)\s*=\s*([^;]+);"
)
# getenv("NAME")
_ENV_RE = re.compile(r"""(?:getenv|environ\.get|environ\[)\s*\(?\s*['"]([A-Z][A-Z0-9_]+)['"]""")


@dataclass
class Flag:
    name: str
    default: str | None
    kind: str  # gflags | argparse | cmake | make | option_field | env
    file: str  # repo-relative, posix
    line: int
    text: str  # the declaring line, verbatim

    @property
    def ref(self) -> str:
        return f"{self.file}:{self.line}"


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
        lines += [f"{f.name} = {f.default}  @ {f.ref}  [{f.kind}]" for f in self.flags[:max_flags]]
        lines += ["## File tree (truncated)"] + self.files[:max_files]
        if self.readme:
            lines += ["## README (first 4000 chars)", self.readme[:4000]]
        return "\n".join(lines)

    def find_flag(self, name: str) -> list[Flag]:
        norm = name.lstrip("-").replace("-", "_").lower()
        return [f for f in self.flags if f.name.lstrip("-").replace("-", "_").lower() == norm]


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


def _read(path: Path) -> str:
    try:
        if path.stat().st_size > 2_000_000:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _scan_flags(path: Path, rel: str) -> list[Flag]:
    text = _read(path)
    if not text:
        return []
    out: list[Flag] = []
    is_py = path.suffix == ".py"
    is_header = path.suffix in {".h", ".hpp"}
    for i, line in enumerate(text.splitlines(), start=1):
        if m := _GFLAGS_RE.search(line):
            out.append(Flag(m.group(2), m.group(3).strip(), "gflags", rel, i, line.strip()))
        elif is_py and "add_argument" in line and (m := _ARGPARSE_RE.search(line.strip())):
            d = _DEFAULT_RE.search(m.group(2))
            out.append(Flag(m.group(1), d.group(1).strip() if d else None, "argparse", rel, i, line.strip()))
        elif path.name == "CMakeLists.txt" and (m := _CMAKE_OPT_RE.match(line)):
            out.append(Flag(m.group(1), m.group(2), "cmake", rel, i, line.strip()))
        elif path.name == "Makefile" and (m := _MAKE_VAR_RE.match(line)):
            out.append(Flag(m.group(1), m.group(2).strip(), "make", rel, i, line.strip()))
        elif is_header and (m := _OPTION_FIELD_RE.match(line)):
            out.append(Flag(m.group(1), m.group(2).strip(), "option_field", rel, i, line.strip()))
        for m in _ENV_RE.finditer(line):
            out.append(Flag(m.group(1), None, "env", rel, i, line.strip()))
    return out
