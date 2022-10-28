#!/usr/bin/env bash
set -euo pipefail

echo "[checkstyle]"
pycodestyle ./cconn

echo "[unittest]"
python -m unittest