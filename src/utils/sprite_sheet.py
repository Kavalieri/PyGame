#!/usr/bin/env python3
"""
Gestor de spritesheets y animaciones para PyGame Shooter
Autor: Kava
Fecha: 2024-12-19
Descripción: Manejo eficiente de spritesheets y animaciones con caché y logging avanzado.
"""

import pygame
import os
import sys
from typing import List, Tuple, Optional, Dict
from utils.advanced_logger import get_logger

# Añadir el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class SpriteSheet:
    """
    Clase para manejar spritesheets de forma eficiente.
    Permite cargar y extraer sprites individuales de una imagen de spritesheet.
    """
    
    def __init__(self, image_path: str, logger=None):
        """
        Inicializa el SpriteSheet.
        
        Args:
            image_path: Ruta al archivo de imagen del spritesheet
            logger: Instancia del logger para debug (opcional, usa AdvancedLogger por defecto)
        """
        self.logger = logger or get_logger("PyGame")
        self.image_path = image_path
        self.sheet = None
        self.sprite_cache: Dict[str, pygame.Surface] = {}
        
        self._load_sheet()
    
    def _load_sheet(self) -> None:
        """Carga la imagen del spritesheet."""
        try:
            if os.path.exists(self.image_path):
                self.sheet = pygame.image.load(self.image_path).convert_alpha()
                self.logger.log_debug(f"Spritesheet cargado: {self.image_path}", "spritesheet")
            else:
                self.logger.log_error(f"Archivo de spritesheet no encontrado: {self.image_path}", "spritesheet")
        except Exception as e:
            self.logger.log_error(f"Error cargando spritesheet {self.image_path}: {e}", "spritesheet")
    
    def get_sprite(self, x: int, y: int, width: int, height: int, 
                  scale: float = 1.0, cache_key: Optional[str] = None) -> Optional[pygame.Surface]:
        """
        Extrae un sprite del spritesheet.
        
        Args:
            x: Posición X en el spritesheet
            y: Posición Y en el spritesheet
            width: Ancho del sprite
            height: Alto del sprite
            scale: Factor de escala (1.0 = tamaño original)
            cache_key: Clave para cachear el sprite (opcional)
            
        Returns:
            Superficie del sprite o None si falla
        """
        if not self.sheet:
            return None
        
        try:
            # Crear clave de cache si no se proporciona
            if not cache_key:
                cache_key = f"{x}_{y}_{width}_{height}_{scale}"
            
            # Verificar cache
            if cache_key in self.sprite_cache:
                return self.sprite_cache[cache_key]
            
            # Extraer sprite del spritesheet
            sprite = self.sheet.subsurface((x, y, width, height))
            
            # Escalar si es necesario
            if scale != 1.0:
                new_width = int(width * scale)
                new_height = int(height * scale)
                sprite = pygame.transform.scale(sprite, (new_width, new_height))
            
            # Guardar en cache
            self.sprite_cache[cache_key] = sprite
            
            return sprite
            
        except Exception as e:
            self.logger.log_error(f"Error extrayendo sprite ({x}, {y}, {width}, {height}): {e}", "spritesheet")
            return None
    
    def get_sprite_grid(self, sprite_width: int, sprite_height: int, 
                       start_x: int = 0, start_y: int = 0,
                       cols: Optional[int] = None, rows: Optional[int] = None,
                       scale: float = 1.0) -> List[pygame.Surface]:
        """
        Extrae múltiples sprites en una cuadrícula.
        
        Args:
            sprite_width: Ancho de cada sprite
            sprite_height: Alto de cada sprite
            start_x: Posición X inicial
            start_y: Posición Y inicial
            cols: Número de columnas (None = automático)
            rows: Número de filas (None = automático)
            scale: Factor de escala
            
        Returns:
            Lista de sprites extraídos
        """
        if not self.sheet:
            return []
        
        sprites = []
        
        try:
            sheet_width, sheet_height = self.sheet.get_size()
            
            # Calcular número de columnas y filas si no se especifican
            if cols is None:
                cols = (sheet_width - start_x) // sprite_width
            if rows is None:
                rows = (sheet_height - start_y) // sprite_height
            
            # Extraer sprites
            for row in range(rows):
                for col in range(cols):
                    x = start_x + (col * sprite_width)
                    y = start_y + (row * sprite_height)
                    
                    sprite = self.get_sprite(x, y, sprite_width, sprite_height, scale)
                    if sprite:
                        sprites.append(sprite)
            
            self.logger.log_debug(f"Extraídos {len(sprites)} sprites de cuadrícula", "spritesheet")
            
        except Exception as e:
            self.logger.log_error(f"Error extrayendo sprites de cuadrícula: {e}", "spritesheet")
        
        return sprites
    
    def clear_cache(self) -> None:
        """Limpia la caché de sprites."""
        self.sprite_cache.clear()
        self.logger.log_event("Caché de sprites limpiada", "spritesheet")
    
    def get_cache_size(self) -> int:
        """Retorna el número de sprites en caché."""
        return len(self.sprite_cache)
    
    def __str__(self) -> str:
        """Representación en string del spritesheet."""
        return f"SpriteSheet(path='{self.image_path}', cached_sprites={len(self.sprite_cache)})"
    
    def __repr__(self) -> str:
        """Representación detallada del spritesheet."""
        return f"SpriteSheet(path='{self.image_path}', cached_sprites={len(self.sprite_cache)}, sheet_size={self.sheet.get_size() if self.sheet else 'None'})"


class AnimationManager:
    """
    Gestor de animaciones basado en spritesheets.
    Maneja la reproducción de animaciones con control de velocidad y loops.
    """
    
    def __init__(self, logger=None):
        """
        Inicializa el gestor de animaciones.
        
        Args:
            logger: Instancia del logger para debug (opcional, usa AdvancedLogger por defecto)
        """
        self.logger = logger or get_logger("PyGame")
        self.animations: Dict[str, Dict] = {}
        self.current_animation: Optional[str] = None
        self.current_frame = 0
        self.frame_time = 0
        self.animation_speed = 0.1  # segundos por frame
        self.loop = True
        self.paused = False
        
        self.logger.log_event("AnimationManager inicializado", "animation")
    
    def add_animation(self, name: str, frames: List[pygame.Surface], 
                     speed: float = 0.1, loop: bool = True) -> None:
        """
        Añade una nueva animación.
        
        Args:
            name: Nombre de la animación
            frames: Lista de frames (superficies)
            speed: Velocidad de la animación en segundos por frame
            loop: Si la animación debe repetirse
        """
        if not frames:
            self.logger.log_warning(f"Intento de añadir animación '{name}' sin frames", "animation")
            return
        
        self.animations[name] = {
            'frames': frames,
            'speed': speed,
            'loop': loop,
            'frame_count': len(frames)
        }
        
        self.logger.log_debug(f"Animación '{name}' añadida con {len(frames)} frames", "animation")
    
    def play_animation(self, name: str, reset: bool = True) -> bool:
        """
        Reproduce una animación.
        
        Args:
            name: Nombre de la animación
            reset: Si reiniciar la animación desde el principio
            
        Returns:
            True si la animación existe y se puede reproducir
        """
        if name not in self.animations:
            self.logger.log_warning(f"Animación '{name}' no encontrada", "animation")
            return False
        
        if self.current_animation != name or reset:
            self.current_animation = name
            self.current_frame = 0
            self.frame_time = 0
            self.animation_speed = self.animations[name]['speed']
            self.loop = self.animations[name]['loop']
            self.paused = False
            
            self.logger.log_debug(f"Reproduciendo animación: {name}", "animation")
        
        return True
    
    def update(self, delta_time: float) -> None:
        """
        Actualiza la animación actual.
        
        Args:
            delta_time: Tiempo transcurrido desde el último frame
        """
        if not self.current_animation or self.paused:
            return
        
        animation = self.animations[self.current_animation]
        self.frame_time += delta_time
        
        if self.frame_time >= self.animation_speed:
            self.frame_time = 0
            self.current_frame += 1
            
            # Verificar si la animación debe terminar o repetirse
            if self.current_frame >= animation['frame_count']:
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = animation['frame_count'] - 1
                    self.paused = True
    
    def get_current_frame(self) -> Optional[pygame.Surface]:
        """
        Obtiene el frame actual de la animación.
        
        Returns:
            Superficie del frame actual o None si no hay animación
        """
        if not self.current_animation:
            return None
        
        animation = self.animations[self.current_animation]
        if 0 <= self.current_frame < len(animation['frames']):
            return animation['frames'][self.current_frame]
        
        return None
    
    def pause(self) -> None:
        """Pausa la animación actual."""
        self.paused = True
        self.logger.log_debug("Animación pausada", "animation")
    
    def resume(self) -> None:
        """Reanuda la animación actual."""
        self.paused = False
        self.logger.log_debug("Animación reanudada", "animation")
    
    def stop(self) -> None:
        """Detiene la animación actual."""
        self.current_animation = None
        self.current_frame = 0
        self.frame_time = 0
        self.paused = False
        self.logger.log_debug("Animación detenida", "animation")
    
    def is_finished(self) -> bool:
        """
        Verifica si la animación actual ha terminado.
        
        Returns:
            True si la animación no está en loop y ha terminado
        """
        if not self.current_animation:
            return True
        
        animation = self.animations[self.current_animation]
        return not self.loop and self.current_frame >= animation['frame_count'] - 1
    
    def get_animation_names(self) -> List[str]:
        """
        Obtiene la lista de nombres de animaciones disponibles.
        
        Returns:
            Lista de nombres de animaciones
        """
        return list(self.animations.keys())
    
    def get_animation_info(self, name: str) -> Optional[Dict]:
        """
        Obtiene información de una animación específica.
        
        Args:
            name: Nombre de la animación
            
        Returns:
            Diccionario con información de la animación o None si no existe
        """
        if name in self.animations:
            return self.animations[name].copy()
        return None
    
    def clear_animations(self) -> None:
        """Limpia todas las animaciones."""
        self.animations.clear()
        self.current_animation = None
        self.current_frame = 0
        self.frame_time = 0
        self.paused = False
        self.logger.log_event("Todas las animaciones limpiadas", "animation")
    
    def __str__(self) -> str:
        """Representación en string del gestor de animaciones."""
        return f"AnimationManager(animations={len(self.animations)}, current='{self.current_animation}')"
    
    def __repr__(self) -> str:
        """Representación detallada del gestor de animaciones."""
        return f"AnimationManager(animations={len(self.animations)}, current='{self.current_animation}', paused={self.paused})" 