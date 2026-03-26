#!/usr/bin/env python3
"""Regenerate index.json from packages/ directory."""
import os
import json
import zipfile
import glob


def main():
    packages = {}

    for pkg_dir in sorted(glob.glob("packages/*")):
        if not os.path.isdir(pkg_dir):
            continue
        name = os.path.basename(pkg_dir)

        # Find wheel
        whls = glob.glob(os.path.join(pkg_dir, "*.whl"))
        if not whls:
            print(f"  SKIP {name}: no .whl file")
            continue
        whl = whls[0]
        whl_rel = whl.replace("\\", "/")  # normalize for URLs

        # Find wasm (optional)
        wasms = glob.glob(os.path.join(pkg_dir, "*.wasm"))
        wasm_rel = wasms[0].replace("\\", "/") if wasms else None

        # Extract metadata from wheel
        version = ""
        summary = ""
        deps = []
        with zipfile.ZipFile(whl) as zf:
            for entry in zf.namelist():
                if entry.endswith("/METADATA"):
                    meta = zf.read(entry).decode("utf-8")
                    for line in meta.split("\n"):
                        if line.startswith("Version:"):
                            version = line.split(":", 1)[1].strip()
                        elif line.startswith("Summary:"):
                            summary = line.split(":", 1)[1].strip()
                        elif line.startswith("Requires-Dist:"):
                            # Parse: "package_name (>=1.0) ; extra == 'test'"
                            dep_str = line.split(":", 1)[1].strip()
                            # Skip optional/extra dependencies
                            if ";" in dep_str:
                                continue
                            dep_name = dep_str.split()[0].split("(")[0].strip()
                            deps.append(dep_name)
                    break

        size = sum(
            os.path.getsize(f)
            for f in [whl] + (wasms or [])
        )

        packages[name] = {
            "version": version,
            "summary": summary,
            "wasm": wasm_rel,
            "wheel": whl_rel,
            "depends": deps,
            "size_bytes": size,
        }

    index = {"version": 1, "packages": packages}

    with open("index.json", "w") as f:
        json.dump(index, f, indent=2)
        f.write("\n")

    print(f"index.json updated: {len(packages)} packages")
    for name, info in sorted(packages.items()):
        wasm_tag = " +wasm" if info["wasm"] else ""
        deps_tag = f" (deps: {', '.join(info['depends'])})" if info["depends"] else ""
        print(f"  {name}=={info['version']}{wasm_tag} ({info['size_bytes']:,} bytes){deps_tag}")


if __name__ == "__main__":
    main()
