#!/usr/bin/env python3
"""
Test simple para pygame-menu
Autor: Gemini
Fecha: 2024-12-19
Descripción: Test básico para verificar que pygame-menu funciona correctamente
"""

import pygame
import pygame_menu
import sys
import os

# Añadir el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def test_menu():
    """Test simple de pygame-menu."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Test Menu')
    
    # Crear un menú simple
    menu = pygame_menu.Menu(
        title='Test Menu',
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        theme=pygame_menu.themes.THEME_BLUE
    )
    
    # Añadir botones
    menu.add.button('Opción 1', lambda: print("Opción 1 seleccionada"))
    menu.add.button('Opción 2', lambda: print("Opción 2 seleccionada"))
    menu.add.button('Salir', pygame_menu.events.EXIT)
    
    print("Menú creado. Ejecutando mainloop...")
    
    # Ejecutar el menú
    try:
        action = menu.mainloop(screen)
        print(f"Acción seleccionada: {action}")
    except Exception as e:
        print(f"Error en menú: {e}")
    
    pygame.quit()

if __name__ == "__main__":
    test_menu() 