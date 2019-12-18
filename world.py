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

    def draw(self, game):
        if not self.repeat: # or not game.x_progression + WIDTH > self.background_width:
            game.screen.blit(self.image.subsurface(
                game.x_progression, 0, self.background_width - game.x_progression, HEIGHT), (0, 0))

        else:
            local_x = game.x_progression % self.background_width
            image_end = self.background_width - local_x
            game.screen.blit(self.image.subsurface(local_x, 0, image_end, HEIGHT), (0, 0))
            game.screen.blit(self.image.subsurface(0, 0, WIDTH, HEIGHT), (image_end, 0))
