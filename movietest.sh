#!/usr/bin/env bash

curl -X POST -H "Content-Type: application/json" -d '{"title": "Incesptio
n", "movies": "A mind-bending thriller about a talented extractor who is off
ered a chance to regain his old life as payment for a task considered to be
impossible: Inception, the implantation of another persons idea into a targe
ts subconscious"}' http://localhost:5000/webhook
