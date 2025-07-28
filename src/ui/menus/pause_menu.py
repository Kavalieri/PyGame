# src/ui/menus/pause_menu.py
# Cabecera descriptiva
# Nombre del script: pause_menu.py
# Autor: Gemini
# Fecha: 27 de julio de 2025
# Descripción: Implementa el menú de pausa del juego.

import pygame
from ui.menus.base_menu import BaseMenu
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, FONT_SIZE, FONT_COLOR, BUTTON_COLOR, HOVER_COLOR

class PauseMenu(BaseMenu):
    def __init__(self, screen, logger):
        options = [
            {"text": "Reanudar", "action": "resume"},
            {"text": "Volver al Menú Principal", "action": "main_menu"},
            {"text": "Salir del Juego", "action": "exit"}
        ]
        super().__init__(screen, logger, title_text="PAUSA", options=options, 
                         background_image_path="assets/images/fondos/parque.jpg",
                         button_images={
                             'normal': "assets/images/ui/Buttons/Blue/Blank 1.png",
                             'hover': "assets/images/ui/Buttons/Blue/Blank 2.png"
                         })
        self.logger.log_debug("Menú de pausa inicializado.")

    def show(self):
        self.logger.log_debug("Mostrando menú de pausa.")
        while True:
            action = self._handle_input()
            if action == "toggle_pause":
                self.logger.log_debug("Reanudando juego desde menú de pausa (tecla P/ESC).")
                return "resume"
            elif action:
                return action
            self._draw()
