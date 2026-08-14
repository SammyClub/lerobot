#!/usr/bin/env bash
# Run the wall policy on the robot via the cloud policy server.
# Prerequisites, in order:
#   1. scripts/serve_policy_cloud.py   (server job running; wait for "server started" in its logs)
#   2. scripts/connect_policy_tunnel.sh  (in its own terminal, left open)
#   3. this script
# The heavy model runs on the cloud GPU; only observations/actions cross the tunnel.
set -e
exec conda run --no-capture-output -n lerobot python -m lerobot.async_inference.robot_client \
    --server_address=127.0.0.1:8080 \
    --policy_type=smolvla \
    --pretrained_name_or_path=sammy-labs/brickbot_smolvla_v1 \
    --policy_device=cuda \
    --robot.type=so101_follower \
    --robot.port=/dev/tty.usbmodem5AE60824171 \
    --robot.id=brick_follower \
    --robot.cameras="{ camera1: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}, camera2: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}}" \
    --task="build the block wall on the green mat in the order yellow, pink, orange - yellow and pink end to end, orange on top of both." \
    --actions_per_chunk=25 \
    --chunk_size_threshold=0.7 \
    --aggregate_fn_name=weighted_average
