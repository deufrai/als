#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."

jupyter nbconvert --to html --output-dir build --no-input notebooks/*.ipynb
