#!/usr/bin/env python3
"""Validate all wheels in the registry are pure Python (no compiled extensions)."""
import glob
import sys
import zipfile

errors = []
count = 0

for whl in glob.glob("packages/*/*.whl"):
    count += 1
    with zipfile.ZipFile(whl) as zf:
        for name in zf.namelist():
            if name.endswith((".so", ".pyd", ".dylib", ".dll")):
                errors.append(f"{whl}: contains compiled extension {name}")

if errors:
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(1)

print(f"All {count} wheels are pure Python")
