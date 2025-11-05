#!/usr/bin/env bash
set -euo pipefail

# Simple wrapper to run your PKMS CLI with JSON storage.
# Usage examples:
#   ./scripts/pkms.sh ?
#   ./scripts/pkms.sh add "Write README" --priority high --due 2025-11-10 --tag docs --note "Initial draft"
#   ./scripts/pkms.sh list
#   ./scripts/pkms.sh done 1
#   ./scripts/pkms.sh delete 1
#   ./scripts/pkms.sh search docs
#   ./scripts/pkms.sh suggest
#   ./scripts/pkms.sh weekly-summary

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
JSON_PATH="${JSON_PATH:-$ROOT_DIR/demo_tasks.json}"

if [[ "${1:-}" == "?" || "${1:-}" == "help" || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  cat <<'USAGE'
PKMS CLI (wrapper)

Commands:
  add <title> [--priority low|normal|high|urgent] [--due YYYY-MM-DD] [--tag TAG ...] [--note NOTE]
  list [--all]
  done <id>
  delete <id>
  search <keyword>
  prioritize
  suggest
  weekly-summary

Examples:
  ./scripts/pkms.sh add "Write README" --priority high --due 2025-11-10 --tag docs --note "Initial draft"
  ./scripts/pkms.sh list
  ./scripts/pkms.sh done 1
  ./scripts/pkms.sh delete 1
  ./scripts/pkms.sh search docs
  ./scripts/pkms.sh suggest
USAGE
  exit 0
fi

exec python3 "$ROOT_DIR/main.py" --storage json --json-path "$JSON_PATH" "$@"
