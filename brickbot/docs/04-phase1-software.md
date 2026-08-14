# 04 — Phase 1: Install the software

[← Phase 0](03-phase0-prepare.md) · [README](../README.md) · [Next: Phase 2 →](05-phase2-build-calibrate.md)

**Goal:** LeRobot installed and verified on the Mac (the machine connected to the arms), and the free online accounts created. Everything happens in the Terminal (macOS: ⌘-Space, type "Terminal", Enter).

> Training happens in the cloud via HF Jobs ([Phase 5](08-phase5-training.md)) — no second machine to set up. This page is for the robot machine.

1. **Install Miniconda (a Python manager).** If `conda --version` already works, skip. Otherwise, with Homebrew:

   ```bash
   brew install miniforge
   ```

   No Homebrew? Download the installer from https://conda-forge.org/download/, run it, then close and reopen the Terminal.

2. **Create the LeRobot environment** — a clean box named "lerobot" for all the robot software:

   ```bash
   conda create -y -n lerobot python=3.12
   ```

3. **Activate the environment:**

   ```bash
   conda activate lerobot
   ```

   **Remember this command.** Run it in every new Terminal window before any `lerobot-…` command. If a command ever says "command not found", this is almost always why.

4. **Install ffmpeg (video encoder):**

   ```bash
   conda install -y -c conda-forge ffmpeg
   ```

5. **Install LeRobot.** The extras in brackets matter: `feetech` talks to the servos, `core_scripts` provides record/teleop, `training` provides the trainer:

   ```bash
   pip install 'lerobot[core_scripts,training,feetech]'
   ```

6. **Verify the install:**

   ```bash
   lerobot-info
   ```

   It should print version information without errors. If not: [Troubleshooting](13-troubleshooting.md).

7. **Create a free Hugging Face account** at https://huggingface.co/join. Datasets and trained policies will live there. Note the username.

8. **Create an access token.** On huggingface.co: avatar → **Settings** → **Access Tokens** → **Create new token** → type **Write**. Copy the token (`hf_…`).

9. **Log in from the Terminal:**

    ```bash
    hf auth login
    ```

    Paste the token when asked (pasting shows nothing on screen — normal). Enter.

10. **Save the username as a shortcut.** Lets later commands say `${HF_USER}`. Run in every new Terminal window (or substitute by hand):

    ```bash
    HF_USER=$(NO_COLOR=1 hf auth whoami | awk -F': *' 'NR==1 {print $2}')
    echo $HF_USER   # should print the username
    ```

> LeLab (Hugging Face's GUI app for the SO-101) exists as an optional alternative to these commands — this project does not use it; everything runs from the Terminal.

[← Phase 0](03-phase0-prepare.md) · [README](../README.md) · [Next: Phase 2 →](05-phase2-build-calibrate.md)
