#!/bin/bash
set -e
cd "$(dirname "$0")"
word=$(.venv/bin/python main.py)

