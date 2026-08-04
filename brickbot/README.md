# Brick-Laying Robot

Building toward a robot that lays **real bricks** with **robot-handleable mortar**, starting from a LeRobot **SO-101** arm and imitation learning.

> 📖 **Live illustrated guide:** the full step-by-step field guide (with diagrams) is published as an artifact:
> https://claude.ai/code/artifact/723f16cf-b18a-475d-98d6-cd401b2bf2b0
> This repo is the durable, version-controlled reference for the same material.

## The reality check

The SO-101 can lift roughly **200–500 g**. A standard clay brick weighs **1.9–2.3 kg** — four to eight times too heavy, and too wide (92 mm) for the gripper. That is fine:

- The SO-101 is the **training ground**: teleop, datasets, policy training, evaluation. Every skill transfers to a bigger arm later. Policy weights do not; pipelines and judgment do.
- Every commercial brick robot (Hadrian X, SAM100, Monumental) uses CAD plans + position control. **None uses learned policies.** The imitation-learning route is genuinely fresh ground.

## The 4-stage brick curriculum

| Stage | What | Hardware | Cost |
|---|---|---|---|
| 1 (now) | Miniature masonry: foam/printed minis → 1:12–1:6 kiln-fired clay minis; running-bond courses with even 3–5 mm gaps | SO-101 | ~$0–50 |
| 2 | Half-scale real fired bricks (250–400 g) — the SO-101's ceiling; wider printed gripper, recovery demos | SO-101 | ~$50–150 |
| 3 | Adhesive skills: servo-triggered glue-gun end effector, bead extrusion practice (hot glue → PU foam) | SO-101 → next arm | ~$100 |
| 4 | Real masonry: **AAC blocks + thin-bed/PU adhesive on AgileX PiPER (~$2.5k)**; standard clay brick needs Unitree Z1 (~$15k) / UR5e ($30k+) | PiPER / Z1 / UR5e | $3k–40k |

Details: [docs/10-brick-curriculum.md](docs/10-brick-curriculum.md)

## Current status

**Stage 1.** Progress checklist (tick as completed):

- [ ] Phase 0 — kit sorted, power supplies labeled, extras ordered
- [ ] Phase 1 — Mac: LeRobot installed, HF account + `hf auth login`
- [x] Training PC ready — WSL2 + Ubuntu, **2× RTX 3090 (24 GB each)**, driver verified via `nvidia-smi` (2026-08-04)
- [ ] Training PC — `lerobot[training]` installed in a fresh conda env + `hf auth login`
- [ ] Phase 2 — ports found, 12 motor IDs programmed, arms assembled, both arms calibrated
- [ ] Phase 3 — teleop works, cameras mounted and framed, everything fixed in place
- [ ] Phase 4 — 50-episode dataset recorded and replay-checked
- [ ] Phase 5 — first ACT policy trained, loss flattened
- [ ] Phase 6 — rollout succeeds at trained position 8+/10

Next action: [Phase 0 — prepare the kit](docs/03-phase0-prepare.md).

## Hardware inventory

- SO-101 leader arm + follower arm, full kit, **disassembled** (Partabot, [SO-ARM101](https://partabot.com/products/so-arm101))
- 12× Feetech STS3215 servos (6 per arm; check voltage variants — see Phase 0)
- 2× bus-servo control boards, USB-C cables, power supplies
- Still to buy: 2× USB webcams, powered USB hub, table clamp, wrist camera mount, foam/mini bricks
- Training machine: PC "Shav" with **2× NVIDIA RTX 3090 (24 GB VRAM each)**, WSL2 + Ubuntu already set up, reachable from the Macs over SSH (`ssh shav@<pc-ip>`). Mac drives the arms; PC trains. See Phase 5.
- Front camera: Logitech StreamCam (from home) — lock its autofocus via Logi Tune before recording. Wrist camera: use the kit's camera if it is a small board cam; otherwise buy a small wide-angle fixed-focus UVC board cam (~$30, e.g. InnoMaker 130°).

## Repo map

### The guide (follow in order)

| Doc | Contents |
|---|---|
| [00 — Glossary](docs/00-glossary.md) | Plain-language definitions of every term used |
| [01 — Concepts](docs/01-concepts.md) | How imitation learning, teleop, ACT, and chunking work |
| [02 — Version drift](docs/02-version-drift.md) | ⚠️ Old tutorials are everywhere — command translation table |
| [03 — Phase 0: Prepare](docs/03-phase0-prepare.md) | Sort the kit, power-supply warning, gear codes, shopping list |
| [04 — Phase 1: Software](docs/04-phase1-software.md) | Miniconda → LeRobot → Hugging Face account |
| [05 — Phase 2: Build & calibrate](docs/05-phase2-build-calibrate.md) | Ports, motor IDs, assembly, calibration |
| [06 — Phase 3: Teleop & cameras](docs/06-phase3-teleop-cameras.md) | Drive the robot by hand, set up cameras, frame the scene |
| [07 — Phase 4: Recording](docs/07-phase4-recording.md) | Record ~50 demonstrations, quality-check, upload |
| [08 — Phase 5: Training](docs/08-phase5-training.md) | Train the ACT policy (RTX PC via WSL2 recommended; Colab/HF Jobs fallback) |
| [09 — Phase 6: Rollout](docs/09-phase6-rollout.md) | Run the policy, evaluate it the right way |
| [10 — Brick curriculum](docs/10-brick-curriculum.md) | Stages 1–4 in full detail |
| [11 — Mortar research](docs/11-mortar-research.md) | What the industry uses instead of mortar |
| [12 — Hardware ladder](docs/12-hardware-ladder.md) | Arm comparison: SO-101 → PiPER → Z1 → UR5e |
| [13 — Troubleshooting](docs/13-troubleshooting.md) | Symptom → cause → fix table |

### Reference

| File | Contents |
|---|---|
| [reference/research-notes.md](reference/research-notes.md) | Condensed research notes with all source URLs |
| [reference/advanced-robotics-repo-review.md](reference/advanced-robotics-repo-review.md) | Review of the cloned Trelis ADVANCED-robotics repo (`~/Code/sammy/ADVANCED-robotics`) |
| [reference/transcripts/](reference/transcripts/index.md) | Cleaned transcripts of the Trelis Research 3-part video series |

## Conventions used throughout

- Robot ids: `brick_follower` / `brick_leader` (chosen at calibration; must never change)
- Camera names: `front` / `wrist` at 640×480 @ 30 fps
- First dataset: `<HF_USER>/so101_brick_place_v1`, task string `"Pick up the brick and place it on the target square"`
- First policy: `<HF_USER>/act_brick_v1`
- Placeholders `FOLLOWER_PORT` / `LEADER_PORT` are your USB port paths from Phase 2

*Compiled 2026-08-04 against LeRobot v0.6.1. If a command errors, check [version drift](docs/02-version-drift.md) first.*
