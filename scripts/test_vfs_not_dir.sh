#!/usr/bin/env sh
cd "$(dirname "$0")/.."
./run.sh --vfs vfs/minimal/readme.txt
echo "код возврата: $?"
