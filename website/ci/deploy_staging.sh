#!/bin/bash
set -euo pipefail

# Check if required environment variables are set
if [ -z "${STAGING_DIR:-}" ]; then
  echo "Error: STAGING_DIR environment variable is not set."
  exit 1
fi

if [ -z "${NODE_PATH:-}" ]; then
  echo "Error: NODE_PATH environment variable is not set."
  exit 1
fi

# Add Node.js binaries to PATH
export PATH="$PATH:$NODE_PATH"

echo "Starting the deployment process..."

REPO_ROOT=$(pwd)
echo "Repository root: $REPO_ROOT"

echo "Installing project-level Node.js dependencies..."
npm install

echo "Initializing and updating Docsy submodule..."
git submodule update --init --recursive
cd website/themes/docsy || { echo "Docsy directory not found"; exit 1; }
git checkout v0.11.0 || { echo "Error: Failed to checkout Docsy version v0.11.0."; exit 1; }

echo "Installing Docsy theme Node.js dependencies..."
npm install

cd "$REPO_ROOT" || { echo "Failed to return to repository root"; exit 1; }

echo "Updating footer with current commit hash..."
sed -i "s/@@COMMIT_ID@@/${CI_COMMIT_SHORT_SHA:-UNDEFINED}/g" website/layouts/partials/footer.html

echo "Building the Hugo site to a temporary directory..."
BUILD_DIR=$(mktemp -d)
hugo --cleanDestinationDir --destination "$BUILD_DIR"

echo "Emptying the target folder: ${STAGING_DIR:?}"
rm -rf "${STAGING_DIR:?}"/*

echo "Copying generated files to the target folder..."
cp -R "$BUILD_DIR"/* "${STAGING_DIR:?}"

echo "Setting permissions for the target folder..."
chmod -R u=rwX,go=rX "${STAGING_DIR:?}"

echo "Deployment process completed successfully."
