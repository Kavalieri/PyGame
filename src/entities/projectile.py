#!/usr/bin/env python3
"""
Entidad Proyectil para PyGame Shooter
Autor: Kava
Fecha: 2024-12-19
Descripción: Lógica de movimiento y colisión de proyectiles del jugador y enemigos.
"""
import pygame
import math
from utils.advanced_logger import get_logger

class Projectile:
    def __init__(self, x, y, target_x, target_y, size=10, speed=5, image_path=None, piercing=False, logger=None):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.piercing = piercing
        self.logger = logger or get_logger("PyGame")
        
        # Calcular dirección hacia el objetivo
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.dx = (dx / distance) * speed
            self.dy = (dy / distance) * speed
        else:
            self.dx = 0
            self.dy = speed  # Movimiento hacia abajo por defecto
        
        # Cargar imagen si se proporciona
        if image_path:
            try:
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (size, size))
            except Exception as e:
                self.logger.log_error(f"Error cargando imagen de proyectil {image_path}: {e}", "projectile")
                self.image = None
        else:
            self.image = None
        
        # Color por defecto si no hay imagen
        self.color = (255, 255, 0)  # Amarillo
        
        self.logger.log_debug(f"Proyectil creado en ({x}, {y}) hacia ({target_x}, {target_y}) con velocidad {speed}", "projectile")
    
    def update(self):
        """Actualiza la posición del proyectil."""
        self.x += self.dx
        self.y += self.dy
    
    def draw(self, screen):
        """Dibuja el proyectil."""
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size // 2)
    
    def is_off_screen(self, screen_width, screen_height):
        """Verifica si el proyectil está fuera de la pantalla."""
        return (self.x < 0 or self.x > screen_width or 
                self.y < 0 or self.y > screen_height)
    
    def get_collision_rect(self):
        """Retorna el rectángulo de colisión del proyectil."""
        return pygame.Rect(self.x, self.y, self.size, self.size)