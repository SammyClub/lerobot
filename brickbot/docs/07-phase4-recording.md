# 07 — Phase 4: Record your demonstrations

[← Phase 3](06-phase3-teleop-cameras.md) · [README](../README.md) · [Next: Phase 5 →](08-phase5-training.md)

**Goal:** a dataset of ~50 good episodes of one task, checked and uploaded. The task: **build a three-block wall** — yellow and pink blocks end to end on the green mat, orange bridging on top of both. With a language-conditioned model like SmolVLA, the task sentence genuinely describes the goal, so it is written to match what happens — and it must stay word-for-word identical from recording through rollout.

1. **Set the scene.** Green mat down (it is the visual anchor for "where the wall goes"). Each of the three blocks — yellow, pink, orange — gets one fixed home position, identical every episode.

   > **Tape is visible to the robot too.** Anything in the camera image becomes part of what the policy learns. The green mat is fine — it is identical in every episode and still there when the policy runs. For the blocks' home positions, put alignment marks **outside** the camera's view (e.g. on the table edge) so you can reset precisely without teaching the robot to depend on a mark.

2. **Decide the task sentence and never change it.** Ours: `build the block wall on the green mat in the order yellow, pink, orange - yellow and pink end to end, orange on top of both.` SmolVLA reads this — keep it word-for-word identical at recording and at rollout.

3. **Start recording:**

   ```bash
   lerobot-record \
       --robot.type=so101_follower \
       --robot.port=FOLLOWER_PORT \
       --robot.id=brick_follower \
       --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}, wrist: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}}" \
       --teleop.type=so101_leader \
       --teleop.port=LEADER_PORT \
       --teleop.id=brick_leader \
       --display_data=true \
       --dataset.repo_id=sammy-labs/brickbot_so101_wall_v1 \
       --dataset.no_stamp=true \
       --dataset.num_episodes=50 \
       --dataset.single_task="build the block wall on the green mat in the order yellow, pink, orange - yellow and pink end to end, orange on top of both." \
       --dataset.episode_time_s=60 \
       --dataset.reset_time_s=25
   ```

   What happens: episode 1 begins — up to 60 seconds to build the wall (end early with → the moment the orange block settles; don't wait out the clock), then a 25-second break to reset all three blocks to their homes, then the next episode starts automatically.

   | Key | What it does |
   |---|---|
   | → (right arrow) | "Done" — ends the episode now and accepts it. |
   | ← (left arrow) | "Redo" — throws away the current episode and restarts it. A redo is cheap, a bad episode is expensive. |
   | ESC | Stops the whole session cleanly, saves, uploads. |

4. **Record each episode by these rules:**
   - **Watch only the camera feeds on screen — never the physical robot.** The policy only ever sees the feeds.
   - **Start moving immediately.** A pause at the start teaches the robot to sit still.
   - **Same style every time.** Same build order (yellow, pink, orange), same approach paths, same grasps. Gripper wide open at start; clearly wide open on release. Place the orange bridge gently — a bump destroys the episode.
   - **Reset precisely** during the break: all three blocks back to their exact homes (use the out-of-view marks).
   - Bumped something? Bad grab? Press ← and redo.

5. **Quality-check by replaying (Terminal step).** Replay makes the follower physically re-execute a recorded episode:

   ```bash
   lerobot-replay \
       --robot.type=so101_follower \
       --robot.port=FOLLOWER_PORT \
       --robot.id=brick_follower \
       --dataset.repo_id=sammy-labs/brickbot_so101_wall_v1 \
       --dataset.episode=0
   ```

   Replay a handful (change the episode number). Smooth motion = good data. Also watch all episodes as videos at https://huggingface.co/spaces/lerobot/visualize_dataset (enter `sammy-labs/brickbot_so101_wall_v1`).

6. **Know the privacy setting.** The dataset — including videos of your desk — uploads to the Hugging Face Hub automatically. To keep it offline add `--dataset.push_to_hub=false` (but the cloud training path needs it on the Hub — see [Phase 5](08-phase5-training.md)). Alternative: after upload, dataset page on huggingface.co → Settings → visibility → **Private**. Private datasets still work for your own training on any machine logged into your account.

7. **To add more episodes later, resume — don't restart (Terminal step):**

   ```bash
   lerobot-record \
       ... same command as before ... \
       --resume=true \
       --dataset.root=~/.cache/huggingface/lerobot/sammy-labs/brickbot_so101_wall_v1 \
       --dataset.num_episodes=25   # number of ADDITIONAL episodes
   ```

   > **Stale-cache trap:** resuming needs the local files intact. The opposite case — reusing a dataset *name* for a fresh start — misbehaves unless you first `rm -rf ~/.cache/huggingface/lerobot/<user>/<dataset>`.

[← Phase 3](06-phase3-teleop-cameras.md) · [README](../README.md) · [Next: Phase 5 →](08-phase5-training.md)
