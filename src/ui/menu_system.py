#!/usr/bin/env python3
"""
Sistema de menús avanzado usando pygame-menu para PyGame Shooter
Autor: Kava
Fecha: 2024-12-19
Descripción: Sistema modular de menús con integración de callbacks, temas y logging avanzado.
"""

import pygame
import pygame_menu
import os
import sys
from typing import Optional, Callable, Dict, Any, List

# Añadir el directorio src al path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from utils.advanced_logger import get_logger
    from constants import SCREEN_WIDTH, SCREEN_HEIGHT
except ImportError:
    # Fallback para cuando se ejecuta desde tools/
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
    from utils.advanced_logger import get_logger
    from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class MenuSystem:
    """
    Sistema de menús moderno usando pygame-menu.
    Proporciona interfaces profesionales con temas y animaciones.
    """
    
    def __init__(self, screen: pygame.Surface, logger=None):
        """
        Inicializa el sistema de menús.
        
        Args:
            screen: Superficie de pygame donde renderizar
            logger: Instancia del logger para debug (opcional, usa AdvancedLogger por defecto)
        """
        self.screen = screen
        self.logger = logger or get_logger("PyGame")
        self.current_menu: Optional[pygame_menu.Menu] = None
        self.menu_stack: List[pygame_menu.Menu] = []
        self.callbacks: Dict[str, Callable] = {}
        
        # Configuración del tema
        self.theme = self._create_theme()
        
        self.logger.log_event("Sistema de menús pygame-menu inicializado", "menu")
    
    def _create_theme(self) -> pygame_menu.themes.Theme:
        """Crea el tema personalizado para los menús."""
        theme = pygame_menu.themes.THEME_BLUE.copy()
        
        # Personalización del tema
        theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY_DIAGONAL
        theme.title_font_size = 45
        theme.title_font_color = (255, 255, 255)
        theme.title_background_color = (0, 0, 0, 180)
        
        # Botones
        theme.widget_font_size = 30
        theme.widget_font_color = (255, 255, 255)
        theme.widget_selection_color = (255, 255, 0)
        theme.widget_background_color = (0, 0, 0, 150)
        theme.widget_border_color = (100, 100, 100)
        theme.widget_border_width = 2
        
        # Menú principal
        theme.background_color = (0, 0, 0, 200)
        theme.menubar_close_button = False
        
        return theme
    
    def create_main_menu(self) -> pygame_menu.Menu:
        """Crea el menú principal del juego."""
        menu = pygame_menu.Menu(
            title='PyGame Shooter',
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            theme=self.theme,
            onclose=pygame_menu.events.EXIT
        )
        
        # Botones del menú principal
        menu.add.button('Nueva Partida', self._callback_wrapper('new_game'))
        menu.add.button('Cargar Partida', self._callback_wrapper('load_game'))
        menu.add.button('Opciones', self._callback_wrapper('options'))
        menu.add.button('Créditos', self._callback_wrapper('credits'))
        menu.add.button('Salir', pygame_menu.events.EXIT)
        
        self.logger.log_event("Menú principal creado", "menu")
        return menu
    
    def create_character_selection_menu(self) -> pygame_menu.Menu:
        """Crea el menú de selección de personajes."""
        menu = pygame_menu.Menu(
            title='Seleccionar Personaje',
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            theme=self.theme,
            onclose=self._callback_wrapper('back_to_main')
        )
        
        # Información de personajes
        characters = {
            'Kava': 'Guerrero equilibrado con buena velocidad y daño',
            'Adventure Girl': 'Personaje ágil con alta velocidad de movimiento',
            'Robot': 'Tanque con mucha vida pero movimiento lento'
        }
        
        for character_name, description in characters.items():
            frame = menu.add.frame_h(600, 100, background_color=(50, 50, 50, 150))
            frame._relax = True  # Permitir widgets más grandes que el frame
            frame.pack(menu.add.label(character_name, font_size=20))
            frame.pack(menu.add.label(description, font_size=15))
            frame.pack(menu.add.button('Seleccionar', 
                                     self._callback_wrapper('select_character', character_name)))
        
        menu.add.button('Volver', self._callback_wrapper('back_to_main'))
        
        self.logger.log_event("Menú de selección de personajes creado", "menu")
        return menu
    
    def create_pause_menu(self) -> pygame_menu.Menu:
        """Crea el menú de pausa."""
        menu = pygame_menu.Menu(
            title='Juego Pausado',
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            theme=self.theme,
            onclose=self._callback_wrapper('resume_game')
        )
        
        menu.add.button('Reanudar', self._callback_wrapper('resume_game'))
        menu.add.button('Opciones', self._callback_wrapper('options'))
        menu.add.button('Guardar', self._callback_wrapper('save_game'))
        menu.add.button('Menú Principal', self._callback_wrapper('main_menu'))
        menu.add.button('Salir', pygame_menu.events.EXIT)
        
        self.logger.log_event("Menú de pausa creado", "menu")
        return menu
    
    def create_upgrade_menu(self, points: int, points_spent: int, 
                           upgrade_levels: Dict[str, int]) -> pygame_menu.Menu:
        """Crea el menú de mejoras."""
        menu = pygame_menu.Menu(
            title='Mejoras Disponibles',
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            theme=self.theme,
            onclose=self._callback_wrapper('continue_game')
        )
        
        # Información de puntos
        points_frame = menu.add.frame_h(400, 80, background_color=(0, 100, 0, 150))
        points_frame.pack(menu.add.label(f'Puntos Disponibles: {points}', font_size=20))
        points_frame.pack(menu.add.label(f'Puntos Gastados: {points_spent}', font_size=20))
        
        # Opciones de mejora
        upgrades = [
            ('Velocidad', 'Aumenta la velocidad de movimiento', 'speed'),
            ('Vidas', 'Añade una vida extra', 'lives'),
            ('Cadencia', 'Reduce el tiempo entre disparos', 'fire_rate'),
            ('Proyectiles', 'Dispara múltiples proyectiles', 'projectiles'),
            ('Ataque Ráfaga', 'Disparo automático rápido', 'burst_attack'),
            ('Ataque Penetrante', 'Los proyectiles atraviesan enemigos', 'piercing_attack')
        ]
        
        for name, description, key in upgrades:
            level = upgrade_levels.get(key, 0)
            frame = menu.add.frame_h(500, 100, background_color=(0, 0, 0, 100))
            frame.pack(menu.add.label(f'{name} (Nivel {level})', font_size=20))
            frame.pack(menu.add.label(description, font_size=15))
            frame.pack(menu.add.button('Mejorar', 
                                     self._callback_wrapper('upgrade', key)))
        
        menu.add.button('Resetear Mejoras', self._callback_wrapper('reset_upgrades'))
        menu.add.button('Continuar', self._callback_wrapper('continue_game'))
        
        self.logger.log_event("Menú de mejoras creado", "menu")
        return menu
    
    def create_game_over_menu(self, final_score: int) -> pygame_menu.Menu:
        """Crea el menú de fin de juego."""
        menu = pygame_menu.Menu(
            title='¡Juego Terminado!',
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            theme=self.theme,
            onclose=self._callback_wrapper('main_menu')
        )
        
        # Puntuación final
        score_frame = menu.add.frame_h(400, 100, background_color=(100, 0, 0, 150))
        score_frame.pack(menu.add.label(f'Puntuación Final: {final_score}', 
                                       font_size=30, font_color=(255, 255, 0)))
        
        menu.add.button('Nueva Partida', self._callback_wrapper('new_game'))
        menu.add.button('Menú Principal', self._callback_wrapper('main_menu'))
        menu.add.button('Salir', pygame_menu.events.EXIT)
        
        self.logger.log_event(f"Menú de fin de juego creado - Puntuación: {final_score}", "menu")
        return menu
    
    def create_options_menu(self) -> pygame_menu.Menu:
        """Crea el menú de opciones."""
        menu = pygame_menu.Menu(
            title='Opciones',
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            theme=self.theme,
            onclose=self._callback_wrapper('back_to_previous')
        )
        
        # Configuraciones
        menu.add.range_slider('Volumen Música', 50, (0, 100), 1, 
                             onchange=self._callback_wrapper('set_music_volume'))
        menu.add.range_slider('Volumen Efectos', 70, (0, 100), 1, 
                             onchange=self._callback_wrapper('set_sfx_volume'))
        menu.add.toggle_switch('Pantalla Completa', False, 
                              onchange=self._callback_wrapper('toggle_fullscreen'))
        menu.add.toggle_switch('Mostrar FPS', False, 
                              onchange=self._callback_wrapper('toggle_fps_display'))
        
        menu.add.button('Aplicar', self._callback_wrapper('apply_options'))
        menu.add.button('Volver', self._callback_wrapper('back_to_previous'))
        
        self.logger.log_event("Menú de opciones creado", "menu")
        return menu
    
    def create_save_load_menu(self, save_slots: Dict[int, Dict[str, Any]]) -> pygame_menu.Menu:
        """Crea el menú de guardado/carga."""
        menu = pygame_menu.Menu(
            title='Guardar/Cargar Partida',
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            theme=self.theme,
            onclose=self._callback_wrapper('back_to_main')
        )
        
        for slot_num in range(1, 4):
            if save_slots[slot_num]:  # Slot ocupado
                # Mostrar información de la partida guardada
                save_data = save_slots[slot_num]
                player_name = save_data.get('player_name', 'Desconocido')
                level = save_data.get('level', 1)
                score = save_data.get('score', 0)
                
                frame = menu.add.frame_h(600, 80, background_color=(50, 50, 50, 150))
                frame._relax = True  # Permitir widgets más grandes que el frame
                frame.pack(menu.add.label(f'Slot {slot_num}: {player_name} - Nivel {level} - Puntuación {score}', font_size=20))
                frame.pack(menu.add.button('Cargar', 
                                         self._callback_wrapper('load_slot', slot_num)))
                frame.pack(menu.add.button('Sobrescribir', 
                                         self._callback_wrapper('save_slot', slot_num)))
            else:
                # Slot vacío
                frame = menu.add.frame_h(500, 80, background_color=(50, 50, 50, 150))
                frame._relax = True  # Permitir widgets más grandes que el frame
                frame.pack(menu.add.label(f'Slot {slot_num}: Vacío', font_size=20))
                frame.pack(menu.add.button('Guardar', 
                                         self._callback_wrapper('save_slot', slot_num)))
        
        menu.add.button('Volver', self._callback_wrapper('back_to_main'))
        
        self.logger.log_event("Menú de guardado/carga creado", "menu")
        return menu
    
    def _callback_wrapper(self, action: str, *args) -> Callable:
        """Envuelve los callbacks para manejo centralizado."""
        def callback():
            self.logger.log_event(f"Callback ejecutado: {action} {args}", "menu")
            if action in self.callbacks:
                self.callbacks[action](*args)
            else:
                self.logger.log_warning(f"Callback no registrado: {action}", "menu")
        
        return callback
    
    def register_callback(self, action: str, callback: Callable) -> None:
        """Registra un callback para una acción específica."""
        self.callbacks[action] = callback
        self.logger.log_event(f"Callback registrado: {action}", "menu")
    
    def show_menu(self, menu: pygame_menu.Menu) -> None:
        """Muestra un menú específico."""
        self.current_menu = menu
        self.menu_stack.append(menu)
        self.logger.log_event(f"Mostrando menú: {menu.get_title()}", "menu")
    
    def show_main_menu(self) -> None:
        """Muestra el menú principal."""
        menu = self.create_main_menu()
        self.show_menu(menu)
    
    def show_character_selection(self) -> None:
        """Muestra el menú de selección de personajes."""
        menu = self.create_character_selection_menu()
        self.show_menu(menu)
    
    def show_pause_menu(self) -> None:
        """Muestra el menú de pausa."""
        menu = self.create_pause_menu()
        self.show_menu(menu)
    
    def show_upgrade_menu(self, points: int, points_spent: int, 
                         upgrade_levels: Dict[str, int]) -> None:
        """Muestra el menú de mejoras."""
        menu = self.create_upgrade_menu(points, points_spent, upgrade_levels)
        self.show_menu(menu)
    
    def show_game_over(self, final_score: int) -> None:
        """Muestra el menú de fin de juego."""
        menu = self.create_game_over_menu(final_score)
        self.show_menu(menu)
    
    def show_options(self) -> None:
        """Muestra el menú de opciones."""
        menu = self.create_options_menu()
        self.show_menu(menu)
    
    def show_save_load(self, save_slots: Dict[int, Dict[str, Any]]) -> None:
        """Muestra el menú de guardado/carga."""
        menu = self.create_save_load_menu(save_slots)
        self.show_menu(menu)
    
    def run(self) -> Optional[str]:
        """Ejecuta el menú actual y retorna la acción seleccionada."""
        if self.current_menu:
            try:
                action = self.current_menu.mainloop(self.screen)
                self.logger.log_event(f"Menú completado: {action}", "menu")
                return action
            except Exception as e:
                self.logger.log_error(f"Error ejecutando menú: {e}", "menu")
                return None
        return None
    
    def back(self) -> None:
        """Vuelve al menú anterior."""
        if len(self.menu_stack) > 1:
            self.menu_stack.pop()  # Remover menú actual
            self.current_menu = self.menu_stack[-1]  # Menú anterior
            self.logger.log_event("Volviendo al menú anterior", "menu")
    
    def clear_stack(self) -> None:
        """Limpia la pila de menús."""
        self.menu_stack.clear()
        self.current_menu = None
        self.logger.log_event("Pila de menús limpiada", "menu")
    
    def get_current_menu_title(self) -> str:
        """Retorna el título del menú actual."""
        return self.current_menu.get_title() if self.current_menu else "Ninguno" 