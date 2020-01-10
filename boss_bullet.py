import pygame as pg
from bullet import Bullet
from settings import *

class BossBullet(Bullet):
    def __init__(self, game, player):
        Bullet.__init__(self, game, player)
        self.image = pg.image.load(IMG_BULLET_PATH + 'heia.png').convert()
        self.image = pg.transform.scale(self.image, (BOSS_BULLET_WIDTH, BOSS_BULLET_HEIGHT))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.game.all_sprites.add(self)
        if self.game.monster.rect.x < DISPLAY_WIDTH // 2:
            self.rect.center = (self.game.monster.rect.x + FINAL_BOSS_WIDTH, self.game.monster.rect.y + BOSS_BULLET_DOWN)
        else:
            self.rect.center = (self.game.monster.rect.x, self.game.monster.rect.y + BOSS_BULLET_DOWN)

    def move_boss_bullet(self):
        self.collision_boss_with_player = pg.sprite.collide_rect(self, self.game.player)
        if self.collision_boss_with_player:
            self.destroy_bullet()
            self.player.remove_life()
        if self.game.monster.rect.x == BOSS_POS_X_LEFT:
            self.rect.x += BOSS_BULLET_SPEED
        else:
            self.rect.x -= BOSS_BULLET_SPEED
        if self.rect.x > DISPLAY_WIDTH or self.rect.x < 0:
            self.destroy_bullet()

    def update(self):
        self.move_boss_bullet()

    def destroy_bullet(self):
        self.kill()
