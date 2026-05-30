#!/bin/bash
set -euo pipefail

print_cmd() {
  printf '+ %q' "$1"
  shift
  printf ' %q' "$@"
  printf '\n'
}

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

require_variable "PROD_DIR"
require_variable "PROD_BACKUP_DIR"
require_variable "NODE_PATH"
require_variable "CI_COMMIT_TAG"
require_variable "CI_PROJECT_DIR"

repo_root="$CI_PROJECT_DIR"
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

backup_name="${CI_COMMIT_TAG}-${CI_COMMIT_SHORT_SHA:-unknown}-$(date -u +%Y%m%dT%H%M%SZ)"
backup_dir="$backup_root/$backup_name"

cat <<EOF
Production website deployment dry run.

This script is intentionally print-only in this validation version.

Repository root: $repo_root
Production webroot: $prod_dir
Production backup root: $backup_root
Planned backup directory: $backup_dir
Tag: $CI_COMMIT_TAG

Planned command sequence:
EOF

print_cmd cd "$repo_root"
print_cmd export "PATH=\$PATH:$NODE_PATH"
print_cmd cd "$repo_root/website"
print_cmd npm install
print_cmd git submodule update --init --recursive
print_cmd cd "$repo_root/website/themes/docsy"
print_cmd git checkout v0.11.0
print_cmd npm install
print_cmd cd "$repo_root"
print_cmd sed -i "s/@@COMMIT_ID@@/${CI_COMMIT_SHORT_SHA:-UNDEFINED}/g" website/layouts/partials/footer.html
echo '+ BUILD_DIR=$(mktemp -d)'
print_cmd hugo --cleanDestinationDir --source website --destination "\$BUILD_DIR"
print_cmd test -f "\$BUILD_DIR/index.html"
print_cmd test -d "\$BUILD_DIR/docs"
print_cmd mkdir -p "$backup_dir"

cat <<EOF

The final deployment script will then:
- list top-level entries from the Hugo build output;
- back up only matching existing production entries;
- back up existing top-level offline-search-index.*.json files;
- remove matching managed entries from production;
- remove stale top-level offline-search-index.*.json files;
- copy the new Hugo build entries into production;
- fix permissions on copied Hugo-managed entries only;
- restore the backup automatically if any deployment step fails.
EOF
