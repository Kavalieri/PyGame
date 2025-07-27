# src/ui/pause_menu.py
# Cabecera descriptiva
# Nombre del script: pause_menu.py
# Autor: Gemini
# Fecha: 27 de julio de 2025
# Descripción: Implementa el menú de pausa del juego.

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, FONT_SIZE, FONT_COLOR, BUTTON_COLOR, HOVER_COLOR

class PauseMenu:
    def __init__(self, screen, logger):
        self.screen = screen
        self.logger = logger
        self.font = pygame.font.Font(None, FONT_SIZE * 2) # Fuente más grande para el título
        self.options_font = pygame.font.Font(None, FONT_SIZE)
        self.title_text = self.font.render("PAUSA", True, FONT_COLOR)
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

        self.options = [
            {"text": "Reanudar", "action": "resume"},
            {"text": "Volver al Menú Principal", "action": "main_menu"},
            {"text": "Salir del Juego", "action": "exit"}
        ]
        self.buttons = []
        self._setup_buttons()

    def _setup_buttons(self):
        self.buttons = []
        button_width = 300
        button_height = 60
        start_y = SCREEN_HEIGHT // 2 - (len(self.options) * button_height) // 2

        for i, option in enumerate(self.options):
            text_surface = self.options_font.render(option["text"], True, FONT_COLOR)
            button_rect = pygame.Rect(
                (SCREEN_WIDTH - button_width) // 2,
                start_y + i * (button_height + 20), # 20px de espacio entre botones
                button_width,
                button_height
            )
            self.buttons.append({"rect": button_rect, "text_surface": text_surface, "action": option["action"]})

    def show(self):
        self.logger.log_debug("Mostrando menú de pausa.")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.logger.log_event("Saliendo del juego desde el menú de pausa.")
                    pygame.quit()
                    import sys
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # Clic izquierdo
                        for button in self.buttons:
                            if button["rect"].collidepoint(event.pos):
                                self.logger.log_event(f"Opción seleccionada en menú de pausa: {button['action']}")
                                return button["action"]
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        self.logger.log_debug("Reanudando juego desde menú de pausa (tecla P/ESC).")
                        return "resume"

            self.screen.fill(BLACK) # Fondo oscuro para el menú de pausa
            self.screen.blit(self.title_text, self.title_rect)

            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                color = BUTTON_COLOR
                if button["rect"].collidepoint(mouse_pos):
                    color = HOVER_COLOR
                pygame.draw.rect(self.screen, color, button["rect"])
                
                # Centrar texto en el botón
                text_rect = button["text_surface"].get_rect(center=button["rect"].center)
                self.screen.blit(button["text_surface"], text_rect)

            pygame.display.flip()
