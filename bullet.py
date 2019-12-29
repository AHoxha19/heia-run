import pygame as pg
from settings import *

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, player, is_boss_bullet=False):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.player = player
        self.is_boss_bullet = is_boss_bullet
       