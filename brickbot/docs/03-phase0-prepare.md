# 03 — Phase 0: Prepare and sort the kit

[← Version drift](02-version-drift.md) · [README](../README.md) · [Next: Phase 1 →](04-phase1-software.md)

**Goal:** parts sorted, dangers understood, extra equipment ordered. You will not assemble anything yet — the motors need software first ([Phase 1](04-phase1-software.md)), because each one must be programmed before it goes into the arm ([Phase 2](05-phase2-build-calibrate.md)).

1. **Clear a workspace.** About 1 m × 1 m of desk, near the computer, with room to clamp the follower down. This desk becomes the robot's permanent home — the cameras must never move once recording starts.

2. **Sort the parts into two piles: follower and leader.** The follower has a **gripper** (two pincers). The leader has a **handle with a trigger**. Each arm has 6 servos, one control board, one USB-C cable, and one power supply.

3. **Check the power supplies and servo labels.**

   > ⚠️ **This can destroy servos — read carefully.**
   > The servos come in two voltage versions. Look at the sticker on each servo — it states the voltage. Count the power supplies.
   >
   > - **Two different supplies (5V and 12V):** the follower has 12V servos (stronger) and the leader has 7.4V servos. The **leader always gets the 5V supply. The follower always gets the 12V supply.** This applies to every step in this guide, including calibration. 12V into the leader permanently kills its servos.
   > - **Identical supplies:** all 12 servos are the 7.4V version. Both arms use the same supply. No danger.
   >
   > Label the supplies with tape right now: "LEADER" and "FOLLOWER".

4. **Check the leader's servo gear labels.** The leader's six servos are **not identical** — they have different internal gears so the arm moves freely in your hand. Each has a small code on its label. During assembly, each code must go into its specific joint:

   | Label code | Gear ratio | Goes into (leader only) |
   |---|---|---|
   | C001 | 1/345 | Shoulder lift (joint 2) |
   | C044 | 1/191 | Shoulder pan (joint 1) and elbow (joint 3) |
   | C046 | 1/147 | Wrist flex (4), wrist roll (5), gripper trigger (6) |

   The follower's six servos are all the same (1/345, C001-type) — no sorting needed there. A leader with the wrong gearing in a joint will either flop or resist your hand.

5. **Find a data-capable USB-C cable (or two).** Charge-only cables are a classic silent failure: the arm powers on but the computer never sees it. If a cable came with the kit, use that one.

6. **Order the extra equipment.**
   - **Two USB webcams** (~$20–40 each). Ordinary 1080p webcams are perfect — recording happens at 640×480 anyway.
   - **A powered USB hub** — 4 devices will be plugged in (2 arms, 2 cameras).
   - **A clamp** to fix the follower's base to the desk.
   - **A wrist-camera mount** — 3D-print one from the [SO-ARM100 repo](https://github.com/TheRobotStudio/SO-ARM100), or improvise a rigid bracket.
   - **First "bricks" — already sorted:** the wooden stacking-tower (Jenga-style) blocks (Flying Tiger). They're brick-shaped, ~10–20 g (far inside payload), ~2.5 cm wide (fits the gripper), and rigid with real sliding friction — better than foam. Two notes: smooth wood is slippery, so grasp across the narrow face and squeeze decisively; and designate ONE block as "the brick" for the first dataset (identical spares are handy). Kiln-fired 1:12-scale clay minis remain the later upgrade.

7. **Bookmark the official assembly guide.** It has a video for every joint: https://huggingface.co/docs/lerobot/so101. Tools needed: precision Phillips #0/#1 screwdrivers and a small flathead. Screws are M2×6 (motor mounts) and M3×6 (horns/structure). Budget 1–2 hours per arm.

[← Version drift](02-version-drift.md) · [README](../README.md) · [Next: Phase 1 →](04-phase1-software.md)
