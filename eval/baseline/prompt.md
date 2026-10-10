<!-- The baseline task prompt, published word for word (fairness rule 2).
     {paper_excerpt}, {claims_table}, {naive_numbers}, {helper} and {budget}
     are filled identically for every arm.

     Change (P1-1 item 2): the baseline now also gets {repo_map}, the same repo-map text
     GapFinder's ledger step receives (`RepoMap.summary(max_files=300, max_flags=500)` from
     gapfinder/ingest/repo_map.py: build files, scripts, config files, every flag with its default
     and file:line, the file tree, the README start). Before, the baseline saw only the paper text,
     so a GapFinder win could come from the repo map rather than the method. -->

You are working in a sandbox. Your current working directory holds a research
artifact: its source code, already built, with its dataset already loaded.

A reproduction of the paper's experiments with this artifact gives numbers that
differ from the paper's. Your job is to **find out why**. Identify which
experimental condition (build options, configuration flags, workload, dataset,
environment) explains each difference, and show evidence for it.

Rules:
- Do not modify the algorithm's source code. Change only configuration,
  flags, workload, build options or environment.
- A benchmark helper is available: `{helper}`. Run it with `--help` for usage.
- Budget: {budget}.

## Paper excerpt (experimental setup)
{paper_excerpt}

## Repo map of the artifact (build files, scripts, config files, flags with defaults)
{repo_map}

## Paper's claims
{claims_table}

## The reproduction's numbers (naive run, artifact defaults)
{naive_numbers}

When you are done, write your final answer to `answer.json` in the working
directory, in this format, and then submit:
`{{"attributions": [{{"claim_id": "...", "knobs": {{"name": "value"}}, "evidence": "...", "gap_before": 0.0, "gap_after": 0.0}}], "unexplained": ["claim ids"]}}`
Claims you could not explain go in "unexplained".
