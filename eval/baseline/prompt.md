<!-- The baseline task prompt, published word for word (fairness rule 2).
     {paper_excerpt}, {claims_table}, {naive_numbers}, {helper} and {budget}
     are filled identically for every arm. -->

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

## Paper's claims
{claims_table}

## The reproduction's numbers (naive run, artifact defaults)
{naive_numbers}

When you are done, write your final answer to `answer.json` in the working
directory, in this format, and then submit:
`{{"attributions": [{{"claim_id": "...", "knobs": {{"name": "value"}}, "evidence": "...", "gap_before": 0.0, "gap_after": 0.0}}], "unexplained": ["claim ids"]}}`
Claims you could not explain go in "unexplained".
