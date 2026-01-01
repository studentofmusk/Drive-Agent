# 🏎️ PPO Self-Driving Car (Reinforcement Learning)

This project demonstrates a **2D self-driving car simulation** using **Reinforcement Learning (PPO)**.  
The environment is built with **Pygame + Gymnasium**, and the agent learns to drive using **ray-based sensors** instead of images.

---

## ✨ Features

- Continuous action space (steering + throttle)
- Ray-casting sensors (8 directions)
- PPO (Proximal Policy Optimization)
- Gymnasium-compatible custom environment
- Real-time visualization using Pygame
- Fully autonomous driving after training

---

## 📂 Project Structure

```text
.
├── assets.py          # Car and Track classes
├── env.py             # Gymnasium RL environment
├── utils.py           # Ray-casting logic
├── train_ppo.py       # PPO training script
├── test.py            # Run trained PPO agent
├── game.py            # Manual driving mode
├── tracks/
│   ├── track1.png
│   └── track1_bg.png
├── ppo_race.zip       # Trained PPO model
└── requirements.txt
```

🛠️ Installation

Follow these steps to install dependencies and set up the project locally.

1️⃣ Install Python

Ensure Python 3.9 or above is installed.

Check your version:

    python --version

If Python is not installed, download it from:
https://www.python.org/downloads/

⚠️ Windows users: Make sure to check “Add Python to PATH” during installation.


2️⃣ Clone the Repository

    git clone https://github.com/your-username/ppo-self-driving-car.git
    cd ppo-self-driving-car



3️⃣ Create a Virtual Environment (Recommended)
Windows

    python -m venv venv
    venv\Scripts\activate

Linux / macOS

    python3 -m venv venv
    source venv/bin/activate


After activation, your terminal should show (venv).

4️⃣ Install Project Dependencies
    
    pip install -r requirements.txt


This installs:

* pygame
* numpy
* gymnasium
* stable-baselines3
* torch


5️⃣ Verify Required Files

Make sure the following files exist before running the project:

    tracks/track1.png
    tracks/track1_bg.png
    ppo_race.zip


⚠️ These files are required for the environment and trained model to work.


▶️ Usage

Run the Trained PPO Agent

    python test.py

Expected Behavior

1. A Pygame window opens
2. The car drives autonomously
3. The environment resets automatically if the car goes off-track


🎮 Manual Driving Mode (Optional)

To control the car manually:

    python game.py


Controls

Key	Action

⬆️	Accelerate

⬅️	Turn Left

➡️	Turn Right

**R**	Reset after crash



🔄 Training the Agent (Optional)

To train the PPO agent from scratch:

    python train_ppo.py


The trained model will be saved as:

    ppo_race.zip
