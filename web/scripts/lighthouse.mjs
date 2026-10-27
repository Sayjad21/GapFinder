// Lighthouse on the built static site: serves <dir> on a local port, audits a few pages, and fails when accessibility
// or best practices fall under their floor. Performance is printed, not enforced: on a shared CI runner it swings too
// much to gate on.
//   node scripts/lighthouse.mjs dist-static [out-dir]
import { spawn } from "node:child_process";
import { createReadStream, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createServer } from "node:http";
import { extname, join, normalize } from "node:path";
import { createGzip } from "node:zlib";

const LIGHTHOUSE = "lighthouse@13.4.1";
const PAGES = ["#/", "#/cases", "#/case/fastgcn-v15", "#/evidence"];
const FLOOR = { accessibility: 0.95, "best-practices": 0.9 };
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".md": "text/markdown",
  ".svg": "image/svg+xml" };

const [root = "dist-static", out = "lighthouse"] = process.argv.slice(2);
if (!existsSync(join(root, "index.html"))) { console.error(`no ${root}/index.html: build the static site first`); process.exit(2); }
mkdirSync(out, { recursive: true });

// gzip, as GitHub Pages serves it, so the audit sees the bytes a visitor downloads
const server = createServer((req, res) => {
  const path = normalize(decodeURIComponent(new URL(req.url, "http://x").pathname)).replace(/^([/\\])+/, "");
  let file = join(root, path || "index.html");
  if (!file.startsWith(normalize(root)) || !existsSync(file) || statSync(file).isDirectory()) file = join(root, "index.html");
  const gz = /\bgzip\b/.test(req.headers["accept-encoding"] || "");
  res.writeHead(200, { "content-type": TYPES[extname(file)] || "application/octet-stream", ...(gz ? { "content-encoding": "gzip" } : {}) });
  const body = createReadStream(file);
  (gz ? body.pipe(createGzip()) : body).pipe(res);
});
await new Promise((r) => server.listen(0, "127.0.0.1", r));
const base = `http://127.0.0.1:${server.address().port}/`;

// run asynchronously: this process is also the web server, and a blocking spawn would leave the page unanswered.
// Windows runs npx through cmd, which needs the URL and the Chrome flags quoted; elsewhere arguments pass as they are.
const win = process.platform === "win32";
const q = (s) => (win ? `"${s}"` : s);
const run = (args) => new Promise((resolve) => {
  spawn(win ? "npx.cmd" : "npx", args, { stdio: "inherit", shell: win }).on("close", resolve);
});

let failed = false;
for (const [i, page] of PAGES.entries()) {
  const report = join(out, `page-${i}.json`);
  const status = await run(["--yes", LIGHTHOUSE, q(base + page), "--quiet", "--output=json", `--output-path=${report}`,
    "--only-categories=performance,accessibility,best-practices", `--chrome-flags=${q("--headless=new --no-sandbox")}`, "--max-wait-for-load=30000"]);
  if (status !== 0 || !existsSync(report)) { console.error(`lighthouse failed on ${page}`); failed = true; continue; }
  const cats = JSON.parse(readFileSync(report, "utf8")).categories;
  const line = Object.values(cats).map((c) => `${c.title} ${Math.round(c.score * 100)}`).join(", ");
  const low = Object.entries(FLOOR).filter(([k, f]) => cats[k] && cats[k].score < f);
  console.log(`${page.padEnd(22)} ${line}${low.length ? `   BELOW FLOOR: ${low.map(([k]) => k).join(", ")}` : ""}`);
  if (low.length) failed = true;
}
server.close();
process.exit(failed ? 1 : 0);
