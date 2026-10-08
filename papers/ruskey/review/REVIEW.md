# RusKey review sheet

Mark each row: put `x` in **OK** if it's right, or write the correction in **Fix**.
Then send the sheet back, or just the rows you changed.

## Part A: gold claims (my draft of the paper's checkable claims)

Check: is it really what the paper claims, is the number right, and should it be a headline claim?
Add any important claim I missed at the bottom.

| ID | Fig/Table | Page | Headline | Value | Quote (verbatim from the PDF) | OK | Fix |
|---|---|---|---|---|---|---|---|
| C1 | — | 1 | yes | 4.0 | achieving up to 4x better end-to-end performance than the RocksDB system under various settings | x |  |
| C2 | Figure 6 | 17 | yes | — | in the read-heavy workload (Figure 6 (a)), Aggressive is the most effective | x | Note: the PDF hyphenates 'read-/heavy' across a line break, so an exact string match fails unless the text is de-hyphenated. |
| C3 | Figure 6 | 17 | yes | — | Lerp selects an aggressive compaction policy with a read-heavy workload and a lazy compaction policy with a write-heavy workload | x |  |
| C4 | Figure 6 | 17 | yes | 4.0 | Lerp selects an intermediate policy K = 4 on the balanced workload, which dominates all baselines after around 600 missions | x |  |
| C5 | Figure 6 | 17 | yes | — | its performance is relatively better than the other two baselines on the balanced workload |  | Subject is Moderate: should say K=5 (Moderate) is the best baseline on balanced; 'its' alone is ambiguous. Fig. 6(c) agrees: K5 0.076 vs K1 0.102 and K10 0.113 ms (missions 1500-2000). |
| C6 | Figure 6 | 17 | no | 300.0 | it takes Lerp around 300 missions to explore and navigate to the optimal setting with the read-heavy and write-heavy workloads | x |  |
| C7 | Figure 6 | 17 | yes | — | the baselines perform sub-optimally on at least one workload | x |  |
| C8 | Table 3 | 18 | yes | 1.2 | it achieves a high average ranking of 1.2 | x |  |
| C9 | Figure 7 | 18 | yes | 4.0 | RusKey achieves up to 4 times better performance than Aggressive (on the write-heavy session) | x |  |
| C10 | Figure 7 | 18 | no | 2.4 | up to 2.4 times better performance than Moderate (on the read-heavy session) | x |  |
| C11 | Figure 7 | 18 | no | — | RusKey adopts compaction policy settings of K = 1, K = 5, K = 10, K = 6, K = 2 on the read-heavy, balanced, write-heavy, write-incline and read-inclined sessions, respectively | x |  |
| C12 | Figure 10 | 21 | no | 40.0 | the greedy transition, lazy transition and flexible transition use 51s, 44s, and 40s, respectively | x |  |
| (new) | Figure 6 | 17 | yes | — | The result shows that RusKey achieves near-optimal performance across all workloads. |  | Missing: the main Figure 6 claim (Part C C11). |
| (new) | Figure 7 | 18 | no | 3.5 | up to 3.5 times better performance than Lazy (on the read-heavy session) |  | Missing: third clause of the C9/C10 sentence. |

## Part B: gold assumptions (settings that could change the results)

Check the paper's value (or 'unstated'), the code default, and whether the setting really matters.
Add settings you know matter from your own debugging.

| ID | Setting | Paper says | Code default | Status | OK | Fix |
|---|---|---|---|---|---|---|
| A1 | `num_keys` | 100000000 | 100000000 | stated_matches |  | Driver default is 100M, but every final Fig. 6 run used 20M (wsl_tuner.sh:27, go20.sh:22), so status is stated_code_differs. Mattered most of all: at 6M keys (fits in RAM) read-heavy K=1 vs K=10 was flat (81.4 vs 81.4 us/op); the K trade-off appeared only at 20M (data > 16 GB RAM). |
| A2 | `rate_limit_mb` | unstated | 0 | unstated | x | Final runs leave it off. It mattered at 500K keys: 30 MB/s gave K=1 152.4 us/op with 3187 s of write stalls (RESULTS_LOG.md:1844); dropped once data reached 20 GB. |
| A3 | `direct_io` | true | false | stated_code_differs |  | Driver default is false, but all final runs pass --direct_io (run_experiments.py:259, wsl_monkey.sh, adapt_curve.py), so it effectively matches. Caveat: under WSL2, O_DIRECT doesn't bypass the host's cache (same run: read-heavy lookups 10.6 us vs write-heavy 394.8 us, RESULTS_LOG.md:2570). |
| A4 | `target_file_size_mb` | unstated | 64 | unstated |  | Driver default is 64 (ruskey_bench.cc:1275), but final runs use 8 MB (wsl_tuner.sh:71, wsl_monkey.sh) and older runs used 2 MB. Matters: GapFinder's own run moved K10/K5 from 0.87 to 2.74 at 64 MB. |
| A5 | `block_cache_mb` | unstated | 32 | unstated |  | Driver default is 32 (ruskey_bench.cc:151), but final runs use 256 (wsl_tuner.sh:28, go20.sh:22). Filter and index blocks sit outside the cache. The 32 -> 256 effect at 20 GB was never isolated. |
| A6 | `background_jobs` | unstated | 4 | unstated | x | Final runs use 4. An old 1/4/8 sweep (500K keys, pre-rewrite engine) didn't change the best K. |
| A7 | `zero_result_ratio` | unstated | 0.0 | unstated |  | Driver default is 0.0, but final runs use 1.0: every lookup misses (wsl_tuner.sh:29, go20.sh:22). Paper: unstated for the experiments, but its cost model analyses the zero-result case (p.13). Mattered: with hit lookups, read-heavy showed no K effect (commit 51c95df). |
| A8 | `propagate_during_learning` | false (other levels frozen while training, sec. 5.2.1) | true | stated_code_differs | x | Paper value confirmed (sec. 5.2.1: 'The compaction policies of other levels remain unchanged throughout this process'). But it is a no-op in the final runs: --mode cost (wsl_tuner.sh:73) bypasses Lerp; see the new tuner_mode row. |
| A9 | `greedy_critic` | false (DDPG actor) | true | stated_code_differs | x | No-op in the final runs (cost mode, not DDPG); see the new tuner_mode row. |
| A10 | `move_margin` | unstated (no such mechanism in the paper) | 0.4 | unstated | x | No-op in the final runs. It mattered earlier: 0.4 vetoed every move; 0.15 found and held K=10 (commit 805fb50). |
| A11 | `write_buffer` | 2 MB | 2 MiB | stated_matches | x |  |
| A12 | `bits_per_key` | 8 | 8.0 | stated_matches |  | The paper's Fig. 6 uses uniform 8 bits/key; Monkey with 4 bits/key is Fig. 8's setting (p.15, p.18). Final repro Fig. 6 runs used Monkey 4 bits/key (wsl_monkey.sh, run_experiments.py:117), so status is stated_code_differs. Mattered: write-heavy K=1 minus K=10 went from +7.4 (uniform) to +16.1 us/op (Monkey) (RESULTS_LOG.md:2464, 2527). |
| A13 | `ops_per_mission` | 50000 | 50000 | stated_matches |  | Driver default is 50000, but final runs used 40,000 (wsl_tuner.sh:70, adapt_curve.py:42, wsl_monkey.sh), so status is stated_code_differs. Effect not tested. |
| A14 | `host_memory_and_device` | 256GB DDR4, 1TB NVMe SSD, Xeon Gold 6326 | n/a (reproduction: 16 vCPU, 15 GB RAM, NVMe under WSL2) | stated_code_differs | x | Repro detail: WSL2 Ubuntu 24.04, 16 cores, 15 GB RAM (host 32 GB), ext4 on a virtual disk on NTFS. Mattered: the trade-off needs data larger than RAM, and host caching is the suspected reason balanced settles at K=10. |
| (new) | `missions` | 2000 (p.16) | final runs: 150 per fixed arm, 480 for the tuner | stated_code_differs |  | Mattered: on read-heavy the tuner averaged 23.2 us/op vs 10.1 for fixed K=1, because exploration isn't paid back within 480 missions (RESULTS_LOG.md:2620). |
| (new) | `tuner_mode` | Lerp (DDPG): tune Level 1, other levels unchanged, then propagate (sec. 5.2.1) | final runs: `--mode cost` (online-fitted cost model, settle 30, average 60), one K on every level (wsl_tuner.sh:73) | stated_code_differs |  | Mattered: on write-heavy DDPG chose K=4; the cost model chose K=10 (commit 3aed1be). |
| (new) | `flsm_sealed_run_merge` | p.16 (RocksDB version): sealed runs merge gradually through file compactions triggered by other runs; sec. 4.2: a full level merges all runs to the next level | rocksdb d36167568: a full level merges into the next level's active run | stated_code_differs (the paper itself gives two versions) |  | Mattered: before this rewrite the tuner trace was inverted on write-heavy (K=1 72.8 vs K=10 84.6 us/op, RESULTS_LOG.md:2189); K=1 write amp fell from 54.1 to 8.37. |
| (new) | `baseline_start_state` | bulk load into an empty DB; RusKey starts at leveling (p.16); the baselines' starting shape is unstated | one pristine tree bulk-loaded at K=1 (20.7 GB), copied for every arm (wsl_monkey.sh) | unstated |  | Effect not tested. |
| (new) | `wal_and_compression` | unstated | WAL off (ruskey_bench.cc:590), no compression (ruskey_bench.cc:296) | unstated |  | Effect not tested. |
| (new) | `key_value_size` | 128 B key, 896 B value (p.16) | 128 / 896 | stated_matches |  |  |

## Part C: claims GapFinder extracted by itself (48)

For each: is this a **real claim the paper makes about its own results**? Write `y` or `n` in **Real?**.
The plan needs at least 90% `y`. Don't fix wording; only judge real vs not.

| ID | Fig/Table | Page | Quote | Real? |
|---|---|---|---|---|
| C1 | — | 1 | Experiments show that RusKey exhibits strong performance robustness across diverse workloads, achieving up to 4x better end-to-end performance than the RocksDB system under various settings. | y |
| C2 | — | 4 | We demonstrate that RusKey achieves high performance in all the tested workloads. RusKey achieves up to 4x throughput compared with the baselines. | n |
| C3 | Figure 2 | 6 | Initially, the compaction policy is set as 1, and the capacity ratio is 10. The dynamic workload is write-heavy at first with 90% of updates and 10% of lookups. It then shifts into a read-write-balanced workload (50% of  | n |
| C4 | Figure 2 | 6 | At the beginning, RusKey tunes the compaction policy of the FLSM-tree from K=1 to K=10 to achieve the best write performance under write-heavy workloads | n |
| C5 | Figure 2 | 7 | Once the workload shifts to the balanced one, RusKey will re-tune the compaction policy of the FLSM-tree from K=10 to K=3, which is more effective in a balanced workload. | n |
| C6 | Figure 2 | 7 | Similarly, when the workload shifts to read-heavy, RusKey will adjust its compaction policy from K=3 to K=1 to achieve an optimized read efficiency. | n |
| C8a | Table 2 | 8 | Case Study 125 I/Os 3.75 I/Os 2.5 I/Os | y |
| C8b | Table 2 | 8 | Case Study 125 I/Os 3.75 I/Os 2.5 I/Os | y |
| C8c | Table 2 | 8 | Case Study 125 I/Os 3.75 I/Os 2.5 I/Os | y |
| C11 | Figure 6 | 17 | The result shows that RusKey achieves near-optimal performance across all workloads. | y |
| C12 | Figure 6 | 17 | In contrast, the baselines perform sub-optimally on at least one workload. | y |
| C13 | Figure 6(a) | 17 | For example, in the read-heavy workload (Figure 6 (a)), Aggressive is the most effective because it maintains a low read cost by merging sorted runs aggressively that promises low read amplification. | y |
| C14 | Figure 6(b) | 17 | However, its performance degrades with the write-heavy workload (Figure 6 (b)) because the aggressive merging incurs significant additional write amplification. | y |
| C15 | Figure 6 | 17 | Moderate achieves moderate performance on each of the workloads. | y |
| C16 | Figure 6 | 17 | It performs worse than aggressive policy on the read-heavy workload and worse than lazy policy on the write-heavy workload. | y |
| C17 | Figure 6(c) | 17 | Meanwhile, its performance is relatively better than the other two baselines on the balanced workload. | y |
| C18 | Figure 6(c) | 17 | Nevertheless, the end-to-end performance of moderate policy is still lower than RusKey on the balanced workload when RusKey finishes the tuning and reaches a sweet trade-off between lookups and updates. | y |
| C19 | Figure 6 (sub-figures) | 17 | Through tracking the tuning strategy of Lerp, we find that Lerp selects an aggressive compaction policy with a read-heavy workload and a lazy compaction policy with a write-heavy workload. | y |
| C20 | Figure 6(c) | 17 | In addition, as shown in Figure 6 (c), Lerp selects an intermediate policy K=4 on the balanced workload, which dominates all baselines after around 600 missions. | y |
| C21 | Figure 6 | 17 | Note that there are still minor gaps between RusKey and the respective optimal baselines on read-heavy and write-heavy workloads because RusKey requires a small number of missions to conduct the online training in order  | y |
| C22 | Figure 6 (sub-figures) | 17 | As shown in the upper sub-figures of Figure 6, it takes Lerp around 300 missions to explore and navigate to the optimal setting with the read-heavy and write-heavy workloads. | y |
| C23 | Figure 6(c) | 17 | Tuning on the balanced workload takes longer, which is around 600 missions. | y |
| C24 | Figure 7 | 17 | The workload is divided into five sessions with different proportions of lookups and updates. They are in the order of read-heavy (10% update), balanced (50% update), write-heavy (90% update), write-inclined (70% update) | n |
| C25 | Figure 7 | 18 | All baselines perform sub-optimally on at least one of the sessions. | y |
| C26 | Figure 7 | 18 | In the meantime, the latency of RusKey is close-to-optimal across all sessions, benefiting from a successful tuning through Lerp and FLSM-tree's ability to flexibly transform the compaction policy. | y |
| C28 | Figure 7 | 18 | Across all workload sessions, RusKey achieves up to 4 times better performance than Aggressive (on the write-heavy session), up to 2.4 times better performance than Moderate (on the read-heavy session), and up to 3.5 tim | y |
| C29 | Figure 7 | 18 | Note that in Figure 7, the latency of RusKey rises slightly at the beginning of each workload session and then drops rapidly. The reason behind this is that Lerp requires a short retraining under a new workload setting. | y |
| C30 | Table 3 | 18 | The result demonstrates that RusKey ranks first for four workloads and ranks second for the remaining one. Overall, it achieves a high average ranking of 1.2, demonstrating the strong robustness of RusKey. | y |
| C35 | Figure 8 | 19 | RusKey achieves near-optimal performance across various workloads under the Monkey scheme as well. | y |
| C36 | Figure 8 | 19 | Moreover, Lazy-Leveling also reaches near-optimal across all workloads, whereas RusKey performs better than Lazy-Leveling on every workload. | y |
| C37 | Figure 8 | 19 | Specifically, RusKey performs significantly better than Lazy-Leveling and other baselines on the balanced workload. | y |
| C38 | Figure 9 | 19 | The experiment is conducted on a workload of 25 million operations under the Monkey scheme after RusKey finishes self-tuning. | n |
| C39 | Figure 9 | 19 | Under this case, RusKey adopts different compaction policies at each level. It sets an aggressive policy at the first level. As the level goes deeper, the policy becomes lazier. | y |
| C40 | Figure 11(a-c) | 19 | As shown in Figure 11 (a), (b), and (c), the results on YCSB are quite similar in trends to the results on uniform workloads, if we set the composition of workloads the same as the previous experiments. | y |
| C41 | Figure 11 | 19 | These results further verify that RusKey delivers near-optimal performance across diverse workloads on the YCSB benchmark. | y |
| C42 | Figure 11(d) | 19 | Furthermore, we evaluate YCSB benchmark with a workload that contains 50% range lookups and 50% updates, and the results are shown in Figure 11 (d). Among all baselines, Aggressive achieves the lowest latency, and the pe | y |
| C43 | Figure 10 | 20 | We employ a read-write-balanced workload (50% lookups and 50% updates) of 120 missions, while each mission contains 1 million operations. Each level's initial compaction policy in the FLSM-tree is 1. The compaction polic | n |
| C44 | Figure 10(a) | 20 | Figure 10 (a) demonstrates that when a greedy transition occurs, it results in a very high write latency spike since changing the compaction policies at every level necessitates compacting all data in each level to the n | y |
| C45 | Figure 10(a) | 20 | With a greedy transition and a flexible transition, the write latency spikes brought on by compactions are significantly lower after the policy is changed. | y |
| C46 | Figure 10(a) | 20 | However, with a lazy transition, the height of spikes stays the same before and after the transition, which means that the compaction policies in larger levels still remain unchanged, because the transition is delayed un | y |
| C48 | Figure 10 | 21 | In terms of the end-to-end latency, the greedy transition, lazy transition and flexible transition use 51s, 44s, and 40s, respectively. | y |
| C49 | Figure 10 | 21 | In general, Figure 10 indicates that the flexible transition incurs almost-free immediate transition cost and has no delay, demonstrating its superiority. | y |
| C50 | Figure 12 (table) | 21 | The right table in Figure 12 summarizes the average performance ranking of all methods, similar to the setting of Table 3. Overall, RusKey achieves the highest average ranking, surpassing the best setting of a greedy app | y |
| C58 | Figure 13 | 22 | Our results show that the model update cost is insignificant compared with the total cost of processing the workload by the LSM-tree. For most workloads, the time spent on updating the model is at most 1% of the time for | y |
| C59 | Figure 13 | 22 | For example, on the balanced workload with the uniform Bloom filter scheme, the average query processing cost per mission is 3.36 seconds, while the average model update cost is only 0.019 seconds. | y |
| C60 | Figure 13 | 22 | For example, on the balanced workload with the uniform Bloom filter scheme, the average query processing cost per mission is 3.36 seconds, while the average model update cost is only 0.019 seconds. | y |
| C61 | — | 22 | We evaluated two brute-force training approaches: (1) without a level-based model that reduces the action space, and (2) without the policy propagation and train all levels. We limit the maximum experiment time to 24 hou | y |
| C62 | — | 22 | the flexible transition degenerates into lazy transition in an extreme read-only case since flexible transition only takes effect when there are updates. | n |
