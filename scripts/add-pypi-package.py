#!/usr/bin/env python3
"""Download a pure-Python wheel from PyPI and add it to the registry."""
import sys
import json
import os
import urllib.request
import zipfile


def main():
    if len(sys.argv) < 2:
        print("Usage: add-pypi-package.py <package-name> [version]")
        sys.exit(1)

    name = sys.argv[1]
    version = sys.argv[2] if len(sys.argv) > 2 else None

    # Fetch package info from PyPI JSON API
    url = f"https://pypi.org/pypi/{name}/json"
    if version:
        url = f"https://pypi.org/pypi/{name}/{version}/json"

    print(f"Fetching metadata from {url}...")
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read())

    info = data["info"]
    ver = info["version"]

    # Find pure-Python wheel
    wheel_url = None
    wheel_filename = None
    for f in data["urls"]:
        fn = f["filename"]
        if fn.endswith(".whl") and (
            "py3-none-any" in fn or "py2.py3-none-any" in fn
        ):
            wheel_url = f["url"]
            wheel_filename = fn
            break

    if not wheel_url:
        print(f"ERROR: No pure-Python wheel found for {name}=={ver}")
        print("Available files:")
        for f in data["urls"]:
            print(f"  {f['filename']}")
        sys.exit(1)

    # Download wheel
    pkg_dir = os.path.join("packages", name)
    os.makedirs(pkg_dir, exist_ok=True)
    dest = os.path.join(pkg_dir, wheel_filename)
    print(f"Downloading {wheel_filename}...")
    urllib.request.urlretrieve(wheel_url, dest)

    # Validate: no compiled extensions
    with zipfile.ZipFile(dest) as zf:
        for entry in zf.namelist():
            if entry.endswith((".so", ".pyd", ".dylib", ".dll")):
                os.remove(dest)
                print(f"ERROR: Wheel contains compiled extension: {entry}")
                sys.exit(1)

    size = os.path.getsize(dest)
    print(f"Added {name}=={ver} ({size:,} bytes)")
    print(f"  {dest}")
    print(f"\nNow run: python3 scripts/build-index.py")


if __name__ == "__main__":
    main()
