# Feedback on Token Factory, Sandboxes and Nemotron

From building GapFinder (October 2026). Every item below was hit while building it, and each one
names the file or log that shows it. The running log, with dates, is [FEEDBACK.md](../FEEDBACK.md).

## Sandboxes

### 1. The reported `cost` isn't billed during the Beta, and nothing says so
- **Issue:** Every run returns a `cost` of about 0.01 per CPU-second (1 core x 20 s = 0.200;
  4 cores x 5 s = 0.200; `sleep 5` = 0.00007). We had a $50 budget, so we treated it as real
  money. When we checked the console on 2026-10-08, its usage page listed only inference ($1.58);
  the $7.82 of sandbox cost our runs had reported by then appeared nowhere in billing. Our runs
  have reported $48.67 in total since.
- **Steps:** Run `sleep 5`, then a command that keeps one core busy for 20 s, then one that keeps 4
  cores busy for 5 s. Read `cost` from each, and compare with the billing page.
- **Impact:** We nearly cut our experiments 20x to stay inside a budget that wasn't being spent.
  Compiling a C++ system in a sandbox looks like it costs more than a hackathon's credits.
- **Suggestion:** Label `cost` as "estimated, not billed during Beta" in the API response and the
  docs; publish the price per CPU-second and the unit of `cost`; show sandbox usage on the
  billing page once it is billed.
- **Evidence:** `eval/results/spikes/S0_pricing_probe.json`.

### 2. `resources.elapsed_time` is CPU time, not wall-clock time
- **Issue:** A `sleep 5` reports `elapsed_time` 0.0; a 4-core busy loop of 5 s reports about 20.
- **Impact:** Anyone timing benchmarks with it gets wrong numbers silently.
- **Suggestion:** Rename it (`cpu_time`), or document it and add a wall-clock field.

### 3. Checkpoint IDs name the filesystem's content: document it, it's a feature
- **Issue:** Runs that leave identical files return the same image UUID, with or without
  different environment variables. Identical commands still re-execute. The branching guide
  doesn't say this; we found it by experiment (spike S2).
- **What we built on it:** GapFinder loads a database several times with the same command and
  compares the IDs. 12 loads of RusKey gave 12 different IDs, and the paper's ratios varied with
  them. This caught a reproducibility problem that forking from one checkpoint hides.
- **Suggestion:** State in the branching guide that UUIDs identify content. Add a way to list
  which paths differ between two checkpoints: we could tell *that* our loads differed, but not
  *where* (timestamps or real structure) without downloading both.
- **Evidence:** `eval/results/ruskey_load_variance.json`, `papers/ruskey/FINDINGS.md`.

### 4. The authentication setup isn't on the overview or branching pages
- **Issue:** The overview and branching guide don't say how to authenticate. The SDK source
  shows that `IAMAuth` reads `NEBIUS_API_KEY` and `NEBIUS_PROJECT_ID` and defaults to
  `https://api.tokenfactory.nebius.com/sandboxes/`. The branching example passes an `api_client`
  whose construction isn't shown.
- **Impact:** A first-time user has to read `contree_sdk/auth.py` to get a client.
- **Suggestion:** Add a three-line quickstart to the overview: the two environment variables and
  `Contree()`.

### 5. The mini-swe-agent integration page is out of date
- **Issue:** The page says `ContreeEnvironment` still imports the removed
  `contree_sdk.config.ContreeConfig` and that no workaround exists. With `mini-swe-agent==2.4.6`
  and `contree-sdk==0.3.6`, the import works. The real limitation is different: the environment
  always builds its own `ContreeSync(config=...)` and can't accept a client.
- **Steps:** `pip install contree-sdk==0.3.6 mini-swe-agent==2.4.6`, then
  `python -c "from minisweagent.environments.extra.contree import ContreeEnvironment"`.
- **Impact:** A reader concludes the integration is unusable and writes their own adapter.
- **Suggestion:** Update the page with a tested version pair. Upstream, accept a `client=`
  argument, or document passing `contree_config`.

## Token Factory inference

### 6. Billed usage was about 10% above the `usage` the responses reported
- **Issue:** Summing `usage` over every response gave $1.42; the console billed $1.58. Ultra
  input was billed at 0.63M tokens against 0.55M seen in responses. Most likely, long Ultra calls
  that timed out on the client were still processed and billed.
- **Impact:** A client-side spend cap based on response `usage` can be exceeded.
- **Suggestion:** A per-key usage endpoint, or request IDs on the billing export, so clients can
  reconcile. (We now record failed calls at their estimated input cost.)

### 7. `/v1/models?verbose=true` returns live pricing: this worked well, so document it
- **What worked:** The verbose list includes per-token prompt and completion prices and context
  length. We price every call from it, so our spend ledger matches the list price without
  hard-coding it.
- **Suggestion:** Document the parameter on the API intro page; we found it by trying it.

### 8. The base URL differs between pages
- **Issue:** The API intro uses `https://api.tokenfactory.nebius.com/v1/`; Nebius's Nemotron page
  shows `https://api.tokenfactory.us-central1.nebius.com/v1/`. The first one works for us.
- **Suggestion:** Use one URL everywhere, or explain when the regional one is needed.

## Nemotron models

### 9. Nemotron 3 Nano Omni isn't served
- **Issue:** `nvidia/Nemotron-3-Nano-Omni` isn't in `/v1/models`. The NVIDIA models served are
  text only (Nemotron 3 Ultra, Super, Nano, and Nemotron 3.5 Lightning).
- **Impact:** A Nemotron-only pipeline has no model that reads images. We wanted it to read values
  off a paper's figures, and the figure had to be digitized outside the pipeline instead.
- **Suggestion:** Serve Nano Omni, or list it as coming soon.

### 10. What worked: long context and structured output
- Nemotron 3 Ultra answered a needle question in a ~100K-token prompt correctly in 5.2 s.
- All three text tiers returned schema-valid JSON when asked for it.
- The docs don't say where a reasoning model's trace is returned (a separate field, or
  `<think>` tags in the content), so our router handles both. Documenting it would help.

## Onboarding

### 11. Bangladesh is missing from the billing-country list
- **Issue:** Bangladesh can't be selected as the billing country. The hackathon rules don't
  exclude Bangladesh, but they require runtime calls to Token Factory.
- **Impact:** An eligible participant was blocked from onboarding until a workaround was found.
- **Suggestion:** Let participants redeem hackathon credits without a billing country, or support
  more countries.
