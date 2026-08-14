#!/usr/bin/env bash
# Open the SSH tunnel to the cloud policy server (job id from
# scripts/.cloud_policy_job.json, written by serve_policy_cloud.py).
# Keeps running in the foreground — leave this terminal open while the robot
# runs; Ctrl-C closes the tunnel.
set -e
STATE="$(dirname "$0")/.cloud_policy_job.json"
[ -f "$STATE" ] || { echo "No $STATE — run serve_policy_cloud.py first" >&2; exit 1; }
JOB_ID=$(python3 -c "import json;print(json.load(open('$STATE'))['job_id'])")
PORT=$(python3 -c "import json;print(json.load(open('$STATE'))['port'])")
echo "Tunneling localhost:$PORT -> job $JOB_ID:$PORT (Ctrl-C to close)"
exec ssh -N -L "$PORT:127.0.0.1:$PORT" \
    -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=15 \
    "$JOB_ID@ssh.hf.jobs"
