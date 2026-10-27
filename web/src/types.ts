// The shapes the site reads: the showcase manifest (scripts/build_showcase.py), a recorded run and its Gap Report
// (gapfinder/api/server.py, gapfinder/report), its event stream, and the GapBench scoreboard. Fields the pages don't
// read are left out; every type here describes JSON, so nothing in it is a class.

export type Changes = Record<string, string>;
export type VerdictWord = "found" | "partial" | "no_gap" | "missed";

// ------------------------------------------------------------------ the showcase manifest
export interface GaugeData {
  claim?: string;
  metric?: string;
  paper: number;
  code: number;
  after: number | null;
  band: number | null;
  changes?: Changes;
  label?: string | null;
  runs?: number;
  quote?: string | null;
  figure?: string | null;
}

export interface VersionRun { id: string; verdict: VerdictWord; reading: string; gauge: GaugeData | null }

export interface RealCase {
  slug: string;
  title: string;
  venue: string;
  documented_cause: string;
  current: string;
  versions: Record<string, VersionRun>;
}

export interface PlantedCase {
  id: string;
  gauge: GaugeData | null;
  paper: string;
  title: string;
  version: string;
  seed: number;
  family: string;
  planted: string[];
  found: Changes;
  label: string | null;
}

export interface GapBenchCase {
  id: string;
  gauge: GaugeData | null;
  title: string;
  category: string;
  outcome: string;
  found: Record<string, { label: string; changes: Changes }>;
}

export interface PlantedTotal {
  version: string;
  adopted: boolean;
  seed: number;
  gaps: number;
  found: number;
  confidently_wrong: number;
  controls: number;
  controls_correct: number;
  by_kind: Record<string, [number, number]>;
}

export interface DevSuiteRow { version: string; runs: number[]; correct: number; adopted?: boolean }
export interface VersionInfo { frozen: string; adopted: boolean; status: string }

export interface Showcase {
  note: string;
  verdict_words: Record<VerdictWord, string>;
  real: RealCase[];
  real_tally: Partial<Record<VerdictWord, number>>;
  tally_version: string;
  real_versions: string[];
  versions?: Record<string, VersionInfo>;
  blind: { papers: number; correct: number; partial: number; missed: number; confidently_wrong: number; note: string };
  dev_suite: DevSuiteRow[];
  planted: PlantedCase[];
  planted_totals: PlantedTotal[];
  gapbench: GapBenchCase[];
  gapbench_totals: { run: number; version: string; runs: number; outcomes: Record<string, number> };
}

// ------------------------------------------------------------------ a Gap Report
export interface Target {
  claim_id: string;
  metric: string;
  paper_value: number;
  held_out?: boolean;
  figure?: string | null;
}

export interface Experiment {
  found: boolean;
  note?: string;
  config: { knob: string; naive: string | null; candidate: string }[];
  command?: string | null;
  env?: Record<string, string>;
  parent_checkpoint?: string;
  result_checkpoint?: string | null;
  branches?: { id: string; value: number | null }[];
  metric?: string;
  gap_after?: number | null;
  repeats?: number;
}

export interface Effect {
  candidate: number | null; naive: number | null; diff: number | null; ci: [number, number] | null; alpha: number;
  excludes_zero?: boolean; n_candidate?: number; n_naive?: number;
}

export interface PaperClaim {
  recorded: boolean; quote?: string; page?: number | null; figure?: string | null; metric: string; paper_value: number;
  unit?: string | null; headline?: boolean;
}

export interface SetupCheck { reproducible?: boolean | null; note: string }

export interface Measured {
  median: number; n?: number; repeats?: number[]; min?: number | null; max?: number | null; band: number; cv?: number | null;
  band_rel: number; gap: number; setup_check?: SetupCheck | null;
}

export interface Belief { note: string; checks: { kind: string; ok: boolean | null; text: string }[] }

export interface Lead { knob: string; value: string; units?: number; gap?: number }
export interface Unknown {
  untestable: { knob: string; value: string }[];
  unmapped: string[];
  setup?: SetupCheck | null;
  leads: Lead[];
  alternatives: { changes: Changes; gap: number; mean_abs_gap: number; runs: number }[];
}

export interface HistoryFit { config: Changes; I?: Record<string, number> }
export interface Diagnosis {
  kind: string;
  text: string;
  per_claim?: Record<string, HistoryFit[]>;
  islands?: unknown[][];
  leads?: { family: string; detail: string; file: string; line: number }[];
}

export interface Attribution { confidence_label?: string | null }

export interface Claim {
  target: Target;
  status: string;
  gap_before: number | null;
  gap_after: number | null;
  band: number;
  changes?: Changes;
  hypotheses_tested: number;
  attribution: Attribution | null;
  cause?: { kind: string; text: string } | null;
  experiment?: Experiment | null;
  effect?: Effect | null;
  paper_claim?: PaperClaim | null;
  measured?: Measured | null;
  belief?: Belief | null;
  unknown?: Unknown | null;
  diagnosis?: Diagnosis | null;
  equivalent?: ({ config: Changes } | null)[];
  missing_sentence?: { paragraph: string; insert_after: number; sentence: string; page: number } | null;
  notes?: string[];
}

export interface Provenance {
  gapfinder?: { commit?: string | null; dirty?: boolean };
  models?: Record<string, string>;
  prompt_sha256?: Record<string, string>;
  harness_spec_sha256?: string | null;
  cost?: { nemotron_billed_usd: number; sandbox_reported_usd: number; total_usd: number; scope: string } | null;
}

export interface Report {
  paper?: string;
  artifact: string;
  generated: string;
  partial?: boolean;
  runs: number;
  setup_runs: number;
  claims: Claim[];
  closest_overall?: { changes: Changes; runs: number; gaps?: Record<string, number>; mean_abs_gap: number }[];
  triaged_failures?: { knob: string; value: string; kind: string; why: string; retried?: string | null; suggestion?: string | null }[];
  setup_check?: SetupCheck | null;
  provenance?: Provenance | null;
  missing_sentence_meta?: { drafted?: number };
}

export interface RunMeta {
  title?: string;
  group?: string;
  version?: string;
  seed?: number;
  planted?: string[];
  hidden?: Changes;
  note?: string;
}

export interface Run {
  id: string;
  meta: RunMeta;
  report: Report | null;
  events: number;
  recorded_at: number | null;
  duration_s: number;
}

// ------------------------------------------------------------------ the event stream
export interface Branch {
  id: string;
  status?: string;
  note?: string;
  knob_changes?: Changes;
  parsed_metrics?: Record<string, number>;
}

type Base = { seq: number; t?: number };
export type GfEvent = Base & (
  | { type: "checkpoint"; node: { stage: string; tag?: string | null } }
  | { type: "branch_created" | "branch_started" | "branch_finished"; branch: Branch }
  | { type: "noise_band"; metric: string; median: number; band: number }
  | { type: "survivor" | "pruned"; knob: string; value: string; units: number }
  | { type: "round"; name: string }
  | { type: "verified"; changes: Changes; label: string }
  | { type: "attribution"; claim: string; label?: string | null; status?: string; changes?: Changes; gap_before?: number; gap_after?: number }
  | { type: "cost"; setup_runs?: number }
  | { type: "note"; msg: string }
  | { type: "run_started" | "run_finished" | "trace" | "done" }
);

// ------------------------------------------------------------------ the GapBench scoreboard
export interface WilsonRate { k: number; n: number; rate: number | null; lo: number; hi: number }
export interface TrustRow { runs: number; [col: string]: number }
export interface ArmStats {
  tasks: number;
  solved_median_run?: number | null;
  solved_best_run?: number | null;
  false_attribution_rate?: number | null;
  median_cost_usd?: number | null;
  median_wall_s?: number | null;
  trust_matrix?: { cause: TrustRow; no_cause: TrustRow };
  rates?: { correct?: WilsonRate; confidently_wrong?: WilsonRate; correct_abstention?: WilsonRate; missed?: WilsonRate };
  answer_stability?: { mean: number | null };
}
export interface ScoreRow { task: string; type: string; arm: string; correct: boolean; false_attr?: boolean;
  claims: Record<string, { label?: string; knobs?: Changes }> }
export interface Split { file: string; run: number; summary?: Record<string, ArmStats>; rows?: ScoreRow[] }
export type Scoreboard = Record<string, Split>;
