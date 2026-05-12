#!/usr/bin/env bash
set -euo pipefail
URL="https://hiveminderbot.github.io/autonomy-supervisor-agent/"
echo "Checking $URL ..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
if [ "$STATUS" = "200" ]; then
    echo "PASS: HTTP $STATUS"
    # Check for key content
    BODY=$(curl -s "$URL")
    if echo "$BODY" | grep -q "Trismegistus Supervisor Agent"; then
        echo "PASS: Title found"
    else
        echo "FAIL: Title not found"
        exit 1
    fi
    if echo "$BODY" | grep -q "90.9%"; then
        echo "PASS: Router accuracy metric found"
    else
        echo "FAIL: Router accuracy metric not found"
        exit 1
    fi
    if echo "$BODY" | grep -q "Live Runs"; then
        echo "PASS: Live Runs metric found"
    else
        echo "FAIL: Live Runs metric not found"
        exit 1
    fi
    echo "All health checks passed."
else
    echo "FAIL: HTTP $STATUS"
    exit 1
fi
