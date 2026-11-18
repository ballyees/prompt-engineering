#!/usr/bin/env bash
set -euo pipefail

BASE_URL="https://raw.githubusercontent.com/ballyees/prompt-engineering/refs/heads/main/agent-templates"
CACHE_DIR="memory/templates"
ALL_TEMPLATES=(choice-architecture refs session session-rollup project tools rca research-topic research-libs)

mkdir -p "$CACHE_DIR"
FORCE=false
TARGETS=()

for arg in "$@"; do
  case "$arg" in
    --force|-f) FORCE=true ;;
    --all|-a) TARGETS=("${ALL_TEMPLATES[@]}") ;;
    *) TARGETS+=("${arg%.md}") ;;
  esac
done

[[ ${#TARGETS[@]} -eq 0 ]] && { echo '{"error":"specify <template-name> or --all [--force]"}'; exit 1; }

updated=0; skipped=0
for name in "${TARGETS[@]}"; do
  dest="$CACHE_DIR/${name}.md"
  if [[ "$FORCE" == true || ! -s "$dest" ]]; then
    curl -fsSL "${BASE_URL}/${name}.md" -o "$dest"
    ((updated+=1))
  else
    ((skipped+=1))
  fi
done

printf '{"updated":%d,"skipped":%d,"cache_dir":"%s"}\n' "$updated" "$skipped" "$CACHE_DIR"
