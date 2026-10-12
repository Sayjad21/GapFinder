# Feedback on Token Factory, Sandboxes and Nemotron

From building GapFinder (October 2026). Every item below was hit while building it (item 8 was planned
around and never hit; it says so), and each one names the file or log that shows it. The running
log, with dates, is [FEEDBACK.md](../FEEDBACK.md).

## Sandboxes

### 1. The reported `cost` isn't billed during the Beta, and it is easy to mistake for billing
- **Issue:** Every run returns a `cost` of about 0.01 per CPU-second (1 core x 20 s = 0.200;
  4 cores x 5 s = 0.200; `sleep 5` = 0.00007). We had a $50 budget, so we treated it as real
  money. When we checked the console on 2026-10-08, its usage page listed only inference ($1.58);
  the $7.82 of sandbox cost our runs had reported by then appeared nowhere in billing.
- **Update, October 12:** the Sandboxes docs do call the field diagnostic, and the console still
  showed no Sandboxes charge for 6-12 October. The trap is that it is dollar-scaled and grows large.
  One default MC Dropout cell reports $26.73. Four pieces of the MC Dropout case alone reported
  $1,043.03, $584.66, $134.56 and $733.06 (total $2,495.31). Any client-side guard that counts it, as
  ours did, refuses to run until you raise it by hand (we set `GF_SANDBOX_GUARD_USD=20000`).
- **Steps:** Run `sleep 5`, then a command that keeps one core busy for 20 s, then one that keeps 4
  cores busy for 5 s. Read `cost` from each, and compare with the billing page.
- **Impact:** We nearly cut our experiments 20x to stay inside a budget that wasn't being spent.
  Compiling a C++ system in a sandbox looks like it costs more than a hackathon's credits.
- **Suggestion:** Name it so it can't be read as money (`estimated_cost`, or CPU-seconds), say so in
  the API response as well as the docs, publish the unit and the price per CPU-second, and show
  sandbox usage on the billing page once it is billed.
- **Evidence:** `eval/results/spikes/S0_pricing_probe.json`,
  `eval/external/mc-dropout/RESULT.md` (Cost), `eval/external/mc-dropout/posthoc/README.md`.

### 2. `resources.elapsed_time` is CPU time summed over processes, not wall-clock time
- **Issue:** A `sleep 5` reports `elapsed_time` 0.0; a 4-core busy loop of 5 s reports about 20.
  Later we measured it directly: it equals user plus system CPU time summed over all processes. A
  test that took 63.9 s of real time reported 180.4 s, and a 4-process test reported 150 s for a 60 s
  wall-clock run. (We log it as `elapsed_s`.) The 3,600 s operation timeout (item 6) is real wall
  time, so the two numbers are not comparable.
- **Impact:** Anyone timing benchmarks with it gets wrong numbers silently. We did: a default
  MC Dropout cell reported 2,673 s, and we concluded a sandbox behaves like one core, then planned
  and froze a design around it. A direct test showed the VM has 4 effective cores (`nproc` 4, four
  CPU-bound processes each got a full core), and the same cell took about 805 s of wall time once
  we sharded it over the 4 cores. The one-core reading was wrong and cost us a deviation to correct.
- **Suggestion:** Rename it (`cpu_time`), or document it and add a wall-clock field.
- **Evidence:** `eval/results/spikes/S0_pricing_probe.json`;
  `eval/external/mc-dropout/FROZEN.md` (Deviation 2, then Deviation 3).

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

### 6. One operation can run for at most 3,600 s, and a longer timeout returns HTTP 400
- **Issue:** Asking for a 14,400 s timeout returned HTTP 400, "Timeout 14400 exceeds the maximum
  allowed value of 3600". The message is clear, but we first met it on a smoke run, after we had
  planned arms around 4-hour cells. In a local run, 21 of 26 cells of one arm took longer than 3,600 s.
- **Steps:** Submit any run with `timeout=14400`.
- **Impact:** Long benchmark cells can't run as one operation. We had to shard each cell over the
  VM's 4 cores (a default cell fell from about 1,910 s to 805 s). Five of 22 runs in one arm still
  hit the limit, so that search lost information.
- **Suggestion:** State the cap on the operations page. For long jobs, offer a way to continue
  work across operations (resumable or detached processes with polling).
- **Evidence:** `eval/external/mc-dropout/FROZEN.md` (Deviations 2 and 3),
  `eval/external/mc-dropout/RESULT.md` ("What went wrong and the deviations", item 6).

### 7. The image's `ENV` is not applied to runs, and libraries start one thread per visible core
- **Issue:** Environment variables set in the Dockerfile we used locally (`THEANO_FLAGS`,
  `KERAS_BACKEND`) were not applied to runs on our Sandboxes checkpoint, and our spec has no place
  to set them, so we exported them in the run command. (We rebuilt the image through build
  operations and did not test whether `ENV` in an imported OCI image is applied.)
- **Related, ours and not Nebius's:** The same artifact first timed out in local Docker because OpenBLAS
  starts one thread per visible core, and Docker Desktop showed each container all 12 host cores.
  Six cells at once ran 7.5 times slower than one cell alone until we set `OPENBLAS_NUM_THREADS=1`.
  A Sandboxes VM shows 4 cores, so numpy-based code that shards over processes needs the same cap.
- **Impact:** Every run command has to carry its own environment, which is easy to forget and
  nothing warns about.
- **Suggestion:** Apply the checkpoint's `ENV` to runs, or document that it isn't, and show how to
  set environment variables for every run of a checkpoint. A docs note on thread caps for scientific
  Python would help.
- **Evidence:** `eval/external/mc-dropout/FROZEN.md` (Deviation 1 for the threads, Deviation 2 for
  `ENV`).

### 8. The Beta limit of 50 simultaneous operations is per project (planned around, not hit)
- **Issue:** The limit is shared by everything running in the project, but a client sees it only
  as its own concurrency. Our search runs several arms as separate processes, each with its own
  concurrency setting, so the limits add up.
- **What we did:** We kept the total at 48 or below (24 each for two arms, 12 each for four), and our
  launcher script refuses a total above 50. We never saw the error the service returns, so we
  don't know what a client would see.
- **Suggestion:** Return the current count and the limit in a response header or a small status call,
  and make the over-limit error distinguishable from other failures, so clients can back off.
- **Evidence:** `eval/external/mc-dropout/FROZEN.md` (Deviation 3, "Concurrency settings"),
  `scripts/run_mcd_sandbox_arms.sh`.

## Token Factory inference

### 9. Billed usage was about 10% above the `usage` the responses reported
- **Issue:** Summing `usage` over every response gave $1.42; the console billed $1.58. Ultra
  input was billed at 0.63M tokens against 0.55M seen in responses. Most likely, long Ultra calls
  that timed out on the client were still processed and billed.
- **Impact:** A client-side spend cap based on response `usage` can be exceeded.
- **Suggestion:** A per-key usage endpoint, or request IDs on the billing export, so clients can
  reconcile. (We now record failed calls at their estimated input cost.)

### 10. `/v1/models?verbose=true` returns live pricing: this worked well, so document it
- **What worked:** The verbose list includes per-token prompt and completion prices and context
  length. We price every call from it, so our spend ledger matches the list price without
  hard-coding it.
- **Suggestion:** Document the parameter on the API intro page; we found it by trying it.

### 11. The base URL differs between pages
- **Issue:** The API intro uses `https://api.tokenfactory.nebius.com/v1/`; Nebius's Nemotron page
  shows `https://api.tokenfactory.us-central1.nebius.com/v1/`. The first one works for us.
- **Suggestion:** Use one URL everywhere, or explain when the regional one is needed.

## Nemotron models

### 12. Nemotron 3 Nano Omni isn't served
- **Issue:** `nvidia/Nemotron-3-Nano-Omni` isn't in `/v1/models`. The NVIDIA models served are
  text only (Nemotron 3 Ultra, Super, Nano, and Nemotron 3.5 Lightning).
- **Impact:** A Nemotron-only pipeline has no model that reads images. We wanted it to read values
  off a paper's figures, and the figure had to be digitized outside the pipeline instead.
- **Suggestion:** Serve Nano Omni, or list it as coming soon.

### 13. What worked: long context and structured output
- Nemotron 3 Ultra answered a needle question in a ~100K-token prompt correctly in 5.2 s.
- All three text tiers returned schema-valid JSON when asked for it.
- The docs don't say where a reasoning model's trace is returned (a separate field, or
  `<think>` tags in the content), so our router handles both. Documenting it would help.

## Onboarding

### 14. Bangladesh is missing from the billing-country list
- **Issue:** Bangladesh can't be selected as the billing country. The hackathon rules don't
  exclude Bangladesh, but they require runtime calls to Token Factory.
- **Impact:** An eligible participant was blocked from onboarding until a workaround was found.
- **Suggestion:** Let participants redeem hackathon credits without a billing country, or support
  more countries.
