# 11 — Robot-friendly mortar: what the industry actually uses

[← Brick curriculum](10-brick-curriculum.md) · [README](../README.md) · [Next: Hardware ladder →](12-hardware-ladder.md)

The instinct about "specialised mortar that robots can handle" is exactly right — and the industry's answer is mostly to **abandon traditional mortar**:

| System | How it bonds bricks | Lesson |
|---|---|---|
| **FBR Hadrian X** (Australia) | No mortar. Machine-applied bead of quick-curing construction adhesive; structural in ~45 min. Lays 45 kg blocks via a 30 m boom. | Adhesive beats mortar for robots: no slump, thin bead, fast strength, no mason finishing. |
| **Monumental** (Netherlands) | Real mortar, extruded from a computer-controlled head. Three-robot cell (ferry, supply, lay); vision/SLAM vs. BIM model; ~0.5 mm accuracy; human smooths joints. | Real mortar is solvable — but rheology control is their moat. Not a garage project. |
| **SAM100** (Construction Robotics, USA) | Conventional mortar pumped to a nozzle that butters each brick; human strikes the joints. | Even the pragmatic approach keeps a human in the mortar loop. |
| **AAC thin-bed mortar** (ASTM C1660) | Polymer-modified cement in 1–3 mm joints — possible because AAC blocks are dimensionally accurate to ±1 mm. | **The Stage-4 system.** Unit tolerance is what makes joints robot-friendly. |
| **PU masonry foam** (Porotherm Dryfix, Tytan) | Gun-applied foam bead on flat, accurate blocks; wall loadable in hours; works to −5 °C. | **Most hobby-robot-friendly of all:** a foam gun is a trivially easy end effector. No pumps, no rheology. |

## What makes a bonding system "robot-handleable"

1. **Long open time** — minutes to reposition, not seconds
2. **Extrudability** — flows through a nozzle without separating
3. **Thin-bed application** — eliminates the wiggle-and-squeeze technique human masons perform
4. **Tolerance forgiveness** — small placement errors don't compound
5. **Fast green strength** — lower courses don't creep under new load

PU foam and AAC thin-bed score best on all five. Traditional trowel mortar scores worst.

## Strategic note

Every commercial system above uses **CAD plans + position control + good metrology — none uses learned policies.** Learned masonry exists only in academic papers (2025): RL for masonry dry-stacking (15th Canadian Masonry Symposium), force-based two-phase imitation learning for construction assembly (arXiv 2501.14942), GAIL for long-horizon construction tasks. The imitation-learning route is genuinely fresh ground — and the industry's history says the hard parts are mortar flow, tolerances, and payload, which is exactly what the [staged curriculum](10-brick-curriculum.md) practices.

## Sources

- Hadrian X: https://www.fbr.com.au/ · https://newatlas.com/robotics/hadrian-x-bricklaying-robot/
- Monumental: https://www.monumental.co/ · https://techcrunch.com/2024/02/17/dutch-startup-monumental-is-using-robots-to-lay-bricks/
- SAM100: https://www.construction-robotics.com/sam-2/ · US patent 8825208
- AAC thin-bed: https://imiweb.org/wp-content/uploads/2015/10/01.02-AAC-MASONRY-UNITS.pdf
- PU foam: https://tytan.com/en/product/foam-adhesives/foam-adhesive-for-bricklaying/
- RL dry-stacking: https://www.canadamasonrydesigncentre.com/wp-content/uploads/15th_symposium/027-Zeng.pdf
- Force-based IL for assembly: https://arxiv.org/pdf/2501.14942

[← Brick curriculum](10-brick-curriculum.md) · [README](../README.md) · [Next: Hardware ladder →](12-hardware-ladder.md)
