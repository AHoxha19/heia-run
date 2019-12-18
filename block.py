# Sprite classes for platform game
import pygame as pg
from settings import *
vec = pg.math.Vector2


class Block(pg.sprite.Sprite):
    def __init__(self, image_name, isHole):
        pg.sprite.Sprite.__init__(self)
        if(not isHole):
            self.image = pg.image.load(IMG_BLOCK_PATH + image_name).convert()
            self.image = pg.transform.scale(self.image, (79, 79))
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (0, HEIGHT)
        self.isHole = isHole
    

