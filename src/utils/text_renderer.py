#!/usr/bin/env python3
"""
Renderizador de texto optimizado para PyGame Shooter
Autor: Kava
Fecha: 2024-12-19
Descripción: Renderizado de texto para HUD y menús usando ptext y logging avanzado.
"""

import pygame
import ptext
import os
import sys
from typing import Tuple, Optional, Dict, Any

# Añadir el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from utils.advanced_logger import get_logger
except ImportError:
    # Fallback para cuando se ejecuta desde tools/
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    from utils.advanced_logger import get_logger


class TextRenderer:
    """
    Sistema de renderizado de texto optimizado usando ptext.
    Proporciona renderizado de texto rápido y con efectos visuales.
    """
    
    def __init__(self, logger=None):
        """
        Inicializa el renderizador de texto.
        
        Args:
            logger: Instancia del logger para debug (opcional, usa AdvancedLogger por defecto)
        """
        self.logger = logger or get_logger("PyGame")
        self.default_font = None
        self.font_cache: Dict[str, pygame.font.Font] = {}
        
        # Configuración por defecto
        self.default_color = (255, 255, 255)  # Blanco
        self.default_size = 24
        self.default_font_name = "Arial"
        
        self.logger.log_event("TextRenderer inicializado con ptext", "text")
    
    def load_font(self, font_name: str, size: int) -> Optional[pygame.font.Font]:
        """
        Carga una fuente específica.
        
        Args:
            font_name: Nombre de la fuente
            size: Tamaño de la fuente
            
        Returns:
            Fuente cargada o None si falla
        """
        font_key = f"{font_name}_{size}"
        
        if font_key in self.font_cache:
            return self.font_cache[font_key]
        
        try:
            font = pygame.font.Font(font_name, size)
            self.font_cache[font_key] = font
            self.logger.log_debug(f"Fuente cargada: {font_name} tamaño {size}", "text")
            return font
        except Exception as e:
            self.logger.log_error(f"Error cargando fuente {font_name}: {e}", "text")
            return None
    
    def render_text(self, text: str, x: int, y: int, 
                   color: Optional[Tuple[int, int, int]] = None,
                   size: Optional[int] = None,
                   font_name: Optional[str] = None,
                   screen_width: Optional[int] = None) -> None:
        """
        Renderiza texto en una posición específica.
        
        Args:
            text: Texto a renderizar
            x: Posición X
            y: Posición Y
            color: Color del texto (RGB)
            size: Tamaño de la fuente
            font_name: Nombre de la fuente
            screen_width: Ancho de pantalla para centrado
        """
        try:
            color = color or self.default_color
            size = size or self.default_size
            
            # Usar ptext para renderizado optimizado
            ptext.draw(text, (x, y), color=color, fontsize=size, fontname=font_name)
            
        except Exception as e:
            self.logger.log_error(f"Error renderizando texto '{text}': {e}", "text")
    
    def render_centered_text(self, text: str, y: int, 
                           color: Optional[Tuple[int, int, int]] = None,
                           size: Optional[int] = None,
                           font_name: Optional[str] = None,
                           screen_width: Optional[int] = None) -> None:
        """
        Renderiza texto centrado horizontalmente.
        
        Args:
            text: Texto a renderizar
            y: Posición Y
            color: Color del texto (RGB)
            size: Tamaño de la fuente
            font_name: Nombre de la fuente
            screen_width: Ancho de pantalla para centrado
        """
        try:
            color = color or self.default_color
            size = size or self.default_size
            screen_width = screen_width or 800  # Valor por defecto
            
            # Usar ptext para centrado automático
            ptext.draw(text, (screen_width//2, y), color=color, fontsize=size, 
                      fontname=font_name, center=True)
            
        except Exception as e:
            self.logger.log_error(f"Error renderizando texto centrado '{text}': {e}", "text")
    
    def render_right_aligned_text(self, text: str, x: int, y: int,
                                color: Optional[Tuple[int, int, int]] = None,
                                size: Optional[int] = None,
                                font_name: Optional[str] = None) -> None:
        """
        Renderiza texto alineado a la derecha.
        
        Args:
            text: Texto a renderizar
            x: Posición X (punto de referencia derecho)
            y: Posición Y
            color: Color del texto (RGB)
            size: Tamaño de la fuente
            font_name: Nombre de la fuente
        """
        try:
            color = color or self.default_color
            size = size or self.default_size
            
            # Usar ptext para alineación a la derecha
            ptext.draw(text, (x, y), color=color, fontsize=size, 
                      fontname=font_name, right=True)
            
        except Exception as e:
            self.logger.log_error(f"Error renderizando texto alineado a la derecha '{text}': {e}", "text")
    
    def get_text_size(self, text: str, size: Optional[int] = None, 
                     font_name: Optional[str] = None) -> Tuple[int, int]:
        """
        Obtiene el tamaño de un texto.
        
        Args:
            text: Texto a medir
            size: Tamaño de la fuente
            font_name: Nombre de la fuente
            
        Returns:
            Tupla con (ancho, alto) del texto
        """
        try:
            size = size or self.default_size
            
            # Usar ptext para obtener dimensiones
            width, height = ptext.getsize(text, fontsize=size, fontname=font_name)
            return width, height
            
        except Exception as e:
            self.logger.log_error(f"Error obteniendo tamaño de texto '{text}': {e}", "text")
            return 0, 0
    
    def render_text_with_shadow(self, text: str, x: int, y: int,
                              color: Optional[Tuple[int, int, int]] = None,
                              shadow_color: Optional[Tuple[int, int, int]] = None,
                              size: Optional[int] = None,
                              font_name: Optional[str] = None) -> None:
        """
        Renderiza texto con sombra.
        
        Args:
            text: Texto a renderizar
            x: Posición X
            y: Posición Y
            color: Color del texto (RGB)
            shadow_color: Color de la sombra (RGB)
            size: Tamaño de la fuente
            font_name: Nombre de la fuente
        """
        try:
            color = color or self.default_color
            shadow_color = shadow_color or (0, 0, 0)  # Negro por defecto
            size = size or self.default_size
            
            # Renderizar sombra primero
            ptext.draw(text, (x + 2, y + 2), color=shadow_color, fontsize=size, fontname=font_name)
            
            # Renderizar texto principal
            ptext.draw(text, (x, y), color=color, fontsize=size, fontname=font_name)
            
        except Exception as e:
            self.logger.log_error(f"Error renderizando texto con sombra '{text}': {e}", "text")
    
    def render_text_with_outline(self, text: str, x: int, y: int,
                               color: Optional[Tuple[int, int, int]] = None,
                               outline_color: Optional[Tuple[int, int, int]] = None,
                               size: Optional[int] = None,
                               font_name: Optional[str] = None) -> None:
        """
        Renderiza texto con contorno.
        
        Args:
            text: Texto a renderizar
            x: Posición X
            y: Posición Y
            color: Color del texto (RGB)
            outline_color: Color del contorno (RGB)
            size: Tamaño de la fuente
            font_name: Nombre de la fuente
        """
        try:
            color = color or self.default_color
            outline_color = outline_color or (0, 0, 0)  # Negro por defecto
            size = size or self.default_size
            
            # Renderizar contorno en todas las direcciones
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        ptext.draw(text, (x + dx, y + dy), color=outline_color, 
                                 fontsize=size, fontname=font_name)
            
            # Renderizar texto principal
            ptext.draw(text, (x, y), color=color, fontsize=size, fontname=font_name)
            
        except Exception as e:
            self.logger.log_error(f"Error renderizando texto con contorno '{text}': {e}", "text")
    
    def clear_cache(self) -> None:
        """Limpia la caché de fuentes."""
        self.font_cache.clear()
        self.logger.log_event("Caché de fuentes limpiada", "text")
    
    def __str__(self) -> str:
        """Representación en string del renderizador."""
        return f"TextRenderer(fonts_cached={len(self.font_cache)})"
    
    def __repr__(self) -> str:
        """Representación detallada del renderizador."""
        return f"TextRenderer(fonts_cached={len(self.font_cache)}, default_size={self.default_size})" 