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
| 1 (now) | Miniature masonry with wooden stacking-tower blocks, policy = SmolVLA fine-tune; first task: three-block wall (yellow + pink end to end, orange bridging) → courses with even gaps → rebuild the tower; later: 1:12–1:6 kiln-fired clay minis | SO-101 | ~$0–50 |
| 2 | Half-scale real fired bricks (250–400 g) — the SO-101's ceiling; wider printed gripper, recovery demos | SO-101 | ~$50–150 |
| 3 | Adhesive skills: servo-triggered glue-gun end effector, bead extrusion practice (hot glue → PU foam) | SO-101 → next arm | ~$100 |
| 4 | Real masonry: **AAC blocks + thin-bed/PU adhesive on AgileX PiPER (~$2.5k)**; standard clay brick needs Unitree Z1 (~$15k) / UR5e ($30k+) | PiPER / Z1 / UR5e | $3k–40k |

Details: [docs/10-brick-curriculum.md](docs/10-brick-curriculum.md)

## Current status

**Stage 1.** Progress checklist (tick as completed):

- [x] Phase 0 — kit sorted, extras acquired (blocks, cameras, mounts) — complete by 2026-08-09
- [x] Phase 1 — Mac: LeRobot 0.6.1 installed in conda env `lerobot` (Python 3.12, torch 2.11 + MPS, all `lerobot-*` commands verified, 2026-08-04)
- [x] Phase 1 — HF account + `hf auth login` on the Mac (logged in as `vik101`, 2026-08-04) — **Phase 1 complete ✓**
- [x] Training compute — **sammy-labs org credit; training runs on a cloud A100 via HF Jobs under `HF_NAMESPACE=sammy-labs`** (plan changed 2026-08-11; RTX-PC plan retired)
- [x] wandb account created + logged in on the Mac as `vikramt-sammy` (2026-08-04)
- [x] Phase 2 — ports found, 12 motor IDs programmed, arms assembled, both arms calibrated (2026-08-10; calibration versioned in `hardware/calibration/`) — **Phase 2 complete ✓**
- [x] Phase 3 — teleop works, cameras mounted/framed/locked (2026-08-13) — **complete ✓**
- [x] Phase 4 — **100-episode** wall dataset recorded and pushed (2026-08-13) — **complete ✓**
- [x] Phase 5 — **SmolVLA fine-tuned: 6,000 steps on all 100 episodes, A100** (2026-08-14) → `sammy-labs/brickbot_smolvla_v1` — **complete ✓**
- [~] Phase 6 — cloud async inference pipeline VALIDATED (70 min continuous rollout, zero server errors, 2026-08-13); formal 8+/10 evaluation pending the full policy

Next action: finish [Phase 3](docs/06-phase3-teleop-cameras.md) — rehearse the wall build to the ~50 s bar, then record ([Phase 4](docs/07-phase4-recording.md)).

## Hardware inventory

- SO-101 leader arm + follower arm, full kit, **disassembled** (Partabot, [SO-ARM101](https://partabot.com/products/so-arm101))
- 12× Feetech STS3215 servos (6 per arm; check voltage variants — see Phase 0)
- 2× bus-servo control boards, USB-C cables, power supplies
- Stage-1 bricks on hand: wooden stacking-tower (Jenga-style) blocks (Flying Tiger) — ~10–20 g each, fits the gripper; later upgrade: kiln-fired 1:12 clay minis
- Training compute: **Hugging Face Jobs (cloud A100), paid from loaded HF credit** — launched from the Mac; see Phase 5. (PC "Shav" with 2× RTX 3090 exists but is no longer part of the plan.)
- Front camera: **Acer 1080p webcam** (generic UVC — lock focus/exposure/WB via CameraController or uvc-util before recording; settings may reset on replug). Wrist camera: InnoMaker U20CAM-1080P on the printed SO-ARM101 mount. Indices in [SETUP-LOG.md](SETUP-LOG.md).

## Repo map

> **Workflow convention:** everything runs from the Terminal with copy-paste commands — each phase doc gives the exact command and what to expect. Machine-specific values (ports, camera indices) live in [SETUP-LOG.md](SETUP-LOG.md).

### The guide (follow in order)

| Doc | Contents |
|---|---|
| [00 — Glossary](docs/00-glossary.md) | Plain-language definitions of every term used |
| [01 — Concepts](docs/01-concepts.md) | How imitation learning, teleop, SmolVLA, and chunking work |
| [02 — Version drift](docs/02-version-drift.md) | ⚠️ Old tutorials are everywhere — command translation table |
| [03 — Phase 0: Prepare](docs/03-phase0-prepare.md) | Sort the kit, power-supply warning, gear codes, shopping list |
| [04 — Phase 1: Software](docs/04-phase1-software.md) | Miniconda → LeRobot → Hugging Face account |
| [05 — Phase 2: Build & calibrate](docs/05-phase2-build-calibrate.md) | Ports, motor IDs, assembly, calibration |
| [06 — Phase 3: Teleop & cameras](docs/06-phase3-teleop-cameras.md) | Drive the robot by hand, set up cameras, frame the scene |
| [07 — Phase 4: Recording](docs/07-phase4-recording.md) | Record ~50 demonstrations, quality-check, upload |
| [08 — Phase 5: Training](docs/08-phase5-training.md) | Fine-tune SmolVLA (6k steps) on a cloud a10g via HF Jobs (launched from the Mac) |
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
- HF username: `vik101` (login identity). Team org: `sammy-labs` — datasets, policies, and the HF Jobs training credit all live there (org-namespace injection handled by scripts/train_wall_smolvla.py — plain HF_NAMESPACE does not work for Jobs)
- **Org demarcation rule: every repo this project pushes to `sammy-labs` is prefixed `brickbot_`** (datasets, policies, eval runs — no exceptions). Other teams share the org; the prefix is our namespace within it. A "Brick-Laying Robot" Collection on the org page groups all `brickbot_*` repos for discoverability.
- Policy: **SmolVLA** (fine-tuned from `lerobot/smolvla_base` via `--policy.path`)
- First dataset: `sammy-labs/brickbot_so101_wall_v1`, task string `"build the block wall on the green mat in the order yellow, pink, orange - yellow and pink end to end, orange on top of both."`
- First policy: `sammy-labs/brickbot_smolvla_v1`
- Placeholders `FOLLOWER_PORT` / `LEADER_PORT` are your USB port paths from Phase 2

*Compiled 2026-08-04 against LeRobot v0.6.1. If a command errors, check [version drift](docs/02-version-drift.md) first.*
