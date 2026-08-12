# 13 — Troubleshooting

[← Hardware ladder](12-hardware-ladder.md) · [README](../README.md)

| Problem | Cause → fix |
|---|---|
| "command not found" for any `lerobot-…` command | The environment isn't active in this Terminal window → `conda activate lerobot` |
| `lerobot-find-port` finds nothing | Charge-only USB cable (swap it); board not powered; Waveshare board jumpers not on channel B |
| Servo not found during motor setup | More than one servo connected — connect exactly ONE; check the 3-pin cable is seated |
| Permission denied on the port (Linux/WSL2) | `sudo chmod 666 /dev/ttyACM*` now; `sudo usermod -aG dialout $USER` + log out/in, forever |
| Arm jumps to a weird pose | Bad calibration or mistyped `--robot.id` → recalibrate; keep ids identical everywhere |
| Cameras swapped or missing | Indices change when replugging → re-run `lerobot-find-cameras opencv`; keep cameras in the same USB sockets |
| Teleop is jittery | The live viewer costs compute → drop `--display_data=true`; use a powered USB hub |
| ffmpeg / video decoding errors | `conda install -c conda-forge ffmpeg=7.1.1` |
| `torch.cuda.is_available()` prints `False` on the RTX PC | Wheel/driver mismatch → `pip install --index-url https://download.pytorch.org/whl/cu128 torch torchvision`; check the NVIDIA driver on Windows (WSL2 inherits it) |
| GPU out-of-memory during training | Lower `--batch_size` (64 → 32 → 16) |
| A tutorial's command doesn't exist | Pre-late-2025 tutorial or Trelis-fork flag → [translation table](02-version-drift.md) |
| Recording to a reused dataset name misbehaves | Stale local leftovers → `rm -rf ~/.cache/huggingface/lerobot/<user>/<dataset>` and start clean (resuming, by contrast, needs those files intact) |
| Old dataset won't load (v2.1 format) | `python -m lerobot.datasets.v30.convert_dataset_v21_to_v30 --repo-id=<user/dataset>` |
| Policy fails even at the exact trained position | Pipeline bug, not a training problem: check ids, camera names, camera positions, policy path |
| Policy works at the trained position, fails elsewhere | Normal — record varied start positions (~10 regions × 10 episodes) and retrain |
| Robot freezes mid-task | Pauses in the demos, or an unseen situation → cleaner data; recovery demos |
| Servos hot or straining | Object too heavy or too far out → lighter object, work closer to the base. Signal to plan the Stage-4 arm |

[← Hardware ladder](12-hardware-ladder.md) · [README](../README.md)
