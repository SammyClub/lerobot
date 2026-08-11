# 08 — Phase 5: Train the policy

[← Phase 4](07-phase4-recording.md) · [README](../README.md) · [Next: Phase 6 →](09-phase6-rollout.md)

**Goal:** a trained ACT policy, stored on the Hugging Face Hub.

**Plan of record (2026-08-11):** training runs on a **rented cloud A100 via Hugging Face Jobs**, paid per second from the sammy-labs org credit. Everything launches from the Mac; no other machine is involved. (The earlier RTX-PC plan is retired.)

## The workflow

```
Mac (arms + cameras)          Hugging Face Hub              HF Jobs (cloud A100)
────────────────────          ────────────────              ────────────────────
record dataset  ──────────▶   dataset repo   ──────────▶   job pulls it, trains
rollout policy  ◀──────────   policy repo    ◀──────────   policy + checkpoints push back
```

Nothing to install, maintain, or SSH into. Billing runs only while a job runs; `hf jobs cancel` stops both.

## Where to train — priority order

| Priority | Option | When | Time (50k-step-equivalent) |
|---|---|---|---|
| **1 — recommended** | **HF Jobs, A100** — `--job.target=a100-large` (or click-launch inside LeLab with live charts) | Default | ~30–60 min |
| 2 | HF Jobs, A10G — `--job.target=a10g-small` | Cheaper first test runs | ~1–2 h |
| 3 | Google Colab — [official ACT notebook](https://colab.research.google.com/github/huggingface/notebooks/blob/main/lerobot/training-act.ipynb) | Jobs unavailable | ~1–3 h |
| 4 — last resort | Mac locally, `--policy.device=mps` | Nothing else available | overnight |

## One-time check (on the Mac)

Credits live in the [sammy-labs org](https://huggingface.co/sammy-labs); jobs must run under that namespace (the `HF_NAMESPACE` prefix in the command below) so billing lands on the org, not your personal account — after the first run, confirm the job appears on the org's Jobs page. Your org membership needs write permission, and a fine-grained token must include sammy-labs access (403 on push = recreate token with org scope). Confirm access and hardware flavors + prices:

```bash
hf jobs hardware
```

Find the A100 entry. These docs assume the flavor is named `a100-large` — if the listing differs, use the listed name. Companions: `hf jobs logs <job-id>` (stream output), `hf jobs cancel <job-id>` (stop + stop billing), `--job.timeout=4h` (runaway guard).

## Weights & Biases

Account exists (`vikramt-sammy`), Mac is logged in — the API key is forwarded to the cloud job automatically. Live charts appear on wandb.ai while the job runs.

## The training command (run on the Mac)

```bash
HF_NAMESPACE=sammy-labs lerobot-train \
  --dataset.repo_id=sammy-labs/so101_brick_place_v1 \
  --policy.type=act \
  --policy.chunk_size=50 \
  --policy.n_action_steps=15 \
  --output_dir=outputs/train/act_brick_v1 \
  --job_name=act_brick_v1 \
  --job.target=a100-large \
  --job.timeout=4h \
  --batch_size=32 \
  --steps=15000 \
  --wandb.enable=true \
  --policy.repo_id=sammy-labs/act_brick_v1 \
  --save_checkpoint_to_hub=true
```

- `--job.target` is what sends the run to the cloud instead of this machine. Note there is **no** `--policy.device` — the job picks its own GPU.
- The dataset comes from the Hub; a local-only dataset is auto-pushed to a private repo first.
- Chunk settings = the "predict 50, execute 15" pattern from [Concepts](01-concepts.md); they bake into the policy config at train time.
- Batch 32 / 15,000 steps suits a ~50-episode dataset on an A100 (same coverage as batch 8 / 50k, faster wall-clock). Loss usually flattens well before the end; stopping early is fine.
- `--save_checkpoint_to_hub=true` pushes mid-run checkpoints — a cancelled/crashed job loses nothing.
- Same job can be click-launched from LeLab instead, with live charts in-app.

## Read the loss, then stop

Watch the loss chart on wandb.ai: falls steeply, then flattens near zero. Flat for a long while = further steps buy nothing — **better data beats more steps, always.** Cancel a job you're done with: `hf jobs cancel <job-id>`.

## Confirm the policy is on the Hub

`--policy.repo_id` uploads the trained policy automatically. Check `huggingface.co/sammy-labs/act_brick_v1` exists. Then go to [Phase 6](09-phase6-rollout.md) — rollout happens on the Mac.

[← Phase 4](07-phase4-recording.md) · [README](../README.md) · [Next: Phase 6 →](09-phase6-rollout.md)
