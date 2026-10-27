import type { GfEvent, Run, Scoreboard, Showcase } from "./types.ts";

export async function getJSON<T>(path: string): Promise<T> {
  const r = await fetch(path);
  if (!r.ok) throw new Error(`${path}: ${r.status}`);
  return r.json() as Promise<T>;
}

// VITE_STATIC=1 builds the server-free site (GitHub Pages): data comes from files written by
// scripts/export_static.py. Either way the replay loads a run's events once and plays them in the browser.
export const STATIC = import.meta.env.VITE_STATIC === "1";
const enc = encodeURIComponent;

// A new investigation's request: started (a run to watch), or not, with the reason in plain words. Never a throw.
export type Submitted = { ok: true; run: string } | { ok: false; reason: string };

const NOT_HERE = "This public site replays recorded investigations; it can’t start new ones. Running one takes a GapFinder "
  + "install with access to Sandboxes, where every experiment runs.";

async function submitLive(request: unknown): Promise<Submitted> {
  try {
    const r = await fetch("/api/live", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(request) });
    const j = await r.json().catch(() => ({})) as { ok?: boolean; run?: string; reason?: string };
    if (r.ok && j.ok && j.run) return { ok: true, run: j.run };
    return { ok: false, reason: j.reason || NOT_HERE };
  } catch {
    return { ok: false, reason: "GapFinder’s server didn’t answer, so nothing was started." };
  }
}

export interface Api {
  run: (id: string) => Promise<Run>;
  scoreboard: () => Promise<Scoreboard>;
  showcase: () => Promise<Showcase>;
  events: (id: string) => Promise<GfEvent[]>;
  submit: (request: unknown) => Promise<Submitted>;
  reportMdUrl: (id: string) => string;
  issueDraftUrl: (id: string) => string;
  runJsonUrl: (id: string) => string;
}

export const api: Api = STATIC ? {
  submit: async () => ({ ok: false, reason: NOT_HERE }),
  run: (id) => getJSON(`data/runs/${enc(id)}.json`),
  scoreboard: () => getJSON("data/scoreboard.json"),
  showcase: () => getJSON("data/showcase.json"),
  events: (id) => getJSON(`data/runs/${enc(id)}/events.json`),
  reportMdUrl: (id) => `data/runs/${enc(id)}/report.md`,
  issueDraftUrl: (id) => `data/runs/${enc(id)}/issue_draft.md`,
  runJsonUrl: (id) => `data/runs/${enc(id)}.json`,
} : {
  submit: submitLive,
  run: (id) => getJSON(`/api/runs/${enc(id)}`),
  scoreboard: () => getJSON("/api/scoreboard"),
  showcase: () => getJSON("/api/showcase"),
  events: (id) => getJSON(`/api/runs/${enc(id)}/events`),
  reportMdUrl: (id) => `/api/runs/${enc(id)}/report.md`,
  issueDraftUrl: (id) => `/api/runs/${enc(id)}/issue_draft.md`,
  runJsonUrl: (id) => `/api/runs/${enc(id)}`,
};

export const pct = (x: number | null | undefined): string =>
  (x === null || x === undefined ? "n/a" : `${x >= 0 ? "+" : ""}${(x * 100).toFixed(1)}%`);

export const LABEL_CLASS: Record<string, string> = {
  Explained: "ok",
  "Paper-artifact inconsistency": "ok",
  "Fits but unsupported": "warn",
  "Explained by the reporting rule": "ok",
  "Paper's stated value refuted; unique fit": "warn",
  "Partially explained": "warn",
  Unexplained: "muted",
  Reproduced: "muted",
  Inconclusive: "warn",
  "Explains target, conflicts with held-out": "warn",
};
