#!/usr/bin/env python3
"""Play the typing clip in a loop for a duration scaled to write size.

Reads the Claude Code hook JSON from stdin. Designed to be backgrounded by
typing.sh so the hook returns instantly.
"""

import json
import subprocess
import sys
import time

CHARS_PER_SECOND = 250
MIN_SECONDS = 0.4
MAX_SECONDS = 15.0
VOLUME = "0.8"


def main():
    if len(sys.argv) < 2:
        sys.exit(0)
    sound = sys.argv[1]

    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_input = payload.get("tool_input") or {}
    content = (
        tool_input.get("content")
        or tool_input.get("new_string")
        or tool_input.get("new_source")
        or ""
    )

    duration = max(MIN_SECONDS, min(MAX_SECONDS, len(content) / CHARS_PER_SECOND))
    end = time.time() + duration

    while time.time() < end:
        proc = subprocess.Popen(
            ["afplay", "-v", VOLUME, sound],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        remaining = end - time.time()
        try:
            proc.wait(timeout=max(0.05, remaining))
        except subprocess.TimeoutExpired:
            proc.terminate()
            try:
                proc.wait(timeout=0.2)
            except subprocess.TimeoutExpired:
                proc.kill()
            break


if __name__ == "__main__":
    main()
