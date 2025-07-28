# src/ui/menus/character_selection_menu.py
# Cabecera descriptiva
# Nombre del script: character_selection_menu.py
# Autor: Gemini
# Fecha: 27 de julio de 2025
# Descripción: Implementa el menú de selección de personaje.

import pygame
from ui.menus.base_menu import BaseMenu
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CHARACTER_STATS, PLAYER_SIZE, WHITE, YELLOW, RED, FONT_SIZE, BLACK
from utils.image_loader import load_animation_frames

class CharacterSelectionMenu(BaseMenu):
    def __init__(self, screen, logger):
        super().__init__(screen, logger, title_text="Selecciona tu Personaje", options=[])
        self.characters = list(CHARACTER_STATS.keys())
        self.selected_character_index = 0

        # Cargar las imágenes de los personajes para el menú
        self.character_images = {}
        for char_name, stats in CHARACTER_STATS.items():
            image_folder = stats["image_folder"]
            try:
                idle_frames = load_animation_frames(image_folder, "Idle", stats["idle_frames"])
                if idle_frames:
                    image = idle_frames[0]
                    self.character_images[char_name] = pygame.transform.scale(image, (PLAYER_SIZE * 2, PLAYER_SIZE * 2))
                else:
                    self.logger.log_error(f"No se encontraron frames para la animación Idle de {char_name}")
                    self.character_images[char_name] = pygame.Surface((PLAYER_SIZE * 2, PLAYER_SIZE * 2))
                    self.character_images[char_name].fill(RED)
            except SystemExit:
                self.logger.log_error(f"No se pudo cargar la imagen para {char_name} en {image_folder}")
                self.character_images[char_name] = pygame.Surface((PLAYER_SIZE * 2, PLAYER_SIZE * 2))
                self.character_images[char_name].fill(RED)

        self.character_name_font = pygame.font.Font(None, int(FONT_SIZE * 1.5))
        self.small_font = pygame.font.Font(None, FONT_SIZE)

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.logger.log_event("Juego terminado por el usuario desde selección de personaje")
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.selected_character_index = (self.selected_character_index - 1) % len(self.characters)
                elif event.key == pygame.K_RIGHT:
                    self.selected_character_index = (self.selected_character_index + 1) % len(self.characters)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return self.characters[self.selected_character_index]
                elif event.key == pygame.K_ESCAPE:
                    return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                center_x = SCREEN_WIDTH // 2
                center_y = SCREEN_HEIGHT // 2
                img_rect = pygame.Rect(center_x - PLAYER_SIZE, center_y - PLAYER_SIZE, PLAYER_SIZE * 2, PLAYER_SIZE * 2)
                accept_rect = pygame.Rect(center_x - 100, center_y + PLAYER_SIZE + 110, 200, 50)
                if img_rect.collidepoint(mouse_x, mouse_y) or accept_rect.collidepoint(mouse_x, mouse_y):
                    return self.characters[self.selected_character_index]
        return None

    def show(self):
        self.logger.log_debug("Mostrando menú de selección de personaje.")
        while True:
            selected = self._handle_input()
            if selected is not None:
                return selected
            self._draw()

    def _draw(self):
        self.screen.fill(BLACK)
        # Título
        self.screen.blit(self.title_text_surface, self.title_rect)
        # Imagen del personaje
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        char_name = self.characters[self.selected_character_index]
        img = self.character_images[char_name]
        img_rect = img.get_rect(center=(center_x, center_y))
        self.screen.blit(img, img_rect)
        # Nombre y descripción
        stats = CHARACTER_STATS[char_name]
        name_surface = self.character_name_font.render(stats["name"], True, YELLOW)
        name_rect = name_surface.get_rect(center=(center_x, center_y + PLAYER_SIZE + 40))
        self.screen.blit(name_surface, name_rect)
        desc_surface = self.small_font.render(stats["description"], True, WHITE)
        desc_rect = desc_surface.get_rect(center=(center_x, center_y + PLAYER_SIZE + 80))
        self.screen.blit(desc_surface, desc_rect)
        # Botón Aceptar
        accept_rect = pygame.Rect(center_x - 100, center_y + PLAYER_SIZE + 110, 200, 50)
        pygame.draw.rect(self.screen, YELLOW, accept_rect, border_radius=10)
        accept_font = pygame.font.Font(None, int(FONT_SIZE * 1.2))
        accept_text = accept_font.render("Aceptar", True, BLACK)
        accept_text_rect = accept_text.get_rect(center=accept_rect.center)
        self.screen.blit(accept_text, accept_text_rect)
        # Indicadores izquierda/derecha
        arrow_font = pygame.font.Font(None, int(FONT_SIZE * 2))
        left_arrow = arrow_font.render("<", True, WHITE)
        right_arrow = arrow_font.render(">", True, WHITE)
        self.screen.blit(left_arrow, (center_x - PLAYER_SIZE * 2, center_y - 20))
        self.screen.blit(right_arrow, (center_x + PLAYER_SIZE * 1.5, center_y - 20))
        pygame.display.flip()
