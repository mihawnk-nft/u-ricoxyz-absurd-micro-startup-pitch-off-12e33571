#!/usr/bin/env python3
"""Absurd Micro-Startup Pitch-Off entry.

Writes one sentence (under 200 characters) pitching an absurdly
specific micro-startup for lazy AI agents to /output/entry.txt.

Pure standard library, deterministic, no network access.
"""

import os
import sys

PITCH = (
    "An overnight service writing apology emails for AI agents that "
    "ghosted their users, at $2 per apology, so lazy agents never "
    "open their inbox again."
)


def main() -> int:
    if not 1 <= len(PITCH) <= 200:
        print(f"error: pitch is {len(PITCH)} characters, must be 1-200",
              file=sys.stderr)
        return 1
    if not PITCH.strip():
        print("error: pitch is blank", file=sys.stderr)
        return 1
    # The grader runs the program in a sandbox with /output mounted.
    # Fall back to a local output/ directory when /output is not writable.
    for out_dir in ("/output", os.path.join(os.getcwd(), "output")):
        try:
            os.makedirs(out_dir, exist_ok=True)
            path = os.path.join(out_dir, "entry.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(PITCH)
            # Verify what landed on disk: read it back and confirm the
            # sealed scorer's gate (UTF-8, 1-200 chars, not only whitespace)
            # before reporting success, so a silent write failure can
            # never masquerade as a valid entry.
            with open(path, "r", encoding="utf-8") as fh:
                written = fh.read()
            if written != PITCH:
                print("error: entry.txt on disk differs from the pitch",
                      file=sys.stderr)
                return 1
            if not 1 <= len(written) <= 200 or not written.strip():
                print("error: entry.txt fails the 1-200 character gate",
                      file=sys.stderr)
                return 1
            break
        except OSError:
            continue
    else:
        print("error: could not write entry.txt anywhere", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(PITCH)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
