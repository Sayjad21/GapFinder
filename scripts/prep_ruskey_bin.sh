#!/usr/bin/env bash
# Run inside WSL: bundle the already-built RusKey driver for upload to Sandboxes.
# Compiling RocksDB inside a sandbox costs thousands of CPU-seconds (~$20-40 at the measured
# price), so the driver is built locally and uploaded: stripped binary + its non-system
# shared libraries + provenance (binary hash, fork commit, dirty flag).
set -euo pipefail
SRC=${1:-/root/ruskey}
OUT=${2:-/tmp/ruskey_bin}
rm -rf "$OUT" && mkdir -p "$OUT/driver" "$OUT/lib"
cp "$SRC/driver/ruskey_bench" "$OUT/driver/" && strip "$OUT/driver/ruskey_bench"
for lib in $(ldd "$OUT/driver/ruskey_bench" | awk '/=> \// {print $3}'); do
  case "$(basename "$lib")" in
    libc.so*|libm.so*|libpthread.so*|libdl.so*|librt.so*|ld-linux*|libgcc_s.so*|libstdc++.so*) ;;
    *) cp -L "$lib" "$OUT/lib/" ;;
  esac
done
dirty=$(cd "$SRC/rocksdb" && [ -z "$(git status --porcelain)" ] && echo false || echo true)
printf '{"binary_sha256": "%s", "rocksdb_commit": "%s", "rocksdb_dirty": %s, "built_on": "%s"}\n' \
  "$(sha256sum "$OUT/driver/ruskey_bench" | cut -d' ' -f1)" "$(cd "$SRC/rocksdb" && git rev-parse HEAD)" \
  "$dirty" "$(. /etc/os-release && echo "$PRETTY_NAME")" > "$OUT/provenance.json"
du -sh "$OUT"; cat "$OUT/provenance.json"
