# 05 — Phase 2: Set up motors, assemble, calibrate

[← Phase 1](04-phase1-software.md) · [README](../README.md) · [Next: Phase 3 →](06-phase3-teleop-cameras.md)

**Goal:** both arms built, every servo programmed, both arms calibrated. The longest phase — take a full afternoon per arm.

## 2a. Find your USB ports

1. **Connect the follower's control board.** USB-C into the computer, power supply (the FOLLOWER-labeled one!) into the wall. No servos connected yet.
2. **Run the port finder:**

   ```bash
   lerobot-find-port
   ```

   It asks you to unplug the USB cable. Unplug it. It prints the port name — something like `/dev/tty.usbmodem58760431551`. Plug back in.
3. **Write the port down. Label it "FOLLOWER PORT".** It goes into almost every command from now on. (In these docs it appears as `FOLLOWER_PORT`.)
4. **Repeat 1–3 for the leader's board.** Label it "LEADER PORT". Keep each board in the *same physical USB socket* from now on — port names can change if plugs move.

> Linux only: if you get "permission denied" on the port — `sudo chmod 666 /dev/ttyACM*` now, or permanently `sudo usermod -aG dialout $USER` + log out/in.

## 2b. Program the motor IDs (before assembly)

Each servo must be told its number (1–6) once, **before** the servos are built into the arm. The tool works on **one servo at a time**.

```
During ID setup:               After setup (inside the arm):
board ──── servo               board ── 1 ── 2 ── 3 ── 4 ── 5 ── 6
        (ONE cable)                    (daisy-chain, servo to servo)
```

1. **Connect ONE follower servo to the follower board** with one 3-pin cable. Any servo — the tool tells you which joint it becomes. Waveshare board? Check its two jumpers are on channel **B** first.
2. **Run the motor setup tool for the follower:**

   ```bash
   lerobot-setup-motors \
       --robot.type=so101_follower \
       --robot.port=FOLLOWER_PORT
   ```

3. **Follow the prompts.** "Connect the controller board to the gripper motor only and press Enter" means: the servo currently plugged in becomes the **gripper** (ID 6). Press Enter. Then unplug it, plug in the next servo, press Enter — it works down from gripper (6) to shoulder pan (1). Stick a number label on each servo as it is programmed.
4. **Repeat for the leader** — but remember the gear codes from [Phase 0, step 4](03-phase0-prepare.md): the servo programmed as "shoulder lift" must be a C001, etc. Choose which physical servo to plug in accordingly.

   ```bash
   lerobot-setup-motors \
       --teleop.type=so101_leader \
       --teleop.port=LEADER_PORT
   ```

   The leader's servos differ per joint (gear codes printed on each servo's sticker). Sort them into three piles first (1x C001, 2x C044, 3x C046 — if a label is unreadable, the C046s twist most freely by hand, the C001 resists most), then plug in the right one as the tool asks:

   | Tool asks for | ID | Plug in a… |
   |---|---|---|
   | Gripper (trigger) | 6 | C046 |
   | Wrist roll | 5 | C046 |
   | Wrist flex | 4 | C046 |
   | Elbow | 3 | C044 |
   | Shoulder lift | 2 | **C001** |
   | Shoulder pan | 1 | C044 |

5. **Now assemble both arms.** Follow the [official guide](https://huggingface.co/docs/lerobot/so101) joint by joint. Each numbered servo goes into its joint (1 = shoulder pan at the base … 6 = gripper at the tip). Daisy-chain the 3-pin cables servo-to-servo, and servo 1 to the control board. Ignore any instruction anywhere about removing gears (that's the old SO-100).
6. **Clamp the follower's base to the desk.**

## 2c. Calibrate both arms

Calibration teaches the software each joint's true range. Once per arm, two minutes each. Files land in `~/.cache/huggingface/lerobot/calibration/` (versioned copies live in [`hardware/calibration/`](../hardware/calibration/)). **Names are forever:** exactly `brick_follower` and `brick_leader`.

1. **Power and connect both arms** (correct supply per the tape labels, USB into data ports); `conda activate lerobot`.
2. **Start the follower's calibration** (ports for each machine are in [SETUP-LOG.md](../SETUP-LOG.md)):

   ```bash
   lerobot-calibrate \
       --robot.type=so101_follower \
       --robot.port=FOLLOWER_PORT \
       --robot.id=brick_follower
   ```

3. **Hold the L-pose, press Enter.** Upright from the base, forearm horizontal, gripper pointing down and closed — every joint near the middle of its range.
4. **Sweep every joint to both ends, then press Enter to save.** One joint at a time, gently to both stops: gripper, wrist roll, wrist flex, elbow, shoulder lift, shoulder pan. The numbers on screen record each range.
5. **Repeat for the leader** (its "gripper" is the trigger — squeeze fully open and closed):

   ```bash
   lerobot-calibrate \
       --teleop.type=so101_leader \
       --teleop.port=LEADER_PORT \
       --teleop.id=brick_leader
   ```

> If the arm later jumps to a weird pose: bad calibration or mistyped name → recalibrate. Two minutes — never live with a bad one.

[← Phase 1](04-phase1-software.md) · [README](../README.md) · [Next: Phase 3 →](06-phase3-teleop-cameras.md)
