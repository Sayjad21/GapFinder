#!/usr/bin/env bash
# Run inside WSL: pack the RusKey sources (no build artifacts, no .git) for upload
# into a sandbox. Records the fork commit + dirty flag next to the tarball.
set -euo pipefail
SRC=${1:-/root/ruskey}
OUT=${2:-/tmp/ruskey_src.tar.gz}
tar -C "$SRC" \
  --exclude='.git' --exclude='*.o' --exclude='*.a' --exclude='*.d' --exclude='*.so*' \
  --exclude='__pycache__' --exclude='.venv' --exclude='java' --exclude='docs' \
  --exclude='driver/--skip_load' --exclude='*.sst' --exclude='*.blob' --exclude='MANIFEST-*' \
  -czf "$OUT" rocksdb driver lerp scripts
( cd "$SRC/rocksdb" && echo "{\"commit\": \"$(git rev-parse HEAD)\", \"dirty\": $([ -z "$(git status --porcelain)" ] && echo false || echo true)}" ) > "${OUT%.tar.gz}.json"
ls -la "$OUT"; cat "${OUT%.tar.gz}.json"
