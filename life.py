import pygame as pg
from settings import *
vec = pg.math.Vector2

class Life(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(IMG_PLAYER_PATH + 'life.png'), (LIFE_WIDTH, LIFE_HEIGHT))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect = self.pos


