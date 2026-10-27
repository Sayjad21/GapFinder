import { useEffect, useState } from "react";
import { api } from "./api.ts";
import type { GaugeData, Report, Run, Showcase } from "./types.ts";

// ------------------------------------------------------------------ the showcase manifest, fetched once per page load
let manifest: Showcase | null = null;
let pending: Promise<Showcase> | null = null;
export function useShowcase(): { data: Showcase | null; error: Error | null } {
  const [data, setData] = useState<Showcase | null>(manifest);
  const [error, setError] = useState<Error | null>(null);
  useEffect(() => {
    if (manifest) return;
    pending ??= api.showcase();
    pending.then((d) => { manifest = d; setData(d); }).catch((e: Error) => { pending = null; setError(e); });
  }, []);
  return { data, error };
}

// for tests: start from a known manifest, or from none
export function primeShowcase(d: Showcase | null): void { manifest = d; pending = null; }

// ------------------------------------------------------------------ one recorded run
// kept with the id it was fetched for, so a new id reads as loading without resetting anything
export function useRun(id: string | undefined): { run: Run | null; error: Error | null } {
  const [got, setGot] = useState<{ id: string; run?: Run; error?: Error } | null>(null);
  useEffect(() => {
    if (!id) return undefined;
    let dead = false;
    api.run(id).then((run) => !dead && setGot({ id, run })).catch((error: Error) => !dead && setGot({ id, error }));
    return () => { dead = true; };
  }, [id]);
  const mine = got && got.id === id ? got : null;
  return { run: mine?.run ?? null, error: mine?.error ?? null };
}

// a run’s gauge, computed from its report when the manifest has none
export function gaugeOf(report: Report | null): GaugeData | null {
  const c = (report?.claims || []).find((x) => !x.target?.held_out);
  if (!report || !c || c.gap_before === null || c.gap_before === undefined) return null;
  const pv = c.target.paper_value;
  const moved = c.gap_after !== null && c.gap_after !== undefined && Math.abs(c.gap_after - c.gap_before) > 1e-9;
  return { paper: pv, code: pv * (1 + c.gap_before), after: moved && c.gap_after !== null ? pv * (1 + c.gap_after) : null, band: c.band,
           metric: c.target.metric, figure: c.target.figure, changes: c.changes, label: c.attribution?.confidence_label, runs: report.runs };
}
