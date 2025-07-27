import pygame

class SoundManager:
    def __init__(self, logger=None):
        pygame.mixer.init()
        self.logger = logger
        self.sounds = {}
        try:
            self.sounds["shoot"] = pygame.mixer.Sound("assets/sounds/shoot.wav")
        except pygame.error as e:
            if self.logger:
                self.logger.log_error(f"Error loading shoot.wav: {e}")
        try:
            self.sounds["explosion"] = pygame.mixer.Sound("assets/sounds/explosion.wav")
        except pygame.error as e:
            if self.logger:
                self.logger.log_error(f"Error loading explosion.wav: {e}")
        self.music_playing = False

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def play_music(self, path, loop=-1):
        try:
            pygame.mixer.music.load("assets/sounds/background_music.mp3")
            pygame.mixer.music.play(loop)
            self.music_playing = True
        except pygame.error as e:
            if self.logger:
                self.logger.log_error(f"Error loading music {path}: {e}")

    def stop_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False
