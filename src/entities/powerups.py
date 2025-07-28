#!/usr/bin/env python3
"""
Entidad PowerUp para PyGame Shooter
Autor: Kava
Fecha: 2024-12-19
Descripción: Lógica y visualización de los power-ups recogibles en el juego.
"""
import pygame
import random
from utils.advanced_logger import get_logger

class PowerUp:
    def __init__(self, x, y, powerup_type, logger=None):
        self.x = x
        self.y = y
        self.type = powerup_type
        self.size = 30
        self.speed = 2
        self.logger = logger or get_logger("PyGame")
        
        # Colores por tipo de powerup
        self.colors = {
            "health": (255, 0, 0),      # Rojo
            "fast_shot": (0, 255, 0),   # Verde
            "shield": (0, 0, 255)       # Azul
        }
        
        self.color = self.colors.get(powerup_type, (255, 255, 255))  # Blanco por defecto
        
        self.logger.log_debug(f"PowerUp {powerup_type} creado en posición ({x}, {y})", "powerup")
    
    def update(self):
        """Actualiza la posición del powerup."""
        self.y += self.speed
    
    def draw(self, screen):
        """Dibuja el powerup."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size // 2)
        
        # Dibujar un borde para hacerlo más visible
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size // 2, 2)
    
    def get_collision_rect(self):
        """Retorna el rectángulo de colisión del powerup."""
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
    
    def is_off_screen(self, screen_height):
        """Verifica si el powerup está fuera de la pantalla."""
        return self.y > screen_height

