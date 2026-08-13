#!/usr/bin/env bash
# Record wall-task episodes into sammy-labs/brickbot_so101_wall_v1 (resume mode:
# always ADDS episodes to the existing dataset).
#
# Usage:
#   scripts/record_wall.sh          # add 25 episodes (one comfortable batch)
#   scripts/record_wall.sh 99       # add 99 episodes
#
# Before each batch: scripts/lock_front_camera.sh, leader power brick check,
# blocks at their home marks. Keys during recording: right-arrow = accept
# episode early, left-arrow = redo, ESC = stop batch cleanly (saves + uploads).
set -e
EPISODES="${1:-25}"

exec conda run --no-capture-output -n lerobot lerobot-record \
    --robot.type=so101_follower \
    --robot.port=/dev/tty.usbmodem5AE60824171 \
    --robot.id=brick_follower \
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}, wrist: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}}" \
    --teleop.type=so101_leader \
    --teleop.port=/dev/tty.usbmodem5B3E0891281 \
    --teleop.id=brick_leader \
    --display_data=true \
    --dataset.repo_id=sammy-labs/brickbot_so101_wall_v1 \
    --dataset.no_stamp=true \
    --resume=true \
    --dataset.root="$HOME/.cache/huggingface/lerobot/sammy-labs/brickbot_so101_wall_v1" \
    --dataset.num_episodes="$EPISODES" \
    --dataset.single_task="build the block wall on the green mat in the order yellow, pink, orange - yellow and pink end to end, orange on top of both." \
    --dataset.episode_time_s=60 \
    --dataset.reset_time_s=25
