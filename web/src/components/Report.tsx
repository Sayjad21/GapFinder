import { useState, type ReactNode } from "react";
import { api, pct, LABEL_CLASS } from "../api.ts";
import type { Belief as BeliefT, Changes, Claim, Effect as EffectT, Experiment as ExperimentT, Measured as MeasuredT, PaperClaim,
  Provenance as ProvenanceT, Report as ReportT, Run, Unknown as UnknownT } from "../types.ts";
import { changeText, changesText, prettyKnob } from "../ui.tsx";
import { PlainLabel, WithCode, claimName, plain } from "../words.tsx";

// The Gap Report, readable at three depths: the claims at a glance; each claim's verdict, cause and gap; and, one click
// further, the five questions a reviewer asks, each with a one-line answer on its heading.

const NR = "not recorded";
const num = (x: number | null | undefined) => (x === null || x === undefined ? NR : String(Number(Number(x).toPrecision(4))));
const signed = (x: number | null | undefined) => (x === null || x === undefined ? NR : `${x >= 0 ? "+" : ""}${Number(Number(x).toPrecision(4))}`);
const knobs = (d: Changes | null | undefined) => changesText(d) || "the code as released";
const LEADS_SHOWN = 5;
const plural = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;
const band = (x: number) => `±${(x * 100).toFixed(1)}%`;

function Copy({ text }: { text: string }) {
  const [done, setDone] = useState(false);
  return (
    <button type="button" className="copy" onClick={() => { void navigator.clipboard?.writeText(text); setDone(true); setTimeout(() => setDone(false), 1200); }}>
      {done ? "copied" : "copy"}
    </button>
  );
}

// a question with its one-line answer on the heading; the detail opens below
function Q({ q, gist, open = false, children }: { q: string; gist?: string; open?: boolean; children: ReactNode }) {
  return (
    <details className="q" open={open}>
      <summary><span className="q-q">{q}</span>{gist && <span className="q-gist">{gist}</span>}</summary>
      <div className="q-body">{children}</div>
    </details>
  );
}

function Effect({ e }: { e: EffectT }) {
  const ci = e.ci;
  return (
    <p className="effect">
      Effect: candidate <b>{num(e.candidate)}</b> minus as released <b>{num(e.naive)}</b> = <b>{signed(e.diff)}</b>
      {ci ? <>, {Math.round((1 - e.alpha) * 100)}% bootstrap interval [{signed(ci[0])}, {signed(ci[1])}]
        {e.excludes_zero === false && <b className="warn"> (includes 0)</b>}</> : <>, bootstrap interval {NR}</>}
      {" "}({e.n_candidate ?? NR} candidate runs vs {e.n_naive ?? NR} as released)
    </p>
  );
}

const experimentGist = (x: ExperimentT | null | undefined) => (!x ? NR : !x.found ? "none: no experiment closed it"
  : x.config.map((k) => `${prettyKnob(k.knob)} ${k.naive ?? "?"} → ${k.candidate}`).join(", "));

function Experiment({ x, effect }: { x: ExperimentT | null | undefined; effect: EffectT | null | undefined }) {
  if (!x) return <p className="small">{NR}</p>;
  if (!x.found) return <p>None: {x.note}.</p>;
  const cmd = x.command ? `${Object.entries(x.env || {}).map(([k, v]) => `${k}=${v}`).join(" ")} ${x.command}`.trim() : null;
  const vals = (x.branches || []).map((b) => b.value).filter((v): v is number => v !== null && v !== undefined);
  return (
    <>
      <div className="scroll"><table className="cfg">
        <thead><tr><th scope="col">Setting</th><th scope="col">As released</th><th scope="col">Changed to</th></tr></thead>
        <tbody>{x.config.map((k) => (
          <tr key={k.knob}><td><code>{prettyKnob(k.knob)}</code></td><td>{k.naive === null || k.naive === undefined ? NR : <code>{k.naive}</code>}</td><td><code>{k.candidate}</code></td></tr>
        ))}</tbody>
      </table></div>
      <p>Output: <code>{x.metric}</code> {vals.length ? vals.map(num).join(", ") : `values ${NR}`} · gap after <b>{pct(x.gap_after)}</b>
        {x.branches?.length ? <> · runs {x.branches.map((b) => <code key={b.id}>{b.id}</code>)}</> : null}</p>
      {effect && <Effect e={effect} />}
      {cmd ? (
        <details className="more">
          <summary>The command, to run it yourself</summary>
          <p className="small">Fork checkpoint <code>{x.parent_checkpoint}</code> and run:</p>
          <pre>{cmd}<Copy text={cmd} /></pre>
          {x.result_checkpoint && <p className="small">Result checkpoint <code>{x.result_checkpoint}</code></p>}
        </details>
      ) : <p className="small">Command: {NR}</p>}
    </>
  );
}

const paperGist = (p: PaperClaim | null | undefined) => (!p ? NR
  : p.recorded ? `quoted${p.page ? `, p. ${p.page}` : ""}${p.figure ? `, ${p.figure}` : ""}: ${num(p.paper_value)}`
  : `${num(p.paper_value)}, no quote linked`);

function Paper({ p }: { p: PaperClaim | null | undefined }) {
  if (!p) return <p className="small">{NR}</p>;
  const where = [p.page ? `p. ${p.page}` : null, p.figure].filter(Boolean).join(", ");
  return (
    <>
      {p.recorded
        ? <blockquote>{p.quote}</blockquote>
        : <p className="small">Quote {NR} (the report has no linked ledger claim).</p>}
      <p className="small">{p.recorded ? (where || `location ${NR}`) : "Value used"}: <code>{p.metric}</code> = {num(p.paper_value)}
        {p.unit ? ` ${p.unit}` : ""}{p.headline ? " (headline claim)" : ""}</p>
    </>
  );
}

const measuredGist = (m: MeasuredT | null | undefined) => (!m ? NR
  : `${num(m.median)} over ${m.n ?? "?"} runs as released, noise ${band(m.band_rel)}, gap ${pct(m.gap)}`);

function Measured({ m }: { m: MeasuredT | null | undefined }) {
  if (!m) return <p className="small">{NR}</p>;
  const sc = m.setup_check;
  return (
    <ul>
      <li>Median <b>{num(m.median)}</b> over {m.n ?? NR} runs of the code as released; the runs: {m.repeats?.length ? m.repeats.map(num).join(", ") : NR}</li>
      <li>Spread: {m.min !== null && m.min !== undefined ? `${num(m.min)} to ${num(m.max)}, ` : ""}noise band ±{num(m.band)} (2 × MAD)
        {m.cv !== null && m.cv !== undefined ? `, CV ${(m.cv * 100).toFixed(1)}%` : ""}</li>
      <li className={sc?.reproducible === false ? "warn" : ""}>Setup check: {sc ? sc.note : "none in this report (the band comes from forks of one setup)"}</li>
      <li>Gap from the paper: <b>{pct(m.gap)}</b>, against a noise band of {band(m.band_rel)} of the paper’s number</li>
    </ul>
  );
}

const KIND: Record<string, string> = { reversal: "Reverse test", held_out: "Held-out number", evidence: "Evidence", effect: "Effect against the noise",
  held_out_separate: "Held-out number, tuned separately", relation: "The paper’s stated relation" };
const checkWord = (x: BeliefT["checks"][number]): [string, string] => (x.kind === "held_out_separate" ? ["Note", "na"]
  : x.ok === true ? ["Pass", "pass"] : x.ok === false ? ["Fail", "fail"] : ["Not checked", "na"]);

function beliefGist(b: BeliefT | null | undefined): string {
  if (!b) return NR;
  if (!b.checks.length) return b.note;
  const n = (f: (x: BeliefT["checks"][number]) => boolean) => b.checks.filter(f).length;
  const pass = n((x) => x.ok === true), fail = n((x) => x.ok === false), na = n((x) => x.ok == null);
  return [pass && `${pass} passed`, fail && `${fail} failed`, na && `${na} not checked`].filter(Boolean).join(", ");
}

function Belief({ b }: { b: BeliefT | null | undefined }) {
  if (!b) return <p className="small">{NR}</p>;
  if (!b.checks.length) return <p>{b.note}</p>;
  return (
    <ul className="checks">
      {b.checks.map((x, i) => {
        const [w, cls] = checkWord(x);
        return <li key={i}><span className={`chk ${cls}`}>{w}</span> {KIND[x.kind] || x.kind}: <WithCode text={x.text} /></li>;
      })}
    </ul>
  );
}

// "Not settable with this harness" mixes setting names and sentences the paper-code contrast wrote; names read as chips,
// sentences as a list
const isName = (s: string) => !/\s/.test(s);

function unknownGist(u: UnknownT | null | undefined): string {
  if (!u) return NR;
  const parts = [u.unmapped.length && plural(u.unmapped.length, "difference the harness can’t set", "differences the harness can’t set"),
    u.leads.length && plural(u.leads.length, "unconfirmed lead", "unconfirmed leads"),
    u.untestable.length && `${u.untestable.length} untestable within the budget`];
  return parts.filter(Boolean).join(", ") || "nothing left open";
}

function Unknown({ u }: { u: UnknownT | null | undefined }) {
  if (!u) return <p className="small">{NR}</p>;
  const leads = [...u.leads].sort((a, b) => (b.units || 0) - (a.units || 0));
  const names = u.unmapped.filter(isName), sentences = u.unmapped.filter((s) => !isName(s));
  return (
    <div className="unknown">
      {sentences.length > 0 && <>
        <p className="sub-head">Differences between the paper and the code it noticed, but couldn’t test</p>
        <ul>{sentences.map((s) => <li key={s}><WithCode text={s} /></li>)}</ul>
      </>}
      {names.length > 0 && <>
        <p className="sub-head">Settings the paper names that this harness can’t change</p>
        <p className="chips-text">{names.map((k) => <code key={k}>{k}</code>)}</p>
      </>}
      {leads.length > 0 && <>
        <p className="sub-head">Unconfirmed leads: they moved the number in the screen but aren’t part of the answer</p>
        <ul>{leads.slice(0, LEADS_SHOWN).map((x) => <li key={`${x.knob}=${x.value}`}><code>{changeText(x.knob, x.value)}</code>: {num(x.units)}× the noise, gap {pct(x.gap)}</li>)}
          {leads.length > LEADS_SHOWN && <li className="small">and {leads.length - LEADS_SHOWN} more in the JSON</li>}</ul>
      </>}
      {u.untestable.length > 0 && <>
        <p className="sub-head">Not testable within the budget</p>
        <p className="chips-text">{u.untestable.map((x) => <code key={`${x.knob}=${x.value}`}>{changeText(x.knob, x.value)}</code>)}</p>
      </>}
      {u.alternatives.length > 0 && <>
        <p className="sub-head">Near alternatives, closest across all claims</p>
        <ul>{u.alternatives.map((a, i) => (
          <li key={i}><code>{knobs(a.changes)}</code>: this claim {pct(a.gap)}, mean |gap| {(a.mean_abs_gap * 100).toFixed(1)}% ({a.runs} runs)</li>
        ))}</ul>
      </>}
      <p className={`small ${u.setup?.reproducible === false ? "warn" : ""}`}>Setup reproducibility: {u.setup ? u.setup.note : "not checked"}.</p>
    </div>
  );
}

const CAUSE_NAME: Record<string, string> = { confirmed_cause: "Confirmed cause", plausible_explanation: "Plausible explanation (fits but unsupported)",
  interacting_factors: "Interacting factors", reporting_rule: "How the paper reports its number", library_drift: "A library release changed the numbers",
  paper_era_code: "The paper-era code gives the numbers" };

function splitSentences(p: string): string[] {
  return p.split(/(?<=[.!?])\s+(?=[A-Z(["'])/).filter(Boolean);
}

// The paper's own setup paragraph with the model-drafted sentence inserted. Drafted text is
// marked by an underline and a tag, not by colour alone.
function MissingSentence({ ms }: { ms: NonNullable<Claim["missing_sentence"]> }) {
  const sents = splitSentences(ms.paragraph);
  const k = Math.max(0, Math.min(ms.insert_after, sents.length));
  return (
    <Q q={`The sentence the paper was missing (p. ${ms.page})`} gist="drafted by GapFinder, for the authors to check" open>
      <p className="small">Setup paragraph from the paper with a sentence drafted by GapFinder (a language model),
        not written by the authors. Check it before use.</p>
      <blockquote>
        {k > 0 && <>{sents.slice(0, k).join(" ")} </>}
        <ins className="drafted"><span className="draft-tag">drafted by GapFinder</span>{ms.sentence}</ins>
        {k < sents.length && <> {sents.slice(k).join(" ")}</>}
      </blockquote>
    </Q>
  );
}

const KIND_TEXT: Record<string, string> = {
  reproduced: "reproduced within noise",
  in_space: "an explanation within the settings is possible",
  out_of_space_suspected: "the cause may be outside the settings",
  out_of_space_likely: "the cause is likely outside the settings",
  insufficient: "not enough measurements",
};

function Diagnosis({ c }: { c: Claim }) {
  const d = c.diagnosis;
  const eq = (c.equivalent || []).filter((e): e is { config: Changes } => Boolean(e && e.config));
  if (!d && eq.length < 2) return null;
  const tid = c.target.claim_id;
  const worst = (r: { I?: Record<string, number> }) => Math.max(...Object.values(r.I || {}));
  const fits = ((d?.per_claim || {})[tid] || []).filter((r) => Object.keys(r.config || {}).length);
  const oos = (d?.kind || "").startsWith("out_of_space");
  const islands = (d?.islands || []).filter((i) => i.length);
  const gist = [eq.length > 1 && `${eq.length} equally good configurations`, d && KIND_TEXT[d.kind]].filter(Boolean).join("; ");
  return (
    <Q q="Could anything else fit as well?" gist={gist}>
      {eq.length > 1 && <>
        <p className="sub-head">Equally good configurations</p>
        <p className="small">This number can’t tell these apart (likelihood within 2 log units, held-out numbers no worse);
          the first is the reported answer.</p>
        <ul>{eq.map((e, i) => <li key={i}><code>{knobs(e.config)}</code>{i === 0 && " (reported)"}</li>)}</ul>
      </>}
      {d && <>
        <p className="sub-head">History matching: {KIND_TEXT[d.kind] || d.kind}</p>
        <p><WithCode text={d.text} /></p>
        {oos && fits.length > 1 && <p className="small">Fit to this number alone (worst claim’s implausibility; lowest is least
          inconsistent): {fits.slice().sort((a, b) => worst(a) - worst(b)).slice(0, 6).map((r, i) =>
            <span key={i}><code>{knobs(r.config)}</code> ({num(worst(r))}) </span>)}</p>}
        {islands.length > 1 && <p className="small">{islands.length} separate islands (no single-setting move joins them)</p>}
        {(d.leads || []).length > 0 && <>
          <p className="sub-head">Leads outside the settings (static code checks; nothing ran unless a patch round tested them)</p>
          <ul>{(d.leads || []).slice(0, 8).map((x, i) => (
            <li key={i}>{x.family.replace(/_/g, " ")}: <WithCode text={x.detail} /> <code>{x.file}:{x.line}</code></li>))}</ul>
        </>}
      </>}
    </Q>
  );
}

const gapLine = (c: Claim) => (c.status === "reproduced" ? `reproduces: ${pct(c.gap_before)} is inside the noise`
  : c.status === "inconclusive" ? `too noisy to tell: ${pct(c.gap_before)} inside a wide band`
  : `${pct(c.gap_before)} → ${pct(c.gap_after)}`);

function Card({ c, open }: { c: Claim; open: boolean }) {
  const label = c.attribution?.confidence_label || "Reproduced";
  const kind = c.cause?.kind;
  return (
    <details className={`card ${kind ? `cause-${kind}` : ""}`} open={open} id={`claim-${c.target.claim_id}`}>
      <summary>
        <span className={`label ${LABEL_CLASS[label] || "muted"}`}>{plain(label)}</span>
        <span className="card-title">{claimName(c.target)}{c.target.held_out && <span className="tag">held out</span>}</span>
        <span className="paperval num">paper {c.target.paper_value} · gap {gapLine(c)}</span>
      </summary>
      <div className="card-body">
        {c.cause && kind && <p className={`cause ${kind}`}><b>{CAUSE_NAME[kind] || "Explanation"}.</b> <WithCode text={c.cause.text.replace(/^[^:]*: /, "").replace(/^./, (m) => m.toUpperCase())} /></p>}
        {c.status === "reproduced" ? (
          <p>Reproduces: the gap as released, {pct(c.gap_before)}, is inside the noise band of {band(c.band)}.</p>
        ) : c.status === "inconclusive" ? (
          <p>Inconclusive: the gap as released, {pct(c.gap_before)}, is inside the noise band of {band(c.band)},
            but the band is too wide to call it a reproduction or to test explanations.</p>
        ) : (
          <p className="gap">The gap went from <b>{pct(c.gap_before)}</b> to <b>{pct(c.gap_after)}</b>, against run-to-run noise of
            {" "}{band(c.band)}, with {plural(c.hypotheses_tested, "hypothesis", "hypotheses")} tested.
            {" "}<span className="small">GapFinder’s label: {label}.</span></p>
        )}
        <Q q="Which experiment changed it?" gist={experimentGist(c.experiment)}><Experiment x={c.experiment} effect={c.effect} /></Q>
        <Q q="Why do we believe it?" gist={beliefGist(c.belief)} open={open && Boolean(c.belief?.checks?.length)}><Belief b={c.belief} /></Q>
        <Q q="What did the paper report?" gist={paperGist(c.paper_claim)}><Paper p={c.paper_claim} /></Q>
        <Q q="What did we measure?" gist={measuredGist(c.measured)}><Measured m={c.measured} /></Q>
        <Q q="What remains unknown?" gist={unknownGist(c.unknown)}><Unknown u={c.unknown} /></Q>
        <Diagnosis c={c} />
        {c.missing_sentence && <MissingSentence ms={c.missing_sentence} />}
        {c.notes && c.notes.length > 0 && <Q q="Notes" gist={plural(c.notes.length, "note from the search", "notes from the search")}>
          <ul>{c.notes.map((n, i) => <li key={i}><WithCode text={n} /></li>)}</ul></Q>}
      </div>
    </details>
  );
}

// every claim on one line: where to start reading a report with many
function AtAGlance({ claims, onOpen }: { claims: Claim[]; onOpen: (id: string) => void }) {
  return (
    <div className="ledger-wrap glance">
      <table>
        <thead><tr><th scope="col">Number</th><th scope="col">Verdict</th><th scope="col">Gap, as released → after</th><th scope="col">Change</th></tr></thead>
        <tbody>
          {claims.map((c) => (
            <tr key={c.target.claim_id} className="link">
              <td className="paper-cell"><a href={`#claim-${c.target.claim_id}`} onClick={(e) => { e.preventDefault(); onOpen(c.target.claim_id); }}>
                {claimName(c.target)}</a>{c.target.held_out && <span className="tag">held out</span>}</td>
              <td><PlainLabel label={c.attribution?.confidence_label} /></td>
              <td className="num nowrap">{gapLine(c)}</td>
              <td>{Object.keys(c.changes || {}).length ? <code>{changesText(c.changes)}</code> : <span className="muted">none</span>}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Closest({ r }: { r: ReportT }) {
  const rows = r.closest_overall || [];
  const ids = r.claims.map((c) => c.target.claim_id).concat(
    Object.keys(rows[0]?.gaps || {}).filter((k) => !r.claims.some((c) => c.target.claim_id === k)));
  const name = (k: string) => claimName(r.claims.find((c) => c.target.claim_id === k)?.target || { claim_id: k });
  return (
    <Q q="Closest configurations across all claims" gist={`${plural(rows.length, "configuration", "configurations")}; not an attribution`}>
      <p className="small">Labels judge one claim at a time. This shows which measured changes move several claims toward the
        paper together.</p>
      <div className="scroll"><table>
        <thead><tr><th scope="col">Configuration</th><th scope="col">Runs</th>{ids.map((k) => <th scope="col" key={k}>{name(k)}</th>)}<th scope="col">Mean |gap|</th></tr></thead>
        <tbody>{rows.map((row, i) => (
          <tr key={i}>
            <td><code>{knobs(row.changes)}</code></td>
            <td>{row.runs}</td>{ids.map((k) => <td key={k}>{pct(row.gaps?.[k])}</td>)}<td>{(row.mean_abs_gap * 100).toFixed(1)}%</td>
          </tr>
        ))}</tbody>
      </table></div>
    </Q>
  );
}

function Provenance({ p }: { p: ProvenanceT | null | undefined }) {
  if (!p) return <Q q="Provenance" gist="not recorded: this report predates it"><p className="small">This report was written before provenance was kept.</p></Q>;
  const g = p.gapfinder || {};
  const c = p.cost;
  return (
    <Q q="Provenance" gist={`GapFinder commit ${g.commit ? g.commit.slice(0, 8) : NR}, models, prompt and harness hashes`}>
      <ul className="provenance">
        <li>GapFinder commit: {g.commit ? <><code>{g.commit}</code>{g.dirty && " (working tree had uncommitted changes)"}</> : `${NR} (no git checkout)`}</li>
        <li>Models: {p.models ? Object.entries(p.models).map(([k, v]) => <span key={k}>{k} <code>{v}</code> </span>) : NR}</li>
        <li>Prompt sha256: {p.prompt_sha256 && Object.keys(p.prompt_sha256).length
          ? Object.entries(p.prompt_sha256).map(([k, v]) => <div key={k}>{k} <code>{v}</code></div>) : NR}</li>
        <li>Harness spec sha256: {p.harness_spec_sha256 ? <code>{p.harness_spec_sha256}</code> : NR}</li>
        <li>Cost: {c ? `Nemotron billed $${c.nemotron_billed_usd.toFixed(4)}, sandbox reported $${c.sandbox_reported_usd.toFixed(4)} (total $${c.total_usd.toFixed(4)}; ${c.scope})` : NR}</li>
      </ul>
    </Q>
  );
}

export default function Report({ run }: { run: Run }) {
  const r = run.report;
  const [opened, setOpened] = useState<Set<string>>(() => new Set());
  if (!r) return <p className="status-line">This run has no report.</p>;
  const head = r.claims.find((c) => !c.target.held_out) || r.claims[0];
  const openCard = (id: string) => {
    setOpened((s) => new Set(s).add(id));
    requestAnimationFrame(() => document.getElementById(`claim-${id}`)?.scrollIntoView({ block: "start", behavior: "smooth" }));
  };
  return (
    <section className="report">
      <div className="report-head">
        <h2>The full Gap Report</h2>
        <p className="small">
          {r.runs} runs of <code>{r.artifact}</code> ({r.setup_runs} builds and loads), written {r.generated}.{" "}
          Download it as <a href={api.reportMdUrl(run.id)}>Markdown</a> or <a href={api.runJsonUrl(run.id)}>JSON</a>.
          {(r.missing_sentence_meta?.drafted || 0) > 0 && <>{" "}<a href={api.issueDraftUrl(run.id)}>Read the drafted issue (not posted)</a>.</>}
        </p>
        {r.partial && <p className="warn">Partial report: the run or dollar budget ran out before every claim was verified.</p>}
        {r.setup_check && <p className={r.setup_check.reproducible === false ? "warn" : "small"}>Setup check: {r.setup_check.note}.</p>}
      </div>
      {r.claims.length > 1 && <AtAGlance claims={r.claims} onOpen={openCard} />}
      {r.claims.map((c) => <Card key={c.target.claim_id} c={c} open={c === head || opened.has(c.target.claim_id)} />)}
      <div className="report-tail">
        {(r.closest_overall?.length || 0) > 0 && <Closest r={r} />}
        {r.triaged_failures && r.triaged_failures.length > 0 && (
          <Q q="Failed hypotheses" gist={`${r.triaged_failures.length} triaged by Nemotron 3 Super`}><ul>
            {r.triaged_failures.map((x, i) => (
              <li key={i}><code>{changeText(x.knob, x.value)}</code>: {x.kind}, {x.why}
                {x.retried ? <> · retried as <code>{x.retried}</code></> : x.suggestion ? <> · suggested <code>{x.suggestion}</code>, already measured</> : null}</li>
            ))}
          </ul></Q>
        )}
        <Provenance p={r.provenance} />
      </div>
    </section>
  );
}
