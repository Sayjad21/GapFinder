# 1. What is GapFinder?

## The problem, as a story

Imagine a recipe book says: "this cake comes out 10 cm tall". You follow the recipe exactly, and your
cake is 6 cm. What went wrong?

Maybe the book forgot to say "preheat the oven", or used a different flour, or the oven temperature
was printed wrong. The recipe isn't lying. Something was **left out or changed**, and you have to find
what.

Research papers have the same problem.
- A paper reports a number: "our method gets 92% accuracy".
- The authors publish their code.
- You run the code, and you get 85%.

This happens all the time, and people call it a **reproduction gap**. The usual question is "does this
paper reproduce?", and the answer is usually just yes or no.

**GapFinder asks a more useful question: *why* doesn't it reproduce?**

## What GapFinder does, in one paragraph

You give GapFinder:
- the paper (a PDF);
- the paper's code;
- a short description of how to run that code.

GapFinder reads the paper and lists every result it claims, together with every setting the result might
depend on: number of training rounds, learning rate, data split, and so on. Then it runs the code many
times, each time changing one setting, to see which changes move the result toward the paper's number.
It checks its own answer carefully. In the end it writes a **Gap Report** that says, for each result,
either "this setting explains the gap, here is the proof", or honestly "we couldn't explain it, and here
is why".

## The running example: MC Dropout

The MC Dropout paper (2016) reports a number called Energy RMSE: **1.66** (smaller is better). When you
run the published code with its default settings, you get about **0.36**, very different.

Years later, the authors explained the difference:
- the paper used about **10 times fewer training rounds** than the code's default (`epochx=10` instead
  of 500);
- the paper used **1 hidden layer** instead of 2 (`hidden=1`);
- there were also differences **inside the code** that no setting can change, such as how the
  hyperparameters were tuned and the batch size.

So the right answer for this paper is: "two settings explain part of it, and the rest is in the code".
What does GapFinder say?

Version v1.3 said, in short:

> "Setting `epochx=10` and `hidden=1` makes the main number match the paper. But a second number from
> the paper (Yacht) then gets worse. No combination of settings matches both, so part of the cause is
> outside the settings: probably in the code, around these lines: `batch_size = 128` in `net/net.py`, and
> the per-split grid search in `experiment.py`."

That is very close to the authors' own explanation. Version 1.0 had simply said "Unexplained".
[The journey](07_the_journey.md) tells how it got there.

## What makes GapFinder different

1. **It runs real experiments.** It doesn't guess from reading. Every claim is backed by runs you can
   replay.
2. **It looks beyond the settings.** A gap can come from:
   - a setting;
   - how the paper chose which number to report;
   - an old library release;
   - a unit convention ("the paper's v is the code's 2 × v");
   - a small difference in the code or the data;
   - or none of these.
   GapFinder tests all six kinds and says which one fits.
3. **It's careful about being wrong.** A wrong answer stated confidently is worse than "I don't know". So
   GapFinder checks every answer three ways (see [design decisions](05_design_decisions.md)), and says
   "Unexplained" or "Inconclusive" when it should.
   - **On practice papers** (three sealed tests) it was confidently wrong **0 times in 90 runs**. A general
     coding agent given the same tasks was confidently wrong in 49 of those 90 runs.
   - **On real papers it is not that safe yet.** In the second blind real-paper test (GraphMAE) it was
     confidently wrong once. That led to new rules: a confident answer now needs a complete search and real
     evidence ([the journey](07_the_journey.md)).
4. **It saves time and money with "forks".** It sets up the experiment once, saves that moment like a save
   point in a video game, and starts every test from that save point instead of from scratch.

## Where it stands today (2026-10-24)

- **Real papers:** 1 correct, 1 partial, 5 missed and 1 confidently wrong out of 8 sealed blind papers. All
  were run before the latest work, so the current version has no blind result yet.
- **Planted gaps in papers that already reproduce:**
  - it mostly finds unit and scale conventions;
  - it finds settings about 3 times in 10 (most misses are ties on few numbers);
  - it rarely finds code defects.
- **Safety:**
  - every "nothing planted" control in every round was answered correctly;
  - the current version had no confident mistakes;
  - a newer version (c6) made two and was not adopted.
- **Compared with the state of the art:** nobody has published a tool for this exact task, so there is
  nothing to beat head to head. [Page 11](11_versus_the_state_of_the_art.md) explains what is known.

## Who is it for?

- **Researchers** checking whether a result holds, and why not.
- **Reviewers and reproducibility volunteers** who want evidence, not opinions.
- **Authors**, to find the sentence their methods section is missing. GapFinder can even draft it.

Next: [Using GapFinder →](02_using_gapfinder.md)
