#!/usr/bin/env python3
"""
Gestor de sonido para PyGame Shooter
Autor: Kava
Fecha: 2024-12-19
Descripción: Gestión de efectos de sonido y música de fondo con logging avanzado.
"""
import pygame
import os
from utils.advanced_logger import get_logger

class SoundManager:
    def __init__(self, logger=None):
        self.logger = logger or get_logger("PyGame")
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self._load_sounds()
    
    def _load_sounds(self):
        """Carga todos los sonidos del juego."""
        sound_files = {
            'shoot': 'assets/sounds/shoot.wav',
            'explosion': 'assets/sounds/explosion.wav',
            'background_music': 'assets/sounds/background_music.mp3'
        }
        
        for sound_name, sound_path in sound_files.items():
            try:
                if os.path.exists(sound_path):
                    if sound_name == 'background_music':
                        # La música se carga de forma diferente
                        self.sounds[sound_name] = sound_path
                    else:
                        self.sounds[sound_name] = pygame.mixer.Sound(sound_path)
                    self.logger.log_debug(f"Sonido cargado: {sound_name}", "sound")
                else:
                    self.logger.log_warning(f"Archivo de sonido no encontrado: {sound_path}", "sound")
            except Exception as e:
                self.logger.log_error(f"Error cargando sonido {sound_name}: {e}", "sound")
    
    def play_sound(self, sound_name):
        """Reproduce un efecto de sonido."""
        try:
            if sound_name in self.sounds:
                sound = self.sounds[sound_name]
                if isinstance(sound, pygame.mixer.Sound):
                    sound.set_volume(self.sfx_volume)
                    sound.play()
                    self.logger.log_debug(f"Reproduciendo sonido: {sound_name}", "sound")
                else:
                    self.logger.log_warning(f"'{sound_name}' no es un efecto de sonido válido", "sound")
            else:
                self.logger.log_warning(f"Sonido no encontrado: {sound_name}", "sound")
        except Exception as e:
            self.logger.log_error(f"Error reproduciendo sonido {sound_name}: {e}", "sound")
    
    def play_music(self, music_name, loop=True):
        """Reproduce música de fondo."""
        try:
            if music_name in self.sounds:
                music_path = self.sounds[music_name]
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1 if loop else 0)
                self.logger.log_event(f"Reproduciendo música: {music_name}", "sound")
            else:
                self.logger.log_warning(f"Música no encontrada: {music_name}", "sound")
        except Exception as e:
            self.logger.log_error(f"Error reproduciendo música {music_name}: {e}", "sound")
    
    def stop_music(self):
        """Detiene la música de fondo."""
        try:
            pygame.mixer.music.stop()
            self.logger.log_event("Música detenida", "sound")
        except Exception as e:
            self.logger.log_error(f"Error deteniendo música: {e}", "sound")
    
    def set_music_volume(self, volume):
        """Establece el volumen de la música (0.0 a 1.0)."""
        try:
            self.music_volume = max(0.0, min(1.0, volume))
            pygame.mixer.music.set_volume(self.music_volume)
            self.logger.log_event(f"Volumen de música establecido: {self.music_volume}", "sound")
        except Exception as e:
            self.logger.log_error(f"Error estableciendo volumen de música: {e}", "sound")
    
    def set_sfx_volume(self, volume):
        """Establece el volumen de los efectos de sonido (0.0 a 1.0)."""
        try:
            self.sfx_volume = max(0.0, min(1.0, volume))
            self.logger.log_event(f"Volumen de efectos establecido: {self.sfx_volume}", "sound")
        except Exception as e:
            self.logger.log_error(f"Error estableciendo volumen de efectos: {e}", "sound")
    
    def pause_music(self):
        """Pausa la música de fondo."""
        try:
            pygame.mixer.music.pause()
            self.logger.log_event("Música pausada", "sound")
        except Exception as e:
            self.logger.log_error(f"Error pausando música: {e}", "sound")
    
    def unpause_music(self):
        """Reanuda la música de fondo."""
        try:
            pygame.mixer.music.unpause()
            self.logger.log_event("Música reanudada", "sound")
        except Exception as e:
            self.logger.log_error(f"Error reanudando música: {e}", "sound")