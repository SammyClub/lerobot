# Hardware setup log

Live record of every machine-specific value for this build. Single source of truth — commands in the docs get their real values from here.

## USB serial ports (Phase 2a)

| Arm | Port | Recorded | Notes |
|---|---|---|---|
| Follower | `/dev/tty.usbmodem5AE60824171` | 2026-08-09 | keep in the same physical USB socket |
| Leader | `/dev/tty.usbmodem5B3E0891281` | 2026-08-09 | keep in the same physical USB socket |

## Arm identities (Phase 2c)

| Arm | Calibration name | Calibrated on |
|---|---|---|
| Follower | `brick_follower` | 2026-08-10 (by teammate, terminal route; imported to Vikram's Mac same day) |
| Leader | `brick_leader` | 2026-08-11 — recalibrated (terminal route) after fixing a loose trigger horn screw; trigger range 2024–3458 |

Calibration files are versioned in [`hardware/calibration/`](hardware/calibration/) — to calibrate any new machine, copy that folder to `~/.cache/huggingface/lerobot/calibration/`. Recalibrate only if the arms are mechanically altered; then re-export to the repo.

## Servos (Phase 2b)

- Power supplies: _pending — record which supply (5V/12V or identical) goes to which arm_
- ⚠️ Lesson (2026-08-09): boards must go into a DATA USB-C port on the Mac — one of the Mac's ports is power-only and causes "Motor not found". Use the same ports as during setup, always.
- ⚠️ Lesson (2026-08-11): the desk extension strip has at least one bad socket — caused hours of intermittent "0/6 motors found" errors alternating between arms as plugs were shuffled. Robot power bricks now go into known-good sockets only; suspect socket taped over. Note: the control-board LED lights from USB alone, so a lit LED does NOT prove servo power is present. Diagnostic that settles any recurrence: `FeetechMotorsBus.scan_port(port)` per board — 6 IDs = bus healthy.
- Follower motor IDs 1–6 programmed: **done 2026-08-09**
- Leader motor IDs 1–6 programmed (gear codes: 1=C044, 2=C001, 3=C044, 4=C046, 5=C046, 6=C046): **done 2026-08-09**

## Cameras (Phase 3)

| Camera | Model | Index / path | Mounted |
|---|---|---|---|
| front (main) | Acer 1080p webcam (B0GJD6PHTZ) | **0** (recorded 2026-08-12) | _pending_ — fixed-focus; lock via `scripts/lock_front_camera.sh` each session — auto-calibrates manual exposure to match auto baseline; WB stays AUTO (manual WB broken, see lesson) |
| wrist | InnoMaker U20CAM-1080P (32×32) | **1** (recorded 2026-08-12) | _pending_ — official SO-ARM101 printed mount |

⚠️ Note: this is the REVERSE of the guide's original examples (which assumed front=1, wrist=0). All doc examples were flipped to match on 2026-08-12. Indices can reshuffle if cameras change USB sockets — re-check with `lerobot-find-cameras opencv` after any replug.

## Datasets & policies

| Item | Name | Created |
|---|---|---|
| First dataset | `sammy-labs/brickbot_so101_wall_v1` (three-block wall task) | recording in progress — 38/100 episodes as of 2026-08-12 |
| First policy | `sammy-labs/brickbot_groot_v1` (GR00T N1.7 fine-tune) | interim v1: 4,000 steps on 38 episodes, org A100 via HF Jobs, 1h41m clean run (2026-08-12). Full 20k run pending 100 episodes. |

## Machines

- Mac (robot machine): conda env `lerobot`, LeRobot 0.6.1, HF `vik101`, wandb `vikramt-sammy` — ready 2026-08-04
- Training: **GR00T N1.7 fine-tune** (`nvidia/GR00T-N1.7-3B`, `--policy.type=groot`) on **HF Jobs cloud A100** (`--job.target=a100-large`; GR00T needs ~40 GB VRAM, so the 80 GB A100 is the only viable Jobs flavor), paid from the sammy-labs org credit (org namespace injected by scripts/train_wall_groot.py) — plan of record since 2026-08-12. Verify flavor names/prices with `hf jobs hardware`. (PC "Shav", 2× RTX 3090 + WSL2, retired from the plan; its env setup was never completed.)
- ⚠️ Lesson (2026-08-12): the Acer A610's MANUAL white balance is broken — AWB off = strong green cast (green-ratio 1.42 vs 1.00 auto), temperature value ignored. WB must stay auto. Manual exposure works but applies a wrong stored value; `scripts/lock_front_camera.sh` binary-searches exposure to match the auto-exposure brightness baseline (found: ~46-50 under current lighting). Re-run after any lighting change.
- ⚠️ Lesson (2026-08-11): follower gripper not tracking the trigger → the leader trigger horn screw was loose (lever moved, servo shaft did not). Diagnosed by live-reading Present_Position — frozen value = mechanical decoupling. After re-seating any horn, recalibrate that arm and re-export to hardware/calibration/.
| Test dataset | `sammy-labs/brickbot_so101_wall_v1_20260812_162234` | 1 episode, 2026-08-12 — pipeline test; real dataset records as `brickbot_so101_wall_v1` with `--dataset.no_stamp=true` |
