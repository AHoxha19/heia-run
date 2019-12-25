# Sprite classes for platform game
import pygame as pg
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (0, DISPLAY_HEIGHT - BLOCK_HEIGHT)
        self.pos = vec(0, DISPLAY_HEIGHT - BLOCK_HEIGHT)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.player_center = self.rect.width / 2
        self.world = game.backgrounds[game.world_number]


    def jump(self):
        if self.pos.y == DISPLAY_HEIGHT - BLOCK_HEIGHT and not self.jumping:
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -PLAYER_SMALL_JUMP:
                self.vel.y = -PLAYER_SMALL_JUMP


    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_UP]:
            self.jump()

        # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        
        # equations of motion
        self.vel += 0.5 * self.acc

        self.pos += self.vel
        

        '''There is a display and a stage area
        the display area is what we see and the stage area is the scrolling background behind       
        '''

        # if the player reaches the end of the stage
        if self.pos.x >STAGE_WIDTH - self.player_center: self.pos.x = STAGE_WIDTH - self.player_center
        # if the player goes to the beginning of the stage
        if self.pos.x < self.player_center: self.pos.x = self.player_center

        # if the player has not reached the middle of the display area
        if self.pos.x < START_SCROLL_X: 
            self.game.x_progression =  self.pos.x 
        # if the player has reached the end of the stage and we don't need to scroll anymore    
        elif self.pos.x > STAGE_WIDTH - START_SCROLL_X: 
            self.game.x_progression = self.pos.x - STAGE_WIDTH + DISPLAY_WIDTH
        # if the player is in the middle, so not at the end or the beginning of the stage
        else:
            self.game.x_progression = START_SCROLL_X
            self.world.stage_pos_x += -self.vel.x
          
        self.rect.midbottom = vec(self.game.x_progression, self.pos.y)
