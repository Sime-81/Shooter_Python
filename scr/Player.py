import pygame
import animation
from Projectile import Projectile


class Player(animation.AnimateSprite):

    def __init__(self, game):
        super().__init__("player")
        self.game = game
        self.healt = 100
        self.max_healt = 100
        self.attack = 10
        self.velocity = 4
        self.healt_kill = 1
        self.all_projectiles = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 500

    def damage(self, amount):
        if self.healt - amount > self.healt_kill:
            self.healt -= amount
        else:
            self.rect.x = 400
            self.game.game_over()

    def update_animation(self):
        self.animate()

    def update_healt_bar(self, surface):
        #gestion de l'affichage des barres de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 50, self.rect.y + 20, self.max_healt, 7])
        pygame.draw.rect(surface, (66, 204, 50), [self.rect.x + 50, self.rect.y + 20, self.healt, 7])

    def launch_projectile(self):
        self.all_projectiles.add(Projectile(self))
        self.start_animation()

        self.game.sound_manager.play('tir')

    def move_right(self):
        if not self.game.check_collision(self, self.game.all_monster):
            self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity
