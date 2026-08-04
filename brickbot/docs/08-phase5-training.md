# 08 — Phase 5: Train the policy

[← Phase 4](07-phase4-recording.md) · [README](../README.md) · [Next: Phase 6 →](09-phase6-rollout.md)

**Goal:** a trained ACT policy, stored on the Hugging Face Hub.

## The cross-machine workflow (recommended)

You have a PC with a GeForce RTX GPU — that is the training machine. The Mac stays the robot machine. The Hugging Face Hub is the courier between them:

```
Mac (arms + cameras)          Hugging Face Hub              RTX PC (GPU)
────────────────────          ────────────────              ────────────
record dataset  ──────────▶   dataset repo   ──────────▶   lerobot-train pulls it
rollout policy  ◀──────────   policy repo    ◀──────────   trained policy pushes back
```

No robot, no cameras, no `feetech` extra needed on the PC. Everything syncs through the Hub automatically.

## Where to train — priority order

| Priority | Option | When | Time (50k steps) |
|---|---|---|---|
| **1 — recommended** | **PC "Shav": 2× RTX 3090** (WSL2 + CUDA) | Always | ~30–90 min |
| 2 | Google Colab — [official ACT notebook](https://colab.research.google.com/github/huggingface/notebooks/blob/main/lerobot/training-act.ipynb) | PC unavailable | ~1–3 h (GPU runtime) |
| 3 | HF Jobs — add `--job.target=a10g-small` to the train command | Zero-setup, pay-per-second | ~1–2 h |
| 4 — last resort | Mac locally with `--policy.device=mps` | Nothing else available | overnight |

## One-time setup on the RTX PC

> **Status (2026-08-04): partially done.** WSL2 + Ubuntu is installed and `nvidia-smi` confirms 2× RTX 3090 (24 GB each) with a current driver — the Windows/WSL2 caveat below is handled. Steps 1–7 below are **still pending**. Note: a `~/lerobot` folder already exists on the PC; leave it alone and do a clean install in its own conda env (avoids inheriting an unknown version).
>
> **Working from the Mac:** `ssh shav@<pc-ip>`, then run training inside `tmux` (`sudo apt install tmux`; detach Ctrl-B D, reattach `tmux attach`) so a dropped SSH session doesn't kill the run.

> **Windows caveat (handled on our PC):** LeRobot on native Windows has caveats. Use **WSL2 with Ubuntu** instead — then everything behaves like Linux. Install WSL2 from PowerShell with `wsl --install -d Ubuntu`, open the Ubuntu terminal, and continue there. Make sure a current NVIDIA driver is installed on Windows (WSL2 uses it automatically).

1. **Install Miniconda inside Ubuntu/WSL2** (download from https://conda-forge.org/download/, run the Linux installer, reopen the shell).
2. **Create and activate the environment:**

   ```bash
   conda create -y -n lerobot python=3.12
   conda activate lerobot
   ```

3. **Install ffmpeg:**

   ```bash
   conda install -y -c conda-forge ffmpeg
   ```

4. **Install LeRobot — training extra only** (no robot attached to this machine):

   ```bash
   pip install 'lerobot[training]'
   ```

5. **CUDA check:** `python -c "import torch; print(torch.cuda.is_available())"` should print `True`. If it prints `False` (default wheel mismatches your driver), install the matching build first:

   ```bash
   pip install --index-url https://download.pytorch.org/whl/cu128 torch torchvision
   ```

6. **Log in to the Hub on the PC** (same account as the Mac):

   ```bash
   hf auth login
   HF_USER=$(NO_COLOR=1 hf auth whoami | awk -F': *' 'NR==1 {print $2}')
   ```

## Weights & Biases (recommended)

Live charts of training progress. Sign up at https://wandb.ai, then on the training machine:

```bash
wandb login   # paste the API key from wandb.ai/authorize
```

Don't want it? Use `--wandb.enable=false` below.

## The training command (run on the RTX PC)

```bash
lerobot-train \
  --dataset.repo_id=${HF_USER}/so101_brick_place_v1 \
  --policy.type=act \
  --policy.chunk_size=50 \
  --policy.n_action_steps=15 \
  --output_dir=outputs/train/act_brick_v1 \
  --job_name=act_brick_v1 \
  --policy.device=cuda \
  --batch_size=8 \
  --steps=50000 \
  --wandb.enable=true \
  --policy.repo_id=${HF_USER}/act_brick_v1
```

- `--dataset.repo_id` pulls the dataset straight from the Hub — nothing to copy from the Mac.
- The two chunk settings are the "predict 50, execute 15" pattern from [Concepts](01-concepts.md) — they must be chosen now, at training time (they are baked into the policy config).
- 50,000 steps suits a ~50-episode dataset at batch 8. On our 24 GB RTX 3090s, raise `--batch_size` to 32 and cut `--steps` roughly in proportion (~15,000) — same data coverage, much faster wall-clock (~30–90 min).
- One 3090 is plenty; the second GPU is spare capacity, not needed for ACT.
- **Out of memory?** Lower `--batch_size` (16, 8, 4).
- Colab users: same command inside the notebook, GPU runtime enabled.
- MPS fallback: same command with `--policy.device=mps`.

## Read the loss, then stop

On the wandb page, watch the "loss" chart. Good: falls steeply, then flattens near zero. When it has been flat for a long while, further training buys nothing — **better data beats more steps, always.**

## Confirm the policy is on the Hub

Because of `--policy.repo_id`, the trained policy uploads automatically. Check that `huggingface.co/<user>/act_brick_v1` exists. If not, upload by hand from the PC:

```bash
hf upload ${HF_USER}/act_brick_v1 outputs/train/act_brick_v1/checkpoints/last/pretrained_model
```

Then walk back to the Mac for [Phase 6](09-phase6-rollout.md) — rollout happens on the robot machine.

[← Phase 4](07-phase4-recording.md) · [README](../README.md) · [Next: Phase 6 →](09-phase6-rollout.md)
