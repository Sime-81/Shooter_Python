import pygame


class SoundManager:

    def __init__(self):
        self.sounds = {
            'click': pygame.mixer.Sound("../assets/sounds/click.ogg"),
            'game_over': pygame.mixer.Sound("../assets/sounds/game_over.ogg"),
            'meteorite': pygame.mixer.Sound("../assets/sounds/meteorite.ogg"),
            'tir': pygame.mixer.Sound("../assets/sounds/tir.ogg"),
            'background': pygame.mixer.Sound("../assets/sounds/last_forever_-_loop.ogg"),
            'mummy1': pygame.mixer.Sound("../assets/sounds/mummy_death1.ogg"),
            'mummy2': pygame.mixer.Sound("../assets/sounds/mummy_death2.ogg"),
            'mummy3': pygame.mixer.Sound("../assets/sounds/mummy_death3.ogg"),
            'alien1': pygame.mixer.Sound("../assets/sounds/alien_death1.ogg"),
            'alien2': pygame.mixer.Sound("../assets/sounds/alien_death2.ogg"),
            'alien3': pygame.mixer.Sound("../assets/sounds/alien_death3.ogg"),
        }
        self.sounds['game_over'].set_volume(5)

    def play(self, name, loop=False):
        self.sounds[name].play(loop)

    def play_ambiance(self):
        self.sounds['background'].set_volume(0.2)
        self.sounds['background'].play(999999999)

    def stop(self, name):
        self.sounds[name].stop()

