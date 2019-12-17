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
        self.pos = vec(random.randint(0, WIDTH), HEIGHT / 2)

    def update(self):
        self.pos -= (1, 0)

        self.rect.center = self.pos
