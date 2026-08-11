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
| Leader | `brick_leader` | 2026-08-10 (same) |

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
| front | Logitech StreamCam | _pending_ | _pending_ — lock focus + exposure + white balance in Logi Tune |
| wrist | InnoMaker U20CAM-1080P (32×32) | _pending_ | _pending_ — official SO-ARM101 printed mount |

## Datasets & policies

| Item | Name | Created |
|---|---|---|
| First dataset | `vik101/so101_brick_place_v1` | _pending_ |
| First policy | `vik101/act_brick_v1` | _pending_ |

## Machines

- Mac (robot machine): conda env `lerobot`, LeRobot 0.6.1, HF `vik101`, wandb `vikramt-sammy` — ready 2026-08-04
- PC "Shav" (training): 2× RTX 3090, WSL2 Ubuntu — env setup pending
