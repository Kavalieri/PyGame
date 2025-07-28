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
        
        if self.logger:
            self.logger.log_event(f"PowerUp inicializado en ({self.x},{self.y}) tipo={powerup_type}", "powerup")
        print(f"[DEBUG] PowerUp inicializado: {self}")
    
    def update(self):
        """Actualiza la posición del powerup."""
        self.y += self.speed
    
    def draw(self, screen):
        """Dibuja el powerup."""
        print(f"[DEBUG] Dibujando powerup en ({self.x},{self.y})")
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size // 2)
        
        # Dibujar un borde para hacerlo más visible
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size // 2, 2)
    
    def get_collision_rect(self):
        """Retorna el rectángulo de colisión del powerup."""
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
    
    def is_off_screen(self, screen_height):
        """Verifica si el powerup está fuera de la pantalla."""
        return self.y > screen_height

