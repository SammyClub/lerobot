# 09 — Phase 6: Run the policy

[← Phase 5](08-phase5-training.md) · [README](../README.md) · [Next: Brick curriculum →](10-brick-curriculum.md)

**Goal:** the robot does the task by itself — and you evaluate it the right way. Rollout runs on the **Mac** (the machine with the arms).

1. **Restore the scene exactly as trained.** Same lighting, cameras untouched, same mat, same brick. Any visible change is an unseen situation for the policy.

2. **Find the exact trained brick position.** Run the replay command from [Phase 4](07-phase4-recording.md) on episode 0 and watch where the gripper goes to pick. Place the brick exactly there. This reconstructs a scene the policy definitely knows.

3. **Let the robot take over.** In LeLab, pick the trained model (`brickbot_act_v1`) and run it on the robot. Enter the **exact task sentence from recording**. The leader arm stays on the shelf — the policy is driving.

   <details><summary>Terminal equivalent</summary>

   ```bash
   lerobot-rollout \
     --strategy.type=episodic \
     --policy.path=sammy-labs/brickbot_act_v1 \
     --robot.type=so101_follower \
     --robot.port=FOLLOWER_PORT \
     --robot.id=brick_follower \
     --robot.cameras="{ front: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}, wrist: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}}" \
     --task="Pick up the brick and place it on the target square" \
     --duration=60
   ```

   Camera names (`front`, `wrist`) and the task sentence must match recording exactly.

   </details>

4. **Judge the result by this rule:**
   - **Works at the trained position:** success! Run it 10 times; 8+/10 is a solid first policy.
   - **Fails even at the trained position:** something in the pipeline is broken — wrong `id`, moved camera, wrong camera names, wrong policy path. Fix the pipeline. Do not touch training settings.
   - **Works at the trained position, fails elsewhere:** completely normal. ACT only knows what it saw. Cure: record a v2 dataset with the brick at ~10 different start positions, ~10 episodes each, and retrain.

5. **Read the failure body-language:**
   - Drifts toward familiar poses and hovers → it's in a situation it never saw.
   - Won't close the gripper → in training, the brick was never at that angle between the pincers.
   - Sits still → the dataset probably contains pauses. Record cleaner data.

## Milestone 1 — complete when

- [ ] Follower mirrors leader smoothly with cameras streaming
- [ ] 50-episode dataset recorded, replayed, checked
- [ ] ACT policy trained; loss curve flattened
- [ ] Robot succeeds at the trained position 8+ times out of 10

## Later options

- **Rollout strategies:** `--strategy.type=sentry` (continuous record + auto-upload), `highlight` (save-on-keystroke), `dagger` (record human corrections during rollouts — very relevant to Stage 2 recovery training).
- **Async inference:** run the policy on the RTX PC and the robot client on the Mac over the network (`python -m lerobot.async_inference.policy_server` / `robot_client`) — useful once you move to heavier VLA policies.

[← Phase 5](08-phase5-training.md) · [README](../README.md) · [Next: Brick curriculum →](10-brick-curriculum.md)
