import pygame
from src.core.constants import *

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, type, logger=None):
        super().__init__()
        self.x = x
        self.y = y
        self.type = type
        self.size = 20
        self.color = WHITE # Default color
        self.speed = 2
        self.logger = logger

        if self.type == "health":
            self.color = GREEN
        elif self.type == "fast_shot":
            self.color = BLUE
        elif self.type == "shield":
            self.color = YELLOW

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

