#!/usr/bin/env python3
"""
Pre-commit hook to block committing .env files.

Scans staged files, ignores safe templates like .env.example or .env.template,
and exits with a failure code if blocked files are found.
Matches:
    - .env
    - .env.local
    - .env.development
Does NOT match:
    - .env.txtignored
    - anything not intended to be blocked
"""

import re
import sys

# Regex for allowed .env files:
# (^|/)      → matches start of string or folder separator
# \.env      → matches literal ".env"
# (\.[a-zA-Z0-9_-]+|$) → matches either:
# - a single "extension" with:
# letters, numbers, underscore, or dash
#  - OR end of string (just ".env")
blocked_pattern = re.compile(r"(^|/)\.env(\.[a-zA-Z0-9_-]+|$)")

# Safe files to ignore
ignore_files = {".env.example", ".env.template"}

# Get staged files from pre-commit.
# sys.argv is list command-line arguments.
# sys.argv[0] is script name.
# sys.argv[1:] all other arguments except for the name (unwanted).
files = sys.argv[1:]

# Filter files that match the blocked pattern but are not in ignore list
blocked_files = [
    f for f in files if blocked_pattern.search(f) and f not in ignore_files
]

if blocked_files:
    print("❌ Commit blocked! The following .env files are not allowed:\n")
    for f in blocked_files:
        print(f"  - {f}")
    sys.exit(1)

# Exit with success if no files are blocked
sys.exit(0)
