#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
exec uv run --quiet python src/shell_emulator/main.py "$@"
