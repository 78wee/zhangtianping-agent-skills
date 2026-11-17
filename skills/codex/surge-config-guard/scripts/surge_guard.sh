#!/usr/bin/env bash
set -euo pipefail

SURGE_CLI="${SURGE_CLI:-/Applications/Surge.app/Contents/Applications/surge-cli}"
PROFILE="${1:-}"
ACTION="${2:-validate}"

usage() {
  printf 'Usage: %s <profile-path> [backup|validate|reload-validate]\n' "$0" >&2
}

if [[ -z "$PROFILE" ]]; then
  usage
  exit 2
fi

if [[ ! -f "$PROFILE" ]]; then
  printf 'Profile not found: %s\n' "$PROFILE" >&2
  exit 2
fi

backup_profile() {
  local reason="${3:-manual}"
  local stamp
  stamp="$(date +%Y%m%d-%H%M%S)"
  local backup="${PROFILE}.bak-${stamp}-${reason}"
  cp "$PROFILE" "$backup"
  printf '%s\n' "$backup"
}

validate_loaded() {
  "$SURGE_CLI" dump rule >/tmp/surge-guard-rules.txt
  "$SURGE_CLI" --raw dump profile original >/tmp/surge-guard-profile.json
  "$SURGE_CLI" --raw dump event >/tmp/surge-guard-events.json
  printf 'OK: dump rule/profile/event completed\n'
}

case "$ACTION" in
  backup)
    backup_profile "$@"
    ;;
  validate)
    validate_loaded
    ;;
  reload-validate)
    "$SURGE_CLI" reload
    validate_loaded
    ;;
  *)
    usage
    exit 2
    ;;
esac
