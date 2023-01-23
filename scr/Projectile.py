import pygame


class Projectile(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.velocity = 7
        self.player = player
        self.image = pygame.image.load('../assets/projectile.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 80
        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        self.angle += 12
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)

        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move_projectile(self):
        self.rect.x += self.velocity
        self.rotate()

        # vérification collision avec monstres
        for monster in self.player.game.check_collision(self, self.player.game.all_monster):
            self.remove()
            monster.damage(self.player.attack)

        #supression des projectiles hors d'écran
        if self.rect.x > 1080:
            self.remove()
