from settings import *
import pygame as pg


class World:
    def __init__(self, path, game_width):
        self.path = path
        loaded_image = pg.image.load(self.path).convert()
        self.game_width = game_width
        self.background_width = round((HEIGHT / loaded_image.get_height()) * loaded_image.get_width())
        self.repeat = game_width > self.background_width
        self.image = pg.transform.scale(loaded_image, (self.background_width, HEIGHT))
