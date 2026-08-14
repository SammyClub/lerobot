# 08 — Phase 5: Train the policy

[← Phase 4](07-phase4-recording.md) · [README](../README.md) · [Next: Phase 6 →](09-phase6-rollout.md)

**Goal:** a fine-tuned **SmolVLA** policy, stored on the Hugging Face Hub.

**Plan of record (2026-08-14):** fine-tune `lerobot/smolvla_base` — Hugging Face's pre-trained 450M vision-language-action model — for **6,000 steps** on the 100-episode wall dataset, on a **rented cloud a10g via Hugging Face Jobs**, paid per second from the sammy-labs org credit. Everything launches from the Mac; no other machine is involved. (SmolVLA replaced GR00T N1.7: it trains on a 24 GB GPU instead of an A100, its checkpoints are 1–2 GB instead of 12.6 GB — which ended the storage-quota pain — and it has none of GR00T's async-serving incompatibilities.)

## The workflow

```
Mac (arms + cameras)          Hugging Face Hub              HF Jobs (cloud a10g)
────────────────────          ────────────────              ────────────────────
record dataset  ──────────▶   dataset repo   ──────────▶   job pulls it, fine-tunes SmolVLA
rollout policy  ◀──────────   policy repo    ◀──────────   policy + checkpoints push back
```

Nothing to install, maintain, or SSH into. Billing runs only while a job runs; `hf jobs cancel` stops both.

## Where to train — priority order

SmolVLA (450M params) fine-tunes comfortably in 24 GB of VRAM:

| Priority | Option | Verdict | Time (6k steps) |
|---|---|---|---|
| **1 — the plan** | **HF Jobs, a10g** — `--job.target=a10g-large` | Comfortable fit; billed to the org | ~1.5–2 h |
| 2 | HF Jobs, A100 — `--job.target=a100-large` | Faster, pricier; unnecessary at this model size | ~1 h |
| 3 | Mac (Apple Silicon) — `--policy.device=mps` | Possible for SmolVLA but slow; cloud is the plan | overnight |

## One-time check (on the Mac)

Credits live in the [sammy-labs org](https://huggingface.co/sammy-labs); jobs must run under the org namespace so billing lands on the org — the training script handles this (see below). Your org membership needs write permission, and a fine-grained token must include sammy-labs access (403 on push = recreate token with org scope). Confirm access and hardware flavors + prices:

```bash
hf jobs hardware
```

Find the a10g entry. These docs assume the flavor is named `a10g-large` — if the listing differs, use the listed name. Companions: `hf jobs logs <job-id>` (stream output), `hf jobs cancel <job-id>` (stop + stop billing), `--job.timeout=6h` (runaway guard).

## Weights & Biases

Account exists (`vikramt-sammy`), Mac is logged in — the API key is forwarded to the cloud job automatically. Live charts appear on wandb.ai while the job runs.

## The training command (run on the Mac)

```bash
conda run -n lerobot python scripts/train_wall_smolvla.py          # full run, 6,000 steps
conda run -n lerobot python scripts/train_wall_smolvla.py 1000     # cheap smoke test
```

Why a script: LeRobot's job submitter has **no org-namespace option** — it always submits to the personal account (`/api/jobs/<user>`), which has no credits → `402 Payment Required`. [scripts/train_wall_smolvla.py](../scripts/train_wall_smolvla.py) injects `namespace=sammy-labs` into the job API calls, then runs the standard trainer with the SmolVLA recipe: fine-tune from `lerobot/smolvla_base` (`--policy.path`, not a from-scratch policy type), batch 64, 6,000 steps, checkpoints pushed to the Hub mid-run (the reliable path — final pushes have failed before), policy landing at `sammy-labs/brickbot_smolvla_v1`. It streams the job logs in your terminal. After the first submission, confirm the job appears on the org's Jobs page — that's the proof it bills org credit. (`HF_NAMESPACE` does NOT work for this path — earlier docs claimed it did; corrected 2026-08-12.)

## After training: prep for serving

```bash
conda run -n lerobot python scripts/tune_policy_for_serving.py
```

Promotes the newest checkpoint's files to the repo root (immune to final-push failures) and squashes the repo history to a single revision so checkpoints never re-create the storage-quota problem.

## Read the loss, then stop

Watch the loss chart on wandb.ai: falls steeply, then flattens. **Fine-tuning loss won't reach zero — flat is the signal, not small.** Flat for a long while = further steps buy nothing — better data beats more steps, always. Cancel a job you're done with: `hf jobs cancel <job-id>`.

## Confirm the policy is on the Hub

Check `huggingface.co/sammy-labs/brickbot_smolvla_v1` exists (the tune script prints the promoted state). Then go to [Phase 6](09-phase6-rollout.md) — rollout happens on the Mac.

## Sources

- [SmolVLA fine-tuning docs](https://huggingface.co/docs/lerobot/smolvla)
- [lerobot/smolvla_base](https://huggingface.co/lerobot/smolvla_base)

[← Phase 4](07-phase4-recording.md) · [README](../README.md) · [Next: Phase 6 →](09-phase6-rollout.md)
