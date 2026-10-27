// Folds the recorded event stream into what the replay screen draws, and lays it out as a timeline.
import { changesText } from "./ui.jsx";

// Same timing rule as the server's SSE replay (gapfinder/api/server.py): original spacing / speed,
// with idle gaps capped at MAX_IDLE_S.
export const MAX_IDLE_S = 2.0;

// seconds to wait between event a and event b at this speed
export function gap(events, a, b, speed) {
  const t = events[a]?.t, next = events[b]?.t;
  return a >= 0 && t != null && next != null ? Math.min((next - t) / speed, MAX_IDLE_S) : 0;
}

export const ROUNDS = ["noise", "screen", "confirm", "combine", "bisect", "counterfactual", "other"];
export const STAGE_NAME = { noise: "Measuring the noise", screen: "Screening settings", confirm: "Confirming with repeats",
  combine: "Combining what survived", bisect: "Cutting to the smallest answer", counterfactual: "Reverting each change",
  other: "Code rounds, probes and checks" };
export const STAGE_SHORT = { noise: "Noise", screen: "Screen", confirm: "Confirm", combine: "Combine", bisect: "Cut",
  counterfactual: "Revert", other: "Checks" };

// The stages along the event stream: each run a branch starts belongs to a stage; consecutive runs of one stage make a
// segment, which lasts until the next stage begins. [{round, from, to}] in event indexes.
export function stages(events) {
  const out = [];
  events.forEach((ev, i) => {
    if (ev.type !== "branch_created") return;
    const r = roundOf(ev.branch?.note);
    if (out.length && out[out.length - 1].round === r) return;
    if (out.length) out[out.length - 1].to = i;
    out.push({ round: r, from: out.length ? i : 0, to: events.length });
  });
  return out;
}

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

const knobText = (k) => changesText(k) || "the code as released";
const one = (k, v) => changesText({ [k]: v });

export function describe(ev) {
  switch (ev.type) {
    case "checkpoint": return ev.node.stage === "branch" ? null : `checkpoint: ${ev.node.stage}${ev.node.tag ? ` (${ev.node.tag})` : ""}`;
    case "branch_created": return `run ${ev.branch.id}: ${knobText(ev.branch.knob_changes)}`;
    case "branch_finished": {
      const b = ev.branch;
      const m = Object.entries(b.parsed_metrics || {}).slice(0, 2).map(([k, v]) => `${k} ${v}`).join(", ");
      return `run ${b.id} ${b.status === "succeeded" ? "finished" : b.status}${m ? `: ${m}` : ""}`;
    }
    case "noise_band": return `noise measured on ${ev.metric}: ${ev.median.toFixed(3)} ± ${ev.band.toFixed(3)}`;
    case "survivor": return `kept after the screen: ${one(ev.knob, ev.value)} (moved the number ${Math.abs(ev.units).toFixed(1)}× the noise)`;
    case "pruned": return `dropped: ${one(ev.knob, ev.value)} (moved it only ${Math.abs(ev.units).toFixed(1)}× the noise)`;
    case "round": return `${(STAGE_NAME[ev.name] || ev.name).toLowerCase()}: done`;
    case "verified": return `checked ${knobText(ev.changes)}: ${ev.label}`;
    case "attribution": return `verdict on ${ev.claim}: ${ev.label || ev.status}`;
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
