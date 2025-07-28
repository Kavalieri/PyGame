#!/usr/bin/env python3
"""
Bucle de juego principal mejorado para PyGame Shooter
Autor: Kava
Fecha: 2024-12-19
Descripción: Bucle de juego optimizado con integración de menús, HUD, físicas y logging avanzado.
"""

import pygame
import time
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from typing import Optional, Dict, Any, Callable
from managers.sound_manager import SoundManager
from managers.save_manager import SaveManager
from managers.enemy_generator import EnemyGenerator
from entities.player import Player
from entities.enemies import Enemy
from entities.projectile import Projectile
from entities.powerups import PowerUp
from ui.menu_system import MenuSystem
from ui.hud import HUD
from utils.text_renderer import TextRenderer
from utils.sprite_sheet import AnimationManager
from utils.advanced_logger import setup_logging, get_logger
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
import pygame_menu


class GameLoop:
    """
    Bucle de juego mejorado con pygame-ce.
    Optimizado para rendimiento y mantenibilidad.
    """
    
    def __init__(self, screen: pygame.Surface, logger=None):
        """
        Inicializa el bucle de juego mejorado.
        
        Args:
            screen: Superficie de pygame donde renderizar
            logger: Instancia del logger para debug (opcional, usa AdvancedLogger por defecto)
        """
        self.screen = screen
        self.logger = logger or get_logger("PyGame")
        self.clock = pygame.time.Clock()
        
        # Estado del juego
        self.running = False
        self.paused = False
        self.game_state = "menu"  # menu, playing, paused, game_over
        
        # Managers
        self.sound_manager = SoundManager(self.logger)
        self.save_manager = SaveManager(self.logger)
        self.enemy_generator = EnemyGenerator(self.logger)
        self.menu_system = MenuSystem(screen, self.logger)
        self.text_renderer = TextRenderer(self.logger)
        self.animation_manager = AnimationManager(self.logger)
        
        # Entidades del juego
        self.player: Optional[Player] = None
        self.enemies: list[Enemy] = []
        self.projectiles: list[Projectile] = []
        self.powerups: list[PowerUp] = []
        
        # HUD
        self.hud = HUD(screen)
        self.active_powerups = {}  # Diccionario para tiempos de powerups activos
        
        # Estadísticas del juego
        self.score = 0
        self.level = 1
        self.level_time = 0
        self.level_duration = 30  # segundos por nivel
        
        # Mejoras del jugador
        self.upgrade_points = 0
        self.points_spent = 0
        self.upgrade_levels = {
            'speed': 0,
            'lives': 0,
            'fire_rate': 0,
            'projectiles': 0,
            'burst_attack': 0,
            'piercing_attack': 0
        }
        
        # Callbacks del menú
        self._setup_menu_callbacks()
        
        # Estadísticas de rendimiento
        self.fps_counter = 0
        self.frame_times = []
        self.last_fps_update = time.time()
        
        self.logger.log_event("GameLoop mejorado inicializado", "game_loop")
        self.logger.log_system_info()
    
    def _setup_menu_callbacks(self) -> None:
        """Configura los callbacks del sistema de menús."""
        callbacks = {
            'new_game': self._start_new_game,
            'load_game': self._load_game,
            'save_game': self._save_game,
            'options': self._show_options,
            'credits': self._show_credits,
            'select_character': self._select_character,
            'resume_game': self._resume_game,
            'main_menu': self._return_to_main_menu,
            'upgrade': self._apply_upgrade,
            'reset_upgrades': self._reset_upgrades,
            'continue_game': self._continue_game,
            'back_to_main': self._return_to_main_menu,
            'back_to_previous': self._back_to_previous_menu,
            'set_music_volume': self._set_music_volume,
            'set_sfx_volume': self._set_sfx_volume,
            'toggle_fullscreen': self._toggle_fullscreen,
            'toggle_fps_display': self._toggle_fps_display,
            'apply_options': self._apply_options,
            'load_slot': self._load_slot,
            'save_slot': self._save_slot
        }
        
        for action, callback in callbacks.items():
            self.menu_system.register_callback(action, callback)
            self.logger.log_debug(f"Callback registrado: {action}", "menu")
        
        self.logger.log_event(f"Total de callbacks registrados: {len(callbacks)}", "menu")
    
    def run(self) -> None:
        """Ejecuta el bucle principal del juego (menús no bloqueantes)."""
        self.running = True
        self.logger.log_event("Iniciando bucle principal del juego", "game_loop")
        
        # Mostrar menú principal
        self.menu_system.show_main_menu()
        self.game_state = "menu"
        # Guardar instancia global para callbacks
        GameLoop.instance = self
        
        while self.running:
            print(f"[DEBUG] game_state={self.game_state}, current_menu={self.menu_system.current_menu}")
            if self.game_state == "menu" and self.menu_system.current_menu:
                self._handle_menu_events_non_blocking()
            else:
                self._handle_events()
                self._update()
                self._render()
                self._update_fps()
            self.clock.tick(FPS)
        self.logger.log_event("Bucle principal terminado", "game_loop")

    def _handle_menu_events_non_blocking(self) -> None:
        """Procesa eventos y dibuja el menú de forma no bloqueante."""
        if not self.menu_system.current_menu:
            return  # No hay menú activo, salir y permitir avanzar el flujo
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                self.logger.log_event("Evento QUIT recibido (menú)", "game_loop")
                return
        self.menu_system.current_menu.update(events)
        # Comprobar si el menú sigue activo tras el update (puede haber sido cerrado por un callback)
        if not self.menu_system.current_menu:
            return
        self.menu_system.current_menu.draw(self.screen)
        pygame.display.flip()
    
    def _handle_events(self) -> None:
        """Maneja los eventos del juego."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.logger.log_event("Evento QUIT recibido", "game_loop")
            
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)
    
    def _handle_keydown(self, event: pygame.event.Event) -> None:
        """Maneja eventos de teclas presionadas."""
        if event.key == pygame.K_ESCAPE:
            if self.game_state == "playing":
                self._pause_game()
            elif self.game_state == "paused":
                self._resume_game()
        
        elif event.key == pygame.K_p:
            if self.game_state == "playing":
                self._pause_game()
            elif self.game_state == "paused":
                self._resume_game()
        
        elif event.key == pygame.K_F1:
            self._toggle_debug_mode()
    
    def _handle_mouse_click(self, event: pygame.event.Event) -> None:
        """Maneja eventos de clics del ratón."""
        if self.game_state == "playing" and self.player:
            # Disparo del jugador
            mouse_x, mouse_y = event.pos if hasattr(event, 'pos') else pygame.mouse.get_pos()
            self._player_shoot(mouse_x, mouse_y)
    
    def _update(self) -> None:
        """Actualiza la lógica del juego."""
        if self.game_state == "playing":
            self._update_game()
    
    def _update_game(self) -> None:
        """Actualiza la lógica del juego durante la partida."""
        current_time = time.time()
        
        # Actualizar jugador
        if self.player:
            self.player.update()
            # El movimiento ya se gestiona en Player.update()
        
        # Actualizar enemigos
        for enemy in self.enemies[:]:
            enemy.update()
            
            # Verificar si el enemigo salió de la pantalla
            if enemy.y > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.logger.log_event("Enemigo eliminado por salir de pantalla", "game_loop")
        
        # Actualizar proyectiles
        for projectile in self.projectiles[:]:
            projectile.update()
            
            # Añadir contador de colisiones para proyectiles perforantes
            if not hasattr(projectile, 'piercing_hits'):
                projectile.piercing_hits = 0
            
            # Verificar colisiones con enemigos
            for enemy in self.enemies[:]:
                if projectile.get_collision_rect().colliderect(enemy.collision_box):
                    self.logger.log_debug(f"Proyectil colisiona con enemigo en ({enemy.x},{enemy.y}) - Daño: {projectile.damage}", "game_loop")
                    enemy.take_damage(projectile.damage)
                    if projectile.piercing:
                        projectile.piercing_hits += 1
                        if projectile.piercing_hits >= 2:  # Por ejemplo, atraviesa 2 enemigos máximo
                            self.logger.log_debug("Proyectil perforante eliminado tras atravesar 2 enemigos.", "game_loop")
                            self.projectiles.remove(projectile)
                            break
                    else:
                        self.logger.log_debug("Proyectil eliminado tras colisión.", "game_loop")
                        self.projectiles.remove(projectile)
                        break
                    
                    if enemy.health <= 0:
                        self.logger.log_event(f"Enemigo eliminado - Puntuación: {self.score}", "game_loop")
                        self.enemies.remove(enemy)
                        self.score += enemy.points
            
            # Verificar si el proyectil salió de la pantalla
            if (projectile.y < 0 or projectile.y > SCREEN_HEIGHT or 
                projectile.x < 0 or projectile.x > SCREEN_WIDTH):
                if projectile in self.projectiles:
                    self.logger.log_debug("Proyectil eliminado por salir de pantalla.", "game_loop")
                    self.projectiles.remove(projectile)
        
        # Actualizar powerups
        for powerup in self.powerups[:]:
            powerup.update()
            
            # Verificar colisiones con power-ups
            for powerup in self.powerups[:]:
                if self.player and powerup.get_collision_rect().colliderect(self.player.collision_box):
                    self.player.activate_powerup(powerup.type)
                    self.powerups.remove(powerup)
                    self.logger.log_event(f"PowerUp recogido: {powerup.type}", "game_loop")
            
            # Verificar si el powerup salió de la pantalla
            if powerup.y > SCREEN_HEIGHT:
                self.powerups.remove(powerup)
        
        # Verificar colisiones jugador-enemigos
        if self.player:
            for enemy in self.enemies[:]:
                if self.player.collision_box.colliderect(enemy.collision_box):
                    self.player.take_damage(enemy.damage)
                    self.enemies.remove(enemy)
                    self.logger.log_event("Jugador dañado por enemigo", "game_loop")
                    
                    if self.player.lives <= 0:
                        self._game_over()
                        return
        
        # Actualizar tiempo del nivel
        self.level_time = current_time - self.level_start_time
        
        # Verificar fin de nivel
        if self.level_time >= self.level_duration:
            self._end_level()
        
        # Generar enemigos
        nuevos_enemigos = self.enemy_generator.generate_enemies(self.score)
        if nuevos_enemigos:
            self.enemies.extend(nuevos_enemigos)
        
        # Generar powerups aleatorios
        if current_time - self.last_powerup_time > 10:  # Cada 10 segundos
            self._spawn_random_powerup()
            self.last_powerup_time = current_time
    
    def _render(self) -> None:
        """Renderiza el juego."""
        if self.game_state == "playing":
            self._render_game()
        elif self.game_state == "menu":
            self._render_menu()
        elif self.game_state == "paused":
            self._render_paused_game()
    
    def _render_game(self) -> None:
        """Renderiza el juego durante la partida."""
        self.screen.fill((0, 0, 0))
        if hasattr(self, 'debug_mode') and self.debug_mode:
            print(f"[DEBUG] Renderizando juego. Jugador: {self.player}, Enemigos: {len(self.enemies)}, Proyectiles: {len(self.projectiles)}")
        # Renderizar entidades
        if self.player:
            self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)
        # Renderizar HUD
        lives = self.player.lives if self.player else 0
        shield_lives = self.player.shield_lives if self.player and hasattr(self.player, 'shield_lives') else 0
        score = self.score
        current_level = self.level
        time_remaining = max(0, self.level_duration - self.level_time)
        active_powerups = self.active_powerups
        self.hud.draw(lives, shield_lives, score, current_level, time_remaining, active_powerups)
        # Renderizar información de debug visual
        if hasattr(self, 'debug_mode') and self.debug_mode:
            font = pygame.font.SysFont('Arial', 18)
            debug_text = f"DEBUG: Jugador={self.player}, Enemigos={len(self.enemies)}, Proyectiles={len(self.projectiles)}, Powerups={len(self.powerups)}"
            text_surface = font.render(debug_text, True, (255,255,0))
            self.screen.blit(text_surface, (10, 10))
        pygame.display.flip()
    
    def _render_menu(self) -> None:
        """Renderiza el menú."""
        # Los menús de pygame-menu se renderizan automáticamente
        # Solo limpiar pantalla y actualizar
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
    
    def _render_paused_game(self) -> None:
        """Renderiza el juego pausado."""
        # Renderizar el juego en segundo plano
        self._render_game()
        
        # Renderizar overlay de pausa
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Renderizar texto de pausa
        self.text_renderer.render_centered_text(
            "JUEGO PAUSADO",
            SCREEN_HEIGHT // 2 - 50,
            size=48,
            color=(255, 255, 255),
            screen_width=SCREEN_WIDTH
        )
        
        self.text_renderer.render_centered_text(
            "Presiona P o ESC para continuar",
            SCREEN_HEIGHT // 2 + 50,
            size=24,
            color=(200, 200, 200),
            screen_width=SCREEN_WIDTH
        )
        
        pygame.display.flip()
    
    def _render_debug_info(self) -> None:
        """Renderiza información de debug."""
        debug_info = {
            'FPS': self.fps_counter,
            'Enemigos': len(self.enemies),
            'Proyectiles': len(self.projectiles),
            'Powerups': len(self.powerups),
            'Nivel': self.level,
            'Puntuación': self.score,
            'Tiempo Nivel': f"{self.level_time:.1f}s"
        }
        
        self.text_renderer.render_debug_info(debug_info, (10, 10))
    
    def _update_fps(self) -> None:
        """Actualiza el contador de FPS."""
        current_time = time.time()
        self.frame_times.append(current_time)
        
        # Mantener solo los últimos 60 frames
        if len(self.frame_times) > 60:
            self.frame_times.pop(0)
        
        # Actualizar FPS cada segundo
        if current_time - self.last_fps_update >= 1.0:
            self.fps_counter = len(self.frame_times)
            self.last_fps_update = current_time
    
    def _start_new_game(self) -> None:
        """Inicia una nueva partida (solo muestra el menú de selección de personajes)."""
        self.logger.log_event("Iniciando nueva partida", "game_loop")
        self.menu_system.show_character_selection()
        # No cambiar el estado ni limpiar entidades aquí
    
    def _select_character(self, character_name: str) -> None:
        """Selecciona un personaje y inicia el juego."""
        self.logger.log_event(f"Personaje seleccionado: {character_name}", "game_loop")
        if hasattr(self, 'debug_mode') and self.debug_mode:
            print(f"[DEBUG] Seleccionando personaje: {character_name}")
        # Crear jugador según el personaje seleccionado
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, self.logger, self.sound_manager, character_name)
        if hasattr(self, 'debug_mode') and self.debug_mode:
            print(f"[DEBUG] Jugador creado: {self.player}")
        # Inicializar juego
        self.score = 0
        self.level = 1
        self.level_start_time = time.time()
        self.last_powerup_time = time.time()
        # Limpiar entidades
        self.enemies.clear()
        self.projectiles.clear()
        self.powerups.clear()
        # Cambiar estado
        self.game_state = "playing"
        self.menu_system.clear_stack()
        self.logger.log_event("Juego iniciado", "game_loop")
        if hasattr(self, 'debug_mode') and self.debug_mode:
            print(f"[DEBUG] Estado cambiado a 'playing'. Jugador y entidades inicializadas.")

    def _pause_game(self) -> None:
        """Pausa el juego."""
        if self.game_state == "playing":
            self.game_state = "paused"
            self.menu_system.show_pause_menu()
            self.logger.log_event("Juego pausado", "game_loop")
    
    def _resume_game(self) -> None:
        """Reanuda el juego."""
        if self.game_state == "paused":
            self.game_state = "playing"
            self.menu_system.clear_stack()
            self.logger.log_event("Juego reanudado", "game_loop")
    
    def _end_level(self) -> None:
        """Termina el nivel actual."""
        self.logger.log_event(f"Nivel {self.level} completado", "game_loop")
        
        # Mostrar menú de mejoras
        self.menu_system.show_upgrade_menu(
            self.upgrade_points, 
            self.points_spent, 
            self.upgrade_levels
        )
    
    def _continue_game(self) -> None:
        """Continúa al siguiente nivel."""
        self.level += 1
        self.level_start_time = time.time()
        self.level_duration = min(30 + (self.level * 5), 60)  # Máximo 60 segundos
        
        # Limpiar entidades
        self.enemies.clear()
        self.projectiles.clear()
        self.powerups.clear()
        
        # Cambiar estado
        self.game_state = "playing"
        self.menu_system.clear_stack()
        
        self.logger.log_event(f"Nivel {self.level} iniciado", "game_loop")
    
    def _game_over(self) -> None:
        """Termina el juego."""
        self.logger.log_event(f"Juego terminado - Puntuación final: {self.score}", "game_loop")
        self.game_state = "game_over"
        self.menu_system.show_game_over(self.score)
    
    def _player_shoot(self, target_x=None, target_y=None) -> None:
        """Hace que el jugador dispare."""
        if self.player and not self.paused:
            if target_x is None or target_y is None:
                target_x, target_y = pygame.mouse.get_pos()
            projectiles = self.player.shoot(target_x, target_y)
            self.projectiles.extend(projectiles)
            self.sound_manager.play_sound("shoot")
    
    def _spawn_random_powerup(self) -> None:
        """Genera un powerup aleatorio."""
        import random
        
        powerup_types = ["health", "shield", "speed", "fire_rate"]
        powerup_type = random.choice(powerup_types)
        
        x = random.randint(50, SCREEN_WIDTH - 50)
        powerup = PowerUp(x, -50, powerup_type, self.logger)
        self.powerups.append(powerup)
        
        self.logger.log_event(f"Powerup generado: {powerup_type}", "game_loop")
    
    def _apply_upgrade(self, upgrade_type: str) -> None:
        """Aplica una mejora al jugador."""
        if self.upgrade_points > 0:
            self.upgrade_points -= 1
            self.points_spent += 1
            self.upgrade_levels[upgrade_type] += 1
            
            # Aplicar mejora al jugador
            if self.player:
                self.player.apply_upgrade(upgrade_type)
            
            self.logger.log_event(f"Mejora aplicada: {upgrade_type}", "game_loop")
    
    def _reset_upgrades(self) -> None:
        """Resetea todas las mejoras."""
        self.upgrade_points += self.points_spent
        self.points_spent = 0
        self.upgrade_levels = {key: 0 for key in self.upgrade_levels}
        
        if self.player:
            self.player.reset_upgrades()
        
        self.logger.log_event("Mejoras reseteadas", "game_loop")
    
    def _load_game(self) -> None:
        """Carga una partida guardada."""
        save_slots = self.save_manager.get_save_slots()
        self.menu_system.show_save_load(save_slots)
    
    def _save_game(self) -> None:
        """Guarda la partida actual."""
        if self.player:
            save_data = {
                'player_name': self.player.character_type,
                'level': self.level,
                'score': self.score,
                'upgrade_levels': self.upgrade_levels,
                'upgrade_points': self.upgrade_points,
                'points_spent': self.points_spent
            }
            # Usar slot 1 por defecto
            self.save_manager.save_game(1, save_data)
            self.logger.log_event("Partida guardada", "game_loop")
    
    def _show_options(self) -> None:
        """Muestra el menú de opciones (solo una vez, permite volver atrás)."""
        # Solo mostrar el menú de opciones, no reabrirlo en cada callback
        if self.game_state != "options":
            self.game_state = "options"
            self.menu_system.show_options()
    
    def _show_credits(self) -> None:
        """Muestra los créditos."""
        # Implementar pantalla de créditos
        self.logger.log_event("Mostrando créditos", "game_loop")
    
    def _return_to_main_menu(self) -> None:
        """Vuelve al menú principal."""
        self.game_state = "menu"
        self.menu_system.show_main_menu()
        self.logger.log_event("Volviendo al menú principal", "game_loop")
    
    def _back_to_previous_menu(self) -> None:
        """Vuelve al menú anterior."""
        self.menu_system.back()
    
    def _set_music_volume(self, volume: float) -> None:
        """Establece el volumen de la música."""
        self.sound_manager.set_music_volume(volume / 100.0)
    
    def _set_sfx_volume(self, volume: float) -> None:
        """Establece el volumen de los efectos de sonido."""
        self.sound_manager.set_sfx_volume(volume / 100.0)
    
    def _toggle_fullscreen(self, enabled: bool) -> None:
        """Alterna la pantalla completa."""
        # Implementar cambio de pantalla completa
        self.logger.log_event(f"Pantalla completa: {enabled}", "game_loop")
    
    def _toggle_fps_display(self, enabled: bool) -> None:
        """Alterna la visualización de FPS."""
        self.debug_mode = enabled
        self.logger.log_event(f"Debug mode: {enabled}", "game_loop")
    
    def _apply_options(self) -> None:
        """Aplica las opciones configuradas."""
        self.logger.log_event("Opciones aplicadas", "game_loop")
    
    def _load_slot(self, slot_num: int) -> None:
        """Carga una partida desde un slot específico."""
        save_data = self.save_manager.load_game(slot_num)
        if save_data:
            # Restaurar estado del juego
            self.level = save_data.get('level', 1)
            self.score = save_data.get('score', 0)
            self.upgrade_levels = save_data.get('upgrade_levels', {})
            self.upgrade_points = save_data.get('upgrade_points', 0)
            self.points_spent = save_data.get('points_spent', 0)
            
            # Crear jugador
            player_name = save_data.get('player_name', 'Kava')
            self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, self.logger, self.sound_manager, player_name)
            # Aplicar mejoras guardadas
            if hasattr(self.player, 'apply_saved_upgrades'):
                self.player.apply_saved_upgrades(self.upgrade_levels)
            
            # Iniciar juego
            self.game_state = "playing"
            self.level_start_time = time.time()
            self.last_powerup_time = time.time()
            
            self.logger.log_event(f"Partida cargada desde slot {slot_num}", "game_loop")
        else:
            self.logger.log_warning(f"No se pudo cargar el slot {slot_num}", "game_loop")
    
    def _save_slot(self, slot_num: int) -> None:
        """Guarda la partida en un slot específico."""
        if self.player:
            save_data = {
                'player_name': self.player.character_type,
                'level': self.level,
                'score': self.score,
                'upgrade_levels': self.upgrade_levels,
                'upgrade_points': self.upgrade_points,
                'points_spent': self.points_spent
            }
            self.save_manager.save_game(slot_num, save_data)
            self.logger.log_event(f"Partida guardada en slot {slot_num}", "game_loop")
    
    def _toggle_debug_mode(self) -> None:
        """Alterna el modo debug."""
        if not hasattr(self, 'debug_mode'):
            self.debug_mode = False
        
        self.debug_mode = not self.debug_mode
        self.logger.log_event(f"Modo debug: {self.debug_mode}", "game_loop")
    
    def cleanup(self) -> None:
        """Limpia los recursos del juego."""
        self.logger.log_event("Limpiando recursos del juego", "game_loop")
        # Limpiar managers
        self.text_renderer.clear_cache()
        # Limpiar entidades
        self.enemies.clear()
        self.projectiles.clear()
        self.powerups.clear()
        self.logger.log_event("Recursos limpiados", "game_loop") 