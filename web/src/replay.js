// Folds the recorded event stream into what the replay screen draws.

export const ROUNDS = ["noise", "screen", "confirm", "combine", "bisect", "counterfactual", "other"];

export function roundOf(note) {
  const n = (note || "").toLowerCase();
  if (n.startsWith("noise")) return "noise";
  if (n.startsWith("screen")) return "screen";
  if (n.startsWith("confirm")) return "confirm";
  if (n.startsWith("combine")) return "combine";
  if (n.startsWith("bisect")) return "bisect";
  if (n.startsWith("counterfactual")) return "counterfactual";
  return "other";
}

export function initialState() {
  return { checkpoints: [], branches: {}, order: [], noise: {}, verdicts: {}, attributions: {},
           cost: null, feed: [], done: false, t0: null, t: null };
}

const knobText = (k) => Object.entries(k || {}).map(([a, b]) => `${a}=${b}`).join(", ") || "defaults";

export function describe(ev) {
  switch (ev.type) {
    case "checkpoint": return ev.node.stage === "branch" ? null : `checkpoint ${ev.node.stage}${ev.node.tag ? ` (${ev.node.tag})` : ""}`;
    case "branch_created": return `fork ${ev.branch.id}: ${knobText(ev.branch.knob_changes)} [${roundOf(ev.branch.note)}]`;
    case "branch_finished": {
      const b = ev.branch;
      const m = Object.entries(b.parsed_metrics || {}).slice(0, 2).map(([k, v]) => `${k}=${v}`).join(" ");
      return `${b.id} ${b.status}${m ? `: ${m}` : ""}`;
    }
    case "noise_band": return `noise band ${ev.metric}: median ${ev.median.toFixed(3)} ± ${ev.band.toFixed(3)}`;
    case "survivor": return `survives screen: ${ev.knob}=${ev.value} (${ev.units} noise units)`;
    case "pruned": return `pruned: ${ev.knob}=${ev.value} (${ev.units} noise units)`;
    case "round": return `round ${ev.name} done`;
    case "verified": return `verified ${knobText(ev.changes)} → ${ev.label}`;
    case "attribution": return `${ev.claim}: ${ev.label || ev.status}`;
    case "note": return ev.msg;
    default: return null;
  }
}

export function reduce(s, ev) {
  const next = { ...s, t: ev.t ?? s.t, t0: s.t0 ?? ev.t ?? null };
  switch (ev.type) {
    case "checkpoint":
      next.checkpoints = [...s.checkpoints, ev.node];
      break;
    case "branch_created":
    case "branch_finished": {
      const b = ev.branch;
      if (b.id === undefined) break;
      const prev = s.branches[b.id];
      next.branches = { ...s.branches, [b.id]: { ...(prev || {}), ...b, round: roundOf(b.note || prev?.note) } };
      if (!prev) next.order = [...s.order, b.id];
      break;
    }
    case "noise_band":
      next.noise = { ...s.noise, [ev.metric]: ev };
      break;
    case "survivor":
    case "pruned":
      next.verdicts = { ...s.verdicts, [`${ev.knob}=${ev.value}`]: ev.type };
      break;
    case "attribution":
      next.attributions = { ...s.attributions, [ev.claim]: ev };
      break;
    case "cost":
      next.cost = ev;
      break;
    default:
      break;
  }
  const line = describe(ev);
  if (line) next.feed = [{ seq: ev.seq, type: ev.type, line }, ...s.feed].slice(0, 14);
  return next;
}

// Status colour for a branch chip, using screen verdicts for single-knob branches.
export function chipClass(b, verdicts) {
  if (b.status === "running" || b.status === "queued") return "running";
  if (b.status !== "succeeded") return "failed";
  const keys = Object.entries(b.knob_changes || {});
  if (b.round === "screen" && keys.length === 1) {
    const v = verdicts[`${keys[0][0]}=${keys[0][1]}`];
    if (v === "pruned") return "pruned";
    if (v === "survivor") return "survivor";
  }
  return "done";
}
