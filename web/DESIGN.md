# GapFinder web: design plan

## Brief

**Subject.** A tool that finds out why a paper's reported number and its released code's number disagree. It runs
the code in sandboxes, changes one condition at a time, and ends with a labelled verdict, or an honest "nothing I
can change explains this".

**Audience.** ML researchers and reviewers deciding whether to trust it, and hackathon judges with ten minutes.

**Primary job.** Show, case by case, the paper's number, the code's number, the gap between them, and what closed
it. Be as clear about the misses as about the finds.

## The idea: the gap is the object

Every case is a measurement. The paper states a number, and the code gives another. The distance between the two is
what the whole product is about. The page treats that distance as a physical thing: **the gap gauge**. It is a
measuring rule with two jaws, the code's reading and the paper's reading, and a marker-highlighted span between
them. When GapFinder's answer is applied, the code's jaw moves to its new reading, and the highlighted span shrinks
to what is left. That one element is the bold move. Everything around it stays quiet.

Typography encodes the two sides:
- **The paper's voice is a serif.** Quotes, claims and the paper's numbers.
- **The machine's voice is a sans.** Readings, labels and the interface.
- **Code identifiers only are monospaced**, e.g. `dominant.py:98`. Monospace is never used for labels.

## Tokens

### Color (light)

| Name | Hex | Role |
|---|---|---|
| sheet | #F4F6F8 | page: a cool, faintly blue sheet, like a lab notebook's ruled page |
| ink | #13243A | primary text: dark iron-gall blue, not a tinted black |
| graphite | #566173 | secondary text, axes |
| rule | #D5DCE4 | gridlines, dividers, the gauge's ticks |
| marker | #F2D94E | **only** the gap: the highlighter stroke between the two readings |
| proof | #1F6F8B | links, focus, the code's jaw: a technical cyan-blue |

Verdicts, a status set that is never used for anything else:
- found #1D7A55
- partial #A86A12
- abstained #566173
- missed #B4372B

Each always comes with a word and a glyph, never color alone.

### Color (dark)

A night version, chosen rather than inverted: sheet #0F1B2A, ink #E6ECF2, graphite #9AA6B6, rule #26364A,
marker #E9CF3F, proof #5FB3CF.

### Type

- **Newsreader** (variable serif, optical sizes) for the paper's voice: headlines, claims, quotes.
- **Instrument Sans** (variable sans) for the interface and readings, with tabular figures in every number column.
- **JetBrains Mono** only inside `code`.
- Scale (1.25 ratio, 17px body): 13.6 / 17 / 21.3 / 26.6 / 33.2 / 41.5 / 51.9.
- Body measure is at most 68ch.
- Headings use `text-wrap: balance`, sentence case, and are never all caps.

### Layout

A 12-column grid, 1200px max, 24px gutters, 16px side gutters on phones.

```
 home                                         case
 ┌──────────────────────────────────────┐    ┌──────────────────────────────────────┐
 │ GapFinder      Cases Planted How …   │    │ ← Cases   GCN topology attack        │
 ├──────────────────────────────────────┤    │ serif title, verdict word + glyph    │
 │ serif headline (one sentence)        │    ├───────────────┬──────────────────────┤
 │ ┌──────── the gap gauge ───────────┐ │    │ gap gauge     │ what the paper says  │
 │ │ code ├▓▓▓▓▓ gap ▓▓▓▓▓┤ paper      │ │    │ (large)       │ (serif quote)        │
 │ └──────────────────────────────────┘ │    ├───────────────┴──────────────────────┤
 │ what closed it, in one line          │    │ the investigation (replay)           │
 │ case switcher: 4 found cases         │    │ experiments as a growing strip       │
 ├──────────────────────────────────────┤    ├──────────────────────────────────────┤
 │ the record: 16 real papers as one    │    │ the verdict card (Gap Report)        │
 │ part-to-whole strip; planted rates   │    ├──────────────────────────────────────┤
 │ by version; dev suite                │    │ versions: c5 → c7 → c8               │
 ├──────────────────────────────────────┤    └──────────────────────────────────────┘
 │ cases index: a ledger table          │
 └──────────────────────────────────────┘
```

- Left-aligned throughout. Only the gauge's readings are centred on their jaws.
- Index pages are tables, not card grids: every case has the same columns (paper, documented cause, GapFinder's
  answer, verdict), and a table is the honest form for comparing rows.

### Principles

1. **The gap is the only highlighter.** Marker yellow appears nowhere else.
2. **Every number names its source**: the paper (serif) or a run (sans, with its count of runs).
3. **Misses are shown in the same place and size as finds.** The record leads with the totals, failures included.
4. **One orchestrated motion**: the gauge closing on the hero, once, and not at all under reduced motion. The
   replay moves only when the viewer presses play.
5. **Labels say what something is**, in plain words: "Found the documented cause", not "SUCCESS".

## Review against the brief: the defaults avoided

- No cream sheet with a terracotta accent. The sheet is cool, and the single accent is a highlighter tied to the
  gap's meaning.
- No dark page with one acid accent. Dark mode is a chosen night palette.
- No SaaS card grid with identical radii and shadows. Indexes are tables, and the case page is a document with
  sections.
- No all-caps eyebrows, no "A · B · C" meta strings, no "→" on links, and no monospace labels.
- No numbered 01/02/03 markers, except in "How it works", where the pipeline really is a sequence.
- No hero made of a big number, a small label and a gradient. The hero is a live measurement of a real case.

Changed after review: the first idea was a blueprint grid (cyan on navy). It read as generic "technical", so it was
replaced by the notebook sheet and highlighter, which come from what reviewers actually do with a paper.

## Code

TypeScript, strict, React 19 and Vite. `npm run check` type-checks and runs the tests; CI (`.github/workflows/web.yml`)
also builds the static site with its data and runs Lighthouse on it, failing under 95 for accessibility or 90 for best
practices.

```
src/types.ts        the JSON the site reads: manifest, run, report, events, scoreboard
src/api.ts          one data layer: /api/... from the server, data/*.json on the static site
src/data.ts         useShowcase (fetched once), useRun, gaugeOf
src/nav.ts          hash routes: href, parseHash
src/ui.tsx          formatting, verdict word and glyph, theme, tooltips
src/words.tsx       the vocabulary: v-names and standing, plain labels, the glossary and <Term>
src/replay.ts       the event fold, the stage timeline, the cached fold behind seeking
src/components/     Gauge, Hero, Record (version strips, planted chart), Replay, Report, Scoreboard
src/pages/          one file per page; every page but Home loads on first visit
src/test/           fixtures and setup; *.test.ts(x) sit beside what they test
```

Styles live in `src/styles.css` as tokens and classes. Inline styles are kept for computed values only: a tooltip's
position, a strip's count, the replay's progress.
