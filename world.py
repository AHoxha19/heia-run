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
        self.world_to_block_and_snd = dict()
        self.world_to_block_and_snd[0] = ('hole', 'cave.ogg')
        self.world_to_block_and_snd[1] = ('forest_grass.png', 'forest.mp3')
        self.world_to_block_and_snd[2] = ('forest_grass.png', 'mountain.wav')
        self.world_to_block_and_snd[3] = ('snow_grass.png', 'snow.ogg')
        self.world_to_block_and_snd[4] = ('hole', 'boss.wav')
        self.stage_pos_x = 0
        


    def load_blocks(self, game):
        return Block.create_all_blocks(game, self.world_to_block_and_snd[game.world_number][0])
        
    def load_world_music(self, game):
        return self.world_to_block_and_snd[game.world_number][1]

    def draw(self, game):
        rel_x = self.stage_pos_x % self.background_width
        game.screen.blit(self.image, (rel_x - self.background_width,0))
        if rel_x < DISPLAY_WIDTH:
            game.screen.blit(self.image, (rel_x, 0))