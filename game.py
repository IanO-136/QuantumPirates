from tkinter.font import Font
import pygame
from pygame.locals import *
import time

#initialize pygame elements
pygame.init()

# Initialize pygame and create game window  
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pirate's Quantum Treasure")

# Load assets (player sprite, chests, map, font)  
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# Set up game variables (player position, timer, quiz status, chests)  
player = pygame.Rect((300,250,50,50))

quiz_stat = 8
chests = [
    pygame.Rect(300,250,50,50),
    pygame.Rect(300,250,50,50),
    pygame.Rect(300,250,50,50),
    pygame.Rect(300,250,50,50)
    ]
walls = [
    pygame.Rect(0, -50, SCREEN_WIDTH, 50),
    pygame.Rect(-50, 0, 50, SCREEN_HEIGHT),
    pygame.Rect(SCREEN_WIDTH, 0, 50, SCREEN_HEIGHT),
    pygame.Rect(0, SCREEN_HEIGHT, SCREEN_WIDTH, 50),
]

# Define chests with quantum questions & answers  
#file = fope


clock = pygame.time.Clock()

#FONT = pygame.font.Font("Copenhagen-z3Z0.ttf")
FONT = pygame.font.SysFont('Arial', 24)
timer_text = FONT.render("240", True, "black")
timer_text_rect = timer_text.get_rect(center=(SCREEN_WIDTH-40, SCREEN_HEIGHT-575))

start_time = 24000


def check_collision(rect, walls):
    """Checks if the given rectangle collides with any of the walls."""
    for wall in walls:
        if rect.colliderect(wall):
            return True
    return False

# WHILE game is running:
run = True
quiz_active = False

while run:
    screen.fill(WHITE)
    #bg_image = pygame.image.load('Background Info.png')
    #bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    timer_text = FONT.render(str((int) (start_time/100)), True, "black")
    screen.blit(timer_text, timer_text_rect)
#     Clear screen and draw background  
#     Draw player at current position  
    pygame.draw.rect(screen, (255, 0, 0), player)


#     Draw chests on the map  
    for chest in chests:
        pygame.draw.rect(screen, GOLD, chest)
#     Check for user input (WASD for movement)  
#     Check if player is interacting with a chest  
#     Update the timer  
#     Check win/loss conditions  
#     Refresh the screen  



# player movement system
    
    key = pygame.key.get_pressed()
    move_x, move_y = 0, 0
    if key[pygame.K_a]:  # Move left
        move_x = -1
    elif key[pygame.K_d]:  # Move right
        move_x = 1
    elif key[pygame.K_w]:  # Move up
        move_y = -1
    elif key[pygame.K_s]:  # Move down
        move_y = 1

    # Create a new rectangle for the player’s potential new position
    new_player_rect = player.move(move_x, move_y)

    # Check if the new position collides with any walls
    if not check_collision(new_player_rect, walls):
        # If no collision, update the player's position
        player.move_ip(move_x, move_y)

# Ensure player stays within map boundaries


# IF player collides with a chest:

#     Show pop-up with a Quantum Computing fact  
#     Display multiple-choice question (or textbox for input)  
#     IF user selects correct answer → give letter for final code  
#     IF wrong → subtract 10 seconds from timer  
#     Hide chest after answering  


# Start countdown from total game time  
# IF time reaches 0 → Game Over screen  
# Display timer at top-right of the screen  


# win condition
# IF user collects all code letters:
#     Show success message "Arrr Matey! You found the treasure!"  
#     End game 

    start_time -= 1

    if start_time <= 0:
        run = False

    clock.tick(100)


    #loop through each events one by one -- event handler
    for event in pygame.event.get():
        #exiting game (X at top)
        if event.type == pygame.QUIT:
            run = False

    #screen.blit(bg_image, (0, 0))
    pygame.display.update()


pygame.quit()
