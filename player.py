# Sprite classes for platform game
import pygame as pg
from settings import *
from game_manager import *
from player_bullet import *
from life import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        # sprites load
        self.crt_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frame
        self.rect = self.image.get_rect()
        self.rect.width = 10
        self.lifes = list()
        
        next_life_pos_x = 0
        for life in range(GameManager.number_of_lifes):
            self.lifes.append(Life(LIFE_POS_X + next_life_pos_x, LIFE_POS_Y))
            next_life_pos_x += 40
        self.number_of_lifes = GameManager.number_of_lifes
        self.rect.center = (DISPLAY_WIDTH / 2 - 100, DISPLAY_HEIGHT / 2)
        
    
        self.throws = False

        # position, velocity,acceleration and movement of the player
        self.pos = vec(DISPLAY_WIDTH / 2 - 100, DISPLAY_HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.walking = False
        self.player_center = self.rect.width / 2
        self.world = game.backgrounds[game.world_number]

    def remove_life(self):
        self.number_of_lifes -= 1
        self.lifes[self.number_of_lifes].kill()
        self.lifes.pop(self.number_of_lifes) 
        
        if self.number_of_lifes <= 1:
            self.game.playing = False 
            GameManager.reset = True

    def throw_bullet(self):
        if not self.throws: 
            self.bullet = PlayerBullet(self.game, self, self.game.is_boss_fight)
            self.throws = True
            self.game.bullet_snd.play()
    def get_image(self, path, img_name):
        return pg.transform.scale(pg.image.load(path + img_name).convert(), (PLAYER_WIDTH, PLAYER_HEIGHT))

    def load_images(self):
        self.standing_frame = self.get_image(IMG_PLAYER_PATH, 'asterix_0.gif')
        self.jump_frame_r = self.get_image(IMG_PLAYER_PATH, 'asterix_jump.gif')
        self.jump_frame_l = pg.transform.flip(self.jump_frame_r, True, False)
        self.walk_frame_r = [self.get_image(IMG_PLAYER_PATH, 'asterix_1.gif'),
                           self.get_image(IMG_PLAYER_PATH, 'asterix_2.gif'),
                           self.get_image(IMG_PLAYER_PATH, 'asterix_3.gif'),
                           self.get_image(IMG_PLAYER_PATH, 'asterix_4.gif')
                          ]
        self.walk_frame_l = []
        for frame in self.walk_frame_r:
            self.walk_frame_l.append(pg.transform.flip(frame, True, False))
        self.walk_len = len(self.walk_frame_r)

    def jump(self):
        if self.pos.y == DISPLAY_HEIGHT - BLOCK_HEIGHT and not self.jumping:
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
            self.game.jump_snd.play()

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -PLAYER_SMALL_JUMP:
                self.vel.y = -PLAYER_SMALL_JUMP


    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.jump()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        

        # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        
        # equations of motion
        self.vel += 0.5 * self.acc
        #fix so that the player stops
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel
        

        '''There is a display and a stage area
        the display area is what we see and the stage area is the scrolling background behind       
        '''
        if not GameManager.world_number == BOSS_WORLD_NUMBER:
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
        else:
            if self.pos.x > DISPLAY_WIDTH - self.player_center: self.pos.x = DISPLAY_WIDTH - self.player_center
            if self.pos.x < self.player_center: self.pos.x = self.player_center
            self.rect.midbottom = self.pos

    def animate(self):
            now = pg.time.get_ticks()
            if self.vel.x != 0 and not self.jumping:
                self.walking = True
            else:
                self.walking = False

            if self.jumping:

                if self.vel.x > 0:
                    self.image = self.jump_frame_r
                else:
                    self.image = self.jump_frame_l
                self.rect = self.image.get_rect()    

            #Walk animation
            if self.walking:
                if now - self.last_update > 200:
                    self.last_update = now
                    self.crt_frame = (self.crt_frame + 1) % self.walk_len
                    if self.vel.x > 0:
                        self.image = self.walk_frame_r[self.crt_frame]
                    else:
                        self.image = self.walk_frame_l[self.crt_frame]
                    self.rect = self.image.get_rect()
            if not self.jumping and not self.walking:
                self.image = self.standing_frame
                self.rect = self.image.get_rect()            

