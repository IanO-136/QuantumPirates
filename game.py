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

#pictures to be used
#background = pygame.image.load("background.png")  # Replace with your actual image file
#background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#correct_img = pygame.image.load("correct.png")  # Image shown when the answer is correct
#incorrect_img = pygame.image.load("incorrect.png")  # Image for incorrect answers

# Set up game variables (player position, timer, quiz status, chests)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Pirate.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,5)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
#player = pygame.Rect((300,250,50,50))
player = Player()

CHEST_SIZE = 50
chests = [
    pygame.Rect(100, 100, CHEST_SIZE, CHEST_SIZE),
    pygame.Rect(500, 200, CHEST_SIZE, CHEST_SIZE),
    pygame.Rect(300, 400, CHEST_SIZE, CHEST_SIZE),
    pygame.Rect(700, 500, CHEST_SIZE, CHEST_SIZE)
]


walls = [
    pygame.Rect(0, -50, SCREEN_WIDTH, 50),
    pygame.Rect(-50, 0, 50, SCREEN_HEIGHT),
    pygame.Rect(SCREEN_WIDTH, 0, 50, SCREEN_HEIGHT),
    pygame.Rect(0, SCREEN_HEIGHT, SCREEN_WIDTH, 50),
]

quiz_questions = [
    {"question": "What is superposition in quantum computing?", 
     "options": ["A state of uncertainty", "A pirate maneuver", "A shipwreck"],
     "answer": "A state of uncertainty"},
    
    {"question": "What is the name of the quantum principle that prevents copying qubits?", 
     "options": ["The No-Clone Theorem", "Schrödinger’s Cat", "Quantum Booty"],
     "answer": "The No-Clone Theorem"}
]

quiz_stat = 8

#func to display quiz
def display_quiz(screen, question_data):
    screen.fill(WHITE)  # Clear screen
    question_text = FONT.render(question_data["question"], True, "black")
    screen.blit(question_text, (50, 100))

    button_rects = []
    y_offset = 200
    for option in question_data["options"]:
        button_rect = pygame.Rect(50, y_offset, 300, 50)
        pygame.draw.rect(screen, (0, 128, 255), button_rect)
        text = FONT.render(option, True, "white")
        screen.blit(text, (60, y_offset + 10))
        button_rects.append((button_rect, option))
        y_offset += 70

    pygame.display.update()
    
    # Wait for user to pick answer
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, option in button_rects:
                    if button.collidepoint(event.pos):
                        if option == question_data["answer"]:
                            print("Yarrr! Right on, pirate!")
                        else:
                            print("Arrrr, that's incorrect!")
                            return -1000  # Subtract 10 seconds
                        return 0  # Correct answer

# Define chests with quantum questions & answers  
#file = fope

def display_end_screen():
    screen.fill(WHITE)  # Clear screen
    background = pygame.image.load("endscreen_failed.png")  # Replace with your actual image file
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background, (0, 0))
    pygame.display.update()
    while True:
        print("end")


    

clock = pygame.time.Clock()

#FONT = pygame.font.Font("Copenhagen-z3Z0.ttf")
FONT = pygame.font.SysFont('Arial', 24)
timer_text = FONT.render("240", True, "black")
timer_text_rect = timer_text.get_rect(center=(SCREEN_WIDTH-40, SCREEN_HEIGHT-575))

start_time = 2400


def check_collision(rect, walls):
    """Checks if the given rectangle collides with any of the walls."""
    for wall in walls:
        if rect.colliderect(wall):
            return True
    return False

# WHILE game is running:
run = True
quiz_active = False
current_question = None
button_rects = []

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

# Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    #player movement
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
    for i, chest in enumerate(chests):
        if player.colliderect(chest):
            print(f"Collided with chest {i+1}! Displaying quiz...")
            chests.pop(i)  # Remove chest after collision
            current_question = quiz_questions[i % len(quiz_questions)]
            quiz_active = True
            button_rects = display_quiz(screen, current_question)
            break  # Prevent iterating over modified list
    # Check for win condition


    if len(chests) == 0:
        print("Arrr Matey! You found all the treasure!")
        run = False

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
        display_end_screen()
        

    #clock.tick(100)


    #loop through each events one by one -- event handler
    #for event in pygame.event.get():
        #exiting game (X at top)
        #if event.type == pygame.QUIT:
            #run = False

    #screen.blit(bg_image, (0, 0))
    pygame.display.update()
    clock.tick(100)


pygame.quit()
