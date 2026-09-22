#!/usr/bin/env sh
cd "$(dirname "$0")/.."
./run.sh --vfs vfs/nope
echo "код возврата: $?"
