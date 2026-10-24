# Learning GapFinder: start here

These pages explain GapFinder from the beginning, in plain words: what it does, how every part works, why it
is built this way, where each idea came from, how it is tested, how it compares with the state of the art,
and what is still missing. You don't need to know anything about the project to start. Read them in order;
each takes about 5-15 minutes. Updated 2026-10-24.

| # | Page | You will learn |
|---|---|---|
| 1 | [What is GapFinder?](01_what_is_gapfinder.md) | the problem it solves, with a simple story, and where it stands today |
| 2 | [Using GapFinder](02_using_gapfinder.md) | how to run it, what you give it, what you get back, how to read the report |
| 3 | [The big picture](03_architecture_overview.md) | the main parts of the current version and how data flows between them |
| 4 | [Inside each part](04_components_deep_dive.md) | what every component does and how, including the parts that are switched off |
| 5 | [Why it's built this way](05_design_decisions.md) | every important choice, where it came from, the evidence, and what we chose not to do |
| 6 | [How we test it](06_how_we_test_it.md) | GapBench, the dev suite, real papers, the planted-gap curriculum, every round, and how to read the numbers |
| 7 | [The journey](07_the_journey.md) | how the project grew, version by version, including the versions that failed |
| 8 | [Limits and what's next](08_limits_and_next.md) | what it can't do yet, and the plan |
| 9 | [Glossary](09_glossary.md) | every special word, explained in one or two lines |
| 10 | [Where the ideas came from](10_where_the_ideas_came_from.md) | every technique: published, from another field, or ours; on or off; did it help |
| 11 | [Compared with the state of the art](11_versus_the_state_of_the_art.md) | what exists, what was measured head to head, what is genuinely new, and the honest verdict |

**If you have 20 minutes:** read pages 1, 11 and 8.

**If you want to understand the design:** read pages 3, 5 and 10.

**One example runs through the early pages:** the MC Dropout paper (Gal and Ghahramani, 2016). Its code
gives different numbers from the paper, and we know why, because the authors later explained it.

If a word is new to you, look it up in the [glossary](09_glossary.md). For the full technical record, read
`docs/CONTEXT_v11.md`.
