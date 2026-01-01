import time
from stable_baselines3 import PPO
from env import RaceEnv

# Load trained model
model = PPO.load("ppo_race")

# Create env with rendering
env = RaceEnv(render_mode="human")

obs, info = env.reset(show_ray=False)

while True:

    # Predict action (deterministic = True for evaluation)
    action, _ = model.predict(obs, deterministic=True)

    obs, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        obs, info = env.reset(show_ray=False)
    
    time.sleep(0.02)