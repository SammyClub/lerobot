"""Live camera-alignment viewer using rerun.

Streams the front and wrist cameras into the rerun viewer, showing for each:
  - the full frame with the crop region drawn on it
  - the cropped view by itself (what a square-cropped policy would see)

Usage (inside the `lerobot` conda env):
    python scripts/camera_align.py --front 1 --wrist 0 --crop 600
    python scripts/camera_align.py --front 1 --wrist 0 --crop 600 --width 1920 --height 1080

Camera indices come from `lerobot-find-cameras opencv`. Ctrl-C to stop.
First run: macOS will ask for camera permission for your terminal app — allow it.
"""

import argparse
import sys

import cv2
import rerun as rr


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--front", type=int, default=1, help="front camera index")
    ap.add_argument("--wrist", type=int, default=0, help="wrist camera index")
    ap.add_argument("--crop", type=int, default=600, help="square crop size (px), centered")
    ap.add_argument("--width", type=int, default=1920, help="capture width")
    ap.add_argument("--height", type=int, default=1080, help="capture height")
    args = ap.parse_args()

    rr.init("camera-align", spawn=True)

    cams = {}
    for name, idx in [("front", args.front), ("wrist", args.wrist)]:
        cap = cv2.VideoCapture(idx)
        if not cap.isOpened():
            print(f"WARNING: camera '{name}' (index {idx}) did not open — skipping")
            continue
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"{name}: index {idx}, capturing at {w}x{h}")
        cams[name] = cap

    if not cams:
        sys.exit("No cameras opened. Check indices with: lerobot-find-cameras opencv")

    print(f"Streaming with centered {args.crop}x{args.crop} crop. Ctrl-C to stop.")
    try:
        while True:
            for name, cap in cams.items():
                ok, frame = cap.read()
                if not ok:
                    continue
                h, w = frame.shape[:2]
                c = min(args.crop, w, h)  # crop can't exceed the frame
                x0, y0 = (w - c) // 2, (h - c) // 2

                full = frame.copy()
                cv2.rectangle(full, (x0, y0), (x0 + c, y0 + c), (0, 90, 255), 3)
                rr.log(f"{name}/full", rr.Image(cv2.cvtColor(full, cv2.COLOR_BGR2RGB)))
                rr.log(
                    f"{name}/crop_{c}px",
                    rr.Image(cv2.cvtColor(frame[y0 : y0 + c, x0 : x0 + c], cv2.COLOR_BGR2RGB)),
                )
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        for cap in cams.values():
            cap.release()


if __name__ == "__main__":
    main()
