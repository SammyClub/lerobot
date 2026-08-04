# 01 — How the robot learns

[← Glossary](00-glossary.md) · [README](../README.md) · [Next: Version drift →](02-version-drift.md)

The method is **imitation learning**. You show the robot the task about 50 times by driving it with the leader arm. Cameras record what the robot sees. The motors record how they moved. Then a neural network learns the pattern: "when the cameras see *this*, the motors should do *that*."

## The teleoperation loop (how training data is made)

```
your hand → leader arm → [joint angles] → computer → [copies angles ~30×/sec] → follower arm
                                             ↑
                              cameras (what the robot "sees")
```

You move the leader. A PID controller drives the follower's motors to match the leader's joint angles. No AI is involved — it is a direct copy. The computer records everything: two camera streams + six motor angles, 30 times per second.

## What the policy sees and does

At each moment the trained policy gets exactly three inputs:

1. The front camera image
2. The wrist camera image
3. The six current motor angles

Nothing else. **No memory, no history.** It outputs a **chunk** — a short plan of future motor angles.

## "Predict 50, execute 15"

```
[■■■■■■■■■■■■■■■][□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□]
 execute first 15    35 more predicted steps — thrown away
 (~0.5 s)            ↺ then look at cameras again, predict a fresh 50
```

- The policy predicts 50 steps ahead (`chunk_size=50`) but the robot acts on only the first 15 (`n_action_steps=15`), then re-looks and re-predicts.
- Too long a chunk → the plan diverges from reality before it finishes. Too short → the computer can't keep up with the ~30 Hz control loop.
- This "train long, execute short" pattern was the most robust configuration in the Trelis live tests — better than temporal ensembling.
- These two values are **set at training time** (they are baked into the policy's config), not at rollout.

## Three facts about ACT that explain almost everything you will observe

1. **ACT memorizes on purpose.** It learns to reproduce your demonstrations extremely well — and only your demonstrations. Put the brick where it never saw a brick, and it is lost. This is expected. Coverage comes from recording more varied episodes, not from more training steps.
2. **Consistency beats quantity.** If half your demos grab the brick one way and half another way, the model averages them into something that works neither way (the "style averaging" problem — ACT has a variational style encoder to combat it, but the practical fix is simply to demonstrate one consistent style).
3. **The cameras are its only eyes.** If you can't tell what to do from the camera images alone, neither can the model. This is why you watch the feeds — never the physical robot — while recording.

## Beyond ACT

Later you can swap ACT for a large pre-trained vision-language-action model:

- **SmolVLA** (~450M params) — language-conditioned, fine-tunable, `pip install 'lerobot[smolvla]'`
- **π₀ (pi0)** — ~3B params, PaliGemma backbone, diffusion action expert
- **GR00T N1** — NVIDIA's diffusion transformer, partly trained on unlabeled robot video

They generalize better but are slower and heavier. Do ACT first — it teaches the whole pipeline with the fewest moving parts.

[← Glossary](00-glossary.md) · [README](../README.md) · [Next: Version drift →](02-version-drift.md)
