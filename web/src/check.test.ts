import { afterEach, describe, expect, it, vi } from "vitest";
import { checkRepo, commands, parseArxiv, parseRepo, pdfFacts, requestFile, sh, type CheckRequest } from "./check.ts";

const bytes = (s: string) => Uint8Array.from(s, (c) => c.charCodeAt(0) & 255);
const PDF = ["%PDF-1.4", "1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj", "2 0 obj << /Type /Pages /Kids [3 0 R 4 0 R] /Count 2 >> endobj",
  "3 0 obj << /Type /Page /Parent 2 0 R >> endobj", "4 0 obj << /Type /Page /Parent 2 0 R >> endobj",
  "5 0 obj << /Title (Graph Structure Learning \\(for GNNs\\)) /Producer (pdfTeX) >> endobj", "%%EOF"].join("\n");

describe("links", () => {
  it("reads a GitHub repository from the ways people paste one", () => {
    expect(parseRepo("https://github.com/matenure/FastGCN")).toEqual({ owner: "matenure", name: "FastGCN", ref: null });
    expect(parseRepo("github.com/o/r.git")).toEqual({ owner: "o", name: "r", ref: null });
    expect(parseRepo("git@github.com:o/r.git")).toEqual({ owner: "o", name: "r", ref: null });
    expect(parseRepo("https://github.com/o/r/tree/v1.0")).toEqual({ owner: "o", name: "r", ref: "v1.0" });
    expect(parseRepo("https://github.com/o/r/blob/main/README.md")).toEqual({ owner: "o", name: "r", ref: null });
    expect(parseRepo("https://github.com/o/r.js/")).toEqual({ owner: "o", name: "r.js", ref: null });
    expect(parseRepo("o/r")).toEqual({ owner: "o", name: "r", ref: null });
    expect(parseRepo("https://gitlab.com/o/r")).toBeNull();
    expect(parseRepo("not a repository")).toBeNull();
  });
  it("reads an arXiv id from an id, a tag or a link, and refuses what isn't one", () => {
    expect(parseArxiv("1801.10247")).toBe("1801.10247");
    expect(parseArxiv("arXiv:1801.10247v3")).toBe("1801.10247v3");
    expect(parseArxiv("https://arxiv.org/abs/1801.10247")).toBe("1801.10247");
    expect(parseArxiv("https://arxiv.org/pdf/1801.10247v1.pdf")).toBe("1801.10247v1");
    expect(parseArxiv("cs/0112017")).toBe("cs/0112017");
    expect(parseArxiv("1813.12345")).toBeNull();
    expect(parseArxiv("hello")).toBeNull();
  });
});

describe("the PDF", () => {
  it("counts the pages and reads the title, and takes the arXiv id only from the file name", () => {
    const r = pdfFacts(bytes(PDF), "1801.10247v2.pdf");
    expect(r).toEqual({ ok: true, paper: { name: "1801.10247v2.pdf", size: PDF.length, pages: 2, title: "Graph Structure Learning (for GNNs)", arxiv: "1801.10247v2" } });
    const plain = pdfFacts(bytes(`${PDF}\n/URI (https://arxiv.org/abs/1706.03762)`), "paper.pdf");
    expect(plain.ok && plain.paper.arxiv).toBeNull();
  });
  it("reads a UTF-16 title, and the page tree's count when the pages are compressed", () => {
    const r = pdfFacts(bytes("%PDF-1.7\n<< /Type /Pages /Count 9 >>\n<< /Title <FEFF004700720061007000680073> >>"), "a.pdf");
    expect(r.ok && [r.paper.pages, r.paper.title]).toEqual([9, "Graphs"]);
  });
  it("ignores titles that are a file name, and says so when the file isn't a PDF", () => {
    const r = pdfFacts(bytes("%PDF-1.5\n<< /Title (Microsoft Word - draft.docx) >>"), "x.pdf");
    expect(r.ok && [r.paper.title, r.paper.pages]).toEqual([null, null]);
    expect(pdfFacts(bytes("PK\u0003\u0004 a zip"), "x.pdf")).toMatchObject({ ok: false });
  });
});

describe("the repository's metadata", () => {
  afterEach(() => { vi.unstubAllGlobals(); });
  it("reads a public repository, and answers missing or unknown instead of throwing", async () => {
    const r = { owner: "o", name: "r", ref: null };
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ description: "code", language: "Python", stargazers_count: 12,
      pushed_at: "2019-03-01T00:00:00Z", size: 2048, license: { spdx_id: "MIT" }, archived: false, default_branch: "master" }))));
    expect(await checkRepo(r)).toEqual({ kind: "ok", facts: { description: "code", language: "Python", stars: 12, pushed: "2019-03-01T00:00:00Z",
      sizeKb: 2048, license: "MIT", archived: false, defaultBranch: "master" } });
    vi.stubGlobal("fetch", vi.fn(async () => new Response("{}", { status: 404 })));
    expect(await checkRepo(r)).toEqual({ kind: "missing" });
    vi.stubGlobal("fetch", vi.fn(async () => new Response("{}", { status: 403 })));
    expect(await checkRepo(r)).toEqual({ kind: "unknown" });
    vi.stubGlobal("fetch", vi.fn(async () => { throw new TypeError("offline"); }));
    expect(await checkRepo(r)).toEqual({ kind: "unknown" });
  });
});

describe("the request", () => {
  const q: CheckRequest = {
    paper: null, arxiv: "1801.10247", title: "FastGCN", repo: { owner: "matenure", name: "FastGCN", ref: null }, commit: "",
    named: { figure: "Table 5", metric: "transductive Cora accuracy", value: "0.818", command: "python train.py --dataset cora" }, budget: 200,
  };
  it("writes the commands a deployment runs, in order, from what was entered", () => {
    const s = commands(q);
    expect(s).toContain("git clone https://github.com/matenure/FastGCN work/fastgcn\n");
    expect(s).toContain("curl -L -o paper.pdf https://arxiv.org/pdf/1801.10247\n");
    expect(s).toContain("gapfinder ledger paper.pdf --repo https://github.com/matenure/FastGCN \\\n  --out runs/fastgcn/ledger --arxiv 1801.10247\n");
    expect(s).toContain("#    the claim from Table 5, transductive Cora accuracy (the paper reports 0.818).\n");
    expect(s).toContain("--target \"$CLAIM\" --out runs/fastgcn/harness \\\n  --command 'python train.py --dataset cora'\n");
    expect(s).toContain("\\\n  --max-runs 200 --out runs/fastgcn/search \\\n  --paper FastGCN\n");
    expect(Math.max(...s.split("\n").map((l) => l.length))).toBeLessThan(110);
    expect(s).not.toContain("checkout");
    expect(commands({ ...q, commit: "a1b2c3", paper: { name: "my paper.pdf", size: 1, pages: 1, title: null, arxiv: null } }))
      .toMatch(/git -C work\/fastgcn checkout a1b2c3\n[\s\S]*gapfinder ledger 'my paper.pdf'/);
  });
  it("quotes for the shell only when it has to", () => {
    expect(sh("runs/x.yaml")).toBe("runs/x.yaml");
    expect(sh("it's")).toBe("'it'\\''s'");
  });
  it("keeps the request as a file, without the PDF itself", () => {
    const f = JSON.parse(requestFile(q, new Date("2026-10-27T10:00:00Z"))) as Record<string, unknown>;
    expect(f).toMatchObject({ made: "2026-10-27T10:00:00.000Z", max_runs: 200, code: { repository: "https://github.com/matenure/FastGCN", commit: null },
      number: { where: "Table 5", paper_value: "0.818" }, paper: { arxiv: "1801.10247", file: null } });
  });
});
