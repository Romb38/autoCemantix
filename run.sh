#!/bin/bash
set -e

cd "$(dirname "$0")"

start=$(date +%s.%N)
word=$(.venv/bin/python main.py)
end=$(date +%s.%N)

duration=$(echo "$end - $start" | bc)
echo "Durée d'exécution : $duration secondes"
if [ -n "$word" ]; then
    echo "Answer : $word"
else
    echo "No solution found."
fi
