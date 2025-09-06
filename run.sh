#!/bin/bash

# This file is here to help running by using bash
# It is currently used for a crontab to start this script every morning

set -e
cd "$(dirname "$0")"
word=$(.venv/bin/python main.py solve)

git add src/resources/frWac.bin src/resources/invalid_words.pkl
git commit -m "Daily dictionary update"
git push
