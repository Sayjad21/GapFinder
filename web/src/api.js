export async function getJSON(path) {
  const r = await fetch(path);
  if (!r.ok) throw new Error(`${path}: ${r.status}`);
  return r.json();
}

export const api = {
  runs: () => getJSON("/api/runs"),
  run: (id) => getJSON(`/api/runs/${encodeURIComponent(id)}`),
  scoreboard: () => getJSON("/api/scoreboard"),
  replayUrl: (id, speed) => `/api/runs/${encodeURIComponent(id)}/replay?speed=${speed}`,
  reportMdUrl: (id) => `/api/runs/${encodeURIComponent(id)}/report.md`,
};

export const pct = (x) => (x === null || x === undefined ? "n/a" : `${x >= 0 ? "+" : ""}${(x * 100).toFixed(1)}%`);

export const LABEL_CLASS = {
  Explained: "ok",
  "Paper-artifact inconsistency": "ok",
  "Fits but unsupported": "warn",
  "Partially explained": "warn",
  Unexplained: "muted",
  Reproduced: "muted",
};
