#!/usr/bin/env bash
set -euo pipefail

python scripts/validate-standard.py
python scripts/run-standard-evals.py
