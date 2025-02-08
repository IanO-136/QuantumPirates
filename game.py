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
BROWN = (150, 75, 0)

start_time = 24000
clock = pygame.time.Clock()

#FONT = pygame.font.Font("Copenhagen-z3Z0.ttf")
FONT = pygame.font.SysFont('Arial', 24)
timer_text = FONT.render("240", True, "black")
timer_text_rect = timer_text.get_rect(center=(SCREEN_WIDTH-40, SCREEN_HEIGHT-575))

def show_start_screen():
    screen.fill(white)
    draw_text("🏴‍☠️ Pirate's Quantum Treasure 🏴‍☠️", 150, 200, BIG_FONT)
    draw_text("Press ENTER to Begin!", 250, 300)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False  # Start the game when enter is pressed

# Game Over Screen
def display_game_over_screen():
    screen.fill(WHITE)
    draw_text("💀 Game Over! Time's up! 💀", 200, 250, BIG_FONT)
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    exit()

# Win Screen
def display_win_screen():
    screen.fill(WHITE)
    draw_text("🏆 Arrr Matey! You found all the treasure! 🏆", 150, 250, BIG_FONT)
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
    exit()

used
#background = pygame.image.load("background.png")  # Replace with your actual image file
#background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#correct_img = pygame.image.load("correct.png")  # Image shown when the answer is correct
#incorrect_img = pygame.image.load("incorrect.png")  # Image for incorrect answers

# Set up game variables (player position, timer, quiz status, chests)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self)s
        #self.images = []
        #for i in range(1, 5):
            #img = pygame.image.load('Pirate.png')
            #self.images.append(img)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Pirate4.png").convert_alpha()  # Load and optimize sprite
        self.image = pygame.transform.scale(self.image, (50, 50))  # Scale image to smaller size
        self.rect = self.image.get_rect(center=(300, 250))  # Position player at (300,250)
        
    def move(self, dx, dy, walls):
        if dx or dy:  # Only move if there's an input
            new_player_rect = self.rect.move(dx * 5, dy * 5)
            if not check_collision(new_player_rect, walls):
                self.rect = new_player_rect  # Update position only if no collision
                return new_player_rect  # Always return the updated rect
        return self.rect  # If no movement, return the current rect

#player = pygame.Rect((300,250,50,50))
player = Player()

CHEST_SIZE = 50
big_chests = [
    pygame.Rect(100, 100, CHEST_SIZE, CHEST_SIZE),
    pygame.Rect(500, 200, CHEST_SIZE, CHEST_SIZE),
    pygame.Rect(300, 400, CHEST_SIZE, CHEST_SIZE),
    pygame.Rect(700, 500, CHEST_SIZE, CHEST_SIZE)
]


class Chest(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("treasure chest.png").convert_alpha()
        self.image = pygame.trans

SMALL_CHEST_SIZE = 30
small_chests = [
    pygame.Rect(120, 150, SMALL_CHEST_SIZE, SMALL_CHEST_SIZE ),
    pygame.Rect(600, 180, SMALL_CHEST_SIZE, SMALL_CHEST_SIZE),
    pygame.Rect(300, 400, SMALL_CHEST_SIZE, SMALL_CHEST_SIZE),
    pygame.Rect(700, 530, SMALL_CHEST_SIZE, SMALL_CHEST_SIZE)
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

small_chest_facts = [
    "Quantum superposition is the ability of a quantum system to act as if it is in multiple states at the same time until it is measured. Superposition is a property of all wave functions.",
    "A qubit, or quantum bit, is the basic unit of information in quantum computing.",
    "Quantum entanglement connects particles over vast distances instantaneously.",
    "Quantum computers use probability rather than certainty to make calculations."
]
quiz_stat = 8

#func to display quiz
def display_quiz(screen, question_data, start_time):
    screen.fill(WHITE)  # Clear screen
    FONT = pygame.font.SysFont('Arial', 24)
    #timer_text_rect = timer_text.get_rect(center=(SCREEN_WIDTH-40, SCREEN_HEIGHT-575))
    timer_text_rect = pygame.Rect(SCREEN_WIDTH-40, SCREEN_HEIGHT-575, 50, 30)
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
        timer_text = FONT.render(str((int) (start_time/100)), True, "black")
        screen.blit(timer_text, timer_text_rect)
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
                            return [-1000, start_time]  # Subtract 10 seconds
                        return [0, start_time]  # Correct answer
        start_time -= 1

        if start_time <= 0:
            display_end_screen()

        pygame.display.update()
            
        clock.tick(100)

# Define chests with quantum questions & answers  
#file = fope




def check_collision(rect, walls):
    """Checks if the given rectangle collides with any of the walls."""
    for wall in walls:
        if player.rect.colliderect(chest):
            return True
    return False

# WHILE game is running:
run = True
quiz_active = False
current_question = None
button_rects = []
fact_active = False

while run:
    screen.fill(WHITE)
    game_background = pygame.image.load('game_background.png')
    game_background = pygame.transform.scale(game_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(game_background, (0, 0))
    pygame.display.update()


    timer_text = FONT.render(str((int) (start_time/100)), True, "black")
    screen.blit(timer_text, timer_text_rect)
#     Clear screen and draw background  
#     Draw player at current position
    screen.blit(player.image, player.rect)
    #pygame.draw.rect(screen, (255, 0, 0), player)


#     Draw chests on the map  
    for chest in big_chests:
        pygame.draw.rect(screen, GOLD, chest)

#       Draw small chests
    for chest in small_chests:
        pygame.draw.rect(screen, BROWN, chest)
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
    new_player_rect = player.move(move_x, move_y, walls)

    # Check if the new position collides with any walls
    if not check_collision(new_player_rect, walls):
        # If no collision, update the player's position
        #player.move_ip(move_x, move_y)
        player.move(move_x, move_y, walls)

# Ensure player stays within map boundaries
    # IF player collides with a chest:
    for i, chest in enumerate(big_chests[:]):
        if player.rect.colliderect(chest):
            print(f"Collided with chest {i+1}! Displaying quiz...")
            big_chests.pop(i)  # Remove chest after collision
            current_question = quiz_questions[i % len(quiz_questions)]
            quiz_active = True
            button_array = display_quiz(screen, current_question, start_time)
            button_rects = button_array[0]
            start_time = button_array[1] + button_array[0]
            break  # Prevent iterating over modified listxs
        # Check for win condition

        # Check collisions with small chests (Show Fact)
        if not fact_active:
            for i, chest in enumerate(small_chests[:]):
                if player.rect.colliderect(chest):
                    fact_text = small_chest_facts[i]
                    fact_active = True
                    small_chests.pop(i)  # Remove small chest after reading fact
                    break

    if len(big_chests) == 0 and not quiz_active:
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

#     Show success message "Arrr Matey! You found the treasure!"  
#     End game 

    start_time -= 1

    if start_time <= 0:
        display_win_screen()
        

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
