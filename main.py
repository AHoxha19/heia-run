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
        self.is_boss_fight = GameManager.world_number == BOSS_WORLD_NUMBER
        self.x_progression = 0
        self.congratulations_screen = False
        self.load_backgrounds()
        self.end_level.append(self.backgrounds[self.world_number].end_sign)
        self.blocks = self.backgrounds[self.world_number].load_blocks()
        self.is_main_menu = False
        GameManager.save_game()


    def play_music(self, music_name):
        pg.mixer.music.load(SND_PATH + music_name)
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(0.3)


    def load_sounds_effect(self):
        self.jump_snd = pg.mixer.Sound(SND_PATH + "jump.wav")
        self.bullet_snd = pg.mixer.Sound(SND_PATH + "bullet.wav")
        self.hit_snd = pg.mixer.Sound(SND_PATH + "hit.ogg")
        self.menu_move = pg.mixer.Sound(SND_PATH + 'menu_move.ogg')

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
        if not GameManager.mute:
            self.music = self.backgrounds[self.world_number].load_world_music()
            self.play_music(self.music)
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)
        self.monsters = pg.sprite.Group()
        if self.is_boss_fight:
            self.monster = Monster(self, self.is_boss_fight)
            self.all_sprites.add(self.monster)
            self.monsters.add(self.monster)
        else:
            for i in range(NB_OF_MONSTERS):
                monster = Monster(self, self.is_boss_fight)
                self.all_sprites.add(monster)
                self.monsters.add(monster)
        self.all_sprites.add(self.player)
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

        #if the player falls in a hole
        if self.player.pos.y > PLAYER_HOLE_KILL:
            self.playing = False
            GameManager.reset = True

        if self.congratulations_screen:
            self.playing = False
            GameManager.next_level = True
            GameManager.reset = True

        block_hit=pg.sprite.spritecollide(self.player, self.blocks, False)
        next_level = pg.sprite.spritecollide(self.player, self.end_level, False)
        player_monster_coll = pg.sprite.spritecollide(self.player, self.monsters, not self.is_boss_fight)
        if next_level:
            self.playing = False
            GameManager.next_level = True
            GameManager.reset = True
        if block_hit:
          self.player.pos.y = DISPLAY_HEIGHT - BLOCK_HEIGHT
          self.player.vel.y = 0
          self.player.jumping = False
        if player_monster_coll:
                if not GameManager.mute:
                    self.hit_snd.play()
                if self.is_boss_fight:
                    player_monster_coll[0].boss_update()
                else:
                    self.player.remove_life()

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

    def draw_congratulations_screen(self):
        self.congratulations_screen = True
        pg.draw.rect(self.screen, BLACK, pg.Rect(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT))
        font = pg.font.Font('freesansbold.ttf', 32)
        initial_y = (DISPLAY_HEIGHT // 2) - 20

        for message in [CONGRATULATIONS_TEXT, CONGRATULATIONS_INFO]:
            text = font.render(message, True, WHITE, BLACK)
            textRect = text.get_rect()
            textRect.center = (DISPLAY_WIDTH // 2, initial_y)
            self.screen.blit(text, textRect)
            initial_y += 40 # space between texts

    def draw(self):
        # Game loop - draw

        self.draw_background()
        self.all_sprites.draw(self.screen)
        # after we draw everything, flip the display
        # sample with whiteboard
        pg.display.flip()

    def select_circle(self):
        circle = pg.image.load(IMG_PATH + 'circle_selection.png')
        circle = pg.transform.scale(circle, (73, 54))
        return circle

    def select_rect(self):
        rect = pg.image.load(IMG_PATH + 'rect_selection.png')
        rect = pg.transform.scale(rect, (270, 60))
        return rect

    def sound_img_toggle(self, is_sound_on):
        if is_sound_on:
            return pg.transform.scale(pg.image.load(IMG_PATH + 'sound_mute.png').convert(), SND_IMG_SIZE)
        return pg.transform.scale(pg.image.load(IMG_PATH + 'sound_on.gif').convert(), SND_IMG_SIZE)

    def show_menu_title(self):
        self.music = 'main_menu.ogg'
        self.play_music(self.music)
        main_menu_image = pg.image.load(IMG_PATH + 'main_menu_bg.png').convert()
        main_menu_image = pg.transform.scale( main_menu_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        is_sound_on = True
        sound_img = pg.image.load(IMG_PATH + 'sound_on.gif').convert()
        sound_img = pg.transform.scale(sound_img, SND_IMG_SIZE)
        select = self.select_rect()

        select_pos = NEW_GAME_POS

        click = False
        while not click:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    click = True
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        ##Press up key
                        if select_pos == NEW_GAME_POS:
                            select = self.select_circle()
                            select_pos = SOUND_MUTE_POS
                        elif select_pos == LOAD_GAME_POS:
                            select_pos = NEW_GAME_POS
                        elif select_pos == SOUND_MUTE_POS:
                            select = self.select_rect()
                            select_pos = LOAD_GAME_POS
                        if not GameManager.mute: self.menu_move.play()
                    if event.key == pg.K_DOWN:
                        #Press down key
                        if select_pos == NEW_GAME_POS:
                            select_pos = LOAD_GAME_POS
                        elif select_pos == LOAD_GAME_POS:
                            select = self.select_circle()
                            select_pos = SOUND_MUTE_POS
                        elif select_pos == SOUND_MUTE_POS:
                            select = self.select_rect()
                            select_pos = NEW_GAME_POS
                        if not GameManager.mute: self.menu_move.play()

                    if event.key == pg.K_SPACE:
                        self.congratulations_screen = False

                    if event.key == pg.K_RETURN:
                        if select_pos == NEW_GAME_POS:
                            GameManager.world_number = 0
                            click = True
                        elif select_pos == LOAD_GAME_POS:
                            GameManager.load_game()
                            click = True
                        elif select_pos == SOUND_MUTE_POS:
                            sound_img = self.sound_img_toggle(is_sound_on)
                            is_sound_on = not is_sound_on
                            if not is_sound_on:
                                pg.mixer.music.stop()
                                GameManager.mute = True
                            else:
                                self.play_music('main_menu.ogg')
                                GameManager.mute = False

            if self.congratulations_screen:
                self.draw_congratulations_screen()
            else:
                self.screen.blit(main_menu_image, (0,0))
                self.screen.blit(sound_img, (DISPLAY_WIDTH /2 -50, DISPLAY_HEIGHT /2 +140))
                self.screen.blit(select, select_pos)
            pg.display.update()

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
        player_pos_x_text = font.render('playerY: '+ str(round(self.player.pos.y, 2)), True, WHITE, BLACK)
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


GameManager.load_game()
game = Game()
game.show_menu_title()

while game.running:
    game.new()
    game.run()
    if GameManager.next_level:
        if game.congratulations_screen:
            GameManager.load_game()
            game.show_menu_title()
        else:
            GameManager.world_number += 1
    if GameManager.reset:
        GameManager.next_level = False
        game = Game()

pg.quit()
