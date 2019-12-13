import random
from settings import *
import pygame as pg
from player import *


class Game:

    def __init__(self):
        pg.init()
        pg.mixer.init()
        pg.display.set_mode((WIDTH, HEIGHT))
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

        self.backgrounds = dict()
        self.load_backgrounds()

    def load_backgrounds(self):
        self.backgrounds['bg1'] = pg.transform.scale(pg.image.load('img/bg1.png'), (11900, 460))

    def draw_background(self, background_name):
        self.screen.blit(self.backgrounds[background_name], (0, 0))

    def new(self):
        # starts a new game
        self.all_sprites = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game loop - update
        self.all_sprites.update()

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False

    def draw(self):
        # Game loop - draw
        self.draw_background('bg1')
        self.all_sprites.draw(self.screen)
        # after we draw everything, flip the display
        # sample with whiteboard
        pg.display.flip()

    def show_menu_title(self):
        pass

    def show_go_screen(self):
        pass


game = Game()
game.show_menu_title()
while game.running:
    game.new()
    game.run()
    game.show_go_screen()

pg.quit()
