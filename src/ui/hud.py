import pygame
from constants import *

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("assets/fonts/arcade.ttf", 36)
        self.powerup_font = pygame.font.Font("assets/fonts/arcade.ttf", 24)

    def draw(self, lives, shield_lives, score, current_level, time_remaining, active_powerups):
        # Dibujar corazones rojos para las vidas (de derecha a izquierda)
        total_hearts = 3
        heart_x_offset = 10
        heart_images = []
        for i in range(total_hearts):
            if i < lives:
                heart_images.append(pygame.image.load("assets/ui/Hearts_Red_1.png")) # Corazón completo
            else:
                heart_images.append(pygame.image.load("assets/ui/Hearts_Red_5.png")) # Corazón vacío
        # Mostrar corazones de izquierda a derecha (el de más a la derecha se vacía primero)
        for img in heart_images:
            self.screen.blit(img, (heart_x_offset, 10))
            heart_x_offset += img.get_width() + 5

        # Dibujar corazones azules para el escudo (aparecen a la derecha de los rojos)
        for i in range(shield_lives):
            shield_image = pygame.image.load("assets/ui/Hearts_Blue_1.png")
            self.screen.blit(shield_image, (heart_x_offset, 10))
            heart_x_offset += shield_image.get_width() + 5

        # Dibujar otros elementos del HUD
        score_text = self.font.render(f'Puntuación: {score}', True, GREEN)
        level_text = self.font.render(f'Nivel: {current_level}', True, BLUE)
        time_text = self.font.render(f'Tiempo: {int(time_remaining)}', True, CYAN)

        self.screen.blit(score_text, (10, 50))
        self.screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))
        self.screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 10, 50))

        # Dibujar power-ups activos
        powerup_y_offset = 90
        for p_type, p_time_left in active_powerups.items():
            powerup_text = self.powerup_font.render(f'{p_type}: {int(p_time_left)}s', True, YELLOW)
            self.screen.blit(powerup_text, (10, powerup_y_offset))
            powerup_y_offset += 30
