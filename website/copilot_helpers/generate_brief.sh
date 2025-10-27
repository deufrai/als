#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the file to read
FILE="${SCRIPT_DIR}/copilot_brief.txt"

# Read the task context file
while IFS= read -r line; do
  # Check if the line is non-blank
  if [[ -n "$line" ]]; then
    # Replace patterns {{...}} with the result of the command execution
    while [[ "$line" =~ \{\{([^}]+)\}\} ]]; do
      # Extract the command from the pattern
      cmd=${BASH_REMATCH[1]}
      # Execute the command and replace the pattern with the result
      result=$(eval "$cmd")
      line=${line//\{\{$cmd\}\}/$result}
    done
    # Print the processed line
    echo "$line"
  fi
done < "$FILE"
