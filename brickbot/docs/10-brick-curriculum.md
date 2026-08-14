# 10 — The brick curriculum: from foam minis to real masonry

[← Phase 6](09-phase6-rollout.md) · [README](../README.md) · [Next: Mortar research →](11-mortar-research.md)

The numbers that shape the plan:

| Unit | Weight |
|---|---|
| Standard clay brick (194×92×57 mm) | **1.9–2.3 kg** |
| UK/engineering brick | 2.3–3.8 kg |
| AAC block cut to brick format (230×110×76 mm @ ~550 kg/m³) | **~1.0–1.1 kg** |
| Small AAC cube (~100 mm) | ~0.5–0.6 kg |
| Half-scale (1:2) fired clay brick | **250–400 g** |
| 1:12–1:6 kiln-fired clay minis | grams |
| **SO-101 usable payload** | **200–500 g** (500 g near base; 200–300 g at extension) |

## Stage 1 — Miniature masonry with your stacking-tower blocks (now, ~$0)

The wooden stacking-tower (Jenga-style) blocks are the stage-1 bricks: brick-shaped, ~10–20 g, rigid, with real sliding friction. Make the **task** harder, not the object:

1. Single placement (Phases 4–6 as written)
2. A straight course of blocks along a guide line with even 3–5 mm gaps
3. Two stacked courses (running bond)
4. A corner
5. **Endgame: rebuild the tower itself** — 3 blocks per layer, alternating direction each layer

A neat, evenly-spaced course of bricks IS bricklaying — in miniature. That gap-consistent running bond is the actual masonry skill.

Then swap to 1:12–1:6 kiln-fired clay minis (real ceramic, real friction, real fragility) and observe the re-learning cost of the material change — a preview of every later stage transition.

## Stage 2 — Half-scale real fired bricks (+2–3 months, ~$50–150)

Work up to 250–400 g half-scale fired clay bricks — the SO-101's ragged edge.

- Print a **wider gripper** with soft/compliant pads (TPU or foam).
- Keep the work **close to the robot's base** (payload drops fast with reach).
- New skills: tolerance stack-up over courses, chipped corners, and **recovery demonstrations** — deliberately record fixing a misplaced brick (the `dagger` rollout strategy records corrections).
- When servos overheat or strain: **stop.** That is the signal to plan Stage 4, not to push harder.

## Stage 3 — Adhesive skills (overlaps Stage 2, ~$100 tooling)

Skip traditional mortar (see [Mortar research](11-mortar-research.md) — the professionals mostly did too).

- Build a **servo-triggered glue-gun / caulk-gun end effector**.
- Practice with **hot glue** on Stage-2 bricks (cheap, removable): laying an even bead, speed-synchronized dispensing, clean bead starts/stops, pressing the brick to a set height.
- Graduate to PU masonry foam (Tytan/Dryfix-style) on the Stage-4 arm.

These are exactly the skills real robot masonry systems need.

## Stage 4 — Real masonry on a bigger arm ($3k–40k)

**Recommended target: AAC blocks + thin-bed/PU adhesive on an AgileX PiPER** (1.5 kg payload, 0.1 mm repeatability, ~$2,499, LeRobot support). AAC is real, building-code-recognized masonry designed for light units, ±1 mm accuracy, and 1–3 mm glued joints — a wall system that happens to fit robots perfectly.

- Budget path: PiPER + AAC brick-format units + PU foam ≈ **$3k total** — the cheapest credible "robot lays real masonry" demo.
- Stretch path: standard 2–3 kg clay bricks need a **Unitree Z1 Pro** (4 kg payload, ~$15k) or a used **UR5e** (~$30k+), plus a wide gripper (+$1–5k).

See [Hardware ladder](12-hardware-ladder.md) for the full comparison.

## What carries over between stages — and what doesn't

**Carries over:**
- The whole LeRobot pipeline (teleop rig, dataset format, training loops, eval discipline)
- Camera/scene setup instincts and recording habits
- Task decomposition (pick → align → place → press) and bond-pattern planning
- Old datasets can co-train alongside new ones

**Does not carry over:**
- **Trained policy weights** — each new arm is a new embodiment; you retrain
- Heavy-object physics intuition — sub-kg demos teach nothing about 2 kg swings
- The gripper design
- Precision: hobby servos land within ±2–3 mm; real thin-bed masonry wants ~±1 mm — an arm-hardware property no policy can conjure

[← Phase 6](09-phase6-rollout.md) · [README](../README.md) · [Next: Mortar research →](11-mortar-research.md)
