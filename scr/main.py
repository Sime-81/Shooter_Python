import pygame

from Game import Game

if __name__ == '__main__':
    print("Game Start")

    pygame.init()
    game = Game()
    game.run()
