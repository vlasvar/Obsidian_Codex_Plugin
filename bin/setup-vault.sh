#!/usr/bin/env sh
set -eu

VAULT_PATH="${1:?usage: setup-vault.sh <vault-path> [mode]}"
MODE="${2:-generic}"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PLUGIN_ROOT="$(dirname "$SCRIPT_DIR")"

python "$PLUGIN_ROOT/scripts/setup_vault.py" "$VAULT_PATH" --mode "$MODE"
