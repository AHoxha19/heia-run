# Sprite classes for platform game
import pygame as pg
import random
from settings import *
from game_manager import *
vec = pg.math.Vector2


class Monster(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        print("yes")
        self.image = pg.transform.scale(pg.image.load(IMG_MONSTER_PATH + 'bapst.png').convert(), (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
        if GameManager.world_number == BOSS_WORLD_NUMBER:
            self.rect.center = (STAGE_WIDTH, DISPLAY_HEIGHT / 2)
        self.pos = vec(-200, DISPLAY_HEIGHT / 2)
        self.pos_in_game = vec(random.randint(0, self.game.get_current_bg().game_width), DISPLAY_HEIGHT / 2)
        self.is_killed = False

    def update(self):
        if not GameManager.world_number == BOSS_WORLD_NUMBER:
            if not self.is_killed:
                self.pos_in_game -= (1, 0)
                self.pos.x = self.pos_in_game.x - self.game.player.pos.x
                self.rect.center = self.pos
            else:
                self.kill()    
            
    def kill_monster(self):
        self.pos_in_game.y = -100
        self.rect.center = self.pos_in_game
        self.is_killed = True