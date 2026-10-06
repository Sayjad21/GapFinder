#!/usr/bin/env bash
# Bulk-load the database once; the loaded state is the checkpoint every branch forks from.
set -euo pipefail
source "$(dirname "$0")/common.sh"
extra=()
[ "$sequential_load" = true ] && extra+=(--sequential_load)
rm -rf "$db"
"$bench" --db "$db" --load_only "${common[@]}" "${extra[@]}" > load.log 2>&1
du -sm "$db" | cut -f1 | sed 's/^/db_mb=/'
