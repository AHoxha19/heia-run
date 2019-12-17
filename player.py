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
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc += self.vel * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc

        new_pos = self.vel + 0.5 * self.acc
        new_game_progression = self.game.x_progression + new_pos.x

        if 0 < new_game_progression < BACKGROUND_WIDTH - WIDTH and -MID_TOL < self.pos.x - WIDTH/2 < MID_TOL:
            self.game.x_progression += new_pos.x
        else:
            new_pos = self.vel + 0.5 * self.acc
            if 0 < (self.pos + new_pos).x < WIDTH:
                self.pos += new_pos

        self.rect.center = self.pos
