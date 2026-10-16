import { useState } from "react";
import { api, pct, LABEL_CLASS } from "./api.js";

const NR = "not recorded";
const num = (x) => (x === null || x === undefined ? NR : String(Number(Number(x).toPrecision(4))));
const signed = (x) => (x === null || x === undefined ? NR : `${x >= 0 ? "+" : ""}${Number(Number(x).toPrecision(4))}`);
const knobs = (d) => Object.entries(d || {}).map(([k, v]) => `${k}=${v}`).join(", ") || "naive";
const LEADS_SHOWN = 5;

function Copy({ text }) {
  const [done, setDone] = useState(false);
  return (
    <button className="copy" onClick={() => { navigator.clipboard?.writeText(text); setDone(true); setTimeout(() => setDone(false), 1200); }}>
      {done ? "copied" : "copy"}
    </button>
  );
}

function Q({ q, children }) {
  return <div className="sub q"><h5>{q}</h5>{children}</div>;
}

function Effect({ e }) {
  const ci = e.ci;
  return (
    <p className="effect">
      Effect: candidate <b>{num(e.candidate)}</b> minus naive <b>{num(e.naive)}</b> = <b>{signed(e.diff)}</b>
      {ci ? <>, {Math.round((1 - e.alpha) * 100)}% bootstrap interval [{signed(ci[0])}, {signed(ci[1])}]
        {e.excludes_zero === false && <b className="warn"> (includes 0)</b>}</> : <>, bootstrap interval {NR}</>}
      {" "}({e.n_candidate ?? NR} candidate runs vs {e.n_naive ?? NR} naive runs)
    </p>
  );
}

function Experiment({ x, effect }) {
  if (!x) return <p className="small">{NR}</p>;
  if (!x.found) return <p>None: {x.note}.</p>;
  const cmd = x.command ? `${Object.entries(x.env || {}).map(([k, v]) => `${k}=${v}`).join(" ")} ${x.command}`.trim() : null;
  const vals = (x.branches || []).map((b) => b.value).filter((v) => v !== null && v !== undefined);
  return (
    <>
      <p>
        Branch: {x.branches?.length
          ? x.branches.map((b) => <code key={b.id}>{b.id}</code>)
          : <span className="small">id {NR}{x.repeats ? ` (${x.repeats} runs)` : ""}</span>}
      </p>
      <div className="scroll"><table className="cfg">
        <thead><tr><th>Config</th><th>Naive</th><th>Changed to</th></tr></thead>
        <tbody>{x.config.map((k) => (
          <tr key={k.knob}><td><code>{k.knob}</code></td><td>{k.naive === null || k.naive === undefined ? NR : <code>{k.naive}</code>}</td><td><code>{k.candidate}</code></td></tr>
        ))}</tbody>
      </table></div>
      {cmd ? (
        <>
          <p className="small">Command: fork checkpoint <code>{x.parent_checkpoint}</code> and run</p>
          <pre>{cmd}<Copy text={cmd} /></pre>
        </>
      ) : <p className="small">Command: {NR}</p>}
      <p>Output: <code>{x.metric}</code> {vals.length ? vals.map(num).join(", ") : `values ${NR}`}
        {" "}· gap after <b>{pct(x.gap_after)}</b>
        {x.result_checkpoint && <> · result checkpoint <code>{x.result_checkpoint}</code></>}</p>
      {effect && <Effect e={effect} />}
    </>
  );
}

function Paper({ p }) {
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

function Measured({ m }) {
  if (!m) return <p className="small">{NR}</p>;
  const sc = m.setup_check;
  return (
    <ul>
      <li>Naive median <b>{num(m.median)}</b> over {m.n ?? NR} runs; repeats: {m.repeats?.length ? m.repeats.map(num).join(", ") : NR}</li>
      <li>Spread: {m.min !== null && m.min !== undefined ? `range ${num(m.min)} to ${num(m.max)}, ` : ""}noise band ±{num(m.band)} (2 x MAD)
        {m.cv !== null && m.cv !== undefined ? `, CV ${(m.cv * 100).toFixed(1)}%` : ""}</li>
      <li className={sc?.reproducible === false ? "warn" : ""}>Setup check: {sc ? sc.note : "none in this report (the band comes from forks of one setup)"}</li>
      <li>Discrepancy from the paper: <b>{pct(m.gap)}</b> (noise band ±{(m.band_rel * 100).toFixed(1)}% of the paper value)</li>
    </ul>
  );
}

const KIND = { reversal: "Counterfactual (reversal test)", held_out: "Held-out claim", evidence: "Evidence", effect: "Effect vs noise", held_out_separate: "Held-out claim, tuned separately" };

function Belief({ b }) {
  if (!b) return <p className="small">{NR}</p>;
  if (!b.checks.length) return <p>{b.note}</p>;
  return (
    <ul className="checks">
      {b.checks.map((x, i) => (
        <li key={i}>
          <span className={`chk ${x.ok === true ? "pass" : x.ok === false ? "fail" : "na"}`}>{x.kind === "held_out_separate" ? "NOTE" : x.ok === true ? "PASS" : x.ok === false ? "FAIL" : "NOT CHECKED"}</span>
          {" "}{KIND[x.kind] || x.kind}: {x.text.replace(/`/g, "")}
        </li>
      ))}
    </ul>
  );
}

function Unknown({ u }) {
  if (!u) return <p className="small">{NR}</p>;
  const leads = [...u.leads].sort((a, b) => (b.units || 0) - (a.units || 0));
  return (
    <ul>
      <li>Untestable within the budget: {u.untestable.length ? u.untestable.map((x) => <code key={`${x.knob}=${x.value}`}>{x.knob}={x.value}</code>) : "none"}</li>
      <li>Not settable with this harness: {u.unmapped.length ? u.unmapped.map((k) => <code key={k}>{k}</code>) : "none"}</li>
      <li className={u.setup?.reproducible === false ? "warn" : ""}>Setup reproducibility: {u.setup ? u.setup.note : "not checked"}</li>
      <li>Unconfirmed leads (moved the gap in the screen, not part of the explanation): {leads.length
        ? <>{leads.slice(0, LEADS_SHOWN).map((x) => <span key={`${x.knob}=${x.value}`}><code>{x.knob}={x.value}</code> ({num(x.units)} noise units, gap {pct(x.gap)}) </span>)}
          {leads.length > LEADS_SHOWN && <span className="small">and {leads.length - LEADS_SHOWN} more in the JSON</span>}</>
        : "none"}</li>
      <li>Near alternatives (closest across all claims): {u.alternatives.length ? (
        <ul>{u.alternatives.map((a, i) => (
          <li key={i}><code>{knobs(a.changes)}</code>: this claim {pct(a.gap)}, mean |gap| {(a.mean_abs_gap * 100).toFixed(1)}% ({a.runs} runs)</li>
        ))}</ul>
      ) : "none recorded"}</li>
    </ul>
  );
}

const CAUSE_NAME = { confirmed_cause: "Confirmed cause", plausible_explanation: "Plausible explanation (fits but unsupported)", interacting_factors: "Interacting factors" };

function splitSentences(p) {
  return p.split(/(?<=[.!?])\s+(?=[A-Z(["'])/).filter(Boolean);
}

// The paper's own setup paragraph with the model-drafted sentence inserted. Drafted text is
// marked by an underline and a tag, not by colour alone.
function MissingSentence({ ms }) {
  const sents = splitSentences(ms.paragraph);
  const k = Math.max(0, Math.min(ms.insert_after, sents.length));
  return (
    <div className="sub missing-sentence">
      <h5>The sentence the paper was missing (p.{ms.page})</h5>
      <p className="small">Setup paragraph from the paper with a sentence drafted by GapFinder (a language model),
        not written by the authors. Check it before use.</p>
      <blockquote>
        {k > 0 && <>{sents.slice(0, k).join(" ")} </>}
        <ins className="drafted"><span className="draft-tag">drafted by GapFinder</span>{ms.sentence}</ins>
        {k < sents.length && <> {sents.slice(k).join(" ")}</>}
      </blockquote>
    </div>
  );
}

const KIND_TEXT = {
  reproduced: "reproduced within noise",
  in_space: "an explanation within the settings is possible",
  out_of_space_suspected: "out of space suspected",
  out_of_space_likely: "out of space likely",
  insufficient: "not enough measurements",
};

function Diagnosis({ c }) {
  const d = c.diagnosis;
  const eq = (c.equivalent || []).filter((e) => e && e.config);
  if (!d && eq.length < 2) return null;
  const tid = c.target.claim_id;
  const worst = (r) => Math.max(...Object.values(r.I || {}));
  const fits = ((d?.per_claim || {})[tid] || []).filter((r) => Object.keys(r.config || {}).length);
  const oos = (d?.kind || "").startsWith("out_of_space");
  const islands = (d?.islands || []).filter((i) => i.length);
  return (
    <div className="sub diagnosis">
      {eq.length > 1 && <>
        <h5>Equally good configurations</h5>
        <p className="small">The target claim can't tell these apart (likelihood within 2 log units, held-out claims no worse);
          the first is the reported answer.</p>
        <ul>{eq.map((e, i) => <li key={i}><code>{knobs(e.config)}</code>{i === 0 && " (reported)"}</li>)}</ul>
      </>}
      {d && <>
        <h5>History matching: {KIND_TEXT[d.kind] || d.kind}</h5>
        <p>{d.text}</p>
        {oos && fits.length > 1 && <p className="small">Fit {tid} alone (worst claim's implausibility; lowest is least
          inconsistent): {fits.slice().sort((a, b) => worst(a) - worst(b)).slice(0, 6).map((r, i) =>
            <span key={i}><code>{knobs(r.config)}</code> ({num(worst(r))}) </span>)}</p>}
        {islands.length > 1 && <p className="small">{islands.length} separate islands (no single-knob move joins them)</p>}
        {(d.leads || []).length > 0 && <>
          <p><b>Leads outside the settings</b> (static code checks, nothing run unless a patch round tested them):</p>
          <ul>{d.leads.slice(0, 8).map((x, i) => (
            <li key={i}>{x.family.replace(/_/g, " ")}: {x.detail} <code>{x.file}:{x.line}</code></li>))}</ul>
        </>}
      </>}
    </div>
  );
}

function Card({ c }) {
  const a = c.attribution;
  const label = a?.confidence_label || "Reproduced";
  const kind = c.cause?.kind;
  return (
    <article className={`card ${kind ? `cause-${kind}` : ""}`}>
      <header>
        <span className={`label ${LABEL_CLASS[label] || "muted"}`}>{label}</span>
        <h4>{c.target.claim_id} · {c.target.metric}</h4>
        <span className="paperval">paper {c.target.paper_value}</span>
      </header>
      {kind && <p className={`cause ${kind}`}><b>{CAUSE_NAME[kind]}.</b> {c.cause.text.replace(/^[^:]*: /, "")}</p>}
      {c.status === "reproduced" ? (
        <p>Reproduces: the naive gap {pct(c.gap_before)} is inside the noise band ±{(c.band * 100).toFixed(1)}%.</p>
      ) : c.status === "inconclusive" ? (
        <p>Inconclusive: the naive gap {pct(c.gap_before)} is inside the noise band ±{(c.band * 100).toFixed(1)}%,
          but the band is too wide to call it a reproduction or to test explanations.</p>
      ) : (
        <p className="gap">gap <b>{pct(c.gap_before)}</b> → <b>{pct(c.gap_after)}</b> · noise ±{(c.band * 100).toFixed(1)}% · {c.hypotheses_tested} hypotheses tested</p>
      )}
      <Q q="Which experiment changed it?"><Experiment x={c.experiment} effect={c.effect} /></Q>
      <Q q="What did the paper report?"><Paper p={c.paper_claim} /></Q>
      <Q q="What did we measure?"><Measured m={c.measured} /></Q>
      <Q q="Why do we believe it?"><Belief b={c.belief} /></Q>
      <Q q="What remains unknown?"><Unknown u={c.unknown} /></Q>
      <Diagnosis c={c} />
      {c.missing_sentence && <MissingSentence ms={c.missing_sentence} />}
      {c.notes?.length > 0 && <div className="sub"><h5>Notes</h5><ul>{c.notes.map((n, i) => <li key={i}>{n}</li>)}</ul></div>}
    </article>
  );
}

function Closest({ r }) {
  const ids = r.claims.map((c) => c.target.claim_id).concat(
    Object.keys(r.closest_overall[0].gaps || {}).filter((k) => !r.claims.some((c) => c.target.claim_id === k)));
  return (
    <div className="sub closest">
      <h5>Closest configurations across all claims</h5>
      <p className="small">Not an attribution: labels judge one claim at a time. This shows which measured changes move
        several claims toward the paper together.</p>
      <div className="scroll"><table>
        <thead><tr><th>Configuration</th><th>Runs</th>{ids.map((k) => <th key={k}>{k}</th>)}<th>Mean |gap|</th></tr></thead>
        <tbody>{r.closest_overall.map((row, i) => (
          <tr key={i}>
            <td><code>{Object.entries(row.changes || {}).map(([k, v]) => `${k}=${v}`).join(", ") || "naive"}</code></td>
            <td>{row.runs}</td>{ids.map((k) => <td key={k}>{pct(row.gaps?.[k])}</td>)}<td>{(row.mean_abs_gap * 100).toFixed(1)}%</td>
          </tr>
        ))}</tbody>
      </table></div>
    </div>
  );
}

function Provenance({ p }) {
  if (!p) return <div className="sub provenance"><h5>Provenance</h5><p className="small">Not recorded: this report was written before provenance was kept.</p></div>;
  const g = p.gapfinder || {};
  const c = p.cost;
  return (
    <div className="sub provenance">
      <h5>Provenance</h5>
      <ul>
        <li>GapFinder commit: {g.commit ? <><code>{g.commit}</code>{g.dirty && " (working tree had uncommitted changes)"}</> : `${NR} (no git checkout)`}</li>
        <li>Models: {p.models ? Object.entries(p.models).map(([k, v]) => <span key={k}>{k} <code>{v}</code> </span>) : NR}</li>
        <li>Prompt sha256: {p.prompt_sha256 && Object.keys(p.prompt_sha256).length
          ? Object.entries(p.prompt_sha256).map(([k, v]) => <div key={k}>{k} <code>{v}</code></div>) : NR}</li>
        <li>Harness spec sha256: {p.harness_spec_sha256 ? <code>{p.harness_spec_sha256}</code> : NR}</li>
        <li>Cost: {c ? `Nemotron billed $${c.nemotron_billed_usd.toFixed(4)}, sandbox reported $${c.sandbox_reported_usd.toFixed(4)} (total $${c.total_usd.toFixed(4)}; ${c.scope})` : NR}</li>
      </ul>
    </div>
  );
}

export default function Report({ run }) {
  const r = run?.report;
  if (!r) return <p>Loading…</p>;
  return (
    <section>
      <div className="report-head">
        <h2>Gap Report: {r.paper}</h2>
        <p className="small">
          Artifact <code>{r.artifact}</code> · {r.runs} branch runs ({r.setup_runs} build/load setups) · generated {r.generated}
          {" · "}<a href={api.reportMdUrl(run.id)}>Markdown</a> · <a href={api.runJsonUrl(run.id)}>JSON</a>
          {r.missing_sentence_meta?.drafted > 0 && <>{" · "}<a href={api.issueDraftUrl(run.id)}>Issue draft (not posted)</a></>}
        </p>
        {r.partial && <p className="warn">Partial report: the run or dollar budget ran out before every claim was verified.</p>}
        {r.setup_check && <p className={r.setup_check.reproducible === false ? "warn" : "small"}>Setup check: {r.setup_check.note}.</p>}
      </div>
      {r.claims.map((c) => <Card key={c.target.claim_id} c={c} />)}
      {r.closest_overall?.length > 0 && <Closest r={r} />}
      {r.triaged_failures?.length > 0 && (
        <div className="sub"><h5>Failed hypotheses (triaged by Nemotron 3 Super)</h5><ul>
          {r.triaged_failures.map((x, i) => (
            <li key={i}><code>{x.knob}={x.value}</code>: {x.kind}, {x.why}
              {x.retried ? <> · retried as <code>{x.retried}</code></> : x.suggestion ? <> · suggested <code>{x.suggestion}</code>, already measured</> : null}</li>
          ))}
        </ul></div>
      )}
      {r.untestable?.length > 0 && (
        <p className="small">Not testable within the budget: {r.untestable.map(({ knob, value }) => <code key={`${knob}=${value}`}>{knob}={value}</code>)}</p>
      )}
      {r.unmapped_assumptions?.length > 0 && (
        <p className="small">Not testable with this harness: {r.unmapped_assumptions.map((k) => <code key={k}>{k}</code>)}</p>
      )}
      <Provenance p={r.provenance} />
    </section>
  );
}
