export async function getJSON(path) {
  const r = await fetch(path);
  if (!r.ok) throw new Error(`${path}: ${r.status}`);
  return r.json();
}

// VITE_STATIC=1 builds the server-free site (GitHub Pages): data comes from files written by
// scripts/export_static.py, and replay runs in the browser instead of over SSE.
export const STATIC = import.meta.env.VITE_STATIC === "1";
const enc = encodeURIComponent;

export const api = STATIC ? {
  runs: () => getJSON("data/runs.json"),
  run: (id) => getJSON(`data/runs/${enc(id)}.json`),
  scoreboard: () => getJSON("data/scoreboard.json"),
  events: (id) => getJSON(`data/runs/${enc(id)}/events.json`),
  reportMdUrl: (id) => `data/runs/${enc(id)}/report.md`,
  issueDraftUrl: (id) => `data/runs/${enc(id)}/issue_draft.md`,
  runJsonUrl: (id) => `data/runs/${enc(id)}.json`,
} : {
  runs: () => getJSON("/api/runs"),
  run: (id) => getJSON(`/api/runs/${enc(id)}`),
  scoreboard: () => getJSON("/api/scoreboard"),
  replayUrl: (id, speed) => `/api/runs/${enc(id)}/replay?speed=${speed}`,
  reportMdUrl: (id) => `/api/runs/${enc(id)}/report.md`,
  issueDraftUrl: (id) => `/api/runs/${enc(id)}/issue_draft.md`,
  runJsonUrl: (id) => `/api/runs/${enc(id)}`,
};

export const pct = (x) => (x === null || x === undefined ? "n/a" : `${x >= 0 ? "+" : ""}${(x * 100).toFixed(1)}%`);

export const LABEL_CLASS = {
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
