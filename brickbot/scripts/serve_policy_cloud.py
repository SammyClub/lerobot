"""Start the GR00T policy server on a cloud GPU (HF Jobs, billed to sammy-labs).

Architecture (decided 2026-08-13, after measuring that Mac MPS runs 3B
inference at 0.6-4 Hz vs the 30 Hz control target):

    Mac (robot client + arms)  <-- SSH tunnel -->  HF Jobs GPU (policy server)

The job exposes no public port; access is via HF Jobs SSH (requires an SSH key
registered at https://huggingface.co/settings/keys). After this script prints
the job id, open the tunnel with scripts/connect_policy_tunnel.sh, then run the
robot client with scripts/rollout_wall_async.sh.

THE SERVER BILLS org credit the whole time it runs. Stop it when done:
    hf jobs cancel <job-id> --namespace sammy-labs

Usage:
    conda run -n lerobot python scripts/serve_policy_cloud.py
"""

import json
import pathlib

from huggingface_hub import HfApi, get_token

NAMESPACE = "sammy-labs"
FLAVOR = "a10g-large"  # SmolVLA (450M) serves comfortably here; the A100 was only needed for 3B GR00T
PORT = 8080
STATE_FILE = pathlib.Path(__file__).parent / ".cloud_policy_job.json"

api = HfApi()
job = api.run_job(
    namespace=NAMESPACE,
    image="huggingface/lerobot-gpu:latest",
    command=[
        "sh", "-c",
        # tee to a file so the server's stderr is always readable over SSH
        # (the platform log endpoint proved flaky under load, 2026-08-13)
        f"python -m lerobot.async_inference.policy_server --host=0.0.0.0 --port={PORT} 2>&1 | tee /tmp/policy_server.log",
    ],
    flavor=FLAVOR,
    timeout="4h",  # auto-stop safety net; cancel earlier when done
    ssh=True,
    secrets={"HF_TOKEN": get_token()},
    labels={"brickbot": "true", "role": "policy-server"},
)

STATE_FILE.write_text(json.dumps({"job_id": job.id, "port": PORT}))
print(f"Policy server job submitted: {job.id} (flavor={FLAVOR}, port={PORT})")
print(f"  Watch startup:  hf jobs logs {job.id} --namespace {NAMESPACE}")
print(f"  Open tunnel:    scripts/connect_policy_tunnel.sh")
print(f"  STOP BILLING:   hf jobs cancel {job.id} --namespace {NAMESPACE}")
