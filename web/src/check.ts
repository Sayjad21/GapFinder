// Checking a paper of your own: what the page reads from the PDF and the links it's given, and the request it makes of
// them. The files never leave the browser; the only call out is GitHub's public API, for the repository's metadata.

export const MAX_PDF_MB = 40;
export const BUDGETS = [60, 120, 200] as const;
export type Budget = (typeof BUDGETS)[number];

export interface PaperFile { name: string; size: number; pages: number | null; title: string | null; arxiv: string | null }
export interface Repo { owner: string; name: string; ref: string | null }
export interface RepoFacts {
  description: string | null; language: string | null; stars: number; pushed: string | null; sizeKb: number;
  license: string | null; archived: boolean; defaultBranch: string;
}
export type RepoCheck = { kind: "ok"; facts: RepoFacts } | { kind: "missing" } | { kind: "unknown" };
export interface Named { figure: string; metric: string; value: string; command: string }
export interface CheckRequest {
  paper: PaperFile | null; arxiv: string | null; title: string; repo: Repo; commit: string; named: Named | null; budget: Budget;
}

// ------------------------------------------------------------------ links
const YYMM = String.raw`\d{2}(?:0[1-9]|1[0-2])\.\d{4,5}`;
const ARXIV_NEW = new RegExp(String.raw`^(${YYMM})(v\d+)?$`);
const ARXIV_OLD = /^([a-z-]+(?:\.[A-Z]{2})?\/\d{7})(v\d+)?$/;

// an arXiv id from an id, "arXiv:..." or an abs/pdf link; null when it isn't one
export function parseArxiv(s: string): string | null {
  const t = s.trim().replace(/^arxiv:\s*/i, "").replace(/^https?:\/\/(www\.)?(export\.)?arxiv\.org\/(abs|pdf|html)\//i, "")
    .replace(/\.pdf$/i, "").replace(/\/$/, "");
  const m = ARXIV_NEW.exec(t) || ARXIV_OLD.exec(t);
  return m ? m[1] + (m[2] || "") : null;
}

// a GitHub repository from a URL (https, git@, with /tree/<ref>) or owner/name; null when it isn't one
export function parseRepo(s: string): Repo | null {
  const t = s.trim().replace(/\/+$/, "");
  const m = /^(?:(?:https?:\/\/)?(?:www\.)?github\.com\/|git@github\.com:)([\w.-]+)\/([\w.-]+?)(?:\.git)?(?:\/(?:tree|commit|releases\/tag)\/([^\s?#/]+)[^\s?#]*|\/[^\s?#]*)?(?:[?#].*)?$/i.exec(t)
    || /^([\w.-]+)\/([\w.-]+?)(?:\.git)?$/.exec(t);
  if (!m || m[1] === "." || m[2] === "." || m[1] === ".." || m[2] === "..") return null;
  return { owner: m[1], name: m[2], ref: m[3] ? decodeURIComponent(m[3]) : null };
}

export const repoUrl = (r: Repo) => `https://github.com/${r.owner}/${r.name}`;

// The repository's public metadata. Never throws: a missing repository and an unreachable API are answers too.
export async function checkRepo(r: Repo, signal?: AbortSignal): Promise<RepoCheck> {
  try {
    const res = await fetch(`https://api.github.com/repos/${encodeURIComponent(r.owner)}/${encodeURIComponent(r.name)}`,
      { headers: { Accept: "application/vnd.github+json" }, signal });
    if (res.status === 404) return { kind: "missing" };
    if (!res.ok) return { kind: "unknown" };
    const j = await res.json() as Record<string, unknown>;
    if (j.private === true) return { kind: "missing" };
    const lic = j.license as { spdx_id?: string; name?: string } | null;
    return { kind: "ok", facts: {
      description: typeof j.description === "string" ? j.description : null,
      language: typeof j.language === "string" ? j.language : null,
      stars: Number(j.stargazers_count) || 0,
      pushed: typeof j.pushed_at === "string" ? j.pushed_at : null,
      sizeKb: Number(j.size) || 0,
      license: lic ? (lic.spdx_id && lic.spdx_id !== "NOASSERTION" ? lic.spdx_id : lic.name || null) : null,
      archived: j.archived === true,
      defaultBranch: typeof j.default_branch === "string" ? j.default_branch : "main",
    } };
  } catch {
    return { kind: "unknown" };
  }
}

// ------------------------------------------------------------------ the PDF
export function readBytes(file: Blob): Promise<Uint8Array> {
  return new Promise((resolve, reject) => {
    const fr = new FileReader();
    fr.addEventListener("load", () => resolve(new Uint8Array(fr.result as ArrayBuffer)));
    fr.addEventListener("error", () => reject(fr.error ?? new Error("unreadable")));
    fr.readAsArrayBuffer(file);
  });
}

// one character per byte (TextDecoder's "latin1" is really windows-1252, which moves 0x80 to 0x9F)
function latin1(b: Uint8Array): string {
  let s = "";
  for (let i = 0; i < b.length; i += 0x8000) s += String.fromCharCode(...b.subarray(i, i + 0x8000));
  return s;
}
const xml = (s: string) => s.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, "\"").replace(/&apos;/g, "'")
  .replace(/&#(\d+);/g, (_, n: string) => String.fromCodePoint(Number(n))).replace(/&amp;/g, "&");

// a PDF literal string's escapes; a UTF-16 string (it starts with þÿ) decoded
function pdfString(raw: string): string {
  const s = raw.replace(/\\([nrtbf()\\]|[0-7]{1,3}|\r?\n)/g, (_, e: string) =>
    /^[0-7]/.test(e) ? String.fromCharCode(parseInt(e, 8)) : e[0] === "\r" || e[0] === "\n" ? ""
      : ({ n: "\n", r: "\r", t: "\t", b: "\b", f: "\f" } as Record<string, string>)[e] ?? e);
  return s.startsWith("þÿ") ? utf16(Uint8Array.from(s.slice(2), (c) => c.charCodeAt(0) & 255)) : s;
}
const utf16 = (b: Uint8Array) => new TextDecoder("utf-16be").decode(b);

const NOT_A_TITLE = /^(untitled|microsoft word|title|paper|main|arxiv|\S+\.(docx?|tex|dvi|pdf|ps))\b/i;

function titleOf(text: string): string | null {
  const found: string[] = [];
  const x = /<dc:title>[\s\S]*?<rdf:li[^>]*>([\s\S]*?)<\/rdf:li>/.exec(text);
  if (x) found.push(xml(x[1]));
  const lit = /\/Title\s*\(((?:\\[\s\S]|[^\\)])*)\)/.exec(text);
  if (lit) found.push(pdfString(lit[1]));
  const hex = /\/Title\s*<([0-9A-Fa-f\s]+)>/.exec(text);
  if (hex) {
    const h = hex[1].replace(/\s/g, "");
    const b = Uint8Array.from(h.match(/../g) || [], (p) => parseInt(p, 16));
    found.push(b[0] === 0xfe && b[1] === 0xff ? utf16(b.slice(2)) : latin1(b));
  }
  for (const f of found) {
    const t = f.replace(/\s+/g, " ").trim();
    if (t.length >= 6 && t.length <= 300 && !NOT_A_TITLE.test(t)) return t;
  }
  return null;
}

function pagesOf(text: string): number | null {
  const leaves = text.match(/\/Type\s*\/Page(?![a-zA-Z])/g)?.length ?? 0;
  if (leaves) return leaves;
  // pages kept in compressed object streams: the page tree's root still says how many, when it isn't compressed too
  let best = 0;
  for (const m of text.matchAll(/\/Type\s*\/Pages\b[^>]*?\/Count\s+(\d+)|\/Count\s+(\d+)[^>]*?\/Type\s*\/Pages\b/g)) {
    best = Math.max(best, Number(m[1] || m[2]));
  }
  return best || null;
}

// an arXiv id in the file's name, as arXiv names its downloads (one in the text could be a cited paper's)
const ARXIV_IN = new RegExp(String.raw`(?:^|[^\d.])(${YYMM})(v\d+)?(?!\d)`);

// What a PDF says about itself: its page count and title, when they can be read without decompressing, and the arXiv
// id its file name gives
export function pdfFacts(bytes: Uint8Array, name: string): { ok: true; paper: PaperFile } | { ok: false; reason: string } {
  const head = latin1(bytes.subarray(0, 1024));
  if (!head.includes("%PDF-")) return { ok: false, reason: "That file isn’t a PDF. Choose the paper’s PDF, or give its arXiv link instead." };
  const text = latin1(bytes);
  const hit = ARXIV_IN.exec(name);
  return { ok: true, paper: { name, size: bytes.length, pages: pagesOf(text), title: titleOf(text), arxiv: hit ? hit[1] + (hit[2] || "") : null } };
}

// ------------------------------------------------------------------ the request
export const mb = (bytes: number) => (bytes >= 1024 * 1024 ? `${(bytes / 1024 / 1024).toFixed(1)} MB` : `${Math.max(1, Math.round(bytes / 1024))} KB`);

// a word for the shell: as it is when it's safe, else single-quoted
export const sh = (s: string) => (/^[\w@%+=:,./-]+$/.test(s) ? s : `'${s.replace(/'/g, "'\\''")}'`);

const slugOf = (r: Repo) => r.name.toLowerCase().replace(/[^a-z0-9._-]+/g, "-") || "paper";
// one command over several lines, each group of flags on its own continued line
const run = (...groups: string[]) => groups.filter(Boolean).join(" \\\n  ");

// The commands a full deployment runs for this request, in order, as one script with a line on what each step does
export function commands(q: CheckRequest): string {
  const url = repoUrl(q.repo);
  const s = slugOf(q.repo);
  const work = `work/${s}`, runs = `runs/${s}`;
  const ref = q.commit.trim() || q.repo.ref;
  const pdf = q.paper ? q.paper.name : "paper.pdf";
  const lines = [
    "# 1. The code, at the commit to check",
    `git clone ${url} ${work}`,
    ...(ref ? [`git -C ${work} checkout ${sh(ref)}`] : []),
    `COMMIT=$(git -C ${work} rev-parse HEAD)`,
    "",
    "# 2. The paper: every number it reports, and every setting it states or leaves out",
    ...(!q.paper && q.arxiv ? [`curl -L -o paper.pdf https://arxiv.org/pdf/${q.arxiv}`] : []),
    run(`gapfinder ledger ${sh(pdf)} --repo ${url}`, `--out ${runs}/ledger${q.arxiv ? ` --arxiv ${q.arxiv}` : ""}`),
    "",
    `# 3. The harness for one number. Set CLAIM to its id in ${runs}/ledger/claim_ledger.json:`,
    q.named && (q.named.figure || q.named.metric)
      ? `#    the claim from ${[q.named.figure, q.named.metric].filter(Boolean).join(", ")}${q.named.value ? ` (the paper reports ${q.named.value})` : ""}.`
      : "#    the paper's headline result, or any number you want explained.",
    `#    Then read ${runs}/harness/HARNESS.md and approve it: nothing is searched before you do.`,
    "CLAIM=C1",
    run(`gapfinder harness ${url} --commit "$COMMIT" --local ${work}`, `--ledger ${runs}/ledger --target "$CLAIM" --out ${runs}/harness`,
      q.named?.command.trim() ? `--command ${sh(q.named.command.trim())}` : ""),
    "",
    `# 4. The search, up to ${q.budget} runs; it ends with ${runs}/search/gap_report.md`,
    run(`gapfinder search --spec ${runs}/harness/spec.yaml --targets ${runs}/harness/targets.json`,
      `--assumptions ${runs}/ledger/assumptions.json --claims ${runs}/ledger/claim_ledger.json`,
      `--max-runs ${q.budget} --out ${runs}/search`, q.title.trim() ? `--paper ${sh(q.title.trim())}` : ""),
  ];
  return lines.join("\n") + "\n";
}

// the request as a file to keep: what was given, without the PDF itself
export function requestFile(q: CheckRequest, made: Date): string {
  return JSON.stringify({
    gapfinder_request: 1,
    made: made.toISOString(),
    paper: { title: q.title.trim() || null, file: q.paper ? { name: q.paper.name, bytes: q.paper.size, pages: q.paper.pages } : null, arxiv: q.arxiv },
    code: { repository: repoUrl(q.repo), commit: q.commit.trim() || q.repo.ref || null },
    number: q.named ? { where: q.named.figure || null, metric: q.named.metric || null, paper_value: q.named.value || null,
                        command: q.named.command.trim() || null } : "every number the paper reports",
    max_runs: q.budget,
  }, null, 2) + "\n";
}
