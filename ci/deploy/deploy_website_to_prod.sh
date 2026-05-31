#!/bin/bash
set -euo pipefail

require_variable() {
  local variable_name="$1"
  local variable_value="${!variable_name:-}"

  if [ -z "$variable_value" ]; then
    echo "Error: ${variable_name} environment variable is not set."
    exit 1
  fi
}

canonicalize_directory() {
  local variable_name="$1"
  local directory_path="${!variable_name}"

  if [ ! -d "$directory_path" ]; then
    echo "Error: ${variable_name} does not point to an existing directory: ${directory_path}"
    exit 1
  fi

  realpath "$directory_path"
}

ensure_safe_directory_pair() {
  local prod_dir="$1"
  local backup_dir="$2"

  if [ "$prod_dir" = "/" ]; then
    echo "Error: PROD_DIR must not be '/'."
    exit 1
  fi

  if [ "$backup_dir" = "/" ]; then
    echo "Error: PROD_BACKUP_DIR must not be '/'."
    exit 1
  fi

  case "$backup_dir" in
    "$prod_dir"|"$prod_dir"/*)
      echo "Error: PROD_BACKUP_DIR must not be equal to or inside PROD_DIR."
      exit 1
      ;;
  esac

  case "$prod_dir" in
    "$backup_dir"|"$backup_dir"/*)
      echo "Error: PROD_DIR must not be equal to or inside PROD_BACKUP_DIR."
      exit 1
      ;;
  esac
}

ensure_stable_release_tag() {
  local tag_name="$1"

  if [[ ! "$tag_name" =~ ^v[0-9]+(\.[0-9]+)*$ ]]; then
    echo "Error: production deployment requires a stable release tag such as v0.7.1."
    echo "Error: got tag: $tag_name"
    exit 1
  fi
}

list_top_level_entries() {
  local directory_path="$1"

  find "$directory_path" -mindepth 1 -maxdepth 1 -printf '%f\n' | sort
}

restore_backup() {
  local rollback_failed=0

  if [ "${deployment_started:-0}" -ne 1 ]; then
    return
  fi

  echo "ROLLBACK STARTED: deployment failed after production changes began."
  echo "ROLLBACK STARTED: restoring backed-up production entries from: $backup_dir"
  set +e

  while IFS= read -r entry_name; do
    if [ -z "$entry_name" ]; then
      continue
    fi

    rm -rf "$prod_dir/$entry_name" || rollback_failed=1
  done < "$managed_entries_file"

  while IFS= read -r search_index_path; do
    if [ -z "$search_index_path" ]; then
      continue
    fi

    rm -f "$search_index_path" || rollback_failed=1
  done < "$search_indexes_file"

  if [ -d "$backup_dir/prod" ]; then
    cp -a "$backup_dir/prod"/. "$prod_dir"/ || rollback_failed=1
  else
    echo "ROLLBACK FAILED: backup payload directory is missing: $backup_dir/prod"
    rollback_failed=1
  fi

  trap - ERR

  if [ "$rollback_failed" -ne 0 ]; then
    echo "ROLLBACK FAILED: manual restore required from backup: $backup_dir"
    exit 2
  fi

  echo "ROLLBACK COMPLETED: restored production entries from backup: $backup_dir"
  exit 1
}

require_variable "PROD_DIR"
require_variable "PROD_BACKUP_DIR"
require_variable "NODE_PATH"
require_variable "PROD_BASE_URL"
require_variable "CI_COMMIT_TAG"
require_variable "CI_PROJECT_DIR"

repo_root="$CI_PROJECT_DIR"
ensure_stable_release_tag "$CI_COMMIT_TAG"

prod_dir="$(canonicalize_directory "PROD_DIR")"
backup_root="$(canonicalize_directory "PROD_BACKUP_DIR")"

if [ ! -d "$repo_root" ]; then
  echo "Error: CI_PROJECT_DIR does not point to an existing directory: ${repo_root}"
  exit 1
fi

ensure_safe_directory_pair "$prod_dir" "$backup_root"

if [ ! -f "$prod_dir/index.html" ]; then
  echo "Error: PROD_DIR does not look like the production webroot: missing index.html."
  exit 1
fi

export PATH="$PATH:$NODE_PATH"
cd "$repo_root"

backup_name="${CI_COMMIT_TAG}-${CI_COMMIT_SHORT_SHA:-unknown}-$(date -u +%Y%m%dT%H%M%SZ)"
backup_dir="$backup_root/$backup_name"
backup_payload_dir="$backup_dir/prod"
manifest_file="$backup_dir/manifest.txt"
managed_entries_file="$backup_dir/managed_entries.txt"
search_indexes_file="$backup_dir/search_indexes.txt"
deployment_started=0

echo "Starting production website deployment..."
echo "Repository root: $repo_root"
echo "Production webroot: $prod_dir"
echo "Production backup root: $backup_root"
echo "Backup directory: $backup_dir"
echo "Tag: $CI_COMMIT_TAG"

echo "Installing project-level Node.js dependencies..."
cd website
npm install

echo "Initializing and updating Docsy submodule..."
git submodule update --init --recursive
cd themes/docsy || { echo "Docsy directory not found"; exit 1; }
git checkout v0.11.0 || { echo "Error: Failed to checkout Docsy version v0.11.0."; exit 1; }

echo "Installing Docsy theme Node.js dependencies..."
npm install

cd "$repo_root" || { echo "Failed to return to repository root"; exit 1; }

echo "Updating footer with current commit hash..."
sed -i "s/@@COMMIT_ID@@/${CI_COMMIT_SHORT_SHA:-UNDEFINED}/g" website/layouts/partials/footer.html

echo "Building the Hugo site to a temporary directory..."
build_dir=$(mktemp -d)
hugo --cleanDestinationDir --source website --destination "$build_dir" --baseURL "$PROD_BASE_URL"

if [ ! -f "$build_dir/index.html" ]; then
  echo "Error: Hugo build output does not contain index.html."
  exit 1
fi

if [ ! -d "$build_dir/docs" ]; then
  echo "Error: Hugo build output does not contain docs directory."
  exit 1
fi

echo "Preparing deployment backup..."
mkdir -p "$backup_payload_dir"

list_top_level_entries "$build_dir" > "$managed_entries_file"
find "$prod_dir" -mindepth 1 -maxdepth 1 -type f -name 'offline-search-index.*.json' | sort > "$search_indexes_file"

{
  echo "Production deployment manifest"
  echo "Tag: $CI_COMMIT_TAG"
  echo "Commit: ${CI_COMMIT_SHA:-UNDEFINED}"
  echo "Build directory: $build_dir"
  echo "Production webroot: $prod_dir"
  echo
  echo "Managed entries from Hugo build:"
  sed 's/^/- /' "$managed_entries_file"
  echo
  echo "Existing search indexes scheduled for cleanup:"
  if [ -s "$search_indexes_file" ]; then
    sed 's/^/- /' "$search_indexes_file"
  else
    echo "- none"
  fi
} > "$manifest_file"

echo "Managed top-level entries that will be replaced:"
sed 's/^/- /' "$managed_entries_file"

echo "Existing top-level search index files that will be removed:"
if [ -s "$search_indexes_file" ]; then
  sed 's/^/- /' "$search_indexes_file"
else
  echo "- none"
fi

echo "Backing up matching production entries..."
while IFS= read -r entry_name; do
  if [ -e "$prod_dir/$entry_name" ]; then
    cp -a "$prod_dir/$entry_name" "$backup_payload_dir/"
  fi
done < "$managed_entries_file"

while IFS= read -r search_index_path; do
  if [ -e "$search_index_path" ]; then
    cp -a "$search_index_path" "$backup_payload_dir/"
  fi
done < "$search_indexes_file"

trap restore_backup ERR
deployment_started=1

echo "Removing managed production entries..."
while IFS= read -r entry_name; do
  rm -rf "$prod_dir/$entry_name"
done < "$managed_entries_file"

echo "Removing stale top-level search indexes..."
while IFS= read -r search_index_path; do
  rm -f "$search_index_path"
done < "$search_indexes_file"

echo "Copying new Hugo build entries to production..."
while IFS= read -r entry_name; do
  cp -a "$build_dir/$entry_name" "$prod_dir/"
done < "$managed_entries_file"

echo "Setting permissions for copied Hugo-managed entries..."
while IFS= read -r entry_name; do
  chmod -R u=rwX,go=rX "$prod_dir/$entry_name"
done < "$managed_entries_file"

deployment_started=0
trap - ERR

echo "Production website deployment completed successfully."
echo "Backup kept at: $backup_dir"
