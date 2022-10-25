#!/usr/bin/env bash
set -euo pipefail

echo "[checkstyle]"
pycodestyle ./src

echo "[unittest]"
python -m unittest