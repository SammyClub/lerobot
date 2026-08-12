# 08 — Phase 5: Train the policy

[← Phase 4](07-phase4-recording.md) · [README](../README.md) · [Next: Phase 6 →](09-phase6-rollout.md)

**Goal:** a fine-tuned **NVIDIA GR00T N1.7** policy, stored on the Hugging Face Hub.

**Plan of record (2026-08-12):** fine-tune `nvidia/GR00T-N1.7-3B` — a pre-trained 3B vision-language-action model, native in LeRobot since July 2026 (`--policy.type=groot`) — on a **rented cloud A100 via Hugging Face Jobs**, paid per second from the sammy-labs org credit. Everything launches from the Mac; no other machine is involved.

## The workflow

```
Mac (arms + cameras)          Hugging Face Hub              HF Jobs (cloud A100)
────────────────────          ────────────────              ────────────────────
record dataset  ──────────▶   dataset repo   ──────────▶   job pulls it, fine-tunes GR00T
rollout policy  ◀──────────   policy repo    ◀──────────   policy + checkpoints push back
```

Nothing to install, maintain, or SSH into. Billing runs only while a job runs; `hf jobs cancel` stops both.

## Where to train — priority order

GR00T fine-tuning needs **~40 GB of VRAM**, which rules out most options:

| Priority | Option | Verdict | Time (20k steps) |
|---|---|---|---|
| **1 — the plan** | **HF Jobs, A100 (80 GB)** — `--job.target=a100-large` | Comfortably sized; billed to the org | a few hours |
| — | HF Jobs, A10G (24 GB) | **Not viable** — under the ~40 GB GR00T needs | — |
| — | Mac (Apple Silicon) | **Not viable** for fine-tuning a 3B model | — |

## One-time check (on the Mac)

Credits live in the [sammy-labs org](https://huggingface.co/sammy-labs); jobs must run under that namespace (the `HF_NAMESPACE` prefix in the command below) so billing lands on the org, not your personal account — after the first run, confirm the job appears on the org's Jobs page. Your org membership needs write permission, and a fine-grained token must include sammy-labs access (403 on push = recreate token with org scope). Confirm access and hardware flavors + prices:

```bash
hf jobs hardware
```

Find the A100 entry. These docs assume the flavor is named `a100-large` — if the listing differs, use the listed name. Companions: `hf jobs logs <job-id>` (stream output), `hf jobs cancel <job-id>` (stop + stop billing), `--job.timeout=8h` (runaway guard).

## Weights & Biases

Account exists (`vikramt-sammy`), Mac is logged in — the API key is forwarded to the cloud job automatically. Live charts appear on wandb.ai while the job runs.

## The training command (run on the Mac)

```bash
HF_NAMESPACE=sammy-labs lerobot-train \
  --dataset.repo_id=sammy-labs/brickbot_so101_wall_v1 \
  --dataset.image_transforms.enable=true \
  --policy.type=groot \
  --policy.base_model_path=nvidia/GR00T-N1.7-3B \
  --policy.embodiment_tag=new_embodiment \
  --policy.chunk_size=16 \
  --policy.n_action_steps=16 \
  --policy.use_relative_actions=true \
  --policy.relative_exclude_joints='["gripper"]' \
  --policy.use_bf16=true \
  --use_policy_training_preset=true \
  --batch_size=64 \
  --steps=20000 \
  --seed=42 \
  --output_dir=outputs/train/brickbot_groot_v1 \
  --job_name=brickbot_groot_v1 \
  --job.target=a100-large \
  --job.timeout=8h \
  --wandb.enable=true \
  --wandb.disable_artifact=true \
  --policy.push_to_hub=true \
  --policy.repo_id=sammy-labs/brickbot_groot_v1 \
  --save_checkpoint_to_hub=true
```

- `--job.target` sends the run to the cloud instead of this machine. Note there is **no** `--policy.device` — the job picks its own GPU.
- The dataset comes from the Hub; a local-only dataset is auto-pushed to a private repo first.
- **Image augmentation is ON** (`--dataset.image_transforms.enable=true`) — recommended for VLA fine-tuning, unlike from-scratch ACT where it hurt small datasets.
- Chunking: 16 predicted / 16 trained; rollout executes 8 (see [Concepts](01-concepts.md)). Actions are relative except the gripper; bf16 keeps the 3B model inside memory.
- ~20,000 steps at batch 64 is NVIDIA's reference recipe. Expect a few hours on the A100.
- `--save_checkpoint_to_hub=true` pushes mid-run checkpoints — a cancelled/crashed job loses nothing.

## Read the loss, then stop

Watch the loss chart on wandb.ai: falls steeply, then flattens. **Fine-tuning loss won't reach zero — flat is the signal, not small.** Flat for a long while = further steps buy nothing — better data beats more steps, always. Cancel a job you're done with: `hf jobs cancel <job-id>`.

## Confirm the policy is on the Hub

`--policy.repo_id` uploads the trained policy automatically. Check `huggingface.co/sammy-labs/brickbot_groot_v1` exists. Then go to [Phase 6](09-phase6-rollout.md) — rollout happens on the Mac.

## Sources

- [GR00T 1.7 in LeRobot — official workflow](https://huggingface.co/blog/nvidia/nvidia-isaac-teleop-and-gr00t17-in-lerobot)
- [nvidia/GR00T-N1.7-3B](https://huggingface.co/nvidia/GR00T-N1.7-3B)

[← Phase 4](07-phase4-recording.md) · [README](../README.md) · [Next: Phase 6 →](09-phase6-rollout.md)
