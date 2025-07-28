#!/usr/bin/env python3
"""
Punto de entrada principal para PyGame Shooter
Autor: Kava
Fecha: 2024-12-19
Descripción: Inicializa el sistema, configura logging y ejecuta el bucle principal del juego.
"""
import pygame
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game_loop_improved import GameLoop
from utils.advanced_logger import setup_logging

def main():
	# Configurar el sistema de logging avanzado
	logger = setup_logging("PyGame", "logs")
	
	# Inicialización de Pygame
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption('PyGame Shooter')

	logger.log_event("Inicializando PyGame", "main")
	logger.log_system_info()

	# Crear y ejecutar el nuevo bucle de juego mejorado
	juego = GameLoop(screen, logger)
	juego.run()

	# Al salir, limpiar recursos
	juego.cleanup()
	pygame.quit()
	logger.log_event("Aplicación terminada", "main")
	sys.exit()

if __name__ == "__main__":
	main()
