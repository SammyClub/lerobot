# 09 — Phase 6: Run the policy

[← Phase 5](08-phase5-training.md) · [README](../README.md) · [Next: Brick curriculum →](10-brick-curriculum.md)

**Goal:** the robot does the task by itself — and you evaluate it the right way. Rollout runs on the **Mac** (the machine with the arms).

1. **Restore the scene exactly as trained.** Same lighting, cameras untouched, same green mat, same three blocks. Any visible change is an unseen situation for the policy.

2. **Restore the exact trained block homes.** Run the replay command from [Phase 4](07-phase4-recording.md) on episode 0 and watch where the gripper goes to pick each block. Place the blocks exactly there. This reconstructs a scene the policy definitely knows.

3. **Let the robot take over.** The leader arm stays on the shelf — the policy is driving now. Camera names (`front`, `wrist`) and the task sentence must match recording exactly:

   ```bash
   lerobot-rollout \
     --strategy.type=base \
     --policy.path=sammy-labs/brickbot_groot_v1 \
     --policy.base_model_path=nvidia/GR00T-N1.7-3B \
     --policy.n_action_steps=8 \
     --robot.type=so101_follower \
     --robot.port=FOLLOWER_PORT \
     --robot.id=brick_follower \
     --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}, wrist: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}}" \
     --task="build the block wall on the green mat in the order yellow, pink, orange: yellow and pink end to end, orange on top of both." \
     --duration=120 \
     --device=mps \
     --display_data=true \
     --inference.type=rtc \
     --inference.rtc.execution_horizon=10
   ```

   > **Open question: is the Mac fast enough to run a 3B model live?** GR00T N1.7 is much heavier at inference than a small policy. First try it on the Mac (`--device=mps`) with RTC (real-time chunking) enabled as above — it is designed to smooth execution on slow hardware. If the arm moves in lurches or stalls between chunks, the fallback is **async inference**: run LeRobot's policy server on a GPU machine or cloud box and keep only the robot client on the Mac (`python -m lerobot.async_inference.policy_server` / `robot_client`).

4. **Judge the result by this rule:**
   - **Works at the trained setup:** success! Run it 10 times; 8+/10 is a solid first policy.
   - **Fails even at the trained setup:** something in the pipeline is broken — wrong `id`, moved camera, wrong camera names, wrong policy path. Fix the pipeline. Do not touch training settings.
   - **Works at the trained setup, fails when things move:** common, though GR00T generalizes better than small models. Cure: record a v2 dataset with varied block start positions and retrain.

5. **Read the failure body-language:**
   - Drifts toward familiar poses and hovers → it's in a situation it never saw.
   - Won't close the gripper → in training, a block was never at that angle between the pincers.
   - Sits still → the dataset probably contains pauses. Record cleaner data.

## Milestone 1 — complete when

- [ ] Follower mirrors leader smoothly with cameras streaming
- [ ] 50-episode dataset recorded, replayed, checked
- [ ] GR00T N1.7 policy fine-tuned; loss curve flattened
- [ ] Robot succeeds at the trained position 8+ times out of 10

## Later options

- **Rollout strategies:** `--strategy.type=sentry` (continuous record + auto-upload), `highlight` (save-on-keystroke), `dagger` (record human corrections during rollouts — very relevant to Stage 2 recovery training).
- **Async inference:** run the policy server on a GPU box and the robot client on the Mac over the network (`python -m lerobot.async_inference.policy_server` / `robot_client`) — useful once you move to heavier VLA policies.

[← Phase 5](08-phase5-training.md) · [README](../README.md) · [Next: Brick curriculum →](10-brick-curriculum.md)
