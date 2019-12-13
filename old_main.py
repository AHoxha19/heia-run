import pygame, sys, glob

pygame.init()
pygame.display.set_caption("Test game")

W = 800
H = 600

screen = pygame.display.set_mode((W,H))
clock = pygame.time.Clock()


class Player:
    def __init__(self):
        self.x = 200
        self.y = 300
        self.speed_init = 10
        self.speed = self.speed_init
        self.animation = glob.glob("./player/*.gif")
        self.animation.sort()
        self.animation_pos = 0
        self.animation_max = len(self.animation) -1
        self.img = pygame.image.load(self.animation[0])
        self.update(0)
    def update(self, pos):
        if pos != 0:
            self.speed -= 1
            self.x += pos
            if self.speed == 0:
                self.img = pygame.image.load(self.animation[self.animation_pos])
                self.speed = self.speed_init
                if self.animation_pos == self.animation_max:
                    self.animation_pos = 0
                else:
                    self.animation_pos +=1
        screen.blit(self.img, (self.x, self.y))
    def jump(self, pos):
        if pos != 0:
            self.y += pos




player = Player()
pos = 0
jump_pos = 0

crashed = False

while not crashed:
    screen.fill((0,0,0))
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            pos+=5
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            pos = 0
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            pos-=5
        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            pos = 0
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            jump_pos -= 5
    player.update(pos)
    player.jump(jump_pos)
    pygame.display.update()
pygame.quit()