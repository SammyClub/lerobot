"""Lock the front camera (Acer A610, UVC index 0) for recording.

Quirk discovered 2026-08-12: this camera's MANUAL WHITE BALANCE IS BROKEN —
disabling auto-WB produces a strong green cast regardless of the temperature
value (measured green-ratio 1.42+ vs 1.00 in auto). So white balance stays
AUTO (harmless under fixed lighting). What this script locks is EXPOSURE,
which is what pulses when the arm crosses the white table:

  1. measure mean brightness under full-auto exposure (the "right" look)
  2. switch to manual exposure and binary-search exposure-time-abs until
     brightness matches the auto baseline
  3. disable auto-exposure-priority (fixed frame rate)

Run at the start of every recording session (UVC settings can reset on
replug/reboot), AFTER the scene and lighting are final, with no other app
holding the camera:

    conda run -n lerobot python scripts/lock_front_camera.py

To undo (back to full auto): add --auto
Requires uvc-util on PATH (built from https://github.com/jtfrey/uvc-util).
"""

import subprocess
import sys

import cv2
import numpy as np


def uvc(*args: str) -> None:
    subprocess.run(["uvc-util", "-I", "0", "-k", *args], capture_output=True)


def check_camera_present() -> None:
    r = subprocess.run(["uvc-util", "-d"], capture_output=True, text=True)
    if "Acer" not in r.stdout:
        sys.exit(f"No Acer device visible — is the front camera plugged in?\n{r.stdout}")


def brightness(warmup: int = 25, samples: int = 8) -> float:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        sys.exit("Camera busy — close the rerun viewer / LeLab / teleop first.")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    for _ in range(warmup):
        cap.read()
    vals = []
    for _ in range(samples):
        ok, f = cap.read()
        if ok:
            vals.append(f.mean())
    cap.release()
    if not vals:
        sys.exit("Camera opened but produced no frames.")
    return float(np.mean(vals))


def main() -> None:
    check_camera_present()

    if "--auto" in sys.argv:
        uvc("-s", "auto-exposure-mode=8", "-s", "auto-white-balance-temp=1")
        print("Front camera back to full auto.")
        return

    uvc("-s", "auto-white-balance-temp=1")  # AWB must stay auto (manual WB broken)
    uvc("-s", "auto-exposure-mode=8")
    target = brightness()
    print(f"auto-exposure baseline brightness: {target:.1f}")

    uvc("-s", "auto-exposure-mode=1", "-s", "auto-exposure-priority=0")
    lo, hi = 5, 600
    best, best_diff = None, float("inf")
    for _ in range(7):
        mid = (lo + hi) // 2
        uvc("-s", f"exposure-time-abs={mid}")
        b = brightness(warmup=15, samples=6)
        print(f"  exposure={mid:4d} -> brightness {b:6.1f}")
        if abs(b - target) < best_diff:
            best, best_diff = mid, abs(b - target)
        if b > target:
            hi = mid
        else:
            lo = mid
    uvc("-s", f"exposure-time-abs={best}")
    final = brightness(warmup=15, samples=6)
    print(f"LOCKED: manual exposure={best} (brightness {final:.1f}, auto target {target:.1f}); "
          f"white balance stays auto (manual WB broken on this camera).")


if __name__ == "__main__":
    main()
