# Pygame template - skeleton for a new pygame project
import pygame
from settings import*
import os


#set up assets folders

game_folder = os.path.dirname("./")
img_folder = os.path.join(game_folder, "img")

class Player(pygame.sprite.Sprite):
    #sprite for the Player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "player-1.gif")).convert()
    #pygame.Surface((50,50))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.rect.x += 5
        if(self.rect.x > WIDTH):
            self.rect.right = 0

#initialize pygame and create window

all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
player = Player()
all_sprites.add(player)
#Game loop
running = True

while running:
    #keep running at the right speed
    clock.tick(FPS)
    #Process input (events)
    

    #Update
    
    #Render
    
pygame.quit()

