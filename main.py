import random
from settings import *
import pygame as pg
from player import *
from monster import *
from world import *
from block import *


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        pg.display.set_mode((WIDTH, HEIGHT))
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.backgrounds = list()
        self.world_number = 3
        
        self.load_backgrounds()
        self.blocks = self.backgrounds[self.world_number].load_blocks(self)
        self.x_progression = 0

    def get_current_bg(self):
        return self.backgrounds[self.world_number]

    def load_backgrounds(self):
        self.backgrounds.append(World(path='img/bg/biblio.png', game_width=12920))
        self.backgrounds.append(World(path='img/bg/forest.png', game_width=12920))
        self.backgrounds.append(World(path='img/bg/mountain.png', game_width=12920))
        self.backgrounds.append(World(path='img/bg/snow.png', game_width=12920))
        self.backgrounds.append(World(path='img/bg/city.png', game_width=12920))

    def draw_background(self):
        self.backgrounds[self.world_number].draw(self)

    def new(self):
        # starts a new game
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)
        self.monsters = [Monster(self) for x in range(10)]
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.monsters)
        for block in self.blocks:
            if not block.isHole:
                self.all_sprites.add(block)
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
        self.draw_background()
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
