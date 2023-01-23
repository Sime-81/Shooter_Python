import pygame
from Comet import Comet


class CometFallEvent:

    def __init__(self, game):
        self.percent = 0
        self.percent_speed = 5
        self.game = game
        self.fall_mode = False

        # création d'un groupe de comets
        self.all_comets = pygame.sprite.Group()

    def add_percent(self):
        self.percent += self.percent_speed / 100

    def is_full_loaded(self):
        return self.percent >= 100

    def reset_percent(self):
        self.percent = 0

    def meteor_fall(self):
        for i in range(0, 15):
            self.all_comets.add(Comet(self))

    def attempt_fall(self):
        if self.is_full_loaded() and len(self.game.all_monster) == 0:
            print("Pluie de Comet")
            self.meteor_fall()
            self.fall_mode = True

    def update_bar(self, surface):
        # ajout de pourcentage
        self.add_percent()

        # Font de la barre
        pygame.draw.rect(surface, (0, 0, 0), [0, surface.get_height() - 10, surface.get_width(), 10])
        # Barre de progression
        pygame.draw.rect(surface, (255, 35, 0), [0, surface.get_height() - 10, (surface.get_width() / 100) * self.percent, 10])
