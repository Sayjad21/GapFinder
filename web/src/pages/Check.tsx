import { useEffect, useId, useMemo, useRef, useState, type ReactNode, type RefObject } from "react";
import { api, type Submitted } from "../api.ts";
import {
  BUDGETS, MAX_PDF_MB, checkRepo, commands, mb, parseArxiv, parseRepo, pdfFacts, readBytes, repoUrl, requestFile,
  type Budget, type CheckRequest, type Named, type PaperFile, type RepoCheck,
} from "../check.ts";
import { href } from "../nav.ts";

// Check a paper of your own: the paper (a PDF, or its arXiv link), its released code (a public GitHub repository), the
// number to explain, and how far to search. The request is made in the browser; a deployment with Sandboxes starts it,
// and this site, which only replays, shows what would run instead.

const BUDGET_WORDS: Record<Budget, string> = {
  60: "A quick look: the noise, then the likeliest settings.",
  120: "The usual depth: settings, repeats, combinations and the checks.",
  200: "The deepest: what the hardest cases on this site took.",
};

// the repository's public metadata, looked up once it has stopped changing; each repository once per visit
const lookups = new Map<string, RepoCheck>();
function useRepoCheck(owner: string | undefined, name: string | undefined): RepoCheck | "checking" | null {
  const key = owner && name ? `${owner}/${name}`.toLowerCase() : null;
  const [got, setGot] = useState<{ key: string; check: RepoCheck } | null>(null);
  useEffect(() => {
    if (!owner || !name) return undefined;
    const k = `${owner}/${name}`.toLowerCase();
    if (lookups.has(k)) return undefined;
    const ctl = new AbortController();
    const t = setTimeout(() => {
      void checkRepo({ owner, name, ref: null }, ctl.signal).then((check) => {
        if (ctl.signal.aborted) return;
        if (check.kind !== "unknown") lookups.set(k, check);
        setGot({ key: k, check });
      });
    }, 450);
    return () => { clearTimeout(t); ctl.abort(); };
  }, [owner, name]);
  if (!key) return null;
  return lookups.get(key) ?? (got && got.key === key ? got.check : "checking");
}

const PageIcon = () => (
  <svg width="34" height="42" viewBox="0 0 34 42" aria-hidden="true" className="page-icon">
    <path d="M3 1.5h19l10.5 10.5v28.5H3z" fill="var(--raised)" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round" />
    <path d="M22 1.5V12h10.5" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round" />
    <path d="M9 21h16M9 26h16M9 31h10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.6" />
  </svg>
);

const Tick = ({ yes }: { yes: boolean }) => (
  <span className={`tickmark ${yes ? "yes" : "no"}`} aria-hidden="true">
    {yes && <svg viewBox="0 0 12 12" width="10" height="10"><path d="M2.5 6.5l2.2 2.2 4.8-5" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" /></svg>}
  </span>
);

function Part({ n, title, hint, done, children }: { n: number; title: string; hint: ReactNode; done: boolean; children: ReactNode }) {
  return (
    <section className={`part${done ? " done" : ""}`} aria-labelledby={`part-${n}`}>
      <span className="part-no" aria-hidden="true">{n}</span>
      <div>
        <div className="part-head"><h2 id={`part-${n}`}>{title}</h2>{done && <span className="part-ready"><Tick yes />Ready</span>}</div>
        <p className="part-hint">{hint}</p>
        {children}
      </div>
    </section>
  );
}

function Msg({ bad, children }: { bad?: boolean; children: ReactNode }) {
  return <p className={`field-msg${bad ? " bad" : ""}`}>{children}</p>;
}

// a labelled input, with its message under it (outside the label, so the message isn't read as the input's name)
function Field({ label, opt, note, children }: { label: string; opt?: string; note?: ReactNode; children: (id: string, noteId: string) => ReactNode }) {
  const id = useId();
  return (
    <div className="form-field">
      <label className="flabel" htmlFor={id}>{label}{opt && <span className="opt"> ({opt})</span>}</label>
      {children(id, `${id}-note`)}
      <div id={`${id}-note`} aria-live="polite">{note}</div>
    </div>
  );
}

// ------------------------------------------------------------------ the paper
// The file input itself covers the zone, unseen: a browser takes a file dropped on a file input as chosen, and a click
// or Enter opens the picker, so dropping, clicking and the keyboard all go through the one control.
function Dropzone({ onFile, reading, inputRef }: { onFile: (f: File) => void; reading: boolean; inputRef: RefObject<HTMLInputElement | null> }) {
  const [over, setOver] = useState(false);
  return (
    <label className={`drop${over ? " over" : ""}`}>
      <PageIcon />
      <span className="drop-main">{reading ? "Reading the PDF…" : <>Drop the paper’s PDF here, or <span className="pick">choose a file</span></>}</span>
      <span className="small">A PDF up to {MAX_PDF_MB} MB. It stays in your browser.</span>
      <input ref={inputRef} type="file" accept="application/pdf,.pdf" className="drop-input"
             onDragEnter={() => setOver(true)} onDragLeave={() => setOver(false)} onDrop={() => setOver(false)}
             onChange={(e) => { const f = e.target.files?.[0]; if (f) onFile(f); e.target.value = ""; }} />
    </label>
  );
}

// ------------------------------------------------------------------ after the request is made
function Sent({ request, reply, at, onEdit }: { request: CheckRequest; reply: Submitted; at: Date; onEdit: () => void }) {
  const script = useMemo(() => commands(request), [request]);
  const [copied, setCopied] = useState<"" | "yes" | "no">("");
  const [saved, setSaved] = useState(false);
  const copy = async () => {
    try { await navigator.clipboard.writeText(script); setCopied("yes"); } catch { setCopied("no"); }
    setTimeout(() => setCopied(""), 2400);
  };
  const save = () => {
    try {
      const url = URL.createObjectURL(new Blob([requestFile(request, at)], { type: "application/json" }));
      const a = document.createElement("a");
      a.href = url; a.download = `gapfinder-request-${request.repo.name.toLowerCase()}.json`;
      document.body.append(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      setSaved(true);
    } catch { setSaved(false); }
  };
  const { paper, named } = request;
  const what = named && (named.metric || named.figure) ? [named.figure, named.metric].filter(Boolean).join(", ") : null;
  const ref = request.commit.trim() || request.repo.ref;
  const plan: [string, string][] = [
    ["Read the paper", `Lists every number ${request.title.trim() ? `“${request.title.trim()}”` : "the paper"} reports, each with its quote, and every setting it states or leaves out.`],
    ["Build the harness", `Builds ${request.repo.owner}/${request.repo.name}${ref ? ` at ${ref}` : ""} in a sandbox and finds the command that prints ${what ? `the number from ${what}` : "the number"}. You read it and approve it before anything is searched.`],
    ["Measure the noise", "Five runs of the code as released give its number, and how much that number moves on its own."],
    ["Search", `Up to ${request.budget} runs, one changed condition at a time, each forked from the same saved checkpoint, then repeats, combinations and the reverse test.`],
    ["Write the Gap Report", "The paper’s number, the code’s, what closed the gap and how sure it is. Or Unexplained, said plainly, when nothing it could change explains it."],
  ];
  return (
    <section className="document receipt" aria-labelledby="sent-title">
      <span className="state-pill">Not started</span>
      <h2 id="sent-title">Your request is ready</h2>
      <p>{reply.ok ? "" : reply.reason} Everything below is made from what you entered: what a full deployment would do, and the
        commands that do it.</p>
      <dl className="facts-list receipt-facts">
        <dt>Paper</dt>
        <dd>{request.title.trim() || paper?.name || `arXiv ${request.arxiv}`}
          {paper && <span className="muted"> · {paper.name}, {mb(paper.size)}{paper.pages ? `, ${paper.pages} pages` : ""}</span>}
          {request.arxiv && <span className="muted"> · arXiv {request.arxiv}</span>}</dd>
        <dt>Code</dt>
        <dd><a href={repoUrl(request.repo)} target="_blank" rel="noreferrer">github.com/{request.repo.owner}/{request.repo.name}</a>
          <span className="muted"> · {ref ? `at ${ref}` : "the latest commit"}</span></dd>
        <dt>Number</dt>
        <dd>{what ? <>{what}{named?.value && <span className="muted"> · the paper reports {named.value}</span>}</> : "Chosen from the paper’s numbers, once it has been read"}</dd>
        <dt>Search</dt>
        <dd>Up to {request.budget} runs</dd>
        <dt>Made</dt>
        <dd>{at.toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" })}</dd>
      </dl>

      <h3 className="minor-head">What happens when it runs</h3>
      <ol className="chapters plan" aria-label="What happens when it runs, step by step">
        {plan.map(([t, d]) => <li key={t}><b>{t}</b><span>{d}</span></li>)}
      </ol>

      <h3 className="minor-head">Run it yourself</h3>
      <p className="small">With GapFinder installed and Sandboxes access set up (see the repository’s README).</p>
      <pre className="script">{script}
        <button type="button" className="copy" onClick={() => void copy()}>{copied === "yes" ? "Copied" : copied === "no" ? "Select to copy" : "Copy"}</button>
      </pre>
      <div className="actions">
        <button type="button" className="btn" onClick={save}>{saved ? "Saved the request" : "Download the request"}</button>
        <button type="button" className="btn quiet" onClick={onEdit}>Change the request</button>
        <a className="btn quiet" href={href("/case/fastgcn-v15")}>Watch a recorded investigation</a>
      </div>
    </section>
  );
}

// ------------------------------------------------------------------ the page
const EMPTY: Named = { figure: "", metric: "", value: "", command: "" };
const NUMBER = /^[-+]?(\d+\.?\d*|\.\d+)(e[-+]?\d+)?\s*%?$/i;

export default function Check() {
  const [paper, setPaper] = useState<PaperFile | null>(null);
  const [paperNote, setPaperNote] = useState<string | null>(null);
  const [reading, setReading] = useState(false);
  const [arxivText, setArxivText] = useState("");
  const [arxivFrom, setArxivFrom] = useState<"" | "name">("");
  const [title, setTitle] = useState("");
  const [titleFrom, setTitleFrom] = useState<"" | "pdf">("");
  const [repoText, setRepoText] = useState("");
  const [commit, setCommit] = useState("");
  const [which, setWhich] = useState<"all" | "named">("all");
  const [named, setNamed] = useState<Named>(EMPTY);
  const [budget, setBudget] = useState<Budget>(120);
  const [touched, setTouched] = useState<Record<string, boolean>>({});
  const [tried, setTried] = useState(false);
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState<{ request: CheckRequest; reply: Submitted; at: Date } | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);
  const arxivRef = useRef<HTMLInputElement>(null);
  const repoRef = useRef<HTMLInputElement>(null);
  const metricRef = useRef<HTMLInputElement>(null);
  const valueRef = useRef<HTMLInputElement>(null);
  // a file dropped beside the zone would otherwise open in the tab, and the form with it would be gone
  useEffect(() => {
    const keep = (e: DragEvent) => { if (!(e.target instanceof HTMLInputElement && e.target.type === "file")) e.preventDefault(); };
    window.addEventListener("dragover", keep);
    window.addEventListener("drop", keep);
    return () => { window.removeEventListener("dragover", keep); window.removeEventListener("drop", keep); };
  }, []);

  const arxiv = parseArxiv(arxivText);
  const arxivBad = arxivText.trim() !== "" && !arxiv;
  const repo = useMemo(() => parseRepo(repoText), [repoText]);
  const repoBad = repoText.trim() !== "" && !repo;
  const looked = useRepoCheck(repo?.owner, repo?.name);
  const facts = looked && looked !== "checking" && looked.kind === "ok" ? looked.facts : null;
  const missing = looked !== null && looked !== "checking" && looked.kind === "missing";
  const valueBad = named.value.trim() !== "" && !NUMBER.test(named.value.trim());

  const paperOk = (paper !== null || arxiv !== null) && !arxivBad;
  const codeOk = repo !== null && !missing;
  const numberOk = which === "all" || (named.metric.trim() !== "" && named.value.trim() !== "" && !valueBad);
  const show = (k: string) => tried || Boolean(touched[k]);
  const blur = (k: string) => () => setTouched((t) => (t[k] ? t : { ...t, [k]: true }));

  const takeFile = async (f: File) => {
    setPaperNote(null);
    if (!/\.pdf$/i.test(f.name) && f.type !== "application/pdf") {
      setPaperNote("That file isn’t a PDF. Choose the paper’s PDF, or give its arXiv link instead.");
      return;
    }
    if (f.size > MAX_PDF_MB * 1024 * 1024) { setPaperNote(`That PDF is ${mb(f.size)}; the limit is ${MAX_PDF_MB} MB.`); return; }
    setReading(true);
    try {
      const got = pdfFacts(await readBytes(f), f.name);
      if (!got.ok) { setPaperNote(got.reason); return; }
      setPaper(got.paper);
      if (got.paper.title && !title.trim()) { setTitle(got.paper.title); setTitleFrom("pdf"); }
      if (got.paper.arxiv && !arxivText.trim()) { setArxivText(got.paper.arxiv); setArxivFrom("name"); }
    } catch {
      setPaperNote("That file couldn’t be read. Try saving the PDF again, or give its arXiv link instead.");
    } finally {
      setReading(false);
    }
  };

  const removePaper = () => {
    setPaper(null);
    if (titleFrom === "pdf") { setTitle(""); setTitleFrom(""); }
    if (arxivFrom === "name") { setArxivText(""); setArxivFrom(""); }
  };

  const example = () => {
    setPaper(null); setPaperNote(null);
    setArxivText("1801.10247"); setArxivFrom("");
    setTitle("FastGCN: Fast Learning with Graph Convolutional Networks via Importance Sampling"); setTitleFrom("");
    setRepoText("https://github.com/matenure/FastGCN"); setCommit("");
    setWhich("named"); setNamed({ figure: "Table 5", metric: "transductive Cora accuracy", value: "0.818", command: "" });
    setBudget(120);
  };

  const start = async () => {
    setTried(true);
    if (!paperOk) { (paper === null && arxivText.trim() === "" ? fileRef : arxivRef).current?.focus(); return; }
    if (!codeOk || !repo) { repoRef.current?.focus(); return; }
    if (!numberOk) { (named.metric.trim() ? valueRef : metricRef).current?.focus(); return; }
    const request: CheckRequest = { paper, arxiv, title, repo, commit, named: which === "named" ? named : null, budget };
    const at = new Date();
    setSending(true);
    let reply: Submitted;
    try { reply = await api.submit(JSON.parse(requestFile(request, at))); } catch { reply = { ok: false, reason: "Nothing was started." }; }
    setSending(false);
    if (reply.ok) { window.location.hash = href(`/run/${reply.run}`).slice(1); return; }
    setSent({ request, reply, at });
    window.scrollTo({ top: 0 });
  };

  const clear = () => {
    setPaper(null); setPaperNote(null); setArxivText(""); setArxivFrom(""); setTitle(""); setTitleFrom("");
    setRepoText(""); setCommit(""); setWhich("all"); setNamed(EMPTY); setBudget(120); setTouched({}); setTried(false);
  };

  const ref = commit.trim() || repo?.ref || null;
  return (
    <div className="shell">
      <section className="hero page-head">
        <h1>Check a paper</h1>
        <p className="lede">Give GapFinder a paper and the code released with it. It runs the code, finds the number the paper
          reports, and looks for why the two disagree.</p>
      </section>

      {sent ? <Sent {...sent} onEdit={() => setSent(null)} /> : (
        <div className="check-grid">
          <form className="check-form" noValidate onSubmit={(e) => { e.preventDefault(); void start(); }} aria-label="A new investigation">
            <Part n={1} title="The paper" done={paperOk} hint="The PDF, or its arXiv link. GapFinder reads every number it reports and every setting it states.">
              {paper ? (
                <div className="filecard">
                  <PageIcon />
                  <div className="filecard-text">
                    <span className="name">{paper.name}</span>
                    <span className="meta">{[paper.pages ? `${paper.pages} pages` : null, mb(paper.size), "PDF"].filter(Boolean).join(" · ")}</span>
                  </div>
                  <div className="filecard-acts">
                    <button type="button" className="btn quiet" onClick={() => fileRef.current?.click()}>Replace</button>
                    <button type="button" className="btn quiet" onClick={removePaper}>Remove</button>
                  </div>
                  <input ref={fileRef} type="file" accept="application/pdf,.pdf" className="visually-hidden" tabIndex={-1} aria-hidden="true"
                         onChange={(e) => { const f = e.target.files?.[0]; if (f) void takeFile(f); e.target.value = ""; }} />
                </div>
              ) : <Dropzone onFile={(f) => void takeFile(f)} reading={reading} inputRef={fileRef} />}
              {paperNote && <Msg bad>{paperNote}</Msg>}
              <div className="row-2">
                <Field label={paper ? "arXiv ID" : "Or its arXiv ID or link"} opt={paper ? "optional: its LaTeX source helps" : undefined}
                       note={arxivBad && show("arxiv") ? <Msg bad>That isn’t an arXiv ID. They look like 1801.10247.</Msg>
                         : !paper && !arxiv && tried ? <Msg bad>Add the paper’s PDF or its arXiv link.</Msg>
                         : arxivFrom === "name" ? <Msg>Read from the file name.</Msg> : null}>
                  {(id, note) => (
                    <input id={id} ref={arxivRef} className="input" value={arxivText} placeholder="1801.10247"
                           aria-invalid={show("arxiv") && (arxivBad || (!paper && !arxiv))} aria-describedby={note} spellCheck={false}
                           onChange={(e) => { setArxivText(e.target.value); setArxivFrom(""); }} onBlur={blur("arxiv")} />
                  )}
                </Field>
                <Field label="Title" opt="optional" note={titleFrom === "pdf" ? <Msg>Read from the PDF.</Msg> : null}>
                  {(id, note) => (
                    <input id={id} className="input" value={title} placeholder="Names the report" aria-describedby={note}
                           onChange={(e) => { setTitle(e.target.value); setTitleFrom(""); }} />
                  )}
                </Field>
              </div>
            </Part>

            <Part n={2} title="The code" done={codeOk && looked !== "checking"} hint="The public GitHub repository the paper released. It is built as it is, at the commit you name.">
              <Field label="Repository" note={<>
                {repoBad && show("repo") ? <Msg bad>That isn’t a GitHub repository link. It looks like github.com/owner/name.</Msg>
                  : !repo && tried ? <Msg bad>Add the repository the paper released.</Msg>
                  : looked === "checking" ? <Msg>Looking it up on GitHub…</Msg>
                  : missing && repo ? <Msg bad>GitHub has no public repository at {repo.owner}/{repo.name}. GapFinder checks public code only.</Msg>
                  : looked?.kind === "unknown" ? <Msg>GitHub couldn’t be reached to look it up; you can still go on.</Msg>
                  : null}</>}>
                {(id, note) => (
                  <input id={id} ref={repoRef} className="input" value={repoText} placeholder="https://github.com/owner/repository" spellCheck={false}
                         inputMode="url" autoComplete="url" aria-invalid={show("repo") && (repoBad || missing || !repo)} aria-describedby={note}
                         onChange={(e) => setRepoText(e.target.value)} onBlur={blur("repo")} />
                )}
              </Field>
              {facts && repo && (
                  <div className="repocard">
                    <span className="rname">{repo.owner}/{repo.name}</span>
                    {facts.description && <p className="rdesc">{facts.description}</p>}
                    <span className="rmeta">
                      {facts.language && <span>{facts.language}</span>}
                      <span>{facts.stars.toLocaleString()} {facts.stars === 1 ? "star" : "stars"}</span>
                      {facts.pushed && <span>last changed {new Date(facts.pushed).toLocaleDateString(undefined, { year: "numeric", month: "short" })}</span>}
                      {facts.license && <span>{facts.license}</span>}
                      <span>{mb(facts.sizeKb * 1024)}</span>
                      {facts.archived && <span>archived, as released</span>}
                    </span>
                  </div>
                )}
              <Field label="Commit, tag or branch" opt="optional">
                {(id) => (
                  <input id={id} className="input mono" value={commit} spellCheck={false} onChange={(e) => setCommit(e.target.value)}
                         placeholder={repo?.ref ? `${repo.ref}, from the link` : `the latest commit on ${facts?.defaultBranch ?? "the default branch"}`} />
                )}
              </Field>
            </Part>

            <Part n={3} title="The number" done={numberOk && (which === "all" || named.metric.trim() !== "")}
                  hint="Which reported number to explain. GapFinder checks the paper’s other numbers too, so a change that fixes one and breaks another is caught.">
              <span className="toggle" role="group" aria-label="Which number">
                <button type="button" aria-pressed={which === "all"} onClick={() => setWhich("all")}>Pick from the paper’s numbers</button>
                <button type="button" aria-pressed={which === "named"} onClick={() => setWhich("named")}>Name one now</button>
              </span>
              {which === "all" ? (
                <p className="field-msg spaced-s">Once it has read the paper, GapFinder lists every number it reports, each with its quote and
                  where it is printed, and you choose the one to explain.</p>
              ) : (
                <>
                  <div className="row-2">
                    <Field label="What it measures" note={show("metric") && !named.metric.trim() ? <Msg bad>Say what the number measures.</Msg> : null}>
                      {(id, note) => (
                        <input id={id} ref={metricRef} className="input" value={named.metric} placeholder="test accuracy on Cora"
                               aria-invalid={show("metric") && !named.metric.trim()} aria-describedby={note} onBlur={blur("metric")}
                               onChange={(e) => setNamed({ ...named, metric: e.target.value })} />
                      )}
                    </Field>
                    <Field label="The paper’s value"
                           note={show("value") && valueBad ? <Msg bad>A number, as the paper prints it: 81.5, 0.818 or 12%.</Msg>
                             : show("value") && !named.value.trim() ? <Msg bad>Give the value the paper reports.</Msg> : null}>
                      {(id, note) => (
                        <input id={id} ref={valueRef} className="input num" value={named.value} placeholder="81.5" inputMode="decimal"
                               aria-invalid={show("value") && (valueBad || !named.value.trim())} aria-describedby={note} onBlur={blur("value")}
                               onChange={(e) => setNamed({ ...named, value: e.target.value })} />
                      )}
                    </Field>
                  </div>
                  <div className="row-2">
                    <Field label="Where it is printed" opt="optional">
                      {(id) => <input id={id} className="input" value={named.figure} placeholder="Table 2"
                                      onChange={(e) => setNamed({ ...named, figure: e.target.value })} />}
                    </Field>
                    <Field label="The command that produces it" opt="optional">
                      {(id) => <input id={id} className="input mono" value={named.command} placeholder="python train.py --dataset cora" spellCheck={false}
                                      onChange={(e) => setNamed({ ...named, command: e.target.value })} />}
                    </Field>
                  </div>
                </>
              )}
            </Part>

            <Part n={4} title="How far to search" done hint="The most runs it may make. It stops sooner when the answer is clear, and says Unexplained when nothing fits.">
              <span className="toggle" role="group" aria-label="How far to search">
                {BUDGETS.map((b) => <button key={b} type="button" aria-pressed={b === budget} onClick={() => setBudget(b)}>{b} runs</button>)}
              </span>
              <p className="field-msg spaced-s">{BUDGET_WORDS[budget]}</p>
            </Part>

            <div className="ready">
              <h2 className="visually-hidden">Ready to start</h2>
              <ul aria-label="What the request has">
                <li><Tick yes={paperOk} /><b>Paper</b><span>{paper ? (title.trim() || paper.name) : arxiv ? (title.trim() || `arXiv ${arxiv}`) : "Not yet"}</span></li>
                <li><Tick yes={codeOk && repo !== null} /><b>Code</b><span>{repo ? `${repo.owner}/${repo.name}${ref ? ` at ${ref}` : ""}` : "Not yet"}</span></li>
                <li><Tick yes={numberOk} /><b>Number</b><span>{which === "all" ? "Chosen once the paper is read" : named.metric.trim() ? `${named.metric.trim()}${named.value.trim() ? `, ${named.value.trim()}` : ""}` : "Not yet"}</span></li>
                <li><Tick yes /><b>Search</b><span>Up to {budget} runs</span></li>
              </ul>
              {tried && !(paperOk && codeOk && numberOk) && (
                <p className="field-msg bad missing" role="status">
                  Still needed: {[!paperOk && "the paper", !codeOk && "the code", !numberOk && "the number"].filter(Boolean).join(", ")}.
                </p>
              )}
              <div className="actions">
                <button type="submit" className="btn big" disabled={sending || reading}>{sending ? "Making the request…" : "Start the investigation"}</button>
                <button type="button" className="btn quiet" onClick={example}>Fill in an example</button>
                <button type="button" className="btn quiet" onClick={clear}>Clear</button>
              </div>
            </div>
          </form>

          <aside className="check-aside" aria-label="Before you start">
            <div className="aside-block">
              <h2>What fits</h2>
              <ul>
                <li>Code that trains and evaluates from the command line, in Python.</li>
                <li>A run that fits a sandbox: 4 CPUs and 3.9 GB of memory. Experiments over an hour run in pieces.</li>
                <li>A number the paper prints in its text or a table.</li>
              </ul>
            </div>
            <div className="aside-block">
              <h2>What you get</h2>
              <p>A Gap Report: the paper’s number, the code’s, what closed the gap and how sure it is, with every run behind it.
                <a href={href("/case/sdcn")}> See one</a>.</p>
            </div>
            <div className="aside-block notice">
              <p>This public site replays recorded investigations, so here the request is made but not started. Your files stay in
                your browser; only the repository’s name goes to GitHub, to look it up.</p>
            </div>
          </aside>
        </div>
      )}
    </div>
  );
}
