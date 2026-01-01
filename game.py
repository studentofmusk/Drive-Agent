import pygame
from assets import Car, Track
import sys
import math
from utils import cast_ray
import random

pygame.init()

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

# Clock
clock = pygame.time.Clock()
FPS = 30

# Font
font = pygame.font.SysFont(None, 20)

class Action:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class RaceEnv:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.reset()
        self.bg_image = pygame.image.load("tracks/track1_bg.png")
    
    def reset(self):
        x, y = random.choice(CAR_XY)
        self.car = Car(x, y, CAR_WIDTH, CAR_HEIGHT, CAR_COLOR)
        self.track = Track((WIDTH, HEIGHT))         
        self.game_over = False

    def step(self, action:Action):
        
        if not self.game_over:
            # Move Straight
            if action.x == 1:
                self.car.accelerate()
            else:
                self.car.brake()

            # Turn
            if action.y == 1:
                self.car.turn_right()
            elif action.y == -1:
                self.car.turn_left()

            # update movement
            self.car.update()

            # check on track
            if not self.track.is_on_road(self.car):
                self.game_over = True

        # Draw       
        self.render()

    def render(self):
        # self.screen.fill(GRASS_COLOR)
        self.screen.blit(self.bg_image, (0, 0))
        self.track.draw(self.screen)
        
        # Mouse position
        x, y = pygame.mouse.get_pos()

        # Render text
        text = font.render(f"({x}, {y})", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        cx, cy = int(self.car.x), int(self.car.y)

        for a, d in zip(SENSOR_ANGLES, self.get_sensors()):
            angle = math.radians(self.car.angle + a)
            end_x = cx + math.cos(angle) * d
            end_y = cy - math.sin(angle) * d
            pygame.draw.line(self.screen, (255, 100, 0), (cx, cy), (end_x, end_y), 2)

        self.car.draw(self.screen)
        
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


if __name__ == "__main__":
    game = RaceEnv()
    action = Action(0, 0)

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over:
                    game.reset()
        

        key_pressed = pygame.key.get_pressed()

        
        if key_pressed[pygame.K_RIGHT]:
            action.y = 1
        elif key_pressed[pygame.K_LEFT]:
            action.y = -1
        else:
            action.y = 0

        if key_pressed[pygame.K_UP]:
            action.x = 1
        else:
            action.x = 0

        game.step(action)

        pygame.display.update()