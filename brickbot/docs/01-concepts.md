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

The policy you will train is **SmolVLA** — Hugging Face's 450-million-parameter vision-language-action model, pre-trained on community robot data and *fine-tuned* on your demonstrations from the `lerobot/smolvla_base` checkpoint (`--policy.path`, not a from-scratch type). Small enough to train and serve cheaply, big enough to read your task sentence and generalize. At each moment it gets:

1. The front camera image
2. The wrist camera image
3. The six current motor angles
4. **The task sentence** — it genuinely reads the instruction

It outputs a **chunk** — a short plan of future motor angles.

## "Predict 50, execute ~25"

```
[■■■■■■■■■■■■■][□□□□□□□□□□□□□]
 execute first    rest of the chunk — thrown away
 ~25 steps        ↺ then look at cameras again, predict a fresh 50
```

- The policy predicts 50 steps ahead (`chunk_size=50`) but the client executes roughly the first half (`actions_per_chunk=25`), then re-looks and re-requests.
- Too long a chunk → the plan diverges from reality before it finishes. Too short → the computer can't keep up with the control loop.
- The chunk size is **set at training time** (baked into the policy's config); the execute count is set at rollout.

## Three facts about SmolVLA that explain almost everything you will observe

1. **It starts smart, and your demos specialize it.** Unlike a from-scratch model, SmolVLA already understands objects, language, and manipulation in general; your episodes teach it your specific arm, cameras, and task. It generalizes better than small models — but coverage still comes from varied episodes, not from more training steps.
2. **Consistency still beats quantity.** Inconsistent demonstrations still teach a muddled behavior. Pick one style — same build order, same grasps — and repeat it every episode.
3. **The cameras and your task sentence are its inputs.** With a language-conditioned model, the task sentence describes the goal, and consistency of wording between recording and rollout matters. If you can't do the task from the camera images alone, neither can the model — which is why you watch the feeds, never the physical robot, while recording.

## The model landscape (context)

Options this project considered, in size order:

- **ACT** (~80M params, from-scratch) — fast and light, but single-task and memorization-bound
- **SmolVLA** (~450M params) — HF's language-conditioned VLA; **the plan of record** — cheap to train (a10g), light to serve, no async-serving traps
- **π₀ (pi0)** — ~3B params, PaliGemma backbone, diffusion action expert
- **GR00T N1.7** (~3B params) — NVIDIA's reasoning VLA; tried 2026-08-12/13, retired: needed A100 training, 12.6 GB checkpoints (storage pain), and relative-action/serving incompatibilities

[← Glossary](00-glossary.md) · [README](../README.md) · [Next: Version drift →](02-version-drift.md)
