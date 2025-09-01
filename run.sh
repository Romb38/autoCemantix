#!/bin/bash

# This file is here to help running by using bash
# It is currently used for a crontab to start this script every morning

set -e
cd "$(dirname "$0")"
word=$(.venv/bin/python main.py solve)

