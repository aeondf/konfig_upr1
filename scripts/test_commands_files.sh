#!/usr/bin/env sh
cd "$(dirname "$0")/.."
./run.sh --vfs vfs/files --script start_scripts/stage4.txt
echo "код возврата: $?"
