import pygame
import random
import animation


class Monster(animation.AnimateSprite):

    def __init__(self, game, name, size, offset=0):
        super().__init__(name, size)
        self.game = game
        self.healt = 100
        self.max_healt = 100
        self.attack = 0.3
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint(0, 300)
        self.loot_amount = 10
        self.rect.y = 540 - offset
        self.start_animation()

        self.default_speed = None
        self.velocity = None

    def set_speed(self, speed):
        self.default_speed = speed
        self.velocity = random.randint(1, speed)

    def set_loot_amount(self, amount):
        self.loot_amount = amount

    def death_mummy_sound(self):
        luck = random.randint(1, 100)
        if 1 <= luck <= 98:
            self.game.sound_manager.play("mummy1")
        elif luck == 99:
            self.game.sound_manager.play("mummy2")
            print("easter_egg mummy death 2")
        elif luck == 100:
            self.game.sound_manager.play("mummy3")
            print("easter_egg mummy death 3")
        else:
            print("Une erreur c'est produite")

    def death_alien_sound(self):
        luck = random.randint(70, 100)
        if 1 <= luck <= 98:
            self.game.sound_manager.play("alien1")
        elif luck == 99:
            self.game.sound_manager.play("alien2")
            print("easter_egg alien death 2")
        elif luck == 100:
            self.game.sound_manager.play("alien3")
            print("easter_egg alien death 3")
        else:
            print("Une erreur c'est produite")

    def update_animation(self):
        self.animate(True)

    def update_healt_bar(self, surface):
        #gestion de l'affichage des barres de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 10, self.rect.y - 20, self.max_healt, 5])
        pygame.draw.rect(surface, (66, 204, 50), [self.rect.x + 10, self.rect.y - 20, self.healt, 5])

    def forward(self):
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        else:
            self.game.player.damage(self.attack)


class Mummy(Monster):

    def __init__(self, game):
        super().__init__(game, "mummy", (130, 130))
        self.set_speed(3)
        self.set_loot_amount(20)

    def damage(self, amount):
        self.healt -= amount

        if self.healt <= 0:
            # récupération du monstre pour respawn
            self.rect.x = 1000 + random.randint(0, 300)
            self.velocity = random.randint(1, self.default_speed)
            self.healt = self.max_healt
            self.game.add_point(self.loot_amount)
            self.death_mummy_sound()

            if self.game.comet_event.is_full_loaded():
                self.game.all_monster.remove(self)
                self.game.comet_event.attempt_fall()


class Alien(Monster):

    def __init__(self, game):
        super().__init__(game, "alien", (300, 300), 130)
        self.healt = 250
        self.max_healt = 250
        self.attack = 0.8
        self.set_loot_amount(80)
        self.set_speed(1)

    def damage(self, amount):
        self.healt -= amount

        if self.healt <= 0:
            # récupération du monstre pour respawn
            self.rect.x = 1000 + random.randint(0, 300)
            self.velocity = random.randint(1, self.default_speed)
            self.healt = self.max_healt
            self.game.add_point(self.loot_amount)
            self.death_alien_sound()

            if self.game.comet_event.is_full_loaded():
                self.game.all_monster.remove(self)
                self.game.comet_event.attempt_fall()
