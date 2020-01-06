from settings import *
import pygame as pg
from block import *


class World:
    def __init__(self, path, game_width, game):
        self.game = game
        self.path = path
        loaded_image = pg.image.load(self.path)
        self.game_width = game_width
        self.background_width = round((DISPLAY_HEIGHT / loaded_image.get_height()) * loaded_image.get_width())
        self.repeat = game_width > self.background_width
        self.image = pg.transform.scale(loaded_image, (self.background_width, DISPLAY_HEIGHT))
        self.world_to_block_and_snd = dict()
        self.world_to_block_and_snd[0] = ('none', 'cave.ogg')
        self.world_to_block_and_snd[1] = ('forest_grass.png', 'forest.ogg')
        self.world_to_block_and_snd[2] = ('forest_grass.png', 'mountain.ogg')
        self.world_to_block_and_snd[3] = ('snow_grass.png', 'snow.ogg')
        self.world_to_block_and_snd[4] = ('none', 'boss.ogg')
        self.stage_pos_x = 0
        self.end_sign = EndSign(self.game)

    def load_blocks(self):
        return Block.create_all_blocks(self.game, self.world_to_block_and_snd[self.game.world_number][0])

    def load_world_music(self):
        return self.world_to_block_and_snd[self.game.world_number][1]

    def draw(self):
        rel_x = self.stage_pos_x % self.background_width
        self.game.screen.blit(self.image, (rel_x - self.background_width,0))
        if rel_x < DISPLAY_WIDTH:
            self.game.screen.blit(self.image, (rel_x, 0))


class EndSign(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.pos_in_game = vec(STAGE_WIDTH, DISPLAY_HEIGHT - BLOCK_HEIGHT)
        self.pos = vec(-500, DISPLAY_HEIGHT - BLOCK_HEIGHT)
        self.image = pg.image.load(IMG_PATH + 'signpost.png')
        self.image = pg.transform.scale(self.image, (SIGN_WIDTH, SIGN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos_in_game

    def update(self):
            self.pos.x = self.pos_in_game.x - self.game.player.pos.x
            self.rect.bottomleft = self.pos
