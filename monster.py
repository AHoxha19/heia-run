# Sprite classes for platform game
import pygame as pg
import random
from settings import *
vec = pg.math.Vector2


class Monster(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(-200, HEIGHT / 2)
        self.pos_in_game = vec(random.randint(0, BACKGROUND_WIDTH), HEIGHT / 2)

    def update(self):
        self.pos_in_game -= (1, 0)
        self.pos.x = self.pos_in_game.x - self.game.x_progression
        self.rect.center = self.pos
