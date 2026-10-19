"""Multi-claim history matching: which measured configurations are Not Ruled Out Yet (NROY) for every claim.

For a configuration x and a claim i (target or held-out), the implausibility is

    I_i(x) = |z_i - m_i(x)| / sqrt(s_i^2 / p + s_i^2 / n_x + (d * z_i)^2)

where:
- z_i is the paper's number and m_i(x) the mean of the n_x runs at x;
- s_i is the run-to-run SD at the naive configuration, counted for the paper's number (an average of
  p runs) and for our mean;
- d is a discrepancy fraction for scaled surrogates.

A configuration is NROY for a claim when I <= cutoff (3, Pukelsheim's rule), and jointly NROY when it is
NROY for every claim. Only *tested* configurations count: an empty set means "not found among these", not
"proven impossible". Validated offline in eval/results/history_match_offline.md.
"""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass, field


@dataclass
class Diagnosis:
    kind: str  # reproduced | in_space | out_of_space_suspected | out_of_space_likely | insufficient
    text: str
    joint: list[dict] = field(default_factory=list)  # [{"config", "I"}], best first
    per_claim: dict[str, list[dict]] = field(default_factory=dict)  # claim -> NROY configs, best first
    params: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {"kind": self.kind, "text": self.text, "joint": self.joint[:10],
                "islands": islands([j["config"] for j in self.joint]),
                "per_claim": {c: v[:10] for c, v in self.per_claim.items()}, "params": self.params}


def _one_move(a: dict, b: dict) -> bool:
    """a and b differ by one knob: set, unset or changed."""
    keys = set(a) | set(b)
    return sum(a.get(k) != b.get(k) for k in keys) == 1


def islands(configs: list[dict]) -> list[list[dict]]:
    """Connected components of the configurations under single-knob moves (BFS), largest first.
    Two islands mean two separate explanations; one island means variations of the same one."""
    left, out = list(range(len(configs))), []
    while left:
        comp, queue = [], [left.pop(0)]
        while queue:
            i = queue.pop(0)
            comp.append(i)
            near = [j for j in left if _one_move(configs[i], configs[j])]
            for j in near:
                left.remove(j)
            queue += near
        out.append([configs[i] for i in sorted(comp)])
    return sorted(out, key=len, reverse=True)


def implausibilities(runs: dict[tuple, list[dict]], claims: list[tuple[str, str, float]], *,
                     paper_n: float = 1.0, disc: float = 0.05, optional: set[str] | frozenset = frozenset(),
                     sd_alias: dict[str, str] | None = None) -> list[dict]:
    """claims: (claim_id, metric, paper_value). runs: frozen config -> parsed metrics per successful run.
    `optional`: claims a configuration may lack (a claim at fixed knob values is measured only for some
    configurations); a row without one has no I for it. `sd_alias`: metric -> the metric whose naive SD it uses."""
    naive = runs.get((), [])
    sd = {}
    for _, metric, _ in claims:
        src = (sd_alias or {}).get(metric, metric)
        vals = [m[src] for m in naive if src in m]
        sd[metric] = statistics.stdev(vals) if len(vals) >= 2 else 0.0
    rows = []
    for key, ms in runs.items():
        row = {"config": dict(key), "n": len(ms), "I": {}}
        for cid, metric, z in claims:
            vals = [m[metric] for m in ms if metric in m]
            if not vals and cid in optional:
                continue
            if not vals:
                break
            s = sd[metric]
            denom = math.sqrt(s ** 2 / paper_n + s ** 2 / len(vals) + (disc * z) ** 2) or 1e-12
            row["I"][cid] = round(abs(z - statistics.fmean(vals)) / denom, 2)
        else:
            rows.append(row)
    return rows


def diagnose(runs: dict[tuple, list[dict]], claims: list[tuple[str, str, float]], target_id: str, *,
             paper_n: float = 1.0, disc: float = 0.05, cutoff: float = 3.0, optional: set[str] | frozenset = frozenset(),
             sd_alias: dict[str, str] | None = None) -> Diagnosis:
    params = {"paper_n": paper_n, "disc": disc, "cutoff": cutoff}
    rows = implausibilities(runs, claims, paper_n=paper_n, disc=disc, optional=optional, sd_alias=sd_alias)
    if not any(r["config"] == {} for r in rows):
        return Diagnosis("insufficient", "no naive measurement of every claim; history matching skipped", params=params)
    # an optional claim measured nowhere says nothing either way
    ids = [c for c, _, _ in claims if c not in optional or any(c in r["I"] for r in rows)]
    per = {c: sorted(({"config": r["config"], "I": r["I"]} for r in rows if c in r["I"] and r["I"][c] <= cutoff),
                     key=lambda r: r["I"][c]) for c in ids}
    joint = sorted(({"config": r["config"], "I": r["I"]} for r in rows if max(r["I"].values()) <= cutoff),
                   key=lambda r: max(r["I"].values()))
    tested = len(rows) - 1
    if any(r["config"] == {} for r in joint):
        return Diagnosis("reproduced", "the naive configuration is within noise of every claim", joint, per, params)
    if joint:
        return Diagnosis("in_space", f"{len(joint)} of {tested} tested configurations fit every claim within "
                         f"{cutoff:g} sigma", joint, per, params)
    target_fits = [r for r in per[target_id] if r["config"]]
    if target_fits and all(per[c] for c in ids):
        others = [c for c in ids if c != target_id]
        return Diagnosis("out_of_space_suspected",
                         f"out-of-space suspected: {len(target_fits)} tested configuration(s) fit {target_id}, and "
                         f"every other claim ({', '.join(others)}) fits some tested configuration, but none of the "
                         f"{tested} tested configurations fits them all. The claims are mutually inconsistent under "
                         "every tested condition, which points to a cause outside the exposed settings (code, data "
                         "or evaluation)", joint, per, params)
    missing = [c for c in ids if not [r for r in per[c] if r["config"]] and not any(r["config"] == {} for r in per[c])]
    return Diagnosis("out_of_space_likely",
                     f"out-of-space likely: no tested configuration comes within {cutoff:g} sigma of "
                     f"{', '.join(missing) or target_id}, among {tested} tested", joint, per, params)
