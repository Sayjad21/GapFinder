"""Metric parser: regex for known formats first, an LLM only for unknown ones.

Rule: every parsed number must appear verbatim in the raw log, otherwise it is
rejected. That stops a hallucinated value from Nano reaching the search.
"""

from __future__ import annotations

import json
import re

_NUM = r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?"

# db_bench: "fillrandom   :       2.345 micros/op 426439 ops/sec 23.450 seconds 10000000 operations;   47.2 MB/s"
_DB_BENCH_RE = re.compile(
    rf"^(?P<bench>\w+)\s*:\s*(?P<micros>{_NUM})\s+micros/op\s+(?P<ops>{_NUM})\s+ops/sec"
    rf"(?:\s+(?P<secs>{_NUM})\s+seconds)?(?:.*?(?P<mbs>{_NUM})\s+MB/s)?",
    re.MULTILINE,
)
# RocksDB statistics dump: "rocksdb.compact.write.bytes COUNT : 12345"
_ROCKS_STAT_RE = re.compile(rf"^(rocksdb\.[\w.]+)\s+COUNT\s*:\s*({_NUM})", re.MULTILINE)
# Compaction stats "Sum" row write-amp column, and the cumulative W-Amp line
_WAMP_RE = re.compile(rf"Cumulative compaction:.*?(?P<wamp>{_NUM})\s*W-?Amp|W-Amp\s*[:=]\s*(?P<wamp2>{_NUM})", re.I)
# Generic "key: value" / "key = value" metric lines (our harnesses print these)
_KV_RE = re.compile(rf"^\s*(?:METRIC\s+)?(?P<k>[A-Za-z_][\w./-]*)\s*[:=]\s*(?P<v>{_NUM})\s*$", re.MULTILINE)


class UngroundedValueError(ValueError):
    pass


def parse_db_bench(log: str) -> dict[str, float]:
    out: dict[str, float] = {}
    for m in _DB_BENCH_RE.finditer(log):
        b = m.group("bench")
        out[f"{b}.micros_per_op"] = float(m.group("micros"))
        out[f"{b}.ops_per_sec"] = float(m.group("ops"))
        if m.group("mbs"):
            out[f"{b}.mb_per_s"] = float(m.group("mbs"))
    for m in _ROCKS_STAT_RE.finditer(log):
        out[m.group(1)] = float(m.group(2))
    if m := _WAMP_RE.search(log):
        out["write_amp"] = float(m.group("wamp") or m.group("wamp2"))
    return out


def parse_kv(log: str) -> dict[str, float]:
    return {m.group("k"): float(m.group("v")) for m in _KV_RE.finditer(log)}


def parse_json_lines(log: str) -> dict[str, float]:
    """Last JSON object line with numeric fields wins (e.g. a summary line)."""
    out: dict[str, float] = {}
    for line in log.splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            out.update({k: float(v) for k, v in obj.items() if isinstance(v, (int, float)) and not isinstance(v, bool)})
    return out


def parse_metrics(log: str, fmt: str = "auto") -> dict[str, float]:
    parsers = {"db_bench": parse_db_bench, "kv": parse_kv, "jsonl": parse_json_lines}
    if fmt != "auto":
        return parsers[fmt](log)
    for p in (parse_db_bench, parse_json_lines, parse_kv):
        if res := p(log):
            return res
    return {}


def _number_forms(v: float) -> set[str]:
    forms = {repr(v), str(v), f"{v:g}"}
    if float(v).is_integer():
        forms.add(str(int(v)))
    for d in range(1, 7):
        forms.add(f"{v:.{d}f}")
    return forms


def ground_values(values: dict[str, float], raw_log: str) -> dict[str, float]:
    """Keep only values whose number appears verbatim in the raw log; raise if any don't."""
    nums_in_log = set(re.findall(_NUM, raw_log))
    bad = [k for k, v in values.items() if not (_number_forms(v) & nums_in_log)]
    if bad:
        raise UngroundedValueError(f"values not in raw log: {bad}")
    return values


async def llm_parse(router, raw_log: str, wanted: list[str]) -> dict[str, float]:
    """Nano fallback for unknown formats; every value is grounded before return."""
    from pydantic import BaseModel

    class Parsed(BaseModel):
        metrics: dict[str, float]

    tail = raw_log[-12000:]
    msg = [
        {
            "role": "user",
            "content": "Extract these metrics from the benchmark log. Copy numbers exactly as printed; "
            f"omit any you cannot find.\nMetrics: {wanted}\n\nLOG:\n{tail}",
        }
    ]
    parsed = await router.structured("nano", msg, Parsed)
    return ground_values(parsed.metrics, raw_log)
