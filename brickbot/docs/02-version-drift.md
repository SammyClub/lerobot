# 02 — Warning: old instructions are everywhere

[← Concepts](01-concepts.md) · [README](../README.md) · [Next: Phase 0 →](03-phase0-prepare.md)

LeRobot changed a lot in 2025–2026. Most tutorials on the internet — **including the Trelis videos and the cloned `~/Code/sammy/ADVANCED-robotics` repo** — show commands that no longer exist. That repo's *advice* is excellent. Its *commands* are from mid-2025, and many rely on the author's personal fork of LeRobot.

**The rule:** take commands from this repo's docs. Take technique and understanding from the videos. Translate anything else with this table.

## Translation table (mid-2025 → LeRobot v0.6.x)

| Videos / Trelis repo say | Type this instead |
|---|---|
| `python lerobot/find_port.py` | `lerobot-find-port` |
| `python -m lerobot.setup_motors` | `lerobot-setup-motors` |
| `python -m lerobot.calibrate` | `lerobot-calibrate` |
| `python -m lerobot.teleoperate` | `lerobot-teleoperate` |
| `python -m lerobot.find_cameras` | `lerobot-find-cameras opencv` |
| `python -m lerobot.record` / `.replay` | `lerobot-record` / `lerobot-replay` |
| `python lerobot/scripts/train.py` | `lerobot-train` |
| Evaluate by "recording with a policy" (`lerobot.record --policy.path=…`) | `lerobot-rollout` |
| `huggingface-cli login` | `hf auth login` |
| Python 3.10, clone repo, `pip install -e .` | Python 3.12, `pip install 'lerobot[…]'` |

## Trelis-fork-only flags — do not use, they don't exist upstream

- `--validation_freq`, `--validation_ratio`, `--max_validation_episodes` (validation split)
- `--robot.p_coefficient`, `--robot.d_coefficient` (PID gains on the CLI)
- KL-weight annealing options (`kl_weight_annealing`, ramp start/end)
- `--policy.type=remote` / `lerobot serve` (speculative remote inference)

## Other era markers of a stale tutorial

- Mentions `control_robot.py` or `--control.type=teleoperate/record` → 2024/early-2025, pre-refactor. Close the tab.
- Tells you to **remove gears from servos** → that's the older SO-100 leader arm. The SO-101 never needs this.
- Uses `--dataset.vcodec` → renamed to `--dataset.rgb_encoder.vcodec` in v0.6.0.
- Dataset in v2.1 format fails on lerobot ≥ 0.4: convert with `python -m lerobot.datasets.v30.convert_dataset_v21_to_v30 --repo-id=<user/dataset>`.

## Version facts (as of 2026-08-04)

- Latest release: **v0.6.1** (2026-08-03). Requires Python ≥ 3.12, PyTorch ≥ 2.7.
- Dataset format: **LeRobotDataset v3**.
- Base `pip install lerobot` is core-only since v0.6.0 — extras are mandatory for real work.

[← Concepts](01-concepts.md) · [README](../README.md) · [Next: Phase 0 →](03-phase0-prepare.md)
