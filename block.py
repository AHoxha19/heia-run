# Sprite classes for platform game
import pygame as pg
from settings import *
from random import randint
from game_manager import *
vec = pg.math.Vector2


class Block(pg.sprite.Sprite):
    def __init__(self, game, x_pos, image_name, is_hole):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image_name = image_name
        if(not is_hole and not image_name == 'none'):
            self.image = pg.image.load(IMG_BLOCK_PATH + image_name).convert()
            self.image = pg.transform.scale(self.image, (BLOCK_WIDTH, BLOCK_HEIGHT))
            self.rect = self.image.get_rect()
            self.pos_in_game = vec(x_pos, DISPLAY_HEIGHT)
            self.pos = vec(-500, DISPLAY_HEIGHT)
        elif GameManager.world_number == BOSS_WORLD_NUMBER or GameManager.world_number == WORLD_WITH_TRANSPARENT_BLOCKS:
            self.image = pg.Surface((BLOCK_WIDTH, BLOCK_HEIGHT), pg.SRCALPHA)
            self.image = self.image.convert_alpha()
            self.rect = self.image.get_rect()
            self.pos = vec(x_pos, DISPLAY_HEIGHT)
            if GameManager.world_number == WORLD_WITH_TRANSPARENT_BLOCKS:
                self.pos_in_game = vec(x_pos, DISPLAY_HEIGHT)
                self.pos = vec(-500, DISPLAY_HEIGHT)
        else:
            self.image = pg.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
            self.rect = self.image.get_rect()
        self.is_hole = is_hole

    def update(self):
        if not self.is_hole and not GameManager.world_number == BOSS_WORLD_NUMBER:
            self.pos.x = self.pos_in_game.x - self.game.player.pos.x
            self.rect.bottomleft = self.pos
        if not self.is_hole:
            self.rect.bottomleft = self.pos

    @staticmethod
    def create_all_blocks(game, image_name):
        is_hole = False
        pos_in_game_x = 0
        blocks = list()

        while pos_in_game_x < STAGE_WIDTH + DISPLAY_WIDTH:
            if image_name == 'hole':
                continue
            if GameManager.world_number == BOSS_WORLD_NUMBER or GameManager.world_number == WORLD_WITH_TRANSPARENT_BLOCKS:
                blocks.append(Block(game, pos_in_game_x, image_name, is_hole))
            else:
                is_hole = randint(0, 100) <= HOLES_PROB
                if (pos_in_game_x < DISPLAY_WIDTH or pos_in_game_x > (STAGE_WIDTH - DISPLAY_WIDTH) or
                   (len(blocks) > 2 and blocks[-1].is_hole and blocks[-2].is_hole)):
                    is_hole = False

                blocks.append(Block(game, pos_in_game_x, image_name, is_hole))
            pos_in_game_x += BLOCK_WIDTH
        return blocks
