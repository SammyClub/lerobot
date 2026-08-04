# 07 — Phase 4: Record your demonstrations

[← Phase 3](06-phase3-teleop-cameras.md) · [README](../README.md) · [Next: Phase 5 →](08-phase5-training.md)

**Goal:** a dataset of ~50 good episodes of one task, checked and uploaded. First task: **"Pick up the brick and place it on the target square."** Use a foam or mini brick under 100 g.

1. **Set the scene.** Brick at one fixed starting spot. Target zone marked.

   > **Tape is visible to the robot too.** Anything in the camera image becomes part of what the policy learns. A taped target square is fine — *if it is identical in every episode and still there when the policy runs*. For the brick's starting spot, put the alignment mark **outside** the camera's view (e.g. on the table edge) so you can reset precisely without teaching the robot to depend on a mark.

2. **Decide the task sentence and never change it.** Ours: `Pick up the brick and place it on the target square`. Exact wording matters little for ACT, but it must be identical at recording and at rollout.

3. **Start recording in LeLab.** In LeLab's recording screen, fill in the form: the task sentence, dataset name `so101_brick_place_v1`, **50 episodes**, 30-second episodes, 10-second reset time. Start. Episode 1 begins: up to 30 seconds to do the task, then a 10-second break to reset the scene, then the next episode starts automatically. Press the **spacebar** to advance the moment the brick is placed — don't wait out the clock.

   <details><summary>Terminal equivalent (has per-episode redo keys)</summary>

   ```bash
   lerobot-record \
       --robot.type=so101_follower \
       --robot.port=FOLLOWER_PORT \
       --robot.id=brick_follower \
       --robot.cameras="{ front: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}, wrist: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}}" \
       --teleop.type=so101_leader \
       --teleop.port=LEADER_PORT \
       --teleop.id=brick_leader \
       --display_data=true \
       --dataset.repo_id=${HF_USER}/so101_brick_place_v1 \
       --dataset.num_episodes=50 \
       --dataset.single_task="Pick up the brick and place it on the target square" \
       --dataset.episode_time_s=30 \
       --dataset.reset_time_s=10
   ```

   | Key | What it does |
   |---|---|
   | → (right arrow) | "Done" — ends the episode now and accepts it. |
   | ← (left arrow) | "Redo" — throws away the current episode and restarts it. A redo is cheap, a bad episode is expensive. |
   | ESC | Stops the whole session cleanly, saves, uploads. |

   If you fumble an episode in LeLab and can't redo it there, note its number and re-record via the terminal — or simply record a replacement episode; one bad episode in 50 hurts less than stopping your flow.

   </details>

4. **Record each episode by these rules:**
   - **Watch only the camera feeds on screen — never the physical robot.** The policy only ever sees the feeds.
   - **Start moving immediately.** A pause at the start teaches the robot to sit still.
   - **Same style every time.** Same approach path, same grasp. Gripper wide open at start; clearly wide open on release.
   - **Reset precisely** during the break: brick back to its exact spot (use the out-of-view mark).
   - Bumped something? Bad grab? Press ← and redo.

5. **Quality-check by replaying (Terminal step).** Replay makes the follower physically re-execute a recorded episode:

   ```bash
   lerobot-replay \
       --robot.type=so101_follower \
       --robot.port=FOLLOWER_PORT \
       --robot.id=brick_follower \
       --dataset.repo_id=${HF_USER}/so101_brick_place_v1 \
       --dataset.episode=0
   ```

   Replay a handful (change the episode number). Smooth motion = good data. Also watch all episodes as videos at https://huggingface.co/spaces/lerobot/visualize_dataset (enter `your-username/so101_brick_place_v1`).

6. **Know the privacy setting.** The dataset — including videos of your desk — uploads to the Hugging Face Hub automatically. To keep it offline add `--dataset.push_to_hub=false` (but the RTX PC / cloud training path needs it on the Hub — see [Phase 5](08-phase5-training.md)). Alternative: after upload, dataset page on huggingface.co → Settings → visibility → **Private**. Private datasets still work for your own training on any machine logged into your account.

7. **To add more episodes later, resume — don't restart (Terminal step):**

   ```bash
   lerobot-record \
       ... same command as before ... \
       --resume=true \
       --dataset.root=~/.cache/huggingface/lerobot/${HF_USER}/so101_brick_place_v1 \
       --dataset.num_episodes=25   # number of ADDITIONAL episodes
   ```

   > **Stale-cache trap:** resuming needs the local files intact. The opposite case — reusing a dataset *name* for a fresh start — misbehaves unless you first `rm -rf ~/.cache/huggingface/lerobot/<user>/<dataset>`.

[← Phase 3](06-phase3-teleop-cameras.md) · [README](../README.md) · [Next: Phase 5 →](08-phase5-training.md)
