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

The policy you will train is **NVIDIA GR00T N1.7** — a 3-billion-parameter vision-language-action model, pre-trained by NVIDIA on huge amounts of robot data and *fine-tuned* on your demonstrations (it joined LeRobot natively in July 2026, `--policy.type=groot`). At each moment it gets:

1. The front camera image
2. The wrist camera image
3. The six current motor angles
4. **The task sentence** — it genuinely reads the instruction

It outputs a **chunk** — a short plan of future motor angles.

## "Predict 16, execute 8"

```
[■■■■■■■■][□□□□□□□□]
 execute     8 more predicted steps — thrown away
 first 8     ↺ then look at cameras again, predict a fresh 16
```

- The policy predicts 16 steps ahead (`chunk_size=16`) but the robot acts on only the first 8 (`n_action_steps=8` at rollout), then re-looks and re-predicts.
- Too long a chunk → the plan diverges from reality before it finishes. Too short → the computer can't keep up with the control loop.
- The chunk size is **set at training time** (baked into the policy's config); the execute count is set at rollout.

## Three facts about GR00T that explain almost everything you will observe

1. **It starts smart, and your demos specialize it.** Unlike a from-scratch model, GR00T already understands objects, language, and manipulation in general; your ~50 episodes teach it your specific arm, cameras, and task. It generalizes better than small models — but coverage still comes from varied episodes, not from more training steps.
2. **Consistency still beats quantity.** Inconsistent demonstrations still teach a muddled behavior. Pick one style — same build order, same grasps — and repeat it every episode.
3. **The cameras and your task sentence are its inputs.** With a language-conditioned model, the task sentence describes the goal, and consistency of wording between recording and rollout matters. If you can't do the task from the camera images alone, neither can the model — which is why you watch the feeds, never the physical robot, while recording.

## The model landscape (context)

GR00T N1.7 replaces smaller options this project considered earlier:

- **ACT** (~80M params, from-scratch) — fast and light, but single-task and memorization-bound
- **SmolVLA** (~450M params) — language-conditioned, lighter fine-tune
- **π₀ (pi0)** — ~3B params, PaliGemma backbone, diffusion action expert
- **GR00T N1.7** (~3B params) — NVIDIA's reasoning VLA; **the plan of record**

[← Glossary](00-glossary.md) · [README](../README.md) · [Next: Version drift →](02-version-drift.md)
