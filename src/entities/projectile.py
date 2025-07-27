import pygame
from src.core.constants import *

class Projectile:
    def __init__(self, x, y, target_x, target_y, size=PROJECTILE_SIZE, speed=PROJECTILE_SPEED, logger=None):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.target_x = target_x
        self.target_y = target_y
        self.direction_x = (target_x - x) / ((target_x - x)**2 + (target_y - y)**2)**0.5
        self.direction_y = (target_y - y) / ((target_x - x)**2 + (target_y - y)**2)**0.5
        self.logger = logger
        if self.logger:
            self.logger.log_debug(f"Proyectil creado en posición x={self.x}, y={self.y}, objetivo x={self.target_x}, y={self.target_y}")

    def move(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed
        if self.logger:
            self.logger.log_debug(f"Proyectil movido a posición x={self.x}, y={self.y}")

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)
