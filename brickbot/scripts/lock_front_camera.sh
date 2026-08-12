#!/usr/bin/env bash
# Freeze the front camera's (Acer A610, UVC index 0) exposure + white balance.
# The Acer is fixed-focus, so focus needs no locking.
#
# Normal use (start of every recording session):
#     scripts/lock_front_camera.sh
# Freezes whatever the camera's auto modes last converged on.
#
# After a lighting change:
#     scripts/lock_front_camera.sh --auto     # re-enable auto modes
#     python scripts/camera_align.py --front 0 --wrist 1   # stream ~10 s so auto converges
#     scripts/lock_front_camera.sh            # freeze the new values
#
# Requires uvc-util (built from https://github.com/jtfrey/uvc-util, installed
# to ~/.local/bin). NOTE: device is selected by UVC index 0 — if cameras are
# ever replugged into different sockets, verify with `uvc-util -d` that index 0
# is still "Acer A610".
set -e
DEV="-I 0"

if ! command -v uvc-util >/dev/null; then
    echo "uvc-util not found on PATH — see comment header for install source" >&2
    exit 1
fi

if ! uvc-util -d | grep -q "Acer"; then
    echo "WARNING: no Acer device visible — is the front camera plugged in?" >&2
    uvc-util -d >&2
    exit 1
fi

if [ "$1" = "--auto" ]; then
    uvc-util -k $DEV -s auto-exposure-mode=8 -s auto-white-balance-temp=1
    echo "Auto modes re-enabled. Stream the camera ~10 s with the real scene/lighting,"
    echo "then re-run this script without --auto to freeze the converged values."
    exit 0
fi

uvc-util -k $DEV -s auto-exposure-mode=1 -s auto-white-balance-temp=0 -s auto-exposure-priority=0
echo "Front camera locked. Current values:"
for c in auto-exposure-mode auto-white-balance-temp exposure-time-abs white-balance-temp gain; do
    uvc-util $DEV -g "$c"
done
