# Sprite classes for platform game
import pygame as pg
from settings import *
from random import randint
vec = pg.math.Vector2


class Block(pg.sprite.Sprite):
    def __init__(self, game, x_pos, image_name, isHole):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        if(not isHole):
            self.image = pg.image.load(IMG_BLOCK_PATH + image_name).convert()
            self.image = pg.transform.scale(self.image, (BLOCK_WIDTH, BLOCK_HEIGHT))
            self.rect = self.image.get_rect()
            self.pos_in_game = vec(x_pos, HEIGHT)
            self.pos = vec(-500, HEIGHT)
        self.isHole = isHole

    def update(self):
        if not self.isHole:
            self.pos.x = self.pos_in_game.x - self.game.x_progression
            self.rect.bottomleft = self.pos

    @staticmethod
    def create_all_blocks(game, image_name):
        isHole = False
        game_progress = 0
        blocks = list()

        while game_progress < game.get_current_bg().game_width:
            game_progress += BLOCK_WIDTH
            if image_name == 'hole':
                continue
            isHole = randint(0, 100) <= HOLES_PROB
            blocks.append(Block(game, game_progress, image_name, isHole))
            

        return blocks
