import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
import math
import random

from assets import Car, Track
from utils import cast_ray

WIDTH = 800
HEIGHT = 600

# Game Variables

CAR_XY = [(600, 500), (300, 500), (140, 300), (380, 95)]

CAR_WIDTH = 10
CAR_HEIGHT = 20

SENSOR_ANGLES = [
    0,        # front
    30,
    -30,
    45,       # front-right
    -45,      # front-left
    90,       # right
    -90,      # left
    180       # back
]

# Colors
BLACK = (0, 0, 0)
GRASS_COLOR = (100, 255, 0)
RED = (255, 0, 0)
CAR_COLOR = (0, 200, 255)

class RaceEnv(gym.Env):
    metadata = {"render_modes":["human"]}

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode

        self.action_space = spaces.Box(
            low=np.array([-1.0, -1.0], dtype=np.float32),
            high=np.array([1.0, 1.0], dtype=np.float32),
            dtype=np.float32
        )
        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(10,), dtype=np.float32
        )

        if render_mode == "human":
            pygame.init()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            self.clock = pygame.time.Clock()
            self.bg_image = pygame.image.load("tracks/track1_bg.png").convert()
                
        self.reset()
    
    def reset(self, seed=None, options=None, show_ray=False):
        super().reset(seed=seed)

        x, y = random.choice(CAR_XY)
        self.car = Car(x, y, CAR_WIDTH, CAR_HEIGHT, CAR_COLOR)
        self.show_ray = show_ray
        self.track = Track((WIDTH, HEIGHT))         
        self.steps = 0
        return self._get_state(), {}

    def step(self, action):
        throttle, steer = action
        self.steps += 1

        throttle = (throttle+1)/2

        # Move Straight
        if throttle > 0.1:
            self.car.accelerate()
        else:
            self.car.brake()

        # Turn
        if steer > 0.1:
            self.car.turn_right()
        elif steer < -0.1:
            self.car.turn_left()

        # update movement
        self.car.update()

        terminated = not self.track.is_on_road(self.car)
        truncated = self.steps >= 2000
        
        if terminated:
            reward = -100
        else:
            reward = self.car.speed * 0.3

        if self.render_mode == "human":
            self.render()

        return self._get_state(), reward, terminated, truncated, {}

    def _get_state(self):
        sensors = self.get_sensors()

        return np.array([
            (self.car.angle % 360)/360,
            self.car.speed / self.car.max_speed,
            *[s / 200 for s in sensors]   # normalize
        ], dtype=np.float32)

    def render(self):
        # self.screen.fill(GRASS_COLOR)
        self.screen.blit(self.bg_image, (0, 0))
        self.track.draw(self.screen)
        if self.show_ray:
            cx, cy = int(self.car.x), int(self.car.y)

            for a, d in zip(SENSOR_ANGLES, self.get_sensors()):
                angle = math.radians(self.car.angle + a)
                end_x = cx + math.cos(angle) * d
                end_y = cy - math.sin(angle) * d
                pygame.draw.line(self.screen, (255, 100, 0), (cx, cy), (end_x, end_y), 2)

        self.car.draw(self.screen)
        pygame.display.update()
        self.clock.tick(30)
    
    def get_sensors(self):
        cx, cy = int(self.car.x), int(self.car.y)
        distances = []
        
        for a in SENSOR_ANGLES:
            ray_angle = self.car.angle + a
            d = cast_ray(
                self.track.road_mask,
                (cx, cy),
                ray_angle
            )
            distances.append(d)
        return distances
    def close(self):
        if self.render_mode == "human":
            pygame.quit()


if __name__ == "__main__":
    from stable_baselines3.common.env_checker import check_env
    env = RaceEnv()
    check_env(env)
    print("Alright!")
