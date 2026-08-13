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

Credits live in the [sammy-labs org](https://huggingface.co/sammy-labs); jobs must run under the org namespace so billing lands on the org — the training script handles this (see below). Your org membership needs write permission, and a fine-grained token must include sammy-labs access (403 on push = recreate token with org scope). Confirm access and hardware flavors + prices:

```bash
hf jobs hardware
```

Find the A100 entry. These docs assume the flavor is named `a100-large` — if the listing differs, use the listed name. Companions: `hf jobs logs <job-id>` (stream output), `hf jobs cancel <job-id>` (stop + stop billing), `--job.timeout=8h` (runaway guard).

## Weights & Biases

Account exists (`vikramt-sammy`), Mac is logged in — the API key is forwarded to the cloud job automatically. Live charts appear on wandb.ai while the job runs.

## The training command (run on the Mac)

```bash
conda run -n lerobot python scripts/train_wall_groot.py          # full run, 20,000 steps
conda run -n lerobot python scripts/train_wall_groot.py 2000     # cheap smoke test first
```

Why a script: LeRobot's job submitter has **no org-namespace option** — it always submits to the personal account (`/api/jobs/<user>`), which has no credits → `402 Payment Required`. [scripts/train_wall_groot.py](../scripts/train_wall_groot.py) injects `namespace=sammy-labs` into the job API calls, then runs the standard trainer with the full GR00T N1.7 recipe (augmentation ON, chunk 16/16, ABSOLUTE actions (async server cannot stream-decode GR00T relative actions — silent hang, diagnosed 2026-08-13), bf16, batch 64, A100-large, checkpoints pushed mid-run, policy to `sammy-labs/brickbot_groot_v1`). It streams the job logs in your terminal. After the first submission, confirm the job appears on the org's Jobs page — that's the proof it bills org credit. (`HF_NAMESPACE` does NOT work for this path — earlier docs claimed it did; corrected 2026-08-12.)

## Read the loss, then stop

Watch the loss chart on wandb.ai: falls steeply, then flattens. **Fine-tuning loss won't reach zero — flat is the signal, not small.** Flat for a long while = further steps buy nothing — better data beats more steps, always. Cancel a job you're done with: `hf jobs cancel <job-id>`.

## Confirm the policy is on the Hub

`--policy.repo_id` uploads the trained policy automatically. Check `huggingface.co/sammy-labs/brickbot_groot_v1` exists. Then go to [Phase 6](09-phase6-rollout.md) — rollout happens on the Mac.

## Sources

- [GR00T 1.7 in LeRobot — official workflow](https://huggingface.co/blog/nvidia/nvidia-isaac-teleop-and-gr00t17-in-lerobot)
- [nvidia/GR00T-N1.7-3B](https://huggingface.co/nvidia/GR00T-N1.7-3B)

[← Phase 4](07-phase4-recording.md) · [README](../README.md) · [Next: Phase 6 →](09-phase6-rollout.md)
