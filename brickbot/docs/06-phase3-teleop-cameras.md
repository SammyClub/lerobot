# 06 — Phase 3: Drive the robot by hand

[← Phase 2](05-phase2-build-calibrate.md) · [README](../README.md) · [Next: Phase 4 →](07-phase4-recording.md)

**Goal:** you can drive the follower smoothly with the leader, both cameras stream, and the scene is framed and fixed in place.

1. **Start teleoperation (no cameras yet):**

   ```bash
   lerobot-teleoperate \
       --robot.type=so101_follower \
       --robot.port=FOLLOWER_PORT \
       --robot.id=brick_follower \
       --teleop.type=so101_leader \
       --teleop.port=LEADER_PORT \
       --teleop.id=brick_leader
   ```

   Pick up the leader and move it slowly. The follower copies. Ctrl-C stops.

2. **Practice for 20 minutes.** Pick things up, put them down. Your smoothness here is the ceiling on your data quality, and data quality is the ceiling on the policy. Jerky puppeteering = jerky robot, forever.

3. **Plug in both cameras and identify them:**

   ```bash
   lerobot-find-cameras opencv
   ```

   Lists each camera with an index number and saves a snapshot from each. Open the snapshots to see which is which. Write down: wrist index = __, front index = __. The laptop's built-in camera also appears — ignore it.

4. **Mount the cameras.**
   - **Wrist camera:** on the arm near the gripper, looking at what the gripper is about to grab. Screw it down hard — glue it if it wobbles.
   - **Front camera:** on a small tripod, looking at the whole work area from the front, slightly above. It must see the brick, the target, and the follower.

5. **Start teleoperation with cameras and a live view** (substitute your index numbers):

   ```bash
   lerobot-teleoperate \
       --robot.type=so101_follower \
       --robot.port=FOLLOWER_PORT \
       --robot.id=brick_follower \
       --robot.cameras="{ front: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}, wrist: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}}" \
       --teleop.type=so101_leader \
       --teleop.port=LEADER_PORT \
       --teleop.id=brick_leader \
       --display_data=true
   ```

   A viewer window opens with both feeds live.

6. **Frame the scene using the live view.** The front camera should see *only* what matters:
   - Visible at all times: the brick, the target area, the follower arm.
   - NOT visible: you, the keyboard, the leader arm, clutter, harsh shadows.
   - Plain background (a plain mat helps).

7. **Fix everything in place. Permanently.** Clamp the arm. Tape the tripod feet. Glue the wrist mount. From this moment until the policy runs, **nothing about the cameras or the arm's position may change.** A camera nudged 2 cm invalidates every recorded episode.

8. **If teleop feels jittery, drop the live view.** The viewer itself costs compute. Once framing is done you don't need it for teleop practice (during recording you do watch the feeds — [Phase 4](07-phase4-recording.md) explains why).

**Workspace layout (top-down):** the front camera's field of view covers the follower arm, brick, and target zone; the laptop, leader arm, and you sit outside that view — invisible to the robot.

[← Phase 2](05-phase2-build-calibrate.md) · [README](../README.md) · [Next: Phase 4 →](07-phase4-recording.md)
