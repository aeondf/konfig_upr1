#!/usr/bin/env sh
cd "$(dirname "$0")/.."
./run.sh --vfs vfs/minimal --script start_scripts/stage5.txt
echo "код возврата: $?"
