# Shared by load.sh and fig6_cell.sh: parse key=value args into driver flags.
# Every knob has a default equal to the driver's own default, so an unset knob
# means "what the artifact does out of the box".
for kv in "$@"; do declare "${kv%%=*}=${kv#*=}"; done
# the prebuilt driver ships its non-system libraries in /work/lib
export LD_LIBRARY_PATH="/work/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
: "${bench:=/work/driver/ruskey_bench}" "${db:=/work/db}"
: "${num_keys:=2000000}" "${key_size:=128}" "${value_size:=896}" "${sequential_load:=false}"
: "${logical_levels:=6}" "${size_ratio:=10}" "${write_buffer:=2097152}" "${target_file_size_mb:=64}"
: "${bits_per_key:=8}" "${monkey:=false}" "${direct_io:=false}" "${background_jobs:=4}"
: "${rate_limit_mb:=0}" "${block_cache_mb:=32}" "${zero_result_ratio:=0.0}" "${seed:=42}"
common=(--num_keys "$num_keys" --key_size "$key_size" --value_size "$value_size"
        --logical_levels "$logical_levels" --size_ratio "$size_ratio" --write_buffer "$write_buffer"
        --target_file_size_mb "$target_file_size_mb" --bits_per_key "$bits_per_key"
        --background_jobs "$background_jobs" --block_cache_mb "$block_cache_mb" --seed "$seed")
[ "$direct_io" = true ] && common+=(--direct_io)
[ "$monkey" = true ] && common+=(--monkey)
[ "$rate_limit_mb" != 0 ] && common+=(--rate_limit_mb "$rate_limit_mb")
true
