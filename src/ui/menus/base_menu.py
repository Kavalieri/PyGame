# src/ui/menus/base_menu.py
# Cabecera descriptiva
# Nombre del script: base_menu.py
# Autor: Gemini
# Fecha: 27 de julio de 2025
# Descripción: Clase base para la creación de menús con navegación por teclado y ratón.

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, FONT_SIZE, FONT_COLOR, BUTTON_COLOR, HOVER_COLOR
from utils.image_loader import load_image

class BaseMenu:
    def __init__(self, screen, logger, title_text="Menú", options=None, background_image_path=None, button_images=None):
        self.screen = screen
        self.logger = logger
        self.font = pygame.font.Font(None, FONT_SIZE * 2)
        self.options_font = pygame.font.Font(None, FONT_SIZE)
        self.title_text_surface = self.font.render(title_text, True, FONT_COLOR)
        self.title_rect = self.title_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

        self.options = options if options is not None else []
        self.buttons = []
        self.selected_option_index = 0

        self.background_image = None
        if background_image_path:
            self.background_image = load_image(background_image_path)
            self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.button_images = {
            'normal': None,
            'hover': None
        }
        if button_images:
            if 'normal' in button_images: self.button_images['normal'] = load_image(button_images['normal'])
            if 'hover' in button_images: self.button_images['hover'] = load_image(button_images['hover'])

        self._setup_buttons()

    def _setup_buttons(self):
        pass

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.logger.log_event("Juego terminado por el usuario desde menú")
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option_index = (self.selected_option_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option_index = (self.selected_option_index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return self.options[self.selected_option_index]["action"]
                elif event.key == pygame.K_ESCAPE:
                    return "toggle_pause"
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(self.buttons):
                    if button["rect"].collidepoint(mouse_pos):
                        self.selected_option_index = i
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(self.buttons):
                    if button["rect"].collidepoint(mouse_pos):
                        return self.options[i]["action"]
        return None

    def _draw(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(BLACK)

        self.screen.blit(self.title_text_surface, self.title_rect)

        button_height = 80
        button_margin = 20
        total_height = len(self.options) * (button_height + button_margin) - button_margin
        start_y = (SCREEN_HEIGHT // 2) - (total_height // 2)

        self.buttons = []
        for i, option in enumerate(self.options):
            button_rect = pygame.Rect(
                (SCREEN_WIDTH // 2) - 200,
                start_y + i * (button_height + button_margin),
                400,
                button_height
            )
            if i == self.selected_option_index:
                button_image = self.button_images['hover'] if self.button_images['hover'] else None
                color = HOVER_COLOR
            else:
                button_image = self.button_images['normal'] if self.button_images['normal'] else None
                color = BUTTON_COLOR

            if button_image:
                self.screen.blit(pygame.transform.scale(button_image, (400, button_height)), button_rect)
            else:
                pygame.draw.rect(self.screen, color, button_rect, border_radius=12)

            text_surface = self.options_font.render(option["text"], True, FONT_COLOR)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)

            self.buttons.append({"rect": button_rect})

        pygame.display.flip()

    def show(self):
        self.logger.log_debug(f"Mostrando menú base: {self.__class__.__name__}")
        while True:
            action = self._handle_input()
            if action:
                return action
            self._draw()
