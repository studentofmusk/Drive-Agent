from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from env import RaceEnv

log_dir = "./logs/"

env = RaceEnv()

env = Monitor(env, log_dir)
model = PPO("MlpPolicy", env, verbose=1)
try:
    model.learn(total_timesteps=1_000_000)
except KeyboardInterrupt:
    print("Training interrupted! Saving model...")

model.save("ppo_race")
print("Model saved successfully.")