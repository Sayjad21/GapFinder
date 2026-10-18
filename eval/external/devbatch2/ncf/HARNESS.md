# devbatch-2 case ncf: harness

Paper: He, Liao, Zhang, Nie, Hu, Chua, "Neural Collaborative Filtering", WWW 2017.
Code: hexiangnan/neural_collaborative_filtering at `4aab159e81c44b062c091bdaed0ab54ac632371f` (Keras 1.0.7,
Theano 0.8.0, Python 2.7 per the README). Scope: MovieLens-1M (`Data/ml-1m.*`, shipped) only; Pinterest is
left out.

## Image: hand-built (the automatic image failed)

Stage 1's image (`env_build.json`: python:3.7-slim, checkpoint `9f6c3874-e551-46d2-bd07-d5654dd92bae`) loads
every import but cannot run the experiment. Measured on that checkpoint (`python NeuMF.py --epochs 1 --out 0`):

```
File "NeuMF.py", line 89, in get_model
    mlp_user_latent = Flatten()(MLP_Embedding_User(user_input))
  ...
TypeError: 'float' object cannot be interpreted as an integer
```

The code is Python 2: `output_dim = layers[0]/2` is a float under Python 3, and past that the scripts use
`xrange` and `dict.has_key`. So the import check passed and the run fails: the builder's "ok" was not usable.

Hand-built instead (`case.json`, `eval/external/devset/build_case.py`): `python:2.7` (Debian buster, has g++
for Theano's C ops and curl), pip `numpy==1.11.0` (the repo's Dockerfile pin), `scipy==0.17.1` (contemporary
cp27 wheel; not pinned by the repo), `Theano==0.8.0`, `keras==1.0.7` (README and Dockerfile), `h5py==2.6.0`
(Dockerfile installs it unpinned). Keras backend set to theano (`KERAS_BACKEND=theano`, as the Dockerfile
does); Theano floatX float32 (Keras default), no BLAS ldflags (numpy's BLAS). build_case.py's own fetch
uses Python 3's `urllib.request` and fails on Python 2, so `setup` fetches the same codeload tarball at the
commit with curl (the md5 of the three ml-1m files is printed in the build log). Checkpoint:
`86fb8606-fb43-451a-9e95-99b4ca256af0`.

## Claims (all ML-1M, predictive factors 8)

| Claim | Metric | Paper | Where in the paper | Role |
|---|---|---|---|---|
| NeuMF HR@10 | `neumf_hr` | 0.688 | Table 2, MovieLens, factors 8, "Without Pre-training" | target |
| NeuMF NDCG@10 | `neumf_ndcg` | 0.410 | Table 2, same row | held-out |
| MLP HR@10 | `mlp_hr` | 0.671 | Table 3, MovieLens, factors 8, MLP-3 | held-out, tuned separately |
| MLP NDCG@10 | `mlp_ndcg` | 0.399 | Table 4, MovieLens, factors 8, MLP-3 | held-out, tuned separately |
| GMF HR@10 | `gmf_hr` | 0.642 | Figure 4a, factors 8 (read from the plot, about +-0.003) | held-out, tuned separately |
| GMF NDCG@10 | `gmf_ndcg` | 0.371 | Figure 4b, factors 8 (read from the plot, about +-0.003) | held-out, tuned separately |

- Factor size 8: Section 4.1 "Parameter Settings": "evaluated the factors of [8, 16, 32, 64]" and "if the
  size of predictive factors is 8, then the architecture of the neural CF layers is 32 -> 16 -> 8, and the
  embedding size is 16". The README's commands use `--num_factors 8 --layers [64,32,16,8]` (code default).
- Why "without pre-training": the README's naive NeuMF command is "Run NeuMF (without pre-training)", the
  code default (`--mf_pretrain ''`). Table 2 gives both columns; Figure 4's NeuMF point at 8 reads 0.684 /
  0.403, which is Table 2's *with* pre-training column, so the target is taken from Table 2's other column.
- MLP-3 = "the MLP method with three hidden layers (besides the embedding layer)" (Section 4.4); the code's
  `[64,32,16,8]` has three hidden Dense layers (32, 16, 8). The Figure 4 MLP point at 8 reads 0.671 / 0.400,
  matching Tables 3/4 (this is also how the plot reading of GMF was calibrated).
- Units: fractions, as the paper prints them and as the scripts print them.

### Tuned separately (rule 5)

NeuMF NDCG@10 comes from the same run and the same model as the target: one setting must fit both
(`tuned_separately` false). GMF and MLP are different models whose hyper-parameters the paper tuned on a
validation split per NCF method; it never says one setting is shared:

> "To determine hyper-parameters of NCF methods, we randomly sampled one interaction for each user as the
> validation data and tuned hyper-parameters on it." ... "We tested the batch size of [128, 256, 512, 1024],
> and the learning rate of [0.0001 ,0.0005, 0.001, 0.005]." (Section 4.1, Parameter Settings)

So the four GMF/MLP claims are `"tuned_separately": true`.

## What a run does, and what it reports

One cell runs the README's three ml-1m commands at once (three processes on the 4 vCPUs,
`OPENBLAS_NUM_THREADS=1`): `NeuMF.py` (without pre-training), `GMF.py`, `MLP.py`, each to `out/<model>.log`.
`harness/emit.sh` reports what each script prints as its result, its last line
`End. Best Iteration i:  HR = x, NDCG = y.` -> `<model>_hr`, `<model>_ndcg`, `<model>_best_iter`; and, as extra
metrics, the `Init:` line and every logged epoch (`<model>_hr_e<k>`, `_ndcg_e<k>`, `_loss_e<k>`, k = 0..19
in the spec's metric list). No other evaluation is computed. `wall_s` is printed too.

## Knobs (ncf.yaml)

Every argparse flag of NeuMF.py, GMF.py and MLP.py that defines training or evaluation, default = the
code's own value:

| Knob | Default | Flag(s) |
|---|---|---|
| epochs | 20 (README; argparse default 100, see deviations) | all three `--epochs`; max 70 |
| batch_size | 256 | all three |
| num_neg | 4 | all three; max 8 (memory, below) |
| lr | 0.001 | all three |
| learner | adam (choices from the help text: adagrad, adam, rmsprop, sgd; anything else runs SGD) | all three |
| verbose | 1 | all three; it is the evaluation interval ("Show performance per X iterations"), and only evaluated epochs can be the reported best, so it shapes the result |
| num_factors | 8 | NeuMF and GMF `--num_factors` |
| layers | 64,32,16,8 | NeuMF and MLP `--layers` (wrapped as `[..]`) |
| reg_mf | 0 | NeuMF |
| reg_layers | 0,0,0,0 | NeuMF and MLP (wrapped as `[..]`) |
| regs | 0,0 | GMF (wrapped as `[..]`) |
| mf_pretrain, mlp_pretrain | "" (none) | NeuMF; passed only when non-empty |

Left out, and why: `--path` and `--dataset` (which data; the claims are ml-1m), `--out` (only whether the
weights are saved, into `Pretrain/`; set to 0 so a run writes only `out/`). `topK = 10` and
`evaluation_threads = 1` are constants in the scripts, not flags.

Seeds: the code sets none (numpy-based Keras init, numpy negative sampling, Keras shuffle). Every run's
noise is the code's own randomness; RUN_TAG is not used.

## Deviations

- Image hand-built (above); the automatic one fails on Python 2 syntax.
- `epochs` default 20, not argparse's 100: the README's commands for this experiment (all three models) say
  `--epochs 20`, and the brief's naive run is what the README says to run. The paper states no epoch count
  for Table 2 (Figure 6 plots 50 iterations). Not a scale-down to fit: full data, README command; so no
  `discrepancy` is set. 100 epochs does not fit one 3500 s run with three models in parallel (about 40 s an
  epoch), hence `max: 70`: larger values are reported as untestable, not run.
- `num_neg` max 8: the three processes hold the sampled instances as Python lists; summed RSS is 2.4 GB
  at 4, 3.4 GB at 8, and at 10 (and 20) the processes are killed for memory on the 3.9 GB VM. Paper
  Figure 7 sweeps 1..10 negatives; 9 and 10 can't be tested in this harness.
- Keras 1.0.7 writes `~/.keras/keras.json` on first import; three processes importing at once raced
  (one died with "No JSON object could be decoded"), so the command imports keras once first.
- List-valued knobs are written without brackets (`64,32,16,8`) because a knob value may not contain `[ ]`;
  the command adds them. Ledger candidates spelled with brackets are skipped by the engine as
  unrenderable (a format mismatch, recorded here; not changed).
- The three models share a cell and the shared knobs; the GMF/MLP claims are only reported (tuned
  separately).
- `OPENBLAS_NUM_THREADS=1` / `OMP_NUM_THREADS=1` so three processes don't oversubscribe 4 vCPUs (speed only).

## Smoke runs (Sandboxes)

Checkpoint `86fb8606-fb43-451a-9e95-99b4ca256af0` (python:2.7, pins above).

| Run | Wall | Peak RSS | NeuMF HR / NDCG (best iter) | GMF HR / NDCG (best iter) | MLP HR / NDCG (best iter) |
|---|---|---|---|---|---|
| defaults (20 epochs) | 891 s | 1.02 GB max process | 0.6818 / 0.4072 (14) | 0.6359 / 0.3672 (15) | 0.6700 / 0.3945 (17) |
| paper | | | 0.688 / 0.410 | 0.642 / 0.371 (plot) | 0.671 / 0.399 |

Further probes (2 epochs each, for cost only): num_neg 4: 138 s, summed RSS 2.44 GB; num_neg 8: 188 s,
3.42 GB; num_neg 10: all three killed (3.89 GB summed when last sampled); num_neg 20: killed. Per epoch with
three processes: NeuMF about 40 s, MLP 36 s, GMF 14 s, evaluation 1.5 s; start-up (data load, Theano
compile, init evaluation) about 50 s.

Note on the reported number: each script's "End. Best Iteration" line is the best epoch over the run (the
script keeps the epoch with the highest HR); the harness reports that line, as the code does.

## Search (added after it ran)

`gapfinder search`, frozen tag devbatch-2, `--max-runs 100 --concurrency 8`, output in `run/`. It stopped after
the 5 naive repeats: C_neumf_hr "Reproduced" (naive median 0.6825, gap -0.8%, noise band +-1.0%). No screen
was run, so no history matching, no leads and no paper-vs-code differences were produced. case.json's smoke
gained the `import keras` pre-step after the image was built (the image is unchanged).
