import pygame
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class SoundManager:
    def __init__(self, logger=None):
        pygame.mixer.init()
        self.logger = logger
        self.sounds = {}
        try:
            shoot_sound_path = resource_path("assets/sounds/shoot.wav")
            print(f"Intentando cargar sonido: {shoot_sound_path}")
            self.sounds["shoot"] = pygame.mixer.Sound(shoot_sound_path)
        except pygame.error as e:
            if self.logger:
                self.logger.log_error(f"Error loading shoot.wav: {e}")
        try:
            self.sounds["explosion"] = pygame.mixer.Sound(resource_path("assets/sounds/explosion.wav"))
        except pygame.error as e:
            if self.logger:
                self.logger.log_error(f"Error loading explosion.wav: {e}")
        self.music_playing = False

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def play_music(self, path, loop=-1):
        try:
            pygame.mixer.music.load(resource_path("assets/sounds/background_music.mp3"))
            pygame.mixer.music.play(loop)
            self.music_playing = True
        except pygame.error as e:
            if self.logger:
                self.logger.log_error(f"Error loading music {path}: {e}")

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False