#!/bin/bash

# Check if path argument is provided
if [ -z "$1" ]; then
    echo "Error: Repository path argument is required"
    exit 1
fi

REPO_PATH="$1"

# Check if the path exists and is a directory
if [ ! -d "$REPO_PATH" ]; then
    echo "Error: $REPO_PATH is not a valid directory"
    exit 1
fi

cd "$REPO_PATH"
git pull 