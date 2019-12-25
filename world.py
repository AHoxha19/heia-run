from settings import *
import pygame as pg
from block import *


class World:
    def __init__(self, path, game_width):
        self.path = path
        loaded_image = pg.image.load(self.path)
        self.game_width = game_width
        self.background_width = round((DISPLAY_HEIGHT / loaded_image.get_height()) * loaded_image.get_width())
        self.repeat = game_width > self.background_width
        self.image = pg.transform.scale(loaded_image, (self.background_width, DISPLAY_HEIGHT))
        self.world_to_block = dict()
        self.world_to_block[0] = 'hole'
        self.world_to_block[1] = 'forest_grass.png'
        self.world_to_block[2] = 'forest_grass.png'
        self.world_to_block[3] = 'snow_grass.png'
        self.world_to_block[4] = 'hole'
        self.stage_pos_x = 0


    def load_blocks(self, game):
        return Block.create_all_blocks(game, self.world_to_block[game.world_number])
        

    def draw(self, game):
        rel_x = self.stage_pos_x % self.background_width
        game.screen.blit(self.image, (rel_x - self.background_width,0))
        if rel_x < DISPLAY_WIDTH:
            game.screen.blit(self.image, (rel_x, 0))