#!/usr/bin/env bash
set -euo pipefail

RPC="${GENLAYER_RPC:-https://studio.genlayer.com/api}"
CONTRACT="contracts/bullproof.py"

if ! command -v genlayer >/dev/null 2>&1; then
  echo "GenLayer CLI is not installed. Install with: npm install -g genlayer" >&2
  exit 1
fi

if [[ ! -f "$CONTRACT" ]]; then
  echo "Run this script from the repository root." >&2
  exit 1
fi

python scripts/preflight.py

echo "Using the currently selected GenLayer account."
echo "No password or private key is read from this repository."
genlayer account show --rpc "$RPC"

genlayer deploy --contract "$CONTRACT" --rpc "$RPC"
