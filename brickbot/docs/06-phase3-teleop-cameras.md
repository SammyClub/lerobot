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

   Pick up the leader and move it slowly — the follower copies. Ctrl-C stops.

2. **Practice for 20 minutes.** Pick things up, put them down. Your smoothness here is the ceiling on your data quality, and data quality is the ceiling on the policy. Jerky puppeteering = jerky robot, forever.

3. **Plug in both cameras and identify them (Terminal step).** The tool saves a snapshot from each camera — the easiest way to tell them apart:

   ```bash
   lerobot-find-cameras opencv
   ```

   Lists each camera with an index number. Open the saved snapshots to see which is which. Write down: wrist index = __, front index = __. The laptop's built-in camera also appears — ignore it.

4. **Mount the cameras.**
   - **Wrist camera:** on the arm near the gripper, looking at what the gripper is about to grab. Screw it down hard — glue it if it wobbles.
   - **Front camera** (Acer 1080p webcam): on the desk-clamp camera arm, high and looking steeply down, so the table fills the frame and nothing beyond the table's back edge is visible.

5. **Open the live alignment view and frame the scene.** The repo has a purpose-built tool ([scripts/camera_align.py](../scripts/camera_align.py)) that shows both cameras live in the rerun viewer:

   ```bash
   python scripts/camera_align.py --front 0 --wrist 1 --width 640 --height 480
   ```

   While watching it, arrange the world until the front camera sees *only* what matters:
   - Visible at all times: the brick, the target area, the follower arm.
   - NOT visible: you, the keyboard, the leader arm, the neighbor's desk, clutter, harsh shadows.
   - Plain background; steady lamp light rather than daylight from a window.

   Leave the viewer running while you adjust. When it's right, don't touch anything and go to the next step.

6. **Fix everything in place. Permanently.** Tighten the camera arm's knobs. Tape the cables. Check the follower's clamp. From this moment until the policy runs, **nothing about the cameras or the arm's position may change.** A camera nudged 2 cm invalidates every recorded episode.

7. **Stop the alignment viewer: Ctrl-C.** Two programs can't share a camera — close it before the lock script (next step) or teleop can use the feeds.

8. **Lock the front camera's settings:** `scripts/lock_front_camera.sh` (run with no camera app open). The Acer A610 is fixed-focus, and its *manual white balance is broken* (green cast — so WB stays auto; harmless under fixed lighting). What the script locks is **exposure**: it measures the auto-exposure brightness baseline, switches to manual, and binary-searches the exposure value until brightness matches — then fixes the frame rate. Unlocked exposure pulses brighter/darker as the dark arm crosses the white table — noise in every frame. ⚠️ UVC settings can reset on replug/reboot, and the right exposure depends on lighting — **run the script at the start of every recording session, after scene + lighting are final.** (`--auto` reverts to full auto. Uses [uvc-util](https://github.com/jtfrey/uvc-util), built to `~/.local/bin`.)

9. **Rehearse: teleop with cameras.** The camera names `front` and `wrist` in this command matter — they're baked into every episode and the trained policy expects them forever:

   ```bash
   lerobot-teleoperate \
       --robot.type=so101_follower \
       --robot.port=FOLLOWER_PORT \
       --robot.id=brick_follower \
       --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}, wrist: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}}" \
       --teleop.type=so101_leader \
       --teleop.port=LEADER_PORT \
       --teleop.id=brick_leader \
       --display_data=true
   ```

   Practice the task **looking only at the camera feeds in the rerun window — never at the robot**. Ready for Phase 4 when: the whole wall built smoothly in under ~50 seconds — same build order (yellow, pink, orange), same grasps, no bumped blocks — several times in a row. 20+ minutes of practice is normal. Ctrl-C to stop.

10. **If teleop feels jittery, drop the live view.** The viewer costs compute; practice without `--display_data=true` for smoothness if needed. During recording you must watch the feeds — [Phase 4](07-phase4-recording.md) explains why — so rehearse with the viewer on at least some of the time.

**Workspace layout (top-down):** the front camera's field of view covers the follower arm, brick, and target zone; the laptop, leader arm, and you sit outside that view — invisible to the robot.

[← Phase 2](05-phase2-build-calibrate.md) · [README](../README.md) · [Next: Phase 4 →](07-phase4-recording.md)
