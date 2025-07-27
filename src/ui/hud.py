import pygame
from constants import *

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.powerup_font = pygame.font.Font(None, 24)

    def draw(self, lives, score, current_level, time_remaining, active_powerups):
        lives_text = self.font.render(f'Vidas: {lives}', True, WHITE)
        score_text = self.font.render(f'Puntuación: {score}', True, WHITE)
        level_text = self.font.render(f'Nivel: {current_level}', True, WHITE)
        time_text = self.font.render(f'Tiempo: {int(time_remaining)}', True, WHITE)

        self.screen.blit(lives_text, (10, 10))
        self.screen.blit(score_text, (10, 50))
        self.screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))
        self.screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 10, 50))

        # Dibujar power-ups activos
        powerup_y_offset = 90
        for p_type, p_time_left in active_powerups.items():
            powerup_text = self.powerup_font.render(f'{p_type}: {int(p_time_left)}s', True, YELLOW)
            self.screen.blit(powerup_text, (10, powerup_y_offset))
            powerup_y_offset += 30
