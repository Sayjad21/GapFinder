# Accounts, keys and repo setup (done; kept for reference)

## What you need, and how many

| # | What | How many | Goes in `.env` as | Needed for |
|---|---|---|---|---|
| 1 | Token Factory API key | 1 | `TOKEN_FACTORY_API_KEY` | All Nemotron calls (ledger, assumptions, spikes S5 and S7) |
| 2 | Sandboxes Beta access | 1 approval | — | Spikes S1–S4 and everything from M2 on |
| 3 | Sandboxes API key | 1 (try key #1 first; it may be the same key) | `NEBIUS_API_KEY` | Sandboxes |
| 4 | Project ID | 1 | `NEBIUS_PROJECT_ID` | Sandboxes |
| 5 | Tavily API key (optional) | 1 | `TAVILY_API_KEY` | M3 evidence search only |

So the minimum is **one key, one project ID and one access approval**. Tavily
can wait until M3.

## Step 1: Unblock billing (needed before any key works)

Nebius won't let you finish account setup without a bank card, and the free
credits only apply to an account that has billing set up.

- [ ] Post in the Nebius Discord (https://discord.gg/eXYTGhgnhK) and ask
      whether participants without a card can get the hackathon credits
      another way. Message to paste:
      > Hi! I'm registered for the Nebius × NVIDIA Global AI Hackathon (building on Token Factory + Sandboxes). I'm a student in Bangladesh and don't have an international bank card, so I can't complete billing setup to redeem the hackathon credits (NEBIUS-DEVPOST-GLOBAL26). Is there another way for participants without a card to activate the credits, for example applying them to an account directly? I'd also like to request Sandboxes Beta access for the same project. Thanks!
- [ ] At the same time, ask your bank about a dual-currency or international
      debit card. These usually need the USD travel or student quota endorsed
      on your passport. A few dollars of USD balance is enough.
- [ ] Or use a family member's card, with their permission. Stay within the
      free credits so nothing is charged.

## Step 2: Token Factory account and key

- [ ] Sign up at https://tokenfactory.nebius.com (Google or GitHub login).
- [ ] Complete the billing setup during onboarding.
- [ ] Claim the **$25 hackathon credit**: fill in the form at
      https://nebius.com/promo-code?utm_promo_event_code=2026-devpost-global-ai-hack&utm_promo_code_type=Token_Factory&utm_promo_activation_code=NEBIUS-DEVPOST-GLOBAL26
      with activation code **`NEBIUS-DEVPOST-GLOBAL26`**.
      To apply a code yourself: click your balance → **Top up** → **With promo code**.
- [ ] Join the Builders Program at https://dev.nebius.com/builders. It's free
      and gives another **$25** of Token Factory credit, plus Tavily credit.
- [ ] Create the API key at https://tokenfactory.nebius.com/project/api-keys
      → **Create API key** → name it `gapfinder` → **Create**.
      **Copy it immediately; it's shown only once.**
- [ ] Set a budget alert on the Billing page if one is offered.

## Step 3: Sandboxes access and project ID

- [ ] Request Beta access at https://tokenfactory.nebius.com/sandboxes/about.
      Use case: *"Nebius × NVIDIA hackathon: forking a built RocksDB checkpoint
      into ~40 parallel branches to find why paper reproductions diverge."*
- [ ] No reply in 1–2 days: email contree@nebius.com and ask in Discord.
- [ ] Once approved, find the **project ID**. It's in the console's project
      settings or project switcher, and may also appear in the browser URL
      inside a project. If you can't find it, ask in Discord.
- [ ] For `NEBIUS_API_KEY`, try the Token Factory key from Step 2 first. If
      Sandboxes rejects it, create a separate key in the Sandboxes section.

## Step 4: Tavily (optional, before M3)

- [ ] Get the Tavily credit through the Builders Program, or sign up at
      https://tavily.com and use promo code **`BBDEVPOST`**.
- [ ] Copy the API key.

## Step 5: Put the keys in `.env` and check them

Never paste keys into chat, commits or screenshots. `.env` is git-ignored.

```bat
cd "C:\Users\Legion\Downloads\nvidia hackathon\gapfinder-repo"
copy .env.example .env
```

Fill in `.env`:

```
TOKEN_FACTORY_API_KEY=...
NEBIUS_API_KEY=...
NEBIUS_PROJECT_ID=...
TAVILY_API_KEY=...
GF_SANDBOX_BACKEND=contree
```

Check (spends nothing):

```bat
.venv\Scripts\python scripts\check_env.py
```

- [ ] `[1]` shows `OK` and all four Nemotron models present. If a model is
      missing, set `GF_MODEL_<TIER>=<exact id>` from the list it prints. If
      the call fails, try
      `TOKEN_FACTORY_BASE_URL=https://api.tokenfactory.us-central1.nebius.com/v1/`.
- [ ] `[2]` shows `OK: authenticated`.
- [ ] Then run the M0 spikes in the order in `tests/spikes/README.md`.

## Step 6: Create the GitHub repo and push

- [ ] On GitHub: **New repository** → name `gapfinder` → **Public** (the
      rules require a public repo) → **don't** add a README, license or
      .gitignore (the repo already has them).
- [ ] Before the first commit, check that no secrets or paper files are staged:

```bat
cd "C:\Users\Legion\Downloads\nvidia hackathon\gapfinder-repo"
git add -A
git status
```

`git status` must **not** list `.env`, `.gf_cache/`, `.gf_local/`, `runs/`,
`*.pdf` or `ruskey_paper.txt`.

```bat
git commit -m "GapFinder: M0 spikes, M1/M2 foundations, local sandbox backend"
git branch -M main
git remote add origin https://github.com/<your-username>/gapfinder.git
git push -u origin main
```

- [ ] On the repo page, confirm the MIT license badge shows at the top of the
      README.
- [ ] Open the **Actions** tab and confirm the `tests` workflow passes.
