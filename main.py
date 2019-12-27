import random
from game_manager import *
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
        self.load_sounds_effect()
        self.screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.backgrounds = list()
        self.end_level = list()
        self.world_number = GameManager.world_number
        self.x_progression = 0
        self.load_backgrounds()
        self.end_level.append(self.backgrounds[self.world_number].end_sign)
        self.blocks = self.backgrounds[self.world_number].load_blocks()
        self.music = self.backgrounds[self.world_number].load_world_music()
        pg.mixer.music.load(SND_PATH + self.music)
        
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(0.3)
        

    def load_sounds_effect(self):
        self.jump_snd = pg.mixer.Sound(SND_PATH + "jump.wav")
        self.bullet_snd = pg.mixer.Sound(SND_PATH + "bullet.wav")
        self.hit_snd = pg.mixer.Sound(SND_PATH + "hit.ogg")

    def get_current_bg(self):
        return self.backgrounds[self.world_number]

    def load_backgrounds(self):
        self.backgrounds.append(World(path='img/bg/biblio.png', game_width=STAGE_WIDTH, game=self))
        self.backgrounds.append(World(path='img/bg/forest.png', game_width=STAGE_WIDTH, game=self))
        self.backgrounds.append(World(path='img/bg/mountain.png', game_width=STAGE_WIDTH, game=self))
        self.backgrounds.append(World(path='img/bg/snow.png', game_width=STAGE_WIDTH, game=self))
        self.backgrounds.append(World(path='img/bg/city.png', game_width=STAGE_WIDTH, game=self))

    def draw_background(self):
        self.backgrounds[self.world_number].draw()

    def new(self):
        # starts a new game
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)
        self.monsters = pg.sprite.Group()
        for i in range(10):
            monster = Monster(self)
            self.all_sprites.add(monster)
            self.monsters.add(monster)
        [Monster(self) for x in range(10)]
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.monsters)
        self.all_sprites.add(self.backgrounds[self.world_number].end_sign)
        self.all_sprites.add(self.player.lifes)
        for block in self.blocks:
            if not block.isHole:
                self.all_sprites.add(block)
        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
                   

    def update(self):
        # Game loop - update
        self.all_sprites.update()
        hits=pg.sprite.spritecollide(self.player, self.blocks, False)
        next_level = pg.sprite.spritecollide(self.player, self.end_level, False)
        player_monster_coll = pg.sprite.spritecollide(self.player, self.monsters, True)
        if next_level:
            self.playing = False
            GameManager.next_level = True
            GameManager.reset = True
        if hits:
          self.player.pos.y = DISPLAY_HEIGHT - BLOCK_HEIGHT
          self.player.vel.y = 0
          self.player.jumping = False
        if player_monster_coll:
                self.hit_snd.play()
                self.player.number_of_lifes -= 1
                self.player.lifes[self.player.number_of_lifes].kill()
                self.player.lifes.pop(self.player.number_of_lifes) 
                if self.player.number_of_lifes <= 1:
                    self.playing = False 
                    GameManager.reset = True
            

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
                GameManager.reset = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
                if event.key == pg.K_SPACE:
                    self.player.throw_bullet()    
            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.player.jump_cut()
             

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

    def show_test_stats(self):
        font = pg.font.Font('freesansbold.ttf', 20) 
        acc_text = font.render("acc: - x: " + str(round(self.player.acc.x, 2)) + " ; y: " + str(round(self.player.acc.y, 2)) , True, WHITE, BLACK)
        acc_text_rect = acc_text.get_rect()
        acc_text_rect.topleft = (0, 0)
        vel_text = font.render("vel - x: " + str(round(self.player.vel.x, 2)) + " ; y: " + str(round(self.player.vel.y, 2)), True, WHITE, BLACK)
        vel_text_rect = vel_text.get_rect()
        vel_text_rect.topleft = (0, 20)
        fps_text = font.render('FPS: '+ str(round(self.clock.get_fps(), 2)), True, WHITE, BLACK)
        fps_text_rect = fps_text.get_rect()
        fps_text_rect.topleft = (0, 40)
        xprog_text = font.render('xprog: '+ str(round(self.x_progression, 2)), True, WHITE, BLACK)
        xprog_text_rect = fps_text.get_rect()
        xprog_text_rect.topleft = (0, 60)
        player_pos_x_text = font.render('playerX: '+ str(round(self.player.pos.x, 2)), True, WHITE, BLACK)
        player_pos_x_text_rect = fps_text.get_rect()
        player_pos_x_text_rect.topleft = (0, 80)
        stagew_text = font.render('STAGEW: '+ str(round(STAGE_WIDTH, 2)), True, WHITE, BLACK)
        stagew_text_rect = fps_text.get_rect()
        stagew_text_rect.topleft = (0, 100)
        displayw_text = font.render('DISPLAYW: '+ str(round(DISPLAY_WIDTH, 2)), True, WHITE, BLACK)
        displayw_text_rect = fps_text.get_rect()
        displayw_text_rect.topleft = (0, 120)
        self.screen.blit(acc_text, acc_text_rect)
        self.screen.blit(vel_text, vel_text_rect)
        self.screen.blit(fps_text, fps_text_rect)
        self.screen.blit(xprog_text, xprog_text_rect)
        self.screen.blit(player_pos_x_text, player_pos_x_text_rect)
        self.screen.blit(stagew_text, stagew_text_rect)
        self.screen.blit(displayw_text, displayw_text_rect)

game = Game()
game.show_menu_title()
while game.running:
    game.new()
    game.run()
    if GameManager.next_level:
        GameManager.world_number+=1
    if GameManager.reset:
        GameManager.next_level = False
        game = Game()
    game.show_go_screen()

pg.quit()
