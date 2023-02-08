#!/usr/bin/env bash

URL="http://localhost:5000/webhook"

for season in {1..2}; do
  for episode in $(seq -f "E%02g" 1 10); do
    data=$(echo -n '{"title": "TV SHOW", "episodes": "S0'$season$episode'"}')
    curl -H "Content-Type: application/json" -X POST -d "$data" "$URL"
    echo '{"title": "TV SHOW", "episode": "S0'$season$episode'"}'
  done
  echo
done

