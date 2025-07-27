import pygame
from src.core.constants import *

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def draw(self, lives, score):
        lives_text = self.font.render(f'Vidas: {lives}', True, WHITE)
        score_text = self.font.render(f'Puntuación: {score}', True, WHITE)
        self.screen.blit(lives_text, (10, 10))
        self.screen.blit(score_text, (10, 50))
