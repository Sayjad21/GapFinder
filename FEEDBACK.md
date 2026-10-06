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

### 4. Branching dedup is documented as a feature but affects benchmarking
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
