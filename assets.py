import pygame
from pygame import Surface
import math

class Track:
    ROAD = (100, 100, 100)
    GRASS = (100, 255, 0)

    def __init__(self, size=(800, 600)):
        self.width, self.height = size
        self.surface = pygame.image.load("tracks/track1.png")
        
        # Create road mask
        self.road_mask = pygame.mask.from_surface(self.surface)


    def draw(self, screen):
        mask_surface = self.road_mask.to_surface(
            setcolor=(255, 0, 0, 100),
            unsetcolor=(0, 0, 0, 0)
        )
        screen.blit(self.surface, (0, 0))
        # screen.blit(mask_surface, (0, 0))
    
    def is_on_road(self, car: 'Car') -> bool:
        offset = (
            int(car.rect.x),
            int(car.rect.y)
        )

        # Total pixels of the car
        car_pixels = car.mask.count()

        # Pixels where car overlaps road
        overlap_pixels = self.road_mask.overlap_area(car.mask, offset)

        # STRICT: every pixel must be on the road
        return overlap_pixels == car_pixels



class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        self.original_image = pygame.Surface((height, width), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, color, (0, 0, height, width))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # --- Physics --
        self.x, self.y = (x, y)
        self.angle = 0
        self.speed = 0
    

        # --- Tunable ---
        self.max_speed = 5
        self.acc = 0.2
        self.turn_speed = 3
    
    def accelerate(self):
        self.speed = min(self.speed + self.acc, self.max_speed)
    
    def brake(self):
        self.speed *= 0.9
    
    def turn_left(self):
        self.angle += self.turn_speed
    
    def turn_right(self):
        self.angle -= self.turn_speed

    def update(self):
        # Math movement
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y -= math.sin(rad) * self.speed

        self.image = pygame.transform.rotate(
            self.original_image, self.angle
        )
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # create mask 
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen: Surface):
        screen.blit(self.image, self.rect)
