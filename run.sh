#!/bin/bash

# This file is here to help running by using bash
# It is currently used for a crontab to start this script every morning

set -e
cd "$(dirname "$0")"

GIT_UPDATE=false
for arg in "$@"; do
    if [[ "$arg" == "--git-update" || "$arg" == "-gu" ]]; then
        GIT_UPDATE=true
    fi
done

word=$(.venv/bin/python main.py solve)

if $GIT_UPDATE; then
    git add src/resources/frWac.bin src/resources/invalid_words.pkl src/resources/stats.csv
    git commit -m "Daily dictionary update"
    git push
fi
