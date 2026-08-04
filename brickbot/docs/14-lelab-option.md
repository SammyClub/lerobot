# The LeLab option — the same workflow, as an app

[← Phase 6: Rollout](09-phase6-rollout.md) · [README](../README.md) · [Brick curriculum →](10-brick-curriculum.md)

[LeLab](https://huggingface.co/docs/lerobot/main/en/lelab) is Hugging Face's official web GUI on top of LeRobot. It replaces most of the terminal commands in Phases 2c–6 with guided, clickable flows — and its only supported robot is the SO-ARM101, which is exactly ours. It uses the same calibration files, datasets, and Hub as the CLI, so you can switch between GUI and terminal freely.

## Install (on the Mac)

1. **Install uv** (a Python tool manager), if not present:

   ```bash
   brew install uv
   ```

2. **Install and launch LeLab:**

   ```bash
   uv tool install git+https://github.com/huggingface/leLab.git && lelab
   ```

   It opens in the browser. From then on, just type `lelab` in any terminal to start it.

## What it replaces — and what stays in the terminal

| In LeLab (clickable) | Still in the terminal |
|---|---|
| Calibration — guided joint-by-joint flow (Phase 2c) | **Motor-ID programming** (Phase 2b) — the one-time, one-servo-at-a-time step for a disassembled kit |
| Teleoperation — live 3D view of both arms (Phase 3) | **Training on the 3090 PC** — LeLab's "local training" means the Mac it runs on; the PC path stays CLI (or pick HF Jobs inside LeLab) |
| Recording — task, episode count, durations in a form; spacebar to advance (Phase 4) | **Debugging** — vanished ports, swapped cameras, weird calibration: the CLI's verbose output is how you diagnose |
| Training locally or on HF Jobs, with live charts (Phase 5) | |
| Running a trained policy in one click (Phase 6) | |

## Recommended hybrid workflow

Do Phases 0–2b (assembly + motor IDs) from this guide. Then try LeLab for calibration, teleop, and recording — if it feels good, live in it day to day. Train on the 3090 PC via the [Phase 5](08-phase5-training.md) command (or HF Jobs from inside LeLab). Drop back to the terminal whenever something misbehaves. Either way, read Phases 2–6 once: they explain what the buttons do, and that understanding is what gets you unstuck.

## Sources

- Official docs: https://huggingface.co/docs/lerobot/main/en/lelab
- Source / issues: https://github.com/huggingface/leLab
