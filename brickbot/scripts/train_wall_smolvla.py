"""Fine-tune SmolVLA on the wall dataset via HF Jobs, billed to sammy-labs.

Plan of record since 2026-08-14 (replaces GR00T N1.7): SmolVLA is HF's 450M
vision-language-action model — fine-tuned from lerobot/smolvla_base. Wins vs
GR00T for this project: trains on a10g (cheaper), ~1-2 GB checkpoints (no more
storage-quota pain), and no relative-action async-serving incompatibility.

Same org-namespace monkeypatch as before (lerobot's job submitter has no
namespace option; personal account would be billed -> 402).

Usage:
    conda run -n lerobot python scripts/train_wall_smolvla.py          # 6000 steps (plan)
    conda run -n lerobot python scripts/train_wall_smolvla.py 1000     # smoke test
"""

import sys

import lerobot.jobs.hf as jobs_hf

NAMESPACE = "sammy-labs"


def _with_namespace(fn):
    def patched(*args, **kwargs):
        kwargs.setdefault("namespace", NAMESPACE)
        return fn(*args, **kwargs)
    return patched


for _name in ("run_job", "inspect_job", "fetch_job_logs"):
    setattr(jobs_hf, _name, _with_namespace(getattr(jobs_hf, _name)))

# Second upstream wart (2026-08-14): for --policy.path fine-tunes the job wrapper
# IGNORES --policy.repo_id and builds "<user>/<job>_<stamp>" instead. Pin it:
jobs_hf.build_repo_id = lambda username, base_name, now: "sammy-labs/brickbot_smolvla_v1"

steps = sys.argv[1] if len(sys.argv) > 1 else "6000"

sys.argv = [
    "lerobot-train",
    "--dataset.repo_id=sammy-labs/brickbot_so101_wall_v1",
    # smolvla_base was pretrained with cameras named camera1/2/3; our dataset
    # says front/wrist. rename_map alone satisfies the feature check (probed
    # locally 2026-08-14 — no third camera needed).
    '--rename_map={"observation.images.front": "observation.images.camera1", "observation.images.wrist": "observation.images.camera2"}',
    "--policy.path=lerobot/smolvla_base",
    "--batch_size=64",
    f"--steps={steps}",
    # checkpoint every 1000 steps, each pushed to the Hub (save_checkpoint_to_hub)
    # — a mid-run failure or upload error costs at most 1000 steps, never the run
    "--save_freq=1000",
    "--seed=42",
    "--output_dir=outputs/train/brickbot_smolvla_v1",
    "--job_name=brickbot_smolvla_v1",
    "--job.target=a100-large",
    "--job.timeout=6h",
    "--wandb.enable=true",
    "--wandb.disable_artifact=true",
    "--policy.push_to_hub=true",
    "--policy.repo_id=sammy-labs/brickbot_smolvla_v1",
    "--save_checkpoint_to_hub=true",
]

from lerobot.scripts.lerobot_train import main  # noqa: E402

main()
