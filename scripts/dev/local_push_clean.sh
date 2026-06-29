#!/usr/bin/env bash
set -euo pipefail
python scripts/quality/strip_notebook_outputs.py notebooks
python scripts/quality/secret_scan.py .
python scripts/quality/check_large_files.py .
git status --short
