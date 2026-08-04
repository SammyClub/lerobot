# Research notes (condensed, with sources)

Compiled 2026-08-04 from four parallel research streams. These notes make the claims in `docs/` traceable.

## 1. LeRobot framework (official docs)

- Latest release **v0.6.1 (2026-08-03)**; v0.6.0 Jul 2026, v0.5.x Mar–Apr 2026, v0.4.x Oct 2025–Feb 2026. Python ≥ 3.12 (since v0.5.0), PyTorch ≥ 2.7 (since v0.6.0). Source: https://pypi.org/project/lerobot/ · https://github.com/huggingface/lerobot/releases
- All workflows use `lerobot-*` console entry points. `lerobot-rollout` (v0.6.0) replaces eval-via-record. v0.6.0 renamed `--dataset.vcodec` → `--dataset.rgb_encoder.vcodec`; v0.6.1 renamed `lerobot.types` → `lerobot.lerobot_types`.
- Base `pip install lerobot` is core-only since v0.6.0; extras: `[core_scripts]`, `[training]`, `[feetech]`, `[smolvla]`, `[async]`, `[all]`.
- Dataset format **v3** (breaking vs v2.1; converter: `python -m lerobot.datasets.v30.convert_dataset_v21_to_v30`). Blog: https://huggingface.co/blog/lerobot-datasets-v3
- Hub login: `hf auth login` (old `huggingface-cli login` deprecated).
- Training defaults (from `src/lerobot/configs/train.py`): steps=100k, batch_size=8, log_freq=200, save_freq=20k. ACT 100k steps ≈ 1.5 h on A100 @ batch 64 (official notebook figure).
- Cloud: official Colab notebooks (ACT, SmolVLA) at https://huggingface.co/docs/lerobot/notebooks; **HF Jobs** via `--job.target=a10g-small`.
- ffmpeg: `conda install -c conda-forge ffmpeg` needed for PyTorch < 2.10 (TorchCodec); fallback pin `ffmpeg=7.1.1`.
- CUDA wheels: PyPI torch default cu130 (driver ≥ 580.65); override `pip install --index-url https://download.pytorch.org/whl/cu128 torch torchvision`.
- Docs: https://huggingface.co/docs/lerobot/so101 · /installation · /il_robots · /cameras · /smolvla · /async

## 2. SO-101 hardware

- Canonical repo: https://github.com/TheRobotStudio/SO-ARM100 (SO-101 lives there; SO-100 deprecated). Kit vendors: Seeed, WowRobo, **Partabot** (US), Autodiscovery (EU).
- Servos: Feetech STS3215, 6 per arm. **7.4V variant** ~16.5 kg·cm (5V supply) vs **12V variant** ~30 kg·cm (12V 5A supply). Mixed "Pro" kits: 12V follower + 7.4V leader → **5V supply to leader, 12V to follower, always** (Seeed wiki warning: https://wiki.seeedstudio.com/lerobot_so100m/).
- Follower gearing: 6× 1/345 (C001). Leader mixed: shoulder pan 1/191 (C044), shoulder lift 1/345 (C001), elbow 1/191 (C044), wrist flex/roll + gripper 1/147 (C046).
- Payload: ~500 g nominal near base (https://www.roboticscenter.ai/hardware/so-101); usable 200–300 g at extension (community consensus). Reach ~450–500 mm. No repeatability spec (hobby grade, few mm).
- BOM ~$230 for both arms excl. printing; assembled kits ~$300–500.
- SO-101 vs SO-100: no gear removal needed on leader; better wiring.

## 3. Trelis Research video series (technique)

- Part 1 (JjCUX4sxrJQ): hardware overview, leader-follower is PID (no AI), model I/O (2 images + 6 joint positions → action chunk), ACT vs GR00T vs π0 taxonomy.
- Part 2 (ZW8OiBGAe0M): realtime/delay/style challenges; ACT's CVAE style encoder & KL weight; GR00T latent-action learning from unlabeled video; π0 bidirectional attention.
- Part 3 (-tkEMLOLEwo): full live ACT run on a MacBook M4 + RunPod H100. Key tips: watch camera feeds not the robot; replay every episode; 16 episodes minimum-viable, 50 recommended, 100+ before augmentation; augmentation off under ~100 episodes (models fail outright); chunk 50 / execute 15 most robust (ensembling made it worse live); steps ≈ 5–10 epochs over frames ÷ batch; validation-loss elbow at 4–6k steps on a 16-episode set; exact-replica eval must succeed before probing generalization; ~10 demos per start region for coverage.
- Timing: ~1k steps per 5–10 min on M4 (MPS); 30k steps ≈ 30 min on H100.

## 4. Brick / masonry domain

- Brick weights: US standard clay 1.9–2.3 kg (https://civilsir.com/weight-of-a-brick/); UK/engineering 2.3–3.8 kg; AAC 600×200×100 @ 550–650 kg/m³ ≈ 7–8 kg; AAC cut to brick format ≈ 1.0–1.1 kg; half-scale fired clay ≈ 250–400 g (computed @ 1900–2100 kg/m³); 1:12 kiln-fired minis: grams (https://miniatures.com/products/miniature-red-bricks-kiln-fired-clay-285-pieces-1-12-scale-covers-72-sq-inches).
- Industry: FBR Hadrian X — adhesive not mortar, US$2M/unit CRH option Jan 2025 (https://www.fbr.com.au/); Monumental — extruded real mortar, 3-robot cell, $32M Series B Jul 2026 (https://tech.eu/2026/07/15/monumental-secures-32m-series-b-to-accelerate-construction-automation/); SAM100 — pumped mortar + human finishing (https://www.construction-robotics.com/sam-2/).
- AAC thin-bed: ASTM C1660, 1–3 mm joints, ±1 mm block tolerance (https://imiweb.org/wp-content/uploads/2015/10/01.02-AAC-MASONRY-UNITS.pdf). PU masonry foam: Porotherm Dryfix, Tytan (https://tytan.com/en/product/foam-adhesives/foam-adhesive-for-bricklaying/).
- No commercial system uses learned policies; academic only: RL dry-stacking (15th Canadian Masonry Symposium 2025), force-based IL (arXiv 2501.14942), GAIL long-horizon construction.
- Arm ladder: AgileX PiPER 1.5 kg / $2,499 (https://global.agilex.ai/products/piper); ARX R5/X5 ~1.5 kg / $5–10k; Unitree Z1 Pro 4 kg / ~$15k (https://shop.unitree.com/products/unitree-z1); UR5e 5 kg / $30–45k.

## Flagged as unverified

- Per-arm assembly time (~1–2 h is community lore)
- Exact Colab free-tier T4 slowdown factor
- Current street prices for assembled kits and arms (check vendor pages)
