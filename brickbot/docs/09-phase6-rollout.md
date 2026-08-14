# 09 — Phase 6: Run the policy

[← Phase 5](08-phase5-training.md) · [README](../README.md) · [Next: Brick curriculum →](10-brick-curriculum.md)

**Goal:** the robot does the task by itself — and you evaluate it the right way. Rollout runs on the **Mac** (the machine with the arms).

1. **Restore the scene exactly as trained.** Same lighting, cameras untouched, same green mat, same three blocks. Any visible change is an unseen situation for the policy.

2. **Restore the exact trained block homes.** Run the replay command from [Phase 4](07-phase4-recording.md) on episode 0 and watch where the gripper goes to pick each block. Place the blocks exactly there. This reconstructs a scene the policy definitely knows.

3. **Let the robot take over — via the cloud policy server.** Measured on 2026-08-13 (with the earlier 3B model), Mac-local inference could not hold the 30 Hz control target, so the policy runs on a rented GPU (HF Jobs, org-billed) and the Mac keeps only a lightweight robot client, connected through an SSH tunnel. Three commands, three terminals, in order:

   ```bash
   # 1. Start the cloud policy server (bills while running!)
   conda run -n lerobot python scripts/serve_policy_cloud.py

   # 2. Open the tunnel (own terminal, leave it running)
   scripts/connect_policy_tunnel.sh

   # 3. Run the robot client (arm moves!)
   scripts/rollout_wall_async.sh
   ```

   Wait for the server job's logs to show it started before step 3. The leader arm stays on the shelf; camera names and the task sentence are baked into the client script (`--policy_type=smolvla`, `--pretrained_name_or_path=sammy-labs/brickbot_smolvla_v1`, `--actions_per_chunk=25`, `--chunk_size_threshold=0.7`). **When you finish a session, stop the server** — `hf jobs cancel <job-id> --namespace sammy-labs` (id printed at step 1, saved in `scripts/.cloud_policy_job.json`); it also auto-stops after 4 h. One-time prerequisite: an SSH key registered at https://huggingface.co/settings/keys.

   > SmolVLA is 7× smaller than the 3B model that failed on the Mac — once the pipeline is stable, it's worth testing whether Mac-local inference now suffices and the cloud server can be retired.

4. **Judge the result by this rule:**
   - **Works at the trained setup:** success! Run it 10 times; 8+/10 is a solid first policy.
   - **Fails even at the trained setup:** something in the pipeline is broken — wrong `id`, moved camera, wrong camera names, wrong policy path. Fix the pipeline. Do not touch training settings.
   - **Works at the trained setup, fails when things move:** common, though a pretrained VLA generalizes better than from-scratch models. Cure: record a v2 dataset with varied block start positions and retrain.

5. **Read the failure body-language:**
   - Drifts toward familiar poses and hovers → it's in a situation it never saw.
   - Won't close the gripper → in training, a block was never at that angle between the pincers.
   - Sits still → the dataset probably contains pauses. Record cleaner data.

## Milestone 1 — complete when

- [ ] Follower mirrors leader smoothly with cameras streaming
- [ ] 100-episode dataset recorded, replayed, checked
- [ ] SmolVLA policy fine-tuned; loss curve flattened
- [ ] Robot succeeds at the trained position 8+ times out of 10

## Later options

- **Rollout strategies:** `--strategy.type=sentry` (continuous record + auto-upload), `highlight` (save-on-keystroke), `dagger` (record human corrections during rollouts — very relevant to Stage 2 recovery training).
- **Async inference:** run the policy server on a GPU box and the robot client on the Mac over the network (`python -m lerobot.async_inference.policy_server` / `robot_client`) — this IS the current architecture (see step 3).

[← Phase 5](08-phase5-training.md) · [README](../README.md) · [Next: Brick curriculum →](10-brick-curriculum.md)
