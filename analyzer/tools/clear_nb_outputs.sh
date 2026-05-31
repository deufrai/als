#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."

jupyter nbconvert \
  --clear-output \
  --ClearMetadataPreprocessor.enabled=True \
  --ClearMetadataPreprocessor.clear_cell_metadata=True \
  --ClearMetadataPreprocessor.clear_notebook_metadata=True \
  notebooks/*.ipynb
