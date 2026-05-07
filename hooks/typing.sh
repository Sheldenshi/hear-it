#!/bin/bash
# Fire-and-forget typing sound. Spawns a Python helper that loops the clip
# for a duration scaled to write size.

if ! command -v afplay >/dev/null 2>&1; then
  exit 0
fi

SOUND="${CLAUDE_PLUGIN_ROOT}/hooks/sounds/typing.mp3"
HELPER="${CLAUDE_PLUGIN_ROOT}/hooks/play.py"
[ -f "$SOUND" ] || exit 0
[ -f "$HELPER" ] || exit 0

PAYLOAD=$(cat)
printf '%s' "$PAYLOAD" | /usr/bin/python3 "$HELPER" "$SOUND" >/dev/null 2>&1 &
disown 2>/dev/null || true

exit 0
