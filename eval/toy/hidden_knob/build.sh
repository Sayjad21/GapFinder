#!/usr/bin/env bash
# "Build": records the build mode; release is 3x faster than debug.
set -e
mkdir -p build
echo "${1:-debug}" > build/mode.txt
