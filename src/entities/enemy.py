import pygame
import random
from src.core.constants import *

class Enemy:
    def __init__(self, x, y, size=ENEMY_SIZE, speed=ENEMY_SPEED, color=RED, health=1, logger=None):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.health = health
        self.logger = logger
        self.collision_box = pygame.Rect(self.x, self.y, self.size, self.size)
        if self.logger:
            self.logger.log_debug(f"Enemigo creado en posición x={self.x}, y={self.y}, tamaño={self.size}, velocidad={self.speed}, color={self.color}, salud={self.health}")

    def move(self):
        self.y += self.speed
        self.collision_box.topleft = (self.x, self.y)
        if self.logger:
            self.logger.log_debug(f"Enemigo movido a posición x={self.x}, y={self.y}")

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.collision_box)

    def is_off_screen(self, screen_height):
        return self.y > screen_height

    def take_damage(self, damage):
        self.health -= damage
        if self.logger:
            self.logger.log_debug(f"Enemigo en x={self.x}, y={self.y} recibió {damage} de daño. Salud restante: {self.health}")
        return self.health <= 0
