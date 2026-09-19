#!/usr/bin/env sh
cd "$(dirname "$0")/.."
./run.sh --script start_scripts/nope.txt
echo "код возврата: $?"
