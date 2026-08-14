#!/usr/bin/env bash
# Thin wrapper — the real logic (with the Acer manual-WB-is-broken workaround
# and auto-calibrated manual exposure) lives in lock_front_camera.py.
exec conda run --no-capture-output -n lerobot python "$(dirname "$0")/lock_front_camera.py" "$@"
