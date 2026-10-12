# MC Dropout attempt 2 (local Docker, after Deviation 1)

- **run-normal:** complete. 26 branch runs (25 succeeded, 1 timed out: the hidden=5 + epochx=2000
  combination). Verdict for C_energy_rmse: **Unexplained**. No tested change moved Energy RMSE by more
  than 1 noise band (naive 0.369, band ±0.057, paper 1.66).
- **run-evidence-off:** stopped by the team partway through the confirm round, about 23 branch runs.
  No verdict.
- Arms 3-4 were started on a teammate's laptop and stopped there (too slow); their outputs aren't
  kept here.

The team then moved all four arms to Token Factory Sandboxes, after checking in the Nebius billing
console that Sandboxes usage isn't billed during the Beta (see FROZEN.md, Deviation 2).

- **run-no-README-stray, run-all-flags-random-stray:** the local runner started these by accident after it
  was asked to stop (arm 3 at 15:22, then arm 4), and they were killed during calibration. No verdict.
