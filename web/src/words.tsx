import { useId, useState, type ReactNode } from "react";
import type { Showcase, Target } from "./types.ts";
import { prettyKnob, tipPlace } from "./ui.tsx";

// The page's vocabulary: what the engine's internal names are called for a reader, and a definition for every word a
// reader new to the project would have to guess at.

// ------------------------------------------------------------------ engine versions
// The repository calls the frozen engine versions c1, c2, ...; the page calls them v1, v2, ... and says where each stands.
export const vName = (v: string | null | undefined): string => (v ? String(v).replace(/^c/, "v") : "");
const STATUS_WORDS: Record<string, string> = { current: "current", earlier: "earlier, adopted", "on trial": "on trial", "not adopted": "not adopted" };
export function versionStatus(data: Showcase | null, v: string): string | null {
  const s = data?.versions?.[v]?.status;
  return s ? STATUS_WORDS[s] || s : v === data?.tally_version ? "current" : null;
}
export const currentVersion = (data: Showcase): string => data.tally_version;

// ------------------------------------------------------------------ the glossary
export type TermKey = keyof typeof GLOSSARY;
export const GLOSSARY = {
  version: ["Engine version", "GapFinder’s search code is frozen into numbered versions (v1, v2, …; c1, c2, … in the repository). A new version is adopted only if it does no worse on a fresh batch of planted gaps made after it was frozen."],
  batch: ["Fresh batch", "Planted gaps generated from a new random seed after a version was frozen, so the engine has never seen them. Batch 8 is seed 8."],
  planted: ["Planted gap", "A known change, such as a setting, a unit convention, a data cut or a one-line code edit, put into a paper whose code reproduces. The right answer is known, so the search can be scored."],
  control: ["Control", "A task with nothing planted. The right answer is “no gap”, and changing anything is wrong."],
  noise: ["Run-to-run noise", "How much the code’s number moves over five identical runs. A gap inside this spread is not a gap."],
  harness: ["Harness", "A short file that says how to build the released code, run it, read its numbers, and which settings may change. A person approves it before anything runs."],
  held_out: ["Held-out number", "Another number from the same paper, kept aside. An answer that closes the gap must not make it worse."],
  posthoc: ["Post-hoc", "The cause was already known, and fixes to the engine were found on these same papers. The result demonstrates the engine; it does not test it."],
  confidently_wrong: ["Confidently wrong", "An answer labelled as explained that is not the real cause: the one outcome GapFinder is built to avoid."],
  dev_suite: ["Dev suite", "138 GapBench runs replayed at no cost from cached model answers, to check that a new version breaks nothing that worked."],
  gapbench: ["GapBench", "Generated tasks with a known cause, a decoy, interacting causes or no cause at all, used to compare GapFinder with a general coding agent."],
  abstain: ["Abstaining", "Saying “nothing I can change explains this gap” instead of guessing. On a task with no cause it is the right answer."],
  sealed: ["Sealed blind papers", "Real papers whose causes were hidden from the people tuning the engine until after it ran. The only clean evidence here."],
} satisfies Record<string, [string, string]>;

// A word with its definition on hover, focus or tap. The definition is in the page for screen readers either way.
export function Term({ k, children }: { k: TermKey; children?: ReactNode }) {
  const [at, setAt] = useState<{ left: number; top: number } | null>(null);
  const id = useId();
  const [word, text] = GLOSSARY[k];
  const show = (el: Element) => setAt(tipPlace(el));
  const hide = () => setAt(null);
  return (
    <span className="term-wrap">
      <button type="button" className="term" aria-describedby={id}
              onPointerEnter={(e) => e.pointerType === "mouse" && show(e.currentTarget)}
              onPointerLeave={(e) => e.pointerType === "mouse" && hide()}
              onFocus={(e) => show(e.currentTarget)} onBlur={hide} onClick={(e) => (at ? hide() : show(e.currentTarget))}
              onKeyDown={(e) => e.key === "Escape" && hide()}>
        {children ?? word.toLowerCase()}
      </button>
      <span id={id} role="tooltip" className={at ? "tooltip" : "visually-hidden"} style={at ?? undefined}>
        <b>{word}</b>{text}
      </span>
    </span>
  );
}

// ------------------------------------------------------------------ the engine's labels, in plain words
export const LABEL_PLAIN: Record<string, string> = {
  Explained: "Explained, with evidence",
  "Paper-artifact inconsistency": "The paper and its code disagree",
  "Fits but unsupported": "A change fits, but nothing else confirms it",
  "Explained by the reporting rule": "Explained by how the paper reports its number",
  "Paper's stated value refuted; unique fit": "The paper’s stated value doesn’t fit; one other value does",
  "Partially explained": "Partly explained",
  Unexplained: "Nothing it could change explains the gap",
  Reproduced: "The code reproduces the paper’s number",
  Inconclusive: "Too noisy to tell",
  "Explains target, conflicts with held-out": "Fits this number but breaks another",
};
export const plain = (label: string): string => LABEL_PLAIN[label] || label;

// The plain words, with the engine's own label kept for anyone matching it against a report file.
export function PlainLabel({ label, formal = false }: { label?: string | null; formal?: boolean }) {
  const l = label || "Reproduced";
  return (
    <span className="plain-label" title={`GapFinder’s label: ${l}`}>
      {plain(l)}{formal && plain(l) !== l && <small className="formal"> ({l})</small>}
    </span>
  );
}

// prose with `backticked` identifiers, the identifiers set as code
export function WithCode({ text }: { text: string }) {
  return <>{String(text).split(/`([^`]+)`/).map((s, i) => (i % 2 ? <code key={i}>{s}</code> : s))}</>;
}

// ------------------------------------------------------------------ a planted change, as the scorer words it
// "scale: lr: the paper's v is the code's 0.5 x v" reads "lr: a value the paper states as v is 0.5 × v in the code";
// "setting: wd = 0.001" reads "wd = 0.001". The identifier is code, the description prose.
export function PlantedChange({ text }: { text: string }) {
  const t = text.replace(/^\w+: /, "");
  const i = t.indexOf(": ");
  if (i > 0 && !t.slice(0, i).includes(" ")) {
    const rest = t.slice(i + 2).replace(/ x /g, " × ").replace(/^the paper's v is the code's (.+?) × v$/, "a value the paper states as v is $1 × v in the code");
    return <span className="planted"><code>{prettyKnob(t.slice(0, i))}</code> <WithCode text={rest} /></span>;
  }
  const [k, v] = t.split(" = ");
  return <span className="planted"><code>{v !== undefined ? `${prettyKnob(k)} = ${v}` : t}</code></span>;
}

// ------------------------------------------------------------------ names
// A claim is named by where the paper prints it ("Table 2 (SDCN ACC, dataset=ACM)"); the internal id is the fallback.
export const claimName = (t: Partial<Target> | null | undefined): string =>
  (t?.figure ? t.figure : String(t?.claim_id || "").replace(/^C_?/, "").replace(/_/g, " "));

export const KIND_WORDS: Record<string, string> = { setting: "A changed setting", scale: "A scale or unit convention", data: "A training-data cut",
  code: "A code defect", reporting: "A reporting rule", control: "A control (nothing planted)" };
export const GAPBENCH_WORDS: Record<string, string> = { known_cause: "A known cause", decoy: "A cause with a decoy", interaction: "Two interacting causes",
  no_cause: "No cause", noise_only: "Only noise", incomplete: "Not enough to tell", out_of_space: "A cause outside the settings" };
