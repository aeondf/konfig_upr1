#!/usr/bin/env sh
cd "$(dirname "$0")/.."
./run.sh --vfs /tmp/myfs --script start_scripts/stage2.txt
echo "код возврата: $?"
