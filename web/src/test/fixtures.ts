// Small hand-made data in the shapes the site reads: a manifest with three real papers and a few synthetic cases, one
// recorded run with its report, an event stream that walks the search's stages, and a scoreboard.
import type { GaugeData, GfEvent, Run, Scoreboard, Showcase } from "../types.ts";

const FAST: GaugeData = { claim: "C_cora", metric: "acc", paper: 0.818, code: 0.795, after: 0.8175, band: 0.0097,
  changes: { learning_rate: "0.001" }, label: "Explained", runs: 40, figure: "Table 5" };
const SDCN: GaugeData = { claim: "C_z_acc", metric: "z_acc", paper: 90.45, code: 88.75, after: 90.13, band: 0.01, changes: {},
  label: "Explained by the reporting rule", runs: 5, figure: "Table 2 (SDCN ACC, dataset=ACM)" };
const GAT: GaugeData = { claim: "C_pubmed", metric: "pubmed", paper: 0.79, code: 0.773, after: null, band: 0.03, changes: {},
  label: null, runs: 5, figure: "Table 2" };

export const SHOWCASE: Showcase = {
  note: "fixture",
  verdict_words: { found: "Found the documented cause", partial: "Found part of it", no_gap: "Correctly found no gap", missed: "Missed it" },
  real: [
    { slug: "fastgcn-v15", title: "FastGCN", venue: "ICLR 2018", documented_cause: "A learning rate of 0.001.", current: "c7",
      versions: { c5: { id: "real~fastgcn-v15", verdict: "found", reading: "Explained: lr=0.001.", gauge: FAST },
                  c7: { id: "real-c7~fastgcn-v15", verdict: "found", reading: "Explained: lr=0.001.", gauge: FAST } } },
    { slug: "sdcn", title: "Structural Deep Clustering Network (SDCN)", venue: "WWW 2020", documented_cause: "Best epoch, picked on test labels.",
      current: "c7", versions: { c5: { id: "real~sdcn", verdict: "missed", reading: "Unexplained.", gauge: SDCN },
                                 c7: { id: "real-c7~sdcn", verdict: "found", reading: "Explained by the reporting rule.", gauge: SDCN } } },
    { slug: "gat", title: "Graph Attention Networks (GAT)", venue: "ICLR 2018", documented_cause: "PubMed used its own settings.", current: "c7",
      versions: { c7: { id: "real-c7~gat", verdict: "no_gap", reading: "Reproduced.", gauge: GAT } } },
  ],
  real_tally: { found: 2, no_gap: 1 },
  tally_version: "c7",
  real_versions: ["c5", "c7"],
  versions: { c5: { frozen: "2026-10-23", adopted: true, status: "earlier" }, c7: { frozen: "2026-10-26", adopted: true, status: "current" },
              c10: { frozen: "2026-10-27", adopted: false, status: "on trial" } },
  blind: { papers: 8, correct: 1, partial: 1, missed: 5, confidently_wrong: 1, note: "fixture" },
  dev_suite: [{ version: "c5", runs: [1, 2], correct: 99, adopted: true }, { version: "c7", runs: [3, 4], correct: 100, adopted: true },
              { version: "c10", runs: [5, 6], correct: 100, adopted: false }],
  planted: [
    { id: "synthetic~planted~a", gauge: FAST, paper: "FastGCN", title: "Planted a changed setting in FastGCN", version: "c7", seed: 8,
      family: "setting", planted: ["setting: lr = 0.01"], found: { lr: "0.01" }, label: "Fits but unsupported" },
    { id: "synthetic~planted~b", gauge: FAST, paper: "FastGCN", title: "Planted a scale convention in FastGCN", version: "c5", seed: 6,
      family: "scale", planted: ["scale: lr: the paper's v is the code's 0.5 x v"], found: { lr: "0.005" }, label: "Paper-artifact inconsistency" },
    { id: "synthetic~planted~c", gauge: null, paper: "SparseTSF", title: "Planted nothing in SparseTSF", version: "c7", seed: 8,
      family: "control", planted: [], found: {}, label: null },
    { id: "synthetic~planted~d", gauge: FAST, paper: "RippleNet", title: "Planted a code defect in RippleNet", version: "c3", seed: 4,
      family: "code", planted: ["code: src/train.py:58 `np.mean(x)` → `np.sum(x)`"], found: { "@ast:src/train.py:58:@mut.17.Call.red.sum": "1" },
      label: "Fits but unsupported" },
  ],
  planted_totals: [
    { version: "c5", adopted: true, seed: 6, gaps: 10, found: 4, confidently_wrong: 0, controls: 5, controls_correct: 5, by_kind: { setting: [2, 4] } },
    { version: "c7", adopted: true, seed: 8, gaps: 12, found: 7, confidently_wrong: 0, controls: 6, controls_correct: 6, by_kind: { scale: [3, 5] } },
  ],
  gapbench: [
    { id: "synthetic~gapbench~dev-ml-normalize", gauge: FAST, title: "GapBench dev-ml-normalize: a known cause", category: "known_cause",
      outcome: "correct", found: { C1: { label: "Fits but unsupported", changes: { normalize: "zscore" } } } },
    { id: "synthetic~gapbench~dev-rl-nocause", gauge: null, title: "GapBench dev-rl-nocause: no cause", category: "no_cause",
      outcome: "correct_abstention", found: { C1: { label: "Unexplained", changes: {} } } },
  ],
  gapbench_totals: { run: 10000, version: "c5", runs: 126, outcomes: { correct: 52 } },
};

export const RUN: Run = {
  id: "real-c7~fastgcn-v15",
  meta: { title: "FastGCN (on c7)", group: "real", version: "c7" },
  events: 0,
  recorded_at: 1793015271,
  duration_s: 780,
  report: {
    paper: "FastGCN", artifact: "harness-c7", generated: "2026-10-26 11:00", runs: 12, setup_runs: 1,
    claims: [{
      target: { claim_id: "C_cora", metric: "acc", paper_value: 0.818, figure: "Table 5" },
      status: "searched", gap_before: -0.028, gap_after: -0.0006, band: 0.0097, changes: { learning_rate: "0.001" }, hypotheses_tested: 30,
      attribution: { confidence_label: "Explained" },
      experiment: { found: true, config: [{ knob: "learning_rate", naive: "0.01", candidate: "0.001" }], metric: "acc", gap_after: -0.0006,
                    branches: [{ id: "B0011", value: 0.8175 }], command: "python train.py --lr 0.001", parent_checkpoint: "ck1" },
      belief: { note: "", checks: [{ kind: "reversal", ok: true, text: "without `learning_rate` the gap comes back" },
                                   { kind: "evidence", ok: null, text: "not checked" }] },
      measured: { median: 0.795, n: 5, repeats: [0.794, 0.795, 0.795, 0.796, 0.797], band: 0.008, band_rel: 0.0097, gap: -0.028 },
      unknown: { untestable: [], unmapped: ["epochs", "The code trains for 200 epochs; the paper says 50."], leads: [], alternatives: [] },
      notes: ["a note with `code`"],
    }],
    provenance: null,
  },
};

// noise (5 runs), a screen of 4 settings, two confirming repeats, the verdict: 27 events, two seconds apart
export const EVENTS: GfEvent[] = (() => {
  const out: GfEvent[] = [];
  let seq = 0, t = 1793015271;
  const push = (e: Record<string, unknown>) => { out.push({ seq: ++seq, t: (t += 2), ...e } as GfEvent); };
  push({ type: "checkpoint", node: { stage: "source", tag: "gf/fastgcn/source" } });
  const run = (id: string, note: string, knobs: Record<string, string>, acc: number) => {
    push({ type: "branch_created", branch: { id, note, knob_changes: knobs, status: "running" } });
    push({ type: "branch_finished", branch: { id, note, knob_changes: knobs, status: "succeeded", parsed_metrics: { acc } } });
  };
  for (let i = 1; i <= 5; i++) run(`B000${i}`, "noise", {}, 0.795);
  push({ type: "noise_band", metric: "acc", median: 0.795, band: 0.008 });
  [["learning_rate", "0.001", 0.817], ["learning_rate", "0.1", 0.7], ["hidden1", "64", 0.799], ["weight_decay", "0", 0.79]]
    .forEach(([k, v, acc], i) => run(`B000${6 + i}`, "screen", { [k as string]: v as string }, acc as number));
  push({ type: "survivor", knob: "learning_rate", value: "0.001", units: 3.1 });
  push({ type: "pruned", knob: "learning_rate", value: "0.1", units: -0.4 });
  run("B0010", "confirm", { learning_rate: "0.001" }, 0.818);
  run("B0011", "confirm", { learning_rate: "0.001" }, 0.817);
  push({ type: "attribution", claim: "C_cora", status: "searched", label: "Explained", changes: { learning_rate: "0.001" }, gap_before: -0.028, gap_after: -0.0006 });
  return out;
})();

const tm = { cause: { runs: 15, correct_cause: 9, partial: 1, wrong_confident: 0, abstained: 0, missed: 5 },
             no_cause: { runs: 15, correct_cause: 0, partial: 0, wrong_confident: 0, abstained: 15, missed: 0 } };
const w = (k: number, n: number) => ({ k, n, rate: k / n, lo: 0.1, hi: 0.8 });
export const SCOREBOARD: Scoreboard = {
  test: {
    file: "gapbench_test_v13.json", run: 13,
    summary: {
      gapfinder: { tasks: 10, solved_median_run: 8, solved_best_run: 8, false_attribution_rate: 0, median_cost_usd: 0.049, median_wall_s: 52,
                   trust_matrix: tm, rates: { correct: w(9, 15), confidently_wrong: w(0, 30), correct_abstention: w(15, 15), missed: w(5, 15) },
                   answer_stability: { mean: 0.8 } },
      "baseline-super": { tasks: 10, solved_median_run: 1, solved_best_run: 2, false_attribution_rate: 0.73, median_cost_usd: 0.052, median_wall_s: 76,
                          trust_matrix: tm, rates: { correct: w(2, 15) }, answer_stability: { mean: 0.5 } },
      "gapfinder-noverify": { tasks: 10, solved_median_run: 6, solved_best_run: 7, trust_matrix: tm },
    },
    rows: Array.from({ length: 30 }, (_, i) => ({ task: `test-v13-${String(1 + (i % 10)).padStart(2, "0")}`, type: i % 2 ? "no_cause" : "known_cause",
      arm: i < 15 ? "gapfinder" : "baseline-super", correct: i % 3 !== 0, false_attr: i % 7 === 0,
      claims: { C1: { label: "Explained", knobs: { lr: "0.01" } } } })),
  },
  dev: { file: "gapbench_dev_v7.json", run: 7, summary: { gapfinder: { tasks: 8, solved_median_run: 7, solved_best_run: 8 } }, rows: [] },
};
