import time

import pygame
from Player import Player
from Monster import Mummy, Alien
from comet_event import CometFallEvent
from sounds import SoundManager


class Game:

    def __init__(self):
        # creation de la fenetre
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("Shooter")

        # état du jeu
        self.is_playing = False

        # mise en place du fond
        self.background = pygame.image.load('../assets/bg.jpg')

        #mise en place de la bannière
        self.banner = pygame.image.load('../assets/banner.png')
        self.banner = pygame.transform.scale(self.banner, (500, 500))
        self.banner_rect = self.banner.get_rect()
        self.banner_rect.x = round(self.screen.get_width() / 4)

        #mise en place du boutton
        self.play_button = pygame.image.load('../assets/button.png')
        self.play_button = pygame.transform.scale(self.play_button, (400, 150))
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.x = self.screen.get_width() / 3.33
        self.play_button_rect.y = self.screen.get_height() / 2

        #mise en place du joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)

        # gestion des monstres
        self.all_monster = pygame.sprite.Group()

        # Comet Event
        self.comet_event = CometFallEvent(self)

        # intégration d'un score
        self.score = 0
        self.font = pygame.font.Font('../assets/Font.ttf', 25)

        # intégration du son
        self.sound_manager = SoundManager()
        self.ambiance = False

    def start(self):
        self.is_playing = True
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)

    def game_over(self):
        self.all_monster = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.player.healt = self.player.max_healt
        self.comet_event.reset_percent()
        self.is_playing = False
        self.score = 0
        self.sound_manager.play('game_over')
        self.sound_manager.stop('background')
        self.ambiance_sound()
        self.ambiance = False

    def ambiance_sound(self):
        self.sound_manager.play_ambiance()

    def update(self):
        # affichage du score
        score_text = self.font.render(f"Score : {self.score}", 1, (0, 0, 0))
        self.screen.blit(score_text, (20, 20))

        # intégration des touche
        self.handel_input()

        # integration du joueur
        self.screen.blit(self.player.image, self.player.rect)

        # actualisation de la barre de vie du joueur
        self.player.update_healt_bar(self.screen)

        #actualisation de l'animation du joueur
        self.player.update_animation()

        # actualisation de la barre d'evenement
        self.comet_event.update_bar(self.screen)

        # déplacement et recuperation des projectile
        for projectile in self.player.all_projectiles:
            projectile.move_projectile()

        # déplacement et recuperation des monstres
        for monster in self.all_monster:
            monster.forward()
            monster.update_healt_bar(self.screen)
            monster.update_animation()

        # déplacement des comets
        for comet in self.comet_event.all_comets:
            comet.fall()

        # integration des projectiles
        self.player.all_projectiles.draw(self.screen)

        # integration des monstres
        self.all_monster.draw(self.screen)

        # intégration des comets
        self.comet_event.all_comets.draw(self.screen)

    def spawn_monster(self, monster_class_name):
        self.all_monster.add(monster_class_name.__call__(self))

    def add_point(self, points=10):
        self.score += points

    @staticmethod
    def check_collision(sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def handel_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT] and self.player.rect.x > 0:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT] and self.player.rect.x + self.player.rect.width < self.screen.get_width():
            self.player.move_right()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:

            # integration du background
            self.screen.blit(self.background, (0, -200))

            #vérification du commencement du jeu
            if self.is_playing:
                self.update()
            else:
                self.screen.blit(self.play_button, self.play_button_rect)
                self.screen.blit(self.banner, self.banner_rect)
                if not self.ambiance:
                    self.ambiance_sound()
                    self.ambiance = True
                else:
                    pass

            # mise a jour de l'ecran
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.sound_manager.play('click')
                    time.sleep(0.09)
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.is_playing:
                            self.player.launch_projectile()
                        else:
                            self.start()
                            self.sound_manager.play('click')

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button_rect.collidepoint(event.pos):
                        self.start()
                        self.sound_manager.play('click')

            clock.tick(90)

        pygame.quit()
