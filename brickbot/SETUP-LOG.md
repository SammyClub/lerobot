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
| First dataset | `sammy-labs/brickbot_so101_wall_v1` (three-block wall task) | COMPLETE: 100 episodes, pushed to Hub 2026-08-13 |
| First policy | `sammy-labs/brickbot_smolvla_v1` (SmolVLA fine-tune) | _pending_ — 6,000 steps on the 100-episode dataset (plan of record 2026-08-14) |
| Legacy policy | `sammy-labs/brickbot_groot_v1` (GR00T N1.7) | interim: 4k steps / 38 episodes, absolute actions — remains on the Hub as a legacy artifact; superseded by the SmolVLA plan |

## Machines

- Mac (robot machine): conda env `lerobot`, LeRobot 0.6.1, HF `vik101`, wandb `vikramt-sammy` — ready 2026-08-04
- Training: **SmolVLA fine-tune** (`lerobot/smolvla_base` via `--policy.path`) on **HF Jobs cloud a10g** (`--job.target=a10g-large`; 450M fits easily in 24 GB — checkpoints are 1–2 GB, ending the storage-quota pressure), paid from the sammy-labs org credit (org namespace injected by scripts/train_wall_smolvla.py) — plan of record since 2026-08-14. Verify flavor names/prices with `hf jobs hardware`. (PC "Shav", 2× RTX 3090 + WSL2, retired from the plan; its env setup was never completed.)
- ⚠️ Lesson (2026-08-12): the Acer A610's MANUAL white balance is broken — AWB off = strong green cast (green-ratio 1.42 vs 1.00 auto), temperature value ignored. WB must stay auto. Manual exposure works but applies a wrong stored value; `scripts/lock_front_camera.sh` binary-searches exposure to match the auto-exposure brightness baseline (found: ~46-50 under current lighting). Re-run after any lighting change.
- ⚠️ Lesson (2026-08-11): follower gripper not tracking the trigger → the leader trigger horn screw was loose (lever moved, servo shaft did not). Diagnosed by live-reading Present_Position — frozen value = mechanical decoupling. After re-seating any horn, recalibrate that arm and re-export to hardware/calibration/.
| Test dataset | `sammy-labs/brickbot_so101_wall_v1_20260812_162234` | 1 episode, 2026-08-12 — pipeline test; real dataset records as `brickbot_so101_wall_v1` with `--dataset.no_stamp=true` |
- ⚠️ Lesson (2026-08-13): GR00T rollout on Mac crashed with "Requested device 'cuda' but CUDA is not available" — upstream bug in `lerobot/policies/groot/processor_groot.py` `_target_device`: the intended CPU fallback catches AssertionError/RuntimeError but `get_safe_torch_device` raises ValueError. Patched locally (added ValueError to the except clause). NOTE: any lerobot upgrade/reinstall erases this patch — re-apply, or check if fixed upstream. Worth filing as an issue on huggingface/lerobot.
- Architecture decision (2026-08-13): Mac MPS measured at 0.6-4 Hz for GR00T 3B inference (30 Hz needed) — NOT viable. Rollout now uses CLOUD ASYNC INFERENCE: policy server on HF Jobs a10g GPU (org-billed), SSH tunnel to Mac, robot client local. Scripts: serve_policy_cloud.py / connect_policy_tunnel.sh / rollout_wall_async.sh. Server bills while running — always `hf jobs cancel` when done. SSH key vik101-brickbot registered on HF required.
- ⚠️ Lesson (2026-08-13): task sentences must NOT contain ": " — draccus parses "A: B" as a dict, and the mangled dict-repr got STORED in the dataset and trained on. Sentence changed to the dash form; tasks.parquet repaired locally + on Hub. Also: a10g-small OOM-kills loading GR00T (system RAM); use a10g-large or a100-large for the policy server.
- ⚠️ Lesson (2026-08-13): GR00T policies trained with use_relative_actions=true CANNOT be served by the async policy server (GrootN17ActionDecodeStep refuses per-step decode of relative actions → server errors on every inference, client hangs silently at "Action receiving thread starting"). All training now uses --policy.use_relative_actions=false. Diagnosed via tee-logged server (/tmp/policy_server.log over SSH) — platform log endpoint alone was not enough.
- ⚠️ Lesson (2026-08-13): recording sessions kept dying on `TimeoutError: latest frame is too old` at barely over 500 ms — a hardcoded freshness limit in camera_opencv.py `read_latest`. Patched the local env default to 1200 ms (tolerates scheduling hiccups; a truly dead camera still aborts in ~1 s). Patch is LOST on lerobot upgrade — re-apply if session-killing camera timeouts return. Also: keep the two cameras on separate USB paths (front camera direct into the Mac, wrist on the hub).
- Serving-speed fixes (2026-08-13 regroup): rollout was jerky/slow — a10g served ~0.5-1.2 chunks/s vs ~2 needed. Fixes: policy server now defaults to a100-large; `scripts/tune_policy_for_serving.py` promotes the newest checkpoint to repo root AND sets num_inference_timesteps=4 (NVIDIA deployment default; huge denoise speedup); client chunk_size_threshold 0.6→0.8. Run the tune script after every training run, before serving.
- ⚠️ Lesson (2026-08-13 evening): the FULL 20k run trained to completion but ALL uploads failed — org private-storage quota full ("Private repository storage limit reached") — weights lost with the container (~5.5 h A100 wasted). Cause: 12.6 GB models kept in triplicate + full LFS history (38 GB in brickbot_groot_v1 alone) plus ~35 GB of teammate runs. Fixed: repo deduped + history squashed (38→12.6 GB); tune script now squashes after every promotion. Rerun of full training pending. Consider making the policy repo public (weights carry no camera footage) to exit the private quota entirely.
- Note (2026-08-14): smolvla_base expects cameras named camera1/2/3. Training uses --rename_map (front→camera1, wrist→camera2; missing camera3 is fine — probed locally). At ASYNC rollout the client has no rename support, so rollout_wall_async.sh names the robot cameras camera1/camera2 directly. front/wrist naming remains the convention for RECORDING only.
- ⚠️ Lesson (2026-08-14): for `--policy.path` fine-tunes, lerobot's job wrapper ignores `--policy.repo_id` and pushes to `<user>/<job>_<timestamp>` (personal namespace!). The 6k SmolVLA model landed at vik101/brickbot_smolvla_v1_2026-08-14_11-15-09 — final model migrated to sammy-labs/brickbot_smolvla_v1 (squashed); the stamped repo is KEPT as backup (holds all six 1000-step checkpoints). train_wall_smolvla.py now pins build_repo_id to the org repo. Also note: the fine-tuned config retains camera3 as a zero-padded input — expected to serve fine with two cameras; watch the first rollout.
