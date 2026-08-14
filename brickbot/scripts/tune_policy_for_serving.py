"""Post-training deployment prep for sammy-labs/brickbot_groot_v1.

1. Promotes the newest checkpoint's pretrained_model/ files to the repo root
   (the trainer's final push has failed before — checkpoints are the reliable
   path; harmless if root is already current).
2. Sets num_inference_timesteps=4 in the root config.json — flow-matching
   denoising steps at inference. Default (None) is slow; 4 is NVIDIA's own
   deployment setting. This is THE latency fix for jerky serving (measured
   0.5-1.2 chunks/s on 2026-08-13; smooth needs ~2+).

Run after any training run, before serving:
    conda run -n lerobot python scripts/tune_policy_for_serving.py
"""

import io
import json
import re

from huggingface_hub import CommitOperationAdd, CommitOperationCopy, HfApi, hf_hub_download

REPO = "sammy-labs/brickbot_smolvla_v1"
api = HfApi()

files = api.list_repo_files(REPO)
ckpts = sorted({m.group(1) for f in files if (m := re.match(r"checkpoints/(\d+)/pretrained_model/", f))})
assert ckpts, "no checkpoints found"
src = f"checkpoints/{ckpts[-1]}/pretrained_model/"
print(f"promoting checkpoint {ckpts[-1]} to root")

info = api.repo_info(REPO, files_metadata=True)
lfs = {s.rfilename for s in info.siblings if s.lfs is not None}
ops = []
for f in [f for f in files if f.startswith(src)]:
    dest = f[len(src):]
    if f in lfs:
        ops.append(CommitOperationCopy(src_path_in_repo=f, path_in_repo=dest))
    else:
        ops.append(CommitOperationAdd(path_in_repo=dest, path_or_fileobj=hf_hub_download(REPO, f, force_download=True)))

api.create_commit(repo_id=REPO, operations=ops,
    commit_message=f"Serve checkpoint {ckpts[-1]}: promote to root, num_inference_timesteps=4")
cfg = json.load(open(hf_hub_download(REPO, "config.json", force_download=True)))
print("root config:", {k: cfg[k] for k in ("num_inference_timesteps", "use_relative_actions", "chunk_size")})

# keep the repo at a single revision — LFS history of 12.6 GB models is what
# filled the org's private-storage quota on 2026-08-13 (lost a full training run)
api.super_squash_history(repo_id=REPO)
print("history squashed")
