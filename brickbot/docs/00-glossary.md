# 00 — Words you will see

[← README](../README.md) · [Next: Concepts →](01-concepts.md)

| Word | What it means here |
|---|---|
| **Follower arm** | The robot. It has a gripper. It does the work. |
| **Leader arm** | Your controller. It looks like the follower but has a handle with a trigger. You move it by hand; the follower copies it. |
| **Servo / motor** | The 12 black boxes in the kit (6 per arm). Each is a motor that knows its own angle and can be told to move to an angle. |
| **Teleoperation ("teleop")** | Driving the follower by moving the leader. No AI involved — a direct copy. |
| **Episode** | One recorded demonstration of the task, start to finish. About 20–30 seconds. |
| **Dataset** | The collection of episodes: camera videos plus motor angles, saved together. |
| **Policy** | The trained AI model. It looks at the cameras and decides how to move the motors. "Training a policy" = creating this model from your dataset. |
| **SmolVLA** | The policy this project trains: Hugging Face's pre-trained 450M vision-language-action model, fine-tuned on the recorded demonstrations. It reads the task sentence. |
| **Calibration** | A one-time procedure that teaches each arm the limits of its joints, so both arms agree on what "elbow at 90°" means. |
| **Hugging Face Hub** | A free website (like GitHub, but for AI) where datasets and policies are stored online. LeRobot uses it automatically. |
| **Terminal / command** | The text window where you type commands. Every command in this guide goes there. |
| **Environment (conda)** | A clean, separate box of Python software so LeRobot's packages don't clash with anything else on the computer. |
| **Chunk** | The short plan of future motor angles a policy outputs at each moment (see [Concepts](01-concepts.md)). |
| **Rollout** | Running the trained policy on the real robot. |

[← README](../README.md) · [Next: Concepts →](01-concepts.md)
