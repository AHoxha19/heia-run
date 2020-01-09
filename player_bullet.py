import pygame as pg
from bullet import Bullet
from settings import *

class PlayerBullet(Bullet):
    def __init__(self, game, player, is_boss_fight):
        Bullet.__init__(self, game, player, is_boss_fight)
        self.game = game
        self.player = player
        self.is_boss_fight = is_boss_fight
        self.last_player_vel_x = self.player.vel.x
        self.image = pg.image.load(IMG_BULLET_PATH + 'bullet.gif').convert()
        self.image = pg.transform.scale(self.image, (BULLET_WIDTH, BULLET_HEIGHT))
        self.rect = self.image.get_rect()
        self.game.all_sprites.add(self)
        self.rect.center = self.player.rect.center

    def move_bullet(self):
        self.collision_player_with_monster = pg.sprite.spritecollide(self, self.game.monsters, False)
        if not self.collision_player_with_monster and (self.rect.x < DISPLAY_WIDTH and self.rect.x > 0):
            if self.last_player_vel_x < 0:
                    self.rect.x -= BULLET_SPEED
            else:
                self.rect.x += BULLET_SPEED
        else:
            self.destroy_bullet()

    def update(self):
        if self.player.throws:
            self.move_bullet()

    def destroy_bullet(self):
        self.player.throws = False
        if self.collision_player_with_monster:
            if self.is_boss_fight:
                self.game.monster.boss_lifes -= 1
                if self.game.monster.boss_lifes == 0:
                     self.collision_player_with_monster[0].kill_monster()
                     self.game.congratulations_screen = True
            else:
                 self.collision_player_with_monster[0].kill_monster()
        self.kill()
