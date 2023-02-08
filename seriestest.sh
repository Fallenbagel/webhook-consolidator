#!/usr/bin/env bash

URL="http://localhost:5000/webhook"

for season in {1..2}; do
  for episode in $(seq -f "E%02g" 1 10); do
    data=$(echo -n '{"title": "My Mum", "episodes": "S0'$season$episode'"}')
    curl -H "Content-Type: application/json" -X POST -d "$data" "$URL"
    echo '{"title": "My mom", "episode": "S0'$season$episode'"}'
  done
  echo
done

