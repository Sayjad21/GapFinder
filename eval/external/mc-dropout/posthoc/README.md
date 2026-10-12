# Post-hoc diagnostic: the documented hypothesis put into the search

**This is not blind and not part of the pre-registered evaluation.** It was run after the answer
key was revealed, with the key's answer written into the hypothesis set by hand. It does not change
any arm's score or label in [../RESULT.md](../RESULT.md). Its only purpose is to show how
GapFinder's own verification judges the documented cause once the search is able to test it.

## Why it is post-hoc

All four pre-registered arms ended Unexplained because `epochx=10` was never a candidate (the
ledger arms proposed `epochx` of 1000 or more, the random arm's lowest value was 250). Here we
supplied `epochx=10` and `hidden=1` ourselves, knowing from the answer key that they close the
Energy gap. A result from a hypothesis list built after reading the key cannot say anything about
whether GapFinder would find the cause unaided. It can only say what the verification step does
with it.

## What was changed

[assumptions.json](assumptions.json) is a copy of the normal arm's ledger
([../ledgers/normal/assumptions.json](../ledgers/normal/assumptions.json)). Two entries differ, and
nothing else (checked field by field against the original):

| Entry | Normal ledger | This diagnostic |
|---|---|---|
| A2 `--epochx` | `paper_value` "unstated", candidates 500, 1000, 2000 | `paper_value` "10", candidates **10**, 500, 1000, 2000; status `stated_code_differs`; added paper evidence (p.6) with the quote "we used 10x more iterations" |
| A3 `--hidden` | `paper_value` "unstated", candidates 4, 5, 2 | `paper_value` `1 (authors' README: "10x epochs one layer")`, candidates **1**, 4, 5, 2; status `stated_code_differs`; added code evidence `readme.md:8` with the quote `run the previous "10x epochs one layer" code` |

The paper itself never says "one hidden layer" (p.6 only gives "50 units"), so the README quote is
the strongest backing the value has. Because of those two edits GapFinder's plausibility check
passes both values ("paper states ..."), and the evidence gate has nothing to look up. A diagnostic
where the values were unsupported would have ended differently for a reason unrelated to the
question asked here. The two evidence quotes were added by hand and were not run through the
ledger's grounding checker (the paper quote is verbatim in the ICML PDF text; the README line is in
`runs/mcd-repo/readme.md`).

Everything else is the pre-registered setup: same spec ([../mcd_sandbox.yaml](../mcd_sandbox.yaml)),
targets ([../targets_mcd.json](../targets_mcd.json); Energy RMSE 1.66 is the target, Yacht RMSE 1.11 is
held out), claims file (the normal ledger's), checkpoint, `--max-runs 40 --candidates-per-knob 2
--cap 0.5`, evidence gate on, ledger ranking, no code or prompt change. Command (with
`GF_MCD_SANDBOX_BASE` set to the `gf/mcd/base-v2` checkpoint, `GF_SANDBOX_GUARD_USD=20000`,
`GF_SANDBOX_CPU_LIMIT_S=60000`, `GF_MAX_CONCURRENCY=24`, `GF_SPEND_TAG=mcd-posthoc`):

```
gapfinder search --spec eval/external/mc-dropout/mcd_sandbox.yaml \
  --targets eval/external/mc-dropout/targets_mcd.json \
  --assumptions eval/external/mc-dropout/posthoc/assumptions.json \
  --claims eval/external/mc-dropout/ledgers/normal/claim_ledger.json \
  --backend contree --max-runs 40 --candidates-per-knob 2 --cap 0.5 \
  --out eval/external/mc-dropout/posthoc/run
```

Outputs: [run/gap_report.md](run/gap_report.md), [run/gap_report.json](run/gap_report.json),
[run/events.jsonl](run/events.jsonl), [search.log](search.log). Cost: 30 branch runs, Nemotron
billed $0.0000 (no triage or evidence call was needed), Sandboxes reported $733.06 (diagnostic, not
billed in the Beta). Wall time about 69 minutes.

## What GapFinder did

**Label: Unexplained** for C_energy_rmse (gap -76.7% before, -76.7% after; "5 hypotheses tested").

The search tested the documented values directly. Medians over 5 runs each (split draws differ
between configurations, so single-run values scatter, Yacht especially):

| Configuration | Energy RMSE (paper 1.66) | Energy gap | Yacht RMSE (paper 1.11, held out) | Yacht gap |
|---|---|---|---|---|
| naive (`epochx=500`, `hidden=2`) | 0.387 | -76.7% | 1.041 | -6.2% |
| `epochx=10` | 0.573 | -65.5% | 1.484 | +33.7% |
| `hidden=1` | 0.440 | -73.8% | 0.594 | -46.5% |
| **`epochx=10`, `hidden=1`** | **1.723** | **+3.8%** | **1.987** | **+79.0%** |
| `epochx=1000` | 0.359 | -78.4% | 0.772 | -30.4% |
| `hidden=4` | 0.365 | -78.0% | 0.708 | -36.2% |

The rounds in `events.jsonl`: the screen kept all four single-knob values as survivors (`epochx=10`
3.97 noise units, `hidden=1` 1.01, `epochx=1000` -0.59, `hidden=4` -0.85); the confirm round kept two
(`epochx=10` and `hidden=1`); the combine round tried the pair and kept it. Verification then
judged the pair, and each single knob, and returned for all three: `plausible: true`,
`counterfactual_ok: true`, `held_out_ok: false`, label Unexplained.

From the gap report:

> {'epochx': '10', 'hidden': '1'} closes this claim but makes held-out claims worse; rejected
>
> closest configuration tried: {'epochx': '10', 'hidden': '1'} (gap +3.8%); it did not pass verification

> Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochx=10` (3.97 noise units, gap -65.5%); `hidden=1` (1.01 noise units, gap -73.8%)
>
> `epochx=10`, `hidden=1`: this claim +3.8%, mean |gap| 41.4% (5 runs)

The "closest configurations" table lists the pair at Energy +3.8% and Yacht +79.0%. Its mean absolute
gap, 41.4%, ties with the naive run's (-76.7% and -6.2%), so by that measure the documented setting
is no closer to the paper than the defaults.

How to read it. GapFinder's verification found the cause on Energy and reported it as the closest
configuration, with the right numbers (Energy 1.723 against 1.66, in line with the
[confirmation runs](../RESULT.md), 1.716). It refused to name it as the explanation because the
held-out check failed: Yacht moved from 6% below the paper to 79% above it, far outside Yacht's
noise band (+-0.10 here). The rule is `held_out_ok = |gap_after| <= |gap_before| + band`, and
0.79 is not below 0.062 + 0.098. The other checks passed: the values were backed by the paper and
the README, and removing either knob reopened the gap. So with the hypothesis in the set, the
product's behaviour is: confirm the Energy effect, flag the Yacht regression, abstain, and point at
the right setting as "closest configuration". That matches what the main result predicted
("Unexplained, with the closest configuration reported"). The limit, also noted there, is that
the held-out guard cannot tell "a cause that over-explains one dataset" from "a wrong cause".

## Why Yacht's paper value is probably not reachable by any setting

The authors' README (`runs/mcd-repo/readme.md`, "Update (2018)") says the paper-era code did not
tune hyperparameters the way the current code does:

> We replaced the Bayesian optimisation implementation (which was used to find hypers) with a
> grid-search over the hypers. This is following feedback from @capybaralet who spotted test-set
> contamination (some train-set points, used to tune hypers which were shared across all splits,
> were used as test-set points in later splits). The new implementation iterates over the 20
> splits, and for each train-test split it creates a _new_ train-val split to tune hypers. These
> hypers are discarded between different train-test splits.

So the paper's Table 1 numbers came from hyperparameters (dropout rate, tau) tuned once, by
Bayesian optimisation, and shared across all splits, so train points used for tuning were test
points in later splits. That makes the reported test error optimistic in a way that depends on
the code's tuning procedure, not on a setting. The repository's current code has no such path (it
re-tunes per split by grid search), so no `--epochx`, `--hidden` or data-file setting can reproduce
the contamination. The paper also used mini-batches of 32 where the code hard-codes 128
([../answer_key.md](../answer_key.md), section 2). This is a probable explanation, not a tested
one: we did not rebuild the paper-era Bayesian-optimisation code. It fits the observation that the
documented pair matches Energy but overshoots the small Yacht set (308 rows), which we have no
other account for.

## Caveats

- One search, one seed, 5 runs per configuration. Yacht RMSE is very noisy under this split scheme
  (the pair's five Yacht runs range from 1.89 to 3.55; the confirmation runs' median was 2.996
  against 1.987 here), so the +79% is a point estimate, but every run of the pair was above 1.8
  against the paper's 1.11.
- The hypothesis set was written after the key was revealed, and the evidence entries were
  chosen so the values pass the plausibility check. Do not cite this as GapFinder finding the
  cause. The pre-registered result is 0 of 4 arms.
