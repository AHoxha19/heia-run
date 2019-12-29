# Sprite classes for platform game
import pygame as pg
import random
from settings import *
from game_manager import *
from boss_bullet import *
vec = pg.math.Vector2


class Monster(pg.sprite.Sprite):
    def __init__(self, game, is_boss):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.collision_with_player = False
        self.is_boss = is_boss
        if self.is_boss: 
            self.last_throw_time = 0
            self.boss_lifes = BOSS_LIFES
            self.image = pg.transform.scale(pg.image.load(IMG_MONSTER_PATH + 'bapst.png').convert(), (BOSS_WIDTH, BOSS_HEIGHT))
        else:
            self.image = pg.transform.scale(pg.image.load(IMG_MONSTER_PATH + 'bapst.png').convert(), (PLAYER_WIDTH, PLAYER_HEIGHT)) 
        self.rect = self.image.get_rect()

        if self.is_boss: 
             self.rect.bottomleft = (BOSS_POS_X_RIGHT, BOSS_POS_Y_RIGHT)
             self.pos = vec(BOSS_POS_X_RIGHT, BOSS_POS_Y_RIGHT)
        else:
            # if GameManager.world_number == BOSS_WORLD_NUMBER:
            #     self.rect.center = (STAGE_WIDTH, DISPLAY_HEIGHT / 2)
            # else: 
            self.rect.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
            self.pos = vec(-200, DISPLAY_HEIGHT / 2)
            self.pos_in_game = vec(random.randint(0, self.game.get_current_bg().game_width), DISPLAY_HEIGHT / 2)          
        self.is_killed = False

    def update(self):
        #not GameManager.world_number == BOSS_WORLD_NUMBER
        if not self.is_boss:
            if not self.is_killed:
                self.pos_in_game -= (1, 0)
                self.pos.x = self.pos_in_game.x - self.game.player.pos.x
                self.rect.center = self.pos
            else:
                self.kill()
        else:
            self.boss_throws()        
    def kill_monster(self):
        if self.is_boss:
            self.kill()
        else:
            self.pos_in_game.y = -100
            self.rect.center = self.pos_in_game
            self.is_killed = True

    def boss_update(self):
        self.boss_lifes-=1
        if self.boss_lifes == 0:
            self.kill_monster()
        if self.rect.x == BOSS_POS_X_RIGHT:
            self.bullet.kill()
            self.rect.x = BOSS_POS_X_LEFT
        else:
            self.bullet.kill()
            self.rect.x = BOSS_POS_X_RIGHT
        self.image = pg.transform.flip( self.image, True, False)
        
    def boss_throws(self):
        now = pg.time.get_ticks()
        if now - self.last_throw_time  > BOSS_TIME_THROW:
            self.last_throw_time = now
            self.bullet = BossBullet(self.game, self.game.player)
            if self.bullet.rect.x > DISPLAY_WIDTH or self.bullet.rect.x < 0:
                self.bullet.kill()  