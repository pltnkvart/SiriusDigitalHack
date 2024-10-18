#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

python3 "$PARENT_DIR/utils/parser.py" "$PARENT_DIR/datasets/original.xlsx" "$PARENT_DIR/datasets/results.json"
