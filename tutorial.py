import pygame
from pygame.locals import *

#initialize pygame elements
pygame.init()

#create scren
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#display screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#making player obj
#takes 4 args -- X, Y coords, wdith, height
player = pygame.Rect((300,250,50,50))


#keeps gaming window open and running -- game loop
run = True
while run:

    screen.fill((0,0,0))

    #screen, RGB, obj
    pygame.draw.rect(screen, (255, 0, 0), player)

    key = pygame.key.get_pressed()
    #a key is pressed (move to left)
    if key[pygame.K_a] == True:
        player.move_ip(-1, 0)
    #d key is pressed (move to right)
    elif key[pygame.K_d] == True:
        player.move_ip(1, 0)
    #w is pressed (move up)
    elif key[pygame.K_w] == True:
        player.move_ip(0, -1)
    #s is pressed (move down)
    elif key[pygame.K_s] == True:
        player.move_ip(0, 1)


    #loop through each events one by one -- event handler
    for event in pygame.event.get():
        #exiting game (X at top)
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


#quit pygame
pygame.quit()


# Notes from Tutorial
'''
Basic Structure:
1. Window
    - dimensions (w,h)
2. Game loop
    - keeps window running
3. Event handler
    - constantly looks for events (ex. mouse clicks)
'''
