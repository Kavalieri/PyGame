import pygame
from constants import *
from utils.image_loader import load_image

class Projectile:
    def __init__(self, x, y, target_x, target_y, size=PROJECTILE_SIZE, speed=PROJECTILE_SPEED, image_path=None, color=WHITE, is_enemy=False, piercing=False, logger=None):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.target_x = target_x
        self.target_y = target_y
        self.direction_x = (target_x - x) / ((target_x - x)**2 + (target_y - y)**2)**0.5
        self.direction_y = (target_y - y) / ((target_x - x)**2 + (target_y - y)**2)**0.5
        self.color = color # Mantener color como fallback o para proyectiles sin imagen
        self.is_enemy = is_enemy
        self.piercing = piercing
        self.logger = logger

        self.image = None
        if image_path:
            self.image = load_image(image_path)
            self.image = pygame.transform.scale(self.image, (self.size, self.size))

        if self.logger:
            self.logger.log_debug(f"Proyectil creado en posición x={self.x}, y={self.y}, objetivo x={self.target_x}, y={self.target_y}, is_enemy={self.is_enemy}, piercing={self.piercing}")

    def move(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed
        if self.logger:
            self.logger.log_debug(f"Proyectil movido a posición x={self.x}, y={self.y}")

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (int(self.x - self.size / 2), int(self.y - self.size / 2))) # Centrar imagen
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)