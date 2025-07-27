import pygame
from src.core.constants import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 50)

    def show(self, message):
        self.screen.fill(BLACK)
        text = self.font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def wait_for_key(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    return

    def show_game_over(self, score):
        self.screen.fill(BLACK)
        game_over_text = self.font.render("GAME OVER", True, RED)
        score_text = self.small_font.render(f"Puntuación: {score}", True, WHITE)
        restart_text = self.small_font.render("Presiona cualquier tecla para salir", True, WHITE)

        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
        pygame.display.flip()
        self.wait_for_key()
