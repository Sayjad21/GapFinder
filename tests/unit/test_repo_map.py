from gapfinder.ingest.repo_map import build_repo_map


def test_flags_from_usage_text_argparse_and_wrappers(tmp_path):
    (tmp_path / "driver").mkdir()
    (tmp_path / "driver" / "bench.cc").write_text(
        'void Usage() {\n'
        '  --num_keys N             entries to load (default 100000000)\n'
        '  --background_jobs N      default 4\n'
        '  --direct_io              open with direct I/O\n'
        '}\n'
    )
    (tmp_path / "tuner.py").write_text(
        'p.add_argument("--move_margin", type=float, default=0.4,\n'
        '               help="hysteresis")\n'
    )
    (tmp_path / "wrapper.py").write_text('p.add_argument("--direct_io", default=True)\n')
    rm = build_repo_map(tmp_path)
    get = lambda n: (rm.find_flag(n)[0].default, rm.find_flag(n)[0].ref)  # noqa: E731
    assert get("num_keys") == ("100000000", "driver/bench.cc:2")
    assert get("background_jobs") == ("4", "driver/bench.cc:3")
    assert get("direct_io") == ("false", "driver/bench.cc:4")  # the binary's switch beats the wrapper's default
    assert get("move_margin") == ("0.4", "tuner.py:1")  # multi-line add_argument


def test_relevant_files_prompt_is_identical_across_processes(tmp_path):
    """Set order varies with PYTHONHASHSEED; a reordered prompt misses the LLM cache and costs money."""
    import subprocess
    import sys

    for i in range(6):
        (tmp_path / f"s{i}.sh").write_text("echo hi\n")  # equal scores -> ties
    code = ("import sys; from gapfinder.ingest.repo_map import build_repo_map; "
            "from gapfinder.ledger.assumptions import relevant_files; "
            f"print(relevant_files(build_repo_map(r'{tmp_path}'), []))")
    outs = {subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                           env={**__import__('os').environ, "PYTHONHASHSEED": str(seed)}).stdout
            for seed in (1, 2, 3)}
    assert len(outs) == 1
