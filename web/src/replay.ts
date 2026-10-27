// Folds the recorded event stream into what the replay screen draws, and lays it out as a timeline.
import { useMemo, useRef } from "react";
import type { Branch, Changes, GfEvent } from "./types.ts";
import { changesText } from "./ui.tsx";

// Same timing rule as the server's SSE replay (gapfinder/api/server.py): original spacing / speed,
// with idle gaps capped at MAX_IDLE_S.
export const MAX_IDLE_S = 2.0;

// seconds to wait between event a and event b at this speed
export function gap(events: GfEvent[], a: number, b: number, speed: number): number {
  const t = events[a]?.t, next = events[b]?.t;
  return a >= 0 && t != null && next != null ? Math.min((next - t) / speed, MAX_IDLE_S) : 0;
}

export const ROUNDS = ["noise", "screen", "confirm", "combine", "bisect", "counterfactual", "other"] as const;
export type Round = (typeof ROUNDS)[number];
export const STAGE_NAME: Record<Round, string> = { noise: "Measuring the noise", screen: "Screening settings", confirm: "Confirming with repeats",
  combine: "Combining what survived", bisect: "Cutting to the smallest answer", counterfactual: "Reverting each change",
  other: "Code rounds, probes and checks" };
export const STAGE_SHORT: Record<Round, string> = { noise: "Noise", screen: "Screen", confirm: "Confirm", combine: "Combine", bisect: "Cut",
  counterfactual: "Revert", other: "Checks" };

export function roundOf(note: string | undefined): Round {
  const n = (note || "").toLowerCase();
  return (ROUNDS.find((r) => r !== "other" && n.startsWith(r)) || "other");
}

export interface Segment { round: Round; from: number; to: number }

// The stages along the event stream: each run a branch starts belongs to a stage; consecutive runs of one stage make a
// segment, which lasts until the next stage begins. Event indexes.
export function stages(events: GfEvent[]): Segment[] {
  const out: Segment[] = [];
  events.forEach((ev, i) => {
    if (ev.type !== "branch_created") return;
    const r = roundOf(ev.branch?.note);
    if (out.length && out[out.length - 1].round === r) return;
    if (out.length) out[out.length - 1].to = i;
    out.push({ round: r, from: out.length ? i : 0, to: events.length });
  });
  return out;
}

export interface RunState extends Branch { round: Round }
export interface FeedLine { seq: number; type: string; line: string }
export interface ReplayState {
  checkpoints: { stage: string; tag?: string | null }[];
  branches: Record<string, RunState>;
  order: string[];
  noise: Record<string, { median: number; band: number }>;
  verdicts: Record<string, "survivor" | "pruned">;
  attributions: Record<string, Extract<GfEvent, { type: "attribution" }>>;
  cost: { setup_runs?: number } | null;
  feed: FeedLine[];
  t0: number | null;
  t: number | null;
}

export function initialState(): ReplayState {
  return { checkpoints: [], branches: {}, order: [], noise: {}, verdicts: {}, attributions: {}, cost: null, feed: [], t0: null, t: null };
}

const knobText = (k: Changes | undefined) => changesText(k) || "the code as released";
const one = (k: string, v: string) => changesText({ [k]: v });

export function describe(ev: GfEvent): string | null {
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
    case "round": return `${(STAGE_NAME[ev.name as Round] || ev.name).toLowerCase()}: done`;
    case "verified": return `checked ${knobText(ev.changes)}: ${ev.label}`;
    case "attribution": return `verdict on ${ev.claim}: ${ev.label || ev.status}`;
    case "note": return ev.msg;
    default: return null;
  }
}

export function reduce(s: ReplayState, ev: GfEvent): ReplayState {
  const next: ReplayState = { ...s, t: ev.t ?? s.t, t0: s.t0 ?? ev.t ?? null };
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

// The state after the first `pos` events, from scratch: what the player's cached fold must always equal.
export function foldTo(events: GfEvent[], pos: number): ReplayState {
  let s = initialState();
  for (let i = 0; i < pos; i++) s = reduce(s, events[i]);
  return s;
}

const SNAP = 64; // a folded state is kept every SNAP events, so dragging back never refolds more than SNAP

interface FoldCache { events: GfEvent[]; snaps: Map<number, ReplayState>; pos: number; state: ReplayState }

// The state after the first `pos` events: folded forward from where it was, or from the nearest kept state behind.
// Equal to foldTo(events, pos), which the tests check.
export function useFold(events: GfEvent[] | null, pos: number): ReplayState {
  const cache = useRef<FoldCache | null>(null);
  return useMemo(() => {
    if (!events) return initialState();
    let c = cache.current;
    if (!c || c.events !== events) c = cache.current = { events, snaps: new Map([[0, initialState()]]), pos: 0, state: initialState() };
    let from = c.pos, s = c.state;
    if (pos < from) {
      from = Math.floor(pos / SNAP) * SNAP;
      while (!c.snaps.has(from)) from -= SNAP;
      s = c.snaps.get(from) as ReplayState;
    }
    for (let i = from; i < pos; i++) {
      s = reduce(s, events[i]);
      if ((i + 1) % SNAP === 0) c.snaps.set(i + 1, s);
    }
    c.pos = pos; c.state = s;
    return s;
  }, [events, pos]);
}

// Status colour for a branch chip, using screen verdicts for single-knob branches.
export function chipClass(b: RunState, verdicts: ReplayState["verdicts"]): string {
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
