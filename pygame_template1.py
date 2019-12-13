# Pygame template - skeleton for a new pygame project
import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30


#define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)



#initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("HEIA Run")
clock = pygame.time.Clock()

#Game loop
running = True

while running:
    #keep running at the right speed
    clock.tick(FPS)
    #Process input (events)
    for event in pygame.event.get():
        #Check for closing window
        if event.type == pygame.QUIT:
            running = False

    #Update


    #Render
    screen.fill(BLACK)
    # after we draw everything, flip the display
    #sample with whiteboard
    pygame.display.flip()
pygame.quit()

