# Review: the cloned ADVANCED-robotics repo

Location: `~/Code/sammy/ADVANCED-robotics`. Reviewed 2026-08-04.

## What it is

Companion repo by **Trelis Research (Ronan McGovern)** for the 3-part LeRobot video series ([transcripts here](transcripts/index.md)). Robot: SO-101 leader/follower pair. Last commit Nov 2025; active window Jun–Nov 2025. `Build_vs_Buy/` covers sourcing/printing an arm — not relevant to this project.

## What it teaches (the good part)

`Training/` walks the full workflow: environment setup → ports → motor IDs → calibration → teleop (`Teleop.md`) → record/replay (`Data-Preparation.md`) → ACT training (`train-ACT.md`, the most polished doc) → SmolVLA fine-tune (`train-SmolVLA.md`) → experiment log (`Experiments.md`) → policy-failure flowchart (`troubleshooting.md`). The *methodology* — dataset discipline, hyperparameter reasoning, exact-replica-first evaluation — is excellent and is baked into this repo's `docs/`.

Useful extras:
- `trelis-utils/test_camera_resolutions.py` — standalone OpenCV camera prober (pure cv2, still usable).
- `troubleshooting.md` decision tree: works-at-exact-position → data-breadth issue; stuck-everywhere → idle-collapse issue.

## The fork problem (the main caveat)

The repo pins a **custom fork** (`TrelisResearch/lerobot`, submodule commit `454570a6…`, **not initialized** — the `Training/lerobot/` dir is empty). Fork-only features that do NOT exist in upstream LeRobot:

- Validation split: `--validation_freq`, `--validation_ratio`, `--max_validation_episodes`
- KL-weight annealing for ACT
- PID gains as CLI flags: `--robot.p_coefficient`, `--robot.d_coefficient`
- A recording episode-index bug fix and a SmolVLA normalization fix (both likely fixed upstream since)

## Staleness inventory (things that will bite)

1. **CLI era:** all commands are mid-2025 style (`python -m lerobot.record`, `python lerobot/scripts/train.py`). Current LeRobot uses `lerobot-*` commands — see [docs/02-version-drift.md](../docs/02-version-drift.md).
2. **Hardcoded personal values:** `HF_USER=Trelis`, ports `/dev/tty.usbmodem5A680105831` / `…87561`, `/Users/ronanmcgovern/.cache/...` paths, camera indices 0/1.
3. **Version pins:** `numpy<2`, `ffmpeg=7`, a `datasets>=4.0.0` TypeError workaround via manual source edit, `flash-attn==2.7.1.post4` (GR00T notebook).
4. **Frozen doc PDFs** in `Training/resources/` (June 23, 2025 snapshots of HF docs) — deliberately frozen; live docs have moved on.
5. **Incomplete docs:** `train-pi0.md` never actually covers pi0 (it repeats the ACT pipeline); `train-SmolVLA.md` has an explicit "NEEDS UPDATING!!!" block; `remote-inference/` references files that don't exist (aspirational).
6. **`Finetuning_GrootN1/`** targets the SO-100 (not 101) with a pre-refactor LeRobot API, and its eval client defaults to a long-dead RunPod IP (`69.30.85.120:5555`).
7. RunPod one-click template links are affiliate links that may no longer exist.

## How to use it now

- **Read** `train-ACT.md`, `Experiments.md`, and `troubleshooting.md` for reasoning and technique.
- **Do not run** its commands or install its fork; use this repo's [docs/](../docs/) instead.
- The validation-split idea is genuinely useful and absent upstream — approximate it by watching the train-loss elbow, or hold out episodes manually.
