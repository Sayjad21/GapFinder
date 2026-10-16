# blind-1 harness: how FastGCN is run, and every deviation

Written by the runner after GapFinder was frozen at tag `blind-1` (`b433ae0`) and the sealer had committed
`case.md` and the answer-key hash (`485c080`), and before the reveal. The runner has not seen the answer
key and has read no reproduction report about FastGCN.

## Roles and what each one saw

- **Sealer:** a separate model (Claude Sonnet, a subagent with its own context). It chose the paper from
  web sources, wrote `answer_key.md` outside the repository and hashed it. Its hand-back message to the
  runner gave the paper, the repo and commit, the targets, the hash and practical facts. Those facts
  included a few neutral observations that the runner then knew before the run: the seed, the sample
  size and the mini-batch size are hard-coded in the scripts, and at the default flags the transductive
  Cora accuracy over 10 seeds averaged about 0.797 while the other three rows landed near their paper
  values.
- **Runner:** the GapFinder builder (Claude Opus, this session). It wrote this harness, the spec and
  the targets, and ran GapFinder.
- **Caveat:** both roles are AI models directed by the same user, and the sealer is not a person. The
  key was never in the runner's context, but this is weaker separation than a human sealer.

## Image (Token Factory Sandboxes)

Built by `build.py` (kept in the run notes):
1. `python:3.7-slim`, with this folder's `harness/` uploaded to `/work/gf_harness/`.
2. The repo fetched inside the sandbox from
   `https://codeload.github.com/matenure/FastGCN/tar.gz/b8e6e6412d8cb696e0adb7910832ed1ae7243ac9` into
   `/work`. An upload of the local clone timed out on the 7.5 MB `ind.pubmed.allx`, an infrastructure
   failure.
3. `pip install tensorflow==1.15.5 numpy==1.18.5 scipy==1.4.1 networkx==2.4 protobuf==3.20.3`. The repo
   has no requirements file. This is the last TensorFlow 1.x release, so the code runs unmodified:
   `tf.app.flags`, `tf.set_random_seed` and `scipy.sparse.linalg.eigen.arpack` all exist.
4. `harness/gf_seed_hook.py` and `gf_seed.pth` are copied into site-packages.

**No repository file is changed.**

## The run cell

One branch runs the four FastGCN rows of Table 5 at once: `pubmed-original_transductive_FastGCN.py` and
`pubmed-original_inductive_FastGCN.py`, each with `--dataset cora` and `--dataset pubmed`, as four
parallel processes on the VM's 4 cores. `harness/emit.sh` reads each script's final "accuracy=" line and
prints `trans_cora_acc`, `trans_pubmed_acc`, `ind_cora_acc` and `ind_pubmed_acc`.

The accuracy on these single-label datasets equals the micro-F1 the table reports.

The scripts run as they ship. The sample size (`main(400)` transductive, `main(100)` inductive) and the
batch size (20) are what the code does, and are not knobs.

## Knobs

All nine `tf.app.flags` the two scripts define, with the code's defaults: `model`, `learning_rate`,
`epochs`, `hidden1`, `dropout`, `weight_decay`, `early_stopping` and `max_degree` (eight knobs), plus
`dataset`.
- `dataset` is fixed per metric instead, because each claim names its dataset.
- The only bound is `epochs` max 2000 (20 × the default), a cost cap fixed before any run.

**GapFinder's repo map found none of these flags.** It reads argparse and C++ gflags
(`DEFINE_int32(name, …)`), not Python `flags.DEFINE_string('name', …)` with a quoted name. GapFinder is
frozen, so the knobs were written into the spec by hand: every flag, nothing selected. This is a
finding of the blind case. The ledger's assumption step saw a repo map without flags.

## Noise between repeats

The scripts fix `seed = 123` for numpy and TensorFlow, so repeats of one configuration would be identical
and the noise band zero.
- `gf_seed_hook` (site-packages, enabled by `GF_SEED_FROM_RUN_TAG=1` in the run command) adds
  `crc32(RUN_TAG) % 100000` to the seed passed to `np.random.seed` and `tf.set_random_seed`.
- GapFinder gives every run a fresh `RUN_TAG`, so every run, including the default-setting calibration
  runs, uses a different seed. Seed 123 itself is never run.
- This is variation of the kind real reruns have; it is not a knob.

## Search

`gapfinder search` at tag `blind-1`, as for MC Dropout v1.3:
- Sandboxes backend;
- `--max-runs 200`, stated before the run;
- defaults for everything else.

The run is committed unchanged before the reveal.
