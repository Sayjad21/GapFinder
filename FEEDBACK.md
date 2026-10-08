# Tool feedback log (running)

Every rough edge goes here as it happens. At submission it becomes the
structured feedback: product, issue, steps to reproduce, impact, suggestion.
**Only issues actually hit go in.** Entries marked *unverified at runtime*
were found by reading code or docs and still need confirmation against the
live service.

---

### 1. Sandboxes docs: the mini-swe-agent integration page looks out of date
- **Product:** Token Factory Sandboxes docs (`/sandboxes/sdk/integrations/mini-swe-agent.md`)
- **Issue:** The page says `ContreeEnvironment` "still imports the removed
  `contree_sdk.config.ContreeConfig` type" and that no workaround exists. With
  `mini-swe-agent==2.4.6` and `contree-sdk==0.3.6`, `contree_sdk/config.py`
  exists and
  `from minisweagent.environments.extra.contree import ContreeEnvironment` imports
  cleanly. The remaining real limitation is that it can't accept an explicit
  client: it always builds its own `ContreeSync(config=...)`.
- **Repro:** `pip install contree-sdk==0.3.6 mini-swe-agent==2.4.6`, then
  `python -c "from minisweagent.environments.extra.contree import ContreeEnvironment"`.
- **Impact:** A reader following the docs concludes the integration is unusable
  and writes their own adapter (we did, for other reasons).
- **Suggestion:** Update the page with the tested version pair, and either
  accept a `client=` kwarg upstream or document passing `contree_config`.
- *Unverified at runtime* (no Beta access yet): import and config construction
  only.

### 2. Sandboxes docs: auth environment variables are not on the overview or branching pages
- **Product:** Sandboxes docs / contree-sdk
- **Issue:** The overview and branching guide don't say how to authenticate.
  We found it in the SDK source: `IAMAuth` reads `NEBIUS_API_KEY` and
  `NEBIUS_PROJECT_ID`, and defaults to
  `https://api.tokenfactory.nebius.com/sandboxes/`. The branching example also
  passes an `api_client` whose construction isn't shown.
- **Impact:** A first-time user has to read `contree_sdk/auth.py` to get a client.
- **Suggestion:** Add a three-line quickstart (env vars + `Contree()`) to the
  overview.

### 3. Token Factory: base URL varies by source
- **Product:** Token Factory inference API
- **Issue:** The API intro uses `https://api.tokenfactory.nebius.com/v1/`;
  Nebius's own Nemotron page shows `https://api.tokenfactory.us-central1.nebius.com/v1/`.
- **Impact:** Unclear which one to hard-code. We made it configurable
  (`TOKEN_FACTORY_BASE_URL`) and spike S5 records which one works.
- *To confirm in S5.*

### 4. Branching dedup (resolved by spike S2)
- **Measured:** identical commands DO re-execute (different stdout each time), but runs that leave
  an identical filesystem return the same image UUID, with or without a distinct env var. UUIDs look
  content-addressed. Harmless for us (each branch writes different result files), but undocumented.
- **Suggestion:** say in the branching guide that UUIDs identify filesystem content, not runs.

### 4a. (original note) Branching dedup is documented as a feature but affects benchmarking
- **Product:** Sandboxes
- **Issue:** The branching guide notes that identical commands from the same
  image return the same UUID. For anyone measuring noise from repeated runs,
  this means repeats may be served from cache. The docs don't say whether the
  command re-executes.
- **Impact:** Silent zero-variance noise estimates.
- **Mitigation here:** a unique `RUN_TAG` env var per run. Spike S2 measures
  the actual behaviour.
- *To confirm in S2.*

### 5. Environment: uv cache extraction races on Windows
- **Product:** n/a (local tooling, not Nebius). Kept here only as a setup note.
- `uv pip install` failed with `failed to open file ...dist-info/WHEEL` from
  the default cache. A fresh `UV_CACHE_DIR` plus `UV_LINK_MODE=copy` fixed it.
  Leave this out of the submitted feedback.

### 6. Token Factory: Nemotron 3 Nano Omni isn't offered (confirmed)
- **Product:** Token Factory model catalogue
- **Issue:** `nvidia/Nemotron-3-Nano-Omni` isn't in `/v1/models`. The only
  NVIDIA models served are text-only: Nemotron 3 Ultra, Super, Nano and
  Nemotron 3.5 Lightning. A Nemotron-only pipeline therefore has no model for
  image input (reading values off figures).
- **Impact:** Figure reading has to use a non-NVIDIA vision model.
- **Suggestion:** Serve Nano Omni, or list it as coming soon.

### 7. Token Factory: `/v1/models?verbose=true` returns live pricing (worked well)
- **Product:** Token Factory API
- **What worked:** The verbose model list includes per-token prompt and
  completion prices plus context length. We use it to price every call
  exactly, so our spend ledger matches the list price without hard-coding it.
- **Suggestion:** Document this parameter on the API intro page. We found it by
  trying it.

### 8. Token Factory: confirmed base URL and real limits
- `https://api.tokenfactory.nebius.com/v1/` works. The regional URL wasn't
  needed (resolves item 3).
- Nemotron 3 Ultra: ~100K-token prompt with a needle answered correctly in 5.2 s.
  The listed context is 1,048,576 tokens.
- All three text tiers returned schema-valid JSON when asked for it.

### 9. Onboarding: Bangladesh is missing from the billing country list
- **Product:** Token Factory signup / billing
- **Issue:** Bangladesh isn't selectable as the billing country. The hackathon
  rules don't exclude Bangladesh, but they require runtime calls to Token
  Factory, so an eligible participant can't complete onboarding without help.
- **Impact:** Blocked a participant until a workaround was found.
- **Suggestion:** Let participants redeem hackathon credits without a billing
  country, or support more countries.

### 10. Sandboxes: pricing and the `elapsed_time` field are undocumented and surprising
- **Product:** Token Factory Sandboxes (Beta)
- **What we measured** (eval/results/spikes/S0_pricing_probe.json): `cost` tracks CPU-seconds at
  about 0.01 per CPU-second (1 core x 20 s = 0.200; 4 cores x 5 s = 0.200; `sleep 5` = 0.00007).
  `resources.elapsed_time` reports CPU time, not wall-clock time (a 5 s sleep reports 0.0 s).
- **Impact:** At ~36 per CPU-hour, compiling a C++ system like RocksDB inside a sandbox (thousands of
  CPU-seconds) costs more than a hackathon's credits. We couldn't find pricing, the unit of `cost`, or
  the meaning of `elapsed_time` in the docs, and only discovered this by spending.
- **Suggestion:** Document the price per CPU-second and the unit of `cost`; rename or document
  `elapsed_time`; show sandbox spend on the billing page; let OCI import cover heavy builds cheaply.
- **Confirmed 2026-10-08:** the console's usage page lists only Token Factory inference ($1.58);
  ~$7.82 of reported sandbox `cost` doesn't appear anywhere in billing. So during the Beta the field
  reports a price that isn't charged. That's good for users, but undocumented and alarming: we nearly
  shrank our experiments 20x to stay inside a budget that wasn't being spent.
- **Suggestion:** label `cost` as "estimated, not billed during Beta" in the API and docs.

### 11. Billing: inference usage exceeded what the API responses reported (~10%)
- **Product:** Token Factory inference / billing
- **Issue:** Summing `usage` from every response gave $1.42; the console billed $1.58 (Ultra input
  0.63M tokens billed vs 0.55M seen in responses). Most likely long Ultra calls that timed out on the
  client were still processed and billed, with no usage reported back.
- **Impact:** Client-side budget tracking undercounts; a hard cap based on response usage can be
  exceeded.
- **Suggestion:** expose a per-key usage endpoint (or request IDs in billing) so clients can reconcile.
  We now record failed calls at their estimated input cost and reconcile against the console.
