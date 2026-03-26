# Codepod Package Registry

Pre-built Python packages for the [codepod](https://github.com/codepod-sandbox/codepod) sandbox.

Served via GitHub Pages at `https://codepod-sandbox.github.io/packages/`.

## Usage (inside a sandbox)

```bash
pip install tabulate
```

## Adding a pure-Python package from PyPI

```bash
python3 scripts/add-pypi-package.py <package-name> [version]
python3 scripts/build-index.py
git add -A && git commit -m "feat: add <package-name>"
```

Or use the GitHub Actions workflow: Actions → Add PyPI Package → Run workflow.

## Adding a WASM package

Place the `.wasm` binary and `.whl` wheel in `packages/<name>/`, then rebuild the index:

```bash
python3 scripts/build-index.py
```

## Structure

```
index.json              # Package index (auto-generated)
packages/
  tabulate/
    tabulate-0.9.0-py3-none-any.whl
  numpy/                # (future: WASM + wheel)
    numpy-1.26.4.wasm
    numpy-1.26.4-py3-none-any.whl
```
