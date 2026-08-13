"""Fine-tune GR00T N1.7 on the wall dataset via HF Jobs, billed to sammy-labs.

Why this wrapper exists (2026-08-12): LeRobot's job submitter has no namespace
option — it always submits to the personal account (`/api/jobs/<user>`), which
has no credits → 402. The huggingface_hub API supports a `namespace` argument,
so we inject it (for submission AND the follow/logs calls) before invoking the
normal trainer.

Usage:
    conda run -n lerobot python scripts/train_wall_groot.py           # full run, 20k steps
    conda run -n lerobot python scripts/train_wall_groot.py 2000      # smoke test, 2k steps
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

steps = sys.argv[1] if len(sys.argv) > 1 else "20000"

sys.argv = [
    "lerobot-train",
    "--dataset.repo_id=sammy-labs/brickbot_so101_wall_v1",
    "--dataset.image_transforms.enable=true",
    "--policy.type=groot",
    "--policy.base_model_path=nvidia/GR00T-N1.7-3B",
    "--policy.embodiment_tag=new_embodiment",
    "--policy.chunk_size=16",
    "--policy.n_action_steps=16",
    # Absolute actions REQUIRED: the async policy server cannot stream-decode
    # GR00T relative actions (discovered 2026-08-13 — silent inference failure).
    "--policy.use_relative_actions=false",
    "--policy.use_bf16=true",
    "--use_policy_training_preset=true",
    "--batch_size=64",
    f"--steps={steps}",
    "--seed=42",
    "--output_dir=outputs/train/brickbot_groot_v1",
    "--job_name=brickbot_groot_v1",
    "--job.target=a100-large",
    "--job.timeout=14h",
    "--wandb.enable=true",
    "--wandb.disable_artifact=true",
    "--policy.push_to_hub=true",
    "--policy.repo_id=sammy-labs/brickbot_groot_v1",
    "--save_checkpoint_to_hub=true",
]

from lerobot.scripts.lerobot_train import main  # noqa: E402

main()
